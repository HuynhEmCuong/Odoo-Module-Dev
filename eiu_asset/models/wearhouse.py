
from odoo import api, fields, models, _,tools, SUPERUSER_ID
from odoo.exceptions import AccessError,ValidationError
from lxml import etree
from odoo.tools.float_utils import float_compare, float_is_zero, float_round

class AssetWearhouse(models.Model):
    _name = 'asset.wearhouse'
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _description ="Asset wearhouse"
    _rec_name ="reference"

    
    #### properties
    reference  = fields.Char(string="Mã phiếu", required=True, copy=False, readonly=True,
                            default=lambda self: _('New'))
    current_user = fields.Many2one('res.users','Người Tạo', default=lambda self: self.env.user,readonly=True )

    date_wearhouse = fields.Datetime(string="Ngày xuất kho",
    default=fields.Datetime.now)

    name_expoter =  fields.Char(string="Người xuất" , required=True )
    mobi_expoter = fields.Char(string="Số điện thoại", required=True)
    dept_expoter = fields.Many2one('asset.dept', string="Bộ phận", required=True)

    name_receiver = fields.Char(string="Người nhận" , required=True )
    mobi_receiver = fields.Char(string="Số điện thoại" , required=True )
    dept_receiver = fields.Many2one('asset.dept', string="Bộ phận", required=True)

    dept = fields.Many2one('hr.department',string="Bộ Phận Odoo")

    note = fields.Text(string='Ghi chú')
    state = fields.Selection([('applying', 'Đang lên đơn'), ('confirm', 'Hoàn thành')],default='applying',string="Trạng thái", tracking=True )
    wearhouse_type = fields.Selection([('wearhouse_out', 'Xuất Kho'), ('wearhouse_in', 'Nhập Kho ')],string="Wearhouse type",default='wearhouse_out')
    block_id =  fields.Many2one('asset.block', string="Block", required=True)
    
    room_id =  fields.Many2one(
        'asset.room',
        string='Phòng', required=True)
    asset_wearhouse_detail =  fields.One2many('asset.wearhouse.detail', 'asset_wearhouse_id',string="Wearhouse Detail", required=True)

    ######## Method ######

    # Load room by block
    @api.onchange('block_id')
    def onchange_block_id(self):
        for rec in self:
            return {'domain':{'room_id':[('block_id','=',rec.block_id.id if rec.block_id else False)]}}

    # overide crete method
    @api.model
    def create(self, vals):
        if vals.get('reference', _('New')) == _('New'):
            vals['reference'] =self.env['ir.sequence'].next_by_code('asset.wearhouse.in') or _('New')
            if vals['wearhouse_type'] =='wearhouse_out':
                 vals['reference']=self.env['ir.sequence'].next_by_code('asset.wearhouse.out') or _('New')
        res = super(AssetWearhouse, self).create(vals)
        return res

    def action_confirm(self):
        for rec in self:
            rec.state = 'confirm'
            

    def action_applying(self):
        for rec in self:
            rec.state = 'applying'

    def get_data(self):
        for rec in self:
            detail_wearhouse= rec.asset_wearhouse_detail
            for item in detail_wearhouse:
                print("data item >>> ", item.quantity_update_inventory)

    #Api get value default of field
    @api.model
    def default_get(self, fields_list):
        res =  super().default_get(fields_list)
        return res

    #change name lable in view or form 
    def fields_view_get(self, view_id=None, view_type='tree', toolbar=False, submenu=False):
        result = super(AssetWearhouse, self).fields_view_get(view_id=view_id, view_type=view_type, toolbar=toolbar, submenu=submenu) 
        check_werhouse_type  = self.env.context.get('default_wearhouse_type','Novalue')
    
        doc = etree.XML(result['arch'])
        name_receiver = doc.xpath("//field[@name='name_receiver']")
        name_expoter = doc.xpath("//field[@name='name_expoter']")

        labale_name_receiver = 'Người trả'
        labale_name_expoter = 'Người nhận'
        if check_werhouse_type =='wearhouse_out':
            labale_name_receiver ='Người nhận'
            labale_name_expoter = 'Người xuất'
       
        if name_receiver:
            name_receiver[0].set("string", labale_name_receiver)
            result['arch'] = etree.tostring(doc, encoding='unicode')
        if name_expoter:
            name_expoter[0].set("string", labale_name_expoter)
            result['arch'] = etree.tostring(doc, encoding='unicode')

        return result       


class AssetWearhouseDetail(models.Model):
    _name="asset.wearhouse.detail"
    _description ="Asset Wearhouse Detail"

    asset_wearhouse_id = fields.Many2one("asset.wearhouse",string ="wear_house",required=True )
    wearhouse_type= fields.Selection(related='asset_wearhouse_id.wearhouse_type',string="wearhouse_type")
    block_id =  fields.Many2one('asset.block',related='asset_wearhouse_id.block_id' ,string="Block", required=True)
    room_id = fields.Many2one(
        'asset.room',
        related='asset_wearhouse_id.room_id',
        string='Phòng', required=True)

    product_id = fields.Many2one('product.product',string='Sản phẩm',required=True )
    quantity =  fields.Integer(string="Số lượng",required=True)
    note = fields.Text(string='Mô tả')
    device_status = fields.Selection([('using','Đang được sử dụng'),
                                      ('warranty','Đang trong thời gian bảo hành'),
                                      ('damaged ','Thiết bị hư'),
                                      ('new','Thiết bị mới 100%'),
                                    ],string='Tình trạng thiết bị',default="using")

    categ_id = fields.Many2one(
        'product.category', 'Danh  mục sản phẩm',change_default=True,  required=True)
    product_attri = fields.Text(string="Đơn vị",readonly=True,default=False)

    quantity_available= fields.Integer(string="Số lượng trước khi thay đổi")
    quantity_update_inventory= fields.Integer(string ="Số lượng cập nhật trong kho",compute='_compute_quantity_inventory',store=True,readonly=False,inverse='_inverse_qty_wearhouse')

    quantity_wearhouse = fields.Integer(string="Số lượng trong kho",compute='_compute_quantity_wearhouse',store=False)



    ##-----Method----##
    @api.depends('quantity')
    def _compute_quantity_inventory(self):
        for rec in self:
        # Tìm số lượng đã thay đổi để update vào kho
            if rec.asset_wearhouse_id.wearhouse_type == 'wearhouse_out':
                rec.quantity_update_inventory = rec.quantity_available - rec.quantity
                if  rec.quantity_update_inventory + rec.quantity_wearhouse < 0:
                    rec.quantity = 0
                    raise ValidationError(_('Số lượng trong kho chỉ còn %d',rec.quantity_wearhouse))
            else :
                rec.quantity_update_inventory = rec.quantity  -  rec.quantity_available
        rec.quantity_available = rec.quantity
           
    #Check product duplicate
    @api.onchange('product_id')
    def check_duplicate_product(self):
        for rec in self:
            existing_product = self.env['asset.wearhouse.detail'].search([('product_id.id','=',rec.product_id.id),('asset_wearhouse_id','=', rec.asset_wearhouse_id._origin.id)])
            if existing_product:
             raise AccessError("Bạn đã chọn trùng")

    #Get product if type wearhouse out : Product from in Rooms Export
    @api.onchange('room_id')
    def _get_product_in_room(self):
            for rec in self :
                if (rec.asset_wearhouse_id.wearhouse_type == 'wearhouse_in'):
                     products = self.env['asset.block.product.line']._get_products_in_room(rec.asset_wearhouse_id.block_id,rec.asset_wearhouse_id.room_id )
                     if not  products:
                         raise ValidationError(_('Không có sản phẩm nào trong phòng '))
                     else :
                         return {'domain': {'product_id': [('id', 'in', products.mapped('id'))]}}

    #Get quantity in wearhouse
    @api.depends('product_id')        
    def _compute_quantity_wearhouse(self):
        for rec in self:
            if rec.product_id:


                ##### Start Get Quantity Product #####
                ## Get quantity in Wearhouse
                item = self.env['stock.quant'].search([('product_id', '=', rec.product_id.id),('location_id.usage', '=', 'internal')])
                rec.quantity_wearhouse =sum(item.mapped('quantity'))

                ## IF werahouse in get qty product in room
                if (rec.asset_wearhouse_id.wearhouse_type == 'wearhouse_in'):

                    ##Get Category of product
                    rec.categ_id = self.env['product.template'].search([('id', '=', rec.product_id.id)],
                                                                       limit=1).mapped('categ_id')
                    quanty = self.env['asset.block.product.line']._get_quantity_product_in_room(rec.asset_wearhouse_id.block_id,rec.asset_wearhouse_id.room_id ,rec.product_id)
                    if quanty ==0:
                        raise ValidationError(_('Số lượng sản phẩm  trong phòng còn 0 '))
                    rec.quantity_wearhouse = quanty
                ##### END Get Quantity Product #####

                    # Add attribute to product
                q_attribute_id = self.env['product.template.attribute.line'].search([('product_tmpl_id', '=', rec.product_id.id)])
                rec.product_attri = q_attribute_id.attribute_id.name if q_attribute_id else ''
            else:
                rec.quantity_wearhouse =0
        
    # Get Product by category
    @api.onchange('categ_id')
    def _get_product_by_cate(self):
        for rec in self:
            if rec.categ_id:
                read_group_cate = self.env['product.template'].search([('categ_id', '=', rec.categ_id.id if rec.categ_id else False )])
                list_cate_id = read_group_cate.mapped('id')
                return {'domain':{'product_id':[('product_tmpl_id', 'in', list_cate_id)]}}
    
    # Tính toán lại số lượng trong kho trước khi update
    @api.onchange("quantity_update_inventory")
    def _inverse_qty_wearhouse(self):
        for rec in self:
            rec.quantity_wearhouse +=  rec.quantity_update_inventory 

    #Constraints quantity (Bắt lỗi validate field trong model)

    @api.constrains('quantity')
    def _check_quantity(self):
        if self.quantity <= 0 :
             raise ValidationError(_('Số lượng xuất hoặc nhập kho phải lớn hơn 0'))
        return True;


    ########override create method######
    @api.model
    def create(self, vals):
        res = super(AssetWearhouseDetail, self).create(vals)

        for rec in res:
            print("Block Id > ",rec.asset_wearhouse_id.block_id)
            self._update_quantity(rec.product_id,rec.quantity_update_inventory, rec.asset_wearhouse_id.room_id,
                                  rec.asset_wearhouse_id.block_id)
        return res

    # #override write(update) method
    def write(self, values):
        for item in self:
            if 'quantity_update_inventory' in values:
                self._update_quantity(item.product_id,values.get('quantity_update_inventory',0), self.asset_wearhouse_id.room_id,self.asset_wearhouse_id.block_id)
            
        return super(AssetWearhouseDetail, self).write(values)

    # Update quantity in wearhouse
    def _update_quantity(self,product_item,quantity,room_id,block_id):
        product = self.env['stock.quant'].search([('product_id', '=', product_item.id),('location_id.usage', '=', 'internal')])

        #update quantity
        product.quantity +=quantity
        self.env['stock.quant'].write(product)
        self.env['asset.block.product.line']._check_quantity(room_id,product_item,-quantity if quantity > 0 else abs(quantity),block_id)


class StockQuantityInherit(models.Model):
    _inherit = 'stock.quant'

            
    #Update stock.move
    def _override_inventory_quantity(self, product_item,qty, location_id, location_dest_id, out=False):

        #method ensure_one : check item only 1
        product_item.ensure_one()

        move_val = {
        'name': _('Product Quantity Updated Out Block'),
        'product_id': product_item.product_id.id,
        'product_uom': product_item.product_uom_id.id,
        'product_uom_qty': qty,
        'company_id': product_item.company_id.id or product_item.env.company.id,
        'state': 'confirmed',
        'location_id': location_id.id,
        'location_dest_id': location_dest_id.id,
            'move_line_ids': [(0, 0, {
            'product_id': product_item.product_id.id,
            'product_uom_id': product_item.product_uom_id.id,
            'qty_done': qty,
            'location_id': location_id.id,
            'location_dest_id': location_dest_id.id,
            'company_id': product_item.company_id.id or product_item.env.company.id,
            'lot_id': product_item.lot_id.id,
            'package_id': out and product_item.package_id.id or False,
            'result_package_id': (not out) and product_item.package_id.id or False,
            'owner_id': product_item.owner_id.id,
        })]
    }
        move = self.env['stock.move'].with_context(inventory_mode=False).create(move_val)
        move._action_done()


class AssetWearhouseInherit(models.Model):
    _inherit = 'asset.wearhouse'

    count_werhouse_applying_in =fields.Integer(string="Số lượng lên đơn nhập kho", store=False,
                                               compute ='_compute_count_state_wearhouse_in')
    count_werhouse_done_in = fields.Integer(string="Số lượng hoàn thành nhập kho",store=False,
                                            compute='_compute_count_state_wearhouse_in')

    count_werhouse_applying_out = fields.Integer(string="Số lượng lên đơn xuất kho", store=False,
                                                 compute='_compute_count_state_wearhouse_out')
    count_werhouse_done_out = fields.Integer(string="Số lượng hoàn thành xuất kho" ,store=False,
                                             compute='_compute_count_state_wearhouse_out')

    @api.model
    def wearhouse_overiview(self):
        action = {
            'name': _('Wearhouse Overivew'),
            'view_type': 'tree',
            'view_mode': 'kanban',
            'res_model': 'asset.wearhouse',
            'type': 'ir.actions.act_window',
            'domain': [],
        }
        action['view_id'] = self.env.ref('eiu_asset.wearhouse_overview_kanban').id
        action.update({
            'views': [
                (action['view_id'], 'kanban'),
            ],
        })
        return action

    def _compute_count_state_wearhouse_in(self):
        list_item_wh_in = self.env['asset.wearhouse'].search([(
            'wearhouse_type', '=' , 'wearhouse_in'
        )])
        for rec in self:
            rec.count_werhouse_applying_in = list_item_wh_in.search_count([(
                'state', '=', 'applying'
            )])
            rec.count_werhouse_done_in = len(list_item_wh_in) - rec.count_werhouse_applying_in


    def _compute_count_state_wearhouse_out(self):
        list_item_wh_in = self.env['asset.wearhouse'].search_count([(
            'wearhouse_type', '=' , 'wearhouse_in'
        )])
        for rec in self:
            rec.count_werhouse_applying_out = list_item_wh_in.search_count([(
                'state', '=', 'applying'
            )])
            rec.count_werhouse_done_out = list_item_wh_in - rec.count_werhouse_applying_in



  


   
 

        
      

    


 



    




     