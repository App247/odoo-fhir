# -*- coding: utf-8 -*-

from openerp import models, fields, api

class Flag(models.Model):	
    _name = "hc.res.flag"	
    _description = "Flag"			

    identifier_ids = fields.One2many(
        comodel_name="hc.flag.identifier", 
        inverse_name="flag_id", 
        string="Identifiers", 
        help="Business identifier.")					
    category_id = fields.Many2one(
        comodel_name="hc.vs.flag.category", 
        string="Category", 
        help="Clinical, administrative, etc.")					
    status = fields.Selection(
        string="Flag Status", 
        required="True", 
        selection=[
            ("active", "Active"), 
            ("inactive", "Inactive"), 
            ("entered-in-error", "Entered In Error")], 
        help="Indicates whether this flag is active and needs to be displayed to a user, or whether it is no longer needed or entered in error.")					
    start_date = fields.Datetime(
        string="Start Date", 
        help="Start of the time period when flag is active.")					
    end_date = fields.Datetime(
        string="End Date", 
        help="End of the time period when flag is active.")					
    subject_type = fields.Selection(
        string="Subject Type",
        required="True", 
        selection=[
            ("Patient", "Patient"), 
            ("Location", "Location"), 
            ("Group", "Group"), 
            ("Organization", "Organization"), 
            ("Practitioner", "Practitioner"), 
            ("Plan Definition", "Plan Definition"), 
            ("Medication", "Medication"), 
            ("Procedure", "Procedure")], 
        help="Type of Who/What is flag about.")
    subject_name = fields.Char(
        string="Subject", 
        compute="_compute_subject_name", 
        help="Who/What is flag about.")
    subject_patient_id = fields.Many2one(
        comodel_name="hc.res.patient", 
        string="Subject Patient", 
        help="Patient who/what is flag about.")
    subject_location_id = fields.Many2one(
        comodel_name="hc.res.location", 
        string="Subject Location", 
        help="Location who/what is flag about.")
    subject_group_id = fields.Many2one(
        comodel_name="hc.res.group", 
        string="Subject Group", 
        help="Group who/what is flag about.")
    subject_organization_id = fields.Many2one(
        comodel_name="hc.res.organization", 
        string="Subject Organization", 
        help="Organization who/what is flag about.")
    subject_practitioner_id = fields.Many2one(
        comodel_name="hc.res.practitioner", 
        string="Subject Practitioner", 
        help="Practitioner who/what is flag about.")
    subject_plan_definition_id = fields.Many2one(
        comodel_name="hc.res.plan.definition", 
        string="Subject Plan Definition", 
        help="Plan Definition who/what is flag about.")
    subject_medication_id = fields.Many2one(
        comodel_name="hc.res.medication", 
        string="Subject Medication", 
        help="Medication who/what is flag about.")
    subject_procedure_id = fields.Many2one(
        comodel_name="hc.res.procedure", 
        string="Subject Procedure", 
        help="Procedure who/what is flag about.")				
    encounter_id = fields.Many2one(
        comodel_name="hc.res.encounter", 
        string="Encounter", 
        help="Alert relevant during encounter.")					
    author_type = fields.Selection(
        string="Author Type", 
        selection=[
            ("device", "Device"),
            ("organization", "Organization"),
            ("patient", "Patient"),
            ("practitioner", "Practitioner")],
        help="Type of flag creator.")					
    author_name = fields.Char(
        string="Author", 
        compute="_compute_author_name", 
        help="Flag creator.")					
    author_device_id = fields.Many2one(
        comodel_name="hc.res.device", 
        string="Author Device", 
        help="Device flag creator.")					
    author_organization_id = fields.Many2one(
        comodel_name="hc.res.organization", 
        string="Author Organization", 
        help="Organization flag creator.")					
    author_patient_id = fields.Many2one(
        comodel_name="hc.res.patient", 
        string="Author Patient", 
        help="Patient flag creator.")					
    author_practitioner_id = fields.Many2one(
        comodel_name="hc.res.practitioner", 
        string="Author Practitioner", 
        help="Practitioner flag creator.")					
    code_id = fields.Many2one(
        comodel_name="hc.vs.flag.code", 
        string="Code", 
        required="True", 
        help="Partially deaf, Requires easy open caps, No permanent address, etc.")					

    @api.multi          
    def _compute_subject_name(self):            
        for hc_res_flag in self:        
            if hc_res_flag.subject_type == 'Patient':   
                hc_res_flag.subject_name = hc_res_flag.subject_patient_id.name
            elif hc_res_flag.subject_type == 'Location':    
                hc_res_flag.subject_name = hc_res_flag.subject_location_id.name
            elif hc_res_flag.subject_type == 'Group':   
                hc_res_flag.subject_name = hc_res_flag.subject_group_id.name
            elif hc_res_flag.subject_type == 'Organization':    
                hc_res_flag.subject_name = hc_res_flag.subject_organization_id.name
            elif hc_res_flag.subject_type == 'Practitioner':    
                hc_res_flag.subject_name = hc_res_flag.subject_practitioner_id.name
            elif hc_res_flag.subject_type == 'Plan Definition': 
                hc_res_flag.subject_name = hc_res_flag.subject_plan_definition_id.name
            elif hc_res_flag.subject_type == 'Medication':  
                hc_res_flag.subject_name = hc_res_flag.subject_medication_id.name
            elif hc_res_flag.subject_type == 'Procedure':   
                hc_res_flag.subject_name = hc_res_flag.subject_procedure_id.name

    @api.multi          
    def _compute_author_name(self):         
        for hc_res_flag in self:        
            if hc_res_flag.author_type == 'Device': 
                hc_res_flag.author_name = hc_res_flag.author_device_id.name
            elif hc_res_flag.author_type == 'Organization': 
                hc_res_flag.author_name = hc_res_flag.author_organization_id.name
            elif hc_res_flag.author_type == 'Patient':  
                hc_res_flag.author_name = hc_res_flag.author_patient_id.name
            elif hc_res_flag.author_type == 'Practitioner': 
                hc_res_flag.author_name = hc_res_flag.author_practitioner_id.name

class FlagIdentifier(models.Model): 
    _name = "hc.flag.identifier"    
    _description = "Flag Identifier"        
    _inherit = ["hc.basic.association", "hc.identifier"]    

    flag_id = fields.Many2one(
        comodel_name="hc.res.flag", 
        string="Flag", 
        help="Flag associated with this Flag Identifier.")                 

class FlagCategory(models.Model):	
    _name = "hc.vs.flag.category"	
    _description = "Flag Category"		
    _inherit = ["hc.value.set.contains"]	

class FlagCode(models.Model):	
    _name = "hc.vs.flag.code"	
    _description = "Flag Code"		
    _inherit = ["hc.value.set.contains"]	
