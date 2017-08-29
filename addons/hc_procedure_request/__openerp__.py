# -*- coding: utf-8 -*-
{
    'name': "Procedure Request",

    'summary': """
        Request, order, or plan for a care activity
        """,

    'description': """
        A request for a procedure to be performed. May be a proposal or an order.

        **Scope and Usage**

        A Procedure Request is a record of a request for a procedure to be performed.
        It can be used to represent a procedure that is planned, that is proposed, or that is ordered,
        as distinguished by the value of the ProcedureRequestStatus field.

        A procedure is an activity that is performed with or on a patient as part of the provision of care.
        Examples include surgical procedures, diagnostic procedures, endoscopic procedures, biopsies, counseling,
        physiotherapy, exercise, etc. Procedures may be performed by a healthcare professional, a friend or relative
        or in some cases by the patient themselves.

        The procedure request may represent an order that is entered by a practitioner in a CPOE system
        as well as a proposal made by a clinical decision support (CDS) system based on a patient's clinical record
        and context of care. Planned procedures referenced by a CarePlan may also be represented by this resource.
    """,

    'author': "Luigi Sison",
    'website': "https://hl7-fhir.github.io/procedurerequest.html",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/openerp/addons/base/module/module_data.xml
    # for the full list
    'category': 'Health Care',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['hc_document_reference', 'hc_plan_definition'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/hc_res_procedure_request_views.xml',
        'views/hc_res_procedure_request_templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    'installable': 'True',
    'auto-install': 'True',
}
