# -*- coding: utf-8 -*-

{
    'name': 'Iem Modifier Timesheet',
    'version': '1.1',
    'category': 'Timesheet',
    'summary': ' ',
    'description': " Make description column in timesheet non compulsory",
    'author': "HashMicro/Smidh Vadera",
    'website':"www.hashmicro.com",
    'maintainer': 'HashMicro',
    'depends': ['iem_modifier_hr_timesheet_sheet','std_timesheet_access_rights'],
    'data': [
        'views/view_hr_timesheet_sheet_inherit.xml',
        'views/time_sheet_setting_view.xml',
    ], 
    'installable': True,
    'application': False,
    
}
