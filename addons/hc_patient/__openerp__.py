# -*- coding: utf-8 -*-
{
    'name': "Patient",

    'summary': """
        Person or animal receiving health-related services
        """,

    'description': """
        Demographics and other administrative information about an individual or animal receiving care or other health-related services.

        **Scope and Usage**

        This Resource covers data about patients and animals involved in a wide range of health-related activities, including:

        * Curative activities
        * Psychiatric care
        * Social services
        * Pregnancy care
        * Nursing and assisted living
        * Dietary services
        * Tracking of personal health and exercise data

        The data in the Resource covers the "who" information about the patient: its attributes are focused on the demographic information necessary
        to support the administrative, financial and logistic procedures. A Patient record is generally created and maintained by each organization providing care for a patient.
        A patient or animal receiving care at multiple organizations may therefore have its information present in multiple Patient Resources.
            """,

    'author': "Luigi Sison",
    'website': "https://hl7-fhir.github.io/patient.html",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/openerp/addons/base/module/module_data.xml
    # for the full list
    'category': 'Health Care',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['hc_practitioner', 'hc_related_person'],


    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'data/data_patient.xml',
        'data/hc.vs.animal.species.csv',
        'data/hc.vs.animal.breed.csv',
        'data/hc.vs.v3.race.value.set.csv',
        'data/hc.vs.v3.race.csv',
        'data/hc.vs.v3.religious.affiliation.csv',
        # 'data/hc.vs.v2.contact.role.csv',
        'examples/example.xml',
        'examples/example_cypress.xml',
        'examples/example_pat1_2.xml',
        'examples/example_pat3.xml',
        'examples/example_pat4.xml',
        'examples/example_stock_persons.xml',
        # 'examples/example_xcda.xml',
        # 'views/hc_marital_status_views.xml',
        'views/hc_res_patient_views.xml',
        'views/hc_res_patient_templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo_example.xml',
    ],
    'installable': 'True',
    'auto-install': 'True',
}
