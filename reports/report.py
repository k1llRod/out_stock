from odoo import models
from odoo.osv import expression
from datetime import datetime

class ProductZeroXLS(models.AbstractModel):
    _name = 'report.out_of_stock.report_product_zero_xls'
    _inherit = 'report.report_xlsx.abstract'
    _description = "Reporte xls"

    def generate_xlsx_report(self, workbook, data, lines):
        domain = []
        if data['form_data']['location']:
            domain = expression.AND([domain, [('location_id', '=', data['form_data']['location'])]])
        if data['form_data']['product_ids']:
            domain = expression.AND([domain, [('products_id', '=', data['form_data']['product_ids'])]])
        # if data['form_data']['date_init'] and data['form_data']['date_end']:
        #     domain = expression.AND([domain, [('date_init', '>=', data['form_data']['date_init']), ('date_end', '<=', data['form_data']['date_end'])]])
        products = self.env['register.zeros'].search(domain)
        # products = self.env['product.product'].search([('id','in',data['form_data']['product_ids'])])
        format1 = workbook.add_format({'font_size':12, 'align': 'vcenter','bold': True})
        format2 = workbook.add_format({'font_size': 11, 'align': 'vcenter'})
        format3 = workbook.add_format({'num_format': 'dd/mm/yy','font_size': 10, 'align': 'vcenter'})
        sheet = workbook.add_worksheet("product product")
        sheet.set_column('A:A', 5)
        sheet.set_column('B:B', 60)
        sheet.set_column('C:C', 30)
        sheet.set_column('D:D', 20)
        sheet.write(0, 0, 'N', format1)
        sheet.write(0, 1, 'Producto', format1)
        sheet.write(0, 2, 'C. de barras', format1)
        sheet.write(0, 3, 'Ubicacion', format1)
        sheet.write(0, 4, 'Cantidad', format1)
        sheet.write(0, 5, 'Fecha inicial', format1)
        sheet.write(0, 6, 'Fecha Actual', format1)
        sheet.write(0, 7, 'Fecha final', format1)
        sheet.write(0, 8, 'Cantidad final', format1)
        sheet.write(0, 9, 'Total dias', format1)
        sheet.write(0, 9, 'Total dias a la fecha', format1)
        c = 1
        for rec in products:
            sheet.write(c, 0,c, format2)
            sheet.write(c, 1, rec.products_id.display_name, format2)
            sheet.write(c, 2, rec.products_id.barcode, format2)
            sheet.write(c, 3, rec.location_id, format2)
            sheet.write(c, 4, rec.product_qty, format2)
            sheet.write(c, 5, rec.date_init, format3)
            sheet.write(c, 6, datetime.now(),format3)
            sheet.write(c, 7, rec.date_end, format3)
            sheet.write(c, 8, rec.product_qty_end, format2)
            sheet.write(c, 9, rec.total_days, format2)
            sheet.write(c, 10, (datetime.now().date() - rec.date_init).days, format2)
            c = c + 1
            # else:
            #     for r in rec.register_zero_ids:
            #         sheet.write(c, 2, r.location_id, format2)
            #         sheet.write(c, 3, r.date_init, format3)
            #         sheet.write(c, 4, r.date_end, format3)
            #         sheet.write(c, 5, r.total_days, format2)
            #         c = c + 1


