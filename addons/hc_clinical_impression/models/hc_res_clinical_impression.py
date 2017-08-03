# -*- coding: utf-8 -*-

from openerp import models, fields, api
from datetime import datetime
from openerp.tools import DEFAULT_SERVER_DATE_FORMAT as DF
from openerp.tools import DEFAULT_SERVER_DATETIME_FORMAT as DTF

class ClinicalImpression(models.Model):
    _name = "hc.res.clinical.impression"
    _description = "Clinical Impression"

    name = fields.Char(
        string="Event Name",
        compute="_compute_name",
        store="True",
        help="Text representation of the clinical impression event. Subject Name + Clinical Impression + Date.")
    identifier_ids = fields.One2many(
        comodel_name="hc.clinical.impression.identifier",
        inverse_name="clinical_impression_id",
        string="Identifiers",
        help="Business identifier.")
    status = fields.Selection(
        string="Status",
        required="True",
        selection=[
            ("in-progress", "In Progress"),
            ("completed", "Completed"),
            ("entered-in-error", "Entered In Error")],
        help="Identifies the workflow status of the assessment.")
    status_history_ids = fields.One2many(
        comodel_name="hc.clinical.impression.status.history",
        inverse_name="clinical_impression_id",
        string="Status History",
        help="The status of the clinical impression over time.")
    code_id = fields.Many2one(
        comodel_name="hc.vs.clinical.impression.kind",
        string="Code",
        required="True",
        default=fields.datetime.now(),
        help="Kind of impression performed.")
    description = fields.Text(
        string="Description",
        help="Why/how the assessment was performed.")
    subject_type = fields.Selection(
        string="Subject Type",
        required="True",
        selection=[
            ("patient", "Patient"),
            ("group", "Group")],
        help="Type of entity assessed.")
    subject_name = fields.Char(
        string="Subject",
        compute="_compute_subject_name",
        store="True",
        help="Patient or group assessed.")
    subject_patient_id = fields.Many2one(
        comodel_name="hc.res.patient",
        string="Subject Patient",
        help="Patient assessed.")
    subject_group_id = fields.Many2one(
        comodel_name="hc.res.group",
        string="Subject Group",
        help="Group assessed.")
    context_type = fields.Selection(
        string="Context Type",
        selection=[
            ("encounter", "Encounter"),
            ("episode_of_care", "Episode Of Care")],
        help="Type of Encounter or Episode created from.")
    context_name = fields.Char(
        string="Context",
        compute="_compute_context_name",
        store="True",
        help="Encounter or Episode created from.")
    context_encounter_id = fields.Many2one(
        comodel_name="hc.res.encounter",
        string="Context Encounter",
        help="Encounter created from.")
    context_episode_of_care_id = fields.Many2one(
        comodel_name="hc.res.episode.of.care",
        string="Context Episode Of Care",
        help="Episode Of Care created from.")
    effective_type = fields.Selection(
        string="Effective Type",
        selection=[
            ("date_time", "Datetime"),
            ("period", "Period")],
        help="Type of time of assessment.")
    effective_name = fields.Char(
        string="Effective",
        compute="_compute_effective_name",
        store="True",
        help="Time of assessment.")
    effective_datetime = fields.Datetime(
        string="Effective Datetime",
        help="Datetime of assessment.")
    effective_start_date = fields.Datetime(
        string="Effective Start Date",
        help="Start of the time of assessment.")
    effective_end_date = fields.Datetime(
        string="Effective End Date",
        help="End of the time of assessment.")
    date = fields.Datetime(
        string="Date",
        required="True",
        default=fields.datetime.now(),
        help="When the assessment was documented.")
    assessor_id = fields.Many2one(
        comodel_name="hc.res.practitioner",
        string="Assessor",
        help="The clinician performing the assessment.")
    previous_id = fields.Many2one(
        comodel_name="hc.res.clinical.impression",
        string="Previous",
        help="Reference to last assessment.")
    problem_ids = fields.One2many(
        comodel_name="hc.clinical.impression.problem",
        inverse_name="clinical_impression_id",
        string="Problems",
        help="General assessment of patient state.")
    protocol_ids = fields.One2many(
        comodel_name="hc.clinical.impression.protocol",
        inverse_name="clinical_impression_id",
        string="Protocol URIs",
        help="URI of clinical protocol followed.")
    summary = fields.Text(
        string="Summary",
        help="Summary of the assessment.")
    prognosis_codeable_concept_ids = fields.Many2many(
        comodel_name="hc.vs.clinical.impression.prognosis",
        relation="clinical_impression_prognosis_codeable_concept_rel",
        string="Prognosis Codeable Concept",
        help="Estimate of likely outcome.")
    prognosis_reference_ids = fields.One2many(
        comodel_name="hc.clinical.impression.prognosis.reference",
        inverse_name="clinical_impression_id",
        string="Prognosis References",
        help="RiskAssessment expressing likely outcome.")
    action_ids = fields.One2many(
        comodel_name="hc.clinical.impression.action",
        inverse_name="clinical_impression_id",
        string="Actions",
        help="Actions taken during assessment.")
    note_ids = fields.One2many(
        comodel_name="hc.clinical.impression.note",
        inverse_name="clinical_impression_id",
        string="Notes",
        help="Comments made about the Clinical Impression.")
    investigation_ids = fields.One2many(
        comodel_name="hc.clinical.impression.investigation",
        inverse_name="clinical_impression_id",
        string="Investigation",
        help="One or more sets of investigations (signs, symptions, etc).")
    finding_ids = fields.One2many(
        comodel_name="hc.clinical.impression.finding",
        inverse_name="clinical_impression_id",
        string="Findings",
        help="Possible or likely findings and diagnoses.")

    @api.depends('subject_patient_id', 'subject_group_id', 'code_id', 'date')
    def _compute_name(self):
        comp_name = '/'
        for hc_res_clinical_impression in self:
            if hc_res_clinical_impression.subject_type == 'patient':
                comp_name = hc_res_clinical_impression.subject_patient_id.name
                if hc_res_clinical_impression.subject_patient_id.birth_date:
                    subject_patient_birth_date = datetime.strftime(datetime.strptime(hc_res_clinical_impression.subject_patient_id.birth_date, DF), "%Y-%m-%d")
                    comp_name = comp_name + "("+ subject_patient_birth_date + "),"
            if hc_res_clinical_impression.subject_type == 'group':
                comp_name = hc_res_clinical_impression.subject_group_id.name + ","
            if hc_res_clinical_impression.code_id:
                comp_name = comp_name + " " + hc_res_clinical_impression.code_id.name + "," or ''
            if hc_res_clinical_impression.date:
                patient_date = datetime.strftime(datetime.strptime(hc_res_clinical_impression.date, DTF), "%Y-%m-%d")
                comp_name = comp_name + " " + patient_date
            hc_res_clinical_impression.name = comp_name

    @api.depends('subject_type')
    def _compute_subject_name(self):
        for hc_res_clinical_impression in self:
            if hc_res_clinical_impression.subject_type == 'patient':
                hc_res_clinical_impression.subject_name = hc_res_clinical_impression.subject_patient_id.name
            elif hc_res_clinical_impression.subject_type == 'group':
                hc_res_clinical_impression.subject_name = hc_res_clinical_impression.subject_group_id.name

    @api.depends('effective_type')
    def _compute_effective_name(self):
        for hc_res_clinical_impression in self:
            if hc_res_clinical_impression.effective_type == 'datetime':
                hc_res_clinical_impression.effective_name = str(hc_res_clinical_impression.effective_datetime)
            elif hc_res_clinical_impression.effective_type == 'period':
                hc_res_clinical_impression.effective_name = 'Between' + str(hc_res_clinical_impression.effective_start_date) + ' and ' + str(hc_res_clinical_impression.effective_end_date)

    @api.depends('context_type')
    def _compute_context_name(self):
        for hc_res_clinical_impression in self:
            if hc_res_clinical_impression.context_type == 'encounter':
                hc_res_clinical_impression.context_name = hc_res_clinical_impression.context_encounter_id.name
            elif hc_res_clinical_impression.context_type == 'episode_of_care':
                hc_res_clinical_impression.context_name = hc_res_clinical_impression.context_episode_of_care_id.name

    @api.model
    def create(self, vals):
        status_history_obj = self.env['hc.clinical.impression.status.history']
        res = super(ClinicalImpression, self).create(vals)
        if vals and vals.get('status'):
            status_history_vals = {
                'clinical_impression_id': res.id,
                'status': res.status,
                'start_date': datetime.today()
                }
            if vals.get('status') == 'entered-in-error':
                status_history_vals.update({'end_date': datetime.today()})
            status_history_obj.create(status_history_vals)
        return res

    @api.multi
    def write(self, vals):
        status_history_obj = self.env['hc.clinical.impression.status.history']
        res = super(ClinicalImpression, self).write(vals)
        status_history_record_ids = status_history_obj.search([('end_date','=', False)])
        if status_history_record_ids:
            if vals.get('status') and status_history_record_ids[0].status != vals.get('status'):
                for status_history in status_history_record_ids:
                    status_history.end_date = datetime.strftime(datetime.today(), DTF)
                    time_diff = datetime.today() - datetime.strptime(status_history.start_date, DTF)
                    if time_diff:
                        days = str(time_diff).split(',')
                        if days and len(days) > 1:
                            status_history.time_diff_day = str(days[0])
                            times = str(days[1]).split(':')
                            if times and times > 1:
                                status_history.time_diff_hour = str(times[0])
                                status_history.time_diff_min = str(times[1])
                                status_history.time_diff_sec = str(times[2])
                        else:
                            times = str(time_diff).split(':')
                            if times and times > 1:
                                status_history.time_diff_hour = str(times[0])
                                status_history.time_diff_min = str(times[1])
                                status_history.time_diff_sec = str(times[2])
                status_history_vals = {
                    'clinical_impression_id': self.id,
                    'status': vals.get('status'),
                    'start_date': datetime.today()
                    }
                if vals.get('status') == 'entered-in-error':
                    status_history_vals.update({'end_date': datetime.today()})
                status_history_obj.create(status_history_vals)
        return res


class ClinicalImpressionAction(models.Model):
    _name = "hc.clinical.impression.action"
    _description = "Clinical Impression Action"
    _inherit = ["hc.basic.association"]

    clinical_impression_id = fields.Many2one(
        comodel_name="hc.res.clinical.impression",
        string="Clinical Impression",
        help="Clinical impression associated with this clinical impression action.")
    action_type = fields.Selection(
        string="Action Type",
        selection=[
            ("referral_request", "Referral Request"),
            ("procedure_request", "Procedure Request"),
            ("procedure", "Procedure"),
            ("medication_request", "Medication Request"),
            ("appointment", "Appointment")],
        help="Type of actions taken during assessment.")
    action_name = fields.Char(
        string="Action",
        compute="_compute_action_name",
        store="True",
        help="Actions taken during assessment.")
    action_referral_request_id = fields.Many2one(
        comodel_name="hc.res.referral.request",
        string="Action Referral Request",
        help="Referral Request actions taken during assessment.")
    action_procedure_request_id = fields.Many2one(
        comodel_name="hc.res.procedure.request",
        string="Action Procedure Request",
        help="Procedure Request actions taken during assessment.")
    action_procedure_id = fields.Many2one(
        comodel_name="hc.res.procedure",
        string="Action Procedure",
        domain="['|',('action_procedure_id.subject_patient_id','=',subject_patient_id), ('action_procedure_id.subject_group_id','=','subject_group_id')]",
        help="Procedure actions taken during assessment.")
    action_medication_request_id = fields.Many2one(
        comodel_name="hc.res.medication.request",
        string="Action Medication Request",
        help="Medication Request actions taken during assessment.")
    action_appointment_id = fields.Many2one(
        comodel_name="hc.res.appointment",
        string="Action Appointment",
        help="Appointment actions taken during assessment.")

    @api.depends('action_type')
    def _compute_action_name(self):
        for hc_res_clinical_impression in self:
            if hc_res_clinical_impression.action_type == 'procedure':
                hc_res_clinical_impression.action_name = hc_res_clinical_impression.action_procedure_id.name
            elif hc_res_clinical_impression.action_type == 'referral_request':
                hc_res_clinical_impression.action_name = hc_res_clinical_impression.action_referral_request_id.name
            elif hc_res_clinical_impression.action_type == 'procedure_request':
                hc_res_clinical_impression.action_name = hc_res_clinical_impression.action_procedure_request_id.name
            elif hc_res_clinical_impression.action_type == 'medication_request':
                hc_res_clinical_impression.action_name = hc_res_clinical_impression.action_medication_request_id.name
            elif hc_res_clinical_impression.action_type == 'appointment':
                hc_res_clinical_impression.action_name = hc_res_clinical_impression.action_appointment_id.name

class ClinicalImpressionInvestigation(models.Model):
    _name = "hc.clinical.impression.investigation"
    _description = "Clinical Impression Investigation"

    clinical_impression_id = fields.Many2one(
        comodel_name="hc.res.clinical.impression",
        string="Clinical Impression",
        help="Clinical impression associated with this investigation.")
    code_id = fields.Many2one(
        comodel_name="hc.vs.investigation.set",
        string="Code",
        required="True",
        help="A name/code for the set.")
    item_type = fields.Selection(
        string="Item Type",
        selection=[
            ("observation", "Observation"),
            ("questionnaire_response", "Questionnaire Response"),
            ("family_member_history", "Family Member History"),
            ("diagnostic_report", "Diagnostic Report"),
            ("risk_assessment", "Risk Assessment"),
            ("imaging_study", "Imaging Study")],
        help="Type of record of a specific investigation.")
    item_name = fields.Char(
        string="Item",
        compute="_compute_item_name",
        store="True",
        help="Record of a specific investigation.")
    item_observation_id = fields.Many2one(
        comodel_name="hc.res.observation",
        string="Item Observation",
        help="Observation record of a specific investigation.")
    item_questionnaire_response_id = fields.Many2one(
        comodel_name="hc.res.questionnaire.response",
        string="Item Questionnaire Response",
        help="Questionnaire Response record of a specific investigation.")
    item_family_member_history_id = fields.Many2one(
        comodel_name="hc.res.family.member.history",
        string="Item Family Member History",
        domain="['|',('item_family_member_history_id.subject_patient_id','=',subject_patient_id), ('item_family_member_history_id.subject_group_id','=','subject_group_id')]",
        help="Family Member History record of a specific investigation.")
    item_diagnostic_report_id = fields.Many2one(
        comodel_name="hc.res.diagnostic.report",
        string="Item Diagnostic Report",
        help="Diagnostic Report record of a specific investigation.")
    item_risk_assessment_id = fields.Many2one(
        comodel_name="hc.res.risk.assessment",
        string="Item Risk Assessment",
        help="Risk Assessment record of a specific investigation.")
    item_imaging_study_id = fields.Many2one(
        comodel_name="hc.res.imaging.study",
        string="Item Imaging Study",
        help="Imaging Study record of a specific investigation.")

    @api.depends('item_type')
    def _compute_item_name(self):
        for hc_res_clinical_impression in self:
            if hc_res_clinical_impression.item_type == 'observation':
                hc_res_clinical_impression.item_name = hc_res_clinical_impression.item_observation_id.name
            elif hc_res_clinical_impression.item_type == 'family_member_history':
                hc_res_clinical_impression.item_name = hc_res_clinical_impression.item_family_member_history_id.record_name
            elif hc_res_clinical_impression.item_type == 'questionnaire_response':
                hc_res_clinical_impression.item_name = hc_res_clinical_impression.item_questionnaire_response_id.name
            elif hc_res_clinical_impression.item_type == 'diagnostic_report':
                hc_res_clinical_impression.item_name = hc_res_clinical_impression.item_diagnostic_report_id.name
            elif hc_res_clinical_impression.item_type == 'risk_assessment':
                hc_res_clinical_impression.item_name = hc_res_clinical_impression.item_risk_assessment_id.name
            elif hc_res_clinical_impression.item_type == 'imaging_study':
                hc_res_clinical_impression.item_name = hc_res_clinical_impression.item_imaging_study_id.name

class ClinicalImpressionFinding(models.Model):
    _name = "hc.clinical.impression.finding"
    _description = "Clinical Impression Finding"

    clinical_impression_id = fields.Many2one(
        comodel_name="hc.res.clinical.impression",
        string="Clinical Impression",
        help="Clinical impression associated with this finding.")
    item_type = fields.Selection(
        string="Item Type",
        required="True",
        selection=[
            ("code", "Code"),
            ("condition", "Condition"),
            ("observation", "Observation")],
        help="Type of what was found.")
    item_name = fields.Char(
        string="Item",
        compute="_compute_item_name",
        store="True",
        required="True", help="What was found.")
    item_code_id = fields.Many2one(
        comodel_name="hc.vs.condition.code",
        string="Item Code",
        help="Code of what was found")
    item_condition_id = fields.Many2one(
        comodel_name="hc.res.condition",
        string="Item Condition",
        help="Condition what was found.")
    item_observation_id = fields.Many2one(
        comodel_name="hc.res.observation",
        string="Item Observation",
        help="Observation what was found.")
    cause = fields.Text(
        string="Cause",
        help="Which investigations support finding.")

    @api.depends('item_type')
    def _compute_item_name(self):
        for hc_res_clinical_impression in self:
            if hc_res_clinical_impression.item_type == 'code':
                hc_res_clinical_impression.item_name = hc_res_clinical_impression.item_code_id.name
            elif hc_res_clinical_impression.item_type == 'condition':
                hc_res_clinical_impression.item_name = hc_res_clinical_impression.item_condition_id.name
            elif hc_res_clinical_impression.item_type == 'observation':
                hc_res_clinical_impression.item_name = hc_res_clinical_impression.item_observation_id.name

class ClinicalImpressionIdentifier(models.Model):
    _name = "hc.clinical.impression.identifier"
    _description = "Clinical Impression Identifier"
    _inherit = ["hc.basic.association", "hc.identifier"]

    clinical_impression_id = fields.Many2one(
        comodel_name="hc.res.clinical.impression",
        string="Clinical Impression",
        help="Clinical Impression associated with this Clinical Impression Identifier.")

class ClinicalImpressionStatusHistory(models.Model):
    _name = "hc.clinical.impression.status.history"
    _description = "Clinical Impression Status History"

    clinical_impression_id = fields.Many2one(
        comodel_name="hc.res.clinical.impression",
        string="Clinical Impression",
        help="Clinical Impression associated with this Clinical Impression Status History.")
    status = fields.Char(
        string="Status",
        help="The status of the clinical impression.")
    start_date = fields.Datetime(
        string="Start Date",
        help="Start of the period during which this clinical impression status is valid.")
    end_date = fields.Datetime(
        string="End Date",
        help="End of the period during which this clinical impression status is valid.")
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

class ClinicalImpressionPrognosisReference(models.Model):
    _name = "hc.clinical.impression.prognosis.reference"
    _description = "Clinical Impression Prognosis Reference"
    _inherit = ["hc.basic.association"]

    clinical_impression_id = fields.Many2one(
        comodel_name="hc.res.clinical.impression",
        string="Clinical Impression",
        help="Clinical Impression associated with this Clinical Impression Prognosis Reference.")
    prognosis_reference_id = fields.Many2one(
        comodel_name="hc.res.risk.assessment",
        string="Prognosis Reference",
        help="Risk Assessment associated with this Clinical Impression Prognosis Reference.")

class ClinicalImpressionNote(models.Model):
    _name = "hc.clinical.impression.note"
    _description = "Clinical Impression Note"
    _inherit = ["hc.basic.association", "hc.annotation"]

    clinical_impression_id = fields.Many2one(
        comodel_name="hc.res.clinical.impression",
        string="Clinical Impression",
        help="Clinical Impression associated with this Clinical Impression Note.")

    @api.depends('author_type')
    def _compute_author_name(self):
        for hc_clinical_impression_note in self:
            if hc_clinical_impression_note.author_type == 'string':
                hc_clinical_impression_note.author_name = hc_clinical_impression_note.author_string
            elif hc_clinical_impression_note.author_type == 'practitioner':
                hc_clinical_impression_note.author_name = hc_clinical_impression_note.author_practitioner_id.name
            elif hc_clinical_impression_note.author_type == 'patient':
                hc_clinical_impression_note.author_name = hc_clinical_impression_note.author_patient_id.name
            elif hc_clinical_impression_note.author_type == 'related_person':
                hc_clinical_impression_note.author_name = hc_clinical_impression_note.author_related_person_id.name

class ClinicalImpressionProblem(models.Model):
    _name = "hc.clinical.impression.problem"
    _description = "Clinical Impression Problem"
    _inherit = ["hc.basic.association"]

    clinical_impression_id = fields.Many2one(
        comodel_name="hc.res.clinical.impression",
        string="Clinical Impression",
        help="Clinical Impression associated with this Clinical Impression Problem.")
    problem_type = fields.Selection(
        string="Problem Type",
        selection=[
            ("condition", "Condition"),
            ("allergy_intolerance", "Allergy Intolerance")],
        help="Type of general assessment of patient state.")
    problem_name = fields.Char(
        string="Problem",
        compute="_compute_problem_name",
        store="True",
        help="General assessment of patient state.")
    problem_condition_id = fields.Many2one(
        comodel_name="hc.res.condition",
        string="Problem Condition",
        help="Condition general assessment of patient state.")
    problem_allergy_intolerance_id = fields.Many2one(
        comodel_name="hc.res.allergy.intolerance",
        string="Problem Allergy Intolerance",
        help="Allergy Intolerance general assessment of patient state.")

    @api.depends('problem_type')
    def _compute_problem_name(self):
        for hc_res_clinical_impression in self:
            if hc_res_clinical_impression.problem_type == 'condition':
                hc_res_clinical_impression.problem_name = hc_res_clinical_impression.problem_condition_id.name
            elif hc_res_clinical_impression.problem_type == 'allergy_intolerance':
                hc_res_clinical_impression.problem_name = hc_res_clinical_impression.problem_allergy_intolerance_id.name

class ClinicalImpressionProtocol(models.Model):
    _name = "hc.clinical.impression.protocol"
    _description = "Clinical Impression Protocol"
    _inherit = ["hc.basic.association"]

    clinical_impression_id = fields.Many2one(
        comodel_name="hc.res.clinical.impression",
        string="Clinical Impression",
        help="Clinical Impression associated with this Clinical Impression Protocol.")
    protocol = fields.Html(
        string="Protocol URI",
        help="URI of Protocol associated with this Clinical Impression Protocol.")

class ClinicalImpressionKind(models.Model):
    _name = "hc.vs.clinical.impression.kind"
    _description = "Clinical Impression Kind"
    _inherit = ["hc.value.set.contains"]

class ClinicalImpressionTrigger(models.Model):
    _name = "hc.vs.clinical.impression.trigger"
    _description = "Clinical Impression Trigger"
    _inherit = ["hc.value.set.contains"]

class ClinicalImpressionPrognosis(models.Model):
    _name = "hc.vs.clinical.impression.prognosis"
    _description = "Clinical Impression Prognosis"
    _inherit = ["hc.value.set.contains"]

class InvestigationSet(models.Model):
    _name = "hc.vs.investigation.set"
    _description = "Investigation Set"
    _inherit = ["hc.value.set.contains"]

class ClinicalImpressionCode(models.Model):
    _name = "hc.vs.clinical.impression.code"
    _description = "Clinical Impression Code"
    _inherit = ["hc.value.set.contains"]

# External Reference

class ConditionStageAssessment(models.Model):
    _inherit = ["hc.condition.stage.assessment"]

    assessment_name = fields.Char(
        string="Assessment",
        compute="_compute_assessment_name",
        store="True",
        help="Formal record of assessment.")
    assessment_clinical_impression_id = fields.Many2one(
        comodel_name="hc.res.clinical.impression",
        string="Assessment Clinical Impression",
        help="Clinical Impression formal record of assessment.")
    assessment_diagnostic_report_id = fields.Many2one(
        comodel_name="hc.res.diagnostic.report",
        string="Assessment Diagnostic Report",
        help="Diagnostic Report formal record of assessment.")
    assessment_observation_id = fields.Many2one(
        comodel_name="hc.res.observation",
        string="Assessment Observation",
        help="Observation formal record of assessment.")

    @api.depends('assessment_type')
    def _compute_assessment_name(self):
        for hc_condition_stage_assessment in self:
            if hc_condition_stage_assessment.assessment_type == 'clinical_impression':
                hc_condition_stage_assessment.assessment_name = hc_condition_stage_assessment.assessment_clinical_impression_id.name
            elif hc_condition_stage_assessment.assessment_type == 'observation':
                hc_condition_stage_assessment.assessment_name = hc_condition_stage_assessment.assessment_observation_id.name
            elif hc_condition_stage_assessment.assessment_type == 'diagnostic_report':
                hc_condition_stage_assessment.assessment_name = hc_condition_stage_assessment.assessment_diagnostic_report_id.name
