
from odoo import api, fields, models, _

class AccountMoveInherit(models.Model):
    _inherit = 'account.move'

    account_file = fields.Binary(string="Upload chứng từ")