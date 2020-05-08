# -*- coding: utf-8 -*-

from odoo import api, models, fields, tools, _

class CrmLeadPipeline(models.Model):
	_inherit = 'hr.employee'

	user_track_history_ids = fields.One2many('timesheet.cost_change','employee_id',string="Timesheet Cost Change")

class TimesheetCostChange(models.Model):
	_name = "timesheet.cost_change"

	employee_id = fields.Many2one('hr.employee',string="Employee Id")

	created_date = fields.Datetime(string="Create Date",default=lambda self: fields.datetime.now())
	applied_date = fields.Datetime(string="Applied Date")
	description = fields.Text(string="Description")
	rate = fields.Float(string="Rate")
	modified_by = fields.Many2one('res.users',string="Modified by",default=lambda self: self.env.uid)

	@api.model
	def create(self,vals):
		res = super(TimesheetCostChange,self).create(vals)
		res.employee_id.timesheet_cost = res.rate
		return res