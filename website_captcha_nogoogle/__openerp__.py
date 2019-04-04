# -*- coding: utf-8 -*-
# © 2015 Elico corp (www.elico-corp.com)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
{
    'name': 'Website Captcha',
    'version': '8.0.1.0.0',
    'category': 'Website',
    'depends': [
        'website',
    ],
    'author': 'Elico Corp',
    # 'license': 'LGPL-3',
    'website': 'https://www.elico-corp.com',
    'currency': 'EUR',
    'price': 19.9,
    'data': [
        'views/website_templates.xml',
        'views/res_config.xml',
    ],
    'external_dependencies': {
        'python': ['captcha', 'simplecrypt'],
    },
    'installable': True,
    'auto_install': False}
