
from odoo import api, fields, models, _

class AccountMoveInherit(models.Model):
    _inherit = 'account.move'

    account_file = fields.Binary(string="Upload chứng từ")
    account_file_name = fields.Char(string= "Tên file")

    def open_qr_code(self):
        print(self.id)
        actions = {
            'type': 'ir.actions.act_window',
            'name': _('Creat Qr Code'),
            'res_model' :'create.qrcode.wizard',
            'target':'new',
            'view_id': self.env.ref('eiu_asset.view_create_qrcode_wizard_form').id,
            'view_mode':'form',
            'context' :{
                'default_account_move_id' : self.id
            }
        }
        return actions