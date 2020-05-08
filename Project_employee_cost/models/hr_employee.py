# -*- coding: utf-8 -*-

from odoo import api, models, fields, tools, _
from datetime import datetime, date


class CrmLeadPipeline(models.Model):
    _inherit = 'hr.employee'

    user_track_history_ids = fields.One2many(
        'timesheet.cost_change', 'employee_id', string="Timesheet Cost Change")


class TimesheetCostChange(models.Model):
    _name = "timesheet.cost_change"
    _order = 'applied_date desc'

    employee_id = fields.Many2one('hr.employee', string="Employee Id")
    created_date = fields.Datetime(
        string="Creation Date", default=lambda self: fields.datetime.now())
    applied_date = fields.Date(string="Date Applied")
    description = fields.Text(string="Description")
    rate = fields.Float(string="Rate")
    modified_by = fields.Many2one(
        'res.users', string="Modified by", default=lambda self: self.env.uid)

    @api.model
    def create(self, vals):
        res = super(TimesheetCostChange, self).create(vals)
        today_date = datetime.now().strftime('%Y-%m-%d')
        history_ids = res.employee_id.user_track_history_ids
        if vals.get('applied_date', False):
            apply_date = vals.get('applied_date') and datetime.strptime(
                vals.get('applied_date'), '%Y-%m-%d')
            apply_date = apply_date.strftime('%Y-%m-%d')
            if len(history_ids) == 1:
                if apply_date <= today_date:
                    res.employee_id.timesheet_cost = res.rate
            for rec in history_ids:
                if rec.id != res.id:
                    if rec.applied_date <= apply_date and apply_date <= today_date:
                        res.employee_id.timesheet_cost = res.rate
        return res

    @api.multi
    def write(self, vals):
        res = super(TimesheetCostChange, self).write(vals)
        today_date = datetime.now().strftime('%Y-%m-%d')
        history_ids = self.employee_id.user_track_history_ids
        if vals.get('applied_date', False):
            apply_date = vals.get('applied_date') and datetime.strptime(
                vals.get('applied_date'), '%Y-%m-%d')
            apply_date = apply_date.strftime('%Y-%m-%d')
            if len(history_ids) == 1:
                if apply_date <= today_date:
                    self.employee_id.timesheet_cost = self.rate
            for rec in history_ids:
                if rec.id != self.id:
                    if rec.applied_date <= apply_date and apply_date <= today_date:
                        self.employee_id.timesheet_cost = self.rate
        return res

    @api.model
    def timesheet_cost_change_schedular(self):
        today_datetime = datetime.now().strftime('%Y-%m-%d')
        for rec in self.search([]):
            if rec.applied_date == today_datetime:
                rec.employee_id.timesheet_cost = rec.rate
