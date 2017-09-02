# -*- coding: utf-8 -*-

from openerp import models, fields, api
from datetime import datetime
from openerp.tools import DEFAULT_SERVER_DATETIME_FORMAT as DTF

class ProcedureRequest(models.Model):
    _name = "hc.res.procedure.request"
    _description = "Procedure Request"
    _inherit = ["hc.domain.resource"]
    _rec_name = "name"

    name = fields.Char(
        string="Event Name",
        compute="_compute_name",
        store="True",
        help="Text representation of the procedure request event. Subject Name + Code + Occurrence.")
    identifier_ids = fields.One2many(
        comodel_name="hc.procedure.request.identifier",
        inverse_name="procedure_request_id",
        string="Identifiers",
        help="Identifier.")
    definition_ids = fields.One2many(
        comodel_name="hc.procedure.request.definition",
        inverse_name="procedure_request_id",
        string="Definitions",
        help="Protocol or definition.")
    based_on_ids = fields.One2many(
        comodel_name="hc.procedure.request.based.on",
        inverse_name="procedure_request_id",
        string="Based Ons",
        help="What request fulfills.")
    replaces_ids = fields.One2many(
        comodel_name="hc.procedure.request.replaces",
        inverse_name="procedure_request_id",
        string="Replaces",
        help="What request replaces.")
    requisition_id = fields.Many2one(
        comodel_name="hc.procedure.request.requisition",
        string="Requisition",
        help="Composite Request ID")
    status = fields.Selection(
        string="Status",
        selection=[
            ("draft", "Draft"),
            ("active", "Active"),
            ("suspended", "Suspended"),
            ("completed", "Completed"),
            ("entered-in-error", "Entered In Error"),
            ("cancelled", "Cancelled")],
        help="The status of the order.")
    intent = fields.Selection(
        string="Intent",
        selection=[
            ("proposal", "Proposal"),
            ("plan", "Plan"),
            ("order", "Order")],
        help="Whether the request is a proposal, plan, an original order or a reflex order.")
    priority = fields.Selection(
        string="Priority",
        selection=[
            ("routine", "Routine"),
            ("urgent", "Urgent"),
            ("asap", "Asap"),
            ("stat", "Stat")],
        help="The clinical priority associated with this order.")
    is_do_not_perform = fields.Boolean(
        string="Do Not Perform",
        help="True if procedure should not be performed")
    category_ids = fields.Many2many(
        comodel_name="hc.vs.procedure.request.category",
        string="Categories",
        help="What part of body to perform on.")
    code_id = fields.Many2one(
        comodel_name="hc.vs.procedure.code",
        string="Code",
        required="True",
        help="What is being requested/ordered.")
    subject_type = fields.Selection(
        string="Subject Type",
        required="True",
        selection=[
            ("patient", "Patient"),
            ("group", "Group"),
            ("location", "Location"),
            ("device", "Device")],
        help="Individual the service is ordered for.")
    subject_name = fields.Char(
        string="Subject",
        compute="_compute_subject_name",
        store="True",
        help="Who the procedure should be done to.")
    subject_patient_id = fields.Many2one(
        comodel_name="hc.res.patient",
        string="Subject Patient",
        help="Patient the service is ordered for.")
    subject_group_id = fields.Many2one(
        comodel_name="hc.res.group",
        string="Subject Group",
        help="Group the service is ordered for.")
    subject_location_id = fields.Many2one(
        comodel_name="hc.res.location",
        string="Subject Location",
        help="Location the service is ordered for.")
    subject_device_id = fields.Many2one(
        comodel_name="hc.res.device",
        string="Subject Device",
        help="Device the service is ordered for.")
    context_type = fields.Selection(
        string="Context Type",
        selection=[
            ("encounter", "Encounter"),
            ("episode_of_care", "Episode Of Care")],
        help="Type of Encounter or Episode during which request was created.")
    context_name = fields.Char(
        string="Context",
        compute="_compute_context_name",
        store="True",
        help="Encounter or Episode during which request was created.")
    context_encounter_id = fields.Many2one(
        comodel_name="hc.res.encounter",
        string="Context Encounter",
        help="Encounter during which request was created.")
    context_episode_of_care_id = fields.Many2one(
        comodel_name="hc.res.encounter",
        string="Context Episode Of Care",
        help="Episode during which request was created.")
    occurrence_type = fields.Selection(
        string="Occurrence Type",
        selection=[
            ("date_time", "Date Time"),
            ("period", "Period"),
            ("timing", "Timing")],
        help="Type of when procedure should occur.")
    occurrence_name = fields.Char(
        string="Occurrence",
        compute="_compute_occurrence_name",
        store="True",
        help="When procedure should occur.")
    occurrence_date_time = fields.Datetime(
        string="Occurrence Date Time",
        help="Date Time when procedure should occur.")
    occurrence_start_date = fields.Datetime(
        string="Occurrence Start Date",
        help="Start of the period when procedure should occur.")
    occurrence_end_date = fields.Datetime(
        string="Occurrence End Date",
        help="End of the period when procedure should occur.")
    occurrence_timing_id = fields.Many2one(
        comodel_name="hc.procedure.request.occurrence.timing",
        string="Occurrence Timing",
        help="Timing when procedure should occur.")
    as_needed_type = fields.Selection(
        string="As Needed Type",
        selection=[
            ("boolean", "Boolean"),
            ("codeable_concept", "Codeable Concept")],
        help="Type of preconditions for procedure.")
    as_needed_name = fields.Char(
        string="As Needed",
        compute="_compute_as_needed_name",
        store="True",
        help="Preconditions for procedure.")
    as_needed_boolean = fields.Boolean(
        string="As Needed Boolean",
        help="Boolean of preconditions for procedure.")
    as_needed_codeable_concept_id = fields.Many2one(
        comodel_name="hc.vs.procedure.request.as.needed",
        string="As Needed Codeable Concept",
        help="Codeable Concept of preconditions for procedure.")
    authored_on = fields.Datetime(
        string="Authored On Date",
        help="Date request signed.")
    performer_role_id = fields.Many2one(
        comodel_name="hc.vs.participant.role",
        string="Performer Role",
        help='Indicates specific responsibility of an individual within the care team, such as "Primary physician", "Team coordinator", "Caregiver", etc.')
    performer_type = fields.Selection(
        string="Performer Type",
        selection=[
            ("practitioner", "Practitioner"),
            ("organization", "Organization"),
            ("patient", "Patient"),
            ("device", "Device"),
            ("related_person", "Related Person"),
            ("healthcare_service", "Healthcare Service")],
        help="Type of requested performer.")
    performer_name = fields.Char(
        string="Performer",
        compute="_compute_performer_name",
        store="True",
        help="Requested performer.")
    performer_practitioner_id = fields.Many2one(
        comodel_name="hc.res.practitioner",
        string="Performer Practitioner",
        help="Practitioner requested performer.")
    performer_organization_id = fields.Many2one(
        comodel_name="hc.res.organization",
        string="Performer Organization",
        help="Organization requested performer.")
    performer_patient_id = fields.Many2one(
        comodel_name="hc.res.patient",
        string="Performer Patient",
        help="Patient requested performer.")
    performer_device_id = fields.Many2one(
        comodel_name="hc.res.device",
        string="Performer Device",
        help="Device requested performer.")
    performer_related_person_id = fields.Many2one(
        comodel_name="hc.res.related.person",
        string="Performer Related Person",
        help="Related Person requested performer.")
    performer_healthcare_service_id = fields.Many2one(
        comodel_name="hc.res.healthcare.service",
        string="Performer Healthcare Service",
        help="Healthcare Service requested performer.")
    reason_code_ids = fields.Many2many(
        comodel_name="hc.vs.procedure.reason",
        string="Reason Codes",
        help="Explanation/justification for procedure or service.")
    reason_reference_ids = fields.One2many(
        comodel_name="hc.procedure.request.reason.reference",
        inverse_name="procedure_request_id",
        string="Reason References",
        help="Explanation/justification for procedure or service.")
    supporting_info_ids = fields.One2many(
        comodel_name="hc.procedure.request.supporting.info",
        inverse_name="procedure_request_id",
        string="Supporting Infos",
        help="Extra information to use in performing request.")
    specimen_ids = fields.One2many(
        comodel_name="hc.procedure.request.specimen",
        inverse_name="procedure_request_id",
        string="Specimens",
        help="Procedure samples.")
    body_site_ids = fields.Many2many(
        comodel_name="hc.vs.body.site",
        string="Body Sites",
        help="Location on Body.")
    note_ids = fields.One2many(
        comodel_name="hc.procedure.request.note",
        inverse_name="procedure_request_id",
        string="Notes",
        help="Comments.")
    description = fields.Text(
        string="Description",
        help="Text Summary.")
    relevant_history_ids = fields.One2many(
        comodel_name="hc.procedure.request.relevant.history",
        inverse_name="procedure_request_id",
        string="Relevant Histories",
        help="Request provenance.")
    requester_ids = fields.One2many(
        comodel_name="hc.procedure.request.requester",
        inverse_name="procedure_request_id",
        string="Requesters",
        help="Who/what is requesting procedure or diagnostic.")

    @api.depends('subject_name', 'code_id', 'authored_on')
    def _compute_name(self):
        comp_name = '/'
        for hc_res_procedure_request in self:
            if hc_res_procedure_request.subject_name:
                comp_name = hc_res_procedure_request.subject_name or ''
            if hc_res_procedure_request.code_id:
                comp_name = comp_name + ", " + hc_res_procedure_request.code_id.name or ''
            if hc_res_procedure_request.authored_on:
                comp_name = comp_name + ", " + datetime.strftime(datetime.strptime(hc_res_procedure_request.authored_on, DTF), "%Y-%m-%d")
            hc_res_procedure_request.name = comp_name

    @api.multi
    def _compute_subject_name(self):
        for hc_res_procedure_request in self:
            if hc_res_procedure_request.subject_type == 'patient':
                hc_res_procedure_request.subject_name = hc_res_procedure_request.subject_patient_id.name
            elif hc_res_procedure_request.subject_type == 'group':
                hc_res_procedure_request.subject_name = hc_res_procedure_request.subject_group_id.name
            elif hc_res_procedure_request.subject_type == 'location':
                hc_res_procedure_request.subject_name = hc_res_procedure_request.subject_location_id.name
            elif hc_res_procedure_request.subject_type == 'device':
                hc_res_procedure_request.subject_name = hc_res_procedure_request.subject_device_id.name

    @api.multi
    def _compute_context_name(self):
        for hc_res_procedure_request in self:
            if hc_res_procedure_request.context_type == 'encounter':
                hc_res_procedure_request.context_name = hc_res_procedure_request.context_encounter_id.name
            elif hc_res_procedure_request.context_type == 'episode_of_care':
                hc_res_procedure_request.context_name = hc_res_procedure_request.context_episode_of_care_id.name

    @api.multi
    def _compute_occurrence_name(self):
        for hc_res_procedure_request in self:
            if hc_res_procedure_request.occurrence_type == 'date_time':
                hc_res_procedure_request.occurrence_name = str(hc_res_procedure_request.occurrence_date_time)
            elif hc_res_procedure_request.occurrence_type == 'period':
                hc_res_procedure_request.occurrence_name = "Between " + str(hc_res_procedure_request.occurrence_start_date) + " and " + str(hc_res_procedure_request.occurrence_end_date)
            elif hc_res_procedure_request.occurrence_type == 'timing':
                hc_res_procedure_request.occurrence_name = hc_res_procedure_request.occurrence_timing_id.name

    @api.multi
    def _compute_as_needed_name(self):
        for hc_res_procedure_request in self:
            if hc_res_procedure_request.as_needed_type == 'boolean':
                hc_res_procedure_request.as_needed_name = hc_res_procedure_request.as_needed_boolean
            elif hc_res_procedure_request.as_needed_type == 'codeable_concept':
                hc_res_procedure_request.as_needed_name = hc_res_procedure_request.as_needed_codeable_concept_id.name

    @api.multi
    def _compute_performer_name(self):
        for hc_res_procedure_request in self:
            if hc_res_procedure_request.performer_type == 'practitioner':
                hc_res_procedure_request.performer_name = hc_res_procedure_request.performer_practitioner_id.name
            elif hc_res_procedure_request.performer_type == 'organization':
                hc_res_procedure_request.performer_name = hc_res_procedure_request.performer_organization_id.name
            elif hc_res_procedure_request.performer_type == 'patient':
                hc_res_procedure_request.performer_name = hc_res_procedure_request.performer_patient_id.name
            elif hc_res_procedure_request.performer_type == 'device':
                hc_res_procedure_request.performer_name = hc_res_procedure_request.performer_device_id.name
            elif hc_res_procedure_request.performer_type == 'related_person':
                hc_res_procedure_request.performer_name = hc_res_procedure_request.performer_related_person_id.name
            elif hc_res_procedure_request.performer_type == 'healthcare_service':
                hc_res_procedure_request.performer_name = hc_res_procedure_request.performer_healthcare_service_id.name

class ProcedureRequestRequester(models.Model):
    _name = "hc.procedure.request.requester"
    _description = "Procedure Request Requester"

    procedure_request_id = fields.Many2one(
        comodel_name="hc.res.procedure.request",
        string="Procedure Request",
        help="Procedure Request associated with this Procedure Request Requester.")
    agent_type = fields.Selection(
        string="Agent Type",
        selection=[
            ("practitioner", "Practitioner"),
            ("organization", "Organization"),
            ("patient", "Patient"),
            ("related_person", "Related Person"),
            ("device", "Device")],
        help="Type of individual making the request.")
    agent_name = fields.Char(
        string="Agent",
        compute="_compute_agent_name",
        store="True",
        help="Individual making the request.")
    agent_practitioner_id = fields.Many2one(
        comodel_name="hc.res.practitioner",
        string="Agent Practitioner",
        help="Practitioner making the request.")
    agent_organization_id = fields.Many2one(
        comodel_name="hc.res.organization",
        string="Agent Organization",
        help="Organization making the request.")
    agent_patient_id = fields.Many2one(
        comodel_name="hc.res.patient",
        string="Agent Patient",
        help="Patient making the request.")
    agent_related_person_id = fields.Many2one(
        comodel_name="hc.res.related.person",
        string="Agent Related Person",
        help="Related Person making the request.")
    agent_device_id = fields.Many2one(
        comodel_name="hc.res.device",
        string="Agent Device",
        help="Device making the request.")
    on_behalf_of_id = fields.Many2one(
        comodel_name="hc.res.organization",
        string="On Behalf Of",
        help="Organization agent is acting for.")

    @api.multi
    def _compute_agent_name(self):
        for hc_res_procedure in self:
            if hc_res_procedure.agent_type == 'practitioner':
                hc_res_procedure.agent_name = hc_res_procedure.agent_practitioner_id.name
            elif hc_res_procedure.agent_type == 'organization':
                hc_res_procedure.agent_name = hc_res_procedure.agent_organization_id.name
            elif hc_res_procedure.agent_type == 'patient':
                hc_res_procedure.agent_name = hc_res_procedure.agent_patient_id.name
            elif hc_res_procedure.agent_type == 'related_person':
                hc_res_procedure.agent_name = hc_res_procedure.agent_related_person_id.name
            elif hc_res_procedure.agent_type == 'device':
                hc_res_procedure.agent_name = hc_res_procedure.agent_device_id.name

class ProcedureRequestIdentifier(models.Model):
    _name = "hc.procedure.request.identifier"
    _description = "Procedure Request Identifier"
    _inherit = ["hc.basic.association", "hc.identifier"]

    procedure_request_id = fields.Many2one(
        comodel_name="hc.res.procedure.request",
        string="Procedure Request",
        help="Procedure Request associated with this Procedure Request Identifier.")

class ProcedureRequestDefinition(models.Model):
    _name = "hc.procedure.request.definition"
    _description = "Procedure Request Definition"
    _inherit = ["hc.basic.association"]

    procedure_request_id = fields.Many2one(
        comodel_name="hc.res.procedure.request",
        string="Procedure Request",
        help="Procedure Request associated with this Procedure Request Definition.")
    definition_type = fields.Selection(
        string="Definition Type",
        selection=[
            ("activity_definition", "Activity Definition"),
            ("plan_definition", "Plan Definition")],
        help="Type of protocol or definition.")
    definition_name = fields.Char(
        string="Definition",
        compute="_compute_definition_name",
        store="True",
        help="Protocol or definition.")
    definition_activity_definition_id = fields.Many2one(
        comodel_name="hc.res.activity.definition",
        string="Definition Activity Definition",
        help="Activity Definition protocol or definition.")
    definition_plan_definition_id = fields.Many2one(
        comodel_name="hc.res.plan.definition",
        string="Definition Plan Definition",
        help="Plan Definition protocol or definition.")

class ProcedureRequestRequisition(models.Model):
    _name = "hc.procedure.request.requisition"
    _description = "Procedure Request Identifier"
    _inherit = ["hc.basic.association", "hc.identifier"]

    procedure_request_id = fields.Many2one(
        comodel_name="hc.res.procedure.request",
        string="Procedure Request",
        help="Procedure Request associated with this Procedure Request Requisition.")

class ProcedureRequestBasedOn(models.Model):
    _name = "hc.procedure.request.based.on"
    _description = "Procedure Request Based On"
    _inherit = ["hc.basic.association"]

    procedure_request_id = fields.Many2one(
        comodel_name="hc.res.procedure.request",
        string="Procedure Request",
        help="Procedure Request associated with this Procedure Request Based On.")
    based_on_type = fields.Selection(
        string="Based On Type",
        selection=[
            # ("care_plan", "Care Plan"),
            # ("medication_request", "medication Request"),
            ("procedure_request", "Procedure Request")],
        help="Type of what request fulfills.")
    based_on_name = fields.Char(
        string="Based On",
        compute="_compute_based_on_name",
        store="True",
        help="What request fulfills.")
    # based_on_care_plan_id = fields.Many2one(
    #     comodel_name="hc.res.care.plan",
    #     string="Based On Care Plan",
    #     help="Care Plan fulfills.")
    based_on_procedure_request_id = fields.Many2one(
        comodel_name="hc.res.procedure.request",
        string="Based On Procedure Request",
        help="Procedure Request fulfills.")
    # based_on_medication_request_id = fields.Many2one(
    #     comodel_name="hc.res.medication.request",
    #     string="Based On Medication Request",
    #     help="Medication Request fulfills.")

    @api.multi
    def _compute_based_on_name(self):
        for hc_procedure_request in self:
            if hc_procedure_request.based_on_type == 'procedure_request':
                hc_procedure_request.based_on_name = hc_procedure_request.based_on_procedure_request_id.name
#             # elif hc_procedure_request.based_on_type == 'care_plan':
#             #     hc_procedure_request.based_on_name = hc_procedure_request.based_on_care_plan_id.name
#             # elif hc_procedure_request.based_on_type == 'medication_request':
#             #     hc_procedure_request.based_on_name = hc_procedure_request.based_on_medication_request_id.name

class ProcedureRequestReplaces(models.Model):
    _name = "hc.procedure.request.replaces"
    _description = "Procedure Request Replaces"
    _inherit = ["hc.basic.association"]

    procedure_request_id = fields.Many2one(
        comodel_name="hc.res.procedure.request",
        string="Procedure Request",
        help="Procedure Request associated with this Procedure Request Replaces.")
    replaces_id = fields.Many2one(
        comodel_name="hc.res.procedure.request",
        string="Replaces",
        help="Procedure Request associated with this Procedure Request Replaces.")

class ProcedureRequestOccurrenceTiming(models.Model):
    _name = "hc.procedure.request.occurrence.timing"
    _description = "Procedure Request Occurrence Timing"
    _inherit = ["hc.basic.association", "hc.timing"]

class ProcedureRequestReasonReference(models.Model):
    _name = "hc.procedure.request.reason.reference"
    _description = "Procedure Request Reason Reference"
    _inherit = ["hc.basic.association"]

    procedure_request_id = fields.Many2one(
        comodel_name="hc.res.procedure.request",
        string="Procedure Request",
        help="Procedure Request associated with this Procedure Request Reason Reference.")
    reason_reference_type = fields.Selection(
        string="Reason Reference Type",
        selection=[
            ("condition", "Condition"),
            # ("observation", "Observation"),
            # ("diagnostic_report", "Diagnostic Report"),
            ("document_reference", "Document Reference")],
        help="Type of explanation/justification for procedure or service.")
    reason_reference_name = fields.Char(
        string="Reason Reference",
        compute="_compute_reason_reference_name",
        store="True",
        help="Explanation/Justification for procedure or service.")
    reason_reference_condition_id = fields.Many2one(
        comodel_name="hc.res.condition",
        string="Reason Reference Condition",
        help="Condition explanation/justification for procedure or service.")
    # reason_reference_observation_id = fields.Many2one(
    #     comodel_name="hc.res.observation",
    #     string="Reason Reference Observation",
    #     help="Observation explanation/justification for procedure or service.")
    # reason_reference_diagnostic_report_id = fields.Many2one(
    #     comodel_name="hc.res.diagnostic.report",
    #     string="Reason Reference Diagnostic Report",
    #     help="Diagnostic Report explanation/justification for procedure or service.")
    reason_reference_document_reference_id = fields.Many2one(
        comodel_name="hc.res.document.reference",
        string="Reason Reference Document Reference",
        help="Document Reference explanation/justification for procedure or service.")

    @api.multi
    def _compute_reason_reference_name(self):
        for hc_res_procedure_request in self:
            if hc_res_procedure_request.reason_type == 'condition':
                hc_res_procedure_request.reason_name = hc_res_procedure_request.reason_condition_id.name
#             # elif hc_res_procedure_request.reason_type == 'observation':
#             #     hc_res_procedure_request.reason_name = hc_res_procedure_request.reason_observation_id.name
#             # elif hc_res_procedure_request.reason_type == 'diagnostic_report':
            #     hc_res_procedure_request.reason_name = hc_res_procedure_request.reason_diagnostic_report_id.name
            elif hc_res_procedure_request.reason_type == 'document_reference':
                hc_res_procedure_request.reason_name = hc_res_procedure_request.reason_document_reference_id.name

class ProcedureRequestSupportingInfo(models.Model):
    _name = "hc.procedure.request.supporting.info"
    _description = "Procedure Request Supporting Info"
    _inherit = ["hc.basic.association"]

    procedure_request_id = fields.Many2one(
        comodel_name="hc.res.procedure.request",
        string="Procedure Request",
        help="Procedure Request associated with this Procedure Request Supporting Info.")
    supporting_info_type = fields.Char(
        string="Supporting Info Type",
        compute="_compute_supporting_info_type",
        store="True",
        help="Type of extra information to use in performing request.")
    supporting_info_name = fields.Reference(
        string="Supporting Info",
        selection="_reference_models",
        help="Extra information to use in performing request.")

    @api.model
    def _reference_models(self):
        models = self.env['ir.model'].search([('state', '!=', 'manual')])
        return [(model.model, model.name)
            for model in models
                if model.model.startswith('hc.res')]

    @api.depends('supporting_info_name')
    def _compute_supporting_info_type(self):
        for this in self:
            if this.supporting_info_name:
                this.supporting_info_type = this.supporting_info_name._description

class ProcedureRequestSpecimen(models.Model):
    _name = "hc.procedure.request.specimen"
    _description = "Procedure Request Specimen"
    _inherit = ["hc.basic.association"]

    procedure_request_id = fields.Many2one(
        comodel_name="hc.res.procedure.request",
        string="Procedure Request",
        help="Procedure Request associated with this Procedure Request Specimen.")
    # specimen_id = fields.Many2one(
    #     comodel_name="hc.res.specimen",
    #     string="Specimen",
    #     help="Specimen associated with this Procedure Request Specimen.")

class ProcedureRequestNote(models.Model):
    _name = "hc.procedure.request.note"
    _description = "Procedure Request Note"
    _inherit = ["hc.basic.association", "hc.annotation"]

    procedure_request_id = fields.Many2one(
        comodel_name="hc.res.procedure.request",
        string="Procedure Request",
        help="Procedure Request associated with this Procedure Request Note.")

class ProcedureRequestRelevantHistory(models.Model):
    _name = "hc.procedure.request.relevant.history"
    _description = "Procedure Request Relevant History"
    _inherit = ["hc.basic.association"]

    procedure_request_id = fields.Many2one(
        comodel_name="hc.res.procedure.request",
        string="Procedure Request",
        help="Procedure Request associated with this Procedure Request Relevant History.")
    relevant_history_id = fields.Many2one(
        comodel_name="hc.res.provenance",
        string="Relevant History",
        help="Provenance associated with this Procedure Request Relevant History.")

class ProcedureRequestCategory(models.Model):
    _name = "hc.vs.procedure.request.category"
    _description = "Procedure Request Category"
    _inherit = ["hc.value.set.contains"]

class ProcedureCode(models.Model):
    _name = "hc.vs.procedure.code"
    _description = "Procedure Code"
    _inherit = ["hc.value.set.contains"]

class MedicationAsNeeded(models.Model):
    _name = "hc.vs.medication.as.needed"
    _description = "Medication As Needed"
    _inherit = ["hc.value.set.contains"]

# External Reference

class EncounterIncomingReferral(models.Model):
    _inherit = "hc.encounter.incoming.referral"

    incoming_referral_id = fields.Many2one(
        comodel_name="hc.res.procedure.request",
        string="Incoming Referral",
        help="Procedure Request associated with this Encounter Incoming Referral.")

class EpisodeOfCareReferralRequest(models.Model):
    _inherit = "hc.episode.of.care.referral.request"

    referral_request_id = fields.Many2one(
        comodel_name="hc.res.procedure.request",
        string="Referral Request",
        required="True",
        help="Procedure Request associated with this Episode Of Care Referral Request.")

class AppointmentIncomingReferral(models.Model):
    _inherit = "hc.appointment.incoming.referral"

    incoming_referral_id = fields.Many2one(
        comodel_name="hc.res.procedure.request",
        string="Incoming Referral",
        help="The ProcedureRequest provided as information to allocate to the Encounter.")
