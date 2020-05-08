# -*- coding: utf-8 -*-

# Add custom view for Project Budget Graph View.

from odoo.tools.translate import _
from odoo import models, fields, api
from odoo.addons.base.ir.ir_actions import VIEW_TYPES

from lxml import etree

# from logging import getLogger

# _logger = getLogger(__name__)
VIEW_TYPE = ('project_budget_graph', _('Project Budget Graph'))
VIEW_TYPES.append(VIEW_TYPE)


def valid_type_project_budget_graph(arch, fromgroup=True):
    return True


class IrUiViewInherit(models.Model):
    _inherit = 'ir.ui.view'

    type = fields.Selection(selection_add=[VIEW_TYPE])

    @api.multi
    def _check_xml_todo_project_budget_graph(self):
        domain = [
            ('id', 'in', self.ids), ('type', '=', VIEW_TYPE[0])
        ]

        for view in self.search(domain):
            fvg = self.env[view.model].fields_view_get(
                view_id=view.id, view_type=view.type
            )

            view_arch_utf8 = fvg['arch']
            view_docs = [etree.fromstring(view_arch_utf8)]

            if view_docs[0].tag == 'data':
                view_docs = view_docs[0]
            for view_arch in view_docs:
                if not valid_type_project_budget_graph(view_arch, fromgroup=False):
                    return False
        return True

    _constraints = [
        (
            _check_xml_todo_project_budget_graph,
            'Invalid XML for Project Budget Graph APS view architecture',
            ['arch'],
        ),
    ]
