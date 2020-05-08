# -*- coding: utf-8 -*-
{
    "name": "Project Access Rights",
    "author": "HashMicro / Sagar",
    "version": "1.0",
    'description': """
    """,
    'summary': 'Project Access Rights for all Users',
    "website": "www.hashmicro.com",
    "category": "project",
    "depends": [
        'project_extension', 'project_issue', 'project_native', 'project_weekly_report',
        'project_task_deadline_approval', 'project_team_role','project_template_job_order',
    ],
    "data": [
        'security/ir.model.access.csv',
        'security/security_view.xml',
        'views/views.xml',
    ],
    "qweb": [],
    'demo': [],
    'installable': True,
    'auto_install': False,
}
