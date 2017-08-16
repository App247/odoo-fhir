# -*- coding: utf-8 -*-
{
    'name': "Specimen Definition",

    'summary': """
        A kind of specimen""",

    'description': """
        A kind of specimen with associated set of requirements.
    """,

    'author': "Luigi Sison",
    'website': "https://hl7-fhir.github.io/specimendefinition.html",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/openerp/addons/base/module/module_data.xml
    # for the full list
    'category': 'Health Care',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['hc_specimen', 'hc_substance'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/hc_res_specimen_definition_views.xml',
        'views/hc_res_specimen_definition_templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    'installable': 'True',
    'auto-install': 'True',
}
