# -*- coding: utf-8 -*-
{
    'name': "Search Parameter",

    'summary': """
        Search or Filter Item
        """,

    'description': """
        A search parameter that defines a named search item that can be used to search/filter on a resource.

    **Scope and Usage**

    A SearchParameter resource specifies a search parameter that may be used on the RESTful API to search or filter on a resource. The SearchParameter resource declares:

    * how to refer to the search parameter from a client
    * how the search parameter is to be understood by the server
    * where in the source resource the parameter matches
    """,

    'author': "Luigi Sison",
    'website': "https://hl7-fhir.github.io/searchparameter.html",

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
        'views/hc_res_search_parameter_views.xml',
        'views/hc_res_search_parameter_templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    'installable': 'True',
    'auto-install': 'True',
}
