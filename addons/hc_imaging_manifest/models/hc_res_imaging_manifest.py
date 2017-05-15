# -*- coding: utf-8 -*-

from openerp import models, fields, api

class ImagingManifest(models.Model):    
    _name = "hc.res.imaging.manifest"    
    _description = "Imaging Manifest"

    name = fields.Char(
        string="Event Name", 
        required="True", 
        help="Text representation of the imaging manifest event. Patient + UID + Authoring Date.")
    uid = fields.Char(
        string="UID", 
        required="True", 
        help="Instance UID.")                
    patient_id = fields.Many2one(
        comodel_name="hc.res.patient", 
        string="Patient", 
        required="True", 
        help="Patient of the selected objects.")                
    authoring_time = fields.Datetime(
        string="Authoring Time", 
        help="Authoring time of the selection.")                
    subject_type = fields.Selection(
        string="Subject Type", 
        selection=[
            ("Practitioner", "Practitioner"), 
            ("Device", "Device"), 
            ("Organization", "Organization"), 
            ("Patient", "Patient"), 
            ("Related Person", "Related Person")], 
        help="Type of author (human or machine).")                
    subject_name = fields.Char(
        string="Subject", 
        compute="_compute_subject_name", 
        store="True", 
        help="Author (human or machine).")                
    author_practitioner_id = fields.Many2one(
        comodel_name="hc.res.practitioner", 
        string="Author Practitioner", 
        help="Practitioner author (human or machine).")                
    author_device_id = fields.Many2one(
        comodel_name="hc.res.device", 
        string="Author Device", 
        help="Device author (human or machine).")                
    author_organization_id = fields.Many2one(
        comodel_name="hc.res.organization", 
        string="Author Organization", 
        help="Organization author (human or machine).")                
    author_patient_id = fields.Many2one(
        comodel_name="hc.res.patient", 
        string="Author Patient", 
        help="Patient author (human or machine).")                
    author_related_person_id = fields.Many2one(
        comodel_name="hc.res.related.person", 
        string="Author Related Person", 
        help="Related Person author (human or machine).")                
    title_id = fields.Many2one(
        comodel_name="hc.vs.kos.title", 
        string="Title", 
        required="True", 
        help="Reason for selection.")                
    description = fields.Text(
        string="Description", 
        help="Description text.")                
    study_ids = fields.One2many(
        comodel_name="hc.img.manif.study", 
        inverse_name="imaging_manifest_id", 
        string="Studies", 
        required="True", 
        help="Study identity of the selected instances.")                

    @api.multi          
    def _compute_subject_name(self):            
        for hc_res_imaging_manifest in self:        
            if hc_res_imaging_manifest.subject_type == 'Practitioner':  
                hc_res_imaging_manifest.subject_name = hc_res_imaging_manifest.subject_practitioner_id.name
            elif hc_res_imaging_manifest.subject_type == 'Device':  
                hc_res_imaging_manifest.subject_name = hc_res_imaging_manifest.subject_device_id.name
            elif hc_res_imaging_manifest.subject_type == 'Organization':    
                hc_res_imaging_manifest.subject_name = hc_res_imaging_manifest.subject_organization_id.name
            elif hc_res_imaging_manifest.subject_type == 'Patient': 
                hc_res_imaging_manifest.subject_name = hc_res_imaging_manifest.subject_patient_id.name
            elif hc_res_imaging_manifest.subject_type == 'Related Person':  
                hc_res_imaging_manifest.subject_name = hc_res_imaging_manifest.subject_related_person_id.name

class ImgManifStudy(models.Model):    
    _name = "hc.img.manif.study"    
    _description = "Imaging Manifest Study"        

    imaging_manifest_id = fields.Many2one(
        comodel_name="hc.res.imaging.manifest", 
        string="Imaging Manifest", 
        help="Imaging Manifest associated with this Imaging Manifest Study.")                
    uid = fields.Char(
        string="UID", 
        required="True", 
        help="Study instance UID.")                
    imaging_study_id = fields.Many2one(
        comodel_name="hc.res.imaging.study", 
        string="Imaging Study", 
        help="Imaging Study reference to Imaging Manifest Study.")                
    base_location_ids = fields.One2many(
        comodel_name="hc.img.manif.study.base.locn", 
        inverse_name="study_id", 
        string="Base Locations", 
        help="Study access service endpoint.")                
    series_ids = fields.One2many(
        comodel_name="hc.img.manif.study.series", 
        inverse_name="study_id", 
        string="Series", 
        required="True", 
        help="Series identity of the selected instances.")                

class ImgManifStudyBaseLocn(models.Model):    
    _name = "hc.img.manif.study.base.locn"    
    _description = "Imaging Manifest Study Base Locn"        

    study_id = fields.Many2one(
        comodel_name="hc.img.manif.study", 
        string="Imaging Manifest Study", 
        help="Imaging Manifest Study associated with this Study Base Location.")                
    type_id = fields.Many2one(
        comodel_name="hc.vs.d.web.type", 
        string="Type",
        required="True", 
        help="The service type for accessing (e.g., retrieving, viewing) the DICOM instances.")                
    url = fields.Char(
        string="URI", 
        required="True", 
        help="Study access URL.")
               
class ImgManifStudySeries(models.Model):    
    _name = "hc.img.manif.study.series"    
    _description = "Imaging Manifest Study Series"        

    study_id = fields.Many2one(
        comodel_name="hc.img.manif.study", 
        string="Imaging Manifest Study", 
        help="Imaging Manifest Study associated with this study series.")                
    uid = fields.Char(
        string="UID", 
        help="Study instance UID.")                
    base_location_ids = fields.One2many(
        comodel_name="hc.img.manif.study.series.base.locn", 
        inverse_name="series_id", 
        string="Base Locations", 
        help="Series access endpoint.")                
    instance_ids = fields.One2many(
        comodel_name="hc.img.manif.study.series.instance", 
        inverse_name="series_id", 
        string="Instances", 
        required="True", 
        help="The selected instance.")                

class ImgManifStudySeriesBaseLocn(models.Model):    
    _name = "hc.img.manif.study.series.base.locn"    
    _description = "Imaging Manifest Study Series Base Locn"        

    series_id = fields.Many2one(
        comodel_name="hc.img.manif.study.series", 
        string="Imaging Manifest Study Series", 
        help="Imaging Manifest Study Series associated with this Study Series Base Location.")                
    type_id = fields.Many2one(
        comodel_name="hc.vs.d.web.type", 
        string="Type",
        required="True",
        help="The service type for accessing (e.g., retrieving, viewing) the DICOM instances.")                
    url = fields.Char(
        string="URI", 
        required="True", 
        help="Series access URL.")                

class ImgManifStudySeriesInstance(models.Model):    
    _name = "hc.img.manif.study.series.instance"    
    _description = "Imaging Manifest Study Series Instance"        

    series_id = fields.Many2one(
        comodel_name="hc.img.manif.study.series", 
        string="Imaging Manifest Study Series", 
        help="Imaging Manifest Study Series associated with this study series instance.")                
    sop_class = fields.Char(
        string="SOP Class", 
        required="True", 
        help="SOP class UID of instance.")                
    uid = fields.Char(
        string="UID", 
        required="True", 
        help="UID of the selected instance.")                

class KOSTitle(models.Model):    
    _name = "hc.vs.kos.title"    
    _description = "KOS Title"        
    _inherit = ["hc.value.set.contains"]
