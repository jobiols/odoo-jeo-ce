# -*- coding: utf-8 -*-
# Part of Odoo, Aktiv Software
# See LICENSE file for full copyright & licensing details.

# Author: Aktiv Software
# mail:   odoo@aktivsoftware.com
# Copyright (C) 2015-Present Aktiv Software
# Contributions:
#           Aktiv Software:
#              - Fatemi Lokhandwala
#              - Kinjal Lalani
#              - Surabh Yadav
#              - Tanvi Gajera

{
    'name': "Sale Discount Limit",
    'summary': """
            Sale Discount Limit based on Sales User Access Right.
             """,
    'description': """
        Sale Discount Limit based on Sales User Access Right.
        Like Sales Manager can giver maximum 15% Discount,
        Sales User can give maximum 10% Discount.
    """,
    'author': "Aktiv Software",
    'website': "http://www.aktivsoftware.com",
    'license': "AGPL-3",
    'category': 'Sales',
    'version': '13.0.1.0.0',
    'depends': ['sale_management'],
    'data': [
        'security/ir.model.access.csv',
        'views/sales_discount_limit_view.xml',
    ],
    'images': ['static/description/banner.jpg'],
    'installable': True,
    'post_init_hook': '_fill_sales_discount_limit',
}
