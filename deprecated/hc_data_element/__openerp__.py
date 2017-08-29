# -*- coding: utf-8 -*-
{
    'name': "Data Element",

    'summary': """
        Data element definitions
        """,

    'description': """
        The formal description of a single piece of information that can be gathered and reported. 

        **Scope and Usage**

        DataElement is an infrastructure resource that supports the defining individual pieces of data that might be collected or stored. 
        While these definitions might apply to elements found in FHIR resources and profiles, they can also apply to questionnaire questions, 
        elements in data stores, and non-FHIR specification (HL7 v2 , CDA , CDISC, etc.) I.e. the definitions aren't FHIR-specific. 
        
        This resource covers two major use-cases: 
        
        * Definitions of types of measurements or observations that may be requested or performed. In HL7, these are sometimes referred to as service, test or observation "master files"
        * Definitions of "data elements" (DEs) that may be used in questionnaires (survey instruments and data collection forms) and profiles and potentially mapped to elements in other resources and profiles
    """,

    'author': "Luigi Sison",
    'website': "https://hl7-fhir.github.io/dataelement.html",

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
        'views/hc_res_data_element_views.xml',
        'views/hc_res_data_element_templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    'installable': 'True',
    'auto-install': 'True',
}