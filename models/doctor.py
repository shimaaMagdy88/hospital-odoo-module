from odoo import api, fields, models

class HospitalAppointment(models.Model):
    _name = "hospital.doctor"
    _description = "hospital doctor"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _rec_name = 'doctors_tags'

    doctor_name = fields.Char(string="Doctor Name", tracking=True, trim=False)
    gender = fields.Selection([('male', 'Male'), ('female', 'Female')], string='Gender')
    age = fields.Integer(string='Age')
    active = fields.Boolean(string='Active', default=True)
    doctors_tags = fields.Char(string='Tag')
    color = fields.Integer(string='Color')
    color_2 = fields.Char(string='Color2')
    test = fields.Char(string='test')
    priority = fields.Selection([('0', 'Very Low'),
                                 ('1', 'Low'),
                                 ('2', 'Normal'),
                                 ('3', 'High')], string='Priority')
    sequence = fields.Char(string='Sequence', default="New")
    salary = fields.Float(string='Salary', digits='Product Price')

    # decimal precision:
    # with float field, we have to use digits='one of the decimal precisions' attribute & 'field_digits':True option

    @api.model
    def create(self, vals):
        vals['sequence'] = self.env['ir.sequence'].next_by_code('hospital.doctor')
        return super(HospitalAppointment, self).create(vals)

    def write(self, vals):
        vals['test'] = '222'                                    # i can create keys & its values if not found: vals['key'] = value
        print(vals, 'hello from write (edit) method')

        if not self.sequence and not vals.get('sequence'):      # if this field was empty & not have been changed (not have this key)
            vals['sequence'] = self.env['ir.sequence'].next_by_code('hospital.doctor')

        return super(HospitalAppointment, self).write(vals)

    def test_query(self):

        query1 = f"select name from hospital_patient"
        self.env.cr.execute(query1)
        doctors = self.env.cr.fetchall()

        query2 = f"select id, doctor_name from hospital_doctor where id={self.id}"
        self.env.cr.execute(query2)
        doctor = self.env.cr.dictfetchall()

        print(doctors)            # [('nana',), ('mmmmmmm',), ('odoo mate',), ('ahmedd',), ('jodyy',), ('lolo',)]
        print(doctor)             # [{'id': 17, 'doctor_name': 'samah'}]



    # NOTE: create, write(edit) methods implement when click at save btn
    # vals parameter: in create is a dictionary that contains all fields in form,
    # vals parameter: in write is a dictionary that contains only changed fields,



    # printing inside method ('write' method as example)
    # print(self)           => model_name(current_record_id,)  ==> hospital.doctor(4,)
    # print(self.id)        => current_record_id               ==> 4
    # print(self.env)       => odoo environment on which action is triggered ==> <odoo.api.Environment object at 0x0901DF10>
    # print(self.env.user)  => return the 'current user' (as an instance) ==> res.users(2,)
    # print(self.env.is_system()) => return whether the 'current user' has group 'Settings' or in superuser mode ? (True/False)
    # print(self.env.is_admin()) => return whether the 'current user' has group 'Access Rights' or 'Settings' or in superuser mode ? (True/False)
    # print(self.env.is_superuser()) => return whether the 'current user' in superuser mode ? (True/False)
    # print(self.env.company) => return the current company (as an instance) ==> res.company(1,)
    # print(self.env.companies) => return a recordset of the enabled companies by the user ==> res.company(1,)
    # print(self.env.company.name) => return the name of company that i use ==> YourCompany || EG Company || ...
    # print(self.env.lang) => return the current language code ==> en_US
    # print(self.env.cr) => curser ==> <odoo.sql_db.Cursor object at 0x08622530>
    # print(self.env.context)
    # # {'lang': 'en_US', 'tz': 'Africa/Cairo', 'uid': 2, 'allowed_company_ids': [1], 'params': {'id': 5, 'cids': 1, 'action': 416, 'model': 'hospital.doctor', 'view_type': 'form', 'menu_id': 239}}
    # print(self.env.context.get('uid')) => get any thing from context ('user id') => 2
    # print(self.env.context.get('params').get("id")) => get any thing from context ('current record id') => 4
    # print(self.env.ref().name)
