{
    'name': 'l10n_ar_fe_qr',
    'version': '11.0.1.0.0',
    "author": "jeo Software",
    "maintainers": ["jobiols"],
    'category': 'l10n_ar_fe_qr',
    'summary': 'Add QR to Invoice',
    'depends': [
        'account',
        'l10n_ar_afipws_fe',
    ],
    'data': [
#        'views/afip_invoice_form_view.xml',
        'reports/custom_reports.xml'
    ],
    'installable': True,
    'application': True,
}
