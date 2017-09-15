# -*- coding: utf-8 -*-
{
    'name': "Naming System",

    'summary': """
        Definition of code systems and identifier systems
        """,

    'description': """
        A curated namespace that issues unique symbols within that namespace for the identification of concepts, people, devices, etc.
        Represents a "System" used within the Identifier and Coding data types.

        **Scope and Usage**

        Defines a specific code system or identifier system, so that it can be noted in a registry for other systems to find and understand the identifier.
    """,

    'author': "Luigi Sison",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/openerp/addons/base/module/module_data.xml
    # for the full list
    'category': 'Health Care',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['hc_base_metadata_type'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/hc_res_naming_system_views.xml',
        'views/hc_res_naming_system_templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    'installable': 'True',
    'auto-install': 'True',
}
