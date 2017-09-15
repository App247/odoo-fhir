# -*- coding: utf-8 -*-
from openerp import http

# class HcBaseMetadataType(http.Controller):
#     @http.route('/hc_base_metadata_type/hc_base_metadata_type/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/hc_base_metadata_type/hc_base_metadata_type/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('hc_base_metadata_type.listing', {
#             'root': '/hc_base_metadata_type/hc_base_metadata_type',
#             'objects': http.request.env['hc_base_metadata_type.hc_base_metadata_type'].search([]),
#         })

#     @http.route('/hc_base_metadata_type/hc_base_metadata_type/objects/<model("hc_base_metadata_type.hc_base_metadata_type"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('hc_base_metadata_type.object', {
#             'object': obj
#         })