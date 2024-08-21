from odoo import api, fields, models

class HospitalSaleReport(models.Model):
    _inherit = 'sale.report'

    confirmed_user_id = fields.Many2one('res.users', string='Confirmed Userss', readonly=True)

    def _query(self, with_clause='', fields={}, groupby='', from_clause=''):
        fields['confirmed_user_id'] = ", s.confirmed_user_id"
        return super(HospitalSaleReport, self)._query(with_clause, fields, groupby, from_clause)
