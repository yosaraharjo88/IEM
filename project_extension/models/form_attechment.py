from odoo import api, fields, models


class Attechment(models.Model):
	_inherit = 'ir.attachment'

	owner = fields.Text('Owner')
	date_created = fields.Date('Date Created')
	description = fields.Text('Description')
	task_id = fields.Many2one('project.project', 'Task')