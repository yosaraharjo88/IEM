from odoo import fields, models, _


class IrActionsActWindowInherit(models.Model):
    _inherit = 'ir.actions.act_window'

    view_type = fields.Selection(selection_add=[('project_budget_table', 'Project Budget Report'),
                                                ('project_budget_graph', 'Project Budget Graph')])
