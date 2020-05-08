# -*- coding: utf-8 -*-
{
    'name': 'IEM Timesheet Access Modifier',
    'version': '1.0',
    'category': 'Project',
    'summary': 'Timesheet customization and Notification mail to user for all timesheet',
    'description': "Timesheet customization and Notification mail to user for all timesheet",
    'author': "HashMicro/ Antsyz-Kannan",
    'website': "www.hashmicro.com",
    'depends': [
        'std_timesheet_access_rights','iem_modifier_hr_timesheet_sheet'
    ],
    'data': [
        'views/hr_timesheet_sheet_view.xml',
    ],
    'installable': True,
    'application': True,
}