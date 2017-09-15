# -*- coding: utf-8 -*-
{
    'name': "Compartment Definition",

    'summary': """
        Logical grouping of resources
        """,

    'description': """
        A compartment definition that defines how resources are accessed on a server.

        **Scope and Usage**

        Each resource may belong to one or more logical compartments. A compartment is a logical grouping of resources which share a common property. Compartments have two principal roles:

        * Function as an access mechanism for finding a set of related resources quickly
        * Provide a definitional basis for applying access control to resources quickly
    """,

    'author': "Luigi Sison",
    'website': "https://hl7-fhir.github.io/compartmentdefinition.html",

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
        'views/hc_res_compartment_definition_views.xml',
        'views/hc_res_compartment_definition_templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    'installable': 'True',
    'auto-install': 'True',
}
