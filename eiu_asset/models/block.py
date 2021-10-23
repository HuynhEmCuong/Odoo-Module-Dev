from odoo import api, fields, models, _


class AssetBlock(models.Model):
    _name="asset.block"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _description = "Asset Blocks"

    reference = fields.Char(string="Order reference", required=True, copy=False, readonly=True,
                            default=lambda self: _('New'))
    name = fields.Char(string="Block Name", required=True)
    code = fields.Char(string="Block Code", required=True)
    note = fields.Text(string='Description')
    responsible_id = fields.Many2one('res.users','Người Tạo', default=lambda self: self.env.user,readonly=True)
    state = fields.Selection([('active', 'Active'), ('lock', 'Lock')],default='active',string="Trạng thái", tracking=True )
    rooms_ids  = fields.One2many('asset.room', 'block_id',string="Rooms")

    count_product = fields.Integer(string="Số lượng sản phẩm",compute='_count_product_block',store=False)
    product_line_block_ids = fields.One2many('asset.block.product.line','block_id',string="Sản phẩm nằm trong block")

    @api.model
    def create(self, vals):
        if vals.get('reference', _('New')) == _('New'):
            vals['reference'] = self.env['ir.sequence'].next_by_code(
                'asset.block') or _('New')
        res = super(AssetBlock, self).create(vals)
        return res

    def _count_product_block(self):
        for rec in self:
            list_product = self.env['asset.block.product.line'].search([('block_id', '=',
                                                                         rec.ids)])
            quantity = 0
            if list_product:
                quantity = sum(list_product.mapped('quantity'))
            rec.count_product = quantity

    # Add menu from python
    @api.model
    def action_menu_report(self):
        action = {
            'name': _('Block Report'),
            'view_type': 'tree',
            'view_mode': 'list,form',
            'res_model': 'asset.block',
            'type': 'ir.actions.act_window',
            'domain': [],
        }
        action['view_id'] = self.env.ref('eiu_asset.view_block_report_tree').id
        form_view = self.env.ref('eiu_asset.view_block_report_form').id
        action.update({
            'views': [
                (action['view_id'], 'list'),
                (form_view, 'form'),
            ],
        })
        return action


