# -*- coding: utf-8 -*-
{
    'name': "Organization",

    'summary': """
        Companies, institutions, corporations, departments, community groups, healthcare practice groups, etc.
    """,

    'description': """
         A formally or informally recognized grouping of people or organizations formed for the purpose of achieving some form of collective action. Includes companies, institutions, corporations, departments, community groups, healthcare practice groups, etc.

        **Scope and Usage**

        This resource may be used in a shared registry of contact and other information for various organizations or it can be used merely as a support
        for other resources that need to reference organizations, perhaps as a document, message or as a contained resource.

        If using a registry approach, it's entirely possible for multiple registries to exist, each dealing with different types or levels of organization.
    """,

    'author': "Luigi Sison",
    'website': "https://hl7-fhir.github.io/organization.html",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/openerp/addons/base/module/module_data.xml
    # for the full list
    'category': 'Health Care',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['hc_person'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'data/data_organization.xml',
        'data/hc.vs.organization.type.csv',

        'examples/example_2.xml',
        'examples/example_hl7.xml',
        'examples/example_f001.xml',
        'examples/example_f002.xml',
        'examples/example_f003.xml',
        'examples/example_f201.xml',
        'examples/example_f203.xml',
        'examples/example_gastro.xml',
        'examples/example_good_health_care.xml',
        'examples/example_lab.xml',
        'examples/example_mihealth.xml',
        'examples/example_mmanu.xml',
        'examples/example_pp.xml',
        'examples/example_pd.xml',

        'views/hc_res_organization_views.xml',
        'views/hc_res_organization_templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    'installable': 'True',
    'auto-install': 'True',
}
