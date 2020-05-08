# -*- coding: utf-8 -*-

from odoo import models, fields, api


class Task(models.Model):
    _inherit = "project.task"

    approved_timesheet_ids = fields.One2many('account.analytic.line', 'task_id', 'Timesheets',
                                             compute="_get_timesheet_lines")

    @api.depends('stage_id', 'timesheet_ids.unit_amount', 'planned_hours', 'child_ids.stage_id',
                 'child_ids.planned_hours', 'child_ids.effective_hours', 'child_ids.children_hours', 'child_ids.timesheet_ids.unit_amount')
    def _hours_get(self):
        for task in self.sorted(key='id', reverse=True):
            children_hours = 0
            for child_task in task.child_ids:
                if child_task.stage_id and child_task.stage_id.fold:
                    children_hours += child_task.effective_hours + child_task.children_hours
                else:
                    children_hours += max(child_task.planned_hours, child_task.effective_hours + child_task.children_hours)

            task.children_hours = children_hours
            task.effective_hours = sum([x.unit_amount for x in task.timesheet_ids if x.sheet_id.state == 'done'])
            task.remaining_hours = task.planned_hours - task.effective_hours - task.children_hours
            task.total_hours = max(task.planned_hours, task.effective_hours)
            task.total_hours_spent = task.effective_hours + task.children_hours
            task.delay_hours = max(-task.remaining_hours, 0.0)

            if task.stage_id and task.stage_id.fold:
                task.progress = 100.0
            elif (task.planned_hours > 0.0):
                task.progress = round(100.0 * (task.effective_hours + task.children_hours) / task.planned_hours, 2)
            else:
                task.progress = 0.0
                
    @api.depends('timesheet_ids')
    def _get_timesheet_lines(self):
        for task in self:
            approved_timesheet_ids = []
            for timesheet in task.timesheet_ids:
                if timesheet.sheet_id.state == 'done':
                    approved_timesheet_ids.append(timesheet.id)
            task.approved_timesheet_ids = approved_timesheet_ids
