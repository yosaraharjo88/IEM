# -*- coding: utf-8 -*-
{
    'name': "Project Budget Scurve Report",

    'summary': """
        Project Budget Report for Construction.
        """,

    'description': """
        - Project Budget Report for Construction custom table view and Graph view.
        - last update: 27AG19
        - Add more two line and two check box for Planned and Actual Budget. | v1.3 | 05SP19.
        - Add Planned Budget in S-curve comparison view. | v1.4 | 12SP19.
        - Arranged Planned Budget, Total Planned Budget Amount, Actual Budget, Total Actual Budget Amount in table. | v1.5 | 13SP19.
        - Add and Actual Budget amount in S-curve comparison view. | v1.6 | 23SP19.
        - Change the amount format. Add some space after Table. | v1.7 | 25SP19.
        - Add for Actual Progress line showing multi-color. | v1.8 | 26SP19.
    """,

    'author': "Hashmicro / TechUltra - Krutarth",
    'website': "http://www.hashmicro.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/10.0/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Project',
    'version': '10.0.1.7',

    # any module necessary for this one to work correctly
    'depends': ['project_management_report'],

    # always loaded
    'data': [
        # 'security/ir.model.accesss.csv',
        'views/project_budget_report_view.xml',
        'views/resources.xml',
    ],
    'qweb': [
        # 'static/src/xml/templates.xml',
        'static/src/xml/project_budget_table_view.xml',
        'static/src/xml/project_budget_graph_view.xml',
        'static/src/xml/scurve_comparison_template_inherit.xml',
    ]
}
