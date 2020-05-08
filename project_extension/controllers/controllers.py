# -*- coding: utf-8 -*-
from odoo import http

# class ../../v10/jobCostingEstimation/projectExtension(http.Controller):
#     @http.route('/../../v_10/job_costing_estimation/project_extension/../../v_10/job_costing_estimation/project_extension/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/../../v_10/job_costing_estimation/project_extension/../../v_10/job_costing_estimation/project_extension/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('../../v_10/job_costing_estimation/project_extension.listing', {
#             'root': '/../../v_10/job_costing_estimation/project_extension/../../v_10/job_costing_estimation/project_extension',
#             'objects': http.request.env['../../v_10/job_costing_estimation/project_extension.../../v_10/job_costing_estimation/project_extension'].search([]),
#         })

#     @http.route('/../../v_10/job_costing_estimation/project_extension/../../v_10/job_costing_estimation/project_extension/objects/<model("../../v_10/job_costing_estimation/project_extension.../../v_10/job_costing_estimation/project_extension"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('../../v_10/job_costing_estimation/project_extension.object', {
#             'object': obj
#         })