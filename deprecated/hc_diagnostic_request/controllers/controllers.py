# -*- coding: utf-8 -*-
from openerp import http

# class HcDiagnosticRequest(http.Controller):
#     @http.route('/hc_diagnostic_request/hc_diagnostic_request/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/hc_diagnostic_request/hc_diagnostic_request/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('hc_diagnostic_request.listing', {
#             'root': '/hc_diagnostic_request/hc_diagnostic_request',
#             'objects': http.request.env['hc_diagnostic_request.hc_diagnostic_request'].search([]),
#         })

#     @http.route('/hc_diagnostic_request/hc_diagnostic_request/objects/<model("hc_diagnostic_request.hc_diagnostic_request"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('hc_diagnostic_request.object', {
#             'object': obj
#         })