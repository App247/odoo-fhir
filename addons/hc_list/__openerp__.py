# -*- coding: utf-8 -*-
{
    'name': "List",

    'summary': """
        Collection of records like Problem List
        """,

    'description': """
        A set of information summarized from a list of other resources.

        **Scope and Usage**

        The List resource is a flat, possibly ordered, collection of records. List resources are used in many places, including allergies, medications, alerts,
        family history, medical history, etc. List resources can be used to support patient-specific clinical lists as well as lists that manage workflows
        such as tracking patients, managing teaching cases, etc. Resources supported by the List resource can be homogenous – consisting of only one type of resource
        (e.g., allergy list); as well as heterogeneous – containing a variety of resources (e.g., a problem list including Conditions, AllergyIntolerances, recent Procedures, etc.).

        Lists will typically include references to the resources that make up the list, however in some cases the details of the content of the list might be expressed
        in narrative only; e.g., a text record of a family history. The List resource is only needed if there is a need to filter the set of resources by a mechanism that
        cannot be accomplished via a simple query; i.e. there is no need to have a list for all AllergyIntolerances that exist on a server for a given patient.
        However, List is an appropriate mechanism to provide a filtered list of the subset of AllergyIntolerances that are deemed to be "current".
        Lists are allowed to contain other lists, so that there is a nested collection of lists.
    """,

    'author': "Luigi Sison",
    'website': "https://hl7-fhir.github.io/list.html",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/openerp/addons/base/module/module_data.xml
    # for the full list
    'category': 'Health Care',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['hc_allergy_intolerance', 'hc_family_member_history', 'hc_procedure'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'data/data_list.xml',
        'views/hc_res_list_views.xml',
        'views/hc_res_list_templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    'installable': 'True',
    'auto-install': 'True',
}
