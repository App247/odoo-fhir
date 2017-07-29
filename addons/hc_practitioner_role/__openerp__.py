# -*- coding: utf-8 -*-
{
    'name': "Practitioner Role",

    'summary': """
        Practitioner roles, locations, specialties, services
    """,

    'description': """
        A specific set of Roles/Locations/specialties/services that a practitioner may perform at an organization for a period of time.

        **Scope and Usage**

        PractitionerRole covers the recording of the location and types of services that Practitioners are able to provide for an organization.

        The role, specialty, Location telecom and HealthcareService properties can be repeated if required in other instances of the PractitionerRole.
        Some systems record a collection of service values for a single location, others record the single service and the list of locations it is available.
        Both are acceptable options for presenting this data.
    """,

    'author': "Luigi Sison",
    'website': "https://hl7-fhir.github.io/practitionerrole.html",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/openerp/addons/base/module/module_data.xml
    # for the full list
    'category': 'Health Care',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['hc_practitioner'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'data/data_practitioner_role.xml',
        'views/hc_res_practitioner_role_views.xml',
        'views/hc_res_practitioner_role_templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
