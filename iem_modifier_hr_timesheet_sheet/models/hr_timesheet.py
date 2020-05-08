from odoo import models, fields, api, SUPERUSER_ID
from datetime import date

class HrTimesheetSheet(models.Model):
    _inherit = 'hr_timesheet_sheet.sheet'

    state2 = fields.Selection([('draft', 'Draft'), ('confirm', 'Confirmed')], copy=False, default='draft', string='Status')
    notification_sent = fields.Boolean(copy=False)

    @api.model
    def create(self, vals):
        record = super(HrTimesheetSheet, self).create(vals)
        if vals.get('timesheet_ids'):
            task_dict = {}
            task_list = []
            for line in record.timesheet_ids:
                if line.task_id in task_dict:
                    task_dict[line.task_id] += line.unit_amount
                else:
                    task_dict[line.task_id] = line.unit_amount
            for task_id in task_dict.keys():
                if task_dict[task_id]:
                    for assign_to in task_id.employee_ids.filtered(lambda x: x.employee_id == record.employee_id):
                        hours_ratio = (float(task_dict[task_id]) * 100.0)/ assign_to.planned_hours
                        if hours_ratio > 80:
                            task_list.append(task_id)
            for task in set(task_list):
                if task.project_id and task.project_id.project_PIC_id:
                    mail_vals = {}
                    mail_vals['subject'] = 'Exceed 80%s of planned hours for task %s' % ('%s', str(task.name))
                    mail_vals['body_html'] = "Hi %s,<br>%s exceed 80%s of planned hours for task %s." % (
                    task.project_id.project_PIC_id.name, record.employee_id.name, '%', task.name)
                    mail_vals['email_to'] = task.project_id.project_PIC_id.email
                    mail_vals['email_from'] = self.env['res.users'].browse(SUPERUSER_ID).email
                    self.env['mail.mail'].create(mail_vals).send()
        return record

    @api.multi
    def write(self, vals):
        res = super(HrTimesheetSheet, self).write(vals)
        if self.env.user != self.user_id:
            template_id = self.env.ref('iem_modifier_hr_timesheet_sheet.email_template_timesheet_notification')
            template_id.email_to = self.user_id.email
            template_id.send_mail(self.id)
            template_id.email_to = False
        if vals.get('timesheet_ids'):
            for record in self:
                task_dict = {}
                task_list = []
                for line in record.timesheet_ids:
                    if line.task_id in task_dict:
                        task_dict[line.task_id] += line.unit_amount
                    else:
                        task_dict[line.task_id] = line.unit_amount
                for task_id in task_dict.keys():
                    if task_dict[task_id]:
                        for assign_to in task_id.employee_ids.filtered(lambda x: x.employee_id == record.employee_id):
                            if assign_to.planned_hours < 0:
                                hours_ratio = (float(task_dict[task_id]) * 100.0) / assign_to.planned_hours
                                if hours_ratio > 80:
                                    task_list.append(task_id)
                for task in set(task_list):
                    if task.project_id and task.project_id.project_PIC_id:
                        mail_vals = {}
                        mail_vals['subject'] = 'Exceed 80%s of planned hours for task %s' % ('%s', str(task.name))
                        mail_vals['body_html'] = "Hi %s,<br>%s exceed 80%s of planned hours for task %s." % (
                            task.project_id.project_PIC_id.name, record.employee_id.name, '%', task.name)
                        mail_vals['email_to'] = task.project_id.project_PIC_id.email
                        mail_vals['email_from'] = self.env['res.users'].browse(SUPERUSER_ID).email
                        self.env['mail.mail'].create(mail_vals).send()
        return res

    @api.onchange('timesheet_ids', 'timesheet_ids.task_id', 'timesheet_ids.unit_amount')
    def onchange_timesheet(self):
        warning = {}
        task_dict = {}
        task_list = []
        for line in self.timesheet_ids:
            if line.task_id in task_dict:
                task_dict[line.task_id] += line.unit_amount
            else:
                task_dict[line.task_id] = line.unit_amount
        for task_id in task_dict.keys():
            if task_dict[task_id]:
                for assign_to in task_id.employee_ids.filtered(lambda x: x.employee_id == self.employee_id):
                    hours_ratio = (float(task_dict[task_id]) * 100.0) / assign_to.planned_hours
                    if hours_ratio > 80:
                        task_list.append(task_id)
        task_names = ''
        project_names = ''
        for task in set(task_list):
            task_names += task.name + ', '
            project_names += task.project_id.name + ', '
        if task_names:
            warning = {'title': 'Timesheet Warning!',
                       'message': self.employee_id.name + ' exceed 80% of planned hours for task(s) ' + task_names[:-2] + 'of '+ project_names[:-2]+'.'}
        return {'warning': warning}

    def action_submit(self):
        self.write({'state': 'done', 'state2': 'confirm'})

    @api.model
    def missing_update_notification(self):
        director = self.env['access.rights.group'].search([('name', '=', 'Director')], limit=1)
        for record in self.env['hr_timesheet_sheet.sheet'].search([('state2', '=', 'draft'), ('notification_sent', '=', False), ('date_to', '<', str(date.today()))]):
            template_id = self.env['ir.model.data'].xmlid_to_object('iem_modifier_hr_timesheet_sheet.email_template_timesheet_missing_update_notification')
            if director:
                for user in self.env['res.users'].search([('access_rights_id', '=', director.id)]):
                    if user:
                        template_id.email_to = user.email
                        template_id.send_mail(record.id, force_send=True)
                        record.with_context({'missing_update': True}).write({'notification_sent': True})

HrTimesheetSheet()