# -*- coding: utf-8 -*-
{
    'name': "Structure Map",

    'summary': """
        Data transformation map
        """,

    'description': """
        A Map of relationships between 2 structures that can be used to transform data.

        The StructureMap resource defines a detailed set of of rules that describe how one Structure is related to another, and provides sufficient detail to
        allow for automated conversion of instances.
    """,

    'author': "Luigi Sison",
    'website': "https://hl7-fhir.github.io/structuremap.html",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/openerp/addons/base/module/module_data.xml
    # for the full list
    'category': 'Health Care',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['hc_base_metadata_type'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/hc_res_structure_map_views.xml',
        'views/hc_res_structure_map_templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    'installable': 'True',
    'auto-install': 'True',
}
