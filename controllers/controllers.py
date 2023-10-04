# -*- coding: utf-8 -*-
# from odoo import http


# class DoctorPat(http.Controller):
#     @http.route('/doctor_pat/doctor_pat', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/doctor_pat/doctor_pat/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('doctor_pat.listing', {
#             'root': '/doctor_pat/doctor_pat',
#             'objects': http.request.env['doctor_pat.doctor_pat'].search([]),
#         })

#     @http.route('/doctor_pat/doctor_pat/objects/<model("doctor_pat.doctor_pat"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('doctor_pat.object', {
#             'object': obj
#         })
