# -*- coding: utf-8 -*-
{
    'name': "Explanation of Benefit",

    'summary': """
        Claim details, adjudication details, account balance, etc.
        """,

    'description': """
        This resource provides: the claim details; adjudication details from the processing of a Claim; and optionally account balance information,
        for informing the subscriber of the benefits provided.

        **Scope and Usage**

        The ExplanationOfBenefit resource combines key information from a Claim, a ClaimResponse and optional Account information
        to inform a patient of the goods and services rendered by a provider and the settlement made under the patients coverage in
        respect of that Claim.
    """,

    'author': "Luigi Sison",
    'website': "https://hl7-fhir.github.io/explanationofbenefit.html",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/openerp/addons/base/module/module_data.xml
    # for the full list
    'category': 'Health Care',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['hc_claim_response'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/hc_res_explanation_of_benefit_views.xml',
        'views/hc_res_explanation_of_benefit_templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    'installable': 'True',
    'auto-install': 'True',
}
