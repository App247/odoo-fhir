# -*- coding: utf-8 -*-
{
    'name': "Terminology Capability",

    'summary': """
        FHIR Server terminology capabilities
        """,

    'description': """
        A Terminology Capabilities documents a set of capabilities (behaviors) of a FHIR Server that may be used
        as a statement of actual server functionality or a statement of required or desired server implementation.

        **Scope and Usage**

        The capability statement is a key part of the overall conformance framework in FHIR. It is used as a statement of the features of actual software, or of a set of rules for an application to provide. This statement connects to all the detailed statements of functionality, such as StructureDefinitions and ValueSets. This composite statement of application capability may be used for system compatibility testing, code generation, or as either the basis for a conformance assessment.
    """,

    'author': "Luigi Sison",
    'website': "https://hl7-fhir.github.io/terminologycapabilities.html",

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
        'views/hc_res_terminology_capability_views.xml',
        'views/hc_res_terminology_capability_templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    'installable': 'True',
    'auto-install': 'True',
}
