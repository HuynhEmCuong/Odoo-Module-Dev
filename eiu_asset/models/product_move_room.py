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
        string='Phòng chuyển', required=True)

    block_id_to = fields.Many2one('asset.block', string="Block nhận", required=True)
    room_id_to = fields.Many2one(
        'asset.room',
        string='Phòng nhận', required=True)

    date_wearhouse = fields.Datetime(string="Ngày chuyển",
                                     default=fields.Datetime.now)

    current_user = fields.Many2one('res.users', 'Người Tạo', default=lambda self: self.env.user, readonly=True)




    @api.model
    def create(self, vals):
        if vals.get('reference', _('New')) == _('New'):
            vals['reference'] = self.env['ir.sequence'].next_by_code(
                'assset.product.move.room') or _('New')
        res = super(AssetProductMoveRoom, self).create(vals)
        return res