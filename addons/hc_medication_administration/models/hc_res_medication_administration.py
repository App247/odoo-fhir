# -*- coding: utf-8 -*-

from openerp import models, fields, api

class MedicationAdministration(models.Model):   
    _name = "hc.res.medication.administration"  
    _description = "Medication Administration"      

    name = fields.Char(
        string="Event Name", 
        compute="_compute_name", 
        store="True", 
        help="Text representation of the medication administration event. Patient Name + Medication + Effective Time.")
    identifier_ids = fields.One2many(
        comodel_name="hc.medication.administration.identifier", 
        inverse_name="medication_administration_id", 
        string="Identifiers", 
        help="External identifier.")                
    status = fields.Selection(
        string="Medication Administration Status", 
        required="True", 
        selection=[
            ("in-progress", "In-Progress"), 
            ("on-hold", "On-Hold"), 
            ("completed", "Completed"), 
            ("entered-in-error", "Entered-In-Error"), 
            ("stopped", "Stopped")], 
        help="The status for the event.")               
    medication_type = fields.Selection(
        string="Medication Type", 
        required="True", 
        selection=[
            ("code", "Code"), 
            ("medication", "Medication")], 
        help="Type of what was administered.")                
    medication_name = fields.Char(
        string="Medication", 
        compute="_compute_medication_name", 
        store="True", 
        help="What was administered?")                
    medication_code_id = fields.Many2one(
        comodel_name="hc.vs.medication.code", 
        string="Medication Code", 
        help="Code of what was administered.")             
    medication_id = fields.Many2one(
        comodel_name="hc.res.medication", 
        string="Medication", 
        help="Medication administered.")             
    patient_id = fields.Many2one(
        comodel_name="hc.res.patient", 
        string="Patient", 
        required="True", 
        help="Who received medication?")             
    encounter_id = fields.Many2one(
        comodel_name="hc.res.encounter", 
        string="Encounter", 
        help="Encounter administered as part of.")              
    supporting_information_ids = fields.One2many(
        comodel_name="hc.medication.administration.supporting.information", 
        inverse_name="medication_administration_id", 
        string="Supporting Information", 
        help="Additional information to support administration.")                
    effective_time_type = fields.Selection(
        string="Effective Time Type", 
        required="True", 
        selection=[
            ("date_time", "Date Time"), 
            ("period", "Period")], 
        help="Type of start and end time of administration.")             
    effective_time_name = fields.Char(
        string="Effective Time", 
        compute="_compute_effective_time_name", 
        store="True", 
        help="Start and end time of administration.")              
    effective_date_time = fields.Datetime(
        string="Effective Date Time", 
        help="Date Time of administration.")             
    effective_time_start_date = fields.Datetime(
        string="Effective Time Start Date", 
        help="Start time of administration.")             
    effective_time_end_date = fields.Datetime(
        string="End Time End Date", 
        help="End time of administration.")               
    performer_type = fields.Selection(
        string="Performer Type", 
        selection=[
            ("practitioner", "Practitioner"), 
            ("patient", "Patient"), 
            ("related_person", "Related Person")], 
        help="Type of who administered substance.")                
    performer_name = fields.Char(
        string="Performer", 
        compute="_compute_performer_name", 
        store="True", 
        help="Who administered substance.")               
    performer_practitioner_id = fields.Many2one(
        comodel_name="hc.res.practitioner", 
        string="Performer Practitioner", 
        help="Practitioner who administered substance.")               
    performer_patient_id = fields.Many2one(
        comodel_name="hc.res.patient", 
        string="Performer Patient", 
        help="Patient who administered substance.")               
    performer_related_person_id = fields.Many2one(
        comodel_name="hc.res.related.person", 
        string="Performer Related Person", 
        help="Related Person who administered substance.")               
    reason_reference_ids = fields.One2many(
        comodel_name="hc.medication.administration.reason.reference", 
        inverse_name="medication_administration_id", 
        string="Reason References", 
        help="Condition or Observation that supports why the medication was administered.")               
    prescription_id = fields.Many2one(
        comodel_name="hc.res.medication.request", 
        string="Prescription", 
        help="Request administration performed against.")                
    is_not_given = fields.Boolean(
        string="Not Given", 
        help="True if medication not administered.")              
    reason_not_given_ids = fields.Many2many(
        comodel_name="hc.vs.reason.medication.not.given.code", 
        relation="medication_administration_reason_not_given_rel", 
        string="Reasons Not Given", 
        help="Reason administration not performed.")              
    reason_given_ids = fields.Many2many(
        comodel_name="hc.vs.reason.medication.given.code", 
        relation="medication_administration_reason_given_rel", 
        string="Reasons Given", 
        help="Reason administration performed.")              
    device_ids = fields.One2many(
        comodel_name="hc.medication.administration.device", 
        inverse_name="medication_administration_id", 
        string="Devices", 
        help="Device used to administer.")              
    note_ids = fields.One2many(
        comodel_name="hc.medication.administration.note", 
        inverse_name="medication_administration_id", 
        string="Notes", 
        help="Information about the administration.")             
    event_history_ids = fields.One2many(
        comodel_name="hc.medication.administration.event.history", 
        inverse_name="medication_administration_id", 
        string="Event Histories", 
        help="A list of events of interest in the lifecycle.")                
    dosage_ids = fields.One2many(
        comodel_name="hc.medication.administration.dosage", 
        inverse_name="medication_administration_id", 
        string="Dosages", 
        help="Details of how medication was taken.")                

class MedicationAdministrationDosage(models.Model): 
    _name = "hc.medication.administration.dosage"   
    _description = "Medication Administration Dosage"       

    medication_administration_id = fields.Many2one(
        comodel_name="hc.res.medication.administration", 
        string="Medication Administration", 
        help="Medication Administration associated with this Medication Administration Dosage.")                
    text = fields.Text(string="Text", 
        help="Dosage Instructions.")              
    site_code_id = fields.Many2one(
        comodel_name="hc.vs.approach.site.code", 
        string="Site Code", 
        help="Code of medication administered")             
    route_code_id = fields.Many2one(
        comodel_name="hc.vs.route.code", 
        string="Route Code", 
        help="Code of path of substance into body.")              
    method_code_id = fields.Many2one(
        comodel_name="hc.vs.administration.method.code", 
        string="Method Code", 
        help="Code of how drug was administered.")              
    quantity = fields.Float(
        string="Dose Quantity", 
        help="Amount of medication per dose.")               
    quantity_uom_id = fields.Many2one(
        comodel_name="product.uom", 
        string="Dose Quantity UOM", 
        help="Amount of medication per dose unit of measure.")             
    rate_type = fields.Selection(
        string="Rate Type", 
        selection=[
            ("ratio", "Ratio"), 
            ("quantity", "Quantity")], 
        help="Type of dose quantity per unit of time.")
    rate_name = fields.Char(
        string="Rate", 
        compute="_compute_rate_name", 
        store="True", 
        help="Dose quantity per unit of time.")
    rate_ratio_numerator = fields.Float(
        string="Rate Ratio Numerator", 
        help="Numerator value of dose quantity per unit of time.")
    rate_ratio_numerator_uom_id = fields.Many2one(
        comodel_name="product.uom", 
        string="Rate Ratio Numerator UOM", 
        help="Dose quantity per unit of time unit of measure.")
    rate_ratio_denominator = fields.Float(
        string="Rate Ratio Denominator", 
        help="Denominator value of dose quantity per unit of time.")
    rate_ratio_denominator_uom_id = fields.Many2one(
        comodel_name="product.uom", 
        string="Rate Ratio Denominator UOM", 
        help="Dose quantity per unit of time unit of measure.")
    rate_ratio = fields.Float(
        string="Rate Ratio", 
        compute="_compute_rate_ratio", 
        store="True", 
        help="Dose quantity per unit of time.")
    rate_ratio_uom = fields.Char(
        string="Rate Ratio UOM", 
        compute="_compute_rate_ratio_uom", 
        store="True", 
        help="Rate Ratio unit of measure.")
    rate_quantity = fields.Float(
        string="Rate Quantity", 
        help="Dose quantity per unit of time")
    rate_quantity_uom_id = fields.Many2one(
        comodel_name="product.uom", 
        string="Rate Quantity UOM", 
        help="Rate Quantity unit of measure.")
                    
class MedicationAdministrationIdentifier(models.Model): 
    _name = "hc.medication.administration.identifier"   
    _description = "Medication Administration Identifier"       
    _inherit = ["hc.basic.association", "hc.identifier"]

    medication_administration_id = fields.Many2one(
        comodel_name="hc.res.medication.administration", 
        string="Medication Administration", 
        help="Medication Administration associated with this Medication Administration Identifier.")                

class MedicationAdministrationSupportingInformation(models.Model):  
    _name = "hc.medication.administration.supporting.information"   
    _description = "Medication Administration Supporting Information"       
    _inherit = ["hc.basic.association"]

    medication_administration_id = fields.Many2one(
        comodel_name="hc.res.medication.administration", 
        string="Medication Administration", 
        help="Medication Administration associated with this Medication Administration Supporting Information.")                
    supporting_information_type = fields.Selection(
        string="Supporting Information Type", 
        selection=[
            ("string", "String"), 
            ("code", "Code")], 
        help="Type of information that supports the dispensing of the medication.")                
    supporting_information_name = fields.Char(
        string="Supporting Information", 
        compute="_compute_supporting_information_name", 
        store="True", 
        help="Additional information to support administration.")              
    supporting_info_string = fields.Char(
        string="Supporting Info String", 
        help="String of additional information to support administration.")               
    supporting_information_code_id = fields.Many2one(
        comodel_name="hc.vs.resource.type", 
        string="Supporting Information Code", 
        help="Type of resource of additional information to support administration.")                         
                    
class MedicationAdministrationReasonReference(models.Model):    
    _name = "hc.medication.administration.reason.reference" 
    _description = "Medication Administration Reason Reference"     
    _inherit = ["hc.basic.association"]

    medication_administration_id = fields.Many2one(
        comodel_name="hc.res.medication.administration", 
        string="Medication Administration", 
        help="Medication Administration associated with this Medication Administration Reason Reference.")              
    reason_reference_type = fields.Selection(
        string="Reason Reference Type", 
        selection=[
            ("condition", "Condition"), 
            ("observation", "Observation")], 
        help="Type of Condition or Observation that supports why the medication was administered.")                
    reason_reference_name = fields.Char(
        string="Reason Reference", 
        compute="_compute_reason_reference_name", 
        store="True", 
        help="Condition or Observation that supports why the medication was administered.")              
    reason_reference_condition_id = fields.Many2one(
        comodel_name="hc.res.condition", 
        string="Reason Reference Condition", 
        help="Condition that supports why the medication was administered.")              
    reason_reference_observation_id = fields.Many2one(
        comodel_name="hc.res.observation", 
        string="Reason Reference Observation", 
        help="Observation that supports why the medication was administered.")                         

class MedicationAdministrationDevice(models.Model): 
    _name = "hc.medication.administration.device"   
    _description = "Medication Administration Device"       
    _inherit = ["hc.basic.association"]

    medication_administration_id = fields.Many2one(
        comodel_name="hc.res.medication.administration", 
        string="Medication Administration", 
        help="Medication Administration associated with this Medication Administration Device.")                
    device_id = fields.Many2one(
        comodel_name="hc.res.device", 
        string="Device", 
        help="Device associated with this Medication Administration Device.")                

class MedicationAdministrationNote(models.Model):   
    _name = "hc.medication.administration.note" 
    _description = "Medication Administration Note"     
    _inherit = ["hc.basic.association", "hc.annotation"]

    medication_administration_id = fields.Many2one(
        comodel_name="hc.res.medication.administration", 
        string="Medication Administration", 
        help="Medication Administration associated with this Medication Administration Note.")  

class MedicationAdministrationEventHistory(models.Model):   
    _name = "hc.medication.administration.event.history"    
    _description = "Medication Administration Event History"        
    _inherit = ["hc.basic.association"]

    medication_administration_id = fields.Many2one(
        comodel_name="hc.res.medication.administration", 
        string="Medication Administration", 
        help="Medication Administration associated with this Medication Administration Event History.")             
    event_history_id = fields.Many2one(
        comodel_name="hc.res.provenance", 
        string="Event History", 
        help="Provenance associated with this Medication Administration Event History.")               

class ReasonMedicationNotGivenCode(models.Model):   
    _name = "hc.vs.reason.medication.not.given.code"    
    _description = "Reason Medication Not Given Code"       
    _inherit = ["hc.value.set.contains"]

class ReasonMedicationGivenCode(models.Model):  
    _name = "hc.vs.reason.medication.given.code"    
    _description = "Reason Medication Given Code"       
    _inherit = ["hc.value.set.contains"]
