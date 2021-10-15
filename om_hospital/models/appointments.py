from odoo import api, fields, models, _


class HospitalAppointments(models.Model):
    _name = "hospital.appointments"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _description = "Hospital Appointments"

    name = fields.Char(string="Name", required=True, copy=False, readonly=True,
                       default=lambda self: _('New'))
    patient_id = fields.Many2one('hospital.patient', string="Patient", required=True)
    age = fields.Integer(string='Age', related="patient_id.age", tracking=True)
    gender = fields.Selection([
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other'),
    ], related="patient_id.gender", required=True)

    note = fields.Text(string='Description')
    state = fields.Selection([('draft', 'Draft'), ('confirm', 'Confirm'), ('done', 'Done'), ('cancel', 'Canceled')],
                             default='draft',string="Status", tracking=True )
    date_appointment = fields.Date(string="Date")

    def action_draft(self):
        self.state = 'draft'

    def action_done(self):
        self.state = 'done'

    def action_confirm(self):
        self.state = 'confirm'

    def action_cancel(self):
        self.state = 'cancel'

    def action_note(self):
        self.note ='Huynh cuong em'

    @api.model
    def create(self, vals):
        if vals.get('name', _('New')) == _('New'):
            vals['name'] = self.env['ir.sequence'].next_by_code('hospital.appointments') or _('New')
        res = super(HospitalAppointments, self).create(vals)
        return res

    @api.onchange('patient_id')
    def onchange_patient_id(self):
        if self.patient_id:
            if self.patient_id.note:
                self.note = self.patient_id.note
        else:
            self.note = ''

