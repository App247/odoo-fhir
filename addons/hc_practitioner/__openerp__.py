# -*- coding: utf-8 -*-
{
    'name': "Practitioner",

    'summary': """
        Physician, nurse, allied health professional, administrative personnnel, service animal, etc.
    """,

    'description': """
        A person or animal who is directly or indirectly involved in the provisioning of healthcare.

        **Scope and Usage**

        Practitioner covers all individuals who are engaged in the healthcare process and healthcare-related services as part of their formal responsibilities and this Resource is used for attribution of activities and responsibilities to these individuals. Practitioners include (but are not limited to):

        * physicians, dentists, pharmacists
        * physician assistants, nurses, scribes
        * midwives, dietitians, therapists, optometrists, paramedics
        * medical technicians, laboratory scientists, prosthetic technicians, radiographers
        * social workers, professional home carers, official volunteers
        * receptionists handling patient registration
        * IT personnel merging or unmerging patient records
        * Service animal (e.g., ward assigned dog capable of detecting cancer in patients)
    """,

    'author': "Luigi Sison",
    'website': "https://hl7-fhir.github.io/practitioner.html",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/openerp/addons/base/module/module_data.xml
    # for the full list
    'category': 'Health Care',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['hc_healthcare_service'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/hc_practitioner_views.xml',
        'views/hc_practitioner_templates.xml',
        'data/hc.vs.practitioner.qualification.csv',
        'data/hc.vs.practitioner.specialty.csv',
        'examples/example_general.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    'installable': 'True',
    'auto-install': 'True',
}
