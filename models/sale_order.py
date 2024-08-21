from odoo import api, fields, models

class HospitalSaleOrder(models.Model):
    _inherit = 'sale.order'

    confirmed_user_id = fields.Many2one('res.users', string='Confirmed Users')

    def action_confirm(self):                       # override method
        super(HospitalSaleOrder, self).action_confirm()
        self.confirmed_user_id = self.env.user.id

    def _prepare_invoice(self):
        invoice_vals = super(HospitalSaleOrder, self)._prepare_invoice()
        print('===', invoice_vals)

        invoice_vals['so_confirmed_user'] = self.confirmed_user_id.id
        return invoice_vals

