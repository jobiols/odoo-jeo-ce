# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models, _


class AccountTax(models.Model):
    _inherit = 'account.tax'

    sicore_tax_code = fields.Integer(
        string="Código de impuesto"
    )
