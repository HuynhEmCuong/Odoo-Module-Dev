from odoo import api, fields, models, _


class AssetRoom(models.Model):
    _name="asset.room"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _description = "Asset Room"

    reference = fields.Char(string="Order reference", required=True, copy=False, readonly=True,
                            default=lambda self: _('New'))
    name = fields.Char(string="Room Name",required=True)
    code = fields.Char(string="Room Code" ,required=True)
    note = fields.Text(string='Description')
    responsible_id = fields.Many2one(comodel_name="res.partner", string='Responsible')
    state = fields.Selection([('active', 'Active'), ('lock', 'Lock')],default='active',string="Status", tracking=True )
    block_id =  fields.Many2one('asset.block', string="Block", required=True)



    @api.model
    def create(self, vals):
        if vals.get('reference', _('New')) == _('New'):
            vals['reference'] = self.env['ir.sequence'].next_by_code(
                'asset.room') or _('New')
        res = super(AssetRoom, self).create(vals)
        return res
