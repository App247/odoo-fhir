# -*- coding: utf-8 -*-

from openerp import models, fields, api

class ImagingStudy(models.Model):    
    _name = "hc.res.imaging.study"    
    _description = "Imaging Study"
  
    name = fields.Char(
        string="Event Name", 
        compute="_compute_name", 
        store="True", 
        help="Text representation of the procedure request event. Patient Name + UID + Started Date.")
    uid = fields.Char(
        string="UID", 
        required="True", 
        help="Formal identifier for the study (0020,000D).")                
    accession_id = fields.Many2one(
        comodel_name="hc.imaging.study.accession", 
        string="Accession Identifier", 
        help="Accession Number (0008,0050).")                
    identifier_ids = fields.One2many(
        comodel_name="hc.imaging.study.identifier", 
        inverse_name="imaging_study_id", 
        string="Identifiers", 
        help="Other identifiers for the study (0020,0010).")                
    availability = fields.Selection(
        string="Imaging Study Availability", 
        selection=[
            ("online", "Online"), 
            ("offline", "Offline"), 
            ("nearline", "Nearline"), 
            ("unavailable (0008,0056)", "Unavailable (0008,0056)")], 
        help="Availability of study (online, offline or nearline).")                
    modality_list_ids = fields.Many2many(
        comodel_name="hc.vs.dicom.cid.29", 
        relation="imaging_study_modality_list_rel", 
        string="Modality Lists", 
        help="All series modality if actual acquisition modalities.")
    patient_id = fields.Many2one(
        comodel_name="hc.res.patient", 
        string="Patient", 
        required="True", 
        help="Who the images are of.")                
    context_type = fields.Selection(
        string="Context Type", 
        selection=[
            ("encounter", "Encounter"), 
            ("episode_of_care", "Episode Of Care")], 
        help="Type of originating context.")                
    context_name = fields.Char(
        string="Context", 
        compute="_compute_context_name", 
        store="True", 
        help="Originating context.")                
    context_encounter_id = fields.Many2one(
        comodel_name="hc.res.encounter", 
        string="Context Encounter", 
        help="Encounter originating context.")                
    context_episode_of_care_id = fields.Many2one(
        comodel_name="hc.res.episode.of.care", 
        string="Context Episode Of Care", 
        help="Episode Of Care originating context.")                
    started = fields.Datetime(
        string="Started Date", 
        help="When the study was started (0008,0020)+(0008,0030).")                
    based_on_ids = fields.One2many(
        comodel_name="hc.imaging.study.based.on", 
        inverse_name="imaging_study_id", 
        string="Based On", 
        help="Request fulfilled.")                
    referrer_id = fields.Many2one(
        comodel_name="hc.res.practitioner", 
        string="Referrer", 
        help="Referring physician (0008,0090).")                
    interpreter_id = fields.Many2one(
        comodel_name="hc.res.practitioner", 
        string="Interpreter", 
        help="Who interpreted images (0008,1060).")                
    number_of_series = fields.Integer(
        string="Number Of Series", 
        required="True", 
        help="Number of Study Related Series.")                
    number_of_instances = fields.Integer(
        string="Number Of Instances", 
        required="True", 
        help="Number of Series Related Instances.")                
    procedure_ids = fields.One2many(
        comodel_name="hc.imaging.study.procedure", 
        inverse_name="imaging_study_id", 
        string="Procedures", 
        help="Type of procedure performed.")                
    reason_id = fields.Many2one(
        comodel_name="hc.vs.imaging.study.reason", 
        string="Reason", 
        help="Reason for study.")                
    description = fields.Text(
        string="Description", 
        help="Institution-generated description (0008,1030).")                
    base_location_ids = fields.One2many(
        comodel_name="hc.imaging.study.base.location", 
        inverse_name="imaging_study_id", 
        string="Base Locations", 
        help="Study access service endpoint.")                
    series_ids = fields.One2many(
        comodel_name="hc.imaging.study.series", 
        inverse_name="imaging_study_id", 
        string="Series", 
        help="Each study has one or more series of instances.")                

class ImagingStudyBaseLocation(models.Model):
    _name = "hc.imaging.study.base.location"    
    _description = "Imaging Study Base Location"

    imaging_study_id = fields.Many2one(
        comodel_name="hc.res.imaging.study", 
        string="Imaging Study", 
        help="Imaging study associated with this Imaging Study Base Location.")                
    type_id = fields.Many2one(
        comodel_name="hc.vs.d.web.type", 
        string="Type", 
        required="True", 
        help="The service type for accessing (e.g., retrieving, viewing) the DICOM instances.")                
    url = fields.Char(
        string="URI", 
        required="True", 
        help="Study access URL.")                

class ImagingStudySeries(models.Model):    
    _name = "hc.imaging.study.series"    
    _description = "Imaging Study Series"        

    imaging_study_id = fields.Many2one(
        comodel_name="hc.res.imaging.study", 
        string="Imaging Study", 
        help="Imaging study associated with this series.")                
    uid = fields.Char(
        string="UID", 
        required="True", 
        help="Formal identifier for this series (0020,000E).")                
    number = fields.Integer(
        string="Number", 
        help="Numeric identifier of this series (0020,0011).")                
    modality_id = fields.Many2one(
        comodel_name="hc.vs.dicom.cid.29", 
        string="Modality", 
        required="True", 
        help="The modality of the instances in the series (0008,0060).")                
    description = fields.Text(
        string="Description", 
        help="A description of the series (0008,103E).")                
    number_of_instances = fields.Integer(
        string="Number Of Instances", 
        required="True", 
        help="Number of Series Related Instances (0020,1209).")                
    availability = fields.Selection(
        string="Series Availability", 
        selection=[
            ("online", "Online"), 
            ("offline", "Offline"), 
            ("nearline", "Nearline"), 
            ("unavailable (0008,0056)", "Unavailable (0008,0056)")], 
        help="Availability of study (online, offline or nearline).")                
    body_site_id = fields.Many2one(
        comodel_name="hc.vs.body.site", 
        string="Body Site", 
        help="Body part examined (Map from 0018,0015).")                
    laterality_id = fields.Many2one(
        comodel_name="hc.vs.body.site.laterality", 
        string="Laterality", 
        help="Body part laterality.")                
    date_time = fields.Datetime(
        string="Date Time", 
        help="When the series started.")                
    base_location_ids = fields.One2many(
        comodel_name="hc.imaging.study.series.base.location", 
        inverse_name="series_id", 
        string="Base Locations", 
        help="Series access endpoint.")                
    instance_ids = fields.One2many(
        comodel_name="hc.imaging.study.series.instance", 
        inverse_name="series_id", 
        string="Instances", 
        help="A single SOP instance from the series.")                

class ImagingStudySeriesBaseLocation(models.Model):
    _name = "hc.imaging.study.series.base.location" 
    _description = "Imaging Study Series Base Location"

    series_id = fields.Many2one(
        comodel_name="hc.imaging.study.series", 
        string="Imaging Study Series", 
        help="Imaging study series associated with this Imaging Study Series Base Location.")                
    type_id = fields.Many2one(
        comodel_name="hc.vs.d.web.type", 
        string="Type", 
        required="True", 
        help="The service type for accessing (e.g., retrieving, viewing) the DICOM instances.")           
    url = fields.Char(
        string="URI", 
        required="True", 
        help="Series access URL.")                

class ImagingStudySeriesInstance(models.Model):    
    _name = "hc.imaging.study.series.instance"    
    _description = "Imaging Study Series Instance"

    series_id = fields.Many2one(
        comodel_name="hc.imaging.study.series", 
        string="Imaging Study Series", 
        help="Imaging study series associated with this instance.")                
    uid = fields.Char(
        string="UID", 
        required="True", 
        help="Formal identifier for this instance (0008,0018).")                
    number = fields.Integer(
        string="Number", 
        help="The number of this instance in the series (0020,0013).")                
    sop_class = fields.Char(
        string="SOP Class", 
        required="True", 
        help="DICOM class type.")                
    title = fields.Char(
        string="Title", 
        help="Description.")                

class ImagingStudyAccession(models.Model):    
    _name = "hc.imaging.study.accession"    
    _description = "Imaging Study Accession"        
    _inherit = ["hc.identifier"]

class ImagingStudyBasedOn(models.Model):    
    _name = "hc.imaging.study.based.on"    
    _description = "Imaging Study Based On"        
    _inherit = ["hc.basic.association"]

    imaging_study_id = fields.Many2one(
        comodel_name="hc.res.imaging.study", 
        string="Imaging Study", 
        help="Imaging study associated with this imaging study based on.")                
    based_on_type = fields.Selection(
        string="Based On Type", 
        selection=[
            ("referral_request", "Referral Request"),
            ("care_plan", "Care Plan"),
            ("diagnostic_request", "Diagnostic Request"),
            ("procedure_request", "Procedure Request")],
        help="Type of originating context.")
    based_on_name = fields.Char(
        string="Based On", 
        compute="_compute_based_on_name", 
        store="True", 
        help="Request fulfilled.")                
    based_on_referral_request_id = fields.Many2one(
        comodel_name="hc.res.referral.request", 
        string="Based On Referral Request", 
        help="Referral Request fulfilled.")                
    based_on_care_plan_id = fields.Many2one(
        comodel_name="hc.res.care.plan", 
        string="Based On Care Plan", 
        help="Care Plan request fulfilled.")                
    based_on_diagnostic_request_id = fields.Many2one(
        comodel_name="hc.res.diagnostic.request", 
        string="Based On Diagnostic Request", 
        help="Diagnostic Request fulfilled.")                
    based_on_procedure_request_id = fields.Many2one(
        comodel_name="hc.res.procedure.request", 
        string="Based On Procedure Request", 
        help="Procedure Request fulfilled.")                

class ImagingStudyIdentifier(models.Model):    
    _name = "hc.imaging.study.identifier"    
    _description = "Imaging Study Identifier"        
    _inherit = ["hc.basic.association", "hc.identifier"]

    imaging_study_id = fields.Many2one(
        comodel_name="hc.res.imaging.study", 
        string="Imaging Study", 
        help="Imaging study associated with this Imaging Study Identifier.")                              

class ImagingStudyProcedure(models.Model):    
    _name = "hc.imaging.study.procedure"    
    _description = "Imaging Study Procedure"        
    _inherit = ["hc.basic.association"]

    imaging_study_id = fields.Many2one(
        comodel_name="hc.res.imaging.study", 
        string="Imaging Study", 
        help="Imaging study associated with this Imaging Study Procedure.")                
    procedure_id = fields.Many2one(
        comodel_name="hc.res.procedure", 
        string="Procedure", 
        help="Procedure associated with this Imaging Study Procedure.")                

class BodySiteLaterality(models.Model):    
    _name = "hc.vs.body.site.laterality"    
    _description = "Body Site Laterality"        
    _inherit = ["hc.value.set.contains"]

class DICOMCID29(models.Model):    
    _name = "hc.vs.dicom.cid.29"    
    _description = "DICOM CID 29"        
    _inherit = ["hc.value.set.contains"]

class dWebType(models.Model):   
    _name = "hc.vs.d.web.type"  
    _description = "dWeb Type"     
    _inherit = ["hc.value.set.contains"]

class ImagingStudyReason(models.Model):    
    _name = "hc.vs.imaging.study.reason"    
    _description = "Imaging Study Reason"        
    _inherit = ["hc.value.set.contains"]
