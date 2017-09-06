# -*- coding: utf-8 -*-
{
    'name': "Allergy Intolerance",

    'summary': """
        Allergy, Intolerance
    """,

    'description': """
        Risk of harmful or undesirable,
        physiological response which is unique to an individual
        and associated with exposure to a substance.

        **Scope and Usage**

        A record of a clinical assessment of an allergy or intolerance;
        a propensity, or a potential risk to an individual, to have an
        adverse reaction on future exposure to the specified substance,
        or class of substance.

        Where a propensity is identified, to record information or evidence
        about a reaction event that is characterized by any harmful or
        undesirable physiological response that is specific to the individual
        and triggered by exposure of an individual to the identified substance
        or class of substance.

        Substances include, but are not limited to: a therapeutic substance
        administered correctly at an appropriate dosage for the individual;
        food; material derived from plants or animals; or venom from insect stings.
    """,

    'author': "Luigi Sison",
    'website': "https://hl7-fhir.github.io/allergyintolerance.html",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/openerp/addons/base/module/module_data.xml
    # for the full list
    'category': 'Health Care',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['hc_patient','hc_substance'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/hc_res_allergy_intolerance_views.xml',
        'views/hc_res_allergy_intolerance_templates.xml',
        'data/hc.vs.allergy.intolerance.code.csv',
        'data/hc.vs.manifestation.code.csv',
        'report/hc_res_allergy_intolerance_report_views.xml',
        'report/hc_res_allergy_intolerance_report_templates.xml',
        'wizard/generate_xml_view.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    'installable': 'True',
    'auto-install': 'True',
}
