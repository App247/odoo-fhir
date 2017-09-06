# -*- coding: utf-8 -*-

from openerp import models, fields, api

class ImmunizationRecommendation(models.Model):
    _name = "hc.res.immunization.recommendation"
    _description = "Immunization Recommendation"

    name = fields.Char(
        string="Event Name",
        compute="_compute_name",
        store="True",
        help="Text representation of the immunization recommendation event. Patient + Recommendation + Date.")
    identifier_ids = fields.One2many(
        comodel_name="hc.immunization.rec.identifier",
        inverse_name="immunization_recommendation_id",
        string="Identifiers",
        help="Business identifier.")
    patient_id = fields.Many2one(
        comodel_name="hc.res.patient",
        string="Patient",
        required="True",
        help="Who this profile is for.")
    recommendation_ids = fields.One2many(
        comodel_name="hc.immunization.rec.rec",
        inverse_name="immunization_recommendation_id",
        string="Recommendations",
        required="True",
        help="Vaccine administration recommendations.")

class ImmunizationRecRec(models.Model):
    _name = "hc.immunization.rec.rec"
    _description = "Immunization Recommendation Recommendation"

    immunization_recommendation_id = fields.Many2one(
        comodel_name="hc.res.immunization.recommendation",
        string="Immunization Recommendation",
        help="Immunization Recommendation associated with this recommendation.")
    date = fields.Datetime(
        string="Created Date",
        required="True",
        help="Date recommendation created.")
    vaccine_code_id = fields.Many2one(
        comodel_name="hc.vs.vaccine.code",
        string="Vaccine Code",
        required="True",
        help="Vaccine recommendation applies to")
    dose_number = fields.Integer(
        string="Dose Number",
        help="Recommended dose number.")
    forecast_status_id = fields.Many2one(
        comodel_name="hc.vs.immunization.rec.status",
        string="Forecast Status",
        required="True",
        help="Vaccine administration status.")
    identifier_ids = fields.One2many(
        comodel_name="hc.immunization.rec.rec.identifier",
        inverse_name="immunization_rec_rec_id",
        string="Identifiers",
        help="Past immunizations supporting recommendation.")
    supporting_patient_info_type = fields.Selection(
        string="Supporting Patient Info Type",
        selection=[
            ("observation", "Observation"),
            ("allergy_intolerance", "Allergy Intolerance")],
        help="Type of patient observations supporting recommendation.")
    supporting_patient_info_name = fields.Text(
        string="Supporting Patient Info",
        compute="_compute_supporting_patient_info_name",
        store="True",
        help="Patient observations supporting recommendation.")
    supporting_patient_info_observation_id = fields.Many2one(
        comodel_name="hc.res.observation",
        string="Supporting Patient Info Observation",
        help="Observation associated with this recommendation.")
    supporting_patient_info_allergy_intolerance_id = fields.Many2one(
        comodel_name="hc.res.allergy.intolerance",
        string="Supporting Patient Info Allergy Intolerance",
        help="Allergy Intolerance associated with this recommendation.")
    date_criterion_ids = fields.One2many(
        comodel_name="hc.immunization.rec.rec.date.criterion",
        inverse_name="immunization_rec_rec_id",
        string="Date Criterions",
        help="Dates governing proposed immunization.")
    protocol_ids = fields.One2many(
        comodel_name="hc.immunization.rec.rec.protocol",
        inverse_name="immunization_rec_rec_id",
        string="Protocols",
        help="Protocol used by recommendation.")

class ImmunizationRecRecDateCriterion(models.Model):
    _name = "hc.immunization.rec.rec.date.criterion"
    _description = "Immunization Recommendation Recommendation Date Criterion"

    immunization_rec_rec_id = fields.Many2one(
        comodel_name="hc.immunization.rec.rec",
        string="Immunization Recommendation Recommendation",
        help="Recommendation associated with this date criterion.")
    code_id = fields.Many2one(
        comodel_name="hc.vs.immunization.rec.date.criterion",
        string="Code",
        required="True",
        help="Type of date.")
    value = fields.Datetime(
        string="Value Date",
        required="True",
        help="Recommended date.")

class ImmunizationRecRecProtocol(models.Model):
    _name = "hc.immunization.rec.rec.protocol"
    _description = "Immunization Recommendation Recommendation Protocol"

    immunization_rec_rec_id = fields.Many2one(
        comodel_name="hc.immunization.rec.rec",
        string="Immunization Recommendation Recommendation",
        help="Recommendation associated with this protocol.")
    dose_sequence = fields.Integer(
        string="Dose Sequence",
        help="Dose number within sequence.")
    description = fields.Text(
        string="Description",
        help="Protocol details.")
    authority_id = fields.Many2one(
        comodel_name="hc.res.organization",
        string="Authority",
        help="Who is responsible for protocol.")
    series = fields.Char(
        string="Series",
        help="Name of vaccination series.")

class ImmunizationRecIdentifier(models.Model):
    _name = "hc.immunization.rec.identifier"
    _description = "Immunization Recommendation Identifier"
    _inherit = ["hc.basic.association", "hc.identifier"]

    immunization_recommendation_id = fields.Many2one(
        comodel_name="hc.res.immunization.recommendation",
        string="Immunization Recommendation",
        help="Immunization Recommendation associated with this immunization Recommendation identifier.")

class ImmunizationRecRecIdentifier(models.Model):
    _name = "hc.immunization.rec.rec.identifier"
    _description = "Immunization Recommendation Recommendation Identifier"
    _inherit = ["hc.basic.association", "hc.identifier"]

    immunization_rec_rec_id = fields.Many2one(
        comodel_name="hc.immunization.rec.rec",
        string="Immunization Recommendation Recommendation",
        elp="Recommendation associated with this Immunization Recommendation Recommendation Identifier.")

class ImmunizationRecDateCriterion(models.Model):
    _name = "hc.vs.immunization.rec.date.criterion"
    _description = "Immunization Recommendation Date Criterion"
    _inherit = ["hc.value.set.contains"]

class ImmunizationRecStatus(models.Model):
    _name = "hc.vs.immunization.rec.status"
    _description = "Immunization Recommendation Status"
    _inherit = ["hc.value.set.contains"]

# External Reference

class ObservationBasedOn(models.Model):
    _inherit = "hc.observation.based.on"

    based_on_type = fields.Selection(
        string="Based On Type",
        selection_add=[
            ("immunization_recommendation", "Immunization Recommendation")])
    based_on_immunization_recommendation_id = fields.Many2one(
        comodel_name="hc.res.immunization.recommendation",
        string="Based On Immunization Recommendation",
        help="Immunization Recommendation fulfills plan, proposal or order.")

    @api.depends('based_on_type')
    def _compute_based_on_name(self):
        for hc_observation_based_on in self:
            if hc_observation_based_on.based_on_type == 'immunization_recommendation':
                hc_observation_based_on.based_on_name = hc_observation_based_on.based_on_immunization_recommendation_id.name
