# -*- coding: utf-8 -*-

from datetime import datetime, date
from datetime import timedelta
from dateutil.relativedelta import relativedelta
from odoo.exceptions import ValidationError

from odoo import api, fields, models


class ProjectTaskTnherit(models.Model):
    _inherit = 'project.task'

    start_date = fields.Datetime(string="Planned Start Date")
    p_start_date = fields.Datetime(string="Planned start Date", compute="get_start_date", store=True)
    p_end_date = fields.Datetime(string="Planned End Date", store=True)
    # end_date = fields.Date(string="Planned Deadline")
    task_duration = fields.Integer(string="Task Duration")
    date_deadline = fields.Datetime(string="Planned Deadline")
    planned_progress = fields.Float(string="Task Weightage")
    max_value = fields.Float(string="Max For Progress Completion", default=100.00)
    progress_completion = fields.Float(string="Task Completion", store=True, compute="set_progress_completion")
    task_progress_ids = fields.One2many('project.task.progress.history', 'project_task_id', string="Progress History")
    stage_name = fields.Char(related='stage_id.name')
    actual_start_date = fields.Datetime(string="Actual Start Date")
    state = fields.Selection([
        ('draft', 'Draft'),
        ('in_progress', 'In Progress'),
        ('on_hold', 'On Hold'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ], string='Status', default="draft", track_visibility='onchange')
    date_start = fields.Datetime(related='start_date')
    date_end = fields.Datetime(related='p_end_date')
    employee_ids = fields.One2many("employee.time.history", "task_id")
    planned_hours = fields.Float(string='Initially Planned Hours', compute="_get_total_planned_hours",
                                 help='Estimated time to do the task, usually set by the project manager when the task is in draft state.')

    @api.model
    def default_get(self, fields):
        res = super(ProjectTaskTnherit, self).default_get(fields)
        IrValue = self.env['ir.values']
        start_date = IrValue.get_default('project.config.settings', 'planned_start_date')
        end_date = IrValue.get_default('project.config.settings', 'planned_end_date')
        if start_date:
            res['start_date'] = start_date or False
        if end_date:
            res['p_end_date'] = end_date or False
            res['date_deadline'] = end_date or False
        return res

    @api.depends('stage_id', 'timesheet_ids.unit_amount', 'planned_hours', 'child_ids.stage_id',
                 'timesheet_ids.sheet_id.state',
                 'child_ids.planned_hours', 'child_ids.effective_hours', 'child_ids.children_hours',
                 'child_ids.timesheet_ids.unit_amount')
    def _hours_get(self):
        for task in self.sorted(key='id', reverse=True):
            super(ProjectTaskTnherit, self)._hours_get()
            total_effective_hours = 0
            for sheet in task.timesheet_ids:
                if sheet.sheet_id.state == 'done':
                    total_effective_hours += sheet.unit_amount
            task.effective_hours = total_effective_hours
            task.remaining_hours = task.planned_hours - task.effective_hours - task.children_hours

    @api.depends('timesheet_ids', 'timesheet_ids.unit_amount', 'timesheet_ids.employee_id')
    def _get_total_planned_hours(self):
        for task in self:
            total_planned_hours = 0
            for emp in task.employee_ids:
                total_actual_hours = 0
                total_planned_hours += emp.planned_hours
                for timesheet in task.timesheet_ids:
                    if timesheet.employee_id.id == emp.employee_id.id:
                        total_actual_hours += timesheet.unit_amount
                emp.actual_hours = total_actual_hours
            task.planned_hours = total_planned_hours

    @api.depends('p_end_date', 'start_date')
    def _compute_duration(self):
        for task in self:
            if task.p_end_date and task.start_date:
                diff = (fields.Datetime.from_string(task.p_end_date) + timedelta(days=1)) - fields.Datetime.from_string(
                    task.start_date)
                duration = diff.total_seconds()
            else:
                duration = 0.0
            task.duration = duration

    # When click on 'Start' event.
    def action_progress(self):
        self.actual_start_date = datetime.now()
        self.project_id.actual_start_date = datetime.now()
        if self.project_id.state_project == 'draft':
            self.project_id.write({'state_project': 'progress'})
        self.state = 'in_progress'

    def action_on_hold(self):
        return self.write({'state': 'on_hold'})

    def action_cancelled(self):
        return self.write({'state': 'cancelled'})

    # When click on 'Continue' button.
    def action_continue(self):
        return self.write({'state': 'in_progress'})

    @api.onchange('p_end_date')
    def onchange_p_end_date(self):
        self.date_deadline = self.p_end_date

    # Autofill date_start and date_end for Gantt view
    @api.onchange('start_date', 'p_end_date')
    def onchange_date_start_end(self):
        if self.start_date:
            self.date_start = self.start_date
        if self.p_end_date:
            self.date_end = self.p_end_date

    @api.model
    def create(self, vals):
        res = super(ProjectTaskTnherit, self).create(vals)
        IrValue = self.env['ir.values']
        start_date = IrValue.get_default('project.config.settings', 'planned_start_date')
        end_date = IrValue.get_default('project.config.settings', 'planned_end_date')
        res.write({'start_date': start_date or False,
                   'p_end_date': end_date or False,
                   'date_deadline': end_date or False})
        return res

    # When 'Start' button is clicked, task’s status become On Progress. Then appear ‘Task Complete’ button.
    @api.multi
    def become_on_progress(self):
        get_stages = self.env["project.task.type"].search([('name', '=', 'On Progress')])
        self.stage_id = get_stages.id
        return True

    # When click on 'Task Complete' button its become 'Done'
    @api.multi
    def become_done(self):
        get_stage = self.env["project.task.type"].search([('name', '=', 'Done')])
        self.stage_id = get_stage.id
        return True

    @api.depends('start_date')
    def get_start_date(self):
        for dates in self:
            if dates.start_date:
                dt = date.strftime(datetime.strptime(dates.start_date, "%Y-%m-%d %H:%M:%S"), "%Y-%m-%d")
                dates.p_start_date = dt

    # change the p_end_date in form view on start_date
    @api.onchange('start_date')
    def onchange_date_start_end(self):
        if self.start_date:
            end_date = datetime.strptime(self.start_date, "%Y-%m-%d %H:%M:%S") + timedelta(
                days=self.env.user.company_id.task_days)
            self.p_end_date = end_date

    # Fetch Progress Completion from additional_progress of project.task.progress.history
    @api.depends('task_progress_ids', 'state')
    def set_progress_completion(self):
        Int = 0.0
        for rec in self:
            if rec.state in ['cancelled', 'completed']:
                incomplete_tasks = self.env['project.task'].search([('project_id', '=', rec.project_id.id)])
                if not incomplete_tasks:
                    rec.project_id.state_project = 'done'
            if rec.state in ['cancelled', 'draft']:
                continue;
            for line in rec.task_progress_ids:
                if line.project_task_id.id == rec.id:
                    Int += line.additional_progress
            if Int <= 100:
                rec.progress_completion = Int
            else:
                flt = 0.0
                rec.progress_completion = flt
                raise ValidationError("Task Completion can not be more than 100")

    @api.onchange('task_duration', 'start_date')
    def set_date_deadline(self):
        if self.task_duration:
            dt = datetime.strptime(self.start_date, "%Y-%m-%d %H:%M:%S")
            final_dt = dt + timedelta(hours=self.task_duration)
            self.date_deadline = final_dt
        if self.start_date:
            dt = datetime.strptime(self.start_date, "%Y-%m-%d %H:%M:%S")
            final_dt = dt + timedelta(hours=self.task_duration)
            self.date_deadline = final_dt

    def task_deadline_scheduler(self):
        task_notification = self.env.user.company_id.task_notification
        notification_period = self.env.user.company_id.notification_period
        deadline = False
        if notification_period == 'days':
            deadline = datetime.now().date() + relativedelta(days=task_notification)
        elif notification_period == 'months':
            deadline = datetime.now().date() + relativedelta(months=task_notification)
        elif notification_period == 'years':
            deadline = datetime.now().date() + relativedelta(years=task_notification)
        else:
            return True
        d1 = datetime.strftime(deadline, "%Y-%m-%d %H:%M:%S")
        d2 = datetime.strftime(deadline, "%Y-%m-%d 23:59:59")
        tasks = self.env['project.task'].search(
            [('state', 'in', ['draft', 'in_progress', 'on_hold']), ('date_deadline', '>=', d1),
             ('date_deadline', '<=', d2)])
        temp_id = self.env.ref('project_extension.task_deadline_reminder_template')
        for task in tasks:
            self.env['mail.template'].browse(temp_id.id).send_mail(task.id)


class ProjectTaskProgressHistory(models.Model):
    _name = 'project.task.progress.history'

    @api.model
    def _get_default_completion_total(self):
        if 'default_project_task_id' in self._context:
            existing_historys = self.env['project.task.progress.history'].search(
                [('project_task_id', '=', self._context['default_project_task_id'])])
            total = 0
            for existing_history in existing_historys:
                total += existing_history.additional_progress
            return total
        return 0

    project_task_id = fields.Many2one('project.task', string='Project Task')
    project_id = fields.Many2one('project.project', string="Project Name", related="project_task_id.project_id")
    stage_id = fields.Many2one('project.task.type', string="Stage Name", related="project_task_id.stage_id")
    created_date = fields.Datetime(string="Created Date", default=datetime.now())
    created_by = fields.Many2one('res.users', string='Created By', default=lambda self: self.env.user)
    progress_summary = fields.Char(string="Progress Summary")
    task_name = fields.Char(
        related="project_task_id.name",
        string="Task Name", readonly=True)
    stage_name = fields.Char(
        related="project_task_id.stage_id.name",
        string="Stage Name", readonly=True)
    project_name = fields.Char(related="project_task_id.project_id.name", string="Project Name", readonly=True)
    progress_start_date = fields.Datetime(string="Progress Start Date")
    progress_end_date = fields.Datetime(string="Progress End Date")
    additional_progress = fields.Float(string="Additional Progress(%)", default=0.0)
    task_completion = fields.Float(string="Latest Completion(%)",
                                   default=lambda self: self._get_default_completion_total())
    latest_completion = fields.Float(string="Completion(%)", related="task_completion")
    attachment_ids = fields.One2many("project.task.attachment", 'attachment_id', string="Attachments")
    status = fields.Selection([('actual', 'Actual'), ('forecast', 'Forecast')], string="Status")

    @api.constrains('additional_progress')
    def check_additional_progress(self):
        if self.additional_progress <= 100:
            print("------")
        else:
            raise ValidationError("Additional Progress not valid it should be less then 100.")


class ProjectTaskAttachment(models.Model):
    _name = "project.task.attachment"

    attachment_id = fields.Many2one("project.task.progress.history", string="Attachments")
    date = fields.Datetime(string="Date")
    file = fields.Binary(string="Attachment")
    file_name = fields.Char(string="Name", size=64, store=True)
    file_size = fields.Integer(string="Size(KB)")

    # Get File Size in KB
    @api.onchange('file')
    def get_file_name(self):
        if self.file:
            a = len(self.file.decode('base64'))
            # for x in ['bytes', 'KB', 'MB', 'GB', 'TB']:
            # if a < 1024.0:
            # return "3.1%d" % (a)
            a /= 1024.0
            self.file_size = a


class UserTimeHistory(models.Model):
    _name = "employee.time.history"

    task_id = fields.Many2one("project.task")
    employee_id = fields.Many2one("hr.employee")
    planned_hours = fields.Float()
    actual_hours = fields.Float(compute="_get_total_actual_hours")
    leftover_hours = fields.Float(compute="_get_total_leftover_hours")
    spentover_hours = fields.Float(string="Spent(%)", compute="_get_total_spentover_hours")

    @api.onchange('employee_id')
    def onchange_user(self):
        domain = {}
        employee_ids = []
        if 'project_id' in self.env.context and self.env.context.get('project_id'):
            project = self.env['project.project'].browse(self.env.context.get('project_id'))
            for employee in project.project_team_ids:
                employee_ids.append(employee.employee_id.id)
        domain = {'domain': {'employee_id': [('id', 'in', employee_ids)]}}
        return domain

    @api.depends('task_id', 'task_id.timesheet_ids', 'task_id.timesheet_ids.unit_amount')
    def _get_total_actual_hours(self):
        for time_history in self:
            total_actual_hours = 0
            for timesheet in time_history.task_id.timesheet_ids:
                if timesheet.employee_id.id == time_history.employee_id.id and timesheet.sheet_id.state == 'done':
                    total_actual_hours += timesheet.unit_amount
            time_history.actual_hours = total_actual_hours

    @api.depends('planned_hours', 'actual_hours')
    def _get_total_leftover_hours(self):
        for time_history in self:
            time_history.leftover_hours = time_history.planned_hours - time_history.actual_hours

    @api.depends('planned_hours', 'actual_hours')
    def _get_total_spentover_hours(self):
        for time_history in self:
            # if time_history.actual_hours > 0 or time_history.planned_hours > 0:
            if time_history.actual_hours > 0:
                time_history.spentover_hours = (time_history.actual_hours * 100) / time_history.planned_hours
            else:
                time_history.spentover_hours = 0
