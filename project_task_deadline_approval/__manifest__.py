{
    "name": "Project Task Deadline Approval",
    "category": 'Project',
    'summary': '',
    "description": """
        - Project/Task Deadline Request and Approval.
        - Create function for only selected employee from Project Team tab of Project Details can approve change Task Deadline request. | v0.2 | 071029.  
    """,
    "sequence": 1,
    'version': '0.2',
    "author": "Hashmicro/Arjun/Techultra - Krutarth",
    "website": "http://hashmicro.com/",
    "depends": ['base', 'project', 'web_readonly_bypass', 'project_extension', 'hr'],
    "data": [
        'views/task_deadline_view.xml',
        'views/project_project_view.xml',
    ],
    "installable": True,
    "application": True,
    "auto_install": False,
}
