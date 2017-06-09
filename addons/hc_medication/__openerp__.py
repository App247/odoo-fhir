# -*- coding: utf-8 -*-
{
    'name': "Medication",

    'summary': """
        Medication and their ingredients, packaging
        """,

    'description': """
        This resource is primarily used for the identification and definition of a medication. It covers the ingredients and the packaging for a medication.

        **Scope and Usage**

        Representing medications in the majority of healthcare settings is a matter of identifying an item from a list and then conveying a reference for the item selected 
        either into a patient related resource or to other applications. Additional information about the medication is frequently provided for human verification, 
        but a full representation of the details of composition and efficacy of the medicine is conveyed by referring to drug dictionaries by means of the codes they define. 
        There are some occasions where it is necessary to identify slightly more detail, such as when dispensing a package containing a particular medicine requires identification 
        both of the medicine and the package at once. There are also some occasions (e.g. custom formulations) where the composition of a medicine must be represented. 
        In these cases the ingredients of the medicine have to be specified together with the amount contained, though the medication resource does not provide full details.
    """,

    'author': "Luigi Sison",
    'website': "https://hl7-fhir.github.io/medication.html",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/openerp/addons/base/module/module_data.xml
    # for the full list
    'category': 'Health Care',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['hc_substance', 'hc_organization'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/hc_res_medication_views.xml',
        'views/hc_res_medication_templates.xml',
        'data/hc.vs.medication.code.csv',
        'data/hc.vs.medication.form.code.csv',
        'data/hc.vs.medication.form.group.code.csv',
        'data/hc.vs.medication.ingredient.code.csv',
        'data/hc.vs.medication.package.form.code.csv',
    ],
    'css': [
        'static/src/css/hc_medication.css',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    'installable': 'True',
    'auto-install': 'True',
    }