# -*- coding: utf-8 -*-
{
    'name': "Implementation Guide Output",

    'summary': """
        Output rules to solve a problem
        """,

    'description': """
        A set of rules of how FHIR is used to solve a particular problem. This resource is used to gather all the parts of an implementation guide into a logical whole and to publish a computable definition of all the parts.

        **Scope and Usage**

        Placeholder for discussion of splitting ImplementationGuide. This resource is focused on use-cases for the ImplementationGuide after the publication process is complete, specifically:

        * Exposing metadata relevant for exposing an implementation guide in a registry
        * Information necessary to support using the implementation guide for instance validation (what resources are part of the IG, what default profiles are declared and imported/contained guides)
        * Information an IG authoring tool requires when refrencing a previously published IG as a dependency, including what artifacts are defined and what links are allowed.
    """,

    'author': "Luigi Sison",
    'website': "https://hl7-fhir.github.io/implementationguideoutput.html",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/openerp/addons/base/module/module_data.xml
    # for the full list
    'category': 'Health Care',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['hc_structure_definition'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/hc_res_implementation_guide_output_views.xml',
        'views/hc_res_implementation_guide_output_templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    'installable': 'True',
    'auto-install': 'True',
}
