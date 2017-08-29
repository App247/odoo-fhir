# -*- coding: utf-8 -*-
{
    'name': "Appointment",

    'summary': """
        Scheduled events (e.g., clinical visit, scheduled surgery, device reservation)
        """,

    'description': """
        A booking of a healthcare event among patient(s), practitioner(s), related person(s) and/or device(s) for a specific date/time. This may result in one or more Encounter(s).

        **Scope and Usage**

        Appointment resources are used to provide information about a planned meeting that may be in the future or past. The resource only describes a single meeting,
        a series of repeating visits would require multiple appointment resources be created for each instance. Examples include a scheduled surgery,
        a follow-up for a clinical visit, a scheduled conference call between clinicians to discuss a case, the reservation of a piece of diagnostic equipment
        for a particular use, etc. The visit scheduled by an appointment may be in person or remote (by phone, video conference, etc.) All that matters is that the time and usage of one or more individuals, locations and/or pieces of equipment is being fully or partially reserved for a designated period of time.

        This definition takes the concepts of appointments in a clinical setting and also extends them to be relevant in the community healthcare space,
        and also ease exposure to other appointment / calendar standards widely used outside of healthcare.
    """,

    'author': "Luigi Sison",
    'website': "http://build.fhir.org/appointment.html",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/openerp/addons/base/module/module_data.xml
    # for the full list
    'category': 'Health Care',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['hc_slot'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/hc_res_appointment_views.xml',
        'views/hc_res_appointment_templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    'installable': 'True',
    'auto-install': 'True',
}
