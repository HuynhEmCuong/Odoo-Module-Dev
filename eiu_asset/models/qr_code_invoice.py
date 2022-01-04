from odoo import api, fields, models, _


class QrCodeInvoice(models.Model):
    _name="asset.qr.code.invoice"
    _description = "Module Qr Code Invoice "
    _rec_name = "img_qr_name"


    account_move_id = fields.Many2one('account.move',string ='Bill')
    product_ids = fields.Many2one('product.product',string='Product',required=True )
    img_qr = fields.Binary(string="Qr Code",attachment=False,)
    img_qr_name = fields.Char()



