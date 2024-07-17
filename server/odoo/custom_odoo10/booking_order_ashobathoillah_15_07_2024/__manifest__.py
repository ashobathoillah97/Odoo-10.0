# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name' : 'booking order ashob athoillah 15/07/2024',
    'version' : '0',
    'sequence': 99,
    'description': """Odoo Developer Test""",
    'category': 'WO',
    'website': 'https://www.linkedin.com/in/ashob-athoillah-756285204/',
    'depends' : ['sale','sales_team'],
    'data': [
        'security/ir.model.access.csv',
        'data/wo_number_sequence.xml',
        'wizard/wizard_cancel_view.xml',
        'views/book_order_view.xml',
        'views/work_order_view.xml',
        'report/work_order_report.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}
