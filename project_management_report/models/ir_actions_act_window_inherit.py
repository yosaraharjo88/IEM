from odoo import fields, models, _


class IrActionsActWindowInherit(models.Model):
    _inherit = 'ir.actions.act_window'

    view_type = fields.Selection(selection_add=[('project_progress_table', 'Project Progress Report'), ('projectprogressgraph', _('Project Progress Graph')), ('scurvecomparison', 'S-curve Comparison')])