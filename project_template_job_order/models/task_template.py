# -*- coding: utf-8 -*-

from odoo import fields, models, api, _


class TaskTemplate(models.Model):
    _name = 'task.template'
    _description = "Task Template"

    name = fields.Char(string='Task Title', track_visibility='always', required=True, index=True)
    description = fields.Html(string='Description')
    priority = fields.Selection([
        ('0', 'Normal'),
        ('1', 'High')
    ], default='0', index=True)
    kanban_state = fields.Selection([
        ('normal', 'In Progress'),
        ('done', 'Ready for next stage'),
        ('blocked', 'Blocked')
    ], string='Kanban State',
        default='normal',
        track_visibility='onchange',
        required=True, copy=False,
        help="A task's kanban state indicates special situations affecting it:\n"
             " * Normal is the default situation\n"
             " * Blocked indicates something is preventing the progress of this task\n"
             " * Ready for next stage indicates the task is ready to be pulled to the next stage")
    child_task_ids = fields.One2many(
        'project.task2',
        'parent_task_template_id',
        string='Child Tasks'
    )
    tag_ids = fields.Many2many('project.tags', string='Tags')
    
    planned_hours = fields.Float(string='Initially Planned Hours')
    task_weightage = fields.Float(string='Task Weightage')
    predecessor_ids = fields.One2many('project.task.predecessor', 'task_temp_id', 'Links')
    successor_ids = fields.One2many('project.task.successor', 'task_temp_id', 'Successor')
    project_id = fields.Many2one('project.project', 'Project')
    
class ProjectTaskPredecessor(models.Model):
    _inherit = 'project.task.predecessor'

    task_temp_id = fields.Many2one('task.template', 'Task Template')
    
class ProjectTaskSuccessor(models.Model):
    _inherit = 'project.task.successor'

    task_temp_id = fields.Many2one('task.template', 'Task Template')
    

class ProjectTask(models.Model):
    _name = 'project.task2'
    _description = "Project Task 2"

    parent_task_template_id = fields.Many2one(
        'task.template',
        string='Parent Task',
        readonly=True
    )
    name = fields.Char(string='Task Title', track_visibility='always', required=True, index=True)
    project_id = fields.Many2one('task.template',
                                 string='Project',
                                 default=lambda self: self.env.context.get('default_project_id'),
                                 index=True,
                                 track_visibility='onchange',
                                 change_default=True)
    planned_hours = fields.Float(string='Initially Planned Hours',
                                 help='Estimated time to do the task, usually set by the project manager when the task is in draft state.')
    remaining_hours = fields.Float(string='Remaining Hours', digits=(16, 2),
                                   help="Total remaining time, can be re-estimated periodically by the assignee of the task.")
    user_id = fields.Many2one('res.users',
                              string='Assigned to',
                              default=lambda self: self.env.uid,
                              index=True, track_visibility='always')
    description = fields.Html(string='Description')
    stage_id = fields.Many2one('project.task.type', string='Stage', track_visibility='onchange', index=True,
                               copy=False)
