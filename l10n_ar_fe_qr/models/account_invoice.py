from odoo import fields, models
import json
import base64
import qrcode

class AccountInvoice(models.Model):
    _inherit = 'account.invoice'

    def _compute_qr(self):
        for rec in self:
            dict_invoice = ''
            if rec.type in ['out_invoice', 'out_refund'] and \
               rec.state == 'open' and \
               rec.afip_auth_code != '':
                try:
                    dict_invoice = {
                        'ver': '1',
                        'fecha': rec.date_invoice,
                        'cuit': rec.company_id.partner_id.main_id_number,
                        'ptoVta': rec.journal_id.point_of_sale_number,
                        'tipoCmp': rec.document_type_id.code,
                        'nroCmp': rec.invoice_number,
                        'importe': rec.amount_total,
                        'moneda': rec.currency_id.afip_code,
                        'ctz': rec.currency_rate,
                        #'tipoDocRec': int(rec.partner_id.l10n_latam_identification_type_id.l10n_ar_afip_code), ##
                        #'nroDocRec': int(rec.partner_id.main_id_number), # OK
                        'tipoCodAut': 'E',
                        'codAut': rec.afip_auth_code, # OK
                        }
                except:
                    dict_invoice = 'ERROR'
                    pass
                res = str(dict_invoice)
            else:
                res = 'N/A'
            rec.json_qr = res
            if type(dict_invoice) == dict:
                enc = res.encode()
                b64 = base64.encodestring(enc)
                rec.texto_modificado_qr = 'https://www.afip.gob.ar/fe/qr/?p=' + str(b64)
            else:
                rec.texto_modificado_qr = 'https://www.afip.gob.ar/fe/qr/?ERROR'

            _qr = qrcode.QRCode(version=1,
                                error_correction=qrcode.constants.ERROR_CORRECT_L,
                                box_size=10,
                                border=4)

            _qr.add_data(rec.texto_modificado_qr)
            _qr.make(fit=True)
            img = _qr.make_image(fill='black', back_color='white')
            a = img.tobytes()

            img.save('/opt/odoo/etc/cacao1.jpeg')
            with open('/opt/odoo/etc/cacao1.jpeg', 'rb') as f:
                 im = base64.b64encode(f.read())

            rec.image_qr = im

    json_qr = fields.Char(
        'JSON QR AFIP',
        compute=_compute_qr
    )
    texto_modificado_qr = fields.Char(
        'Texto Modificado QR',
        compute=_compute_qr
    )
    image_qr = fields.Binary(
        compute=_compute_qr,
        string="AFIP Barcode Image"
    )

# In the ODT file, create a Frame object (Insert > Frame > Frame).
# Go to tab "Options" and fill the "Name" field with the following code:
# image: asimage(o.image_qr, size_x=90,size_y=90,hold_ratio=True)
