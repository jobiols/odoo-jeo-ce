##############################################################################
#
#    Copyright (C) 2020  jeo Software  (http://www.jeosoft.com.ar)
#    All Rights Reserved.
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

{
    "name": "Standard Dependencies CE",
    "version": "15.0.1.1.0",
    "category": "Tools",
    "summary": "Add standard dependecies for ADHOC Argentinian localization "
               "on Community Edition",
    "author": "jeo Software",
    "website": "http://github.com/jobiols/odoo-addons",
    "license": "AGPL-3",
    "depends": [
        # para la localizacion argentina version Community
        "l10n_ar_ux",  # localizacion base + check + payment group + withholding

        "l10n_ar_afipws_fe",  # Factura electronica Argentina
        "l10n_ar_bank",  # Bancos Argentinos
        "base_currency_inverse_rate",  # TC en Argentino

        # "l10n_ar_stock",  # Remito electrónico Argentino tiene una rara
        # dependencia con l10n_ar_account
        # "l10n_ar_report_stock", # OJO esto instala Stock
        # Para mejorar la usabilidad
        "base_ux",  # mejoras de base
        "product_ux",  # mejoras en productos
        # "sale_ux",  # mejoras en ventas falla
        "auto_backup",  # poner el backup en: /var/odoo/backups/
        # "mail_activity_board_ux",  # quitar actividades del chatter
        # "partner_ref_unique",  # evita duplicados en referencia
        # "partner_vat_unique",  # evita duplicados numeros de referencia
        # "product_unique",  # no se pueden duplicar codigos de producto
        # "web_export_view",  # exportar cualquier vista en excel
        # "account_clean_cancelled_invoice_number",  # no esta migrado
        "web_responsive",
    ],
    "data": [],
    "demo": [],
    'installable': False,
    "auto_install": False,
    "application": False,
}
