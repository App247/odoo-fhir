# -*- coding: utf-8 -*-
{
    'name': "Flag",

    'summary': """
        Notification, warning""",

    'description': """
        Prospective warnings of potential issues when providing care to the patient.

        **Scope and Usage**

        A flag is a warning or notification of some sort presented to the user - who may be a clinician or some other person involve in patient care. It usually represents something of sufficient significance to be warrant a special display of some sort - rather than just a note in the resource. A flag has a subject representing the resource that will trigger its display. This subject can be of different types, as described in the examples below:

        * A note that a patient has an overdue account, which the provider may wish to discuss with them - in case of hardship for example (subject = Patient)
        * An outbreak of Ebola in a particular region (subject=Location) so that all patients from that region have a higher risk of having that condition
        * A particular provider is unavailable for referrals over a given period (subject = Practitioner)
        * A patient who is enrolled in a clinical trial (subject=Group)
        * Special guidance or caveats to be aware of when following a protocol (subject=PlanDefinition)
        * Warnings about using a drug in a formulary requires special approval (subject=Medication)

    """,

    'author': "Luigi Sison",
    'website': "https://hl7-fhir.github.io/flag.html",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/openerp/addons/base/module/module_data.xml
    # for the full list
    'category': 'Health Care',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['hc_procedure'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/hc_res_flag_views.xml',
        'views/hc_res_flag_templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    'installable': 'True',
    'auto-install': 'True',
}
