# Copyright 2021 jeo Software
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    "name": "l10n ar withholding fix",
    "summary": "Este modulo queda depreciado porque la funcionalidad ya esta incluida en l10n_ar_ux",
    "version": "13.0.1.0.0",
    "development_status": "Alpha", # "Alpha|Beta|Production/Stable|Mature"
    "category": "Accounting",
    "website": "http://jeosoft.com.ar",
    "author": "jeo Software",
    "maintainers": ["jobiols"],
    "license": "AGPL-3",
    "application": False,
    "installable": True,
    "depends": [
        'l10n_ar_account_withholding',
        'account',
    ],
    "data": [
        'reports/report_withholding_certificate.xml',
        'views/res_config_settings_views.xml'
    ],
}
