from odoo import api, fields, models

class HospitalSaleOrderDuration(models.Model):
    _name = 'sale.order.duration'
    _description = 'Sales Orders Duration'

    start_date = fields.Date(string='Start Date')
    end_date = fields.Date(string='End Date')
