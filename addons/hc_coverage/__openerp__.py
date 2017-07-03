# -*- coding: utf-8 -*-
{
    'name': "Coverage",

    'summary': """
        Insurance plans
        """,

    'description': """
        Financial instrument which may be used to pay for or reimburse health care products and services.

        **Scope and Usage**

        The Coverage resource is intended to provide the high level identifiers and potentially descriptors of 
        insurance plans which may used to pay for, in part or in whole, the provision of health care products and services.
    """,

    'author': "Luigi Sison",
    'website': "https://hl7-fhir.github.io/coverage.html",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/openerp/addons/base/module/module_data.xml
    # for the full list
    'category': 'Health Care',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['hc_patient'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/hc_res_coverage_views.xml',
        'views/hc_res_coverage_templates.xml',
        'data/data_coverage.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    'installable': 'True',
    'auto-install': 'True',
}