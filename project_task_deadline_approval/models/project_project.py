from odoo import api, fields, models


class ProjectProjectInherit(models.Model):
    _inherit = 'project.team'

    other_project_pic = fields.Boolean(string='Other Project PIC')
