# -*- coding: utf-8 -*-
{
    'name': "Health Care Base",

    'summary': """
        Module needed by other Health Care modules.""",

    'description': """
        Contains: FHIR Complex Types, common definitions and data sets

        **Data Types**

        The FHIR specification defines a set of data types that are used for the resource elements. There are four categories of data types:

        * Simple / primitive types, which are single elements with a primitive value. Examples: string, boolean, dateTime, integer and decimal. Simple/primitive types do not have any models because they have equivalent types in Odoo.
        * General purpose complex types, which are re-usable clusters of elements. Examples: Address, Identity, HumanName.
        * Complex data types for metadata. Examples: AvailableTime, ContactDetail, Contributor, RelatedArtifact, UsageContext.
        * Special purpose data types: Reference, Narrative, Extension, Meta, and Dosage.

        This module defines the last 3 categories.

        **Data Sets**

        This module contains data sets which are used by several other models. Examples: Body Site, Route of Administration, Substance.
    """,

    'author': "FHIR® and Luigi Sison",
    'website': "https://hl7-fhir.github.io/datatypes.html",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/openerp/addons/base/module/module_data.xml
    # for the full list
    'category': 'Health Care',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'product', 'mail'],

    # always loaded
    'data': [
        'security/hc_base_security.xml',
        'security/ir.model.access.csv',

        'data/data_partner_category.xml',
        'data/data_source.xml',
        'data/data_act_code.xml',
        'data/data_act_code_observation.xml',
        'data/data_base.xml',
        'data/data_base_v3.xml',
        'data/data_country.xml',
        'data/data_identifier_type.xml',
        'data/data_language.xml',
        'data/data_timing.xml',
        'data/data_uom_basic.xml',
        # 'data/data_uom_advanced.xml',
        'data/data_value_set.xml',
        'data/hc.human.name.suffix.csv',
        'data/data_participation_type.xml',
        'data/hc.vs.additional.instruction.code.csv',
        'data/hc.vs.body.site.csv',
        'data/hc.vs.c80.practice.code.csv',
        'data/hc.vs.defined.type.csv',
        'data/hc.vs.encounter.reason.csv',
        'data/hc.vs.mime.type.csv',
        'data/hc.vs.participant.role.csv',
        'data/hc.vs.resource.type.csv',
        'data/data_partner_title.xml',
        'data/hc.vs.route.code.csv',
        # 'data/l10n_au/country_pl.xml',
        # 'data/l10n_ph/country_pl.xml',
        'data/l10n_us/country_pl.xml',
        'data/l10n_us/res.country.state.csv',
        'data/l10n_us/hc.vs.country.city.type.csv',
        'data/l10n_us/res.country.state.csv',
        'data/l10n_us/hc.vs.country.city.type.csv',

        'views/hc_menu_views.xml',
        'views/hc_value_set_views.xml',
        'views/hc_act_code_views.xml',
        'views/hc_telecom_views.xml',
        'views/hc_address_views.xml',
        'views/hc_annotation_views.xml',
        'views/hc_attachment_views.xml',
        'views/hc_codeable_concept_views.xml',
        'views/hc_coding_views.xml',
        'views/hc_human_name_views.xml',
        'views/hc_identifier_views.xml',
        'views/hc_language_views.xml',
        'views/hc_meta_views.xml',
        'views/hc_narrative_views.xml',
        'views/hc_odoo_partner_views.xml',
        'views/hc_participation_type_views.xml',
        'views/hc_reference_views.xml',
        'views/hc_resource_views.xml',
        'views/hc_resource_type_views.xml',
        'views/hc_domain_resource_views.xml',
        'views/hc_element_definition_views.xml',
        'views/hc_defined_type_views.xml',
        'views/hc_timing_views.xml',
        'views/hc_route_code_views.xml',
        'views/hc_uom_views.xml',
        'views/hc_value_set_v3_views.xml',
        'views/templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
        # 'demo/hc.vs.country.city.csv',
        'demo/hc.human.name.term.csv',
        'demo/hc.human.name.csv',
        # 'demo/hc.res.person.csv',
    ],
}
