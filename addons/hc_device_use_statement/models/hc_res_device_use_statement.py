# -*- coding: utf-8 -*-

from openerp import models, fields, api

class DeviceUseStatement(models.Model):
    _name = "hc.res.device.use.statement"
    _description = "Device Use Statement"

    identifier_ids = fields.One2many(
        comodel_name="hc.device.use.statement.identifier",
        inverse_name="device_use_statement_id",
        string="Identifiers",
        help="Period when used.")
    status = fields.Selection(
        string="Status",
        selection=[
            ("active", "Active"),
            ("completed", "Completed"),
            ("entered-in-error", "Entered-In-Error")],
        default="active",
        help="A code representing the patient or other source's judgment about the state of the device used that this statement is about. Generally this will be active or completed.")
    subject_type = fields.Selection(
        string="Subject Type",
        selection=[
            ("patient", "Patient"),
            ("group", "Group")],
        help="Type of patient using device.")
    subject_name = fields.Char(
        string="Subject",
        compute="_compute_subject_name",
        help="Patient using device.")
    subject_patient_id = fields.Many2one(
        comodel_name="hc.res.patient",
        string="Subject Patient",
        help="Patient using device.")
    subject_group_id = fields.Many2one(
        comodel_name="hc.res.group",
        string="Subject Group",
        help="Group using device.")
    when_used_start_date = fields.Datetime(
        string="When Used Start Date",
        help="Start of the period when used.")
    when_used_end_date = fields.Datetime(
        string="When Used End Date",
        help="End of the period when used.")
    timing_type = fields.Selection(
        string="Timing Type",
        selection=[
            ("timing", "Timing"),
            ("period", "Period"),
            ("date_time", "Date Time")],
        help="Type of how often the device was used.")
    timing_name = fields.Char(
        string="Timing",
        compute="_compute_timing_name",
        store="True",
        help="How often the device was used.")
    timing_id = fields.Many2one(
        comodel_name="hc.device.use.statement.timing",
        string="Timing",
        help="Timing the patient used the device.")
    timing_start_date = fields.Datetime(
        string="Scheduled Start Date",
        help="Start of the period when the patient used the device.")
    timing_end_date = fields.Datetime(
        string="Scheduled End Date",
        help="End of the period when the patient used the device.")
    timing_date_time = fields.Datetime(
        string="Timing Date",
        help="Datetime the patient used the device.")
    recorded_on = fields.Datetime(
        string="Recorded On",
        help="When statement was recorded.")
    source_type = fields.Selection(
        string="source Type",
        selection=[
            ("patient", "Patient"),
            ("practitioner", "Practitioner"),
            ("related_person", "Related Person")],
        help="Type of patient using device.")
    source_name = fields.Char(
        string="source",
        compute="_compute_source_name",
        help="Patient using device.")
    source_patient_id = fields.Many2one(
        comodel_name="hc.res.patient",
        string="Source Patient",
        help="Patient using device.")
    source_practitioner_id = fields.Many2one(
        comodel_name="hc.res.practitioner",
        string="Source Practitioner",
        help="Practitioner using device.")
    source_related_person_id = fields.Many2one(
        comodel_name="hc.res.related.person",
        string="Source Related Person",
        help="Related Person using device.")
    device_id = fields.Many2one(
        comodel_name="hc.res.device",
        string="Device",
        required="True",
        help="Period when used.")
    indication_ids = fields.Many2many(
        comodel_name="hc.vs.act.reason",
        string="Indications",
        help="Reason or justification for the use of the device.")
    body_site_id = fields.Many2one(
        comodel_name="hc.vs.body.site",
        string="Body Site",
        help="Target body site.")
    note_ids = fields.One2many(
        comodel_name="hc.device.use.statement.note",
        inverse_name="device_use_statement_id",
        string="Notes",
        help="Details about the device statement that were not represented at all or sufficiently in one of the attributes provided in a class. These may include for example a comment, an instruction, or a note associated with the statement.")

class DeviceUseStatementIdentifier(models.Model):
    _name = "hc.device.use.statement.identifier"
    _description = "Device Use Statement Identifier"
    _inherit = ["hc.basic.association", "hc.identifier"]

    device_use_statement_id = fields.Many2one(
        comodel_name="hc.res.device.use.statement",
        string="Device Use Statement",
        help="Device Use Statement associated with this Device Use Statement Identifier.")

class DeviceUseStatementNote(models.Model):
    _name = "hc.device.use.statement.note"
    _description = "Device Use Statement Note"
    _inherit = ["hc.basic.association", "hc.annotation"]

    device_use_statement_id = fields.Many2one(
        comodel_name="hc.res.device.use.statement",
        string="Device Use Statement",
        help="Device Use Statement associated with this Device Use Statement Note.")

class DeviceUseStatementTiming(models.Model):
    _name = "hc.device.use.statement.timing"
    _description = "Device Use Statement Timing"
    _inherit = ["hc.basic.association", "hc.timing"]
