# -*- coding: utf-8 -*-
from odoo import models, fields, api


class promotion(models.Model):
    _name = 'sale.promotion'
    _description = 'sale_promotion'

    product = fields.Many2one("product.product", string="name of product",
                              ondelete='set null')

    quantity_2 = fields.Float(string="quantity", default=1.00)
    offer = fields.Float(string="offer", readonly=True, store=True)
    total_quantity = fields.Float(string="total quantity", compute="_total_quantity", store=True)
    price_2 = fields.Float(string="Price", readonly=True, store=True)
    total_2 = fields.Float(string="total", store=True)

    @api.onchange('product')
    def _price_change(self):
        self.price_2 = self.product.list_price

    @api.depends('quantity_2')
    def _total_quantity(self):
        for r in self:
            if r.quantity_2 > 2:
                r.total_quantity = r.quantity_2 + 1
                r.offer = 1.00
            else:
                r.total_quantity = r.quantity_2
                r.offer = 0.00

    @api.onchange('price_2', 'quantity_2')
    def _total_price_2(self):
        for r in self:
            r.total_2 = r.quantity_2 * r.price_2
