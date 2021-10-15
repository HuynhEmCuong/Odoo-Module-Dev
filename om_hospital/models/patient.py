from odoo import api, fields, models, _


class HospitalPatient(models.Model):
    _name = "hospital.patient"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _description = "Hospital Patient"

    name = fields.Char(string='Name', required=True)
    age = fields.Integer(string='Age', tracking=True)
    reference = fields.Char(string="Order reference", required=True, copy=False, readonly=True,
                            default=lambda self: _('New'))
    gender = fields.Selection([
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other'),
    ], required=True, default='male')
    note = fields.Text(string='Description')
    state = fields.Selection([('draft', 'Draft'), ('confirm', 'Confirm'), ('done', 'Done'), ('cancel', 'Canceled')],
                             string="Status", tracking=True,default="draft")

    responsible_id = fields.Many2one(
        comodel_name="res.partner", string='Responsible')
    appointment_count = fields.Integer(string="Appointment Count", compute='_compute_appointment_count')
    image =fields.Binary(string="Paitient Image")
    
    # Use function get data from child
    def _compute_appointment_count(self):
        for res in self:
            appointment_count = self.env['hospital.appointments'].search_count(
                [('patient_id', '=', res.id)])
            res.appointment_count = appointment_count

    def action_draft(self):
        for res in self:
            res.state = 'draft'

    def action_done(self):
        for res in self:
            self.state = 'done'

    def action_confirm(self):
        for res in self:
            self.state = 'confirm'

    def action_cancel(self):
        for res in self:
            self.state = 'cancel'

    # api create record 
    @api.model
    def create(self, vals):
        if not vals.get('note'):
            vals['note'] = 'New Patient'
        if vals.get('reference', _('New')) == _('New'):
            vals['reference'] = self.env['ir.sequence'].next_by_code(
                'hospital.patient') or _('New')
        res = super(HospitalPatient, self).create(vals)
        return res

    #Api get value default of field
    # @api.model
    # def default_get(self, fields_list):
    #     res =  super().default_get(fields_list)
    #     print("field............", res)
    #     return res
