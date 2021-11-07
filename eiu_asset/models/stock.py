from odoo import api, fields, models, _

class StockMoveLineInherit(models.Model):
    _inherit = "stock.move.line"

    pro_status = fields.Selection([('using','Đang được sử dụng'),
                                      ('warranty','Đang trong thời gian bảo hành'),
                                      ('damaged ','Thiết bị hư'),
                                      ('new','Thiết bị mới 100%'),
                                    ],string='Tình trạng thiết bị',default="using")

