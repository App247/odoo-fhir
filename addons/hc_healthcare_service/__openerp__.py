# -*- coding: utf-8 -*-
{
    'name': "Healthcare Service",

    'summary': """
        Health care services at a location
        """,

    'description': """
        The details of a healthcare service available at a location.

        **Scope and Usage**

        The Healthcare Service resource is used to describe a single healthcare service or category of services
        that are provided by an organization at a location. The location of the services could be virtual, as with TeleMedicine Services.
    """,

    'author': "Luigi Sison",
    'website': "https://hl7-fhir.github.io/healthcareservice.html",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/openerp/addons/base/module/module_data.xml
    # for the full list
    'category': 'Health Care',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['hc_location'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'data/data_healthcare_service.xml',
        'data/hc.vs.service.category.csv',
        'data/hc.vs.service.type.csv',

        'examples/example.xml',

        'views/hc_res_healthcare_service_views.xml',
        'views/hc_res_healthcare_service_templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    'installable': 'True',
    'auto-install': 'True',
}
