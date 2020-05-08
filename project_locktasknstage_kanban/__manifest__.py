# -*- coding: utf-8 -*-
{
    'name': "Project Lock task & stage Kanban",

    'summary': """
        In this module, Lock task and stages into can't move.""",

    'description': """
        - Lock Stage position to can’t move to other position in Kanban view.
        - Lock Add new column in Stage Kanban view. So user can add new stage from this Kanban view.
        - Last update 05AG19-1607 --> 10.0.0.1. 
        - Old name:  project_locktask_kanban.
        
        - Remove "ADD NEW COLUMN" section from, -- 10.0.0.2 
    """,

    'author': "Hashmicro / TechUltra - Krutarth",
    'website': "http://www.hashmicro.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/10.0/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Project',
    'version': '10.0.0.2',

    # any module necessary for this one to work correctly
    'depends': ['project_extension'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/resources.xml',
        # 'views/templates.xml',
    ],
}