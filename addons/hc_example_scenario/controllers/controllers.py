# -*- coding: utf-8 -*-
from openerp import http

# class HcExampleScenario(http.Controller):
#     @http.route('/hc_example_scenario/hc_example_scenario/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/hc_example_scenario/hc_example_scenario/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('hc_example_scenario.listing', {
#             'root': '/hc_example_scenario/hc_example_scenario',
#             'objects': http.request.env['hc_example_scenario.hc_example_scenario'].search([]),
#         })

#     @http.route('/hc_example_scenario/hc_example_scenario/objects/<model("hc_example_scenario.hc_example_scenario"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('hc_example_scenario.object', {
#             'object': obj
#         })