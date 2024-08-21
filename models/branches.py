from odoo import api, fields, models


class CrmBranches(models.Model):
    _inherit = 'res.branch'

    user_id = fields.Many2many('res.users', string='Branch Manager', readonly=False)


