# -*- coding: utf-8 -*-

from odoo import fields, models, api, _
from odoo.exceptions import ValidationError


class ProjectTemplate(models.Model):
    _name = 'project.template'
    _description = "Project Template"

    name = fields.Char(string='Project Type', track_visibility='always', required=True, index=True)
    task_ids = fields.One2many(
        'project.template.task',
        'tasks_id',
        string='Project Template',
    )
    
    duration = fields.Integer(string='Duration')


    @api.one
    @api.constrains('task_ids')
    def _check_task_weightage(self):
        # To check the total task weightage and raises validation error, if total is not 100.
        total = [x.stage_weightages for x in self.task_ids]
        if (total and sum(total) != 100):
            raise ValidationError('Total Stage Weightage should be 100')


class ProjectTemplateTask(models.Model):
    _name = 'project.template.task'
    _description = "Project Template Task"
    _order = "sequence"

    tasks_id = fields.Many2one(
        'project.template',
        string='Parent Task',
        readonly=True
    )
    stage_number = fields.Integer(
        # related='stage_id.sequence',
        string='Stage Number')
    sequence = fields.Integer(string='sequence', default=10)
    stage_weightages = fields.Float(string="Stage Weightage (%)")
    # stage_id = fields.Many2one('project.task.type', string="Stage Name", required=True)
    stage = fields.Char(string="Stage Name", required=True)
    task_template_id = fields.Many2many('task.template', 'project_template_task_id', 'task_temp_id', string="Task Name")

    def default_get(self, context=None):
        res = {}
        if self.env.context:
            context_keys = self.env.context.keys()
            next_sequence = 1
            if 'task_ids' in context_keys:
                if len(self.env.context.get('task_ids')) > 0:
                    next_sequence = len(self.env.context.get('task_ids')) + 1
            res.update({'stage_number': next_sequence})
        return res

    # for parser sequence to the Stages from project templates'task
    @api.model
    def create(self, vals):
        stages = self.env['project.task.type'].search([('id', '=', vals.get('stage_id'))])
        stages.write({'sequence': vals.get('stage_number')})
        result = super(ProjectTemplateTask, self).create(vals)
        return result

    # for parser sequence to the Stages from project templates'task
    @api.multi
    def write(self, vals):
        stages = self.env['project.task.type'].search([('id', '=', vals.get('stage_id'))])
        stages.write({'sequence': vals.get('stage_number')})
        return super(ProjectTemplateTask, self).write(vals)