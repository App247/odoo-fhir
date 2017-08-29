# -*- coding: utf-8 -*-

from openerp import models, fields, api

class MedicationRequest(models.Model):
    _name = "hc.res.medication.request"
    _description = "Medication Request"

    name = fields.Char(
        string="Event Name",
        compute="_compute_name",
        store="True",
        help="Text representation of the medication request event. Subject Name + Medication + Authored Date.")
    identifier_ids = fields.One2many(
        comodel_name="hc.medication.request.identifier",
        inverse_name="medication_request_id",
        string="Identifiers",
        help="External identifier.")
    definition_ids = fields.One2many(
        comodel_name="hc.medication.request.definition",
        inverse_name="medication_request_id",
        string="Libraries",
        help="Protocol or definition.")
    based_on_ids = fields.One2many(
        comodel_name="hc.medication.request.based.on",
        inverse_name="medication_request_id",
        string="Libraries",
        help="What request fulfills.")
    group_identifier_id = fields.Many2one(
        comodel_name="hc.medication.request.group.identifier",
        string="Group Identifier",
        help="Composite request this is part of.")
    status = fields.Selection(
        string="Status",
        selection=[
            ("active", "Active"),
            ("on-hold", "On-Hold"),
            ("cancelled", "Cancelled"),
            ("completed", "Completed"),
            ("entered-in-error", "Entered-In-Error"),
            ("stopped", "Stopped"),
            ("draft", "Draft")],
        help="A code specifying the state of the order. Generally this will be active or completed state.")
    intent = fields.Selection(
        string="Intent",
        required="True",
        selection=[
            ("proposal", "Proposal"),
            ("plan", "Plan"),
            ("order", "Order")],
        help="Whether the request is a proposal, plan, or an original order.")
    priority = fields.Selection(
        string="Priority",
        selection=[
            ("routine", "Routine"),
            ("urgent", "Urgent"),
            ("stat", "Stat"),
            ("asap", "Asap")],
        help="Indicates how quickly the Medicaiton Request should be addressed with respect to other requests.")
    medication_type = fields.Selection(
        string="Medication Type",
        required="True",
        selection=[
            ("code", "Code"),
            ("medication", "Medication")],
         help="Type of medication to be taken.")
    medication_name = fields.Char(
        string="Medication",
        compute="_compute_medication_name",
        store="True",
        help="Medication to be taken.")
    medication_code_id = fields.Many2one(
        comodel_name="hc.vs.medication.code",
        string="Medication Code",
        help="Code of medication to be taken.")
    medication_id = fields.Many2one(
        comodel_name="hc.res.medication",
        string="Medication",
        required="True",
        help="Medication to be taken.")
    subject_type = fields.Selection(
        string="Subject Type",
        required="True",
        selection=[
            ("patient", "Patient"),
            ("group", "Group")],
        help="Who or group prescription is for.")
    subject_name = fields.Char(
        string="Subject",
        compute="_compute_subject_name",
        store="True",
        help="Who or group prescription is for.")
    subject_patient_id = fields.Many2one(
        comodel_name="hc.res.patient",
        string="Subject Patient",
        required="True",
        help="Who or group prescription is for.")
    subject_group_id = fields.Many2one(
        comodel_name="hc.res.group",
        string="Subject Group",
        help="Group or group prescription is for.")
    # replaced by subject
    # patient_id = fields.Many2one(
    #     comodel_name="hc.res.patient",
    #     string="Patient",
    #     required="True",
    #     help="Who prescription is for.")
    context_type = fields.Selection(
        string="Context Type",
        selection=[
            ("encounter", "Encounter"),
            ("episode_of_care", "Episode Of Care")],
        help="Type created during encounter/admission/stay.")
    context_name = fields.Char(
        string="Context",
        compute="_compute_context_name",
        store="True",
        help="Created during encounter/admission/sta.")
    context_encounter_id = fields.Many2one(
        comodel_name="hc.res.encounter",
        string="Context Encounter",
        help="Encounter created during encounter/admission/stay.")
    context_episode_of_care_id = fields.Many2one(
        comodel_name="hc.res.episode.of.care",
        string="Context Episode Of Care",
        help="Episode Of Care during encounter/admission/stay.")
    supporting_information_type = fields.Selection(
        string="Supporting Information Type",
        selection=[
            ("string", "String"),
            ("code", "Code")],
        help="Type of what is account tied to.")
    supporting_information_name = fields.Char(
        string="Supporting Information",
        compute="_compute_supporting_information_name",
        store="True",
        help="Information to support ordering of the medication.")
    supporting_information_string = fields.Char(
        string="Supporting Information String",
        help="String of information to support ordering of the medication.")
    supporting_information_code_id = fields.Many2one(
        comodel_name="hc.vs.resource.type",
        string="Supporting Information Code",
        help="Type of resource of information to support ordering of the medication.")
    authored_on = fields.Datetime(
        string="Authored On",
        help="When request was initially authored.")
    # replaced by authored_on
    # date_written = fields.Datetime(
    #     string="Date Written",
    #     help="When prescription was initially authorized.")
    recorder_id = fields.Many2one(
        comodel_name="hc.res.practitioner",
        string="Recorder",
        help="Person who entered the request.")
    # replaced by recorder
    # prescriber_id = fields.Many2one(
    #     comodel_name="hc.res.practitioner",
    #     string="Prescriber",
    #     help="Who ordered the initial medication(s).")
    reason_code_ids = fields.Many2many(
        comodel_name="hc.vs.condition.code",
        string="Reason Codes",
        help="Reason or indication for writing the prescription.")
    reason_reference_ids = fields.One2many(
        comodel_name="hc.medication.request.reason.reference",
        inverse_name="medication_request_id",
        string="Libraries",
        help="Condition or Observation that supports why the prescription is being written.")
    note_ids = fields.One2many(
        comodel_name="hc.medication.request.note",
        inverse_name="medication_request_id",
        string="Notes",
        help="Information about the prescription.")
    category_id = fields.Many2one(
        comodel_name="hc.vs.medication.request.category",
        string="Category",
        help="Type of medication usage.")
    dosage_instruction_ids = fields.One2many(
        comodel_name="hc.medication.request.dosage.instruction",
        inverse_name="medication_request_id",
        string="Dosage Instructions",
        help="How the medication should be taken.")
    prior_prescription_id = fields.Many2one(
        comodel_name="hc.res.medication.request",
        string="Prior Prescription",
        help="An order/prescription that this supersedes.")
    event_history_ids = fields.One2many(
        comodel_name="hc.medication.request.event.history",
        inverse_name="medication_request_id",
        string="Libraries",
        help="A list of events of interest in the lifecycle.")
    requester_ids = fields.One2many(
        comodel_name="hc.medication.request.requester",
        inverse_name="medication_request_id",
        string="Requesters",
        help="Who/What requested the Request.")
    dispense_request_ids = fields.One2many(
        comodel_name="hc.medication.request.dispense.request",
        inverse_name="medication_request_id",
        string="Dispense Requests",
        help="Medication supply authorization.")
    substitution_ids = fields.One2many(
        comodel_name="hc.medication.request.substitution",
        inverse_name="medication_request_id",
        string="Substitutions",
        help="Any restrictions on medication substitution.")

class MedicationRequestRequester(models.Model):
    _name = "hc.medication.request.requester"
    _description = "Medication Request Requester"

    medication_request_id = fields.Many2one(
        comodel_name="hc.res.medication.request",
        string="Medication Request",
        help="Medication Request associated with this Medication Request Requester.")
    agent_type = fields.Selection(
        string="Agent Type",
        required="True",
        selection=[
            ("practitioner", "Practitioner"),
            ("organization", "Organization"),
            ("patient", "Patient"),
            ("related_person", "Related Person"),
            ("device", "Device")],
        help="Type of who ordered the initial medication(s).")
    agent_name = fields.Char(
        string="Agent",
        compute="_compute_agent_name",
        store="True",
        help="Who ordered the initial medication(s).")
    agent_practitioner_id = fields.Many2one(
        comodel_name="hc.res.practitioner",
        string="Agent Practitioner",
        help="Practitioner who ordered the initial medication(s).")
    agent_organization_id = fields.Many2one(
        comodel_name="hc.res.organization",
        string="Agent Organization",
        help="Organization ordered the initial medication(s).")
    agent_patient_id = fields.Many2one(
        comodel_name="hc.res.patient",
        string="Agent Patient",
        help="Patient ordered the initial medication(s).")
    agent_related_person_id = fields.Many2one(
        comodel_name="hc.res.related.person",
        string="Agent Related Person",
        help="Related Person ordered the initial medication(s).")
    agent_device_id = fields.Many2one(
        comodel_name="hc.res.device",
        string="Agent Device",
        help="Device ordered the initial medication(s).")
    on_behalf_of_id = fields.Many2one(
        comodel_name="hc.res.organization",
        string="On Behalf Of",
        required="True",
        help="Organization agent is acting for.")

class MedicationRequestDispenseRequest(models.Model):
    _name = "hc.medication.request.dispense.request"
    _description = "Medication Request Dispense Request"

    medication_request_id = fields.Many2one(
        comodel_name="hc.res.medication.request",
        string="Medication Request",
        help="Medication Request associated with this Medication Request Dispense Request.")
    validity_period_start_date = fields.Datetime(
        string="Validity Period Start Date",
        help="Start of the time period supply is authorized for.")
    validity_period_end_date = fields.Datetime(
        string="Validity Period End Date",
        help="End of the time period supply is authorized for.")
    number_of_repeats_allowed = fields.Integer(
        string="Number Of Repeats Allowed",
        elp="Number of refills authorized.")
    quantity = fields.Float(
        string="Quantity",
        help="Amount of medication to supply per dispense.")
    expected_supply_duration = fields.Float(
        string="Expected Supply Duration",
        help="Number of days supply per dispense.")
    expected_supply_duration_uom_id = fields.Many2one(
        comodel_name="product.uom",
        string="Expected Supply Duration UOM",
        domain="[('category_id','=','Time (UCUM)')]",
        default="d",
        help="Expected Supply Duration unit of measure.")
    performer_id = fields.Many2one(
        comodel_name="hc.res.organization",
        string="Performer",
        help="Intended dispenser.")

class MedicationRequestSubstitution(models.Model):
    _name = "hc.medication.request.substitution"
    _description = "Medication Request Substitution"

    medication_request_id = fields.Many2one(
        comodel_name="hc.res.medication.request",
        string="Medication Request",
        help="Medication Request associated with this Medication Request Substitution.")
    is_allowed = fields.Boolean(
        string="Allowed",
        required="True",
        help="Whether substitution is allowed or not.")
    reason_id = fields.Many2one(
        comodel_name="hc.vs.substance.admin.substitution.reason",
        string="Reason",
        help="Why should (not) substitution be made.")

class MedicationRequestIdentifier(models.Model):
    _name = "hc.medication.request.identifier"
    _description = "Medication Request Identifier"
    _inherit = ["hc.basic.association", "hc.identifier"]

    medication_request_id = fields.Many2one(
        comodel_name="hc.res.medication.request",
        string="Medication Request",
        help="Medication Request associated with this Medication Request Identifier.")

class MedicationRequestDefinition(models.Model):
    _name = "hc.medication.request.definition"
    _description = "Medication Request Definition"
    _inherit = ["hc.basic.association"]

    medication_request_id = fields.Many2one(
        comodel_name="hc.res.medication.request",
        string="Medication Request",
        help="Medication Request associated with this Medication Request Definition.")
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
        help="Activity Definition protocol or definition.")
    definition_plan_definition_id = fields.Many2one(
        comodel_name="hc.res.plan.definition",
        string="Definition Plan Definition",
        help="Plan Definition or definition.")

class MedicationRequestBasedOn(models.Model):
    _name = "hc.medication.request.based.on"
    _description = "Medication Request Based On"
    _inherit = ["hc.basic.association"]

    medication_request_id = fields.Many2one(
        comodel_name="hc.res.medication.request",
        string="Medication Request",
        help="Medication Request associated with this Medication Request Based On.")
    based_on_type = fields.Selection(
        string="Based On Type",
        selection=[
            # ("care_plan", "Care Plan"),
            ("medication_request", "Medication Request"),
            ("procedure_request", "Procedure Request")],
        help="Type of what request fulfills.")
    based_on_name = fields.Char(
        string="Based On",
        compute="_compute_based_on_name",
        store="True", help="What request fulfill.")
    # based_on_care_plan_id = fields.Many2one(
    #     comodel_name="hc.res.care.plan",
    #     string="Based On Care Plan",
    #     help="Care Plan request fulfills.")
    based_on_medication_request_id = fields.Many2one(
        comodel_name="hc.res.medication.request",
        string="Based On Medication Request",
        help="Medication Request fulfills.")
    based_on_procedure_request_id = fields.Many2one(
        comodel_name="hc.res.procedure.request",
        string="Based On Procedure Request",
        help="Procedure Request fulfills.")

class MedicationRequestGroupIdentifier(models.Model):
    _name = "hc.medication.request.group.identifier"
    _description = "Medication Request Group Identifier"
    _inherit = ["hc.basic.association", "hc.identifier"]

class MedicationRequestReasonReference(models.Model):
    _name = "hc.medication.request.reason.reference"
    _description = "Medication Request Reason Reference"
    _inherit = ["hc.basic.association"]

    medication_request_id = fields.Many2one(
        comodel_name="hc.res.medication.request",
        string="Medication Request",
        help="Medication Request associated with this Medication Request Reason Reference.")
    reason_reference_type = fields.Selection(
        string="Reason Reference Type",
        selection=[
            ("condition", "Condition"),
            ("observation", "Observation")],
        help="Condition or Observation that supports why the prescription is being written.")
    reason_reference_name = fields.Char(
        string="Reason Reference",
        compute="_compute_reason_reference_name",
        store="True",
        help="Condition or Observation that supports why the prescription is being writte.")
    reason_reference_condition_id = fields.Many2one(
        comodel_name="hc.res.condition",
        string="Reason Reference Condition",
        help="Condition that supports why the prescription is being written.")
    reason_reference_observation_id = fields.Many2one(
        comodel_name="hc.res.observation",
        string="Reason Reference Observation",
        help="Observation that supports why the prescription is being written.")

class MedicationRequestNote(models.Model):
    _name = "hc.medication.request.note"
    _description = "Medication Request Note"
    _inherit = ["hc.basic.association", "hc.annotation"]

    medication_request_id = fields.Many2one(
        comodel_name="hc.res.medication.request",
        string="Medication Request",
        help="Medication Request associated with this Medication Request Note.")

class MedicationRequestDosageInstruction(models.Model):
    _name = "hc.medication.request.dosage.instruction"
    _description = "Medication Request Dosage Instruction"
    _inherit = ["hc.basic.association", "hc.dosage"]

    medication_request_id = fields.Many2one(
        comodel_name="hc.res.medication.request",
        string="Medication Request",
        help="Medication Request associated with this Medication Request Dosage Instruction.")

class MedicationRequestEventHistory(models.Model):
    _name = "hc.medication.request.event.history"
    _description = "Medication Request Event History"
    _inherit = ["hc.basic.association"]

    medication_request_id = fields.Many2one(
        comodel_name="hc.res.medication.request",
        string="Medication Request",
        help="Medication Request associated with this Medication Request Event History.")
    event_history_id = fields.Many2one(
        comodel_name="hc.res.provenance",
        string="Event History",
        help="Event History associated with this Medication Request Event History.")

class MedicationRequestCategory(models.Model):
    _name = "hc.vs.medication.request.category"
    _description = "Medication Request Category"
    _inherit = ["hc.value.set.contains"]

    name = fields.Char(
        string="Name",
        help="Name of this medication request category.")
    code = fields.Char(
        string="Code",
        help="Code of this medication request category.")
    contains_id = fields.Many2one(
        comodel_name="hc.vs.substance.admin.substitution.reason",
        string="Parent",
        help="Parent medication request category.")

class SubstanceAdminSubstitutionReason(models.Model):
    _name = "hc.vs.substance.admin.substitution.reason"
    _description = "Substance Admin Substitution Reason"
    _inherit = ["hc.value.set.contains"]

    name = fields.Char(
        string="Name",
        help="Name of this substance admin substitution reason.")
    code = fields.Char(
        string="Code",
        help="Code of this substance admin substitution reason.")
    contains_id = fields.Many2one(
        comodel_name="hc.vs.substance.admin.substitution.reason",
        string="Parent",
        help="Parent substance admin substitution reason.")
