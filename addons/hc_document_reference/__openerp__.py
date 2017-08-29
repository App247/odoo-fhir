# -*- coding: utf-8 -*-
{
    'name': "Document Reference",

    'summary': """
        Reference to a document
        """,

    'description': """
        A reference to a document.

        **Scope and Usage**

        A DocumentReference resource is used to describe a document that is made available to a healthcare system. A document is some sequence of bytes
        that is identifiable, establishes its own context (e.g., what subject, author, etc. can be displayed to the user), and has defined update management.
        The DocumentReference resource can be used with any document format that has a recognized mime type and that conforms to this definition.

        Typically, DocumentReference resources are used in document indexing systems, such as IHE XDS  (see the XDS specific profile), and are used to refer to:

        * CDA  documents in FHIR systems
        * FHIR documents stored elsewhere (i.e. registry/repository following the XDS model)
        * PDF documents , and even digital records of faxes where sufficient information is available
        * Other kinds of documents, such as records of prescriptions
    """,

    'author': "Luigi Sison",
    'website': "https://hl7-fhir.github.io/documentreference.html",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/openerp/addons/base/module/module_data.xml
    # for the full list
    'category': 'Health Care',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['hc_encounter'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/hc_res_document_reference_views.xml',
        'views/hc_res_document_reference_templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    'installable': 'True',
    'auto-install': 'True',
}
