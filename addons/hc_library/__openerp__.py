# -*- coding: utf-8 -*-
{
    'name': "Library",

    'summary': """
        Knowledge asset definitions like XML schemas and CQL clinical logic
        """,

    'description': """
        The Library resource is a general-purpose container for knowledge asset definitions. It can be used to describe and expose exist knowledge assets such as
        logic libraries and information model descriptions, as well as to describe a collection of knowledge assets.

        **Scope and Usage**

        The Library resource is a general purpose container for clinical knowledge that is defined using a non-FHIR representation.
        For example, a shareable library of clinical logic, written in Clinical Quality Language (CQL), or the XML Schema for an information model.
        In addition to representing the metadata of the library, the resource has elements for tracking dependencies, as well as for representing
        the parameters and data requirements for any expression functionality provided by the library.

        The actual content of the library is represented using the Attachment data type, and may either be referenced with a url, or the content
        may be embedded as a base-64 encoded string. Either way, the contentType element of the attachment is used to indicate the representation of the library content.

        Note that because the library content may be embedded as well as be retrievable from an external repository via the attachment URL, the possibility
        exists for the embedded content to be different from the content on the repository. With proper versioning and governance, this should never occur,
        but to minimize the potential impact of this possibility, implementers SHALL give precedence to the embedded content of a library when it is present.
    """,

    'author': "Luigi Sison",
    'website': "https://hl7-fhir.github.io/library.html",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/openerp/addons/base/module/module_data.xml
    # for the full list
    'category': 'Health Care',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['hc_base_metadata_type'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/hc_res_library_views.xml',
        'views/hc_res_library_templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    'installable': 'True',
    'auto-install': 'True',
}
