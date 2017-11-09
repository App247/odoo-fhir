# -*- coding: utf-8 -*-
from openerp import http

# class HcImplementationGuideOutput(http.Controller):
#     @http.route('/hc_implementation_guide_output/hc_implementation_guide_output/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/hc_implementation_guide_output/hc_implementation_guide_output/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('hc_implementation_guide_output.listing', {
#             'root': '/hc_implementation_guide_output/hc_implementation_guide_output',
#             'objects': http.request.env['hc_implementation_guide_output.hc_implementation_guide_output'].search([]),
#         })

#     @http.route('/hc_implementation_guide_output/hc_implementation_guide_output/objects/<model("hc_implementation_guide_output.hc_implementation_guide_output"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('hc_implementation_guide_output.object', {
#             'object': obj
#         })