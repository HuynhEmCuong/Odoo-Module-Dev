from odoo import api, fields, models, _

class StockMoveLineInherit(models.Model):
    _inherit = "stock.move"

    pro_status = fields.Selection([('using','Đang được sử dụng'),
                                      ('warranty','Đang trong thời gian bảo hành'),
                                      ('damaged ','Thiết bị hư'),
                                      ('new','Thiết bị mới 100%'),
                                    ],string='Status Pro',default="using")


class StockPickingInherit(models.Model):
    _inherit = 'stock.picking'

    pro_status = fields.Selection( related ='move_ids_without_package.pro_status',copy=True, )