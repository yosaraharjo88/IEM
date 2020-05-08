from odoo import fields, models, api, _
from datetime import datetime


class TaskDeadline(models.Model):
    _name = 'task.deadline'

    state = fields.Selection(
        [('draft', 'Draft'), ('waiting', 'Waiting for Approval'), ('approved', 'Approved'), ('rejected', 'Rejected')],
        string='State',
        required=True, readonly=True, copy=False, track_visibility='onchange', default='draft')
    project_id = fields.Many2one('project.project', string='Project')
    task_id = fields.Many2one('project.task', string='Task')
    actual_deadline = fields.Datetime(string='Actual Deadline', store=True)
    new_deadline = fields.Datetime(sting='New Deadline')
    is_user = fields.Boolean(default=False, compute='_compute_user')
    reason = fields.Text(string="Reason")
    create_date = fields.Date(string="Created Date", default=fields.Date.today())
    approve_reject = fields.Date(string="Approve/Reject Date")
    request_by_id = fields.Many2one('hr.employee', string="Request By")
    affect_other_task = fields.Boolean(string="Affect Other Task", default=True)

    @api.depends('project_id')
    def _compute_user(self):
        user = self.env.user
        pic_user = self.project_id.project_PIC_id
        if user == pic_user:
            self.is_user = True
        else:
            for project_team in self.project_id.project_team_ids:
                if project_team.other_project_pic:
                    for employee in project_team.employee_id:
                        if user == employee.user_id:
                            self.is_user = True

    @api.multi
    def request_for_approval(self):
        self.write({'state': 'waiting'})

    @api.multi
    def approve_request(self):
        print(self.task_id.date_deadline)
        date1 = datetime.strptime(self.task_id.date_deadline, '%Y-%m-%d %H:%M:%S')
        date2 = datetime.strptime(self.new_deadline, '%Y-%m-%d %H:%M:%S')
        date3 = date2 - date1
        self.task_id.date_deadline = self.new_deadline
        self.task_id.p_end_date = self.new_deadline
        today = fields.Date.today()
        self.approve_reject = today
        if self.affect_other_task:
            task_list = self.env['project.task'].search([('project_id', '=', self.project_id.id)])
            for task in task_list:
                if task != self.task_id:
                    if task.state not in ['completed', 'cancelled']:
                        if task.state == 'draft':
                            if task.start_date:
                                s_date = datetime.strptime(task.start_date, '%Y-%m-%d %H:%M:%S')
                                new_s_date = s_date + date3
                                task.start_date = str(new_s_date)
                        if task.p_end_date:
                            p_date = datetime.strptime(task.p_end_date, '%Y-%m-%d %H:%M:%S')
                            new_p_date = p_date + date3
                            task.p_end_date = str(new_p_date)
                        if task.date_deadline:
                            d_date = datetime.strptime(task.date_deadline, '%Y-%m-%d %H:%M:%S')
                            new_d_date = d_date + date3
                            task.date_deadline = str(new_d_date)
        self.write({'state': 'approved'})

    @api.multi
    def reject_request(self):
        today = fields.Date.today()
        self.approve_reject = today
        self.write({'state': 'rejected'})

    @api.onchange('project_id')
    def onchange_project(self):
        self.task_id = False
        return {'domain': {
            'task_id': [('project_id', '=', self.project_id.id), ('state', 'in', ['in_progress', 'on_hold'])]}}

    @api.onchange('task_id')
    def onchange_task(self):
        self.actual_deadline = self.task_id.date_deadline
