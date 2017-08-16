# -*- coding: utf-8 -*-
{
    'name': "Catalog Entry",

    'summary': """
        Catalog item definitions
        """,

    'description': """
        Catalog entries are wrappers that contextualize items included in a catalog.

        **Scope and Usage**

        This resource is an administrative resource for using definitional resources in the scope of a catalog.
        This resource contains additional information about each catalog entry, in the scope of a specific catalog, such as attributes and relations to other entries.
    """,

    'author': "Luigi Sison",
    'website': "https://hl7-fhir.github.io/catalogentry.html",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/openerp/addons/base/module/module_data.xml
    # for the full list
    'category': 'Health Care',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['hc_care_plan', 'hc_procedure', 'hc_service_definition'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/hc_res_catalog_entry_views.xml',
        'views/hc_res_catalog_entry_templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    'installable': 'True',
    'auto-install': 'True',
}
