from odoo import api, fields, models, _

class HospitalDoctors(models.Model):
    _name="hospital.doctors"
    _inherit=["mail.thread", "mail.activity.mixin"]
    _description = "Hospital Doctors"

    doctor_code = fields.Char(string="Order reference", required=True, copy=False, readonly=True,
                            default=lambda self: _('New'))
    name = fields.Char(string="Name", required=True)
    age = fields.Integer(string='Age',  tracking=True,required=True)
    state = fields.Selection([('active', 'Active'), ('lock', 'Lock')],default='active',string="Status", tracking=True )
    note =  fields.Text(string='Description')
    image =fields.Binary(string="Doctor Image")
    gender = fields.Selection([
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other'),
    ], required=True, default='male')

    def action_active(self):
        self.state= 'active'
    
    def action_lock(self):
        self.state= 'lock'


    @api.model
    def create(self, vals):
        if vals.get('doctor_code', _('New')) == _('New'):
            vals['doctor_code'] = self.env['ir.sequence'].next_by_code('hospital.doctors') or _('New')
        res = super(HospitalDoctors, self).create(vals)
        return res