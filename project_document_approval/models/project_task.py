# -*- coding: utf-8 -*-

from odoo import api, fields, models
from odoo.exceptions import ValidationError
from datetime import datetime, date
from datetime import timedelta


class ProjectTask(models.Model):
    _inherit = 'project.task'

    document_ids = fields.One2many('ir.attachment', 'task_id')
    is_approve_visible = fields.Boolean(compute="check_is_approve_visible")

    @api.multi
    def check_is_approve_visible(self):
        for task in self:
            if self.env.user.id == task.project_id.project_PIC_id.id:
                task.is_approve_visible = True
            else:
                task.is_approve_visible = False

    def action_completed(self):
        incomplete_docs = self.env['ir.attachment'].search([('task_id', '=', self.id), ('state', '!=', 'approved')])
        if len(incomplete_docs) > 0:
            raise ValidationError("All document is not approved so you can not complete task.")
        self.date_finished = datetime.now()
        self.state = 'completed'
