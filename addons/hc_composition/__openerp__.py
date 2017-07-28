# -*- coding: utf-8 -*-
{
    'name': "Composition",

    'summary': """
        A logical document (container) of a set of healthcare-related information
        """,

    'description': """
        A set of healthcare-related information that is assembled together into a single logical document that provides a single coherent statement of meaning,
        establishes its own context and that has clinical attestation with regard to who is making the statement. While a Composition defines the structure,
        it does not actually contain the content: rather the full content of a document is contained in a Bundle, of which the Composition is the first resource contained.

        **Scope and Usage**

        A Composition is also the basic structure from which FHIR Documents - immutable bundles with attested narrative - are built.
        A single logical composition may be associated with a series of derived documents, each of which is a frozen copy of the composition.

        Note: EN 13606 (http://www.en13606.org/) uses the term "Composition" to refer to a single commit to an EHR system, and offers some common examples:
        a composition containing a consultation note, a progress note, a report or a letter, an investigation report,
        a prescription form or a set of bedside nursing observations. Using Composition for an attested EHR commit is a valid uses of the Composition resource,
        but for FHIR purposes, it would be usual to make more granular updates with individual provenance statements.
    """,

    'author': "Luigi Sison",
    'website': "https://hl7-fhir.github.io/composition.html",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/openerp/addons/base/module/module_data.xml
    # for the full list
    'category': 'Health Care',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['hc_list',"hc_diagnostic_report"],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'data/data_composition.xml',
        'data/hc.vs.doc.class.code.csv',
        'data/hc.vs.doc.type.code.csv',
        'data/hc.vs.doc.section.code.csv',
        'views/hc_res_composition_views.xml',
        'views/hc_res_composition_templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    'installable': 'True',
    'auto-install': 'True',
}
