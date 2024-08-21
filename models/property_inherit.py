from odoo import models, fields, api


class Property(models.Model):
    _inherit = 'property'

    garden_orientation = fields.Selection([('west2', 'West 2'),
                                           ('west3', 'West 3')])


