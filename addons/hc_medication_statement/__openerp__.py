# -*- coding: utf-8 -*-
{
    'name': "Medication Statement",

    'summary': """
        Medication consumption (e.g., active medications)
        """,

    'description': """
        A record of a medication that is being consumed by a patient.

        **Scope and Usage**

        A MedicationStatement may indicate that the patient may be taking the medication now,
        or has taken the medication in the past or will be taking the medication in the future.
        The source of this information can be the patient, significant other (such as a family
        member or spouse), or a clinician.

        A common scenario where this information is captured is during the history taking process
        during a patient visit or stay. The medication information may come from e.g. the patient's memory,
        from a prescription bottle, or from a list of medications the patient, clinician or other party maintains.
    """,

    'author': "Luigi Sison",
    'website': "https://hl7-fhir.github.io/medicationstatement.html",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/openerp/addons/base/module/module_data.xml
    # for the full list
    'category': 'Health Care',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['hc_medication_request'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/hc_res_medication_statement_views.xml',
        'views/hc_res_medication_statement_templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    'installable': 'True',
    'auto-install': 'True',
}
