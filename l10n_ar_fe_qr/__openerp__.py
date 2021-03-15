# -*- coding: utf-8 -*-
{
    'name': 'l10n_ar_fe_qr',
    'version': '8.0.1.0.0',
    "author": "jeo Software",
    "maintainers": ["jobiols"],
    'category': 'Invoicing',
    'summary': 'Add QR to Invoice',
    'depends': [
        'base',
        'account',
        'l10n_ar_afipws_fe',
        'l10n_ar_aeroo_einvoice'
    ],
    'data': [
        'views/afip_invoice_form_view.xml',
        'reports/custom_reports.xml'
    ],

    'installable': True,
    'application': False,
}
