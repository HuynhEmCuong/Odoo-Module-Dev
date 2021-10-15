from odoo import api, fields, models, _


class CreateAppointmentWizard(models.Model):
    _name = "create.appointment.wizard"
    _description = "Create Appointment Wizard"

    date_appointment = fields.Date(string="Date",required=True)
    patient_id  = fields.Many2one('hospital.patient',string='Patient',required=True)

    def action_create_appointment(self):
        vals = {
            'date_appointment':self.date_appointment,
            'patient_id':self.patient_id.id
        }
        appointment_rec =  self.env['hospital.appointments'].create(vals)
        return {
            'type': 'ir.actions.act_window',
            'name': _('Appointments'),
            'view_mode': 'form',
            'res_model': 'hospital.appointments',
            'res_id':appointment_rec.id,
            
        }

    def action_view_appointment(self):
        action = self.env.ref('om_hospital.appointments_action').read()[0]
        action['domain'] =[('patient_id', '=',self.patient_id.id)]
        return action 
