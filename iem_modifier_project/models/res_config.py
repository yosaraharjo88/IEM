from odoo import models, fields, api

class ProjectConfiguration(models.TransientModel):
    _inherit = 'project.config.settings'

    minimum_hr_day = fields.Float(string='Minimum Hour/day')

    @api.multi
    def set_working_hr(self):
        return self.env['ir.values'].sudo().set_default('project.config.settings', 'minimum_hr_day', self.minimum_hr_day)

ProjectConfiguration()