# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models, _
from odoo.tools import date_utils
from datetime import date, timedelta, datetime
import base64
import calendar
from odoo.exceptions import UserError

# Diseno de registro de exportacion segun documento en la carpeta doc

WITHHOLDING = '6'
PERCEPTION = '7'


class AccountExportSicore(models.Model):
    _name = 'account.export.sicore'
    _description = 'account.export.sicore'

    year = fields.Integer(
        default=lambda self: self._default_year(),
        help='año del periodo',
        string='Año'
    )
    month = fields.Integer(
        default=lambda self: self._default_month(),
        help='mes del periodo',
        string='Mes'
    )
    period = fields.Char(
        compute="_compute_period",
        string='Periodo'
    )
    quincena = fields.Selection(
        [('0', 'Mensual'),
         ('1', 'Primera'),
         ('2', 'Segunda')],
        default=0
    )
    doc_type = fields.Selection(
        [
            (WITHHOLDING, 'Retencion'),
            (PERCEPTION, 'Percepcion')
        ],
        string="Tipo de archivo",
        default="6"
    )
    date_from = fields.Date(
        'Desde',
        readonly=True,
        compute="_compute_dates"
    )
    date_to = fields.Date(
        'Hasta',
        readonly=True,
        compute="_compute_dates"
    )
    export_sicore_data = fields.Text(
        'Contenido archivo'
    )
    export_sicore_file = fields.Binary(
        'Descargar Archivo',
        compute="_compute_files",
        readonly=True
    )
    export_sicore_filename = fields.Char(
        'Archivo sicore',
        compute="_compute_files",
        readonly=True
    )

    def name_get(self):
        res = []
        for rec in self:
            res.append((rec.id, '%s%.2d' % (rec.year, rec.month)))
        return res

    @staticmethod
    def _last_month():
        today = date.today()
        first = today.replace(day=1)
        return first - timedelta(days=1)

    def _default_year(self):
        return self._last_month().year

    def _default_month(self):
        return self._last_month().month

    @api.onchange('year', 'month')
    def _compute_period(self):
        for reg in self:
            reg.period = '%s/%s' % (reg.year, reg.month)

    @api.onchange('year', 'month', 'quincena', 'doc_type')
    def _compute_dates(self):
        """ Dado el mes y el año calcular el primero y el ultimo dia del
            periodo
        """
        for rec in self:
            # Las retenciones se hacen por mes
            if rec.doc_type == WITHHOLDING:
                rec.quincena = 0

            month = rec.month
            year = int(rec.year)

            _ds = fields.Date.to_date('%s-%.2d-01' % (year, month))
            _de = date_utils.end_of(_ds, 'month')

            if rec.quincena == '1':
                _ds = datetime(year, month, 1)
                _de = datetime(year, rec.month, 15)
            if rec.quincena == '2':
                _ds = datetime(year, month, 16)
                last_day = calendar.monthrange(year, rec.month)[1]
                _de = datetime(year, month, last_day)

            rec.date_from = _ds
            rec.date_to = _de

    @api.depends('export_sicore_data')
    def _compute_files(self):
        for rec in self:
            # segun vimos aca la afip espera "ISO-8859-1" en vez de utf-8
            # filename sicore-30708346655-201901.txt

            if not rec.env.company.vat:
                raise UserError(_('No tiene configurado el CUIT para esta compañia'))

            cuit = rec.env.company.vat
            if rec.date_from and rec.date_to:
                _date = '%s%s' % (rec.date_from.year, rec.date_from.month)
            else:
                _date = '000000'

            filename = 'sicore-%s-%s.txt' % (cuit, _date)
            rec.export_sicore_filename = filename
            if rec.export_sicore_data:
                rec.export_sicore_file = base64.encodebytes(
                    rec.export_sicore_data.encode('ISO-8859-1'))
            else:
                rec.export_sicore_file = False

    def get_withholding_payments(self):
        """ Obtiene los pagos a proveedor que son retenciones y que
            estan en el periodo seleccionado
        """
        return self.env['account.payment'].search([
            ('payment_date', '>=', self.date_from),
            ('payment_date', '<=', self.date_to),
            ('state', '=', 'posted'),
            ('journal_id.inbound_payment_method_ids.code', '=', 'withholding')]
        )

    def get_perception_invoices(self):
        """ Obtiene las facturas de cliente que tienen percepciones y que
            estan en el periodo seleccionado.
        """

        # busco el id de la etiqueta que marca los impuestos de Ganancias
        name = 'Ret/Perc SICORE Aplicada'
        account_tag_obj = self.env['account.account.tag']
        percSICORE = account_tag_obj.search([('name', '=', name)]).id

        invoice_obj = self.env['account.invoice']
        invoices = invoice_obj.search([
            ('date_invoice', '>=', self.date_from),
            ('date_invoice', '<=', self.date_to),
            ('state', 'in', ['open', 'paid']),
            ('type', 'in', ['out_invoice', 'out_refund'])
        ])
        ret = invoice_obj

        for inv in invoices:
            if any([tax for tax in inv.tax_line_ids
                    if percSICORE in tax.tax_id.tag_ids.ids]):
                ret += inv
        return ret

    def compute_sicore_data(self):
        line = ''
        for rec in self:
            if rec.doc_type == WITHHOLDING:

                # Retenciones
                payments = self.get_withholding_payments()
                data = []
                for payment in payments:

                    # Campo 01 -- Código de comprobante
                    code = '1'
                    line = code.zfill(2)

                    # Campo 02 -- Fecha de emision del comprobante
                    _date = payment.payment_date.strftime('%d/%m/%Y')
                    line += _date

                    # Campo 03 -- Numero comprobante
                    try:
                        line += payment.withholding_number[0:16].zfill(16)
                    except Exception as _ex:
                        raise UserError(_('El pago %s no tiene numero de '
                                          'comprobante') % payment.name) from _ex

                    # Campo 04 -- Importe del comprobante
                    amount = '{:.2f}'.format(payment.amount)
                    line += amount.zfill(16)

                    # Campo 05 Código de impuesto
                    code = '0'
                    line += amount.zfill(4)

                    # Campo 06 Código de régimen
                    code = '0'
                    line += amount.zfill(3)

                    # Campo 07 Código de operación
                    code = '0'
                    line += amount.zfill(1)

                    # Campo 07 Base de Cálculo
                    amount = '{:.2f}'.format(0)
                    line += amount.zfill(14)

                    # Campo 08 Fecha de emisión de la retención
                    _date = fields.Date.today().strftime('%d/%m/%Y')
                    line += _date

                    # Campo 09 Código de condición
                    code = '0'
                    line += code.zfill(2)

                    # Campo 10 Retención practicada a sujetos suspendidos según:
                    code = '0'
                    line += code.zfill(1)

                    # Campo 10 Importe de la retencion
                    amount = '{:.2f}'.format(1.1)
                    line += amount.zfill(14)

                    # Campo 11 Porcentaje de exclusión
                    amount = '{:.2f}'.format(1.1)
                    line += amount.zfill(6)

                    # Campo 12 Fecha publicación o de finalización de la vigencia
                    _date = fields.Date.today().strftime('%d/%m/%Y')
                    line += _date

                    # Campo 13 Tipo de documento del retenido
                    code = '0'
                    line += code.zfill(2)

                    # Campo 14 Número de documento del retenido
                    cuit = payment.payment_group_id.partner_id.vat
                    line += cuit.zfill(20)

                    # Campo 15 Número certificado original
                    number = '0'
                    line += number.zfill(14)

                    data.append(line)
            else:
                #  Percepciones
                # traer todas las facturas con percepciones en el periodo
                invoices = rec.get_perception_invoices()
                data = []
                for invoice in invoices:

                    # puede haber varios impuestos de percepcion en la factura
                    perception_taxes = invoice.tax_line_ids.filtered(
                        lambda r: r.tax_id.tax_group_id.type == 'perception')

                    for tax in perception_taxes:
                        # Campo 01 -- Código de comprobante
                        code = '1'
                        line = code.zfill(2)

                        # Campo 02 -- Fecha de emision del comprobante
                        _date = payment.payment_date.strftime('%d/%m/%Y')
                        line += _date

                        # Campo 03 -- Numero comprobante
                        try:
                            line += payment.withholding_number[0:16].zfill(16)
                        except Exception as _ex:
                            raise UserError(_('El pago %s no tiene numero de '
                                            'comprobante') % payment.name) from _ex

                        # Campo 04 -- Importe del comprobante
                        amount = '{:.2f}'.format(payment.amount)
                        line += amount.zfill(16)

                        # Campo 05 Código de impuesto
                        code = '0'
                        line += amount.zfill(4)

                        # Campo 06 Código de régimen
                        code = '0'
                        line += amount.zfill(3)

                        # Campo 07 Código de operación
                        code = '0'
                        line += amount.zfill(1)

                        # Campo 07 Base de Cálculo
                        amount = '{:.2f}'.format(0)
                        line += amount.zfill(14)

                        # Campo 08 Fecha de emisión de la retención
                        _date = fields.Date.today().strftime('%d/%m/%Y')
                        line += _date

                        # Campo 09 Código de condición
                        code = '0'
                        line += code.zfill(2)

                        # Campo 10 Retención practicada a sujetos suspendidos según:
                        code = '0'
                        line += code.zfill(1)

                        # Campo 10 Importe de la retencion
                        amount = '{:.2f}'.format(1.1)
                        line += amount.zfill(14)

                        # Campo 11 Porcentaje de exclusión
                        amount = '{:.2f}'.format(1.1)
                        line += amount.zfill(6)

                        # Campo 12 Fecha publicación o de finalización de la vigencia
                        _date = fields.Date.today().strftime('%d/%m/%Y')
                        line += _date

                        # Campo 13 Tipo de documento del retenido
                        code = '0'
                        line += code.zfill(2)

                        # Campo 14 Número de documento del retenido
                        cuit = payment.payment_group_id.partner_id.vat
                        line += cuit.zfill(20)

                        # Campo 15 Número certificado original
                        number = '0'
                        line += number.zfill(14)

                        # # Campo 2 Cuit Agente
                        # cuit = invoice.partner_id.vat
                        # line = cuit

                        # # Campo 3 -- Fecha de la percepcion
                        # _date = invoice.date_invoice.strftime('%d/%m/%Y')
                        # line += _date

                        # # Campo 4 -- Numero comprobante
                        # line += invoice.document_number[0:16].zfill(16)

                        # # Campo 5 -- Importe de percepcion
                        # # ver si es invoice o refund
                        # invoice = invoice.type == 'in_invoice'
                        # amount = tax.amount if invoice else -tax.amount
                        # line += '{:.2f}'.format(amount).zfill(11)

                data.append(line)

            rec.export_sicore_data = '\n'.join(data)