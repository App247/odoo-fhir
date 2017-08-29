# -*- coding: utf-8 -*-

from openerp import models, fields, api

class DiagnosticReport(models.Model):
    _name = "hc.res.diagnostic.report"
    _description = "Diagnostic Report"
    _inherit = ["hc.domain.resource"]
    _rec_name = "name"

    name = fields.Char(
        string="Name",
        compute="_compute_name",
        store="True",
        help="Name for this diagnostic report. Subject Name + Code + Issued.")
    identifier_ids = fields.One2many(
        comodel_name="hc.diagnostic.report.identifier",
        inverse_name="diagnostic_report_id",
        string="Identifiers",
        help="Id for external references to this report.")
    based_on_ids = fields.One2many(
        comodel_name="hc.diagnostic.report.based.on",
        inverse_name="diagnostic_report_id",
        string="Based Ons",
        help="What was requested.")
    status = fields.Selection(
        string="Diagnostic Report Status",
        required="True",
        selection=[
            ("registered", "Registered"),
            ("partial", "Partial"),
            ("final", "Final"),
            ("corrected", "Corrected"),
            ("appended", "Appended"),
            ("cancelled", "Cancelled"),
            ("entered-in-error", "Entered-In-Error")],
        help="The status of the diagnostic report as a whole.")
    category_id = fields.Many2one(
        comodel_name="hc.vs.diagnostic.report.category",
        string="Category",
        help="Service category")
    code_id = fields.Many2one(
        comodel_name="hc.vs.diagnostic.report.code",
        string="Code",
        required="True",
        help="Name/Code for this diagnostic report")
    subject_type = fields.Selection(
        string="Subject Type",
        required="True",
        selection=[
            ("patient", "Patient"),
            ("group", "Group"),
            ("device", "Device"),
            ("location", "Location")],
        help="Type of plan or agreement issuer.")
    subject_name = fields.Char(
        string="Subject",
        compute="_compute_subject_name",
        help="The subject of the report, usually, but not always, the patient.")
    subject_patient_id = fields.Many2one(
        comodel_name="hc.res.patient",
        string="Subject Patient",
        required="True",
        help="Patient subject of the report, usually, but not always, the patient.")
    subject_group_id = fields.Many2one(
        comodel_name="hc.res.group",
        string="Subject Group",
        help="Group subject of the report, usually, but not always, the patient.")
    subject_location_id = fields.Many2one(
        comodel_name="hc.res.location",
        string="Subject Location",
        help="Location subject of the report, usually, but not always, the patient.")
    subject_device_id = fields.Many2one(
        comodel_name="hc.res.device",
        string="Subject Device",
        help="Device subject of the report, usually, but not always, the patient.")
    context_type = fields.Selection(
        string="Context Type",
        selection=[
            ("encounter", "Encounter"),
            ("episode_of_care", "Episode Of Care")],
        help="Type of health care event when test ordered.")
    context_name = fields.Char(
        string="Context",
        compute="_compute_context_name",
        store="True",
        help="Health care event when test ordered.")
    context_encounter_id = fields.Many2one(
        comodel_name="hc.res.encounter",
        string="Context Encounter",
        help="Encounter health care event when test ordered.")
    context_episode_of_care_id = fields.Many2one(
        comodel_name="hc.res.episode.of.care",
        string="Context Episode Of Care",
        help="Episode Of Care health care event when test ordered.")
    effective_type = fields.Selection(
        string="Effective Type",
        required="True",
        selection=[
            ("date_time", "Date Time"),
            ("period", "Period")],
        help="Type of plan or agreement issuer.")
    effective_name = fields.Char(
        string="Effective",
        compute="_compute_effective_name",
        required="True",
        help="Clinically Relevant time/time-period for report.")
    effective_date_time = fields.Datetime(
        string="Effective Date Time",
        help="DateTime clinically relevant time/time-period for report.")
    effective_start_date = fields.Datetime(
        string="Effective Start Date",
        help="Start of the clinically relevant time/time-period for report.")
    effective_end_date = fields.Datetime(
        string="Effective End Date",
        help="End of the clinically relevant time/time-period for report.")
    issued = fields.Datetime(
        string="Issued Date",
        required="True",
        help="DateTime this version was released.")
    specimen_ids = fields.One2many(
        comodel_name="hc.diagnostic.report.specimen",
        inverse_name="diagnostic_report_id",
        string="Specimens",
        help="Specimens this report is based on.")
    result_ids = fields.One2many(
        comodel_name="hc.diagnostic.report.result",
        inverse_name="diagnostic_report_id",
        string="Results",
        help="Observations - simple, or complex nested groups.")
    imaging_study_ids = fields.One2many(
        comodel_name="hc.diagnostic.report.imaging.study",
        inverse_name="diagnostic_report_id",
        string="Imaging Supplies",
        help="Reference to full details of imaging associated with the diagnostic report.")
    conclusion = fields.Text(
        string="Conclusion",
        help="Clinical Interpretation of test results.")
    coded_diagnosis_ids = fields.Many2many(
        comodel_name="hc.vs.clinical.finding",
        string="Coded Diagnosis",
        help="Codes for the conclusion.")
    presented_form_ids = fields.One2many(
        comodel_name="hc.diagnostic.report.presented.form",
        inverse_name="diagnostic_report_id",
        string="Presented Forms",
        help="Entire Report as issued.")
    performer_ids = fields.One2many(
        comodel_name="hc.diagnostic.report.performer",
        inverse_name="diagnostic_report_id",
        string="Performers",
        help="Participants in producing the report.")
    image_ids = fields.One2many(
        comodel_name="hc.diagnostic.report.image",
        inverse_name="diagnostic_report_id",
        string="Images",
        help="Key images associated with this report.")

    @api.depends('subject_type')
    def _compute_subject_name(self):
        for hc_res_diagnostic_report in self:
            if hc_res_diagnostic_report.subject_type == 'patient':
                hc_res_diagnostic_report.subject_name = hc_res_diagnostic_report.subject_patient_id.name
            elif hc_res_diagnostic_report.subject_type == 'group':
                hc_res_diagnostic_report.subject_name = hc_res_diagnostic_report.subject_group_id.name
            elif hc_res_diagnostic_report.subject_type == 'device':
                hc_res_diagnostic_report.subject_name = hc_res_diagnostic_report.subject_device_id.name
            elif hc_res_diagnostic_report.subject_type == 'location':
                hc_res_diagnostic_report.subject_name = hc_res_diagnostic_report.subject_location_id.name

    @api.depends('effective_type')
    def _compute_effective_name(self):
        for hc_res_diagnostic_report in self:
            if hc_res_diagnostic_report.effective_type == 'date_time':
                hc_res_diagnostic_report.effective_name = str(hc_res_diagnostic_report.effective_date_time)
            elif hc_res_diagnostic_report.effective_type == 'period':
                hc_res_diagnostic_report.effective_name = 'Between' + str(hc_res_diagnostic_report.effective_start_date) + ' and ' + str(hc_res_diagnostic_report.effective_end_date)

class DiagnosticReportPerformer(models.Model):
    _name = "hc.diagnostic.report.performer"
    _description = "Diagnostic Report Performer"

    diagnostic_report_id = fields.Many2one(
        comodel_name="hc.res.diagnostic.report",
        string="Diagnostic Report",
        help="Diagnostic Report associated with this performer.")
    role_id = fields.Many2one(
        comodel_name="hc.vs.performer.role",
        string="Role",
        help="Type of performer")
    actor_type = fields.Selection(
        string="Actor Type",
        required="True",
        selection=[
            ("practitioner", "Practitioner"),
            ("organization", "Organization")],
        help="Type of participant.")
    actor_name = fields.Char(
        string="Actor",
        compute="_compute_actor_name",
        store="True",
        help="Practitioner or Organization participant.")
    actor_practitioner_id = fields.Many2one(
        comodel_name="hc.res.practitioner",
        string="Actor Practitioner",
        required="True",
        help="Practitioner participant.")
    actor_organization_id = fields.Many2one(
        comodel_name="hc.res.organization",
        string="Actor Organization",
        help="Organization participant.")

    @api.depends('actor_type')
    def _compute_actor_name(self):
        for hc_diagnostic_report_performer in self:
            if hc_diagnostic_report_performer.actor_type == 'practitioner':
                hc_diagnostic_report_performer.actor_name = hc_diagnostic_report_performer.actor_practitioner_id.name
            elif hc_diagnostic_report_performer.actor_type == 'organization':
                hc_diagnostic_report_performer.actor_name = hc_diagnostic_report_performer.actor_organization_id.name

class DiagnosticReportImage(models.Model):
    _name = "hc.diagnostic.report.image"
    _description = "Diagnostic Report Image"

    diagnostic_report_id = fields.Many2one(
        comodel_name="hc.res.diagnostic.report",
        string="Diagnostic Report",
        help="Diagnostic Report associated with this image.")
    comment = fields.Text(
        string="Comment",
        help="Comment about the image (e.g. explanation).")
    link_id = fields.Many2one(
        comodel_name="hc.res.media",
        string="Link",
        required="True",
        help="Reference to the image source.")

class DiagnosticReportIdentifier(models.Model):
    _name = "hc.diagnostic.report.identifier"
    _description = "Diagnostic Report Identifier"
    _inherit = ["hc.basic.association", "hc.identifier"]

    diagnostic_report_id = fields.Many2one(
        comodel_name="hc.res.diagnostic.report",
        string="Diagnostic Report",
        help="Diagnostic Report associated with this Diagnostic Report Identifier.")

class DiagnosticReportBasedOn(models.Model):
    _name = "hc.diagnostic.report.based.on"
    _description = "Diagnostic Report Based On"
    _inherit = ["hc.basic.association"]

    diagnostic_report_id = fields.Many2one(
        comodel_name="hc.res.diagnostic.report",
        string="Diagnostic Report",
        help="Diagnostic Report associated with this diagnostic report based on.")
    based_on_type = fields.Selection(
        string="Based On Type",
        selection=[
            ("care_plan", "Care Plan"),
            ("immunization_recommendation", "Immunization Recommendation"),
            ("medication_request", "Medication Request"),
            ("nutrition_order", "Nutrition Order"),
            ("procedure_request", "Procedure Request")],
        help="Type of what was requested.")
    based_on_name = fields.Char(
        string="Based On",
        compute="_compute_based_on_name",
        store="True",
        help="What was requested.")
    based_on_care_plan_id = fields.Many2one(
        comodel_name="hc.res.care.plan",
        string="Diagnostic Report",
        help="Care Plan what was requested.")
    based_on_immunization_recommendation_id = fields.Many2one(
        comodel_name="hc.res.immunization.recommendation",
        string="Based On Immunization Recommendation",
        help="Immunization Recommendation what was requested.")
    based_on_medication_request_id = fields.Many2one(
        comodel_name="hc.res.medication.request",
        string="Based On Medication Request",
        help="Medication Request what was requested.")
    based_on_nutrition_order_id = fields.Many2one(
        comodel_name="hc.res.nutrition.order",
        string="Based On Nutrition Order",
        help="Nutrition Order what was requested.")
    bsaed_on_procedure_request_id = fields.Many2one(
        comodel_name="hc.res.procedure.request",
        string="Bsaed On Procedure Request",
        help="Procedure Request what was requested.")

class DiagnosticReportImagingStudy(models.Model):
    _name = "hc.diagnostic.report.imaging.study"
    _description = "Diagnostic Report Imaging Study"
    _inherit = ["hc.basic.association"]

    diagnostic_report_id = fields.Many2one(
        comodel_name="hc.res.diagnostic.report",
        string="Diagnostic Report",
        help="Diagnostic Report associated with this Diagnostic Report Imaging Study.")
    imaging_study_type = fields.Selection(
        string="Imaging Study Type",
        selection=[
            ("imaging_study", "Imaging Study"),
            ("imaging_manifest", "Imaging Manifest")],
        help="Type of reference to full details of imaging associated with the diagnostic report.")
    imaging_study_name = fields.Char(
        string="Imaging Study",
        compute="_compute_imaging_study_name",
        help="Reference to full details of imaging associated with the diagnostic report.")
    imaging_study_id = fields.Many2one(
        comodel_name="hc.res.imaging.study",
        string="Imaging Study",
        help="Imaging Study reference to full details of imaging associated with the diagnostic report.")
    imaging_manifest_id = fields.Many2one(
        comodel_name="hc.res.imaging.manifest",
        string="Imaging Manifest",
        help="Imaging Manifest reference to full details of imaging associated with the diagnostic report.")

class DiagnosticReportResult(models.Model):
    _name = "hc.diagnostic.report.result"
    _description = "Diagnostic Report Result"
    _inherit = ["hc.basic.association"]

    diagnostic_report_id = fields.Many2one(
        comodel_name="hc.res.diagnostic.report",
        string="Diagnostic Report",
        help="Diagnostic Report associated with this Diagnostic Report Result.")
    result_id = fields.Many2one(
        comodel_name="hc.res.observation",
        string="Result",
        help="Observation associated with this Diagnostic Report Result.")

class DiagnosticReportPresentedForm(models.Model):
    _name = "hc.diagnostic.report.presented.form"
    _description = "Diagnostic Report Presented Form"
    _inherit = ["hc.basic.association", "hc.attachment"]

    diagnostic_report_id = fields.Many2one(
        comodel_name="hc.res.diagnostic.report",
        string="Diagnostic Report",
        help="Diagnostic Report associated with this Diagnostic Report Presented Form.")

class DiagnosticReportSpecimen(models.Model):
    _name = "hc.diagnostic.report.specimen"
    _description = "Diagnostic Report Specimen"
    _inherit = ["hc.basic.association"]

    diagnostic_report_id = fields.Many2one(
        comodel_name="hc.res.diagnostic.report",
        string="Diagnostic Report",
        help="Diagnostic Report associated with this Diagnostic Report Specimen.")
    specimen_id = fields.Many2one(
        comodel_name="hc.res.specimen",
        string="Specimen",
        help="Specimen associated with this Diagnostic Report Specimen.")

class DiagnosticReportCategory(models.Model):
    _name = "hc.vs.diagnostic.report.category"
    _description = "Diagnostic Report Category"
    _inherit = ["hc.value.set.contains"]

    name = fields.Char(
        string="Name",
        help="Name of this diagnostic report category.")
    code = fields.Char(
        string="Code",
        help="Code of this diagnostic report category.")
    contains_id = fields.Many2one(
        comodel_name="hc.vs.diagnostic.report.category",
        string="Parent",
        help="Parent diagnostic report category.")

class DiagnosticReportCode(models.Model):
    _name = "hc.vs.diagnostic.report.code"
    _description = "Diagnostic Report Code"
    _inherit = ["hc.value.set.contains"]

    name = fields.Char(
        string="Name",
        help="Name of this diagnostic report code.")
    code = fields.Char(
        string="Code",
        help="Code of this diagnostic report code.")
    contains_id = fields.Many2one(
        comodel_name="hc.vs.diagnostic.report.code",
        string="Parent",
        help="Parent diagnostic report code.")

# External Reference

class ConditionStageAssessment(models.Model):
    _inherit = "hc.condition.stage.assessment"

    assessment_type = fields.Selection(
        selection_add=[
            ("diagnostic_report", "Diagnostic Report")])
    assessment_diagnostic_report_id = fields.Many2one(
        comodel_name="hc.res.diagnostic.report",
        string="Assessment Diagnostic Reports",
        help="Diagnostic Report formal record of assessment.")

    @api.depends('assessment_type')
    def _compute_stage_assessment_name(self):
        for hc_condition_stage_assessment in self:
            if hc_condition_stage_assessment.assessment_type == 'observation':
                hc_condition_stage_assessment.assessment_name = hc_condition_stage_assessment.assessment_observation_id.name
            elif hc_condition_stage_assessment.assessment_type == 'diagnostic_report':
                hc_condition_stage_assessment.assessment_name = hc_condition_stage_assessment.assessment_diagnostic_report_id.name

class ProcedureReport(models.Model):
    _inherit = "hc.procedure.report"

    report_id = fields.Many2one(
        comodel_name="hc.res.diagnostic.report",
        string="Report",
        help="Report associated with this Procedure Report.")

class ProcedureRequestReasonReference(models.Model):
    _inherit = "hc.procedure.request.reason.reference"

    reason_reference_type = fields.Selection(
        selection_add=[
            ("diagnostic_report", "Diagnostic Report")])
    reason_reference_diagnostic_report_id = fields.Many2one(
        comodel_name="hc.res.diagnostic.report",
        string="Reason Reference Diagnostic Report",
        help="Diagnostic Report explanation/justification for procedure or service.")

    @api.multi
    def _compute_reason_reference_name(self):
        for hc_res_procedure_request in self:
            if hc_res_procedure_request.reason_type == 'condition':
                hc_res_procedure_request.reason_name = hc_res_procedure_request.reason_condition_id.name
            elif hc_res_procedure_request.reason_type == 'observation':
                hc_res_procedure_request.reason_name = hc_res_procedure_request.reason_observation_id.name
            elif hc_res_procedure_request.reason_type == 'diagnostic_report':
                hc_res_procedure_request.reason_name = hc_res_procedure_request.reason_diagnostic_report_id.name
            elif hc_res_procedure_request.reason_type == 'document_reference':
                hc_res_procedure_request.reason_name = hc_res_procedure_request.reason_document_reference_id.name
