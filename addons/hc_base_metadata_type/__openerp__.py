# -*- coding: utf-8 -*-
{
    'name': "Metadata Type",

    'summary': """
        Complex data types for metadata
        """,

    'description': """

        * ContactDetail defines general contact details.
        * Contributor defines who contributes content.
        * DataRequirement defines a general data requirement for a knowledge asset such as a decision support rule or quality measure.
        * ParameterDefinition defines a parameter to a knowledge asset such as a decision support rule or quality measure.
        * RelatedArtifact structure defines resources related to a module such as previous and next versions of documents, documentation, citations, etc.
        * TriggerDefinition structure defines when a knowledge artifact is expected to be evaluated.
        * UsageContext structure defines the context of use for a module.
    """,

    'author': "Luigi Sison",
    'website': "https://hl7-fhir.github.io/metadatatypes.html",

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
        'views/hc_contact_detail_views.xml',
        'views/hc_contributor_views.xml',
        'views/hc_data_requirement_views.xml',
        'views/hc_parameter_definition_views.xml',
        'views/hc_related_artifact_views.xml',
        'views/hc_trigger_definition_views.xml',
        'views/hc_usage_context_views.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    'installable': 'True',
    'auto-install': 'False',
}
