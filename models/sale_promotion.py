# -*- coding: utf-8 -*-
from odoo import models, fields, api


class promotion(models.Model):
    _name = 'sale.promotion'
    _description = 'sale_promotion'
    _rec_name = "product"

    type = fields.Selection(selection=[
        ('draft', 'discount'),
        ('offer', 'buy x get y'),
    ], string='Type', required=True)
    product = fields.Many2one("product.product", string="product")
    add_offers = fields.Boolean()
    quantity = fields.Float(string="quantity", default=1.00)
    get_product = fields.Many2one("product.product", string="get product")
    offer_amount = fields.Float(string="offer amount", default=2.00)
    discount = fields.Float(string="discount", default=2.00)
