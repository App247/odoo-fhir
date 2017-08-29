# -*- coding: utf-8 -*-
from openerp import http

# class HcEventDefinition(http.Controller):
#     @http.route('/hc_event_definition/hc_event_definition/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/hc_event_definition/hc_event_definition/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('hc_event_definition.listing', {
#             'root': '/hc_event_definition/hc_event_definition',
#             'objects': http.request.env['hc_event_definition.hc_event_definition'].search([]),
#         })

#     @http.route('/hc_event_definition/hc_event_definition/objects/<model("hc_event_definition.hc_event_definition"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('hc_event_definition.object', {
#             'object': obj
#         })