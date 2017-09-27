# -*- coding: utf-8 -*-
{
    'name': "Person",

    'summary': """
        A person independent of a specific health-related context
    """,

    'description': """

        Demographics and administrative information about a person independent of a specific health-related context.

        **Scope and Usage**

        An individual has identity outside of a healthcare setting. The Person resource is used to capture
        this information and to relate the person as an individual to other resources that do have a health-related context.

        For example, while a patient resource may be created and maintained by each organization providing
        care for that person as a patient, a person resource provides a mechanism for linking patient resources
        across different organizations and their unique patient identity domains.
    """,

    'author': "HL7 FHIR",
    'website': "https://hl7-fhir.github.io/person.html",
    'contributors': "Luigi Sison",
    'maintainer': "Luigi Sison",
    'license': "GPL-3",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/openerp/addons/base/module/module_data.xml
    # for the full list
    'category': 'Health Care',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['hc_base'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'security/hc_person_security.xml',
        'views/hc_res_person_views.xml',
        'views/hc_res_person_templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
        'demo/demo_patient.xml',
    ],
    'installable': 'True',
    # 'auto-install': 'True',
}
