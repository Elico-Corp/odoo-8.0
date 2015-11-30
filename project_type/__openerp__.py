# -*- coding: utf-8 -*-
# © 2015 Elico Corp (www.elico-corp.com).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
{
    "name": "Project Configurable Type",
    "summary": "Allow for Project specific type lists for Tasks",
    "version": "8.0.1.0.0",
    "category": "Project Management",
    "website": "www.elico-corp.com",
    "author": "Elico corp",
    "license": "AGPL-3",
    "application": False,
    "installable": True,
    "depends": [
        "project",
    ],
    "data": [
        'security/ir.model.access.csv',
        "views/task_category_view.xml",
        "data/task_category_demo.xml",
    ],
}
