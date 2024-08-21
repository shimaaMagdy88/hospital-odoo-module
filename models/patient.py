from datetime import date
from odoo import api, fields, models, _
from odoo.exceptions import ValidationError
from dateutil import relativedelta

class HospitalPatient(models.Model):
    _name = "hospital.patient"
    _description = "hospital patient"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _log_access = False
    # _rec_name = 'name'

    tag_ids = fields.One2many('hospital.patient.tag', 'patient_id')
    name = fields.Char(string="Name", tracking=2, required=True, translate=True)
    ref = fields.Char(string="Reference")
    date_of_birth = fields.Date(string="Birthdate", required=False)
    age = fields.Integer(string="Age", compute="_compute_age", inverse='_inverse_compute_age', search='_search_age')
    gender = fields.Selection([("male", "Male"), ("female", "Female")], string="Gender", tracking=1, default='male')
    active = fields.Boolean(string="Active", default=True)
    appointment_count = fields.Integer(string='Appointment Count', compute="_compute_appointment_count", store=True)
    appointment_ids = fields.One2many('hospital.appointment', 'patient_id', string='Appointments')
    # new_field = fields.Char()
    parent = fields.Char(string='Parent', tracking=5)
    country = fields.Many2one('hospital.country', string='Country')
    city = fields.Many2one('hospital.city3', string='City')
    is_birthday = fields.Boolean(string='Is Birthday', compute='_compute_is_birthday')
    phone = fields.Char(string='Phone')
    email = fields.Char(string='Email')
    website = fields.Char(string='Website URL')
    image = fields.Image(string='Image')

    def object_view_appointment(self):
        action = self.env.ref('om_hospital.action_hospital_appointment').read()[0]
        # return action
        return {
            'name': _('Appointments'),
            'res_model': 'hospital.appointment',
            'view_mode': 'tree,form,calendar',
            'context': {'default_patient_id': self.id},
            'domain': [('patient_id', '=', self.id)],
            'type': 'ir.actions.act_window'
        }

    @api.depends('date_of_birth')               # take age when typed (not when submit)
    def _compute_age(self):
        print('self --------------')
        for rec in self:
            today = date.today()
            if rec.date_of_birth:
                rec.age = today.year - rec.date_of_birth.year
            else:
                rec.age = 0

    @api.depends('age')
    def _inverse_compute_age(self):
        print('-----inversed-------')
        today = date.today()
        for rec in self:
            rec.date_of_birth = today - relativedelta.relativedelta(years=rec.age)

            # my_year = today.year - rec.age
            # rec.date_of_birth = today - relativedelta.relativedelta(year=my_year)
        return

    def _search_age(self, operator, value):
        birthdate = date.today() - relativedelta.relativedelta(years=value)
        # return [('date_of_birth', '=', birthdate)]   => we can return any field except 'age' that has that we want to search

        start_of_year = birthdate.replace(day=1, month=1)
        end_of_year = birthdate.replace(day=31, month=12)
        return [('date_of_birth', '>=', start_of_year), ('date_of_birth', '<=', end_of_year)]

    @api.model
    def create(self, vals):
        # print('odoo creation method override', vals)
        vals['ref'] = '111'
        return super(HospitalPatient, self).create(vals)

    def name_get(self):      # change the _rec_name
        patient_list = []

        for record in self:
            if record.ref:
                name = record.ref + ' ' + record.name
            else:
                name = 'No Ref. ' + ' ' + record.name

            patient_list.append((record.id, name))

        return patient_list    # list of tuples [(id, ..), ..] , that will be used in relations instead of _rec_name

        # return [(record.id, "%s %s" % (record.ref, record.name)) for record in self]    => shortest

    def copy(self, default=None):
        if default is None:
            default = {}

        if not default.get('appointment_ids'):
            default['appointment_ids'] = [(0, 0, {'doctor': line.doctor.id}) for line in self.appointment_ids]

        return super(HospitalPatient, self).copy(default)


    @api.constrains('date_of_birth')
    def _check_birthdate(self):
        for rec in self:
            if rec.date_of_birth and rec.date_of_birth > fields.Date.today():
                raise ValidationError(_('date not acceptable'))

    @api.depends('appointment_ids')
    def _compute_appointment_count(self):
        for rec in self:
            # count = rec.env['hospital.appointment'].search_count([('patient_id', '=', rec.id)])
            # rec.appointment_count = count

            appointment_group = rec.env['hospital.appointment'].read_group(domain=[], fields=['patient_id'], groupby=['patient_id'])

            for appointment in appointment_group:
                patient_id = appointment.get('patient_id')[0]
                patient_rec = self.browse(patient_id)
                patient_rec.appointment_count = appointment.get('patient_id_count')


    @api.ondelete(at_uninstall=False)
    def _check_appointments(self):
        for rec in self:
            if rec.appointment_count:
                raise ValidationError(_('you can\'t delete patient with appointments'))

    def object_patient_test(self):
        print('---clicked---')
        return

    @api.onchange('country')
    def onchange_country(self):
        for rec in self:
            return {
                'domain': {'city': [('country', '=', rec.country.country_name)]}
            }
            print('changed')


    @api.depends('date_of_birth')
    def _compute_is_birthday(self):
        today = date.today()
        for record in self:
            if record.date_of_birth:
                if today.day == record.date_of_birth.day and today.month == record.date_of_birth.month:
                    record.is_birthday = True
                else:
                    record.is_birthday = False
            else:
                record.is_birthday = False


