# -*- coding: utf-8 -*-

from openerp import models, fields, api

class MedicationStatement(models.Model):
    _name = "hc.res.medication.statement"
    _description = "Medication Statement"

    name = fields.Char(
        string="Event Name",
        compute="_compute_name",
        store="True",
        help="Text representation of the medication statement. Subject Name + Medication + Effective Date.")
    identifier_ids = fields.One2many(
        comodel_name="hc.medication.statement.identifier",
        inverse_name="medication_statement_id",
        string="Identifiers",
        help="External Identifier.")
    based_on_ids = fields.One2many(
        comodel_name="hc.medication.statement.based.on",
        inverse_name="medication_statement_id",
        string="Based On",
        help="Fulfils plan, proposal or order.")
    context_type = fields.Selection(
        string="Context Type",
        selection=[
            ("encounter", "Encounter"),
            ("episode_of_care", "Episode Of Care")],
        help="Encounter / Episode associated with Medication Statement.")
    context_name = fields.Char(
        string="Context",
        compute="_compute_context_name",
        store="True",
        help="Encounter / Episode associated with Medication Statement.")
    context_encounter_id = fields.Many2one(
        comodel_name="hc.res.encounter",
        string="Context Encounter",
        help="Encounter associated with medication statement.")
    context_episode_of_care_id = fields.Many2one(
        comodel_name="hc.res.episode.of.care",
        string="Context Episode Of Care",
        help="Episode Of Care associated with medication statement.")
    status = fields.Selection(
        string="Status",
        required="True",
        selection=[
            ("active", "Active"),
            ("completed", "Completed"),
            ("entered-in-error", "Entered-In-Error"),
            ("intended", "Intended"),
            ("stopped", "Stopped"),
            ("on-hold", "On-Hold")],
        help="A code representing the patient or other source's judgment about the state of the medication used that this statement is about.")
    medication_type = fields.Selection(
        string="Medication Type",
        required="True",
        selection=[
            ("code", "Code"),
            ("Medication", "Medication")],
        help="Type of what medication was taken.")
    medication_name = fields.Char(
        string="Medication",
        compute="_compute_medication_name",
        store="True",
        help="What medication was taken.")
    medication_code_id = fields.Many2one(
        comodel_name="hc.vs.medication.code",
        string="Medication Code",
        help="Code of what medication was taken.")
    medication_id = fields.Many2one(
        comodel_name="hc.res.medication",
        string="Medication",
        help="What medication was taken.")
    subject_type = fields.Selection(
        string="Subject Type",
        required="True",
        selection=[
            ("patient", "Patient"),
            ("group", "Group")],
        help="Type of who is/was taking the medication.")
    subject_name = fields.Char(
        string="Subject",
        compute="_compute_subject_name",
        store="True",
        help="Who is/was taking the medication.")
    subject_patient_id = fields.Many2one(
        comodel_name="hc.res.patient",
        string="Subject Patient",
        help="Patient who is/was taking the medication.")
    subject_group_id = fields.Many2one(
        comodel_name="hc.res.group",
        string="Subject Group",
        help="Group who is/was taking the medication.")
    effective_type = fields.Selection(
        string="Effective Type",
        selection=[
            ("dateTime", "Datetime"),
            ("Period", "Period")],
        help="Type of over what period was medication consumed.")
    effective_name = fields.Char(
        string="Effective",
        compute="_compute_effective_name",
        store="True",
        help="Over what period was medication consumed?")
    effective_date = fields.Datetime(
        string="Effective Date",
        help="Over what period was medication consumed?")
    effective_start_date = fields.Datetime(
        string="Effective Start Date",
        help="Start of the period when medication was consumed.")
    effective_end_date = fields.Datetime(
        string="Effective End Date",
        help="End of the period when medication was consumed.")
    information_source_type = fields.Selection(
        string="Information Source Type",
        selection=[
            ("patient", "Patient"),
            ("practitioner", "Practitioner"),
            ("related_person", "Related Person")],
        help="Type of person who provided the information about the taking of this medication.")
    information_source_name = fields.Char(
        string="Information Source",
        compute="_compute_information_source_name",
        store="True",
        help="Person who provided the information about the taking of this medication.")
    information_source_patient_id = fields.Many2one(
        comodel_name="hc.res.patient",
        string="Information Source Patient",
        help="Patient who provided the information about the taking of this medication.")
    information_source_practitioner_id = fields.Many2one(
        comodel_name="hc.res.practitioner",
        string="Information Source Practitioner",
        help="Practitioner who provided the information about the taking of this medication.")
    information_source_related_person_id = fields.Many2one(
        comodel_name="hc.res.related.person",
        string="Information Source Related Person",
        help="Related Person who provided the information about the taking of this medication.")
    derived_from_ids = fields.One2many(
        comodel_name="hc.medication.statement.derived.from",
        inverse_name="medication_statement_id",
        string="Derived From",
        help="Additional supporting information.")
    date_asserted = fields.Datetime(
        string="Date Asserted",
        help="When the statement was asserted?")
    is_not_taken = fields.Boolean(
        string="Not Taken",
        help="True if medication is/was not being taken.")
    reason_not_taken_ids = fields.Many2many(
        comodel_name="hc.vs.medication.reason.not.taken",
        relation="medication_statement_reason_not_taken_rel",
        string="Reasons Not Taken",
        help="True if asserting medication was not given.")
    reason_for_use_ids = fields.Many2many(
        comodel_name="hc.vs.condition.code",
        relation="medication_statement_reason_for_use_rel",
        string="Reasons For Use",
        help="Reason for why the medication is being/was taken.")
    reason_for_use_reference_ids = fields.One2many(
        comodel_name="hc.medication.statement.reason.for.use.reference",
        inverse_name="medication_statement_id",
        string="Reasons For Use Reference",
        help="Condition that supports why the medication is being/was taken.")
    note_ids = fields.One2many(
        comodel_name="hc.medication.statement.note",
        inverse_name="medication_statement_id",
        string="Notes",
        help="Further information about the statement.")
    category_id = fields.Many2one(
        comodel_name="hc.vs.medication.statement.category",
        string="Medication Statement Category",
        help="Type of medication usage.")
    dosage_ids = fields.One2many(
        comodel_name="hc.medication.statement.dosage",
        inverse_name="medication_statement_id",
        string="Dosages",
        help="Details of how medication was taken.")

class MedicationStatementIdentifier(models.Model):
    _name = "hc.medication.statement.identifier"
    _description = "Medication Statement Identifier"
    _inherit = ["hc.basic.association", "hc.identifier"]

    medication_statement_id = fields.Many2one(
        comodel_name="hc.res.medication.statement",
        string="Medication Statement",
        help="Medication Statement associated with this Medication Statement Identifier.")

class MedicationStatementBasedOn(models.Model):
    _name = "hc.medication.statement.based.on"
    _description = "Medication Statement Based On"
    _inherit = ["hc.basic.association"]

    medication_statement_id = fields.Many2one(
        comodel_name="hc.res.medication.statement",
        string="Medication Statement",
        help="Medication Statement associated with this Medication Statement Based On.")
    based_on_type = fields.Selection(
        string="Based On Type",
        selection=[
            ("medication_request", "Medication Request"),
            # ("care_plan", "Care Plan"),
            ("procedure_request", "Procedure Request")],
        help="Type of fulfils plan, proposal or order.")
    based_on_name = fields.Char(
        string="Based On",
        compute="_compute_based_on_name",
        store="True",
        help="Fulfils plan, proposal or order.")
    based_on_medication_request_id = fields.Many2one(
        comodel_name="hc.res.medication.request",
        string="Based On Medication Request",
        help="Medication Request that is fulfilled in whole or in part by this event.")
    # based_on_care_plan_id = fields.Many2one(
    #     comodel_name="hc.res.care.plan",
    #     string="Based On Care Plan",
    #     help="Care Plan that is fulfilled in whole or in part by this event.")
    based_on_procedure_request_id = fields.Many2one(
        comodel_name="hc.res.procedure.request",
        string="Based On Procedure Request",
        help="Procedure Request that is fulfilled in whole or in part by this event.")

class MedicationStatementDerivedFrom(models.Model):
    _name = "hc.medication.statement.derived.from"
    _description = "Medication Statement Supporting Information"
    _inherit = ["hc.basic.association"]

    medication_statement_id = fields.Many2one(
        comodel_name="hc.res.medication.statement",
        string="Medication Statement",
        help="Medication Statement associated with this Medication Statement Supporting Information.")
    derived_from_type = fields.Selection(
        string="Derived From Type",
        selection=[
            ("string", "String"),
            ("code", "Code")],
        help="Type of additional supporting information.")
    derived_from_name = fields.Char(
        string="Derived From",
        compute="_compute_derived_from_name",
        store="True",
        help="Additional supporting information.")
    derived_from_string = fields.Char(
        string="Derived From String",
        help="String of additional supporting information.")
    derived_from_code_id = fields.Many2one(
        comodel_name="hc.vs.resource.type",
        string="Derived From Code",
        help="Resource type of additional supporting information.")

class MedicationStatementReasonForUseReference(models.Model):
    _name = "hc.medication.statement.reason.for.use.reference"
    _description = "Medication Statement Reason For Use Reference"
    _inherit = ["hc.basic.association"]

    medication_statement_id = fields.Many2one(
        comodel_name="hc.res.medication.statement",
        string="Medication Statement",
        help="Medication Statement associated with this Medication Statement Reason For Use Reference.")
    reason_for_use_reference_id = fields.Many2one(
        comodel_name="hc.res.condition",
        string="Reason For Use Reference",
        help="Condition associated with this Medication Statement Reason For Use Reference.")

class MedicationStatementNote(models.Model):
    _name = "hc.medication.statement.note"
    _description = "Medication Statement Note"
    _inherit = ["hc.basic.association", "hc.annotation"]

    medication_statement_id = fields.Many2one(
        comodel_name="hc.res.medication.statement",
        string="Medication Statement",
        help="Medication Statement associated with this Medication Statement Note.")

class MedicationStatementDosage(models.Model):
    _name = "hc.medication.statement.dosage"
    _description = "Medication Statement Supporting Information"
    _inherit = ["hc.basic.association", "hc.dosage"]

    medication_statement_id = fields.Many2one(
        comodel_name="hc.res.medication.statement",
        string="Medication Statement",
        help="Medication Statement associated with this Medication Statement Supporting Information.")

class MedicationStatementCategory(models.Model):
    _name = "hc.vs.medication.statement.category"
    _description = "Medication Statement Category"
    _inherit = ["hc.value.set.contains"]

class MedicationReasonNotTaken(models.Model):
    _name = "hc.vs.medication.reason.not.taken"
    _description = "Medication Reason Not Taken"
    _inherit = ["hc.value.set.contains"]
