from odoo import api, fields, models, _


class AssetRoom(models.Model):
    _name="asset.room"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _description = "Asset Room"

    reference = fields.Char(string="Order reference", required=True, copy=False, readonly=True,
                            default=lambda self: _('New'))
    name = fields.Char(string="Tên phòng",required=True)
    code = fields.Char(string="Mã phòng" ,required=True)
    note = fields.Text(string='Miêu tả')
    responsible_id = fields.Many2one(comodel_name="res.partner", string='Người tạo')
    state = fields.Selection([('active', 'Active'), ('lock', 'Lock')],default='active',string="Trạng thái", tracking=True )
    block_id =  fields.Many2one('asset.block', string="Block", required=True)
    count_product = fields.Integer(string="Số lượng sản phẩm", compute="_compute_quanity_product",store=False)

    product_line_block_ids = fields.One2many('asset.block.product.line', 'room_id', string="Sản phẩm nằm trong phòng")


    @api.model
    def create(self, vals):
        if vals.get('reference', _('New')) == _('New'):
            vals['reference'] = self.env['ir.sequence'].next_by_code(
                'asset.room') or _('New')
        res = super(AssetRoom, self).create(vals)
        return res

    # show quantity product in room
    def _compute_quanity_product(self):
        for rec in self:
            list_product = self.env['asset.block.product.line'].search([('room_id', '=',
                                                                         rec.ids)])
            quantity = 0
            if list_product:
                quantity = sum(list_product.mapped('quantity'))
            rec.count_product = quantity

    @api.model
    def action_menu_report(self):

        action = {
            'name': _('Room Report'),
            'view_type': 'tree',
            'view_mode': 'list,form',
            'res_model': 'asset.room',
            'type': 'ir.actions.act_window',
            'domain': [],
        }
        action['view_id'] = self.env.ref('eiu_asset.view_room_report_tree').id
        form_view = self.env.ref('eiu_asset.view_room_report_form').id
        action.update({
            'views': [
                (action['view_id'], 'list'),
                (form_view, 'form'),
            ],
        })
        return action