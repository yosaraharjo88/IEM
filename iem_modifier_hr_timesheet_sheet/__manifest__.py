# -*- coding: utf-8 -*-
{
    'name': 'IEM Modifier Timesheet',
    'version': '1.0',
    'category': 'Project',
    'summary': 'Timesheet customization and Notification mail to user if someone edited their timesheet',
    'description': "Timesheet customization and Notification mail to user if someone edited their timesheet",
    'author': "HashMicro/ Antsyz-Goutham Thapa",
    'website': "www.hashmicro.com",
    'depends': [
        'project_timesheet_extension'
    ],
    'data': [
        'data/ir_cron_data.xml',
        'data/hr_timesheet_notification_template.xml',
        'views/hr_timesheet_sheet_view.xml',
    ],
    'installable': True,
    'application': True,
}