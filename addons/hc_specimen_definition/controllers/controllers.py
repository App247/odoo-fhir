# -*- coding: utf-8 -*-
from openerp import http

# class HcSpecimenDefinition(http.Controller):
#     @http.route('/hc_specimen_definition/hc_specimen_definition/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/hc_specimen_definition/hc_specimen_definition/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('hc_specimen_definition.listing', {
#             'root': '/hc_specimen_definition/hc_specimen_definition',
#             'objects': http.request.env['hc_specimen_definition.hc_specimen_definition'].search([]),
#         })

#     @http.route('/hc_specimen_definition/hc_specimen_definition/objects/<model("hc_specimen_definition.hc_specimen_definition"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('hc_specimen_definition.object', {
#             'object': obj
#         })