from datetime import date
from odoo import api, fields, models, _
from odoo.exceptions import ValidationError
from dateutil import relativedelta

class CancelAppointmentWizard(models.TransientModel):
    _name = "cancel.appointment.wizard.two"
    _description = "cancel appointment wizard two"
    _inherit = ["mail.thread", "mail.activity.mixin"]

    appointment_id = fields.Many2one('hospital.appointment', string='Appointment', domain=['|', ('state', '=', 'draft'), ('priority', '=', '2')])
    reason = fields.Text(string='Reason', default='no reason')
    cancel_date = fields.Date(string='Date Cancellation')


    def default_get(self, fields):
        result = super(CancelAppointmentWizard, self).default_get(fields)
        print(self.env.context)

        # set default values:
        result['reason'] = 'Odoo Mates'

        if self.env.context.get('active_id'):
            result['appointment_id'] = self.env.context.get('active_id')

        return result

    def action_cancel_btn(self):
        # cancel_days = self.env['ir.config_parameter'].get_param('om_hospital.cancel_days')
        # allowed_cancel_date = self.appointment_id.booking_date - relativedelta.relativedelta(days=int(cancel_days))
        #
        # if allowed_cancel_date < date.today():       # means that: if today reached to the date which is allowed cancellation 'before' it
        #     raise ValidationError(_('sorry, cancellation is not allowed for this booking!'))
        # else:
        self.appointment_id.state = 'cancel'

        # return {
        #     'type': 'ir.actions.client',
        #     'tag': 'reload',
        # }
        return {
            'res_model': 'cancel.appointment.wizard.two',
            'view_mode': 'form',
            'type': 'ir.actions.act_window',
            'target': 'new',
            # 'res_id': self.id
        }
