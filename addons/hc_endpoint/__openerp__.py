# -*- coding: utf-8 -*-
{
    'name': "Endpoint",

    'summary': """
        Technical details
        """,

    'description': """
        The technical details of an endpoint that can be used for electronic services, such as for web services providing XDS.b or a REST endpoint for another FHIR server.
        This may include any security context information.

        **Scope and Usage**

        An endpoint describes the technical details of a location that can be connected to for the delivery/retrieval of information.
        Sufficient information is required to ensure that a connection can be made securely, and appropriate data transmitted as defined by the endpoint owner.
        This is not a description of details of the current system, as found in conformance, but of another (potentially external) system.
    """,

    'author': "Luigi Sison",
    'website': "https://hl7-fhir.github.io/endpoint.html",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/openerp/addons/base/module/module_data.xml
    # for the full list
    'category': 'Health Care',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['hc_organization'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'data/hc.vs.endpoint.connection.type.csv',
        'data/hc.vs.endpoint.payload.type.csv',
        'examples/example.xml',
        'views/hc_res_endpoint_views.xml',
        'views/hc_res_endpoint_templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    'installable': 'True',
    'auto-install': 'True',
}
