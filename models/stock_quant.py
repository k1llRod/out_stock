from odoo import api, fields, models, tools, _
from datetime import datetime, timedelta


class StockQuant(models.Model):
    _inherit = 'stock.quant'

    @api.model
    def create(self, vals_list):
        result = super(StockQuant, self).create(vals_list)
        product = vals_list['product_id']
        location = self.env['stock.location'].search([('id', '=', vals_list['location_id'])]).display_name
        verify = result.product_id.register_zero_line_ids.filtered(lambda x:x.products_id.id == product and x.location_id == location and x.date_end == False)
        if verify:
            verify.write({'date_end': fields.Date.today()})
        return result

    @api.model
    def _unlink_zero_quants(self):
        quants = self.search([('quantity', '=', 0)])
        product_location_ids = self.env['stock.warehouse'].search([]).mapped('lot_stock_id').ids
        filter = quants.filtered(lambda x: x.location_id.id in product_location_ids)
        for quant in filter:
            location = quant.location_id.display_name
            register_object = self.env['register.zeros']
            register_object.create({
                'register_zero_ids': quant.product_id.id,
                'products_id': quant.product_id.id,
                'product_qty': quant.quantity,
                'location_id': location,
                'date_init': datetime.now(),
            })
        res = super(StockQuant, self)._unlink_zero_quants()

        return res

    @api.depends('quantity')
    def _compute_inventory_quantity(self):
        for quant in self:
            if quant.quantity < 0 and not quant.product_id.register_zero_line_ids.filtered(lambda x: x.location_id == quant.location_id.display_name and x.date_end == False):
                location = quant.location_id.display_name
                register_object = self.env['register.zeros']
                register_object.create({
                    'register_zero_ids': quant.product_id.id,
                    'products_id': quant.product_id.id,
                    'product_qty': quant.quantity,
                    'location_id': location,
                    'date_init': datetime.now(),
                })
            else:
                pick = quant.product_id.register_zero_line_ids.filtered(lambda x: x.date_end == False and x.location_id == quant.location_id.display_name and x.product_qty < quant.quantity)
                if pick:
                    pick.write({'date_end': quant.in_date,
                                'product_qty_end': quant.quantity})
        res = super(StockQuant, self)._compute_inventory_quantity()
        return res