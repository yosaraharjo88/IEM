# -*- coding: utf-8 -*-

{
    "name": "Project Employee Cost",
    'summary': """
    		Project Employee Cost
        """,
    'description': """
        Project Employee Cost
    """,
    "version": "0.1",
    "category": "crm",
    "author": "Hashmicro / Uday",
    "website": "http://www.hashmicro.com",
    "depends": ['hr', 'sale_timesheet'],
    "data": [
        'security/ir.model.access.csv',
        'data/ir_cron.xml',
        'views/hr_employee_view.xml',
    ],
    "installable": True,
    "auto_install": True,
}
