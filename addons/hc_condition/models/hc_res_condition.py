# -*- coding: utf-8 -*-

from openerp import models, fields, api
from datetime import datetime
from openerp.tools import DEFAULT_SERVER_DATE_FORMAT as DF
from openerp.tools import DEFAULT_SERVER_DATETIME_FORMAT as DTF

class Condition(models.Model):    
    _name = "hc.res.condition"    
    _description = "Condition"            

    name = fields.Char(
        string="Event Name", 
        compute="_compute_name", 
        store="True", 
        help="Text representation of the condition event. Subject Name + Condition Code + Asserted Date.")
    identifier_ids = fields.One2many(
        comodel_name="hc.condition.identifier", 
        inverse_name="condition_id", 
        string="Identifiers", 
        help="External Ids for this condition.")                    
    clinical_status = fields.Selection(
        string="Clinical Status",
        selection=[
            ("active", "Active"), 
            ("recurrence", "Recurrence"), 
            ("inactive", "Inactive"), 
            ("remission", "Remission"), 
            ("resolved", "Resolved")],
        default="active",
        help="The clinical status of the condition.")                    
    verification_status = fields.Selection(
        string="Verification Status", 
        required="True", 
        selection=[
            ("provisional", "Provisional"), 
            ("differential", "Differential"), 
            ("confirmed", "Confirmed"), 
            ("refuted", "Refuted"), 
            ("entered-in-error", "Entered-In-Error"), 
            ("unknown", "Unknown")],
        default="provisional", 
        help="The verification status to support the clinical status of the condition.")                    
    category_ids = fields.Many2many(
        comodel_name="hc.vs.condition.category", 
        # relation="condition_category_rel", 
        string="Categories", 
        help="A category assigned to the condition.")              
    severity_id = fields.Many2one(
        comodel_name="hc.vs.condition.severity", 
        string="Severity", 
        help="A category assigned to the condition.")                    
    code_id = fields.Many2one(
        comodel_name="hc.vs.condition.code", 
        string="Condition", 
        required="True", 
        help="Condition, problem or diagnosis.")                       
    code = fields.Char(
        string="Code", 
        related="code_id.code", 
        help="Identification of the condition, problem or diagnosis.")
    body_site_ids = fields.Many2many(
        comodel_name="hc.vs.body.site", 
        relation="condition_body_site_rel", 
        string="Body Sites", 
        help="Anatomical location, if relevant.")              
    subject_type = fields.Selection(
        string="Subject Type",
        required="True", 
        selection=[
            ("patient", "Patient"), 
            ("group", "Group")], 
        help="Type of who has the condition.")
    subject_name = fields.Char(
        string="Subject", 
        compute="_compute_subject_name", 
        store="True", 
        help="Who has the condition?")             
    subject_patient_id = fields.Many2one(
        comodel_name="hc.res.patient", 
        string="Subject Patient", 
        help="Patient who has the condition.")                    
    subject_group_id = fields.Many2one(
        comodel_name="hc.res.group", 
        string="Subject Group", 
        help="Group who has the condition.")                
    # context_type = fields.Selection(
    #     string="Context Type",
    #     selection=[
    #         ("encounter", "Encounter"), 
    #         ("episode_of_care", "Episode of Care")], 
    #     help="Type of encounter when condition first asserted.")                    
    # context_name = fields.Char(
    #     string="Context", 
    #     compute="_compute_context_name",
    #     store="True", 
    #     help="Encounter when condition first asserted.")                
    # context_encounter_id = fields.Many2one(
    #     comodel_name="hc.res.encounter", 
    #     string="Context Encounter", 
    #     help="Encounter when condition first asserted.")                    
    # context_episode_of_care_id = fields.Many2one(
    #     comodel_name="hc.res.episode.of.care", 
    #     string="Context Episode Of Care", 
    #     help="Episode Of Care when condition first asserted.")                    
    onset_type = fields.Selection(
        string="Onset Type",
        selection=[
            ("date_time", "Date Time"), 
            ("age", "Age"), 
            ("period", "Period"), 
            ("range", "Range"), 
            ("string", "String")], 
        help="Type of onset.")
    onset_name = fields.Char(
        string="Onset", 
        compute="_compute_onset_name",
        store="True", 
        help="Estimated or actual date, date-time, or age.")             
    onset_date_time = fields.Datetime(
        string="Onset Date Time", 
        help="Estimated or actual onset date time.")                    
    onset_age = fields.Integer(
        string="Onset Age", 
        size=3, 
        help="Estimated or actual onset age.")
    onset_age_uom_id = fields.Many2one(
        comodel_name="product.uom", 
        string="Onset Age UOM", 
        domain="[('category_id','=','Time (UCUM)')]", 
        default="a", 
        help="Onset age unit of measure.")
    onset_start_date = fields.Datetime(
        string="Onset Start Date", 
        help="Start of the estimated or actual onset.")                    
    onset_end_date = fields.Datetime(
        string="Onset End Date", 
        help="End of the estimated or actual onset.")                    
    onset_range_low = fields.Float(
        string="Onset Range Low", 
        help="Low limit of estimated or actual onset.")                    
    onset_range_high = fields.Float(
        string="Onset Range High", 
        help="High limit of estimated or actual onset.")
    onset_string = fields.Char(
        string="Onset String", 
        help="String of estimated or actual onset.")                      
    abatement_type = fields.Selection(
        string="Abatement Type", 
        selection=[
            ("date_time", "Date Time"), 
            ("Age", "Age"), 
            ("Period", "Period"), 
            ("Range", "Range"), 
            ("string", "String")], 
        help="Type of when in resolution/remission.")
    abatement_name = fields.Char(
        string="Abatement", 
        ompute="_compute_abatement_name", 
        store="True", 
        help="When in resolution/remission.")
    abatement_date_time = fields.Datetime(
        string="Abatement Date Time", 
        help="Date time of resolution/remission.")
    abatement_age = fields.Integer(
        string="Abatement Age", 
        size=3, 
        help="Age of resolution/remission.")
    abatement_age_uom_id = fields.Many2one(
        comodel_name="product.uom", 
        string="Abatement Age UOM", 
        domain="[('category_id','=','Time (UCUM)')]", 
        default="a", 
        help="Abatement age unit of measure.")
    abatement_boolean = fields.Boolean(
        string="Abatement Boolean", 
        help="Boolean of when in resolution/remission.")
    abatement_start_date = fields.Datetime(
        string="Abatement Start Date", 
        help="Start of the resolution/remission.")
    abatement_end_date = fields.Datetime(
        string="Abatement End Date", 
        help="End of the resolution/remission.")
    abatement_range_low = fields.Float(
        string="Abatement Range Low", 
        help="Low limit of when in resolution/remission.")
    abatement_range_high = fields.Float(
        string="Abatement Range High",
        help="High limit of when in resolution/remission.")
    abatement_string = fields.Char(
        string="Abatement String", 
        help="String of when in resolution/remission.")       
    asserted_date = fields.Datetime(
        string="Asserted Date",
        required="True",
        default=fields.datetime.now(), 
        help="Date record was believed accurate.")                  
    asserter_type = fields.Selection(
        string="Asserter Type",
        selection=[
            ("practitioner", "Practitioner"), 
            ("patient", "Patient"),
            ("related_person", "Related Person")], 
        help="Type of asserter.")                    
    asserter_name = fields.Char(
        string="Asserter", 
        compute="_compute_asserter_name",
        store="True",  
        help="Person who asserts this condition.")                  
    asserter_practitioner_id = fields.Many2one(
        comodel_name="hc.res.practitioner", 
        string="Asserter Practitioner", 
        help="Practitioner who asserts this condition.")                    
    asserter_patient_id = fields.Many2one(
        comodel_name="hc.res.patient", 
        string="Asserter Patient", 
        help="Patient who asserts this condition.")                    
    asserter_related_person_id = fields.Many2one(
        comodel_name="hc.res.related.person", 
        string="Asserter Related Person", 
        help="Related Person who asserts this condition.")
    note_ids = fields.One2many(
        comodel_name="hc.condition.note", 
        inverse_name="condition_id", 
        string="Notes", 
        help="Additional information about the Condition.")                                  
    stage_ids = fields.One2many(
        comodel_name="hc.condition.stage", 
        inverse_name="condition_id", 
        string="Stages", 
        help="Stage/grade, usually assessed formally.")
    evidence_ids = fields.One2many(
        comodel_name="hc.condition.evidence", 
        inverse_name="condition_id", 
        string="Evidence", 
        help="Supporting evidence.")                    

    @api.one                
    @api.depends('subject_patient_id', 'subject_group_id', 'code_id', 'asserted_date')              
    def _compute_name(self):                
        comp_name = '/'         
        for hc_res_condition in self:
            if hc_res_condition.subject_type == 'patient':           
                comp_name = hc_res_condition.subject_patient_id.name    
                if hc_res_condition.subject_patient_id.birth_date:  
                    subject_patient_birth_date = datetime.strftime(datetime.strptime(hc_res_condition.subject_patient_id.birth_date, DF), "%Y-%m-%d")
                    comp_name = comp_name + "("+ subject_patient_birth_date + ")"
            if hc_res_condition.subject_type == 'group':
                    comp_name = hc_res_condition.subject_group_id.name            
            if hc_res_condition.code_id:        
                comp_name = comp_name + ", " + hc_res_condition.code_id.name or ''   
            if hc_res_condition.asserted_date:      
                patient_asserted_date = datetime.strftime(datetime.strptime(hc_res_condition.asserted_date, DTF), "%Y-%m-%d")   
                comp_name = comp_name + ", " + patient_asserted_date 
            hc_res_condition.name = comp_name       
          
    @api.depends('subject_type')          
    def _compute_subject_name(self):            
        for hc_res_condition in self:       
            if hc_res_condition.subject_type == 'patient':  
                hc_res_condition.subject_name = hc_res_condition.subject_patient_id.name
            elif hc_res_condition.subject_type == 'group':  
                hc_res_condition.subject_name = hc_res_condition.subject_group_id.name

    # @api.multi          
    # def _compute_context_name(self):            
    #     for hc_res_condition in self:       
    #         if hc_res_condition.context_type == 'encounter':
    #             hc_res_condition.context_name = hc_res_condition.context_encounter_id.name
    #         elif hc_res_condition.context_type == 'episode_of_care':  
    #             hc_res_condition.context_name = hc_res_condition.context_episode_of_care_id.name
     
    @api.depends('onset_type')          
    def _compute_onset_name(self):          
        for hc_res_condition in self:       
            if hc_res_condition.onset_type == 'date_time':   
                hc_res_condition.onset_name = str(hc_res_condition.onset_date_time)
            elif hc_res_condition.onset_type == 'age':  
                hc_res_condition.onset_name = str(hc_res_condition.onset_age) + " " + str(hc_res_condition.onset_age_uom_id.name) + "s old"
            elif hc_res_condition.onset_type == 'period':  
                hc_res_condition.onset_name = "Between " + str(hc_res_condition.onset_start_date) + " and " + str(hc_res_condition.onset_end_date)
            elif hc_res_condition.onset_type == 'range':    
                hc_res_condition.onset_name = "Between " + str(hc_res_condition.onset_range_low) + " and " + str(hc_res_condition.onset_range_high)
            elif hc_res_condition.onset_type == 'string':
                hc_res_condition.onset_name = hc_res_condition.onset_string

    @api.depends('abatement_type')          
    def _compute_abatement_name(self):          
        for hc_res_condition in self:       
            if hc_res_condition.abatement_type == 'date_time':   
                hc_res_condition.abatement_name = str(hc_res_condition.abatement_date_time)
            elif hc_res_condition.abatement_type == 'age':  
                hc_res_condition.abatement_name = str(hc_res_condition.abatement_age) + " " + str(hc_res_condition.abatement_age_uom_id.name) + "s old"
            elif hc_res_condition.abatement_type == 'boolean':  
                hc_res_condition.abatement_name = hc_res_condition.abatement_boolean
            elif hc_res_condition.abatement_type == 'period':   
                hc_res_condition.abatement_name = "Between " + str(hc_res_condition.abatement_start_date) + " and " + str(hc_res_condition.abatement_end_date)
            elif hc_res_condition.abatement_type == 'range':    
                hc_res_condition.abatement_name = "Between " + str(hc_res_condition.abatement_range_low) + " and " + str(hc_res_condition.abatement_range_high)
            elif hc_res_condition.abatement_type == 'string':   
                hc_res_condition.abatement_name = hc_res_condition.abatement_string

    @api.depends('asserter_type')           
    def _compute_asserter_name(self):           
        for hc_res_condition in self:       
            if hc_res_condition.asserter_type == 'practitioner':    
                hc_res_condition.asserter_name = hc_res_condition.asserter_practitioner_id.name
            elif hc_res_condition.asserter_type == 'patient':   
                hc_res_condition.asserter_name = hc_res_condition.asserter_patient_id.name
            elif hc_res_condition.asserter_type == 'related_person':   
                hc_res_condition.asserter_name = hc_res_condition.asserter_related_person_id.name                 

class ConditionStage(models.Model):    
    _name = "hc.condition.stage"
    _description = "Condition Stage"

    condition_id = fields.Many2one(
        comodel_name="hc.res.condition", 
        string="Condition", 
        help="Condition associated with this Condition Stage.")
    summary_id = fields.Many2one(
        comodel_name="hc.vs.condition.stage.code", 
        string="Summary", 
        help="Simple summary (disease specific).")
    assessment_ids = fields.One2many(
        comodel_name="hc.condition.stage.assessment", 
        inverse_name="stage_id", 
        string="Assessments", 
        help="Formal record of assessment.")
    has_assessment = fields.Boolean(
        string='Has Assessment', 
        invisible=True,
        help="Indicates if assessment exists. Used to enforce constraint summary_id or assessment_ids.")

    @api.onchange('assessment_ids')
    def onchange_assessment_ids(self):
        if self.assessment_ids:
            self.summary_id = False
            self.has_assessment = True
        else:
            self.has_assessment = False

class ConditionEvidence(models.Model):    
    _name = "hc.condition.evidence"    
    _description = "Condition Evidence"        

    condition_id = fields.Many2one(
        comodel_name="hc.res.condition", 
        string="Condition", 
        help="Condition associated with this Condition Evidence.")                    
    detail_ids = fields.One2many(
        comodel_name="hc.condition.evidence.detail", 
        inverse_name="evidence_id", 
        string="Details", 
        help="Supporting information found elsewhere.")                    
    code_id = fields.Many2one(
        comodel_name="hc.vs.condition.evidence.code", 
        string="Code", 
        help="Manifestation/symptom.")                    

class ConditionIdentifier(models.Model):    
    _name = "hc.condition.identifier"    
    _description = "Condition Identifier"        
    _inherit = ["hc.basic.association", "hc.identifier"]    

    condition_id = fields.Many2one(
        comodel_name="hc.res.condition", 
        string="Condition", 
        help="Condition associated with this Condition Identifier.")                                  

class ConditionStageAssessment(models.Model):    
    _name = "hc.condition.stage.assessment"    
    _description = "Condition Stage Assessment"        
    _inherit = ["hc.basic.association"]    

    stage_id = fields.Many2one(
        comodel_name="hc.condition.stage", 
        string="Stage", 
        help="Stage associated with this Condition Stage Assessment.")              
    assessment_type = fields.Selection(
        string="Assessment Type", 
        selection=[
            ("clinical_impression", "Clinical Impression"), 
            ("diagnostic_report", "Diagnostic Report"),
            ("observation", "Observation")], 
        help="Type of assessment.")                    
    assessment_name = fields.Char(
        string="Assessment", 
        # compute="_compute_assessment_name",
        # store="True",  
        help="Formal record of assessment.")                   
    # assessment_clinical_impression_id = fields.Many2one(
    #     comodel_name="hc.res.clinical.impression", 
    #     string="Assessment Clinical Impression", 
    #     help="Clinical Impression formal record of assessment.")                    
    # assessment_diagnostic_report_id = fields.Many2one(
    #     comodel_name="hc.res.diagnostic.report", 
    #     string="Assessment Diagnostic Report", 
    #     help="Diagnostic Report formal record of assessment.")                    
    # assessment_observation_id = fields.Many2one(
    #     comodel_name="hc.res.observation", 
    #     string="Assessment Observation", 
    #     help="Observation formal record of assessment.")                    

    # @api.depends('assessment_type')                
    # def _compute_assessment_name(self):         
    #     for hc_condition_stage_assessment in self:       
    #         if hc_condition_stage_assessment.assessment_type == 'clinical_impression':   
    #             hc_condition_stage_assessment.assessment_name = hc_condition_stage_assessment.assessment_clinical_impression_id.name
    #         elif hc_condition_stage_assessment.assessment_type == 'observation': 
    #             hc_condition_stage_assessment.assessment_name = hc_condition_stage_assessment.assessment_observation_id.name
    #         elif hc_condition_stage_assessment.assessment_type == 'diagnostic_report':   
    #             hc_condition_stage_assessment.assessment_name = hc_condition_stage_assessment.assessment_diagnostic_report_id.name
            
class ConditionEvidenceDetail(models.Model):    
    _name = "hc.condition.evidence.detail"    
    _description = "Condition Evidence Detail"        
    _inherit = ["hc.basic.association"]    

    evidence_id = fields.Many2one(
        comodel_name="hc.condition.evidence", 
        string="Evidence", 
        help="Evidence associated with this Condition Evidence Detail.")                    
    detail_type = fields.Char(
        string="Detail Type",
        compute="_compute_detail_type",
        help="Type of supporting information found elsewhere.")
    detail_name = fields.Reference(
        string="Detail",
        selection="_reference_models", 
        help="Supporting information found elsewhere.")
                 
    @api.model
    def _reference_models(self):
        models = self.env['ir.model'].search([('state', '!=', 'manual')])
        return [(model.model, model.name)
            for model in models
                if model.model.startswith('hc.res')]

    @api.depends('detail_name')
    def _compute_detail_type(self):
        for this in self:
            if this.detail_name:
                this.detail_type = this.detail_name._description


class ConditionNote(models.Model):  
    _name = "hc.condition.note" 
    _description = "Condition Note"     
    _inherit = ["hc.basic.association", "hc.annotation"]

    condition_id = fields.Many2one(
        comodel_name="hc.res.condition", 
        string="Condition", 
        help="Condition associated with this Condition Note.")              

class ConditionSeverity(models.Model):    
    _name = "hc.vs.condition.severity"    
    _description = "Condition Severity"        
    _inherit = ["hc.value.set.contains"]    

    name = fields.Char(
        string="Name", 
        help="Name of this condition severity.")
    code = fields.Char(
        string="Code", 
        help="Code of this condition severity.")
    contains_id = fields.Many2one(
        comodel_name="hc.vs.condition.severity", 
        string="Parent", 
        help="Parent condition severity.")

class ConditionEvidenceCode(models.Model):    
    _name = "hc.vs.condition.evidence.code"    
    _description = "Condition Evidence Code"        
    _inherit = ["hc.value.set.contains"]    

    name = fields.Char(
        string="Name", 
        help="Name of this condition evidence code.")
    code = fields.Char(
        string="Code", 
        help="Code of this condition evidence code.")
    contains_id = fields.Many2one(
        comodel_name="hc.vs.condition.evidence.code", 
        string="Parent", 
        help="Parent condition evidence code.")

class ConditionStageCode(models.Model):
    _name = "hc.vs.condition.stage.code"
    _description = "Condition Stage Code"
    _inherit = ["hc.value.set.contains"]

    name = fields.Char(
        string="Name", 
        help="Name of this condition stage code.")                                
    code = fields.Char(
        string="Code", 
        help="Code of this condition stage code.")                                
    contains_id = fields.Many2one(
        comodel_name="hc.vs.condition.stage.code", 
        string="Parent", 
        help="Parent condition stage code.")                              

class ConditionCategory(models.Model):  
    _name = "hc.vs.condition.category"  
    _description = "Condition Category"         
    _inherit = ["hc.value.set.contains"]

    name = fields.Char(
        string="Name", 
        help="Name of this condition category.")
    code = fields.Char(
        string="Code", 
        help="Code of this condition category.")
    contains_id = fields.Many2one(
        comodel_name="hc.vs.condition.category", 
        string="Parent", 
        help="Parent condition category.")

