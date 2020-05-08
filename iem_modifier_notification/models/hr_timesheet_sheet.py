# -*- coding: utf-8 -*-

from odoo import api, fields, models


class HrTimesheetSheet(models.Model):
    _inherit = "hr_timesheet_sheet.sheet"

    @api.multi
    def write(self, vals):
        # send mail to employee if timesheet refus or change.
        if self.state  != 'confirm':
            return super(HrTimesheetSheet, self).write(vals)
        if 'state' not in vals or vals['state'] != 'done':
            temp_id = self.env.ref('iem_modifier_notification.notify_timesheet_reset_template')
            self.env['mail.template'].browse(temp_id.id).send_mail(self.id)
        return super(HrTimesheetSheet, self).write(vals)