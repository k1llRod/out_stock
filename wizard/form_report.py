# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import UserError
from datetime import datetime

class FormReport(models.TransientModel):
    _name = 'form.report'

    date_init = fields.Date('Fecha de inicio')
    date_end = fields.Date('Fecha de fin')
    location_ids = fields.Many2one('stock.warehouse', string='Almacén')
    location = fields.Char('Ubicacion', related='location_ids.lot_stock_id.complete_name')
    product_ids = fields.Many2many('product.product', string='Productos')
    def generate_report(self):
        products = self.env['product.product'].search([('id','in',self.product_ids.ids)])
        data = {
            'products': products,
            'form_data': self.read()[0]
        }
        return self.env.ref('out_of_stock.report_product_zero_xlsx').report_action(self, data=data)


