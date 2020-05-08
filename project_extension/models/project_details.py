# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from datetime import date, datetime
from datetime import timedelta

class ProjectDetails(models.Model):
    _name = 'project.details'
    _rec_name = 'project_id'

    project_id = fields.Many2one('project.project', string="Project Name")
    # project_duration = fields.Integer(string="Days") #####
    # project_start_date = fields.Datetime(string="Project Start Date") ####deleted
    # project_end_date = fields.Datetime(string="Project End Date") ####deleted
    # description = fields.Text(string="Description") ####deleted
    # project_scope_ids = fields.One2many('project.scope', 'project_details_id',string="Project Scope") ####deleted
    # project_team_ids = fields.One2many('project.team', 'project_details_id',string="Project Team")
    # project_documents_ids = fields.One2many('project.documents', 'project_details_id', string="Project Documents") ####deleted

    # @api.onchange('project_duration', 'project_start_date')
    # def set_date_deadline(self):
    #     if self.project_duration:
    #         dt = datetime.strptime(self.project_start_date, "%Y-%m-%d %H:%M:%S")
    #         final_dt = dt + timedelta(days=self.project_duration)
    #         self.project_end_date = final_dt
    #     if self.project_start_date:
    #         dt = datetime.strptime(self.project_start_date, "%Y-%m-%d %H:%M:%S")
    #         final_dt = dt + timedelta(days=self.project_duration)
    #         self.project_end_date = final_dt

# class ProjectScope(models.Model):
#     _name = 'project.scope'
#     _rec_name = 'project_scope_name'
#
#     project_scope_name = fields.Char(string="Project Scope Name")
#     project_details_id = fields.Many2one('project.details', string="Project Details")

# class ProjectTeam(models.Model):
#     _name = 'project.team'
#     _rec_name = 'role'
#
#     role = fields.Char(string="Role")
#     name = fields.Char(string="Name")
#     project_details_id = fields.Many2one('project.details', string="Project Details")

# class ProjectDocuments(models.Model):
#     _name = 'project.documents'
#     _rec_name = 'document_name'
#
#     date = fields.Datetime(string="Date", default=datetime.now())
#     document_name = fields.Char(string="Document Name")
#     document_type = fields.Char(string="Document Type")
#     document_size = fields.Char(string="Document Size")
#     project_details_id = fields.Many2one('project.details', string="Project Details")
