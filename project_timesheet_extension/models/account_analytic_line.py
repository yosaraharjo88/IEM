# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class AccountAnalyticLine(models.Model):
    _inherit = 'account.analytic.line'

    stage_id = fields.Many2one('project.task.type', "Stage", compute="compute_task_hours")
    task_id = fields.Many2one('project.task', "Task")
    rate = fields.Float(string="Rate", compute="compute_rate_employee")

    @api.constrains('unit_amount')
    def check_daily_hour_limit(self):
        for line in self:
            timesheet_lines = self.env['account.analytic.line'].search([
                ('sheet_id', '=', line.sheet_id.id), ('date', '=', line.date),
                ('employee_id', '=', line.sheet_id.employee_id.id)])

            day_hours = 0
            for l in timesheet_lines:
                day_hours += l.unit_amount
            if day_hours > 24:
                raise ValidationError(_('Timesheet Limit Exceed 24 Hours In a Day!'))

    @api.model
    def default_get(self, fields):
        res = super(AccountAnalyticLine, self).default_get(fields)
        if 'employee_id' in self.env.context and self.env.context.get('employee_id'):
            res.update({'employee_id': self.env.context.get('employee_id')})
        return res

    @api.onchange('project_id')
    def onchange_project_id(self):
        domain = {}
        project_ids = []
        task_ids = []
        if 'employee_id' in self.env.context and self.env.context.get('employee_id'):
            projects = self.env['project.project'].search([])
            for project in projects:
                for team in project.project_team_ids:
                    if self.env.context.get('employee_id') == team.employee_id.id:
                        project_ids.append(project.id)
        if self.project_id.id:
            for task in self.project_id.task_ids:
                for emp in task.employee_ids:
                    if emp.employee_id.id == self.employee_id.id:
                        task_ids.append(task.id)
        domain = {'domain': {'project_id': [('id', 'in', project_ids)], 'task_id': [('id', 'in', task_ids)]}}
        # domain = {'domain': { 'task_id': [('id', 'in', task_ids)]}}
        return domain


    @api.depends('task_id')
    @api.onchange('task_id')
    def compute_task_hours(self):
        for line in self:
#             total_hours = 0
#             for sheet in line.task_id.timesheet_ids:
#                 if 'employee_id' in self.env.context and self.env.context.get('employee_id'):
#                     if sheet.sheet_id.state == 'done' and self.env.context.get('employee_id') == sheet.employee_id.id:
#                         total_hours += sheet.unit_amount
#             line.unit_amount = total_hours
            if line.task_id:
                line.stage_id = line.task_id.stage_id.id

    @api.depends('date')
    def compute_rate_employee(self):
        for line in self:
            if line.employee_id.id:
                total_rate = 0
                history = self.env['timesheet.cost_change'].search([
                    ('employee_id', '=', line.employee_id.id),
                    ('applied_date', '<=', line.date)
                ], order='applied_date desc', limit=1)
                line.rate = history.rate
