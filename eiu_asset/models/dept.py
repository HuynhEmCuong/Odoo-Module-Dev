from odoo import api, fields, models, _


class AssetDept (models.Model):
    _name = "asset.dept"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _description = 'Assset Deptment'

    name = fields.Char(string="Tên bộ phận ", required=True)
    code = fields.Char(string="Kí hiệu", required=True)
    note = fields.Text(string='Description')
    state = fields.Selection([('active', 'Active'), ('lock', 'Lock')], default='active', string="Trạng thái",
                             tracking=True)
    responsible_id = fields.Many2one('res.users', 'Người Tạo', default=lambda self: self.env.user, readonly=True)
