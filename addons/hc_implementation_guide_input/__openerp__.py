# -*- coding: utf-8 -*-
{
    'name': "Implementation Guide Input",

    'summary': """
        Input Rules to solve a problem
        """,

    'description': """
        A set of rules of how FHIR is used to solve a particular problem. This resource is used to gather all the parts of an implementation guide into a logical whole and to publish a computable definition of all the parts.

        **Scope and Usage**

        Placeholder for discussion of splitting ImplementationGuide. This resource is focused on content needed to support publishing of an ImplementationGuide.
    """,

    'author': "Luigi Sison",
    'website': "https://hl7-fhir.github.io/implementationguideinput.html",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/openerp/addons/base/module/module_data.xml
    # for the full list
    'category': 'Health Care',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['hc_structure_definition', 'hc_binary'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/hc_res_implementation_guide_input_views.xml',
        'views/hc_res_implementation_guide_input_templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    'installable': 'True',
    'auto-install': 'True',
}
