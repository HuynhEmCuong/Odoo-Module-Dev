from odoo import api, fields, models, _

class AssetProductMoveRoom(models.Model):
    _name = "asset.product.move.room"

    reference = fields.Char(string="Order reference", required=True, copy=False, readonly=True,
                            default=lambda self: _('New'))
    state = fields.Selection([('applying', 'Đang lên đơn'), ('confirm', 'Hoàn thành')],default='applying',string="Trạng thái", tracking=True )

    contact = fields.Char(string="Người chuyển" , required=True )
    mobi = fields.Char(string="Số điện thoại", required=True)
    note = fields.Text(string='Ghi chú')
    dept = fields.Many2one('asset.dept', string="Bộ phận", required=True)

    block_id_from = fields.Many2one('asset.block', string="Block chuyển", required=True)
    room_id_from = fields.Many2one(
        'asset.room',
        string='Phòng chuyển',domain=[('block_id','=','block_id_from')], required=True)

    block_id_to = fields.Many2one('asset.block', string="Block nhận", required=True)
    room_id_to = fields.Many2one(
        'asset.room',
        string='Phòng nhận', required=True)

    date_wearhouse = fields.Datetime(string="Ngày chuyển",
                                     default=fields.Datetime.now)

    current_user = fields.Many2one('res.users', 'Người Tạo', default=lambda self: self.env.user, readonly=True)

    product_move_detail_ids = fields.One2many('asset.product.move.room.detail','product_move_id',string="Danh sách sản phẩm")


    @api.model
    def create(self, vals):
        if vals.get('reference', _('New')) == _('New'):
            vals['reference'] = self.env['ir.sequence'].next_by_code(
                'assset.product.move.room') or _('New')
        res = super(AssetProductMoveRoom, self).create(vals)
        return res

    @api.onchange('block_id_from' , 'block_id_to')
    def _get_room_by_block(self):
        for rec in self:
            return {'domain':{'room_id_from': [('block_id', '=', rec.block_id_from.id if rec.block_id_from else False)],
                             'room_id_to':[('block_id', '=', rec.block_id_to.id if rec.block_id_to else False),
                                           ('id','!=', rec.room_id_from.id if rec.room_id_from else False)]}}


class AssetProductMoveRoomDetial(models.Model):
    _name = "asset.product.move.room.detail"
    _description = 'Asset Product Move Room Detail'

    product_move_id = fields.Many2one('asset.product.move.room')
    room_id_from = fields.Many2one(
        'asset.room',
        related="product_move_id.room_id_from",
        string='Phòng chuyển', required=True)
    product_ids = fields.Many2one('product.product',string='Sản phẩm' ,required=True)
    product_code = fields.Char("Mã sản phẩm",related='product_ids.default_code')
    quantity = fields.Integer(string="Số lượng")

    @api.onchange('room_id_from')
    def _get_product_in_room(self):
        for rec in self:
            if rec.room_id_from:
                list_product_in_room = self.env['asset.block.product.line'].search(
                    [('room_id', '=', rec.room_id_from.id if rec.room_id_from else False)])
                products =list_product_in_room.mapped('product_id').mapped('id')
                return {'domain': {'product_ids': [('id', 'in', products)]}}




