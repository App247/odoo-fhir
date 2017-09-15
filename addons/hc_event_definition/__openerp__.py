# -*- coding: utf-8 -*-
{
    'name': "Event Definition",

    'summary': """
        Event description""",

    'description': """
        The EventDefinition resource provides a reusable description of when a particular event can occur.

        **Scope and Usage**

        This resource is a definition resource from a FHIR workflow perspective - see Workflow, specifically Definition.

        The EventDefinition provides a reusable description of an event. The resource supports describing different kinds of events,
        including named events, periodic events, and data-based events. For each of these, the resource also supports a formal description of the event.
        For example, a 'monitor-emergency-admissions' event can be a named event, but also provide a formal description of the event as monitoring for encounters
        that occur in emergency department locations.
    """,

    'author': "Luigi Sison",
    'website': "https://hl7-fhir.github.io/event_definition.html",

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
        'views/hc_res_event_definition_views.xml',
        'views/hc_res_event_definition_templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    'installable': 'True',
    'auto-install': 'True',
}
