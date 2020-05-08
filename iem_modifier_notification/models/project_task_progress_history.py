# -*- coding: utf-8 -*-

from odoo import fields, models
from dateutil.relativedelta import relativedelta
from datetime import datetime


class ProjectTaskProgressHistory(models.Model):
    _inherit = 'project.task.progress.history'

    def progress_history_scheduler(self):
        creation_date = datetime.now().date() - relativedelta(days=7)
        creation_datetime = datetime.strftime(
            creation_date, "%Y-%m-%d %H:%M:%S")
        progress_history_ids = self.search([
            ('create_date', '<=', creation_datetime), 
            ('additional_progress', '=', 0)
        ])
        temp_id = self.env.ref('iem_modifier_notification.progress_history_reminder_template')
        for line in progress_history_ids:
            self.env['mail.template'].browse(temp_id.id).send_mail(line.id)