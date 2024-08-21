from odoo import api, fields, models

class HospitalPatientTag(models.Model):
    _name = "hospital.patient.tag"
    _description = "hospital patient tag"
    _inherit = ["mail.thread", "mail.activity.mixin"]

    patient_id = fields.Many2one('hospital.patient')
    name = fields.Char(string='Tag Name', required=True)
    color = fields.Integer(string='Color')
    active = fields.Boolean(string='Active', default="True")
    nums = fields.Integer(string='Number', copy=False, default='2')
    code = fields.Text(string='Code')
    states = fields.Selection([('draft', 'Draft'),
                               ('won', 'Won')], string='Status', default='draft')

    def copy(self, default=None):
        if default is None:
            default = {}
        if not default.get('name'):    # if not equal none
            default['name'] = self.name + ' (copy)'

        return super(HospitalPatientTag, self).copy(default)

    def unlink(self):
        return super(HospitalPatientTag, self).unlink()

    def object_won(self):
        self.states = 'won'
        vals = {'doctor_name': 'galal2',
                'age': 55,
                'doctors_tags': self.name}

        self.env['hospital.doctor'].create(vals)
        s = self.env['hospital.patient'].with_context(active_test=False).search_count([])
        print(s)

    def default_get(self, fields):
        result = super(HospitalPatientTag, self).default_get(fields)

        result['nums'] = 4   # we can set default values in this way or using default attribute in the field

        print(result)       # {'active': True, 'nums': 4, 'states': 'draft'}
        print(fields)       # ['activity_ids', 'message_follower_ids', 'message_ids', 'name', 'active', 'nums', 'states']
        return result


    _sql_constraints = [
        ('unique_tag_name', 'unique(name)', 'Tag Name Must Be Unique'),
        ('check_num', 'check(nums > 0)', 'The Number Must Be Positive')
    ]
