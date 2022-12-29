# -*- coding: utf-8 -*-
# from odoo import http


# class OutOfStock(http.Controller):
#     @http.route('/out_of_stock/out_of_stock/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/out_of_stock/out_of_stock/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('out_of_stock.listing', {
#             'root': '/out_of_stock/out_of_stock',
#             'objects': http.request.env['out_of_stock.out_of_stock'].search([]),
#         })

#     @http.route('/out_of_stock/out_of_stock/objects/<model("out_of_stock.out_of_stock"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('out_of_stock.object', {
#             'object': obj
#         })
