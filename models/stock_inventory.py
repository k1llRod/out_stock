from odoo import api, fields, models, tools, _
from datetime import datetime, timedelta


class Inventory(models.Model):
    _inherit = "stock.inventory"

    def action_check(self):
        res = super(Inventory, self).action_check()
        for line in self.line_ids:
            pick = line.product_id.register_zero_ids.filtered(
                lambda x: x.date_end == False and x.location_id == line.location_id.display_name)
            if pick:
                pick.write({'date_end': line.inventory_date,
                            'product_qty_end': line.quantity})
        return res