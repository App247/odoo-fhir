# -*- coding: utf-8 -*-
{
    'name': "Procedure",

    'summary': """
        Operation, counseling, or other health-related action
        """,

    'description': """
        An action that is or was performed on a patient. This can be a physical intervention like an operation, or less invasive like counseling or hypnotherapy.

        **Scope and Usage**

        This resource is used to record the details of procedures performed on a patient. A procedure is an activity that is performed with or on a patient as part of the provision of care. Examples include surgical procedures, diagnostic procedures, endoscopic procedures, biopsies, counseling, physiotherapy, exercise, etc. Procedures may be performed by a healthcare professional, a friend or relative or in some cases by the patient themselves.

        This resource provides summary information about the occurrence of the procedure and is not intended to provide real-time snapshots of a procedure as it unfolds, though for long-running procedures such as psychotherapy, it could represent summary level information about overall progress. The creation of a resource to support detailed real-time procedure information awaits the identification of a specific implementation use-case to share such information.
    """,

    'author': "Luigi Sison",
    'website': "https://hl7-fhir.github.io/procedure.html",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/openerp/addons/base/module/module_data.xml
    # for the full list
    'category': 'Health Care',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['hc_medication_administration'],

    # always loaded
	'data': [
        'security/ir.model.access.csv',
        'data/hc.vs.procedure.code.csv',
        # 'data/hc.vs.procedure.not.performed.reason.csv',
        'views/hc_res_procedure_views.xml',
        'views/hc_res_procedure_templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    'installable': 'True',
    'auto-install': 'True',
}