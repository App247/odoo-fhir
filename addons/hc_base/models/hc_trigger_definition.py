# -*- coding: utf-8 -*-

from openerp import models, fields, api

class TriggerDefinition(models.Model):
    _name = "hc.trigger.definition"
    _description = "Trigger Definition"
    _inherit = ["hc.element"]            

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
    event_name = fields.Char(
        string="Event Name",
        help="Name of the event.")
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
    event_data_id = fields.Many2one(
        comodel_name="hc.trigger.definition.event.data",
        string="Event Data",
        help="Triggering data of the event.")

class TriggerDefinitionEventTiming(models.Model):
    _name = "hc.trigger.definition.event.timing"
    _description = "Trigger Definition Event Timing"
    _inherit = ["hc.basic.association", "hc.timing"]

class TriggerDefinitionEventData(models.Model):
    _name = "hc.trigger.definition.event.data"
    _description = "Trigger Definition Event Data"
    _inherit = ["hc.basic.association", "hc.data.requirement"]
