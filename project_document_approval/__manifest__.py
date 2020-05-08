# -*- coding: utf-8 -*-
{
    'name': "project_document_approval",

    'summary': """
        Allow user to approve document.
        """,

    'description': """
        Allow user to approve document
    """,

    'author': "Hashmicro / Vasant Chauhan",
    'website': "http://www.hashmicro.com",

    'category': 'Project',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'project_extension'],

    # always loaded
    'data': [
        'views/ir_attachment_view.xml',
        'views/project_task_view.xml'
    ],
}
