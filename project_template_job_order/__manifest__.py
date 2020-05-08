{
    'name': "Project Template Job Order",
    'summary': """ """,
    'description': """ 
        - New submenu Task Template and Project Template master data.
        - Change field type, auto create stage & tasks function in create project pop up form view. V0.2
     """,
    'category': 'Project',
    'version': '1.0',
    'author': "HashMicro / Smidh Vadera / Yajushi-PYVTech",
    'website': "http://www.hashmicro.com",
    'depends': ['project_native', 'project_successor'],
    'data': [
        'security/ir.model.access.csv',
        'views/task_template_view.xml',
        'views/project_template_view.xml',
        'views/project_view.xml',
    ],
    'installable': True,
    'application': False,
}
