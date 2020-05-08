# -*- coding: utf-8 -*-
import logging
from odoo import fields, models, api, _

_logger = logging.getLogger(__name__)


class Project(models.Model):
    _inherit = "project.project"

    project_type = fields.Many2one('project.template', string="Project Type")

    @api.model
    def create(self, vals):
        
        # print("Create | self --> ", self)
        res = super(Project, self).create(vals)
        # print("Create | res --> ", res)
        if vals and vals.get('project_type'):
            ProjectTaskObj = self.env['project.task'].search([])
            ProjectTaskTypeObj = self.env['project.task.type']
            ProjectTemplateObj = self.env['project.template'].search([('id', '=', vals.get('project_type'))])
            project_stage_list = []
            for line in ProjectTemplateObj.task_ids:
                # print("Line line line ", line)
                res_project_task_type = ProjectTaskTypeObj.search([('name', '=', line.stage)], limit=1)
#                 if res_project_task_type: res_project_task_type.write({'project_ids': [(4, res.id)]})
                if res_project_task_type:
                    # print("All ready created.")
                    _logger.info(["Stages all ready created."])
                    project_stage_list.append((0, 0, {'type_id': res_project_task_type.id,
                                                      'stage_weightage': res_project_task_type.stage_weightage}
                                               ))
                else:
                    # print("Else else")
                    res_project_task_type = ProjectTaskTypeObj.create({
                        'name': line.stage,
                        'stage_weightage': line.stage_weightages,
                        'sequence': line.stage_number,
                        'project_ids': [(4, res.id)]
                    })
                    # print("Created Project task type: ", res_project_task_type)
                    project_stage_list.append((0, 0, {'type_id': res_project_task_type.id,
                                                      'stage_weightage': res_project_task_type.stage_weightage}
                                               ))
                    # print("Created project stage list: ", project_stage_list)

                for mac in line.task_template_id: 
                    IrValue = self.env['ir.values']
                    start_date = IrValue.get_default('project.config.settings', 'planned_start_date')
                    end_date = IrValue.get_default('project.config.settings', 'planned_end_date')
                    tags = mac.mapped('tag_ids').ids
                    res1 = ProjectTaskObj.create({
                        'name': mac.name,
                        'project_id': res.id,
                        'kanban_state': 'normal',
                        'stage_id': res_project_task_type.id if res_project_task_type.name == line.stage else False,
                        'tag_ids': [(6, 0, tags)],
                        'planned_progress': mac.task_weightage or 0.0,
                        'start_date': start_date or False,
                        'p_end_date': end_date or False,
                        'date_deadline': end_date or False,
                    })

                    # print("Created Project task", res1)
                    _logger.info(["Created Task", res1])

            # print("Create | Updated vals --> ", vals)

            # stages_obj = self.env['project.task.type'].search([('id', '=', line.stage)])
            # stages_obj.project_ids = [(4, res.id)]
            # for rec in line.task_template_id:
            #     res1 = ProjectTaskObj.create({
            #         'name': rec.name,
            #         'project_id': res.id,
            #         'kanban_state': 'normal',
            #         'description': rec.description,
            #     })
            #     res1.write({
            #         'stage_id': line.stage_id.id,
            #     })
            #
            #     if rec.child_task_ids:
            #         for l in rec.child_task_ids:
            #             res2 = ProjectTaskObj.create({
            #                 'parent_task_id': res1.id,
            #                 'name': l.name,
            #                 'project_id': res.id,
            #                 #                                 'subtask_project_id' : self.id,
            #                 'planned_hours': l.planned_hours,
            #                 'remaining_hours': l.remaining_hours,
            #                 'user_id': l.user_id.id,
            #                 'description': l.description,
            #                 'parent_task_id': res1.id,
            #             })
            #             res2.write({
            #                 'stage_id': line.stage_id.id,
            #             })
#             vals.update({'project_stage_ids': project_stage_list, 'total_stage_weightage': 100})
#             # print("vals vals", vals)
#             res_write = res.write(vals)
#             print("res_write ----> ", res_write)
        return res
