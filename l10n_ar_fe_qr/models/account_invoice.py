# -*- coding: utf-8 -*-
##############################################################################
# For copyright and license notices, see __manifest__.py file in module root
# directory
##############################################################################

import json
import base64
from io import BytesIO
import qrcode
from openerp import fields, models, api
from openerp.tools import float_repr


class AccountInvoice(models.Model):
    _inherit = 'account.invoice'

    afip_qr_code = fields.Char(
        compute='_compute_qr_code',
        string='AFIP QR Code'
    )
    afip_qr_code_img = fields.Binary(
        compute='_compute_qr_code',
        string='AFIP QR Code Image'
    )

    @api.depends('afip_auth_code')
    def _compute_qr_code(self):

        for rec in self:
            qr_code = False
            if rec.afip_auth_code and rec.afip_auth_mode in ['CAE', 'CAEA']:
                data = {
                    'ver': 1,
                    'fecha': rec.date_invoice,
                    'cuit': rec.company_id.partner_id.get_id_number_sanitize(),
                    'ptoVta': rec.journal_id.point_of_sale_number,
                    'tipoCmp': int(rec.journal_document_class_id.afip_document_class_id.afip_code), # noqa
                    'nroCmp': int(rec.invoice_number),
                    'importe': float(float_repr(rec.amount_total, precision_digits=2)),
                    'moneda': rec.currency_id.afip_code,
                    'ctz': float(float_repr(rec.currency_rate, precision_digits=6)),
                    'tipoCodAut': 'E' if rec.afip_auth_mode == 'CAE' else 'A',
                    'codAut': int(rec.afip_auth_code),
                }
                if rec.commercial_partner_id.document_number:
                    data.update({'nroDocRec': rec.commercial_partner_id.get_id_number_sanitize()}) # noqa
                if rec.commercial_partner_id.document_type_id:
                    data.update({'tipoDocRec': rec.commercial_partner_id.document_type_id.afip_code}) # noqa
                qr_code = 'https://www.afip.gob.ar/fe/qr/?p=%s' % base64.b64encode(json.dumps( # noqa
                    data, indent=None).encode('ascii')).decode('ascii') # noqa

            rec.afip_qr_code = qr_code
            rec.afip_qr_code_img = rec.make_image_qr(qr_code)

    @api.model
    def make_image_qr(self, qr_code):
        """ Generate the required QR code """
        image = False
        if qr_code:
            qr_obj = qrcode.QRCode()
            output = BytesIO()
            qr_obj.add_data(qr_code)
            qr_obj.make(fit=True)
            qr_img = qr_obj.make_image()
            qr_img.save(output)
            image = base64.b64encode(output.getvalue())
        return image
