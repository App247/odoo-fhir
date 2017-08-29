# -*- coding: utf-8 -*-
{
    'name': "Task",

    'summary': """
        Activities
        """,

    'description': """
        A task to be performed.

        **Scope and Usage**

        An task resource describes an activity that can be performed, and tracks the state of completion of that activity.
        It is a representation that an activity should be or has been initiated, and eventually, represents the successful or unsuccessful completion of that activity.

        Note that there are a variety of processes associated with making and processing orders. Some orders may be handled immediately
        by automated systems but most require real world actions by one or more humans. Some orders can only be processed when other real world actions happen,
        such as a patient actually presenting themselves so that the action to be performed can actually be performed. Often these real world dependencies
        are only implicit in the order details.
    """,

    'author': "Luigi Sison",
    'website': "https://hl7-fhir.github.io/task.html",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/openerp/addons/base/module/module_data.xml
    # for the full list
    'category': 'Health Care',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['hc_group', 'hc_provenance', 'hc_encounter', 'hc_activity_definition'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/hc_res_task_views.xml',
        'views/hc_res_task_templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    'installable': 'True',
    'auto-install': 'True',
}
