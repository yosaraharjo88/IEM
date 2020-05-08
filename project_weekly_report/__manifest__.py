# -*- coding: utf-8 -*-
{
    'name': 'Project Weekly Report',
    'version': '1.0',
    'category': 'Project',
    'sequence': 1,
    'summary': ' create weekly report',
    'description': "This module will create project report weekly.",
    'website': 'http://www.hashmicro.com/',
    'author': 'Hashmicro / Niyas',
    'depends': ['project_issue_extension'],
    'data': [
            'views/project_weekly_report_view.xml',
        'security/ir.model.access.csv',

    ],
    'qweb' : [
    ],
    'installable': True,
    'auto_install': False,
    'application': True,
}
