from datetime import date
from odoo import api, fields, models

class HospitalPatient(models.Model):
    _name = "odoo.playground"
    _description = "odoo playground"
    _inherit = ["mail.thread", "mail.activity.mixin"]

    model_id = fields.Many2one('ir.model', string='Model')
    code = fields.Text(string='Code')
    result = fields.Text(string='Result')

    # def action_execution(self):
    #     try:
    #         if self.model_id:
    #             model = self.env[self.model_id.model]
    #         else:
    #             model = self
    #         self.result = safe_eval(self.code.strip()), {'self', model})
    #     except Exception as e:
    #         self.result = str(e)

