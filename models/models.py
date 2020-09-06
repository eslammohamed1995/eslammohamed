# -*- coding: utf-8 -*-
from datetime import datetime
from odoo import models, fields, api


class order(models.Model):
    _name = 'coffee.order'
    _description = 'coffee_order'
    _rec_name = "customer"

    customer = fields.Many2one("res.partner", ondelet="set null", string="customer name",
                               required=True)
    date = fields.Date(string="date", default=datetime.today())
    number = fields.Char(string="Task No", readonly=True, copy=False, default='New')
    description = fields.Text(string="description")
    line_ids = fields.One2many("order.line", "order_id", string="line_id")

    @api.model
    def create(self, vals):
        vals['number'] = self.env['ir.sequence'].next_by_code('coffe.order')
        result = super(order, self).create(vals)
        return result

    def confirm(self):
        for r in self.env['sale.promotion'].search([]):
            for line in self.line_ids:
                if (line.product_id == r.product) & (line.quantity == r.quantity):
                    vals = {
                        "quantity": r.offer_amount,
                        "order_id": self.id,
                        "product_id":r.get_product.id
                    }
                    self.env["order.line"].create(vals)



class product(models.Model):
    _name = 'order.line'
    _description = 'order_line'

    product_id = fields.Many2one("product.product", string="name of product",
                                 ondelete='set null')

    quantity = fields.Float(string="quantity", default=1.00)
    price = fields.Float(string="price")
    total = fields.Float(string="total", compute="_total_price")
    order_id = fields.Many2one("coffee.order", string="order_id")
    discount = fields.float(string="discount")

    @api.depends('price', 'quantity')
    def _total_price(self):
        for r in self:
            r.total = r.price * r.quantity

    @api.onchange('product_id')
    def _price_change(self):
        self.price = self.product_id.list_price
