from odoo import api, fields, models, _
import pyqrcode
import qrcode
import base64
import io

class CreateQrCodeProduct(models.Model):
    _name='create.qrcode.wizard'
    _description = 'Create Qr Code for Product'


    account_move_id = fields.Many2one('account.move',string ='Bill')
    product_ids = fields.Many2one('product.product',string='Product',required=True )

    @api.onchange('account_move_id')
    def get_data_product(self):
        if self.account_move_id:
            account_move_line = self.env['account.move.line'].search([('move_id' , '=', self.account_move_id.id) ,('product_uom_id' , '!=',False ),('product_id' , '!=',False )])
            return {'domain': {'product_ids': [('id', 'in', account_move_line.mapped('product_id').mapped('id'))]}}

    def print_qrcode(self):
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=20,
            border=4,
        )
        name_bill = self.account_move_id.name
        name_payment = self.account_move_id.partner_id.name
        name_pro = self.product_ids.name
        data_qr = "Hoá đơn: " + name_bill + "\n" + "Nhà CC: " + name_payment + "\n" + "Tên SP: " + name_pro
        qr.add_data(data_qr)
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")
        buffer = io.BytesIO()
        img.save(buffer, format="PNG")
        img_str = base64.b64encode(buffer.getvalue())
        img_name = name_bill+"_"+name_pro + "_"+"qr.png"

        vals = {
            'account_move_id':self.account_move_id.id,
            'product_ids' :self.product_ids.id,
            'img_qr' : img_str,
            'img_qr_name':img_name
        }
        qr_code_rec = self.env['asset.qr.code.invoice'].create(vals)
        return {
            'type': 'ir.actions.act_window',
            'name': _('Qr Code'),
            'view_mode': 'form',
            'res_model': 'asset.qr.code.invoice',
            'res_id': qr_code_rec.id,
        }



