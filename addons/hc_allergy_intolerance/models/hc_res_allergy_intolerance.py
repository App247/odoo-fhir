# -*- coding: utf-8 -*-

from openerp import models, fields, api
from datetime import datetime
from openerp.tools import DEFAULT_SERVER_DATE_FORMAT as DF
from openerp.tools import DEFAULT_SERVER_DATETIME_FORMAT as DTF

class AllergyIntolerance(models.Model):
    _name = "hc.res.allergy.intolerance"
    _description = "Allergy Intolerance"
    _inherit = ["hc.domain.resource"]
    _rec_name = "name"

    name = fields.Char(
        string="Event Name",
        compute="_compute_name",
        store="True",
        help="Text representation of the allergy intolerance event. Patient + DOB + Allergy + Asserted Date.")
    identifier_ids = fields.One2many(
        comodel_name="hc.allergy.intolerance.identifier",
        inverse_name="allergy_intolerance_id",
        string="Identifiers",
        help="External IDs for the allergy.")
    clinical_status = fields.Selection(
        string="Clinical Status",
        selection=[
            ("draft", "Draft"),
            ("active", "Active"),
            ("resolved", "Resolved")],
        help="The clinical status of the allergy or intolerance.")
    clinical_status_history_ids = fields.One2many(
        comodel_name="hc.allergy.intolerance.clinical.status.history",
        inverse_name="allergy_intolerance_id",
        string="Clinical Status History",
        help="The clinical status of the allergy or intolerance over time.")
    verification_status = fields.Selection(
        string="Verification Status",
        required="True",
        selection=[
            ("unconfirmed", "Unconfirmed"),
            ("confirmed", "Confirmed"),
            ("refuted", "Refuted"),
            ("entered-in-error", "Entered-In-Error")],
        default="unconfirmed",
        help="Assertion about certainty associated with the propensity, or potential risk, of a reaction to the identified substance (including pharmaceutical product).")
    verification_status_history_ids = fields.One2many(
        comodel_name="hc.allergy.intolerance.verification.status.history",
        inverse_name="allergy_intolerance_id",
        string="Verification Status History",
        help="The verification status of the allergy or intolerance over time.")
    type = fields.Selection(
        string="Type",
        selection=[
            ("allergy", "Allergy"),
            ("intolerance", "Intolerance")],
        default="allergy",
        help="Identification of the underlying physiological mechanism for a Reaction Risk.")
    category_ids = fields.One2many(
        comodel_name="hc.allergy.intolerance.category",
        inverse_name="allergy_intolerance_id",
        string="Categories",
        help="Category of the identified substance.")
    criticality = fields.Selection(
        string="Criticality",
        selection=[
            ("low", "Low"),
            ("high", "High"),
            ("unable-to-assess", "Unable to Assess")],
        default="low",
        help="Estimate of the potential clinical harm, or seriousness, of a reaction to an identified Substance.")
    code_id = fields.Many2one(
        comodel_name="hc.vs.allergy.intolerance.code",
        required="True",
        string="Allergy/Intolerance",
        help="Allergy or intolerance.")
    code = fields.Char(
        string="Code",
        related="code_id.code",
        help="Allergy or intolerance code.")
    patient_id = fields.Many2one(
        comodel_name="hc.res.patient",
        string="Patient",
        required="True",
        help="Patient who the sensitivity is for.")
    onset_type = fields.Selection(
        string="Onset Type",
        selection=[
            ("date_time", "Date Time"),
            ("age", "Age"),
            ("period", "Period"),
            ("range", "Range"),
            ("string", "String")],
        help="Type of when allergy or intolerance was identified.")
    onset_name = fields.Char(
        string="Onset",
        compute="_compute_onset_name",
        store="True",
        help="When allergy or intolerance was identified.")
    onset_date_time = fields.Datetime(
        string="Onset Datetime",
        help="Date Time when allergy or intolerance was identified.")
    onset_age = fields.Integer(
        string="Onset Age",
        size=3,
        help="Age when allergy or intolerance was identified.")
    onset_age_uom_id = fields.Many2one(
        comodel_name="product.uom",
        string="Onset Age UOM",
        domain="[('category_id','=','Time (UCUM)')]",
        default="a",
        help="Onset age unit of measure.")
    onset_start_date = fields.Datetime(
        string="Onset Start Date",
        help="Start of when allergy or intolerance was identified.")
    onset_end_date = fields.Datetime(
        string="Onset End Date",
        help="End of when allergy or intolerance was identified.")
    onset_range_low = fields.Float(
        string="Onset Range Low",
        help="Low limit of range when allergy or intolerance was identified.")
    onset_range_high = fields.Float(
        string="Onset Range High",
        help="High limit of range when allergy or intolerance was identified.")
    onset_string = fields.Char(
        string="Onset String",
        help="String of when allergy or intolerance was identified.")
    asserted_date = fields.Datetime(
        string="Asserted Date",
        required="True",
        default=fields.datetime.now(),
        help="Date record was believed accurate.")
    recorder_type = fields.Selection(
        string="Recorder Type",
        selection=[
            ("practitioner", "Practitioner"),
            ("patient", "Patient")],
        help="Type of individual who recorded the sensitivity.")
    recorder_name = fields.Char(
        string="Recorder",
        compute="_compute_recorder_name",
        store="True",
        help="Individual who recorded the sensitivity.")
    recorder_practitioner_id = fields.Many2one(
        comodel_name="hc.res.practitioner",
        string="Recorder Practitioner",
        help="Practitioner who recorded the sensitivity.")
    recorder_patient_id = fields.Many2one(
        comodel_name="hc.res.patient",
        string="Recorder Patient",
        help="Patient who recorded the sensitivity.")
    asserter_type = fields.Selection(
        string="Asserter Type",
        selection=[
            ("patient", "Patient"),
            ("related_person", "Related Person"),
            ("practitioner", "Practitioner")],
        help="Type of source of the information about the allergy.")
    asserter_name = fields.Char(
        string="Asserter",
        compute="_compute_asserter_name",
        store="True",
        help="Source of the information about the allergy.")
    asserter_patient_id = fields.Many2one(
        comodel_name="hc.res.patient",
        string="Asserter Patient",
        help="Patient source of the information about the allergy.")
    asserter_related_person_id = fields.Many2one(
        comodel_name="hc.res.related.person",
        string="Asserter Related Person",
        help="Related Person source of the information about the allergy.")
    asserter_practitioner_id = fields.Many2one(
        comodel_name="hc.res.practitioner",
        string="Asserter Practitioner",
        help="Practitioner source of the information about the allergy.")
    last_occurence = fields.Datetime(
        string="Last Occurence Date",
        help="Date(/time) of last known occurence of a reaction.")
    note_ids = fields.One2many(
        comodel_name="hc.allergy.intolerance.note",
        inverse_name="allergy_intolerance_id",
        string="Notes",
        help="Additional text (i.e., comment, explanation) not captured in other fields.")
    reaction_ids = fields.One2many(
        comodel_name="hc.allergy.intolerance.reaction",
        inverse_name="allergy_intolerance_id",
        string="Reactions",
        help="Adverse Reaction Events linked to exposure to substance.")

    @api.one
    @api.depends('patient_id', 'code_id', 'asserted_date')
    def _compute_name(self):
        comp_name = '/'
        for hc_res_allergy_intolerance in self:
            if hc_res_allergy_intolerance.patient_id:
                comp_name = hc_res_allergy_intolerance.patient_id.name
                if hc_res_allergy_intolerance.patient_id.birth_date:
                    patient_birth_date = datetime.strftime(datetime.strptime(hc_res_allergy_intolerance.patient_id.birth_date, DF), "%Y-%m-%d")
                    comp_name = comp_name + "("+ patient_birth_date + ")"
            if hc_res_allergy_intolerance.code_id:
                comp_name = comp_name + ", " + hc_res_allergy_intolerance.code_id.name or ''
            if hc_res_allergy_intolerance.asserted_date:
                patient_asserted_date = datetime.strftime(datetime.strptime(hc_res_allergy_intolerance.asserted_date, DTF), "%Y-%m-%d")
                comp_name = comp_name + ", " + patient_asserted_date
            hc_res_allergy_intolerance.name = comp_name

    @api.depends('onset_type')
    def _compute_onset_name(self):
        for hc_res_allergy_intolerance in self:
            if hc_res_allergy_intolerance.onset_type == 'date_time':
                    hc_res_allergy_intolerance.onset_name = str(hc_res_allergy_intolerance.onset_date_time)
            elif hc_res_allergy_intolerance.onset_type == 'age':
                    hc_res_allergy_intolerance.onset_name = str(hc_res_allergy_intolerance.onset_age) + ' ' + str(hc_res_allergy_intolerance.onset_age_uom_id.name) + "s old"
            elif hc_res_allergy_intolerance.onset_type == 'period':
                    hc_res_allergy_intolerance.onset_name = 'Between ' + str(hc_res_allergy_intolerance.onset_start_date) + ' and ' + str(hc_res_allergy_intolerance.onset_end_date)
            elif hc_res_allergy_intolerance.onset_type == 'range':
                    hc_res_allergy_intolerance.onset_name = 'Between ' + str(hc_res_allergy_intolerance.onset_range_low) + ' and ' + str(hc_res_allergy_intolerance.onset_range_high)
            elif hc_res_allergy_intolerance.onset_type == 'string':
                    hc_res_allergy_intolerance.onset_name = hc_res_allergy_intolerance.onset_string

    @api.depends('recorder_type')
    def _compute_recorder_name(self):
        for hc_res_allergy_intolerance in self:
            if hc_res_allergy_intolerance.recorder_type == 'practitioner':
                hc_res_allergy_intolerance.recorder_name = hc_res_allergy_intolerance.recorder_practitioner_id.name
            elif hc_res_allergy_intolerance.recorder_type == 'patient':
                hc_res_allergy_intolerance.recorder_name = hc_res_allergy_intolerance.recorder_patient_id.name

    @api.depends('asserter_type')
    def _compute_asserter_name(self):
        for hc_res_allergy_intolerance in self:
            if hc_res_allergy_intolerance.asserter_type == 'patient':
                hc_res_allergy_intolerance.asserter_name = hc_res_allergy_intolerance.asserter_patient_id.name
            elif hc_res_allergy_intolerance.asserter_type == 'related_person':
                hc_res_allergy_intolerance.asserter_name = hc_res_allergy_intolerance.asserter_related_person_id.name
            elif hc_res_allergy_intolerance.asserter_type == 'practitioner':
                hc_res_allergy_intolerance.asserter_name = hc_res_allergy_intolerance.asserter_practitioner_id.name

    @api.model
    def create(self, vals):
        clinical_status_history_obj = self.env['hc.allergy.intolerance.clinical.status.history']
        verification_status_history_obj = self.env['hc.allergy.intolerance.verification.status.history']
        res = super(AllergyIntolerance, self).create(vals)

        # For Verification Status
        if vals and vals.get('verification_status'):
            verification_status_history_vals = {
                'allergy_intolerance_id': res.id,
                'verification_status': res.verification_status,
                'start_date': datetime.today()
                }
            if vals.get('verification_status') == 'entered-in-error':
                verification_status_history_vals.update({'end_date': datetime.today()})
            verification_status_history_obj.create(verification_status_history_vals)

        # For Clinical Status
        if vals.get('verification_status') != 'entered-in-error':
            if vals and vals.get('clinical_status'):
                clinical_status_history_vals = {
                    'allergy_intolerance_id': res.id,
                    'clinical_status': res.clinical_status,
                    'start_date': datetime.today()
                    }
                clinical_status_history_obj.create(clinical_status_history_vals)

        return res

    @api.multi
    def write(self, vals):
        clinical_status_history_obj = self.env['hc.allergy.intolerance.clinical.status.history']
        verification_status_history_obj = self.env['hc.allergy.intolerance.verification.status.history']
        res = super(AllergyIntolerance, self).write(vals)

        # For Verification Status
        verification_status_history_record_ids = verification_status_history_obj.search([('end_date','=', False)])
        if verification_status_history_record_ids:
            if vals.get('verification_status') and verification_status_history_record_ids[0].verification_status != vals.get('verification_status'):
                for verification_status_history in verification_status_history_record_ids:
                    verification_status_history.end_date = datetime.strftime(datetime.today(), DTF)
                    time_diff = datetime.today() - datetime.strptime(verification_status_history.start_date, DTF)
                    if time_diff:
                        days = str(time_diff).split(',')
                        if days and len(days) > 1:
                            verification_status_history.time_diff_day = str(days[0])
                            times = str(days[1]).split(':')
                            if times and times > 1:
                                verification_status_history.time_diff_hour = str(times[0])
                                verification_status_history.time_diff_min = str(times[1])
                                verification_status_history.time_diff_sec = str(times[2])
                        else:
                            times = str(time_diff).split(':')
                            if times and times > 1:
                                verification_status_history.time_diff_hour = str(times[0])
                                verification_status_history.time_diff_min = str(times[1])
                                verification_status_history.time_diff_sec = str(times[2])
                verification_status_history_vals = {
                    'allergy_intolerance_id': self.id,
                    'verification_status': vals.get('verification_status'),
                    'start_date': datetime.today()
                    }
                if vals.get('verification_status') == 'entered-in-error':
                    verification_status_history_vals.update({'end_date': datetime.today()})
                verification_status_history_obj.create(verification_status_history_vals)

        # For Clinical Status
        clinical_status_history_record_ids = clinical_status_history_obj.search([('end_date','=', False)])
        if clinical_status_history_record_ids:
            if vals.get('verification_status') == 'entered-in-error' or (vals.get('clinical_status') and clinical_status_history_record_ids[0].clinical_status != vals.get('clinical_status')):
                for clinical_status_history in clinical_status_history_record_ids:
                    clinical_status_history.end_date = datetime.strftime(datetime.today(), DTF)
                    time_diff = datetime.today() - datetime.strptime(clinical_status_history.start_date, DTF)
                    if time_diff:
                        days = str(time_diff).split(',')
                        if days and len(days) > 1:
                            clinical_status_history.time_diff_day = str(days[0])
                            times = str(days[1]).split(':')
                            if times and times > 1:
                                clinical_status_history.time_diff_hour = str(times[0])
                                clinical_status_history.time_diff_min = str(times[1])
                                clinical_status_history.time_diff_sec = str(times[2])
                        else:
                            times = str(time_diff).split(':')
                            if times and times > 1:
                                clinical_status_history.time_diff_hour = str(times[0])
                                clinical_status_history.time_diff_min = str(times[1])
                                clinical_status_history.time_diff_sec = str(times[2])
                    clinical_status_history_vals = {
                        'allergy_intolerance_id': self.id,
                        'clinical_status': vals.get('clinical_status'),
                        'start_date': datetime.today()
                        }
                    if vals.get('verification_status') == 'entered-in-error':
                        clinical_status_history_vals.update({'end_date': datetime.today()})
                    if vals.get('verification_status') != 'entered-in-error':
                        clinical_status_history_obj.create(clinical_status_history_vals)
        else:
            clinical_status_history_vals = {
                    'allergy_intolerance_id': self.id,
                    'clinical_status': vals.get('clinical_status'),
                    'start_date': datetime.today()
                    }
            if vals.get('verification_status') == 'entered-in-error':
                    clinical_status_history_vals.update({'end_date': datetime.today()})
            clinical_status_history_obj.create(clinical_status_history_vals)

        return res

class AllergyIntoleranceReaction(models.Model):
    _name = "hc.allergy.intolerance.reaction"
    _description = "Allergy Intolerance Reaction"

    allergy_intolerance_id = fields.Many2one(
        comodel_name="hc.res.allergy.intolerance",
        string="Allergy Intolerance",
        help="Allergy intolerance.")
    substance_id = fields.Many2one(
        comodel_name="hc.vs.substance.code",
        string="Substance",
        help="Type of the substance.")
    certainty = fields.Selection(
        string="Reaction Certainty",
        selection=[
            ("unlikely", "Unlikely"),
            ("likely", "Likely"),
            ("confirmed", "Confirmed"),
            ("unknown", "Unknown")],
        help="Statement about the degree of clinical certainty that a Specific Substance was the cause of the Manifestation in a reaction event.")
    manifestation_ids = fields.Many2many(
        comodel_name="hc.vs.manifestation.code",
        string="Manifestations",
        required="True",
        help="Clinical symptoms and/or signs that are observed or associated with an Adverse Reaction Event.")
    description = fields.Text(
        string="Description",
        help="Description of the event as a whole.")
    onset = fields.Datetime(
        string="Onset Date",
        help="Date(/time) when manifestations showed.")
    duration = fields.Float(
        string="Duration",
        help="How long Manifestations persisted.")
    duration_uom_id = fields.Many2one(
        comodel_name="product.uom",
        string="Duration UOM",
        domain="[('category_id','=','Time (UCUM)')]",
        help="Duration unit of measure.")
    severity = fields.Selection(
        string="Reaction Severity",
        selection=[
            ("mild", "Mild"),
            ("moderate", "Moderate"),
            ("severe", "Severe")],
        help="Clinical assessment of the severity of a reaction event as a whole, potentially considering multiple different manifestations.")
    exposure_route_id = fields.Many2one(
        comodel_name="hc.vs.route.code",
        string="Exposure Route",
        help="The route or physiological path of administration of a therapeutic agent into or onto the body of a subject.")
    note_ids = fields.One2many(
        comodel_name="hc.allergy.intolerance.reaction.note",
        inverse_name="reaction_id",
        string="Notes",
        help="Text about event not captured in other fields.")

class AllergyIntoleranceIdentifier(models.Model):
    _name = "hc.allergy.intolerance.identifier"
    _description = "Allergy Intolerance Identifier"
    _inherit = ["hc.basic.association", "hc.identifier"]

    allergy_intolerance_id = fields.Many2one(
        comodel_name="hc.res.allergy.intolerance",
        string="Allergy Intolerance",
        help="Allergy Intolerance associated with this Allergy Intolerance Identifier.")

class AllergyIntoleranceNote(models.Model):
    _name = "hc.allergy.intolerance.note"
    _description = "Allergy Intolerance Note"
    _inherit = ["hc.basic.association", "hc.annotation"]

    allergy_intolerance_id = fields.Many2one(
        comodel_name="hc.res.allergy.intolerance",
        string="Allergy Intolerance",
        help="Allergy Intolerance associated with this Allergy Intolerance Note.")

class AllergyIntoleranceCategory(models.Model):
    _name = "hc.allergy.intolerance.category"
    _description = "Allergy Intolerance Category"
    _inherit = ["hc.basic.association"]

    allergy_intolerance_id = fields.Many2one(
        comodel_name="hc.res.allergy.intolerance",
        string="Allergy Intolerance",
        help="Allergy Intolerance associated with this Allergy Intolerance Category.")
    category = fields.Selection(
        string="Category",
        selection=[
            ("food", "Food"),
            ("medication", "Medication"),
            ("biologic", "Biologic"),
            ("environment", "Environment")],
        help="Category of the identified substance.")

class AllergyIntoleranceReactionNote(models.Model):
    _name = "hc.allergy.intolerance.reaction.note"
    _description = "Allergy Intolerance Reaction Note"
    _inherit = ["hc.basic.association", "hc.annotation"]

    reaction_id = fields.Many2one(
        comodel_name="hc.allergy.intolerance.reaction",
        string="Reaction",
        help="Reaction associated with this Allergy Intolerance Reaction Note.")

class AllergyIntoleranceClinicalStatusHistory(models.Model):
    _name = "hc.allergy.intolerance.clinical.status.history"
    _description = "Allergy Intolerance Clinical Status History"

    allergy_intolerance_id = fields.Many2one(
        comodel_name="hc.res.allergy.intolerance",
        string="Allergy Intolerance",
        help="Allergy Intolerance associated with this Allergy Intolerance Clinical Status History.")
    clinical_status = fields.Char(
        string="Clinical Status",
        help="The clinical status of the allergy or intolerance.")
    start_date = fields.Datetime(
        string="Start Date",
        help="Start of the period during which this clinical status is valid.")
    end_date = fields.Datetime(
        string="End Date",
        help="End of the period during which this clinical status is valid.")
    time_diff_day = fields.Char(
        string="Time Diff (days)",
        help="Days duration of the clinical status.")
    time_diff_hour = fields.Char(
        string="Time Diff (hours)",
        help="Hours duration of the clinical status.")
    time_diff_min = fields.Char(
        string="Time Diff (minutes)",
        help="Minutes duration of the clinical status.")
    time_diff_sec = fields.Char(
        string="Time Diff (seconds)",
        help="Seconds duration of the clinical status.")

class AllergyIntoleranceVerificationStatusHistory(models.Model):
    _name = "hc.allergy.intolerance.verification.status.history"
    _description = "Allergy Intolerance Verification Status History"

    allergy_intolerance_id = fields.Many2one(
        comodel_name="hc.res.allergy.intolerance",
        string="Allergy Intolerance",
        help="Allergy Intolerance associated with this Allergy Intolerance Verification Status History.")
    verification_status = fields.Char(
        string="Verification Status",
        help="The verification status of the allergy or intolerance.")
    start_date = fields.Datetime(
        string="Start Date",
        help="Start of the period during which this verification status is valid.")
    end_date = fields.Datetime(
        string="End Date",
        help="End of the period during which this verification status is valid.")
    time_diff_day = fields.Char(
        string="Time Diff (days)",
        help="Days duration of the verification status.")
    time_diff_hour = fields.Char(
        string="Time Diff (hours)",
        help="Hours duration of the verification status.")
    time_diff_min = fields.Char(
        string="Time Diff (minutes)",
        help="Minutes duration of the verification status.")
    time_diff_sec = fields.Char(
        string="Time Diff (seconds)",
        help="Seconds duration of the verification status.")

class AllergyIntoleranceCode(models.Model):
    _name = "hc.vs.allergy.intolerance.code"
    _description = "Allergy Intolerance Code"
    _inherit = ["hc.value.set.contains"]

    name = fields.Char(
        string="Name",
        help="Name of this allergy intolerance.")
    code = fields.Char(
        string="Code",
        help="Code of this allergy intolerance.")
    contains_id = fields.Many2one(
        comodel_name="hc.vs.allergy.intolerance.code",
        string="Parent",
        help="Parent concept.")

class ManifestationCode(models.Model):
    _name = "hc.vs.manifestation.code"
    _description = "Manifestation Code"
    _inherit = ["hc.value.set.contains"]

    name = fields.Char(
        string="Name",
        help="Name of this manifestation.")
    code = fields.Char(
        string="Code",
        help="Code of this manifestation.")
    contains_id = fields.Many2one(
        comodel_name="hc.vs.manifestation.code",
        string="Parent",
        help="Parent concept.")

# External Reference

class Patient(models.Model):
    _inherit = ["hc.res.patient"]

    allergy_intolerance_ids = fields.One2many(
        comodel_name="hc.res.allergy.intolerance",
        inverse_name="patient_id",
        string="Allergies/Intolerances",
        help="Allergies and intolerances of this patient.")
