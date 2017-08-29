# -*- coding: utf-8 -*-
{
    'name': "Imaging Study",

    'summary': """
        DICOM imaging study content
        """,

    'description': """
        Representation of the content produced in a DICOM imaging study. A study comprises a set of series,
        each of which includes a set of Service-Object Pair Instances (SOP Instances - images or other data) acquired or
        produced in a common context. A series is of only one modality (e.g. X-ray, CT, MR, ultrasound), but a study may have multiple series of different modalities.

        **Scope and Usage**

        ImagingStudy provides information on a DICOM imaging study, and the series and imaging objects in that study. It also provides information on how to retrieve that information (in a native DICOM format, or in a rendered format, such as JPEG). ImagingStudy is used to make available information about all parts of a single DICOM study.
    """,

    'author': "Luigi Sison",
    'website': "https://hl7-fhir.github.io/imagingstudy.html",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/openerp/addons/base/module/module_data.xml
    # for the full list
    'category': 'Health Care',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['hc_procedure_request','hc_care_plan'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/hc_res_imaging_study_views.xml',
        'views/hc_res_imaging_study_templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    'installable': 'True',
    'auto-install': 'True',
}
