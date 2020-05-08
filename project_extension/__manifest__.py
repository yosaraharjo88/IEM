# -*- coding: utf-8 -*-
{
    'name': "Project Extension",

    'summary': """
        This is an extension of 'project'.
        """,

    'description': """
        * Added new field ‘Start Date’, ‘End Date’, ‘Planned Progress’, ‘Progress Completion’ and hide ‘Deadline’ field.
        * Add new column ‘Status’ in Progress History after Progress Summary. | v1.6 | 26SP19.
        * Add tree for Project dashboard. | v1.7. 
	* Fix error when save Team members under Project Details task by Vivian | v1.8 | 16DE19 | Dev: Krutarth.
    """,

    'author': "Hashmicro / TechUltra - Pratik / Himanee / Ritesh / Sagar / TechUltra - Krutarth",
    'website': "http://www.hashmicro.com",

    'category': 'Project',
    'version': '1.7',

    # any module necessary for this one to work correctly
    'depends': ['project_native', 'project_issue', 'project', 'base', 'project_team_role', 'hr_timesheet_attendance'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'data/project_seq_view.xml',
        'data/project_milestone_sequence.xml',
        'data/deadline_reminder_cron_view.xml',
        'views/project_task_type_view_inherit.xml',
        'views/project_project_view_inherit.xml',
        'views/resources.xml',
        'views/project_task_view_inherit.xml',
        'views/project_stage_project_view.xml',
        'views/project_scope_view.xml',
        'views/project_team_view.xml',
        'views/project_documents_view.xml',
        'views/project_milestone_status.xml',
        'views/project_views_inherit.xml',
        'views/project_stage_detail_view.xml',
        'views/project_field_view.xml',
        'views/attechment_form_inherit_view.xml',
        'views/document_menu_view.xml',
        'views/sequence_view.xml',
    ],
    'qweb': [
        'static/src/xml/*.xml',
    ],
}
