from odoo import models, fields, api


class IrAttachment(models.Model):
    _inherit = 'ir.attachment'

    state = fields.Selection([('draft', "Draft"), ('wait', "Waiting for Approval"), ('approved', "Approved")], 
        string="Status", default="draft")
    is_approve_visible = fields.Boolean(compute="check_is_approve_visible")
    approve_date = fields.Datetime("Approve Date")

    @api.multi
    def check_is_approve_visible(self):
        for doc in self:
            if self.env.user.id == doc.task_id.project_id.project_PIC_id.id:
                doc.is_approve_visible = True
            else:
                doc.is_approve_visible = False

    @api.multi
    def action_request_for_approval(self):
        for doc in self:
            doc.state = 'wait'

    @api.multi
    def action_approved(self):
        for doc in self:
            doc.approve_date = fields.datetime.now()
            doc.state = 'approved'

    @api.multi
    def action_reject(self):
        for doc in self:
            doc.state = 'draft'