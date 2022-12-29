from odoo import _, api, fields, models
from odoo.exceptions import UserError

class StockImmediateTransfer(models.TransientModel):
    _inherit = 'stock.immediate.transfer'

    def process(self):
        vals = super(StockImmediateTransfer, self).process()
        if self.pick_ids.picking_type_code == 'incoming':
            picks_products = self.pick_ids.move_line_ids_without_package
            for pick_product in picks_products:
                pick = pick_product.product_id.register_zero_line_ids.filtered(lambda x: x.date_end == False and x.location_id == pick_product.location_dest_id.display_name)
                if pick:
                    pick.write({'date_end': pick_product.date,
                                'product_qty_end': pick_product.qty_done})
        # else:
        #     picks_products = self.pick_ids.move_line_ids_without_package
        #     for pick in picks_products:
        #         quant = self.env['stock.quant'].search([('quantity', '<=', 0)]).filtered(lambda x:x.product_id == pick.product_id and x.location_id == pick.location_id)
        #         if quant:
        #             location = quant.location_id.display_name
        #             register_object = self.env['register.zeros']
        #             register_object.create({
        #                      'product_id': quant.product_id.id,
        #                      'product_qty': quant.quantity,
        #                      'location_id': location,
        #                      'date_init': quant.in_date,
        #                  })
        return vals