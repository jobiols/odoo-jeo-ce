# Copyright 2020 jeo Software
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class AccountLournal(models.Model):
    _inherit = "account.journal"

    report_partner_id = fields.Many2one(
        'res.partner',
        ondelete='set null'
    )
