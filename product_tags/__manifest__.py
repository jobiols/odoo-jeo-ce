# Copyright 2020 jeo Software
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    "name": "Product Tags",
    "summary": "Add product Tags",
    "version": "15.0.1.0.0",
    "development_status": "Production/Stable",
    "category": "Tools",
    "website": "http://jeosoft.com.ar",
    "author": "jeo Software",
    "maintainers": ["jobiols"],
    "license": "AGPL-3",
    "depends": ["base", 'product', 'stock'],
    "data": ["security/ir.model.access.csv", "views/product_view.xml"],
    "demo": ["demo/product_tags.xml"],
    "application": False,
    "installable": False,
}
