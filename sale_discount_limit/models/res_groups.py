# -*- coding: utf-8 -*-
# Part of Odoo, Aktiv Software.
# See LICENSE file for full copyright & licensing details.

from odoo import api, models


class Groups(models.Model):
    """Enhance the feature of the Group Object."""

    _inherit = "res.groups"

    def unlink(self):
        """While delete group, Sale Discount Limit should be delete."""
        for group in self:
            sale_discount_limit_rec = self.env['sales.discount.limit'].search([
                ('group_id', '=', group.id)])
            if sale_discount_limit_rec:
                sale_discount_limit_rec.unlink()
        return super(Groups, self).unlink()
