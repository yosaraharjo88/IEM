# -*- coding: utf-8 -*-
# Add new custom 'S-curve Comparison' view.
from odoo.tools.translate import _
from odoo import models, fields, api
from odoo.addons.base.ir.ir_actions import VIEW_TYPES
from lxml import etree

VIEW_TYPE = ('scurvecomparison', _('S-curve Comparison'))
VIEW_TYPES.append(VIEW_TYPE)

# print("-----------------> New View Types: ", VIEW_TYPES)


def valid_type_scurve_comparison(arch, fromgroup=True):
    return True


class IrUiViewInherit(models.Model):
    _inherit = 'ir.ui.view'

    type = fields.Selection(selection_add=[VIEW_TYPE])

    @api.multi
    def _check_xml_todo_scurve_comparison(self):
        domain = [
            ('id', 'in', self.ids), ('type', '=', VIEW_TYPE[0]),
        ]
        # print("View Model, Self Ids, VIEW_TYPE[0] : NEW NEW ---------------- ", self.ids, VIEW_TYPE[0])

        for view in self.search(domain):
            # print("View Model: for loop-------------------------------- ", view.model)
            fvg = self.env[view.model].fields_view_get(
                view_id=view.id, view_type=view.type
            )
            # print("fvg['arch']-----------------------fvg['arch']", fvg['arch'])
            view_arch_utf8 = fvg['arch']
            view_docs = [etree.fromstring(view_arch_utf8)]
            # print("###########   view_docs    ########", view_docs)

            if view_docs[0].tag == 'data':
                view_docs = view_docs[0]
            for view_arch in view_docs:
                if not valid_type_scurve_comparison(view_arch, fromgroup=False):
                    return False
        return True

    _constraints = [
        (
            _check_xml_todo_scurve_comparison,
            'Invalid XML for S-curve Comparison architecture',
            ['arch'],
        ),
    ]