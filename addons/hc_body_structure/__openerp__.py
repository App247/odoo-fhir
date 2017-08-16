# -*- coding: utf-8 -*-
{
    'name': "Body Structure",

    'summary': """
        Anatomic structure""",

    'description': """
        Record details about an anatomical structure. This resource may be used when a coded concept does not provide the necessary detail needed for the use case.

        10.8.1 Scope and Usage
        The BodyStructure resource contains details about the anatomical location of a specimen or body part, including patient information, identifiers,
        as well as text descriptons and images. It provides for the addition of qualifiers such as laterality and directionality to the anatomic location
        for those use cases where precoordination of codes is not possible. The BodyStructure resource supports recording and tracking of an anatomic location
        or structure on a patient outside the context of another resource. For example it can be the target of a Procedure resource or Observation resource.
    """,

    'author': "Luigi Sison",
    'website': "https://hl7-fhir.github.io/bodystructure.html",

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
        'data/data_body_structure.xml',
        'views/hc_res_body_structure_views.xml',
        'views/hc_res_body_structure_templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    'installable': 'True',
    'auto-install': 'True',
}
