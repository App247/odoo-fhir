# -*- coding: utf-8 -*-
from openerp import http

# class HcTerminologyCapability(http.Controller):
#     @http.route('/hc_terminology_capability/hc_terminology_capability/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/hc_terminology_capability/hc_terminology_capability/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('hc_terminology_capability.listing', {
#             'root': '/hc_terminology_capability/hc_terminology_capability',
#             'objects': http.request.env['hc_terminology_capability.hc_terminology_capability'].search([]),
#         })

#     @http.route('/hc_terminology_capability/hc_terminology_capability/objects/<model("hc_terminology_capability.hc_terminology_capability"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('hc_terminology_capability.object', {
#             'object': obj
#         })