# -*- coding: utf-8 -*-
{
    'name': "Diagnostic Request",

    'summary': """
        Request for diagnostic investigation
        """,

    'description': """
        A record of a request for a diagnostic investigation service to be performed.

        **Scope and Usage**

        A Diagnostic Request is a record of a request for a set of diagnostic investigations to be performed. 
        The investigation will lead to a Diagnostic Report that summarizes the outcome of the investigation, and includes any 
        useful data and/or images that are relevant to the treatment/management of the subject.
    """,

    'author': "Luigi Sison",
    'website': "https://hl7-fhir.github.io/diagnosticrequest.html",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/openerp/addons/base/module/module_data.xml
    # for the full list
    'category': 'Health Care',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['hc_provenance', 'hc_encounter'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/hc_res_diagnostic_request_views.xml',
        'views/hc_res_diagnostic_request_templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    'installable': 'True',
    'auto-install': 'True',
}