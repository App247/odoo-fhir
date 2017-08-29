# -*- coding: utf-8 -*-
from openerp import http

# class HcReferralRequest(http.Controller):
#     @http.route('/hc_referral_request/hc_referral_request/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/hc_referral_request/hc_referral_request/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('hc_referral_request.listing', {
#             'root': '/hc_referral_request/hc_referral_request',
#             'objects': http.request.env['hc_referral_request.hc_referral_request'].search([]),
#         })

#     @http.route('/hc_referral_request/hc_referral_request/objects/<model("hc_referral_request.hc_referral_request"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('hc_referral_request.object', {
#             'object': obj
#         })