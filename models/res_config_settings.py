from odoo import api, exceptions, fields, models, _


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    cancel_days = fields.Integer(string='Cancel Days', config_parameter='om_hospital.cancel_days')

    # attribute: config_parameter: to enable saving of this field value in the sitting page
