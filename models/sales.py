# -*- coding: utf-8 -*-
from odoo import models, fields, api


class sales(models.Model):
    _inherit = "sale.order"

    add_offer_2 = fields.Boolean(string="add offer")
    discount = fields.Float(string="discount", default=2.00)

    def confirm(self):
        for r in self.env['sale.promotion'].search([]):
            if r.type == "offer":
                for line in self.order_line:
                    if (self. add_offer_2 == True) & (r.add_offers == True):
                        if (line.product_id == r.product) & (line.product_uom_qty == r.quantity):
                            vals = {
                                "product_uom_qty": r.offer_amount,
                                "order_id": self.id,
                                "product_id": r.get_product.id,
                            }
                            self.env["sale.order.line"].create(vals)
                            self. add_offer_2 = False





