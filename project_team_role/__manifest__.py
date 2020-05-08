# -*- coding: utf-8 -*-

{
    'name': 'Project Team Role',
    'version': '1.1',
    'category': 'project',
    'summary': ' ',
    'description': " Add new Role master in Project menu",
    'author': "HashMicro/Smidh Vadera",
    'website':"www.hashmicro.com",
    'maintainer': 'HashMicro',
    'depends': ['project_native',],
    'data': [
        'security/ir.model.access.csv',
        'views/team_role_view.xml',
    ], 
    'installable': True,
    'application': False,
    
}
