# -*- coding: utf-8 -*-

from openerp import models, fields, api

class RiskAssessment(models.Model):    
    _name = "hc.res.risk.assessment"    
    _description = "Risk Assessment"        

    name = fields.Char(
        string="Name", 
        required="True", 
        help="Text representation of the risk assessment event. Subject Name + Context Name + Occurrence Date.")
    identifier_id = fields.Many2one(
        comodel_name="hc.risk.assessment.identifier", 
        string="Identifier", 
        help="Unique identifier for the assessment.")                
    based_on_string = fields.Char(
        string="Based On String", 
        help="Request fulfilled by this assessment.")                
    parent = fields.Char(
        string="Parent", 
        help="Part of this occurrence.")                
    status = fields.Selection(
        string="Status", 
        required="True", 
        selection=[
            ("registered", "Registered"), 
            ("preliminary", "Preliminary"), 
            ("final", "Final"), 
            ("amended", "Amended")], 
        help="The status of the result value.")                
    code_id = fields.Many2one(
        comodel_name="hc.vs.risk.assessment.type", 
        string="Code", 
        help="Type of assessment.")                
    subject_type = fields.Selection(
        string="Subject Type", 
        selection=[
            ("Patient", "Patient"), 
            ("Group", "Group")], 
        help="Type of who/what does assessment apply to.")                
    subject_name = fields.Char(
        string="Subject", 
        compute="_compute_subject_name", 
        store="True", 
        help="Who/what does assessment apply to?")                
    subject_patient_id = fields.Many2one(
        comodel_name="hc.res.patient", 
        string="Subject Patient", 
        help="Patient that the assessment applies to.")                
    subject_group_id = fields.Many2one(
        comodel_name="hc.res.group", 
        string="Subject Group", 
        help="Group that the assessment applies to.")                
    context_type = fields.Selection(
        string="Context Type", 
        selection=[
            ("Encounter", "Encounter"), 
            ("Episode of Care", "Episode Of Care")], 
        help="Type of originating encounter.")                
    context_name = fields.Char(
        string="Context", 
        compute="_compute_context_name", 
        store="True", 
        help="Where was assessment performed?")                
    context_encounter_id = fields.Many2one(
        comodel_name="hc.res.encounter", 
        string="Context Encounter", 
        help="Encounter that the assessment applies to.")                
    context_episode_of_care_id = fields.Many2one(
        comodel_name="hc.res.episode.of.care", 
        string="Context Episode Of Care", 
        help="Episode Of Care that the assessment applies to.")                
    occurrence_type = fields.Selection(
        string="Occurrence Type", 
        selection=[
            ("date_time", "Date Time"), 
            ("Period", "Period")], 
        help="Type of originating encounter.")                
    occurrence_name = fields.Char(
        string="Occurrence", 
        compute="_compute_occurrence_name", 
        store="True", 
        help="When was assessment made?")                
    occurrence_date_time = fields.Datetime(
        string="Occurrence Date Time", 
        help="Datetime when was assessment made.")                
    occurrence_start_date = fields.Datetime(
        string="Occurrence Start Date", 
        help="Start of the when was assessment made.")                
    occurrence_end_date = fields.Datetime(
        string="Occurrence End Date",
        help="End of the when was assessment made.")                
    condition_id = fields.Many2one(
        comodel_name="hc.res.condition", 
        string="Condition", 
        help="Condition assessed.")                
    performer_type = fields.Selection(
        string="Performer Type", 
        selection=[
            ("Practitioner", "Practitioner"), 
            ("Device", "Device")], 
        help="Type of originating encounter.")                
    performer_name = fields.Char(
        string="Performer", 
        compute="_compute_performer_name", 
        store="True", 
        help="Who did assessment?")                
    performer_practitioner_id = fields.Many2one(
        comodel_name="hc.res.practitioner", 
        string="Performer Practitioner", 
        help="Practitioner who did assessment.")                
    performer_device_id = fields.Many2one(
        comodel_name="hc.res.device", 
        string="Performer Device", 
        help="Device who did assessment.")                
    reason_type = fields.Selection(
        string="Reason Type", 
        selection=[
            ("code", "Code"), 
            ("string", "String")], 
        help="Type of originating encounter.")                
    reason_name = fields.Char(
        string="Reason", 
        compute="_compute_reason_name", 
        store="True", 
        help="Why the assessment was necessary?")                
    reason_code_id = fields.Many2one(
        comodel_name="hc.vs.risk.assessment.reason", 
        string="Reason Code", 
        help="Code of why the assessment was necessary.")                
    reason_string = fields.Char(
        string="Reason String", 
        help="String why the assessment was necessary.")                
    method_id = fields.Many2one(
        comodel_name="hc.vs.risk.assessment.method", 
        string="Method", 
        help="Evaluation mechanism.")                
    basis_ids = fields.One2many(
        comodel_name="hc.risk.assessment.basis", 
        inverse_name="risk_assessment_id", 
        string="Basis", 
        help="Information used in assessment.")                
    mitigation = fields.Text(
        string="Mitigation", 
        help="How to reduce risk.")                
    note_id = fields.Many2one(
        comodel_name="hc.risk.assessment.note", 
        string="Note", 
        help="Comments on the risk assessment.")                
    prediction_ids = fields.One2many(
        comodel_name="hc.risk.assessment.prediction", 
        inverse_name="risk_assessment_id", 
        string="Predictions", 
        help="Outcome predicted.")                

class RiskAssessmentPrediction(models.Model):    
    _name = "hc.risk.assessment.prediction"    
    _description = "Risk Assessment Prediction"        

    risk_assessment_id = fields.Many2one(
        comodel_name="hc.res.risk.assessment", 
        string="Risk Assessment", 
        help="Risk Assessment associated with this Risk Assessment Prediction.")                
    outcome_id = fields.Many2one(
        comodel_name="hc.vs.risk.assessment.outcome", 
        string="Outcome", 
        required="True", 
        help="Possible outcome for the subject.")                
    probability_type = fields.Selection(
        string="Probability Type",
        selection=[
            ("decimal", "Decimal"), 
            ("Range", "Range"), 
            ("code", "Code")],
        help="Type of likelihood of specified outcome.")                
    probability_name = fields.Char(
        string="Probability", 
        compute="_compute_probability_name", 
        store="True", 
        help="Likelihood of specified outcome")                
    probability_decimal = fields.Float(
        string="Probability Decimal", 
        help="Decimal likelihood of specified outcome.")                
    probability_range_low = fields.Float(
        string="Probability Range Low", 
        help="Low limit of likelihood of specified outcome.")                
    probability_range_high = fields.Float(
        string="Probability Range High", 
        help="High limit of likelihood of specified outcome.")                
    probability_code_id = fields.Many2one(
        comodel_name="hc.vs.risk.probability", 
        string="Probability Code", 
        help="Code of likelihood of specified outcome.")                
    relative_risk = fields.Float(
        string="Relative Risk", 
        help="Relative likelihood.")                
    when_start_date = fields.Datetime(
        string="When Start Date", 
        help="Start of the timeframe or age range.")                
    when_end_date = fields.Datetime(
        string="When End Date", 
        help="End of the timeframe or age range.")                
    when_range_low = fields.Float(
        string="When Range Low", 
        help="Low limit of timeframe or age range.")                
    when_range_high = fields.Float(
        string="When Range High", 
        help="High limit of timeframe or age range.")                
    rationale = fields.Text(
        string="Rationale", 
        help="Explanation of prediction.")                

class RiskAssessmentBasis(models.Model):    
    _name = "hc.risk.assessment.basis"    
    _description = "Risk Assessment Basis"        
    _inherit = ["hc.basic.association"]

    risk_assessment_id = fields.Many2one(
        comodel_name="hc.res.risk.assessment", 
        string="Risk Assessment", 
        help="Risk Assessment associated with this Risk Assessment Basis.")                
    basis_type = fields.Selection(
        string="Basis Type", 
        selection=[
            ("string", "String"), 
            ("code", "Code")], 
        help="Type of information used in assessment.")                
    basis_name = fields.Char(
        string="Basis", 
        compute="_compute_basis_name", 
        store="True", 
        help="Information used in assessment.")                
    basis_string = fields.Char(
        string="Basis String", 
        help="Information used in assessment.")                
    basis_code_id = fields.Many2one(
        comodel_name="hc.vs.risk.assessment.basis", 
        string="Basis Code", 
        help="Code of information used in assessment.")                

class RiskAssessmentIdentifier(models.Model):    
    _name = "hc.risk.assessment.identifier"    
    _description = "Risk Assessment Identifier"        
    _inherit = ["hc.basic.association", "hc.identifier"]

    risk_assessment_id = fields.Many2one(
        comodel_name="hc.res.risk.assessment", 
        string="Risk Assessment", 
        help="Risk Assessment associated with this Risk Assessment Identifier.")                

class RiskAssessmentNote(models.Model):    
    _name = "hc.risk.assessment.note"    
    _description = "Risk Assessment Note"        
    _inherit = ["hc.basic.association", "hc.annotation"]

class RiskAssessmentMethod(models.Model):    
    _name = "hc.vs.risk.assessment.method"    
    _description = "Risk Assessment Method"        
    _inherit = ["hc.value.set.contains"]

class RiskAssessmentOutcome(models.Model):    
    _name = "hc.vs.risk.assessment.outcome"    
    _description = "Risk Assessment Outcome"        
    _inherit = ["hc.value.set.contains"]

class RiskAssessmentReason(models.Model):    
    _name = "hc.vs.risk.assessment.reason"    
    _description = "Risk Assessment Reason"        
    _inherit = ["hc.value.set.contains"]

class RiskAssessmentType(models.Model):    
    _name = "hc.vs.risk.assessment.type"    
    _description = "Risk Assessment Type"        
    _inherit = ["hc.value.set.contains"]

class RiskAssessmentBasis(models.Model):    
    _name = "hc.vs.risk.assessment.basis"    
    _description = "Risk Assessment Basis"        
    _inherit = ["hc.value.set.contains"]

class RiskProbability(models.Model):    
    _name = "hc.vs.risk.probability"    
    _description = "Risk Probability"        
    _inherit = ["hc.value.set.contains"]

