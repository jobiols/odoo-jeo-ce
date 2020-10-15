# Copyright 2020 jeo Software
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    "name": "l10n_ar Business Unit",
    "summary": "Module summary",
    "version": "13.0.1.0.0",
    "development_status": "Beta",  # "Alpha|Beta|Production/Stable|Mature"
    "category": "Tools",
    "website": "http://jeosoft.com.ar",
    "author": "jeo Software",
    "maintainers": ["jobiols"],
    "license": "AGPL-3",
    "application": False,
    "installable": True,
    "depends": [
        "base",
        "account",
    ],
    "data": [
        "views/account_journal_view.xml",
        "views/report_invoice.xml"
    ],
}
