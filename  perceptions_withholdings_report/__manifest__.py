# Copyright 2021 jeo Software
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    "name": "Reporte de percepciones y retenciones",
    "summary": "Genera un archivo excel con las retenciones y percepciones",
    "version": "13.0.1.0.0",
    "development_status": "Alpha", # "Alpha|Beta|Production/Stable|Mature"
    "category": "Accounting",
    "website": "http://jeosoft.com.ar",
    "author": "jeo Software",
    "maintainers": ["jobiols"],
    "license": "AGPL-3",
    "application": False,
    "installable": True,
    "external_dependencies": {
        "python": ['xlsxwriter'],
    },
    "depends": [
        "account",
    ],
    "data": [
        "views/report_menu_view.xml",
        "wizards/report_wizard_view.xml"
    ],
}
