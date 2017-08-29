# -*- coding: utf-8 -*-
from openerp import http

# class HcDataElement(http.Controller):
#     @http.route('/hc_data_element/hc_data_element/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/hc_data_element/hc_data_element/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('hc_data_element.listing', {
#             'root': '/hc_data_element/hc_data_element',
#             'objects': http.request.env['hc_data_element.hc_data_element'].search([]),
#         })

#     @http.route('/hc_data_element/hc_data_element/objects/<model("hc_data_element.hc_data_element"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('hc_data_element.object', {
#             'object': obj
#         })