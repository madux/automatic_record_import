# -*- coding: utf-8 -*-
##############################################################################
#

##############################################################################
{
    'name' : 'Odoo Auto import',
    'version' : '10.0',
    'author' : 'Maach Media',
    'category' : 'Extra Tools',
    'description' : """Import your Membership records with different scenario as per your business requirements""",
    "summary":"Odoo Auto import Module for Membership Migration via csv/xls",
    "price": "200.00",
    "currency": "EUR", 
    'images': ['static/description/icon.png'],
    'depends' : ['member_app'],
    'data': [
        'view/auto_import_view.xml',
    ],
    'qweb' : [
    ],
    'test': [
    ],
    'installable': True,
    'auto_install': False,
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
