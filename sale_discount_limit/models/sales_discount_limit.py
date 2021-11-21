# -*- coding: utf-8 -*-
# Part of Odoo, Aktiv Software.
# See LICENSE file for full copyright & licensing details.


from odoo import fields, models
import odoo.addons.decimal_precision as dp


class SalesDiscountLimit(models.Model):
    """Configuration for Set Sale Discount Limit."""

    _name = "sales.discount.limit"
    _rec_name = "group_id"
    _order = "discount desc"
    _sql_constraints = [
        ('discount', 'check(discount >= 1 and discount <= 100)',
         'Discount should be between 1 to 100 percentage.'),
        ('group_id_uniq', 'unique(group_id)',
            'Group already exists!'),
    ]

    group_id = fields.Many2one(
        'res.groups', "Group", domain=lambda self: [
            ('category_id.id', '=',
                self.env.ref('base.module_category_sales_sales').id)])
    discount = fields.Float("Discount (%)",
                            digits=dp.get_precision('Discount'), default=10.0)
