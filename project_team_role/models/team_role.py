from odoo import fields,api,models,_

class ProjectTeamRole(models.Model):
    _name = "project.team.role"
    _description = "Project Team Role"
    _order = "create_date desc"
    
    name = fields.Char("Role name")
    description = fields.Text("Description")
    