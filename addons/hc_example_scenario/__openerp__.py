# -*- coding: utf-8 -*-
{
    'name': "Example Scenario",

    'summary': """
        Example of workflow instance""",

    'description': """
        Example of workflow instance
    """,

    'author': "Luigi Sison",
    'website': "https://hl7-fhir.github.io/examplescenario.htm",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/openerp/addons/base/module/module_data.xml
    # for the full list
    'category': 'Health Care',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['hc_base_metadata_type'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/hc_example_scenario_views.xml',
        'views/hc_example_scenario_templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    'installable': 'True',
    'auto-install': 'True',
}
