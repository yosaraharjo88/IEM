# -*- coding: utf-8 -*-
from odoo import models, fields, api, _



class CalenderEvent(models.Model):
	_inherit = "calendar.event"

	
	@api.multi
	def _get_project_meeting(self):
		print ("/////////////////////////////////////////////////")
		for val in self:
			if val.project_id:
				val.is_project_meeting = True
			print (self._context,"+++++++++++++++++++++++++",val.is_project_meeting)


	project_id = fields.Many2one('project.project',"Project")
	p_document_ids = fields.One2many('p.document','calender_event_id',"Project Document")
	is_project_meeting = fields.Boolean("Is project",compute="_get_project_meeting")





class Project(models.Model):
	_inherit = "project.project"


	@api.multi
	def _compute_p_meeting_count(self):
		meeting_data = self.env['calendar.event'].read_group([('project_id', 'in', self.ids)], ['project_id'], ['project_id'])
		mapped_data = {m['project_id'][0]: m['project_id_count'] for m in meeting_data}
		for lead in self:
			lead.p_meeting_count = mapped_data.get(lead.id, 0)

	p_meeting_count = fields.Integer('# Meetings', compute='_compute_p_meeting_count')
	

	@api.multi
	def action_schedule_project_meeting(self):
		""" Open meeting's calendar view to schedule meeting on current opportunity.
			:return dict: dictionary value for created Meeting view
		"""
		self.ensure_one()
		action = self.env.ref('calendar.action_calendar_event').read()[0]
		partner_ids = self.env.user.partner_id.ids
		if self.partner_id:
			partner_ids.append(self.partner_id.id)
		action['context'] = {
			"search_default_project_id": self.id ,
			'default_project_id': self.id ,
			'default_partner_id': self.partner_id.id,
			'is_project_metting':True
			# 'default_partner_ids': partner_ids,
			# 'default_project_id': self.id,
			# 'default_name': self.name,
		}
		print ("&********************8",action['context'])
		return action

class ProjectDocument(models.Model):
	_name = "p.document"

	calender_event_id = fields.Many2one('project.project',"Project")
	name = fields.Char("Uploaded By Type")
	document_attch = fields.Binary("Document / File")
	file_type = fields.Text("File Type")
	uploaded_by = fields.Text("Uploaded By",default=lambda self: self.env.user.name,)
	discription = fields.Text("Description")




	@api.onchange('name')
	def get_extension(self):
		
		if self.name:
			print (">>>>>>>>>>>>>>>>>>>>>>",self.name)
			file_extension = self.name.split(".")[-1]
			self.file_type = file_extension
			file_name = self.name.split(".")[0]
			self.file_name = file_name


