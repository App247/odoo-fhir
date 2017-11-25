# -*- coding: utf-8 -*-
{
    'name': "Location",

    'summary': """
        Physical place of service
        """,

    'description': """
        Details and position information for a physical place where services are provided
        and resources and participants may be stored, found, contained or accommodated.

        **Scope and Usage**

        A Location includes both incidental locations (a place which is used for healthcare without prior designation or authorization)
        and dedicated, formally appointed locations. Locations may be private, public, mobile or fixed and scale from small freezers to
        full hospital buildings or parking garages.
    """,

    'author': "Luigi Sison",
    'website': "https://hl7-fhir.github.io/location.html",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/openerp/addons/base/module/module_data.xml
    # for the full list
    'category': 'Health Care',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['hc_endpoint'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'data/data_location.xml',
        'data/hc.vs.service.delivery.location.role.type.csv',

        'examples/example_1.xml',
        'examples/example_amb.xml',
        'examples/example_hl7.xml',
        'examples/example_ph.xml',
        'examples/example_2.xml',
        'examples/example_ukp.xml',
        'examples/example_general.xml',

        'views/hc_res_location_views.xml',
        'views/hc_res_location_templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    'installable': 'True',
    'auto-install': 'True',
}
