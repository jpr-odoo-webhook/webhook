# -*- coding: utf-8 -*-
{
    'name': 'GitHub',
    'category': 'Website',
    'summary': 'Pretty Way to Display GitHub pull request',
    'version': '1.0',
    'description': """
Display your social media to large screen
=========================================
""",
    'author': 'Odoo S.A.',
    'depends': ['website'],
    'website': 'https://www.odoo.com',
    'data': [
        'views/website_github_template.xml',
        'views/res_config.xml'
    ],
    'qweb': ['static/src/xml/*.xml'],
    'installable': True,
}
