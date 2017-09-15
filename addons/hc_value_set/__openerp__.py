# -*- coding: utf-8 -*-
{
    'name': "Value Set",

    'summary': """
        Set of codes
        """,

    'description': """
        A value set specifies a set of codes drawn from one or more code systems.

        **Scope and Usage**

        The FHIR terminology specification is based two key concepts, originally defined in HL7 v3 Core Principles :

        * CodeSystem - defines a set of codes with meanings (also known as enumeration, terminology, classification, and/or ontology) - e.g. define which codes (symbols and/or expressions) exist, and how they are understood
        * ValueSet - selects a set of codes from those defined by one or more code systems to specify which codes can be used in a particular context
    """,

    'author': "Luigi Sison",
    'website': "https://hl7-fhir.github.io/valueset.html",

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
        'views/hc_res_value_set_views.xml',
        'views/hc_res_value_set_templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    'installable': 'True',
    'auto-install': 'True',
}
