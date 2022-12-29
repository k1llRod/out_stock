from odoo import api, fields, models, tools, _
from datetime import datetime, timedelta
from odoo.exceptions import UserError, ValidationError


class RegisterZeros(models.Model):
    _name = 'register.zeros'
    _description = 'Registrar cero stock en productos'

    products_id = fields.Many2one('product.product', string='Producto')
    product_qty = fields.Float(string='Cantidad')
    product_qty_end = fields.Float(string='Cantidad final')
    location_id = fields.Char(string='Ubicacion')
    date_init = fields.Date(string='Fecha inicial')
    date_end = fields.Date(string='Fecha final')
    total_days = fields.Integer(string='Total de días', compute='_compute_total_days', store=True)

    register_zero_ids = fields.Many2one('product.product',string='Registro cero stock', ondelete='cascade')

    @api.depends('date_init', 'date_end')
    def _compute_total_days(self):
        for record in self:
            if record.date_init and record.date_end:
                record.total_days = (record.date_end - record.date_init).days
