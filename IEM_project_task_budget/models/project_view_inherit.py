from odoo import api, fields, models, _

class ProjectProject(models.Model):
    _inherit = 'project.project'
    
    task_budgeted_cost = fields.Float(string="Budgeted Cost", compute="_get_related_stage_id")
    
    @api.depends('project_stage_ids','task_ids')
    def _get_related_stage_id(self):
        stage_id = []
        for rec in self:
            for stage in rec.project_stage_ids:
                stage_id.append(stage.type_id.id)
            task_id = self.env['project.task'].search([('project_id','=',rec.id),
                                                       ('stage_id','in',stage_id),
                                                       ('id','in',rec.task_ids.ids)])
            for task in task_id:
                rec.task_budgeted_cost += task.budgeted_cost
                
class ProjectTask(models.Model):
    _inherit = 'project.task'
    
    budgeted_cost = fields.Float(string="Budgeted Cost")
    
