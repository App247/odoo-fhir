# -*- coding: utf-8 -*-

from openerp import models, fields, api

class DeviceRequest(models.Model):
    _name = "hc.res.device.request"
    _description = "Device Request"
    
    name = fields.Char(
        string="Event Name", 
        required="True", 
        help="Text representation of the device request event. Subject + Code + Occurrence.")
    identifier_ids = fields.One2many(
        comodel_name="hc.device.request.identifier", 
        inverse_name="device_request_id", 
        string="Identifiers", 
        help="External Request identifier.")
    definition_ids = fields.One2many(
        comodel_name="hc.device.request.definition", 
        inverse_name="device_request_id", 
        string="Relevant Histories", 
        help="Protocol or definition.")
    based_on_ids = fields.One2many(
        comodel_name="hc.device.request.based.on", 
        inverse_name="device_request_id", 
        string="Based On", 
        help="What request fulfills.")
    prior_request_ids = fields.One2many(
        comodel_name="hc.device.request.prior.request", 
        inverse_name="device_request_id", 
        string="Prior Requests",
        help="What request replaces.")
    group_identifier_id = fields.Many2one(
        comodel_name="hc.device.request.group.identifier", 
        string="Group Identifier", 
        help="Identifier of composite request.")
    status = fields.Selection(
        string="Status", 
        selection=[
            ("draft", "Draft"), 
            ("active", "Active"), 
            ("suspended", "Suspended"), 
            ("completed", "Completed"), 
            ("entered-in-error", "Entered-In-Error"), 
            ("cancelled", "Cancelled")], 
        help="The status of the request.")
    intent = fields.Selection(
        string="Device Request Intent", 
        selection=[
            ("mild", "Mild"), 
            ("moderate", "Moderate"), 
            ("severe", "Severe")], 
        help="Whether the request is a proposal, plan, an original order or a reflex order.")
    priority_id = fields.Many2one(
        comodel_name="hc.vs.request.priority", 
        string="Priority", 
        help="how quickly the title should be addressed with respect to other requests.")
    code_type = fields.Selection(
        string="Code Type", 
        required="True", 
        selection=[
            ("device", "Device"), 
            ("codeable_concept", "Codeable Concept")], 
        help="Type of device requested.")
    code_name = fields.Char(
        string="Code", 
        compute="_compute_code_name", 
        store="True", 
        help="Device requested.")
    code_device_id = fields.Many2one(
        comodel_name="hc.res.device", 
        string="Code Device", 
        help="Device individual responsible for the annotation.")
    code_id = fields.Many2one(
        comodel_name="hc.vs.device.kind", 
        string="Code", 
        help="Code of individual responsible for the annotation.")
    subject_type = fields.Selection(
        string="Subject Type", 
        required="True", 
        selection=[("patient", "Patient"), 
        ("group", "Group"), 
        ("location", "Location"), 
        ("device", "Device")], 
        help="Type of focus of request.")
    subject_name = fields.Char(
        string="Subject", 
        compute="_compute_subject_name", 
        store="True", 
        help="Focus of request.")
    subject_patient_id = fields.Many2one(
        comodel_name="hc.res.patient", 
        string="Subject Patient", 
        required="True", 
        help="Patient focus of request.")
    subject_group_id = fields.Many2one(
        comodel_name="hc.res.group", 
        string="Subject Group Date", 
        help="Group focus of request.")
    subject_location_id = fields.Many2one(
        comodel_name="hc.res.location", 
        string="Subject Location Date", 
        help="Location focus of request.")
    subject_device_id = fields.Many2one(
        comodel_name="hc.res.device", 
        string="Subject Device Date", 
        help="Device focus of request.")
    context_type = fields.Selection(
        string="Context Type", 
        selection=[
        ("encounter", "Encounter"), 
        ("episode_of_care", "Episode Of Care")], 
        help="Encounter or Episode motivating request.")
    context_name = fields.Char(
        string="Context", 
        compute="_compute_context_name", 
        store="True", 
        help="Encounter or Episode motivating request.")
    context_encounter_id = fields.Many2one(
        comodel_name="hc.res.encounter", 
        string="Context Encounter", 
        help="Encounter motivating request.")
    context_episode_of_care_id = fields.Many2one(
        comodel_name="hc.res.episode.of.care", 
        string="Context Episode Of Care", 
        help="Episode Of Care motivating request.")
    occurrence_type = fields.Selection(
        string="Occurrence Type", 
        selection=[
            ("date_time", "Date Time"), 
            ("Period", "Period"), 
            ("Timing", "Timing")], 
        help="Type of desired time or schedule for use.")
    occurrence_name = fields.Char(
        string="Occurrence", 
        compute="_compute_occurrence_name", 
        store="True", help="Desired time or schedule for use.")
    occurrence_datetime = fields.Datetime(
        string="Occurrence Datetime", 
        help="Date Time desired time or schedule for use.")
    occurrence_start_date = fields.Datetime(
        string="Occurrence Start Date", 
        help="Start of desired time or schedule for use.")
    occurrence_end_date = fields.Datetime(
        string="Occurrence End Date", 
        help="End of desired time or schedule for use.")
    occurrence_timing_id = fields.Many2one(
        comodel_name="hc.device.request.occurrence.timing", 
        string="Occurrence Timing", 
        help="Timing desired time or schedule for use.")
    authored_on = fields.Datetime(
        string="Authored On", 
        help="When recorded.")
    performer_type_id = fields.Many2one(
        comodel_name="hc.vs.participant.role", 
        string="Performer Type", 
        help="Filler role.")
    performer_type = fields.Selection(
        string="Performer Type", 
        selection=[
            ("practitioner", "Practitioner"), 
            ("organization", "Organization"), 
            ("patient", "Patient"), 
            ("device", "Device"), 
            ("related_person", "Related Person"), 
            ("healthcare_service", "Healthcare Service")], 
        help="Type of requested filler.")
    performer_name = fields.Char(
        string="Performer", 
        compute="_compute_performer_name", 
        store="True", 
        help="Requested Filler.")
    performer_practitioner_id = fields.Many2one(
        comodel_name="hc.res.practitioner", 
        string="Performer Practitioner", 
        help="Practitioner requested filler.")
    performer_organization_id = fields.Many2one(
        comodel_name="hc.res.organization", 
        string="Performer Organization Date", 
        help="Organization requested filler.")
    performer_patient_id = fields.Many2one(
        comodel_name="hc.res.patient", 
        string="Performer Patient Date", 
        help="Patient requested filler.")
    performer_device_id = fields.Many2one(
        comodel_name="hc.res.device", 
        string="Performer Device Date", 
        help="Device requested filler.")
    performer_related_person_id = fields.Many2one(
        comodel_name="hc.res.related.person", 
        string="Performer Related Person Date", 
        help="Related Person requested filler.")
    performer_healthcare_service_id = fields.Many2one(
        comodel_name="hc.res.healthcare.service", 
        string="Performer Healthcare Service Date", 
        help="Healthcare Service requested filler.")
    reason_code_ids = fields.Many2many(
        comodel_name="hc.vs.condition.code", 
        relation="device_request_reason_code_rel", 
        string="Reason Codes", 
        help="Coded Reason for request.")
    reason_reference_ids = fields.One2many(
        comodel_name="hc.device.request.reason.reference", 
        inverse_name="device_request_id", 
        string="Reason References", help="Linked Reason for request.")
    supporting_info_ids = fields.One2many(
        comodel_name="hc.device.request.supporting.info", 
        inverse_name="device_request_id", 
        string="Supporting Info", 
        help="Additional clinical information.")
    note_ids = fields.One2many(
        comodel_name="hc.device.request.note", 
        inverse_name="device_request_id", 
        string="Notes", 
        help="Notes or comments.")
    relevant_history_ids = fields.One2many(
        comodel_name="hc.device.request.relevant.history", 
        inverse_name="device_request_id", 
        string="Relevant Histories", 
        help="Request provenance.")
    requester_id = fields.Many2one(
        comodel_name="hc.device.request.requester", 
        string="Requester", 
        help="Who/what is requesting diagnostics.")
    
class DeviceRequestRequester(models.Model):
    _name = "hc.device.request.requester"
    _description = "Device Request Requester"
    
    name = fields.Char(
        string="Event Name", 
        required="True", 
        help="Human-readable label for this device requester.")
    agent_type = fields.Selection(
        string="Agent Type", 
        required="True", 
        selection=[
            ("device", "Device"), 
            ("practitioner", "Practitioner"), 
            ("organization", "Organization")], 
        help="Type of individual making the request.")
    agent_name = fields.Char(
        string="Agent", 
        compute="_compute_agent_name", 
        store="True", 
        help="Individual making the request.")
    agent_device_id = fields.Many2one(
        comodel_name="hc.res.device", 
        string="Agent Device", 
        required="True", 
        help="Device making the request.")
    agent_practitioner_id = fields.Many2one(
        comodel_name="hc.res.practitioner", 
        string="Agent Practitioner Date", 
        help="Practitioner making the request.")
    agent_organization_id = fields.Many2one(
        comodel_name="hc.res.organization", 
        string="Agent Organization Date", 
        help="Organization making the request.")
    on_behalf_of_id = fields.Many2one(
        comodel_name="hc.res.organization", 
        string="On Behalf Of", 
        help="Organization agent is acting for.")
    
class DeviceRequestIdentifier(models.Model):
    _name = "hc.device.request.identifier"
    _description = "Device Request Identifier"
    _inherit = ["hc.basic.association", "hc.identifier"]
    
    device_request_id = fields.Many2one(
        comodel_name="hc.res.device.request", 
        string="Device Request", 
        help="Device Request associated with this Device Request Identifier.")
    
class DeviceRequestDefinition(models.Model):
    _name = "hc.device.request.definition"
    _description = "Device Request Definition"
    _inherit = ["hc.basic.association"]
    
    device_request_id = fields.Many2one(
        comodel_name="hc.res.device.request", 
        string="Device Request", 
        help="Device Request associated with this Device Request Definition.")
    definition_type = fields.Selection(
        string="Definition Type", 
        selection=[
            ("activity_definition", "Activity Definition"), 
            ("plan_definition", "Plan Definition")], 
        help="Protocol or definition.")

    definition_name = fields.Char(
        string="Definition", 
        compute="_compute_definition_name", 
        store="True", 
        help="Protocol or definition.")
    definition_activity_definition_id = fields.Many2one(
        comodel_name="hc.res.activity.definition", 
        string="Definition Activity Definition", 
        help="Activity Definition making the request.")
    definition_organization_id = fields.Many2one(
        comodel_name="hc.res.organization", 
        string="Definition Organization Date", 
        help="Organization making the request.")
    
class DeviceRequestBasedOn(models.Model):
    _name = "hc.device.request.based.on"
    _description = "Device Request Based On"
    _inherit = ["hc.basic.association"]
    
    device_request_id = fields.Many2one(
        comodel_name="hc.res.device.request", 
        string="Device Request", 
        help="Device Request associated with this Device Request Based On.")
    detail_type = fields.Char(
        string="Detail Type", 
        compute="_compute_detail_type", 
        store="True", 
        help="Type of what request fulfills.")
    based_on_name = fields.Reference(
        string="Based On", 
        selection="_reference_models", 
        help="What request fulfills.")
    
class DeviceRequestPriorRequest(models.Model):
    _name = "hc.device.request.prior.request"
    _description = "Device Request Prior Request"
    _inherit = ["hc.basic.association"]
    
    device_request_id = fields.Many2one(
        comodel_name="hc.res.device.request", 
        string="Device Request", 
        help="Device Request associated with this Device Request Prior Request.")
    detail_type = fields.Char(
        string="Detail Type", 
        compute="_compute_detail_type", 
        store="True", 
        help="Type of what request replaces.")
    prior_request_name = fields.Reference(
        string="Prior Request", 
        selection="_reference_models", 
        help="What request replaces.")
    
class DeviceRequestGroupIdentifier(models.Model):
    _name = "hc.device.request.group.identifier"
    _description = "Device Request Group Identifier"
    _inherit = ["hc.basic.association", "hc.identifier"]
    
class DeviceRequestOccurrenceTiming(models.Model):
    _name = "hc.device.request.occurrence.timing"
    _description = "Device Request Occurrence Timing"
    _inherit = ["hc.basic.association", "hc.timing"]
    
class DeviceRequestReasonReference(models.Model):
    _name = "hc.device.request.reason.reference"
    _description = "Device Request Reason Reference"
    _inherit = ["hc.basic.association"]
    
    device_request_id = fields.Many2one(
        comodel_name="hc.res.device.request", 
        string="Device Request", 
        help="Device Request associated with this Device Request Reason Reference.")
    reasonreference_type = fields.Char(
        string="Reasonreference Type", 
        compute="_compute_reasonreference_type", 
        store="True", 
        help="Type of linked Reason for request.")
    reason_reference_name = fields.Reference(
        string="Reason Reference", 
        selection="_reference_models", 
        help="Linked Reason for request.")
    
class DeviceRequestSupportingInfo(models.Model):
    _name = "hc.device.request.supporting.info"
    _description = "Device Request Supporting Info"
    _inherit = ["hc.basic.association"]
    
    device_request_id = fields.Many2one(
        comodel_name="hc.res.device.request", 
        string="Device Request", 
        help="Device Request associated with this Device Request Supporting Info.")
    supporting_info_type = fields.Char(
        string="Supporting Info Type", 
        compute="_compute_supporting_info_type", 
        store="True", 
        help="Type of additional clinical information.")
    supporting_info_name = fields.Reference(
        string="Supporting Info", 
        selection="_reference_models", 
        help="Additional clinical information.")
    
class DeviceRequestNote(models.Model):
    _name = "hc.device.request.note"
    _description = "Device Request Note"
    _inherit = ["hc.basic.association", "hc.annotation"]
    
    device_request_id = fields.Many2one(
        comodel_name="hc.res.device.request", 
        string="Device Request", 
        help="Device Request associated with this Device Request Note.")
    
class DeviceRequestRelevantHistory(models.Model):
    _name = "hc.device.request.relevant.history"
    _description = "Device Request Relevant History"
    _inherit = ["hc.basic.association"]
    
    device_request_id = fields.Many2one(
        comodel_name="hc.res.device.request", 
        string="Device Request", 
        help="Device Request associated with this Device Request Relevant History.")
    relevant_history_id = fields.Many2one(
        comodel_name="hc.res.provenance", 
        string="Relevant History", 
        help="Request provenance.")
