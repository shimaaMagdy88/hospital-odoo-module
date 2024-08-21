from odoo import api, fields, models, _
from odoo.exceptions import ValidationError
import random


class HospitalAppointment(models.Model):
    _name = "hospital.appointment"
    _description = "hospital appointment"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _rec_name = 'sequence'      # by default=> model_name, id
    _order = 'id asc'

    patient_id = fields.Many2one('hospital.patient', string="Patient", tracking=True, required=True)
    doctor = fields.Many2one('res.users', string="Doctor", tracking=True)
    patient_phone = fields.Char(string='Patient Phone', related='patient_id.phone')
    gender = fields.Selection(related='patient_id.gender')
    ref = fields.Char(string="Reference")
    age = fields.Integer(related='patient_id.age', readonly=False)
    appointment_time = fields.Datetime(string="Appointment Time", tracking=True, default=fields.Datetime.now)
    booking_date = fields.Date(string="Booking Date", tracking=True, default=fields.Date.context_today)
    prescription = fields.Html(string='prescription')
    active = fields.Boolean(string='Active', default=True)
    image = fields.Image(string='Image')
    hide_sales_price = fields.Boolean(string='Hide Sales Price')
    doctors_tag_ids = fields.Many2many('hospital.patient.tag', string='Tags')
    sequence = fields.Char(string='Sequence')
    priority = fields.Selection([('0', 'Very Low'),
                                 ('1', 'Low'),
                                 ('2', 'Normal'),
                                 ('3', 'High')], string='Priority')
    state = fields.Selection([('draft', 'Draft'),
                              ('in_consultation', 'In_consultation'),
                              ('done', 'Done'),
                              ('cancel', 'Canceled')], string='Status', default='draft', required=True)
    pharmacy_line_ids = fields.One2many('appointment.pharmacy.lines', 'appointment_id', string='Pharmacy Line')
    operation = fields.Many2one('hospital.operation', string='Operation')
    progress = fields.Integer(string='Progress', compute='_compute_progress')
    duration = fields.Integer(string='Duration')    # will be computed from calendar -> date_delay
    url = fields.Char(string='URL')
    # total = fields.Monetary(string='Total', compute='_compute_total')

    company_id = fields.Many2one('res.company', string='Company')
    currency_id = fields.Many2one('res.currency', string='Currency')
    country_id = fields.Many2one('res.country', string='Country')
    city_id = fields.Many2one('res.country.state', string='City')

    my_company_id = fields.Many2one('res.company', string='My Company', default=lambda self: self.env.company)
    company_currency_id = fields.Many2one('res.currency', string='My Currency', related='company_id.currency_id')
    my_country_id = fields.Many2one('res.country', string='My Country')
    my_city_id = fields.Many2one('res.country.state', string='My City', domain="[('country_id', '=', country_id)]")

    def object_send_mail(self):
        template = self.env.ref('om_hospital.appointment_mail_template')  # mail.template(45,)
        for rec in self:
            template.send_mail(rec.id)                      # use the built_in_method (send_mail)

            # 1- we can use force_send to change mail state
            template.send_mail(rec.id, force_send=True)

            # 2- we can use email_values to change subject, and other values: EX
            email_values = {
                    'email_cc': False,
                    'auto_delete': True,
                    'subject': 'OM Test',
                },
            template.send_mail(rec.id, email_values=email_values)


        print(email_values)

    @api.depends('state')
    def _compute_progress(self):
        for rec in self:
            if rec.state == 'draft':
                rec.progress = 25
            elif rec.state == 'in_consultation':
                rec.progress = random.randrange(25, 99)
            elif rec.state == 'done':
                rec.progress = 100
            else:
                rec.progress = 0

    @api.onchange('patient_id')          # like related attribute
    def onchange_patient_id(self):
        self.ref = self.patient_id.ref

    def object_test(self):
        print("button clicked!!!!!!!!!")
        patient = self.env['hospital.patient'].search(args=[('id', '=', self.patient_id.id)]).name
        print(patient)

        return {
            'type': 'ir.actions.act_url',
            'target': 'new',                 # default: new

            # ----- 1- static url -----
            # 'url': 'http://127.0.0.1:8015/shop',         # url inside odoo
            # 'url': 'shop'                                # url inside odoo
            # 'url': 'https://www.youtube.com'               # url outside odoo

            # ----- 2- dynamic url -----
            'url': self.url                   # not that url is a field in this model (has a url: facebook)
        }

    def object_share_whatsapp(self):
        if self.patient_phone:
            message = 'Hi %s' % self.patient_id.name
            whatsapp_api_url = 'https://api.whatsapp.com/send?phone=%s&text=%s' % (self.patient_phone, message)

            return {
                'type': 'ir.actions.act_url',
                'url': whatsapp_api_url
            }
        else:
            raise ValidationError(_('There Is No User Phone'))

    def object_chatter_message(self):
        message = f"hello {self.patient_id.name}"
        self.message_post(body=message, subject='Whatsapp')

    def object_show_notification(self):
        search_patient = self.env['hospital.patient'].search(args=[('id', '=', self.patient_id.id)])
        print(search_patient.name, search_patient.age)

        message = 'Button Clicked Successfully'
        action = self.env.ref('om_hospital.action_hospital_patient')
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'type': 'info',
                'title': _('Click Here To Open Patient Record'),
                'message': '%s',
                'links': [{
                    'label': self.patient_id.name,
                    'url': f'#acion={action.id}&id={self.patient_id.id}&model=hospital.patient'
                }],
                'sticky': True,
                'next': {
                    'type': 'ir.actions.act_window',
                    'res_model': 'hospital.patient',
                    'res_id': self.patient_id.id,
                    'views': [(False, 'form')]
                }
            }
        }

    def object_in_consultation(self):
        for rec in self:
            if rec.state == 'draft':
                rec.state = 'in_consultation'

    def object_done(self):
        for rec in self:
            rec.state = 'done'
        return {
            'effect': {
                'message': 'Appointment was Done Successfully',
                'fadeout': 'slow',
                'type': 'rainbow_man'
            }
        }

    def object_cancel(self):
        action = self.env.ref('om_hospital.action_cancel_appointment_two').read()[0]
        return action

    def object_draft(self):
        for rec in self:
            rec.state = 'draft'

    def set_line_number(self):
        num = 0
        for line in self.pharmacy_line_ids:
            num += 1
            line.sl_no = num

    @api.model
    def create(self, vals):
        vals['sequence'] = self.env['ir.sequence'].next_by_code('hospital.appointment')
        result = super(HospitalAppointment, self).create(vals)   # result => hospital.appointment(12,)
        result.set_line_number()
        return result

    def write(self, vals):
        if not self.sequence:
            vals['sequence'] = self.env['ir.sequence'].next_by_code('hospital.appointment')

        result = super(HospitalAppointment, self).write(vals)
        self.set_line_number()                                 # call another method in write method

        return result

    def unlink(self):
        if self.state == 'done':
            raise ValidationError(_("you can't delete record with 'done' status")) # raise ... and not delete
        return super(HospitalAppointment, self).unlink()


class AppointmentPharmacyLines(models.Model):
    _name = "appointment.pharmacy.lines"
    _description = "appointment pharmacy lines"
    _inherit = ["mail.thread", "mail.activity.mixin"]

    sl_no = fields.Integer(string='SNO.', readonly=True)
    product_id = fields.Many2one('product.product')
    price = fields.Float(related='product_id.list_price', digits='Product Price')
    quantity = fields.Integer(string='Quantity')
    appointment_id = fields.Many2one('hospital.appointment', string='Appointment')

    currency_idd = fields.Many2one('res.currency', related='appointment_id.company_currency_id')
    price_subtotal = fields.Monetary(string='Sub Total', currency_field='currency_idd', compute='_compute_subtotal')
    # total = fields.Monetary(string='Total', compute='_compute_total')

    @api.depends('price', 'quantity')
    def _compute_subtotal(self):
        for rec in self:
            rec.price_subtotal = rec.price * rec.quantity

