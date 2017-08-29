# -*- coding: utf-8 -*-
from openerp import http

# class HcBodySite(http.Controller):
#     @http.route('/hc_body_site/hc_body_site/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/hc_body_site/hc_body_site/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('hc_body_site.listing', {
#             'root': '/hc_body_site/hc_body_site',
#             'objects': http.request.env['hc_body_site.hc_body_site'].search([]),
#         })

#     @http.route('/hc_body_site/hc_body_site/objects/<model("hc_body_site.hc_body_site"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('hc_body_site.object', {
#             'object': obj
#         })