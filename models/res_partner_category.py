from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

class PartnerCategory(models.Model):
    _name = 'res.partner.category'
    _inherit = ['res.partner.category', 'mail.thread']

    # => the original field:
    # name = fields.Char(string='Tag Name', required=True, translate=True)

    # the overriding one:
    name = fields.Char(tracking=True)  # the old attributes (string,required,..) will be inherited if not changed


