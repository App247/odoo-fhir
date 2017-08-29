# -*- coding: utf-8 -*-
{
    'name': "Referral Request",

    'summary': """
        Request for referral service or transfer
        """,

    'description': """
        Used to record and send details about a request for referral service or transfer of a patient
        to the care of another provider or provider organization.

        **Scope and Usage**

        This resource is used to share relevant information required to support a referral request or a
        transfer of care request from one practitioner or organization to another. It is intended for use when a patient
        is required to be referred to another provider for a consultation/second opinion and/or for short term or longer term
        management of one or more health issues or problems.

        Examples include:

        * Request for a consult from a specialist
        * Referral for support from community services
        * District nursing services referral
        * Request for aged care placement assessment
        * Request for a pharmacist medication review
        * Referral for physiotherapy or occupational therapy

    """,

    'author': "Luigi Sison",
    'website': "https://hl7-fhir.github.io/referralrequest.html",

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
        'views/hc_res_referral_request_views.xml',
        'views/hc_res_referral_request_templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    'installable': 'True',
    'auto-install': 'True',
}
