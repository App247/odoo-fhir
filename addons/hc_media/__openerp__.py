# -*- coding: utf-8 -*-
{
    'name': "Media",

    'summary': """
        Photo, video, audio recording
        """,

    'description': """
        A photo, video, or audio recording acquired or used in healthcare. The actual content may be inline or provided by direct reference.

        **Scope and Usage**

        The Media resource contains photos, videos, and audio recordings. It is used with media acquired or used as part of the healthcare process. Here are some typical usages:

        * Photos of patients and staff for identification purposes
        * Photos and videos of diagnostic or care provision procedures for recording purposes
        * Storing scans and faxes of paper documents where not enough metadata exists to create a DocumentReference
        * Images on diagnostic reports
    """,

    'author': "Luigi Sison",
    'website': "https://hl7-fhir.github.io/media.html",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/openerp/addons/base/module/module_data.xml
    # for the full list
    'category': 'Health Care',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['hc_specimen', 'hc_device_metric'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/hc_res_media_views.xml',
        'views/hc_res_media_templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    'installable': 'True',
    'auto-install': 'True',
}
