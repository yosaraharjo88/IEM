# -*- coding: utf-8 -*-

from odoo import models, fields, api

class ProjectTaskTnherit(models.Model):
    _inherit = 'project.task'


    project_task = fields.Many2one('project.task',string='Project Task', readonly=True)



