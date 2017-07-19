# -*- coding: utf-8 -*-
{
    'name': "Structure Definition",

    'summary': """
        FHIR Structures (e.g., resources, data types, extensions, constraints)
        """,

    'description': """
        A definition of a FHIR structure. This resource is used to describe the underlying resources, data types defined in FHIR, 
        and also for describing extensions, and constraints on resources and data types. 

        **Scope and Usage** 

        The StructureDefinition resource describes a structure - a set of data element definitions, and their associated rules of usage. 
        These structure definitions are used to describe both the content defined in the FHIR specification itself - Resources, data types, 
        the underlying infrastructural types, and also are used to describe how these structures are used in implementations. 
        This allows the definitions of the structures to be shared and published through repositories of structure definitions, compared with each other, 
        and used as the basis for code, report and UI generation. 
    """,

    'author': "Luigi Sison",
    'website': "https://hl7-fhir.github.io/structuredefinition.html",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/openerp/addons/base/module/module_data.xml
    # for the full list
    'category': 'Health Care',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['hc_base'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'data/data_structure_definition_ccda_care_plan.xml',
        'views/hc_res_structure_definition_views.xml',
        'views/hc_res_structure_definition_templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    'installable': 'True',
    'auto-install': 'True',
}