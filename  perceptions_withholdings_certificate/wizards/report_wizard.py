# Copyright 2021 jeo Software
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

import logging
import base64
from odoo.tools.misc import xlsxwriter
from odoo import models, api, fields, _
_logger = logging.getLogger(__name__)
from odoo.exceptions import UserError
import io


class PercepWithholdWizardReport(models.TransientModel):
    _name = "percep.withhold.wizard.report"
    _description = "Wizard del reporte de retenciones y percepciones"

    date_from = fields.Date()
    date_to = fields.Date()

    def get_payments(self, data):
        """ Recorrer los pagos buscando retenciones
        """
        domain = [('payment_date' ,'>=', self.date_from),
                  ('payment_date' ,'<=', self.date_to)]
        account_payment_ids = self.env['account.payment'].search(domain)
        return account_payment_ids


    def get_invoices(self, data):
        """ Recorrer las facturas buscando percepciones
        """
        perception_ids = self.get_perceptions(self)

        domain = [('invoice_date' ,'>=', self.date_from),
                  ('invoice_date' ,'<=', self.date_to)]
        account_move_ids = self.env['account.move'].search(domain)
        return account_move_ids

    def do_report(self):
        """ Imprimir el reporte, en planilla excel
        """
        headers = ['Cuit Retenido','Nombre Retenido','Impuesto','Monto retenido',
                   'Nro Factura', 'Nro Comprobante', 'Fecha Emisión']

        sheet_lines = list()
        # obtener los datos y ponerlos en una estructura
        for payment in self:
            line = list()
            cuit = payment.payment_group_id.partner_id.vat
            line.append(cuit)
            name = payment.payment_group_id.partner_id.name
            line.append(name)
            tax = payment.tax_withholding_id.name
            line.append(tax)
            amount = payment.amount
            line.append(amount)
            try:
                payment_group = payment.payment_group_id
                invoice = payment_group.matched_move_line_ids[0].move_id
                _date = invoice.invoice_date.strftime('%d/%m/%Y')
            except Exception as _ex:
                raise UserError(
                    _('La linea %s del pago %s no tiene un comprobante '
                        'asociado. Posiblemente falte conciliar el comprobante '
                        'con este pago.') %
                        (payment.name, payment.payment_group_id.name))
            line.append(invoice.name)
            line.append(payment.withholding_number)
            line.append(payment.payment_date)

            sheet_lines.append(line)

        # Crear planilla en memoria
        output = io.BytesIO()
        workbook = xlsxwriter.Workbook(output, {'in_memory': True})
        worksheet = workbook.add_worksheet()

        # Escribir los titulos en negrita
        bold = workbook.add_format({'bold': True})
        for col, header in enumerate(headers):
            worksheet.write(0, col, header, bold)

        # Escribir los datos
        date_format = workbook.add_format({'num_format': 'dd/mm/yyyy'})
        for row, line in enumerate(sheet_lines):
            for col, cell in enumerate(line):
                if col == 3:
                    worksheet.write(row+1, col, cell, date_format)
                else:
                    worksheet.write(row+1, col, cell)
        workbook.close()

        # encode
        output.seek(0)
        attachment_obj = self.env['ir.attachment']

        # crear el attachment
        attachment_id = attachment_obj.create({
            'name': 'erp.xlsx',
            'datas': base64.b64encode(output.read()),
            })

        return {
            'type': 'ir.actions.act_url',
            'url': '/web/content/' + str(attachment_id.id) + '?download=true',
            'target': 'new'
            }
