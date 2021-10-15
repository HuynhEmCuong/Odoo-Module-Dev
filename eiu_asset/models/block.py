from odoo import api, fields, models, _


class AssetBlock(models.Model):
    _name="asset.block"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _description = "Asset Blocks"

    reference = fields.Char(string="Order reference", required=True, copy=False, readonly=True,
                            default=lambda self: _('New'))
    name = fields.Char(string="Block Name",required=True)
    code = fields.Char(string="Block Code" ,required=True)
    note = fields.Text(string='Description')
    responsible_id = fields.Many2one(comodel_name="res.partner", string='Responsible',required=True)
    state = fields.Selection([('active', 'Active'), ('lock', 'Lock')],default='active',string="Status", tracking=True )
    rooms_ids  = fields.One2many('asset.room', 'block_id',string="Rooms")

    @api.model
    def create(self, vals):
        if vals.get('reference', _('New')) == _('New'):
            vals['reference'] = self.env['ir.sequence'].next_by_code(
                'asset.block') or _('New')
        res = super(AssetBlock, self).create(vals)
        return res
