# -*- coding: utf-8 -*-
{
    'name': "Request Group",

    'summary': """
        Related requests
        """,

    'description': """
        A group of related requests that can be used to capture intended activities that have inter-dependencies such as "give this medication after that one".

        **Scope and Usage**

        The RequestGroup resource is used to represent a group of optional activities that may be performed for a specific patient or context.
    """,

    'author': "Luigi Sison",
    'website': "https://hl7-fhir.github.io/requestgroup.html",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/openerp/addons/base/module/module_data.xml
    # for the full list
    'category': 'Health Care',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['hc_base_metadata_type', 'hc_encounter'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/hc_res_request_group_views.xml',
        'views/hc_res_request_group_templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    'installable': 'True',
    'auto-install': 'True',
}
