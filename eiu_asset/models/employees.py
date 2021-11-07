
from odoo import api, fields, models

class EmployeesInherit(models.Model):
    _inherit = "hr.employee"
    _description = "Employee Inherit"

    employee_number = fields.Char(string="Id Number")
    employes_email = fields.Char(string="Work Email ")




