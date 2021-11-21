# -*- coding: utf-8 -*-

from odoo.tests import common


class TestSaleDiscountLimit(common.TransactionCase):
    """Test Over Discount Sale Order."""

    def setUp(self):
        """Create a Sale User."""
        super(TestSaleDiscountLimit, self).setUp()
        self.sale_user = self.env['res.users'].with_context(
            {'no_reset_password': True}).create(dict(
                name="SaleUser",
                company_id=self.env.ref('base.main_company').id,
                login="saleuser",
                email="saleuser@test.com",
                groups_id=[(6, 0, [self.env.ref(
                    'sales_team.group_sale_salesman_all_leads').id,
                    self.env.ref('sale.group_discount_per_so_line').id])]
            ))

    def test_sale_discount_limit(self):
        """Throw an exception of more discount using Sale Order."""
        product = self.env.ref('product.product_product_5')
        partner = self.env.ref('base.res_partner_2')
        with self.assertRaises(Exception):
            self.env['sale.order'].sudo(self.sale_user.id).create({
                'partner_id': partner.id,
                'partner_invoice_id': partner.id,
                'partner_shipping_id': partner.id,
                'order_line': [(0, 0, {
                    'name': product.name, 'product_id': product.id,
                    'product_uom_qty': 2, 'product_uom': product.uom_id.id,
                    'price_unit': product.list_price,
                    'discount': 125.00,
                })],
                'pricelist_id': self.env.ref('product.list0').id,
            })
