from odoo import api, fields, models

class DepartmentInherit(models.Model):
    _inherit = 'hr.department'
    _description = 'Department Inherit'

    dep_code = fields.Char(string="Display Code")