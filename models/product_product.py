# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

import logging
import re

from odoo import api, fields, models, tools, _
from odoo.exceptions import UserError, ValidationError
from odoo.osv import expression


from odoo.tools import float_compare

_logger = logging.getLogger(__name__)

class ProductTemplate(models.Model):
    _inherit = "product.template"

    register_zero_line_ids = fields.One2many('register.zeros', 'register_zero_ids', string='Log productos stock cero')

    # flag_out_of_stock = fields.Boolean(string='Producto sin stock', compute='_compute_flag_out_of_stock', store=True)
    # @api.depends('qty_available')
    # def _compute_flag_out_of_stock(self):
    #     for record in self:
    #         record.flag_out_of_stock = record.qty_available > 0

class ProductProduct(models.Model):
    _inherit = "product.product"

    register_zero_line_ids = fields.One2many('register.zeros', 'register_zero_ids', string='Log productos stock cero')
    def report_stock_cero(self):
        lines = []
        for rec in self:
            lines.append(rec.id)

        wizard_object = self.env['form.report'].create({
            'product_ids': self.ids,
        })
        return {
            'type': 'ir.actions.act_window',
            'name': 'Reporte de stock cero',
            'res_model': 'form.report',
            'view_mode': 'form',
            'target': 'new',
            'res_id': wizard_object.id,
        }


