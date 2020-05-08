from odoo import api, fields, models
# from pygments.lexer import _inherit


class ProjectHM(models.Model):
	_inherit = 'project.project'
	
	project_current_task_id = fields.Integer('Project current task', compute='_get_current_task')
	
	@api.multi
	def _get_current_task(self):
		if self._context:
			context_keys = self._context.keys()
			
			if 'default_project_current_task_id' in context_keys:
				self.project_current_task_id = self._context.get('default_project_current_task_id', 0)
			


class Attechment(models.Model):
	_inherit = 'ir.attachment'
	
	issue_id = fields.Many2one("project.issue", 'Issue')
    	
class ProjectIssue(models.Model):
    _inherit = "project.issue"
    
    
    @api.model
    def _get_default_task_id(self):
        task_id = self.env.context.get('project_current_task_id', False)
        if not task_id:
            return False
        return task_id
    
    
    image = fields.Binary("Photo", attachment=True, copy=False)
    image_lines = fields.One2many('ir.attachment', 'issue_id', string='Images', copy=False)
    issue_found_date = fields.Date("Issue Found Date", required=True)
    issue_solved_date = fields.Date("Issue Solved Date")
    state = fields.Selection([
        ('found', 'Found'),
        ('on_progress', 'On Progress'),
        ('done', 'Done'),
        ('cancel', 'Cancelled'),
        ], string='Status', default='found')

    project_id = fields.Many2one('project.project', string='Project', track_visibility='onchange', index=True)

    task_id = fields.Many2one('project.task', string='Task', domain="[('project_id','=',project_id)]", default=_get_default_task_id,
							  help="You can link this issue to an existing task or directly create a new one from here")
        
    @api.multi
    def btn_cancle(self):
        self.state = 'cancel'
    
    @api.multi
    def btn_on_progress(self):
        self.state = 'on_progress'
    
    @api.multi
    def btn_done(self):
        self.state = 'done'

			
