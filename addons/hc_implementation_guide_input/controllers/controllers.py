# -*- coding: utf-8 -*-
from openerp import http

# class HcImplementationGuideInput(http.Controller):
#     @http.route('/hc_implementation_guide_input/hc_implementation_guide_input/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/hc_implementation_guide_input/hc_implementation_guide_input/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('hc_implementation_guide_input.listing', {
#             'root': '/hc_implementation_guide_input/hc_implementation_guide_input',
#             'objects': http.request.env['hc_implementation_guide_input.hc_implementation_guide_input'].search([]),
#         })

#     @http.route('/hc_implementation_guide_input/hc_implementation_guide_input/objects/<model("hc_implementation_guide_input.hc_implementation_guide_input"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('hc_implementation_guide_input.object', {
#             'object': obj
#         })