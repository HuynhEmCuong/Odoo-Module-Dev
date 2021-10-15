from odoo import api, fields, models

class ProductCategoryInherit(models.Model):
    _inherit ="product.category"

    product_code_category = fields.Char(string ="Code", required=True, )
    check_barcode         = fields.Selection([('Use', 'use'),('Not', 'not')],default="not", string="Use barcode")

# class ProductInherit(models.Model):
#     block_id = 

