# -*- coding: utf-8 -*-
{
    'name': "Care Plan",

    'summary': """
        Care plan for a patient, group, or community
        """,

    'description': """
        Describes the intention of how one or more practitioners intend to deliver care for a particular patient, group or community for a period of time, possibly limited to care for a specific condition or set of conditions.

        **Scope and Usage**

        Care Plans are used in many of areas of healthcare with a variety of scopes.
        They can be as simple as a general practitioner keeping track of when their patient is next due for a tetanus immunization
        through to a detailed plan for an oncology patient covering diet, chemotherapy, radiation, lab work and counseling
        with detailed timing relationships, pre-conditions and goals. They may be used in veterinary care or clinical research
        to describe the care of a herd or other collection of animals. In public health, they may describe education or immunization campaigns.
    """,

    'author': "Luigi Sison",
    'website': "https://hl7-fhir.github.io/careplan.html",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/openerp/addons/base/module/module_data.xml
    # for the full list
    'category': 'Health Care',
    'version': '0.1',

    # any module necessary for this one to work correctly
    # 'hc_supply_request'
    'depends': ['hc_questionnaire','hc_vision_prescription','hc_goal','hc_communication_request','hc_device_request','hc_process_request', 'hc_request_group','hc_task'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/hc_res_care_plan_views.xml',
        'views/hc_res_care_plan_templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    'installable': 'True',
    'auto-install': 'True',
}
