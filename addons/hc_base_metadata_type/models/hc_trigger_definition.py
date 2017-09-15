# -*- coding: utf-8 -*-

from openerp import models, fields, api

class TriggerDefinition(models.Model):
    _name = "hc.trigger.definition"
    _description = "Trigger Definition"
    _inherit = ["hc.element"]
    _rec_name = "name"

    type = fields.Selection(
        string="Type",
        required="True",
        selection=[
            ("named-event", "Named-Event"),
            ("periodic", "Periodic"),
            ("data-added", "Data-Added"),
            ("data-modified", "Data-Modified"),
            ("data-removed", "Data-Removed"),
            ("data-accessed", "Data-Accessed"),
            ("data-access-ended", "Data-Access-Ended")],
        help="The type of triggering event.")
    name = fields.Char(
        string="Name",
        help="Name or URI that identifies the event.")
    event_timing_type = fields.Selection(
        string="Event Timing Type",
        selection=[
            ("Timing", "Timing"),
            ("Schedule", "Schedule"),
            ("date", "Date"),
            ("dateTime", "Datetime")],
        help="Type of timing of the event.")
    event_timing_name = fields.Char(
        string="Event Timing",
        compute="_compute_event_timing_name",
        store="True",
        help="Timing of the event.")
    event_timing_id = fields.Many2one(
        comodel_name="hc.trigger.definition.event.timing",
        string="Event Timing",
        help="Timing of the event.")
    # event_timing_schedule_id = fields.Many2one(
    #     comodel_name="hc.res.schedule",
    #     string="Event Timing Schedule",
    #     help="Schedule timing of the event.")
    event_timing_date = fields.Date(
        string="Event Timing Date",
        help="Date timing of the event.")
    event_timing_datetime = fields.Datetime(
        string="Event Timing Datetime",
        help="Datetime timing of the event.")
    data_id = fields.Many2one(
        comodel_name="hc.trigger.definition.data",
        string="Data",
        help="Triggering data of the event.")
    condition_id = fields.Many2one(
        comodel_name="hc.trigger.definition.condition",
        string="Condition",
        help="Whether the event triggers.")

class TriggerDefinitionEventTiming(models.Model):
    _name = "hc.trigger.definition.event.timing"
    _description = "Trigger Definition Event Timing"
    _inherit = ["hc.basic.association", "hc.timing"]

class TriggerDefinitionData(models.Model):
    _name = "hc.trigger.definition.data"
    _description = "Trigger Definition Data"
    _inherit = ["hc.basic.association", "hc.data.requirement"]

    trigger_definition_id = fields.Many2one(
        comodel_name="hc.trigger.definition",
        string="Trigger Definition",
        help="Trigger Definition associated with this Trigger Definition Data.")

class TriggerDefinitionCondition(models.Model):
    _name = "hc.trigger.definition.condition"
    _description = "Trigger Definition Condition"

    trigger_definition_id = fields.Many2one(
        comodel_name="hc.trigger.definition",
        string="Trigger Definition",
        help="Trigger Definition associated with this Trigger Definition Condition.")
    name = fields.Char(
        string="Name",
        required="True",
        help="Human-readable label for this trigger definition condition.")
    description = fields.Text(
        string="Description",
        help="Natural language description of the condition.")
    language = fields.Selection(
        string="Language",
        required="True",
        selection=[
            ("text/cql", "Text/CQL"),
            ("text/fhirpath", "Text/FHIRPath")],
        help="The media type of the language for the expression.")
    expression = fields.Text(
        string="Exression",
        required="True",
        help="Boolean-valued expression.")
