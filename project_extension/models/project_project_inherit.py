# -*- coding: utf-8 -*-

from datetime import datetime
from datetime import timedelta
from odoo.exceptions import Warning, UserError
from odoo import api, fields, models, _
from odoo.http import Controller, route, request, Response
class ResCompany(models.Model):
    _inherit = 'res.company'

    days = fields.Integer(string='Standard Project Duration (Days)', help='Set default days on project.', default=7)
    task_days = fields.Integer(string='Standard Task Duration (Days)', help='Set default days on Task.', default=7)
    task_notification = fields.Integer("Task Notification")
    notification_period = fields.Selection([('days', "Day(s)"), ('months', "Month(s)"), ('years', "Year(s)")])
 
class ProjectProjectInherit(models.Model):
    _inherit = 'project.project'
    

    def _get_default_days(self):
        return self.env.user.company_id.days
    
    project_stage_ids = fields.One2many('project.stage.project', 'project_id', string="Stage")
    total_stage_weightage = fields.Integer(compute="get_total_stage_weightage", store=True)
    project_duration = fields.Integer(string="Duration (Days)", default=_get_default_days)
    project_start_date = fields.Datetime(string="Project Start Date")
    project_end_date = fields.Datetime(string="Project End Date")
    description = fields.Text(string="Description")
    project_scope_ids = fields.One2many('project.scope', 'project_details_id', string="Project Scope")
    project_team_ids = fields.One2many('project.team', 'project_details_id', string="Project Team")
    project_documents_ids = fields.One2many('project.documents', 'project_details_id', string="Project Documents")
    milestone_ids = fields.One2many('project.milestone', 'milestone_id', string="Milestone")
    state_project = fields.Selection([
        ('draft', 'Draft'),
        ('progress', 'On Progress'),
        ('done', 'Completed'),
    ], default='draft')
    state_stages_draft = fields.Boolean(compute='check_stages_draft')
    milestone_status_ids = fields.Many2many('project.milestone.status', string="Milestone Status")
    max_value = fields.Float(string="Max For Project Completion", default=100.00)
    project_completion = fields.Float(string="Project Completion", compute='compute_project_completion')

    project_PIC_id = fields.Many2one("res.users", "Project PIC")

    sequence_id = fields.Char('Name')
    actual_start_date = fields.Datetime(string="Actual Start Date")
    actual_end_date = fields.Datetime(string="Actual End Date")
    type_ids = fields.Many2many('project.task.type', 'project_task_type_rel', 'project_id', 'type_id', string='Tasks Stages',copy=False)
    project_PIC_ids = fields.Many2many('res.users', string="Project PIC 1")
    
    
    
    @api.onchange('project_PIC_id')
    def project_PIC_onchange(self):
        if self.project_PIC_id :
            self.user_id = self.project_PIC_id.id
    
    
    #get user  
    @api.multi
    @api.depends('project_team_ids')
    def get_project_PIC_id(self):
        for rec in self:
            users = []
            for line in rec.project_team_ids:
                if line.other_project_pic == True and line.employee_id.user_id:
                    users.append(line.employee_id.user_id.id)
            #if len(users) != 0:
            #    rec.write({
            #        'project_PIC_ids' : [(4,users)],
            #        })
            #else:
            rec.write({
                'project_PIC_ids' : [(4,self.env['res.users'].search([]).ids)],
                })
 
    @api.model
    def fields_view_get(self, view_id=None, view_type='form', toolbar=False, submenu=False):
        res = super(ProjectProjectInherit, self).fields_view_get(
            view_id=view_id, view_type=view_type, toolbar=toolbar, submenu=submenu)
        for rec in self.env['project.project'].search([]):
            rec.get_project_PIC_id()
        return res
    
    @api.multi
    def map_tasks(self, new_project_id):
        """ copy and map tasks from old to new project """
        tasks = self.env['project.task']
        for task in self.tasks:
            ProjectObj = self.env['project.project'].search([('id','=',new_project_id)])
            # preserve task name and stage, normally altered during copy
            defaults = {'stage_id': task.stage_id.id,
                        'name': task.name}
            ### code for not to copy stage for newly created project ###
            stage_ids = self.env['project.stage.project'].search([('project_id', '=', new_project_id)])
            typeIds = []
            for type_id in stage_ids:
                typeIds.append(type_id.type_id.id)
            for type in ProjectObj.type_ids:
                if type.id in typeIds:
                    type.write({'project_ids':[(4,[new_project_id,])]}) #adds project for new stage
                else:
                    type.write({'project_ids':[(3,new_project_id)]}) #removes project from existing stage
            for s in stage_ids:
                if s.stage_name == self.env['project.task.type'].search([('id','=',task.stage_id.id)]).name:
                    defaults['stage_id'] = s.type_id.id
                    s.type_id.write({'project_ids':[(4,[new_project_id,])]})
                    task.stage_id.write({'project_ids':[(3,new_project_id)]})
            ### end of code for not to copy stage for newly created project ###
            tasks += task.copy(defaults)
            
        return self.browse(new_project_id).write({'tasks': [(6, 0, tasks.ids)]})
    
    @api.multi
    def copy(self, default=None):
        if default is None:
            default = {}
        self = self.with_context(active_test=False)
        
        if not default.get('name'):
            default['name'] = _("%s (copy)") % (self.name)
        project = super(ProjectProjectInherit, self).copy(default)
        for follower in self.message_follower_ids:
            project.message_subscribe(partner_ids=follower.partner_id.ids, subtype_ids=follower.subtype_ids.ids)
        if 'tasks' not in default:
            self.map_tasks(project.id)
        return project
    
    @api.multi
    def force_complete(self):
        for project in self:
            incomplete_tasks = self.env['project.task'].search([('project_id', '=', project.id),
                ('state', 'in', ['in_progress', 'draft'])
            ])
            for task in incomplete_tasks:
                subject = ()
                state = dict(task._fields['state'].selection).get(task.state)
                body = "----- Force Completed -----" + "<br/>"
                body += "Status : " + state + "<br/>"
                body += "Date : " + str(datetime.now().date()) + "<br/>"
                body += "User : " + self.env.user.name
                task.state = 'completed'
                task.actual_end_date = datetime.now()
                task.message_post(body=body, subject=subject)
            project.actual_end_date = datetime.now()
            project.state_project = 'done'

    @api.model
    def create(self, vals):
        seq = self.env['ir.sequence'].get('project.project')
        vals['sequence_id'] = seq
        ir_values = self.env['ir.values'].get_default('project.config.settings', 'generate_project_alias')
        if ir_values:
            vals['alias_name'] = vals.get('alias_name') or vals.get('name')
        self = self.with_context(project_creation_in_progress=True, mail_create_nosubscribe=True)
        res = super(ProjectProjectInherit, self).create(vals)
        stage_list = self.env['project.task.type'].search([('project_ids', 'in', res.ids)])
        for line in res.project_stage_ids:
            if stage_list:
                for stage in stage_list:
                    if stage.name == line.stage_name:
                        raise UserError(_("The Stage Already Exist"))
#             self.env['project.task.type'].create({'name': line.stage_name, 'project_ids': [(6, 0, res.ids)]})
        # Get the Project task template details
        if vals and vals.get('project_type'):
            ProjectTaskTypeObj = self.env['project.task.type']
            ProjectTemplateObj = self.env['project.template'].search([('id', '=', vals.get('project_type'))])
            project_stage_list = []
            for line in ProjectTemplateObj.task_ids:
                res_project_task_type1 = ProjectTaskTypeObj.create({
                    'name': line.stage,
                    'stage_weightage': line.stage_weightages,
                    'sequence': line.stage_number,
                })
                res_project_task_type1.write({'project_ids':[(4,[res.id,])]})
                project_stage_list.append((0, 0, {'type_id': res_project_task_type1.id,
                                                  'stage_name' : res_project_task_type1.name,
                                                  'sequence' : res_project_task_type1.sequence,
                                                  'stage_weightage': res_project_task_type1.stage_weightage,
                                                  'project_id' : res.id}
                                           ))
                
            vals.update({'project_stage_ids': project_stage_list, 'total_stage_weightage': 100})
            res.write(vals)
        return res
    @api.multi
    def write(self, vals):
        if "project_team_ids" in vals.keys():
            for line in vals['project_team_ids']:
                if line[0] == 0:
                    users = []
                    if line[2]['other_project_pic'] == True:
                        emp = self.env['hr.employee'].search([('id','=',line[2]['employee_id'])])
                        for emp in emp:
                            users.append(emp.user_id.id)
                        if len(users) != 0:
                            self.update({
                                'project_PIC_ids': [(4,users[0])],
                            })
                        else:
                            self.update({
                                'project_PIC_ids': [(4,self.env['res.users'].search([]).ids)],
                            })
                if line[0] == 1:
                    users = []
                    if line[2]['other_project_pic'] == True:
                        project = self.env['project.team'].search([('id','=',line[1])])
                        for pro in project:
                            emp = self.env['hr.employee'].search([('id','=',pro.employee_id.id)])
                            for emp in emp:
                                users.append(emp.user_id.id)
                            if len(users) != 0:
                                self.update({
                                    'project_PIC_ids': [(4,users[0])],
                                })
                        
        res = super(ProjectProjectInherit, self).write(vals)
        return res
    
    @api.multi
    def unlink(self):
        # remove selected stage in project task type
        for project in self:
            ProjectTaskTypeObj = self.env['project.task.type'].search([('project_ids','in',project.id),
                                                                       ('id','in',project.type_ids.ids)
                                                                       ])
            ProjectTaskTypeObj.unlink()
            
        return super(ProjectProjectInherit, self).unlink()
    
    @api.multi
    @api.depends('project_stage_ids')
    def get_total_stage_weightage(self):
        for project in self:
            total_w = 0
            for line in project.project_stage_ids:
                total_w += line.stage_weightage
            project.total_stage_weightage = total_w

    def _get_type_common(self):
        type_ids = False
        for rec in self:
            type_ids = self.env['project.task.type'].search([('project_ids', 'in', [rec.id])])
        return type_ids

    @api.multi
    def get_stages_from_type(self):
        for rec in self:
            stage_list = []
            unwanted_list = []
            for stage in rec.project_stage_ids:
                stage_list.append(stage.type_id.id)
                if stage.type_id.id not in rec.type_ids.ids:
                    unwanted_list.append(stage)
            append_list = []
            for ty in rec.type_ids:
                if ty.id not in stage_list:
                    append_list.append((0, 0, {'type_id': ty.id}))
            if append_list:
                rec.project_stage_ids = append_list
            for stage in rec.project_stage_ids:
                stage.stage_name = stage.type_id.name
            for op in unwanted_list:
                op.unlink()

    type_ids = fields.Many2many(
        comodel_name='project.task.type', relation='project_task_type_rel',
        column1='project_id', column2='type_id', string='Tasks Stages',
        default=_get_type_common
    )

    @api.multi
    def compute_project_completion(self):
        for rec in self:
            grand = 0.0
            for line in rec.project_stage_ids:
                tasks = self.env['project.task'].search(
                    [('stage_id', '=', line.type_id.id), ('project_id', '=', rec.id),
                     ('state', 'not in', ['draft', 'cancelled'])])
                stage_completion = 0
                for task in tasks:
                    stage_completion += (task.planned_progress * task.progress_completion) / 100
                grand += (line.stage_weightage * stage_completion) / 100
            rec.project_completion = grand

    @api.multi
    def check_stages_draft(self):
        # search all task
        all_stages = self.env['project.task.type'].search([])
        # search task which in draft
        stages_draft = self.env['project.task.type'].search([('status_stage', '=', 'draft')])
        stages_done = self.env["project.task.type"].search([('status_stage', '=', 'done')])
        if len(all_stages.ids) == len(stages_draft.ids):
            self.write({
                'state_project': 'draft',
            })
            return True

        if len(stages_done.ids) == len(all_stages.ids):
            self.write({
                'state_project': 'done',
            })
            return True

    @api.onchange('project_duration', 'project_start_date', 'project_end_date')
    def set_date_deadline(self):
        if 'duration' in self._context:
            if self.project_duration and self.project_start_date:
                dt = datetime.strptime(self.project_start_date, "%Y-%m-%d %H:%M:%S")
                final_dt = dt + timedelta(days=self.project_duration - 1)
                self.project_end_date = final_dt

            elif self.project_duration and not self.project_start_date and self.project_end_date:
                edt = datetime.strptime(self.project_end_date, "%Y-%m-%d %H:%M:%S")
                sdt = edt - timedelta(days=self.project_duration - 1)
                self.project_start_date = sdt

            elif self.project_duration == 0 and self.project_start_date and self.project_end_date:
                sdt = datetime.strptime(self.project_start_date, "%Y-%m-%d %H:%M:%S")
                edt = datetime.strptime(self.project_end_date, "%Y-%m-%d %H:%M:%S")
                self.project_duration = (edt - sdt).days + 1

        elif 'start_date' in self._context:
            if self.project_duration and self.project_start_date:
                dt = datetime.strptime(self.project_start_date, "%Y-%m-%d %H:%M:%S")
                final_dt = dt + timedelta(days=self.project_duration - 1)
                self.project_end_date = final_dt

            elif self.project_duration == 0 and self.project_start_date and self.project_end_date:
                sdt = datetime.strptime(self.project_start_date, "%Y-%m-%d %H:%M:%S")
                edt = datetime.strptime(self.project_end_date, "%Y-%m-%d %H:%M:%S")
                self.project_duration = (edt - sdt).days + 1

            elif self.project_duration and not self.project_start_date and self.project_end_date:
                edt = datetime.strptime(self.project_end_date, "%Y-%m-%d %H:%M:%S")
                sdt = edt - timedelta(days=self.project_duration - 1)
                self.project_start_date = sdt

        elif 'end_date' in self._context:
            if self.project_start_date and self.project_end_date:
                sdt = datetime.strptime(self.project_start_date, "%Y-%m-%d %H:%M:%S")
                edt = datetime.strptime(self.project_end_date, "%Y-%m-%d %H:%M:%S")
                self.project_duration = (edt - sdt).days + 1

            elif self.project_duration and not self.project_start_date and self.project_end_date:
                edt = datetime.strptime(self.project_end_date, "%Y-%m-%d %H:%M:%S")
                sdt = edt - timedelta(days=self.project_duration - 1)
                self.project_start_date = sdt

            elif not self.project_end_date and self.project_duration and self.project_start_date:
                dt = datetime.strptime(self.project_start_date, "%Y-%m-%d %H:%M:%S")
                final_dt = dt + timedelta(days=self.project_duration - 1)
                self.project_end_date = final_dt


class ProjectMilestone(models.Model):
    _name = "project.milestone"
    _order = 'sequence asc'

    milestone_id = fields.Many2one('project.project', string="Milestone")
    sequence = fields.Integer('sequence', help="Sequence for the handle.", default=10)
    milestone_no = fields.Char(string='Reference Number', copy=False)
    milestone_name = fields.Char(string="Milestone Name", required=True)
    milestone_description = fields.Text(string="Milestone Description")
    deliverable = fields.Text(string="Deliverables")
    expected_date = fields.Date(string="Expected Date")
    tolerance_days = fields.Integer(string="Tolerance Days")
    archived_date = fields.Date(string="Archived Date")
    variance_days = fields.Integer(string="Variance Days")
    status = fields.Many2one('project.milestone.status', string="Status")

    def default_get(self, context=None):
        res = {}
        if self._context:
            context_keys = self._context.keys()
            next_sequence = 1
            if 'milestone_ids' in context_keys:
                if len(self._context.get('milestone_ids')) > 0:
                    next_sequence = len(self._context.get('milestone_ids')) + 1
            res.update({'milestone_no': next_sequence})
        return res


class ProjectDocuments(models.Model):
    _name = 'project.documents'
    _rec_name = 'document_name'

    date = fields.Datetime(string="Date", default=datetime.now())
    document_name = fields.Char(string="Document Name")
    document_type = fields.Char(string="Document Type")
    document_size = fields.Char(string="Document Size")
    project_details_id = fields.Many2one('project.project', string="Project Details")


class ProjectTeam(models.Model):
    _name = 'project.team'
    _rec_name = 'role_id'

    role_id = fields.Many2one('project.team.role', string="Role")
    employee_id = fields.Many2one('hr.employee', string="Employee")
    project_details_id = fields.Many2one('project.project', string="Project Details")
    project_planned_hours = fields.Float(string="Planned Hours", compute="get_total_project_planned_hours")
    project_actual_hours = fields.Float(string="Actual Hours", compute="get_total_project_actual_hours")

    def get_total_project_planned_hours(self):
        for team in self:
            tasks = team.project_details_id.task_ids
            total_planned_hours = 0
            for task in tasks:
                for emp in task.employee_ids:
                    if emp.employee_id.id == team.employee_id.id:
                        total_planned_hours += emp.planned_hours
            team.project_planned_hours = total_planned_hours

    def get_total_project_actual_hours(self):
        for team in self:
            tasks = team.project_details_id.task_ids
            total_actual_hours = 0
            for task in tasks:
                for emp in task.employee_ids:
                    if emp.employee_id.id == team.employee_id.id:
                        total_actual_hours += emp.actual_hours
            team.project_actual_hours = total_actual_hours


class ProjectScope(models.Model):
    _name = 'project.scope'
    _rec_name = 'project_scope_name'

    project_scope_name = fields.Char(string="Project Scope Name")
    project_details_id = fields.Many2one('project.project', string="Project Details")


class ProjectStageProject(models.Model):
    _name = 'project.stage.project'
    _order = 'sequence'

    @api.model
    def default_get(self, fields):
        res = super(ProjectStageProject, self).default_get(fields)
        if self._context:
            context_keys = self._context.keys()
            next_sequence = 1
            if 'project_stage_ids' in context_keys:
                if len(self._context.get('project_stage_ids')) > 0:
                    next_sequence = len(self._context.get('project_stage_ids')) + 1
            res.update({'sequence': next_sequence})
        return res

    # def _get_default_stage_id(self):
    #     """ Gives default stage_id """
    #     project_id = self.env.context.get('default_project_id')
    #     if not project_id:
    #         return False
    #     return self.stage_find(project_id, [('fold', '=', False)])

    project_id = fields.Many2one('project.project', string="Project")
    type_id = fields.Many2one('project.task.type', string='Stage')
    stage_weightage = fields.Float(string="Stage Weightage", store=True)
    stage_completion = fields.Float(string="Stage Completion")
    sequence = fields.Integer(string="Sequence", store=True)
    stage_name = fields.Char(string='Stage', store=True)

    @api.model
    def create(self, vals):
        res = super(ProjectStageProject, self).create(vals)
        if not res.type_id:
            type_search = self.env['project.task.type'].search(
                [('name', '=', res.stage_name), ('project_ids', 'in', res.project_id.id)], limit=1)
            if type_search:
                res.type_id = type_search.id
            else:
                stage_vals = {'name': res.stage_name}
                type_search = self.env['project.task.type'].create(stage_vals)
                res.type_id = type_search.id
            if res.project_id.id not in res.type_id.project_ids.ids:
                res.type_id.write({
                    'project_ids': [(4, [res.project_id.id])],
                })
        return res

    @api.multi
    def unlink(self):
        # remove selected stage in project task type
        for stage in self:
            ProjectTaskTypeObj = self.env['project.task.type'].search([('project_ids','in',stage.project_id.id),
                                                                       ('id','=',stage.type_id.id)
                                                                       ])
            ProjectTaskTypeObj.unlink()
            #remove only project name
#             if stage.project_id.id in stage.type_id.project_ids.ids:
#                 stage.type_id.write({
#                     'project_ids': [(3, stage.project_id.id)],
#                 })
#                 
        return super(ProjectStageProject, self).unlink()

    # @api.model
    # def create(self, vals):
    #     res = super(ProjectStageProject, self).create(vals)
    #     # type_search = self.search([('project_id','=',res.project_id.id), ('type_id','=',res.type_id.id)])
    #     # if    type_search:
    #     #     type_search.unlink()
    #     #     raise UserError(_('Duplicate records cannot be created'))
    #     if res.project_id.id not in res.type_id.project_ids.ids:
    #         res.type_id.write({
    #             'project_ids': [(4, res.project_id.ids)],
    #         })
    #     return res

class ProjectSettings(models.TransientModel):
    _inherit = 'project.config.settings'

    company_id = fields.Many2one('res.company', string='Company', required=True,
                                 default=lambda self: self.env.user.company_id)
    days = fields.Integer(related='company_id.days', string='Days', help='Set default days on project.')
    task_days = fields.Integer(related='company_id.task_days', string='Task Days', help='Set default days on Task.')
    planned_start_date = fields.Date(string="Planned Start Date")
    planned_end_date = fields.Date(string="Planned End Date")
    task_notification = fields.Integer("Task Notification", related='company_id.task_notification')
    notification_period = fields.Selection(related='company_id.notification_period')
    project_late_parameter = fields.Float(string="Project Late Parameter (%)",
                                          help="The difference value between Planned & Actual progress in percentage to declare a project's progress is On Progress or Late")

    @api.model
    def get_values(self, fields):
        IrValue = self.env['ir.values'].sudo()
        return {
            'planned_start_date': IrValue.get_default('project.config.settings', 'planned_start_date'),
            'planned_end_date': IrValue.get_default('project.config.settings', 'planned_end_date'),
            'project_late_parameter': IrValue.get_default('project.config.settings', 'project_late_parameter'),
        }

    @api.multi
    def set_values(self):
        IrValue = self.env['ir.values'].sudo()
        IrValue.sudo().set_default('project.config.settings', 'planned_start_date', self.planned_start_date)
        IrValue.set_default('project.config.settings', 'planned_end_date', self.planned_end_date)
        IrValue.set_default('project.config.settings', 'project_late_parameter', self.project_late_parameter)
