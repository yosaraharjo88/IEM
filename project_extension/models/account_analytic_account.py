# -*- coding: utf-8 -*-

from odoo import _, api, fields, models


class AccountAnalyticAccount(models.Model):
    _inherit = 'account.analytic.line'

    @api.model
    def _default_employee_id(self):
        res = False
        if 'task_id' in self.env.context and self.env.context.get('task_id'):
            task = self.env['project.task'].browse(self.env.context.get('task_id'))
            employee_ids = []
            for employee in task.employee_ids:
                employee_ids.append(employee.employee_id.id)
            if len(employee_ids) > 0:
                return employee_ids[0]

        return res

    @api.model
    def _default_user_id(self):
        return self.env.user.id

    employee_id = fields.Many2one('hr.employee', string='Employee', default=_default_employee_id)
    # user_id = fields.Many2one('res.users', string='User', default=_default_user_id)


    @api.onchange('employee_id')
    def onchange_user(self):
        domain = {}
        employee_ids = []
        if 'task_id' in self.env.context and self.env.context.get('task_id'):
            task = self.env['project.task'].browse(self.env.context.get('task_id'))
            for employee in task.employee_ids:
                employee_ids.append(employee.employee_id.id)