# -*- coding: utf-8 -*-
{
    'name': "Body Site",

    'summary': """
        Anatomical location of a body part or specimen
        """,

    'description': """
        Record details about the anatomical location of a specimen or body part. This resource may be used when a coded concept 
        does not provide the necessary detail needed for the use case.

        **Scope and Usage**

        The BodySite resource contains details about the anatomical location of a specimen or body part, including patient information, 
        identifiers, as well as text descriptons and images. It provides for the addition of modifiers such as laterality and directionality 
        o the anatomic location for those use cases where precoordination of codes is not possible. The BodySite resource supports recording 
        and tracking of an anatomic location or structure on a patient outside the context of another resource. For example it can be the target 
        of a Procedure resource or Observation resource.
    """,

    'author': "Luigi Sison",
    'website': "https://hl7-fhir.github.io/bodysite.html",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/openerp/addons/base/module/module_data.xml
    # for the full list
    'category': 'Health Care',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['hc_patient'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/hc_res_body_site_views.xml',
        'views/hc_res_body_site_templates.xml',
        'data/hc.vs.body.site.relative.location.csv',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    'installable': 'True',
    'auto-install': 'True',
}