# -*- coding: utf-8 -*-
{
    'name': "IEM Modifier Notification",

    'summary': """
        Send Notification Mail to Employee In case of Reset or Change timesheet by Administor
        """,

    'description': """
        Send Notification Mail to Employee In case of Reset or Change timesheet by Administor
    """,

    'author': "Hashmicro / Vasant Chauhan",
    'website': "http://www.hashmicro.com",

    'category': 'Project',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['hr_timesheet_sheet', 'project_extension'],

    # always loaded view
    'data': [
        'data/notification_mail_templete_view.xml',
        'data/mail_scheduler_view.xml',
    ],
}
