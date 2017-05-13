# -*- coding: utf-8 -*-
{
    'name': "Medication Dispense",

    'summary': """
        Supply of medication
        """,

    'description': """
        Indicates that a medication product is to be or has been dispensed for a named person/patient. 
        This includes a description of the medication product (supply) provided and the instructions 
        for administering the medication. The medication dispense is the result of a pharmacy system 
        responding to a medication order.

        **Scope and Usage**
         
        This resource covers the supply of medications to a patient. Examples include dispensing and 
        pick-up from an out-patient or community pharmacy, dispensing patient-specific medications 
        from in-patient pharmacy to ward, as well as issuing a single dose from ward stock to a 
        patient for consumption. The medication dispense is the result of a pharmacy system responding 
        to a medication order.

    """,

    'author': "Luigi Sison",
    'website': "https://hl7-fhir.github.io/medicationdispense.html",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/openerp/addons/base/module/module_data.xml
    # for the full list
    'category': 'Health Care',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['hc_detected_issue', 'hc_procedure'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/hc_res_medication_dispense_views.xml',
        'views/hc_res_medication_dispense_templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    'installable': 'True',
    'auto-install': 'True',
}