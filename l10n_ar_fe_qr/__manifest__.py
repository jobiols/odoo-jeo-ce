{
    'name': 'l10n_ar_fe_qr',
    'version': '13.0.1.0.0',
    'category': 'Accounting',
    'summary': 'Agregado de QR a Factura Electrónica',
    "author": "jeo Software",
    "maintainers": ["jobiols"],
    "license": "AGPL-3",
    'depends': [
        'account',
        'l10n_ar',
        'l10n_ar_afipws_fe',
        'l10n_ar_report_fe'
    ],
    'data': [
        'views/afip_view.xml',
        'views/report_template.xml'
    ],
    'installable': True,
    'application': True,
}
