# -*- coding: utf-8 -*-
from datetime import datetime
from odoo import models, fields, api
from odoo.exceptions import ValidationError


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
            if r.type == "offer":
                for line in self.line_ids:
                    if (line.product_id == r.product) & (line.quantity == r.quantity):
                        vals = {
                            "quantity": r.offer_amount,
                            "order_id": self.id,
                            "product_id": r.get_product.id
                        }
                        self.env["order.line"].create(vals)

            else:
                for line in self.line_ids:
                    if line.product_id == r.product:
                        line.discount = r.discount

    @api.constrains('line_ids')
    def _check_offer(self):
        global count
        count = 0
        for record in self.line_ids:
            if record.total == 0.00:
                count = count + 1
        if count > 1:
            raise ValidationError("you already had offer")


class product(models.Model):
    _name = 'order.line'
    _description = 'order_line'

    product_id = fields.Many2one("product.product", string="name of product",
                                 ondelete='set null')

    quantity = fields.Float(string="quantity", default=1.00)
    price = fields.Float(string="price")
    total = fields.Float(string="total", compute="_total_price")
    discount = fields.Float(string="discount")
    order_id = fields.Many2one("coffee.order", string="order_id")

    @api.depends('price', 'quantity')
    def _total_price(self):
        for r in self:
            if r.discount == 0:
                r.total = r.price * r.quantity
            else:
                r.total = r.price * r.quantity * (1.00 - r.discount / 100 * 1.00)

    @api.onchange('product_id')
    def _price_change(self):
        self.price = self.product_id.list_price
