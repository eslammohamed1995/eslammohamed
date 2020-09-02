# -*- coding: utf-8 -*-
from odoo import models, fields, api


class promotion(models.Model):
    _name = 'sale.promotion'
    _description = 'sale_promotion'

    product = fields.Selection(selection=[
        ('draft', 'Tea'),
        ('orange', 'Orange juice'),
    ], string='product', required=True)

    quantity = fields.Float(string="quantity", default=1.00)
    offer = fields.Float(string="offer", readonly=True, store=True)
    price = fields.Float(string="Price", store=True)
    total = fields.Float(string="total", store=True)

    @api.onchange('price', 'quantity')
    def _total_price(self):
        for r in self:
            r.total = r.price * r.quantity

    @api.onchange('product')
    def _price_change(self):
        if self.product == "draft":
            self.price = 10.00
        elif self.product == "orange":
            self.price = 20.00



