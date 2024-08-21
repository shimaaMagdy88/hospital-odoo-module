from odoo import api, fields, models

class HospitalOperation(models.Model):
    _name = "hospital.operation"
    _description = "hospital operation"
    _order = 'sequence,id'

    operation_name = fields.Char(string='Operation Name')
    doctor_id = fields.Many2one('res.users', string='Doctor')
    record = fields.Reference(selection=[('hospital.patient', 'Patient'),
                                         ('hospital.patient.tag', 'Tag')], string='Record')
    sequence = fields.Integer(string='String', default=10)

    @api.model
    def name_create(self, name):
        print('-----', name)
        return self.create({'operation_name': name}).name_get()[0]
