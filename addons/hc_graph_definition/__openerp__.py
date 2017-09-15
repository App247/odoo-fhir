# -*- coding: utf-8 -*-
{
    'name': "Graph Definition",

    'summary': """
        Graph of resources
        """,

    'description': """
    A formal computable definition of a graph of resources - that is, a coherent set of resources that form a graph by following references.
    The Graph Definition resource defines a set and makes rules about the set.

    **Scope and Usage**

    The GraphDefinition resource provides a formal computable definition of a graph of resources - that is, a coherent set of resources that form a graph by following references.
    The Graph Definition resource defines a set and makes rules about the set. The GraphDefinition resource can be used to:

    * Summarize a set of profiles on resources
    * Define a graph of resources to return in a query
    * Define a graph of resources to include in a document
    * Document rules about the relationship between a set of resources e.g. must all resources concern the same patient?
    """,

    'author': "Luigi Sison",
    'website': "https://hl7-fhir.github.io/graph_definition.html",

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
        'views/hc_res_graph_definition_views.xml',
        'views/hc_res_graph_definition_templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    'installable': 'True',
    'auto-install': 'True',
}
