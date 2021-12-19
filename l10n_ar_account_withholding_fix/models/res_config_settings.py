# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    withholding_signer_name = fields.Char(
        string="Firma del responsable",
    )
    withholding_signer_position = fields.Char(
        string="Cargo del responsable",
    )

    withholding_singner_sign = fields.Image(
        string='Firma:',
        related='company_id.l10n_ar_report_signature',
        readonly=False
    )

    def clean_signature(self):
        self.withholding_signer_name = False
        self.withholding_signer_position = False
        self.withholding_singner_sign = False
