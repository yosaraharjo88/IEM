# -*- coding: utf-8 -*-
{
    'name': "Project Successor",

    'summary': """
        This is an extension of 'project'.
        """,

    'description': """
        Added new tab successor in the project task 
    """,

    'author': "Hashmicro / TechUltra - Pratik",
    'website': "http://www.hashmicro.com",

    'category': 'Project',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['project_native','project_extension'],

    # always loaded
    'data': [
        'views/project_task_inherit_view.xml',
    ],
}
