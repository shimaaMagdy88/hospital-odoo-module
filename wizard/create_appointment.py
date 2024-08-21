from odoo import fields, models, api, _
from odoo.exceptions import ValidationError


class CreateAppointment(models.TransientModel):
    _name = 'create.appointment.wizard'

    patient_id = fields.Many2one('hospital.patient', require=True)
    date = fields.Date(string='Appointment Date')

    def action_create(self):
        dict = {
            'patient_id': self.patient_id.id,
        }
        self.env['hospital.appointment'].create(dict)

    def action_print_pdf(self):
        data = {
            'model': 'create.appointment.wizard',
            'form': self.read()[0]
        }

        if not self.patient_id:
            raise ValidationError(_('Patient is required'))

        selected_patient = data['form']['patient_id'][0]     # id as num
        appointments = self.env['hospital.appointment'].search([('patient_id', '=', selected_patient)])

        appointments_list = []
        for appoint in appointments:
            appoint_dict = {
                'name': appoint.patient_id.name,
                'appointment_date': appoint.appointment_time,
                'ref': appoint.ref
            }
            appointments_list.append(appoint_dict)

        data['appointments'] = appointments_list
        return self.env.ref('om_hospital.action_appointment_report').report_action(self, data=data)
