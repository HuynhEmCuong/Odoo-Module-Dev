from odoo import api, fields, models, _
import pyqrcode

class CreateQrCodeProduct(models.Model):
    _name='create.qrcode.wizard'
    _description = 'Create Qr Code for Product'


    account_move_id = fields.Many2one('account.move',string ='Bill')
    product_ids = fields.Many2one('product.product',string='Product',required=True )

    @api.onchange('account_move_id')
    def get_data_product(self):
        if self.account_move_id:
            acount_move  = self.env['account.move'].browse(self.id)
            test = self.browse()
            account_move_line = self.env['account.move.line'].search([('move_id' , '=', self.account_move_id.id) ,('product_uom_id' , '!=',False ),('product_id' , '!=',False )])
            return {'domain': {'product_ids': [('id', 'in', account_move_line.mapped('product_id').mapped('id'))]}}

    def print_qrcode(self):
        print(self.product_ids.id)

        # print("OK")
        # tesst = self.browse()
        # print(tesst.product_ids[0].name)
        #qr = pyqrcode.QRCode('HCE')
        # qr.svg()



