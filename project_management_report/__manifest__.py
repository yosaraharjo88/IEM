# -*- coding: utf-8 -*-
{
    'name': "Project Management Report",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': """
        - Table view and Graph view for Project report -> 0.1
        - Add new submenu for Project Progress Report & Remove selection & button in report view from Project -> 0.2
        - Add new custom S-curve Comparison view -> 04SP19 -> 1.5
    """,

    'author': "Hashmicro / TechUltra - Krutarth",
    'website': "http://www.hashmicro.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/10.0/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Project',
    'version': '10.0.1.5',

    # any module necessary for this one to work correctly
    'depends': ['project_extension'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/project_project_form.xml',
        'views/project_task_view_inherit.xml',
        'views/resources.xml',
    ],
    'qweb': [
        # 'static/src/xml/templates.xml',
        'static/src/xml/project_progress_table_view.xml',
        'static/src/xml/project_progress_graph_view.xml',
        'static/src/xml/scurve_comparison_template.xml'
    ],
}
