
from odoo import api, fields, models,_
from werkzeug.urls import url_encode
import unicodedata

class EmployeesInherit(models.Model):
    _inherit = "hr.employee"
    _description = "Employee Inherit"

    employee_number = fields.Char(string="Id Number", readonly =1)
    employee_email = fields.Char(string="Email EIU")
    employee_is_delete = fields.Selection([('active', 'Active'),('force', 'Force'),('temporary','Temporary')],
                                          string="Status staff", tracking =True,default ='active')
    employee_email_gg = fields.Selection([('created', 'Created'),('not', 'Not Crated')],
                                         string=" Mail Google", tracking =True,default ='not')
    employee_account_system = fields.Selection([('created', 'Created'), ('not', 'Not Crated')],
                                               string=" Portal", tracking =True,default ='not')
    employee_card = fields.Selection([('created', 'Created'), ('not', 'Not Crated')],
                                     string=" Card", tracking =True,default ='not')
    employee_staff = fields.Selection([('staff', 'Staff'), ('lecturers', 'Lecturers')],string= "Type")




    def get_id_number_emp(self,dept):
        items = self.env['hr.employee'].search([('department_id', '=', dept)])
        if items:
            # Get emp_number max
            idNumber_max_items = max(items.mapped('employee_number'))
            # Get dept code
            dept_code = idNumber_max_items[:2]

            # Get Last 4 characters string(emp_num)
            emp_max = idNumber_max_items[-4:]
            # Create new emp_number
            emp_number_new = self._sync_emp_number(int(emp_max)+1)

            return  f'{dept_code}{emp_number_new}'

        else :
            dept_code =max(( self.env['hr.department'].search([('id', '=',dept)], limit =1)).mapped('dep_code'))
            print(dept_code)
            return  f'{dept_code}0001'

    def _sync_emp_number(self,x):
       if (x <10) :
           return f'000{x}'
       elif (x >=10):
           return f'00{x}'
       elif(x >=100):
           return f'0{x}'
       else:
           x
    def get_email_emp(self,emp_name):
        print(emp_name)

    # Overide method create
    @api.model
    def create(self, vals):
        if vals.get('user_id'):
            user = self.env['res.users'].browse(vals['user_id'])
            vals.update(self._sync_user(user, vals.get('image_1920') == self._default_image()))
            vals['name'] = vals.get('name', user.name)


        if vals.get('department_id'):
            vals['employee_number'] = self.get_id_number_emp(vals.get('department_id'))

        if vals.get('name'):
            self.get_email_emp(vals.get('name'))

        employee = super(EmployeesInherit, self).create(vals)
        url = '/web#%s' % url_encode({
            'action': 'hr.plan_wizard_action',
            'active_id': employee.id,
            'active_model': 'hr.employee',
            'menu_id': self.env.ref('hr.menu_hr_root').id,
        })
        employee._message_log(
            body=_('<b>Congratulations!</b> May I recommend you to setup an <a href="%s">onboarding plan?</a>') % (url))
        if employee.department_id:
            self.env['mail.channel'].sudo().search([
                ('subscription_department_ids', 'in', employee.department_id.id)
            ])._subscribe_users()
        return employee

    # Overide method create
    def write(self, vals):
        if 'address_home_id' in vals:
            account_id = vals.get('bank_account_id') or self.bank_account_id.id
            if account_id:
                self.env['res.partner.bank'].browse(account_id).partner_id = vals['address_home_id']
        if vals.get('user_id'):
            # Update the profile pictures with user, except if provided
            vals.update(self._sync_user(self.env['res.users'].browse(vals['user_id']), bool(vals.get('image_1920'))))
        res = super(EmployeesInherit, self).write(vals)
        if vals.get('department_id') or vals.get('user_id'):
            department_id = vals['department_id'] if vals.get('department_id') else self[:1].department_id.id
            # When added to a department or changing user, subscribe to the channels auto-subscribed by department
            self.env['mail.channel'].sudo().search([
                ('subscription_department_ids', 'in', department_id)
            ])._subscribe_users()
        return res

