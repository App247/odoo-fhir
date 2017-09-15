# -*- coding: utf-8 -*-
{
    'name': "Code System",

    'summary': """
        Enumerations, terminologies, classifications, ontologies and other sets of codes with meaning
        """,

    'description': """
        A code system resource specifies a set of codes drawn from one or more code systems.

        **Scope and Usage**

        The FHIR terminology specification is based two key concepts, originally defined in HL7 v3 Core Principles :

        * code system - defines a set of codes with meanings (also known as enumeration, terminology, classification, and/or ontology)
        * value set - selects a set of codes from those defined by one or more code systems

        Code systems define which codes (symbols and/or expressions) exist, and how they are understood.
        Value Sets select a set of codes from one or more code systems to specify which codes can be used in a particular context.

        The CodeSystem resource is used to declare the existence of a code system, and it's key properties:

        * Identifying URL and version
        * Description, Copyright, publication date, and other metadata
        * Some key properties of the code system itself - whether it's case sensitive, version safe, and whether it defines a compositional grammar
        * What filters can be used in value sets that use the code system in a ValueSet.compose element
        * What properties the concepts defined by the code system

        In addition, the CodeSystem resource may list some or all of the concepts in the code system, along with their basic properties (code, display, definition),
        designations, and additional properties.

        The CodeSystem resource is not intended to support the process of maintaining a code system.
        Instead, the focus is on publishing the properties and optionally the content of a code system for use throughout the FHIR eco-system,
        such as to support value set expansion and validation. Note that the important existing (large) code systems
        (SNOMED CT, LOINC, RxNorm, ICD family, etc) all have their own distribution formats, and there is no intent that the CodeSystem resource be used for
        distributing these kind of terminologies. Instead, it is intended to be used for distributing the smaller ad-hoc code systems that are ubiqutiously encountered
        through out the healthcare process.
    """,

    'author': "Luigi Sison",
    'website': "https://hl7-fhir.github.io/codesystem.html",

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
        'views/hc_res_code_system_views.xml',
        'views/hc_res_code_system_templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    'installable': 'True',
    'auto-install': 'True',
}
