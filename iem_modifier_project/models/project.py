from odoo import models, fields, api
from odoo.exceptions import ValidationError

class ProjectTaskType(models.Model):
    _inherit = 'project.task.type'

    budgeted_stage_cost = fields.Float(string='Budgeted Stage Cost')

ProjectTaskType()

class ProjectProject(models.Model):
    _inherit = 'project.project'

    project_number = fields.Char(string='Project Number')

    @api.multi
    def name_get(self):
        res = []
        for record in self:
            name = ''
            if record.project_number:
                name = record.project_number + ' - '
            name += record.name if record.name else ''
            res.append((record.id, name))
        return res

    @api.constrains('project_number')
    def _check_project_number(self):
        for record in self:
            if record.project_number and self.env['project.project'].sudo().search([('project_number', '=', record.project_number), ('id', '!=', record.id)]):
                raise ValidationError('Project Number is unique per Project')

ProjectProject()