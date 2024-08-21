from odoo import api, fields, models

class HospitalCity(models.Model):
    _name = "hospital.city3"
    _description = "hospital city"
    _rec_name = 'city_name'

    city_name = fields.Char(string='City')
    country = fields.Many2one('hospital.country', string='Country')
