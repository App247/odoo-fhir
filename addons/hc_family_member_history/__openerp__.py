# -*- coding: utf-8 -*-
{
    'name': "Family Member History",

    'summary': """
        Health events and conditions of patient's relatives
    """,

    'description': """
        Significant health events and conditions for a person related to the patient relevant in the context of care for the patient.

        **Scope and Usage**

        This resource records significant health events and conditions for a particular individual related to the subject. This information can be known to different levels of accuracy. Sometimes the exact condition ('asthma') is known, and sometimes it is less precise ('some sort of cancer'). Equally, sometimes the person can be identified ('my aunt Agatha') and sometimes all that is known is that the person was an uncle.

        This resource represents a simple structure used to capture an 'elementary' family history for a particular family member. However, it can also be the basis for capturing a more rigorous history useful for genetic and other analysis - refer to the Genetic Pedigree profile for an example.
    """,

    'author': "Luigi Sison",
    'website': "https://hl7-fhir.github.io/familymemberhistory.html",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/openerp/addons/base/module/module_data.xml
    # for the full list
    'category': 'Health Care',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['hc_allergy_intolerance', 'hc_condition', 'hc_plan_definition', 'hc_questionnaire_response'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'data/data_family_member_history.xml',
        'data/hc.vs.v3.family.member.csv',
        'views/hc_res_family_member_history_views.xml',
        'views/hc_res_family_member_history_templates.xml',
    ],
    
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}