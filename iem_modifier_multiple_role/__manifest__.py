{
    'name':"IEM Modifier Multiple Role",
    'summary': """ 
        Project Employee Cost Report based on PD 
    """,
    'description': '',
    'category': 'Project',
    'version':'1.0',
    'author': "HashMicro / Allen",
    'website':"http://www.hashmicro.com",
    'depends': ['project_employee_planned_actual_cost'],
    'data': [
        'security/ir.model.access.csv',
        'views/assets.xml',
        'views/project_project_view.xml',
    ],
    'installable': True,
    'application': False,
}
