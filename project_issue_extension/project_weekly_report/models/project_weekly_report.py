from odoo import models,fields,api
from datetime import datetime,timedelta


class ProjectIssues(models.Model):
    _inherit = 'project.issue'

    report_id = fields.Many2one('project.weekly.report',string='Report')

class ProjectWeeklyReport(models.Model):
    _name = 'project.weekly.report'

    name = fields.Char('Weekly Report Name', required=True)
    project_id = fields.Many2one('project.project', 'Project', required= True)
    project_start = fields.Date('Report Start Date')
    project_end = fields.Date('Report End Date')
    progress = fields.Integer('Completion Progress')
    report_creation_date = fields.Date('Created On')
    weekly_segment = fields.Selection([('w1', "W1"),
                                       ('w2', "W2"),
                                       ('w3', "W3"),
                                       ('w4', "W4"),
                                       ('w5', "W5")], 'Weekly Segment')
    tag_ids = fields.Many2many('project.tags', string='Tags')
    description = fields.Html(string='Description')
    progressive_history_ids = fields.One2many('weekly.report.progress.history', 'weekly_report_id', string="Progress History")
    issue_ids = fields.One2many('project.issue','report_id',string='Issues',store=True,compute='compute_issue_ids')
    
    @api.onchange('project_id')
    def _onchange_project(self):
        for rec in self:
            if rec.project_id:
                report = self.env['project.weekly.report'].search([('project_id', '=', rec.project_id.id)])
                if report:
                    sorted_reports = sorted(report, key=lambda x: (x.project_start))
                    if sorted_reports:
                        report = sorted_reports[-1]
                        if report.project_start:
                            rec.project_start =datetime.strptime(report.project_start, '%Y-%m-%d').date()+timedelta(days=7)
                            rec.project_end = datetime.strptime(rec.project_start, '%Y-%m-%d').date()+timedelta(days=6)
                else:
                    if rec.project_start:
                        rec.project_start = rec.project_start
                        rec.project_end =datetime.strptime(rec.project_start, '%Y-%m-%d').date()+ timedelta(days=6)

    @api.depends('project_id')
    def compute_issue_ids(self):
        for rec in self:
            issues = self.env['project.issue'].search([('project_id', '=', rec.project_id.id), ('active', '=', True)])
            if issues:
                self.issue_ids = [(6,0,issues.ids)]

    @api.onchange('project_start')
    def _onchange_project_start(self):
        if self.project_start:
            self.project_end = datetime.strptime(self.project_start, '%Y-%m-%d').date() + timedelta(days=6)

    @api.onchange('project_id', 'project_start', 'project_end', 'weekly_segment')
    def _onchange_segment(self):
        self.progressive_history_ids = False
        if self.project_id and self.project_start:
            start_date = datetime.strptime(self.project_start, "%Y-%m-%d")
            if self.weekly_segment == 'w1':
                end_date =  start_date + timedelta(weeks=1)
            elif self.weekly_segment == 'w2':
                end_date = start_date + timedelta(weeks=2)
            elif self.weekly_segment == 'w3':
                end_date = start_date + timedelta(weeks=3)
            elif self.weekly_segment == 'w4':
                end_date = start_date + timedelta(weeks=4)
            elif self.weekly_segment == 'w5':
                end_date = start_date + timedelta(weeks=5)
            else:
                end_date = False
            data_set = []
            project_end = datetime.strptime(self.project_end, "%Y-%m-%d")
            for task in self.project_id.tasks:
                    for history in task.task_progress_ids:
                        data = history.read()[0]
                        if data.get('create_date'):
                            created_date = datetime.strptime(data.get('created_date'), "%Y-%m-%d %H:%M:%S")

                            if start_date <= created_date <= project_end:
                                data_set.append((0, 0, data))
            self.progressive_history_ids = data_set


class WeeklyReportProgressHistory(models.Model):
    _name = 'weekly.report.progress.history'

    weekly_report_id = fields.Many2one('project.weekly.report', string='Project Task')
    project_task_id = fields.Many2one('project.task', string='Project Task')
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
    latest_completion = fields.Float(string="Latest Completion(%)", default=0.0)
    attachment_ids = fields.One2many("project.task.attachment", 'attachment_id', string="Attachments")


