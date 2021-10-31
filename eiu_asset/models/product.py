from odoo import api, fields, models

class ProductCategoryInherit(models.Model):
    _inherit ="product.category"

    product_code_category = fields.Char(string ="Code", required=True, )
    check_barcode         = fields.Selection([('Use', 'use'),('Not', 'not')], string="Use barcode",required=True)


class AssetBlockProduct (models.Model):
    _name='asset.block.product.line'
    _description = "Asset Block Realationship Product"

    block_id = fields.Many2one('asset.block', string='Block')
    room_id = fields.Many2one('asset.room', string='Phòng')
    product_id = fields.Many2one('product.product', string='Sản phẩm')
    quantity= fields.Integer(string="Số lương")

    # Find product and update quantity if exits reverse
    def _check_quantity(self, room_id, product_id,quantity,block_id):
        item = self.env['asset.block.product.line'].search([('product_id', '=' , product_id.id),
                                                            ('room_id','=', room_id.id),
                                                            ('block_id','=', block_id.id)])
        if item:
            item.quantity += quantity
            super(AssetBlockProduct, self).write(item)
        else:
            new_vals = {
                'block_id': block_id.id,
                'room_id': room_id.id,
                'product_id': product_id.id,
                'quantity': abs(quantity)
            }
            super(AssetBlockProduct, self).create(new_vals)
