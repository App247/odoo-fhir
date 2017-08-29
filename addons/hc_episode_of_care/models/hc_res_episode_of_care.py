# -*- coding: utf-8 -*-

from openerp import models, fields, api

class EpisodeOfCare(models.Model):
    _name = "hc.res.episode.of.care"
    _description = "Episode Of Care"

    name = fields.Char(
        string="Name",
        compute="_compute_name",
        store="True",
        help="Text representation of the episode of care event. Patient Name + Episode of Care Type + Start Date.")
    identifier_ids = fields.One2many(
        comodel_name="hc.episode.of.care.identifier",
        inverse_name="episode_of_care_id",
        string="Identifiers",
        help="Identifier(s) by which this Episode of Care is known.")
    status = fields.Selection(
        string="Episode Of Care Status",
        required="True",
        selection=[
            ("planned", "Planned"),
            ("waitlist", "Waitlist"),
            ("active", "Active"),
            ("onhold", "On hold"),
            ("finished", "Finished"),
            ("cancelled", "Cancelled")],
        help="The status of the episode of care.")
    type_ids = fields.Many2many(
        comodel_name="hc.vs.episode.of.care.type",
        inverse_name="",
        string="Types",
        help="Specific type of Episode of Care.")
    condition_ids = fields.One2many(
        comodel_name="hc.episode.of.care.condition",
        inverse_name="episode_of_care_id",
        string="Conditions", help="Conditions/problems/diagnoses this episode of care is for.")
    patient_id = fields.Many2one(
        comodel_name="hc.res.patient",
        string="Patient",
        required="True",
        help="The patient that this Episode of CaEe applies to.")
    managing_organization_id = fields.Many2one(
        comodel_name="hc.res.organization",
        string="Managing Organization",
        help="Organization that assumes care.")
    start_date = fields.Datetime(
        string="Start Date",
        help="Start of the interval during responsibility is assumed.")
    end_date = fields.Datetime(
        string="End Date",
        help="End of the interval during responsibility is assumed.")
    referral_request_ids = fields.One2many(
        comodel_name="hc.episode.of.care.referral.request",
        inverse_name="episode_of_care_id",
        string="Referral Requests",
        help="Originating Referral Request(s).")
    care_manager_id = fields.Many2one(
        comodel_name="hc.res.practitioner",
        string="Care Manager",
        help="Care manager/care co-ordinator for the patient.")
    team_ids = fields.One2many(
        comodel_name="hc.episode.of.care.team",
        inverse_name="episode_of_care_id",
        string="Teams",
        help="Other practitioners facilitating this episode of care.")
    account_ids = fields.One2many(
        comodel_name="hc.episode.of.care.account",
        inverse_name="episode_of_care_id",
        string="Accounts",
        help="The set of accounts that may be used for billing for this Episode of Care.")
    status_history_ids = fields.One2many(
        comodel_name="hc.episode.of.care.status.history",
        inverse_name="episode_of_care_id",
        string="Status Histories",
        help="The status history for the Episode of Care.")
    diagnosis_ids = fields.One2many(
        comodel_name="hc.episode.of.care.diagnosis",
        inverse_name="episode_of_care_id",
        string="Diagnosis",
        help="The list of diagnosis relevant to this episode of care.")

class EpisodeOfCareStatusHistory(models.Model):
    _name = "hc.episode.of.care.status.history"
    _description = "Episode Of Care Status History"

    episode_of_care_id = fields.Many2one(
        comodel_name="hc.res.episode.of.care",
        string="Episode Of Care",
        required="True",
        help="Episode Of Care associated with this Episode Of Care Status History.")
    status = fields.Selection(
        string="Status History Status",
        required="True",
        selection=[
            ("planned", "Planned"),
            ("waitlist", "Waitlist"),
            ("active", "Active"),
            ("onhold", "On hold"),
            ("finished", "Finished"),
            ("cancelled", "Cancelled")],
        help="The status of the episode of care.")
    start_date = fields.Datetime(
        string="Start Date",
        required="True",
        help="Start of the the period during this episode of care that the specific status applied.")
    end_date = fields.Datetime(
        string="End Date",
        required="True",
        help="End of the the period during this episode of care that the specific status applied.")

class EpisodeOfCareDiagnosis(models.Model):
    _name = "hc.episode.of.care.diagnosis"
    _description = "Episode Of Care Diagnosis"

    episode_of_care_id = fields.Many2one(
        comodel_name="hc.res.episode.of.care",
        string="Episode Of Care",
        help="Episode Of Care associated with this Episode Of Care Diagnosis.")
    condition_id = fields.Many2one(
        comodel_name="hc.res.condition",
        string="Condition",
        required="True",
        help="Conditions/problems/diagnoses this episode of care is for.")
    role_id = fields.Many2one(
        comodel_name="hc.vs.diagnosis.role",
        string="Role",
        help="Role that this diagnosis has within the episode of care (e.g. admission, billing, discharge _).")
    rank = fields.Integer(
        string="Rank",
        help="Ranking of the diagnosis (for each role type).")

class EpisodeOfCareIdentifier(models.Model):
    _name = "hc.episode.of.care.identifier"
    _description = "Episode Of Care Identifier"
    _inherit = ["hc.basic.association", "hc.identifier"]

    episode_of_care_id = fields.Many2one(
        comodel_name="hc.res.episode.of.care",
        string="Episode Of Care",
        required="True",
        help="Episode Of Care associated with this Episode Of Care Identifier.")

class EpisodeOfCareCondition(models.Model):
    _name = "hc.episode.of.care.condition"
    _description = "Episode Of Care Condition"
    _inherit = ["hc.basic.association"]

    episode_of_care_id = fields.Many2one(
        comodel_name="hc.res.episode.of.care",
        string="Episode Of Care",
        required="True",
        help="Episode Of Care associated with this Episode Of Care Condition.")
    condition_id = fields.Many2one(
        comodel_name="hc.res.condition",
        string="Condition",
        help="Condition associated with this Episode Of Care Condition.")

class EpisodeOfCareAccount(models.Model):
    _name = "hc.episode.of.care.account"
    _description = "Episode Of Care Account"
    _inherit = ["hc.basic.association"]

    episode_of_care_id = fields.Many2one(
        comodel_name="hc.res.episode.of.care",
        string="Episode Of Care",
        required="True",
        help="Episode Of Care associated with this Episode Of Care Account.")
    account_id = fields.Many2one(
        comodel_name="hc.res.account",
        string="Account",
        help="Account associated with this Episode Of Care Account.")

class EpisodeOfCareReferralRequest(models.Model):
    _name = "hc.episode.of.care.referral.request"
    _description = "Episode Of Care Referral Request"
    _inherit = ["hc.basic.association"]

    episode_of_care_id = fields.Many2one(
        comodel_name="hc.res.episode.of.care",
        string="Episode Of Care",
        required="True",
        help="Episode Of Care associated with this Episode Of Care Referral Request.")
    # referral_request_id = fields.Many2one(
    #     comodel_name="hc.res.procedure.request",
    #     string="Referral Request",
    #     required="True",
    #     help="Procedure Request associated with this Episode Of Care Referral Request.")

class EpisodeOfCareTeam(models.Model):
    _name = "hc.episode.of.care.team"
    _description = "Episode Of Care Team"
    _inherit = ["hc.basic.association"]

    episode_of_care_id = fields.Many2one(
        comodel_name="hc.res.episode.of.care",
        string="Episode Of Care",
        required="True",
        help="Episode Of Care associated with this Episode Of Care Team.")
    team_id = fields.Many2one(
        comodel_name="hc.res.care.team",
        string="Team",
        required="True",
        help="Care Team associated with this Episode Of Care Team.")

class EpisodeOfCareType(models.Model):
    _name = "hc.vs.episode.of.care.type"
    _description = "Episode of Care Type"
    _inherit = ["hc.value.set.contains"]

class DiagnosisRole(models.Model):
    _name = "hc.vs.diagnosis.role"
    _description = "Diagnosis Role"
    _inherit = ["hc.value.set.contains"]

# External Reference

class Condition(models.Model):
    _inherit = "hc.res.condition"

    context_type = fields.Selection(
        string="Condition Context Type",
        selection=[
            ("episode_of_care", "Episode of Care")],
        help="Type of encounter when condition first asserted.")
    context_name = fields.Char(
        string="Context",
        compute="_compute_context_name",
        store="True",
        help="Encounter when condition first asserted.")
    context_episode_of_care_id = fields.Many2one(
        comodel_name="hc.res.episode.of.care",
        string="Context Episode Of Care",
        help="Episode Of Care when condition first asserted.")

    @api.multi
    def _compute_context_name(self):
        for hc_res_condition in self:
            if hc_res_condition.context_type == 'episode_of_care':
                hc_res_condition.context_name = hc_res_condition.context_episode_of_care_id.name
            # elif hc_res_condition.context_type == 'encounter':
            #     hc_res_condition.context_name = hc_res_condition.context_encounter_id.name
