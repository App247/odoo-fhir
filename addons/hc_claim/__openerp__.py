# -*- coding: utf-8 -*-
{
    'name': "Claim",

    'summary': """
        Services and products for payment
        """,

    'description': """
        A provider issued list of services and products provided, or to be provided, to a patient which is provided to an insurer for payment recovery.

        **Scope and Usage**

        The Claim is used by providers and payors, insurers, to exchange the financial information, and supporting clinical information, regarding the provision of
        healthcare services with payors an firms which provide data analytics. The primary uses of this resource is to support eClaims, the exchange of proposed or
        actual services to benefit payors, insurers and national health programs, for treatment payment planning and reimbursement.

        The Claim is intended to support:

        * Claims - where the provision of goods and services is complete and reimbursement is sought.
        * Pre-Authorization - where the provision of goods and services is proposed and either authorization and/or the reservation of funds is desired.
        * Pre-Determination - where the provision of goods and services is explored to determine what services may be covered and to what amount. Essentially a 'what if' claim.

        The Claim also supports:

        * Up to a 3 tier hierarchy of Goods, products, and Services, to support simple to complex billing.
        * Multiple insurance programs arranged in a Coordination of Benefit sequence to enable exchange with primary, secondary, tertiary etc. insurance coverages.
        * Assignment of benefit - the benefit may be requested to be directed to the subscriber, the provider or another party.
    """,

    'author': "Luigi Sison",
    'website': "https://hl7-fhir.github.io/claim.html",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/openerp/addons/base/module/module_data.xml
    # for the full list
    'category': 'Health Care',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['hc_eligibility_request','hc_medication_request','hc_vision_prescription','hc_procedure'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',

        'data/data_claim.xml',

        'views/hc_res_claim_views.xml',
        'views/hc_res_claim_templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    'installable': 'True',
    'auto-install': 'True',
}
