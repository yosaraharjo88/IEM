# -*- coding: utf-8 -*-
{
    'name': 'project_issue_extension',
    'version': '1.0',
    'category': 'Project',
    'sequence': 7,
    'summary': 'Add issue smart button and issue for each project and task to help user track and handle ongoing issue in project.',
    'description': "add issue smart button and issue for each project and task to help user track and handle ongoing issue in project.",
    'website': 'www.hashmicro.com',
    'author': 'Hashmicro/GYB IT SOLUTIONS-Trivedi, Hashmicro/ PYVTECH - Yajushi',
    'depends': [
        'project_issue','project_extension'
    ],
    'data': [
        'views/project_issue.xml',
    ],
    'installable': True,
    'auto_install': True,
    'application': True,
}
