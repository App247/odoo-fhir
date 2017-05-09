# -*- coding: utf-8 -*-
{
    'name': "Substance",

    'summary': """
        Ingredients of a medication
        """,

    'description': """
        A homogeneous material with a definite composition.

        **Scope and Usage**

        This resource allows for a material to be represented. The resource can be used 
        to represent either a kind of a substance - e.g. a formulation commonly used for 
        treating patients, or it can be used to describe a particular package of a known substance 
        (e.g. bottle, jar, packet).
    """,

    'author': "Luigi Sison",
    'website': "https://hl7-fhir.github.io/substance.html",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/openerp/addons/base/module/module_data.xml
    # for the full list
    'category': 'Health Care',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['hc_base'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'data/data_substance.xml',
        # 'data/hc.vs.substance.code.csv',
        # 'data/hc.parent.substance.code.csv',
        # 'data/hc.child.parent.substance.code.csv',
        'views/hc_res_substance_views.xml',
        'views/hc_res_substance_templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    'installable': 'True',
    'auto-install': 'True',
}