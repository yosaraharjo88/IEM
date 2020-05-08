# -*- coding: utf-8 -*-

{
    'name':"Project Timesheet Ext",
    'summary': """
    """,
    'description': '',
    'category': 'Project',
    'version':'1.0',
    'author': "Vasant Chauhan",
    'depends': ['hr_timesheet_attendance','project_extension', 'Project_employee_cost'],
    'data': [
        'views/hr_timesheet_sheet_views.xml',
        'views/project_task_view.xml',
    ],
    'installable': True,
    'application': False,
}
