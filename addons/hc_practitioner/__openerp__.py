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
        'data/hc.vs.practitioner.qualification.code.csv',
        'data/hc.vs.practitioner.specialty.csv',
        'examples/example_general.xml',
        'examples/example_person_pd.xml',
        'examples/example_f001.xml',
        'examples/example_f002.xml',
        'examples/example_f003.xml',
        'examples/example_f004.xml',
        'examples/example_f005.xml',
        'examples/example_f006.xml',
        'examples/example_f007.xml',
        'examples/example_f201.xml',
        'examples/example_f202.xml',
        'examples/example_f203.xml',
        'examples/example_f204.xml',
        'examples/example_xcda1.xml',

        'views/hc_practitioner_views.xml',
        'views/hc_practitioner_templates.xml',

    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    'installable': 'True',
    'auto-install': 'True',
}
