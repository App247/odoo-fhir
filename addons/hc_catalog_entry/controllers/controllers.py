# -*- coding: utf-8 -*-
from openerp import http

# class HcCatalogEntry(http.Controller):
#     @http.route('/hc_catalog_entry/hc_catalog_entry/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/hc_catalog_entry/hc_catalog_entry/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('hc_catalog_entry.listing', {
#             'root': '/hc_catalog_entry/hc_catalog_entry',
#             'objects': http.request.env['hc_catalog_entry.hc_catalog_entry'].search([]),
#         })

#     @http.route('/hc_catalog_entry/hc_catalog_entry/objects/<model("hc_catalog_entry.hc_catalog_entry"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('hc_catalog_entry.object', {
#             'object': obj
#         })