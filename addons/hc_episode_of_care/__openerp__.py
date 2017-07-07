# -*- coding: utf-8 -*-
{
    'name': "Episode of Care",

    'summary': """
        Related patient-provider healthcare activities
    """,

    'description': """
        An association between a patient and an organization / healthcare provider(s) during which time encounters 
        may occur. The managing organization assumes a level of responsibility for the patient during this time.

        **Scope and Usage**

        The EpisodeOfCare Resource contains information about an association of a Patient with a Healthcare Provider 
        for a period of time under which related healthcare activities may occur.

        In many cases, this represents a period of time where the Healthcare Provider has some level of responsibility 
        for the care of the patient regarding a specific condition or problem, even if not currently participating in 
        an encounter.

        These resources are typically known in existing systems as:

        * EpisodeOfCare: Case, Program, Problem, Episode
        * Encounter: Visit, Contact
    """,

    'author': "Luigi Sison",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/openerp/addons/base/module/module_data.xml
    # for the full list
    'category': 'Health Care',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['hc_condition', 'hc_account', 'hc_care_team'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'data/data_episode_of_care.xml',
        'views/hc_res_episode_of_care_views.xml',
        'views/hc_res_episode_of_care_templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    'installable': 'True',
    'auto-install': 'True',
}