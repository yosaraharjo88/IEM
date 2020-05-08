# -*- coding: utf-8 -*-
{
    'name': "project employee planned actual cost",

    'summary': """
        Add field in measures in pivot view""",

    'description': """
        Long description of module's purpose to Add field in measures in pivot view
    """,

    'author': "Hashmicro / Ritesh",
    'website': "http://www.hashmicro.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['project_timesheet_extension',
                'project_access_rights',],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/views.xml',
        'report/new_pivot_view.xml',
    ],
}