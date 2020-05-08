# -*- coding: utf-8 -*-

# This is for add custom view for Project Progress Graph View.
from odoo.tools.translate import _
from odoo import models, fields, api
from odoo.addons.base.ir.ir_actions import VIEW_TYPES

from lxml import etree

VIEW_TYPE = ('projectprogressgraph', _('Project Progress Graph'))
VIEW_TYPES.append(VIEW_TYPE)


def valid_type_project_progress_graph(arch, fromgroup=True):
    return True


class IrUiViewProjectProgressGraph(models.Model):
    _inherit = 'ir.ui.view'

    type = fields.Selection(selection_add=[VIEW_TYPE])

    @api.multi
    def _check_xml_todo_project_progress_graph(self):
        domain = [
            ('id', 'in', self.ids), ('type', '=', VIEW_TYPE[0]),
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
                if not valid_type_project_progress_graph(view_arch, fromgroup=False):
                    return False
        return True

    _constraints = [
        (
            _check_xml_todo_project_progress_graph,
            'Invalid XML for Project Progress Graph APS view architecture',
            ['arch'],
        ),
    ]
