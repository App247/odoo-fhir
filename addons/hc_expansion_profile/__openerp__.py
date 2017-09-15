# -*- coding: utf-8 -*-
{
    'name': "Expansion Profile",

    'summary': """
        Constraints on expansion of value sets
        """,

    'description': """
        Resource to define constraints on the Expansion of a FHIR ValueSet.

        **Scope and Usage**

        The purpose of the expansion profile is to allow a client that is using a terminology service to configure the behaviour of the terminology server in regard to how it
        builds expansions - and, in a similar manner, how it validates codes in value set.
    """,

    'author': "Luigi Sison",
    'website': "https://hl7-fhir.github.io/expansionprofile.html",

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
        'views/hc_res_expansion_profile_views.xml',
        'views/hc_res_expansion_profile_templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    'installable': 'True',
    'auto-install': 'True',
}
