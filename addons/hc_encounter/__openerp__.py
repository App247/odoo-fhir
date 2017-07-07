# -*- coding: utf-8 -*-
{
    'name': "Encounter",

    'summary': """
        Patient-Provider Interaction
    """,

    'description': """
        An interaction between a patient and healthcare provider(s) for the purpose of providing healthcare service(s) 
        or assessing the health status of a patient.

        **Scope and Usage**

        A patient encounter is further characterized by the setting in which it takes place. 
        Amongst them are ambulatory, emergency, home health, inpatient and virtual encounters. 
        An Encounter encompasses the lifecycle from pre-admission, the actual encounter (for ambulatory encounters), 
        and admission, stay and discharge (for inpatient encounters).

        During the encounter the patient may move from practitioner to practitioner and location to location.
    """,

    'author': "Luigi Sison",
    'website': "https://hl7-fhir.github.io/encounter.html",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/openerp/addons/base/module/module_data.xml
    # for the full list
    'category': 'Health Care',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['hc_episode_of_care', 'hc_appointment'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'data/data_encounter.xml',
        'views/hc_res_encounter_views.xml',
        'views/hc_res_encounter_templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    'installable': 'True',
    'auto-install': 'True',
}