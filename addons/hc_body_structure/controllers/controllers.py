# -*- coding: utf-8 -*-
from openerp import http

# class HcBodyStructure(http.Controller):
#     @http.route('/hc_body_structure/hc_body_structure/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/hc_body_structure/hc_body_structure/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('hc_body_structure.listing', {
#             'root': '/hc_body_structure/hc_body_structure',
#             'objects': http.request.env['hc_body_structure.hc_body_structure'].search([]),
#         })

#     @http.route('/hc_body_structure/hc_body_structure/objects/<model("hc_body_structure.hc_body_structure"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('hc_body_structure.object', {
#             'object': obj
#         })