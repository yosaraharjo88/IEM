# -*- coding: utf-8 -*-

from odoo import fields, models, api, _

class Project(models.Model):
    _inherit = "project.project"
    
    project_type = fields.Many2one('project.template',string="Project Type")
    
    
    @api.model
    def create(self, vals):
        res=super(Project, self).create(vals)
        if vals and vals.get('project_type'):
            ProjectTaskObj = self.env['project.task'].search([])
            ProjectTemplateObj = self.env['project.template'].search([('id','=',vals.get('project_type'))])
            
            for line in ProjectTemplateObj.task_ids:
                 stages_obj = self.env['project.task.type'].search([('id','=',line.stage_id.id)])
                 stages_obj.write({
                     'project_ids' : [(4,res.id)],
                     })
                for rec in line.task_template_id:
                    res1 = ProjectTaskObj.create({
                        'name' : rec.name,
                        'project_id' : res.id,
                        'kanban_state' : 'normal',
                        'description' : rec.description,
                        })
                    res1.write({
                        'stage_id' : line.stage_id.id,
                        })
                    
                    if rec.child_task_ids:
                        for l in rec.child_task_ids:
                            res2 = ProjectTaskObj.create({
                                    'name': l.name,
                                    'project_id': res.id,
    #                                 'subtask_project_id' : self.id,
                                    'planned_hours' : l.planned_hours,
                                    'remaining_hours': l.remaining_hours,
                                    'user_id': l.user_id.id,
                                    'description': l.description,
                                    'parent_task_id' : res1.id,
                                    })
                            res2.write({
                            'stage_id' : line.stage_id.id,
                            })
        return res 

