# -*- coding: utf-8 -*-
# Part of Odoo, Aktiv Software.
# See LICENSE file for full copyright & licensing details.

from . import models
from odoo import api, SUPERUSER_ID


def _fill_sales_discount_limit(cr, registry):
    env = api.Environment(cr, SUPERUSER_ID, {})
    for group in env['res.groups'].search([
            ('category_id.id', '=',
                env.ref('base.module_category_sales_sales').id)]):
        env['sales.discount.limit'].create({'group_id': group.id})
