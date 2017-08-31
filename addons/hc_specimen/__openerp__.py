# -*- coding: utf-8 -*-
{
    'name': "Specimen",

    'summary': """
        Biological or physical material samples
        """,

    'description': """
        A sample to be used for analysis.

        **Scope and Usage**

        Any material sample:

        * taken from a biological entity, living or dead
        * taken from a physical object or the environment

        Some specimens are biological and can contain one or more components including but not limited to cellular molecules, cells, tissues, organs, body fluids, embryos, and body excretory products (source: NCI Thesaurus , modified).
    """,

    'author': "Luigi Sison",
    'website': "https://hl7-fhir.github.io/specimen.html",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/openerp/addons/base/module/module_data.xml
    # for the full list
    'category': 'Health Care',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['hc_procedure_request'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/hc_res_specimen_views.xml',
        'views/hc_res_specimen_templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    'installable': 'True',
    'auto-install': 'True',
    }
