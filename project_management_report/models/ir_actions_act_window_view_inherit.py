# -*- coding: utf-8 -*-
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).
from odoo import fields, models, _


class IrActionsActWindowView(models.Model):
    _inherit = 'ir.actions.act_window.view'

    view_mode = fields.Selection(selection_add=[('project_progress_table', 'Project Progress Report'), ('projectprogressgraph', _('Project Progress Graph')), ('scurvecomparison', 'S-curve Comparison')])