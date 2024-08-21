from odoo import api, fields, models

class HospitalCountry(models.Model):
    _name = "hospital.country"
    _description = "hospital country"
    _rec_name = 'country_name'

    country_name = fields.Char(string='Country')

