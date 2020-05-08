from odoo import api, fields, models, _


class ProjectTaskTypeTnherit(models.Model):
    _inherit = 'project.task.type'
    _order = 'sequence'

    stage_weightage = fields.Float(string="Stage Weightage")
    stage_completion = fields.Float(
        default=0.0, string="Stage Completion")
    # States for Stages
    status_stage = fields.Selection([('draft', 'Draft'),
                                     ('on_progress', 'On Progress'),
                                     ('done', 'Done')])
    # for extra compute to change state by default
    extra = fields.Boolean(string="extra", compute="check_task_draft")
    check_onprogress = fields.Boolean(compute="check_task_onprogress")
    check_status_done = fields.Boolean(compute="check_task_done")

    @api.model
    def create(self,vals):
        res  = super(ProjectTaskTypeTnherit,self).create(vals)
        if vals.get("project_ids"):
            project_ids = self.env['project.project'].search([])    
            for o in project_ids:
                    o._get_type_common()
#                     o.get_stages_from_type()
        return res

    @api.multi
    def write(self,vals):
        res  = super(ProjectTaskTypeTnherit,self).write(vals)
        if vals.get("project_ids"):
            project_ids = self.env['project.project'].search([])    
            for o in project_ids:
                o._get_type_common()
#                 o.get_stages_from_type()
        return res

    # Method for selection field
    @api.multi
    def check_task_draft(self):
        if self.name == "Draft":
            # search all task
            all_task = self.env['project.task'].search([])
            # search task which in draft
            task_draft = self.env['project.task'].search([('stage_id', '=', self.id)])
            if len(all_task.ids) == len(task_draft.ids):
                self.write({
                    'status_stage': 'draft',
                })
                return True
            else:
                self.write({
                    'status_stage': 'on_progress',
                })
                return True
        else:
            return True

    @api.multi
    def check_task_onprogress(self):
        if self.name == "On Progress":
            task_onprogress = self.env['project.task'].search([('stage_id', '=', self.id)])
            if len(task_onprogress.ids) >= 1:
                self.write({
                    'status_stage': 'on_progress',
                })
                return True
            else:
                return True
        else:
            return True

    @api.multi
    def check_task_done(self):
        if self.name == 'Done':
            task_all = self.env['project.task'].search([])
            task_done = self.env['project.task'].search([('stage_id', '=', self.id)])
            if len(task_all.ids) == len(task_done.ids):
                self.write({
                    'status_stage': 'done',
                })
                return True
            else:
                self.write({
                    'status_stage': 'on_progress',
                })
                return True
        else:
            return True
