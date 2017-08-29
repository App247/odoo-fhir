# -*- coding: utf-8 -*-
{
    'name': "Device Use Statement",

    'summary': """
        Report on device use
        """,

    'description': """
        A record of a device being used by a patient where the record is the result of a report from the patient or another clinician.

        **Scope and Usage**

        This resource records the use of a healthcare-related device by a patient. The record is the result of a report of use by the
        patient or another provider. The resource can be used to note the use of an assistive device such as a wheelchair or hearing aid,
        a contraceptive such an intra-uterine device, or other implanted devices such as a pacemaker.
    """,

    'author': "Luigi Sison",
    'website': "https://hl7-fhir.github.io/deviceusestatement.html",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/openerp/addons/base/module/module_data.xml
    # for the full list
    'category': 'Health Care',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['hc_group'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/hc_res_device_use_statement_views.xml',
        'views/hc_res_device_use_statement_templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    'installable': 'True',
    'auto-install': 'True',
}
