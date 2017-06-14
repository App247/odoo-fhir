# -*- coding: utf-8 -*-

from openerp import models, fields, api

class Encounter(models.Model):
    _name = "hc.res.encounter"
    _description = "Encounter"

    name = fields.Char(
        string="Name",
        compute="_compute_name",
        store="True",
        help="Text representation of the encounter event. Patient Name + Encounter Type + Start Date.")
    identifier_ids = fields.One2many(
        comodel_name="hc.encounter.identifier",
        inverse_name="encounter_id",
        string="Identifiers",
        help="Identifier(s) by which this encounter is known.")
    status = fields.Selection(
        string="Status",
        required="True",
        selection=[
            ("planned", "Planned"),
            ("arrived", "Arrived"),
            ("triaged", "Triaged"),
            ("in-progress", "In-Progress"),
            ("onleave", "On Leave"),
            ("finished", "Finished"),
            ("cancelled", "Cancelled"),
            ("entered-in-error", "Entered-In-Error"),
            ("unknown", "Unknown")],
        help="Current state of the encounter.")
    class_id = fields.Many2one(
        comodel_name="hc.vs.act.encounter.code",
        string="Class",
        help="Classification of the encounter.")
    type_ids = fields.Many2many(
        comodel_name="hc.vs.encounter.type",
        relation="encounter_type_rel",
        string="Types",
        help="Specific type of encounter.")
    priority_id = fields.Many2one(
        comodel_name="hc.vs.act.priority",
        string="Priority",
        help="Indicates the urgency of the encounter.")
    subject_type = fields.Selection(
        string="Subject Type",
        selection=[
            ("patient", "Patient"),
            ("group", "Group")],
        help="The patient or group present at the encounter.")
    subject_name = fields.Char(
        string="Subject",
        compute="_compute_subject_name",
        store="True",
        help="The patient ro group present at the encounter.")
    subject_patient_id = fields.Many2one(
        comodel_name="hc.res.patient",
        string="Subject Patient",
        help="Patient present at the encounter.")
    subject_group_id = fields.Many2one(
        comodel_name="hc.res.group",
        string="Subject Group",
        help="Group present at the encounter.")
    episode_of_care_ids = fields.One2many(
        comodel_name="hc.encounter.episode.of.care",
        inverse_name="encounter_id",
        string="Episodes of Care",
        help="Episode(s) of care that this encounter should be recorded against.")
    incoming_referral_ids = fields.One2many(
        comodel_name="hc.encounter.incoming.referral",
        inverse_name="encounter_id",
        string="Incoming Referrals",
        help="The ProcedureRequest that initiated this encounter.")
    appointment_id = fields.Many2one(
        comodel_name="hc.res.appointment",
        string="Appointment",
        help="The appointment that scheduled this encounter.")
    start_date = fields.Datetime(
        string="Start Date",
        help="Start of the encounter.")
    end_date = fields.Datetime(
        string="End Date",
        help="End of the encounter.")
    length = fields.Float(
        string="Length",
        help="Quantity of time the encounter lasted (less time absent).")
    length_uom_id = fields.Many2one(
        comodel_name="product.uom",
        string="Length UOM",
        domain="[('category_id','=','Time (UCUM)')]",
        help="Length unit of measure.")
    reason_ids = fields.Many2many(
        comodel_name="hc.vs.encounter.reason",
        relation="encounter_reason_rel",
        string="Reasons",
        help="Reason the encounter takes place (code).")
    account_ids = fields.One2many(
        comodel_name="hc.encounter.account",
        inverse_name="encounter_id",
        string="Accounts",
        help="The set of accounts that may be used for billing for this Encounter.")
    service_provider_id = fields.Many2one(
        comodel_name="hc.res.organization",
        string="Service Provider",
        help="The custodian organization of this Encounter record.")
    part_of_id = fields.Many2one(
        comodel_name="hc.res.encounter",
        string="Part Of",
        help="Another Encounter this encounter is part of.")
    status_history_ids = fields.One2many(
        comodel_name="hc.encounter.status.history",
        inverse_name="encounter_id",
        string="Status History",
        help="List of Encounter statuses.")
    class_history_ids = fields.One2many(
        comodel_name="hc.encounter.class.history",
        inverse_name="encounter_id",
        string="Class Histories",
        help="List of past encounter classes.")
    participant_ids = fields.One2many(
        comodel_name="hc.encounter.participant",
        inverse_name="encounter_id",
        string="Participants",
        help="List of participants involved in the encounter.")
    diagnosis_ids = fields.One2many(
        comodel_name="hc.encounter.diagnosis",
        inverse_name="encounter_id",
        string="Diagnosis",
        help="The list of diagnosis relevant to this encounter.")
    hospitalization_ids = fields.One2many(
        comodel_name="hc.encounter.hospitalization",
        inverse_name="encounter_id",
        string="Hospitalizations",
        help="Details about an admission to a clinic.")
    location_ids = fields.One2many(
        comodel_name="hc.encounter.location",
        inverse_name="encounter_id",
        string="Locations",
        help="List of locations the patient has been at.")

class EncounterStatusHistory(models.Model):
    _name = "hc.encounter.status.history"
    _description = "Encounter Status History"

    encounter_id = fields.Many2one(
        comodel_name="hc.res.encounter",
        string="Encounter",
        help="Encounter associated with this Encounter Status History.")
    status = fields.Char(
        string="Status",
        compute="_compute_status",
        store="True",
        help="Status of the encounter.")
    start_date = fields.Datetime(
        string="Start Date",
        required="True",
        help="Start of the the time that the episode was in the specified status.")
    end_date = fields.Datetime(
        string="End Date",
        help="End of the the time that the episode was in the specified status.")
    time_diff_day = fields.Char(
        string="Time Diff (days)",
        help="Days duration of the status.")
    time_diff_hour = fields.Char(
        string="Time Diff (hours)",
        help="Hours duration of the status.")
    time_diff_min = fields.Char(
        string="Time Diff (minutes)",
        help="Minutes duration of the status.")
    time_diff_sec = fields.Char(
        string="Time Diff (seconds)",
        help="Seconds duration of the status.")

class EncounterClassHistory(models.Model):
    _name = "hc.encounter.class.history"
    _description = "Encounter Class History"

    encounter_id = fields.Many2one(
        comodel_name="hc.res.encounter",
        string="Encounter",
        help="Encounter associated with this Encounter Class History.")
    encounter_class = fields.Char(
        string="Class",
        help="Class of the encounter.")
    start_date = fields.Datetime(
        string="Start Date",
        required="True",
        help="Start of the the time that the episode was in the specified class.")
    end_date = fields.Datetime(
        string="End Date",
        help="End of the the time that the episode was in the specified class.")
    time_diff_day = fields.Char(
        string="Time Diff (days)",
        help="Days duration of the class.")
    time_diff_hour = fields.Char(
        string="Time Diff (hours)",
        help="Hours duration of the class.")
    time_diff_min = fields.Char(
        string="Time Diff (minutes)",
        help="Minutes duration of the class.")
    time_diff_sec = fields.Char(
        string="Time Diff (seconds)",
        help="Seconds duration of the class.")

class EncounterParticipant(models.Model):
    _name = "hc.encounter.participant"
    _description = "Encounter Participant"

    encounter_id = fields.Many2one(
        comodel_name="hc.res.encounter",
        string="Encounter",
        help="Encounter associated with this Encounter Participant.")
    type_ids = fields.Many2many(
        comodel_name="hc.vs.encounter.participant.type",
        relation="encounter_participant_type_rel",
        string="Types",
        help="Role of participant in encounter.")
    start_date = fields.Datetime(
        string="Start Date",
        help="Start of the period of time during the encounter participant was present.")
    end_date = fields.Datetime(
        string="End Date",
        help="End of the period of time during the encounter participant was present.")
    individual_type = fields.Selection(
        string="Individual Type",
        selection=[
            ("practitioner", "Practitioner"),
            ("related_person", "Related Person")],
        help="Persons involved in the encounter other than the patient.")
    individual_name = fields.Char(
        string="Individual",
        compute="_compute_individual_name",
        store="True",
        help="Persons involved in the encounter other than the patient.")
    individual_practitioner_id = fields.Many2one(
        comodel_name="hc.res.practitioner",
        string="Individual Practitioner",
        help="Practitioner involved in the encounter other than the patient.")
    individual_related_person_id = fields.Many2one(
        comodel_name="hc.res.related.person",
        string="Individual Related Person",
        help="Related Person involved in the encounter other than the patient.")

class EncounterDiagnosis(models.Model):
    _name = "hc.encounter.diagnosis"
    _description = "Encounter Diagnosis"

    encounter_id = fields.Many2one(
        comodel_name="hc.res.encounter",
        string="Encounter",
        help="Encounter associated with this Encounter Diagnosis.")
    condition_type = fields.Selection(
        string="Condition Type",
        required="True",
        selection=[
            ("condition", "Condition")],
        help="Type of reason the encounter takes place (resource).")
    condition_name = fields.Char(
        string="Condition",
        compute="_compute_condition_name",
        store="True",
        help="Reason the encounter takes place (resource).")
    condition_condition_id = fields.Many2one(
        comodel_name="hc.res.condition",
        string="Condition Condition",
        help="Condition reason the encounter takes place (resource).")
    # condition_procedure_id = fields.Many2one(
    #     comodel_name="hc.res.procedure",
    #     string="Condition Procedure",
    #     help="Procedure reason the encounter takes place (resource).")
    role_id = fields.Many2one(
        comodel_name="hc.vs.diagnosis.role",
        string="Role",
        help="Role that this diagnosis has within the encounter (e.g. admission, billing, discharge _).")
    rank = fields.Integer(
        string="Rank",
        help="Ranking of the diagnosis (for each role type).")

class EncounterHospitalization(models.Model):
    _name = "hc.encounter.hospitalization"
    _description = "Encounter Hospitalization"

    encounter_id = fields.Many2one(
        comodel_name="hc.res.encounter",
        string="Encounter",
        help="Encounter associated with this Encounter Hospitalization.")
    pre_admission_identifier_id = fields.Many2one(
        comodel_name="hc.encounter.hospitalization.pre.admission.identifier",
        string="Encounter Hospitalization Pre-Admission Identifier",
        help="Pre-admission identifier.")
    origin_id = fields.Many2one(
        comodel_name="hc.res.location",
        string="Origin",
        help="The location from which the patient came before admission.")
    admit_source_id = fields.Many2one(
        comodel_name="hc.vs.encounter.admit.source",
        string="Admit Source",
        help="From where patient was admitted (physician referral, transfer).")
    re_admission_id = fields.Many2one(
        comodel_name="hc.vs.v2.readmission.indicator",
        string="Re-Admission",
        help="The type of hospital re-admission that has occurred (if any). If the value is absent, then this is not identified as a readmission.")
    diet_preference_ids = fields.Many2many(
        comodel_name="hc.vs.encounter.diet",
        relation="encounter_hospitalization_diet_preference_rel",
        string="Diet Preferences",
        help="Diet preferences reported by the patient.")
    special_courtesy_ids = fields.Many2many(
        comodel_name="hc.vs.encounter.special.courtesy",
        relation="encounter_hospitalization_special_courtesy_rel",
        string="Special Courtesies",
        help="Special courtesies (VIP, board member).")
    special_arrangement_ids = fields.Many2many(
        comodel_name="hc.vs.encounter.special.arrangements",
        relation="encounter_hospitalization_special_arrangement_rel",
        string="Special Arrangements",
        help="Wheelchair, translator, stretcher, etc.")
    destination_id = fields.Many2one(
        comodel_name="hc.res.location",
        string="Destination",
        help="Location to which the patient is discharged.")
    discharge_disposition_id = fields.Many2one(
        comodel_name="hc.vs.encounter.discharge.disposition",
        string="Discharge Disposition",
        help="Category or kind of location after discharge.")

class EncounterLocation(models.Model):
    _name = "hc.encounter.location"
    _description = "Encounter Location"

    encounter_id = fields.Many2one(
        comodel_name="hc.res.encounter",
        string="Encounter",
        help="Encounter associated with this Encounter Location.")
    location_id = fields.Many2one(
        comodel_name="hc.res.location",
        string="Location",
        required="True",
        help="Location the encounter takes place.")
    status = fields.Selection(
        string="Location Status",
        selection=[
            ("planned", "Planned"),
            ("present", "Present"),
            ("reserved", "Reserved"),
            ("completed", "Completed")],
        help="The status of the participants' presence at the specified location during the period specified.")
    start_date = fields.Datetime(
        string="Start Date",
        help="Start of the time period during which the patient was present at the location.")
    end_date = fields.Datetime(
        string="End Date",
        help="End of the time period during which the patient was present at the location.")
    status_history_ids = fields.One2many(
        comodel_name="hc.encounter.location.status.history",
        inverse_name="location_id",
        string="Location Status History",
        help="List of Encounter Location statuses.")

class EncounterLocationStatusHistory(models.Model):
    _name = "hc.encounter.location.status.history"
    _description = "Encounter Location Status History"

    location_id = fields.Many2one(
        comodel_name="hc.encounter.location",
        string="Location",
        help="List of locations the patient has been at.")
    status = fields.Char(
        string="Status",
        help="The status of the encounter location.")
    start_date = fields.Datetime(
        string="Start Date",
        help="Start of the the time that the episode was in the specified class.")
    end_date = fields.Datetime(
        string="End Date",
        help="End of the the time that the episode was in the specified class.")
    time_diff_day = fields.Char(
        string="Time Diff (days)",
        help="Days duration of the status.")
    time_diff_hour = fields.Char(
        string="Time Diff (hours)",
        help="Hours duration of the status.")
    time_diff_min = fields.Char(
        string="Time Diff (minutes)",
        help="Minutes duration of the status.")
    time_diff_sec = fields.Char(
        string="Time Diff (seconds)",
        help="Seconds duration of the status.")

class EncounterIdentifier(models.Model):
    _name = "hc.encounter.identifier"
    _description = "Encounter Identifier"
    _inherit = ["hc.basic.association", "hc.identifier"]

    encounter_id = fields.Many2one(
        comodel_name="hc.res.encounter",
        string="Encounter",
        help="Encounter associated with this Encounter Identifier.")

class EncounterEpisodeOfCare(models.Model):
    _name = "hc.encounter.episode.of.care"
    _description = "Encounter Episode Of Care"
    _inherit = ["hc.basic.association"]

    encounter_id = fields.Many2one(
        comodel_name="hc.res.encounter",
        string="Encounter",
        help="Encounter associated with this Encounter Episode Of Care.")
    episode_of_care_id = fields.Many2one(
        comodel_name="hc.res.episode.of.care",
        string="Episode Of Care",
        help="Episode Of Care associated with this Encounter Episode Of Care.")

class EncounterIncomingReferral(models.Model):
    _name = "hc.encounter.incoming.referral"
    _description = "Encounter Incoming Referral"
    _inherit = ["hc.basic.association"]

    encounter_id = fields.Many2one(
        comodel_name="hc.res.encounter",
        string="Encounter",
        help="Encounter associated with this Encounter Incoming Referral.")
    # incoming_referral_id = fields.Many2one(
    #     comodel_name="hc.res.procedure.request",
    #     string="Incoming Referral",
    #     help="Procedure Request associated with this Encounter Incoming Referral.")

class EncounterAccount(models.Model):
    _name = "hc.encounter.account"
    _description = "Encounter Account"
    _inherit = ["hc.basic.association"]

    encounter_id = fields.Many2one(
        comodel_name="hc.res.encounter",
        string="Encounter",
        help="Encounter associated with this Encounter Account.")
    account_id = fields.Many2one(
        comodel_name="hc.res.account",
        string="Account",
        help="Account associated with this Encounter Account.")

class EncounterHospitalizationPreAdmissionIdentifier(models.Model):
    _name = "hc.encounter.hospitalization.pre.admission.identifier"
    _description = "Encounter Hospitalization Pre-Admission Identifier"
    _inherit = ["hc.basic.association", "hc.identifier"]

class ActEncounterCode(models.Model):
    _name = "hc.vs.act.encounter.code"
    _description = "Act Encounter Code"
    _inherit = ["hc.value.set.contains"]

class EncounterType(models.Model):
    _name = "hc.vs.encounter.type"
    _description = "Encounter Type"
    _inherit = ["hc.value.set.contains"]

class ActPriority(models.Model):
    _name = "hc.vs.act.priority"
    _description = "Act Priority"
    _inherit = ["hc.value.set.contains"]

class EncounterAdmitSource(models.Model):
    _name = "hc.vs.encounter.admit.source"
    _description = "Encounter Admit Source"
    _inherit = ["hc.value.set.contains"]

class EncounterType(models.Model):
    _name = "hc.vs.encounter.type"
    _description = "Encounter Type"
    _inherit = ["hc.value.set.contains"]

class EncounterDiet(models.Model):
    _name = "hc.vs.encounter.diet"
    _description = "Encounter Diet"
    _inherit = ["hc.value.set.contains"]

class EncounterSpecialCourtesy(models.Model):
    _name = "hc.vs.encounter.special.courtesy"
    _description = "Encounter Special Courtesy"
    _inherit = ["hc.value.set.contains"]

class V2ReadmissionIndicator(models.Model):
    _name = "hc.vs.v2.readmission.indicator"
    _description = "V2 Readmission Indicator"
    _inherit = ["hc.value.set.contains"]

class EncounterSpecialArrangements(models.Model):
    _name = "hc.vs.encounter.special.arrangements"
    _description = "Encounter Special Arrangements"
    _inherit = ["hc.value.set.contains"]

class EncounterDischargeDisposition(models.Model):
    _name = "hc.vs.encounter.discharge.disposition"
    _description = "Encounter Discharge Disposition"
    _inherit = ["hc.value.set.contains"]

# External Reference

class Condition(models.Model):
    _inherit = "hc.res.condition"

    context_type = fields.Selection(
        string="Condition Context Type",
        selection_add=[
            ("encounter", "Encounter")],
        help="Type of encounter when condition first asserted.")
    context_encounter_id = fields.Many2one(
        comodel_name="hc.res.encounter",
        string="Context Encounter",
        help="Encounter when condition first asserted.")

    @api.multi
    def _compute_context_name(self):
        for hc_res_condition in self:
            if hc_res_condition.context_type == 'encounter':
                hc_res_condition.context_name = hc_res_condition.context_encounter_id.name
            elif hc_res_condition.context_type == 'episode_of_care':
                hc_res_condition.context_name = hc_res_condition.context_episode_of_care_id.name