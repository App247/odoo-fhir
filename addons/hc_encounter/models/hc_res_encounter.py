# -*- coding: utf-8 -*-

from openerp import models, fields, api

class Encounter(models.Model):  
    _name = "hc.res.encounter"  
    _description = "Encounter"      

    name = fields.Char(
        string="Name", 
        compute="_compute_name", 
        store="True", 
        help="Text representation of the encounter event. Patient Name + Encounter Type + Start Date.")
    identifier_ids = fields.One2many(
        comodel_name="hc.encounter.identifier", 
        inverse_name="encounter_id", 
        string="Identifiers", 
        help="Identifier(s) by which this encounter is known.")                
    status = fields.Selection(
        string="Encounter Status", 
        required="True", 
        selection=[
            ("planned", "Planned"), 
            ("arrived", "Arrived"), 
            ("in-progress", "In-Progress"), 
            ("onleave", "On Leave"), 
            ("finished", "Finished"), 
            ("cancelled", "Cancelled")], 
        help="Current state of the encounter.")             
    encounter_class = fields.Selection(
        string="Encounter Class", 
        selection=[
            ("inpatient", "Inpatient"), 
            ("outpatient", "Outpatient"), 
            ("ambulatory", "Ambulatory"), 
            ("emergency", "Emergency")], 
        help="Classification of the encounter.")             
    type_ids = fields.Many2many(
        comodel_name="hc.vs.encounter.type", 
        string="Types", 
        help="Specific type of encounter.")                
    priority_id = fields.Many2one(
        comodel_name="hc.vs.act.priority", 
        string="Priority", 
        help="Indicates the urgency of the encounter.")               
    patient_id = fields.Many2one(
        comodel_name="hc.res.patient", 
        string="Patient", 
        help="The patient present at the encounter.")             
    episode_of_care_ids = fields.One2many(
        comodel_name="hc.encounter.episode.of.care", 
        inverse_name="encounter_id", 
        string="Episodes of Care", 
        help="Episode(s) of care that this encounter should be recorded against.")              
    incoming_referral_ids = fields.One2many(
        comodel_name="hc.encounter.referral.request", 
        inverse_name="encounter_id", 
        string="Incoming Referrals", 
        help="The ReferralRequest that initiated this encounter.")             
    appointment_id = fields.Many2one(
        comodel_name="hc.res.appointment", 
        string="Appointment", 
        help="The appointment that scheduled this encounter.")                
    start_date = fields.Datetime(
        string="Start Date", 
        help="Start of the encounter.")               
    end_date = fields.Datetime(
        string="End Date", 
        help="End of the encounter.")                          
    length = fields.Float(
        string="Length", 
        help="Quantity of time the encounter lasted (less time absent).")
    length_uom_id = fields.Many2one(
        comodel_name="product.uom", 
        string="Length UOM", 
        domain="[('category_id','=','Time (UCUM)')]", 
        help="Length unit of measure.")
    reason_ids = fields.Many2many(
        comodel_name="hc.vs.encounter.reason", 
        string="Reasons", 
        help="Reason the encounter takes place (code).")             
    indication_ids = fields.One2many(
        comodel_name="hc.encounter.indication", 
        inverse_name="encounter_id", 
        string="Indications", 
        help="Reason the encounter takes place (resource).")               
    account_ids = fields.One2many(
        comodel_name="hc.encounter.account", 
        inverse_name="encounter_id", 
        string="Accounts", 
        help="The set of accounts that may be used for billing for this Encounter.")                
    service_provider_id = fields.Many2one(
        comodel_name="hc.res.organization", 
        string="Service Provider", 
        help="The custodian organization of this Encounter record.")               
    part_of_id = fields.Many2one(
        comodel_name="hc.res.encounter", 
        string="Part Of", 
        help="Another Encounter this encounter is part of.")                
    status_history_ids = fields.One2many(
        comodel_name="hc.encounter.status.history", 
        inverse_name="encounter_id", 
        string="Status History", 
        help="List of Encounter statuses.")              
    participant_ids = fields.One2many(
        comodel_name="hc.encounter.participant", 
        inverse_name="encounter_id", 
        string="Participants", 
        help="List of participants involved in the encounter.")              
    hospitalization_ids = fields.One2many(
        comodel_name="hc.encounter.hospitalization", 
        inverse_name="encounter_id", 
        string="Hospitalizations", 
        help="Details about an admission to a clinic.")              
    location_ids = fields.One2many(
        comodel_name="hc.encounter.location", 
        inverse_name="encounter_id", 
        string="Locations", 
        help="List of locations the patient has been at.")                

class EncounterStatusHistory(models.Model):    
    _name = "hc.encounter.status.history"    
    _description = "Encounter Status History"        

    encounter_id = fields.Many2one(
        comodel_name="hc.res.encounter", 
        string="Encounter", 
        help="Encounter associated with this Encounter Status History.")                
    status = fields.Selection(
        string="Status History Status", 
        required="True", 
        selection=[
            ("planned", "Planned"), 
            ("arrived", "Arrived"), 
            ("in-progress", "In-Progress"), 
            ("onleave", "Onleave"), 
            ("finished", "Finished"), 
            ("cancelled", "Cancelled")], 
        help="Current state of the encounter.")                
    start_date = fields.Datetime(
        string="Start Date", 
        required="True", 
        help="Start of the the time that the episode was in the specified status.")                
    end_date = fields.Datetime(
        string="End Date", 
        required="True", 
        help="End of the the time that the episode was in the specified status.")                

class EncounterParticipant(models.Model):    
    _name = "hc.encounter.participant"    
    _description = "Encounter Participant"        

    encounter_id = fields.Many2one(
        comodel_name="hc.res.encounter", 
        string="Encounter", 
        help="Encounter associated with this Encounter Participant.")                
    type_ids = fields.Many2many(
        comodel_name="hc.vs.encounter.participant.type", 
        string="Types", 
        help="Role of participant in encounter.")                
    start_date = fields.Datetime(
        string="Start Date", 
        help="Start of the period of time during the encounter participant was present.")                
    end_date = fields.Datetime(
        string="End Date", 
        help="End of the period of time during the encounter participant was present.")                
    individual_practitioner_id = fields.Many2one(
        comodel_name="hc.res.practitioner", 
        string="Individual Practitioner", 
        help="Practitioner involved in the encounter other than the patient.")                
    individual_related_person_id = fields.Many2one(
        comodel_name="hc.res.related.person", 
        string="Individual Related Person", 
        help="Related Person involved in the encounter other than the patient.")                

class EncounterHospitalization(models.Model):   
    _name = "hc.encounter.hospitalization"  
    _description = "Encounter Hospitalization"      

    encounter_id = fields.Many2one(
        comodel_name="hc.res.encounter", 
        string="Encounter", 
        help="Encounter associated with this Encounter Hospitalization.")             
    pre_admission_identifier_id = fields.Many2one(
        comodel_name="hc.encounter.hospitalization.pre.admission.identifier", 
        string="Encounter Hospitalization Pre-Admission Identifier", 
        help="Pre-admission identifier.")              
    origin_location_id = fields.Many2one(
        comodel_name="hc.res.location", 
        string="Origin Location", 
        help="The location from which the patient came before admission.")               
    admit_source_id = fields.Many2one(
        comodel_name="hc.vs.encounter.admit.source", 
        string="Admit Source", 
        help="From where patient was admitted (physician referral, transfer).")               
    admitting_diagnosis_ids = fields.One2many(
        comodel_name="hc.encounter.hospitalization.admitting.diagnosis", 
        inverse_name="encounter_hospitalization_id", 
        string="Encounter Hospitalization Admitting Diagnosis", 
        help="The admitting diagnosis as reported by admitting practitioner.")               
    re_admission_id = fields.Many2one(
        comodel_name="hc.vs.v2.readmission.indicator", 
        string="Re-Admission", 
        help="The type of hospital re-admission that has occurred (if any). If the value is absent, then this is not identified as a readmission.")             
    diet_preference_id = fields.Many2one(
        comodel_name="hc.vs.encounter.diet", 
        string="Diet Preference", 
        help="Diet preferences reported by the patient.")               
    special_courtesy_ids = fields.Many2many(
        comodel_name="hc.vs.special.courtesy", 
        string="Special Courtesies", 
        help="Special courtesies (VIP, board member).")               
    special_arrangement_ids = fields.Many2many(
        comodel_name="hc.vs.special.arrangements", 
        string="Special Arrangements", 
        elp="Wheelchair, translator, stretcher, etc.")              
    destination_location_id = fields.Many2one(
        comodel_name="hc.res.location", 
        string="Destination Location", 
        help="Location to which the patient is discharged.")               
    discharge_disposition_id = fields.Many2one(
        comodel_name="hc.vs.discharge.disposition", 
        string="Discharge Disposition", 
        help="Category or kind of location after discharge.")              
    discharge_diagnosis_ids = fields.One2many(
        comodel_name="hc.encounter.hospitalization.discharge.diagnosis", 
        inverse_name="encounter_hospitalization_id", 
        string="Encounter Hospitalization Discharge Diagnosis", 
        help="The final diagnosis given a patient before release from the hospital after all testing, surgery, and workup are complete.")                
                
class EncounterLocation(models.Model):  
    _name = "hc.encounter.location" 
    _description = "Encounter Location"

    encounter_id = fields.Many2one(
        comodel_name="hc.res.encounter", 
        string="Encounter", 
        help="Encounter associated with this Encounter Location.")                
    location_id = fields.Many2one(
        comodel_name="hc.res.location", 
        string="Location", 
        required="True", 
        help="Location the encounter takes place.")               
    status = fields.Selection(
        string="Location Status", 
        selection=[
            ("planned", "Planned"), 
            ("present", "Present"), 
            ("reserved", "Reserved")], 
        help="The status of the participants' presence at the specified location during the period specified.")               
    start_date = fields.Datetime(
        string="Start Date", 
        help="Start of the time period during which the patient was present at the location.")                
    end_date = fields.Datetime(
        string="End Date", 
        help="End of the time period during which the patient was present at the location.")              
                  
class EncounterIdentifier(models.Model):    
    _name = "hc.encounter.identifier"   
    _description = "Encounter Identifier"       
    _inherit = ["hc.basic.association", "hc.identifier"]

    encounter_id = fields.Many2one(
        comodel_name="hc.res.encounter", 
        string="Encounter", 
        help="Encounter associated with this Encounter Identifier.")                

class EncounterEpisodeOfCare(models.Model): 
    _name = "hc.encounter.episode.of.care"  
    _description = "Encounter Episode Of Care"      
    _inherit = ["hc.basic.association"]

    encounter_id = fields.Many2one(
        comodel_name="hc.res.encounter", 
        string="Encounter", 
        help="Encounter associated with this Encounter Episode Of Care.")             
    episode_of_care_id = fields.Many2one(
        comodel_name="hc.res.episode.of.care", 
        string="Episode Of Care", 
        help="Episode Of Care associated with this Encounter Episode Of Care.")               

class EncounterReferralRequest(models.Model):   
    _name = "hc.encounter.referral.request" 
    _description = "Encounter Referral Request"     
    _inherit = ["hc.basic.association"]

    encounter_id = fields.Many2one(
        comodel_name="hc.res.encounter", 
        string="Encounter", 
        help="Encounter associated with this Encounter Referral Request.")                
    # referral_request_id = fields.Many2one(
    #     comodel_name="hc.res.referral.request", 
    #     string="Referral Request", 
    #     help="Referral Request associated with this Encounter Referral Request.")               

class EncounterAccount(models.Model):   
    _name = "hc.encounter.account"  
    _description = "Encounter Account"      
    _inherit = ["hc.basic.association"]

    encounter_id = fields.Many2one(
        comodel_name="hc.res.encounter", 
        string="Encounter", 
        help="Encounter associated with this Encounter Account.")             
    account_id = fields.Many2one(
        comodel_name="hc.res.account", 
        string="Account", 
        help="Account associated with this Encounter Account.")               

class EncounterIndication(models.Model):    
    _name = "hc.encounter.indication"   
    _description = "Encounter Indication"       
    _inherit = ["hc.basic.association"]

    encounter_id = fields.Many2one(
        comodel_name="hc.res.encounter", 
        string="Encounter", 
        help="Encounter associated with this Encounter Indication.")                
    indication_type = fields.Selection(
        string="Indication Type", 
        selection=[
            ("Condition", "Condition"), 
            ("Procedure", "Procedure")], 
        help="Type of plan or agreement issuer.")             
    indication_name = fields.Char(
        string="Indication", 
        compute="compute_indication_name", 
        required="True", 
        help="Reason the encounter takes place (resource).")                
    # indication_condition_id = fields.Many2one(
    #     comodel_name="hc.res.condition", 
    #     string="Indication Condition", 
    #     help="Condition reason the encounter takes place (resource).")                
    # indication_procedure_id = fields.Many2one(
    #     comodel_name="hc.res.procedure", 
    #     string="Indication Procedure", 
    #     help="Procedure reason the encounter takes place (resource).")                

class EncounterHospitalizationPreAdmissionIdentifier(models.Model): 
    _name = "hc.encounter.hospitalization.pre.admission.identifier"   
    _description = "Encounter Hospitalization Pre-Admission Identifier"       
    _inherit = ["hc.basic.association", "hc.identifier"]            

class EncounterHospitalizationAdmittingDiagnosis(models.Model): 
    _name = "hc.encounter.hospitalization.admitting.diagnosis"  
    _description = "Encounter Hospitalization Admitting Diagnosis"      
    _inherit = ["hc.basic.association"]

    encounter_hospitalization_id = fields.Many2one(
        comodel_name="hc.encounter.hospitalization", 
        string="Encounter Hospitalization", 
        help="Hospitalization associated with this encounter hospitalization admitting diagnosis.")             
    # condition_id = fields.Many2one(
    #     comodel_name="hc.res.condition", 
    #     string="Condition", 
    #     help="Condition associated with this encounter hospitalization admitting diagnosis.")                

class EncounterHospitalizationDischargeDiagnosis(models.Model): 
    _name = "hc.encounter.hospitalization.discharge.diagnosis"  
    _description = "Encounter Hospitalization Discharge Diagnosis"      
    _inherit = ["hc.basic.association"]

    encounter_hospitalization_id = fields.Many2one(
        comodel_name="hc.encounter.hospitalization", 
        string="Encounter Hospitalization", 
        help="Hospitalization associated with this encounter hospitalization discharge diagnosis.")             
    # condition_id = fields.Many2one(
    #     comodel_name="hc.res.condition", 
    #     string="Condition", 
    #     help="Condition associated with this encounter hospitalization discharge diagnosis.")                

class EncounterParticipantType(models.Model):   
    _name = "hc.encounter.participant.type" 
    _description = "Encounter Participant Type"     
    _inherit = ["hc.basic.association"]

    encounter_hospitalization_id = fields.Many2one(
        comodel_name="hc.encounter.hospitalization", 
        string="Encounter Hospitalization", 
        help="Participant with this participant type.")             
    participant_type_id = fields.Many2one(
        comodel_name="hc.vs.encounter.participant.type", 
        string="Participant Type", 
        help="Participant Type associated with this participant.")              

class EncounterType(models.Model):  
    _name = "hc.vs.encounter.type"  
    _description = "Encounter Type"     
    _inherit = ["hc.value.set.contains"]

class ActPriority(models.Model):    
    _name = "hc.vs.act.priority"    
    _description = "Act Priority"       
    _inherit = ["hc.value.set.contains"]

class EncounterAdmitSource(models.Model):   
    _name = "hc.vs.encounter.admit.source"  
    _description = "Encounter Admit Source"     
    _inherit = ["hc.value.set.contains"]

class EncounterDiet(models.Model):  
    _name = "hc.vs.encounter.diet"  
    _description = "Encounter Diet"     
    _inherit = ["hc.value.set.contains"]

class SpecialCourtesy(models.Model):   
    _name = "hc.vs.special.courtesy"  
    _description = "Encounter Special Courtesy"     
    _inherit = ["hc.value.set.contains"]

class SpecialArrangements(models.Model):   
    _name = "hc.vs.special.arrangements"  
    _description = "Encounter Special Arrangements"     
    _inherit = ["hc.value.set.contains"]

class DischargeDisposition(models.Model):  
    _name = "hc.vs.discharge.disposition" 
    _description = "Encounter Discharge Disposition"        
    _inherit = ["hc.value.set.contains"]

class V2ReadmissionIndicator(models.Model): 
    _name = "hc.vs.v2.readmission.indicator"    
    _description = "V2 Readmission Indicator"       
    _inherit = ["hc.value.set.contains"]

# External Reference

class Condition(models.Model):    
    _inherit = "hc.res.condition"

    context_type = fields.Selection(
        string="Condition Context Type",
        selection=[
            ("encounter", "Encounter"), 
            ("episode_of_care", "Episode of Care")], 
        help="Type of encounter when condition first asserted.")                    
    context_encounter_id = fields.Many2one(
        comodel_name="hc.res.encounter", 
        string="Context Encounter", 
        help="Encounter when condition first asserted.")

    @api.multi          
    def _compute_context_name(self):            
        for hc_res_condition in self:       
            if hc_res_condition.context_type == 'encounter':
                hc_res_condition.context_name = hc_res_condition.context_encounter_id.name
            elif hc_res_condition.context_type == 'episode_of_care':  
                hc_res_condition.context_name = hc_res_condition.context_episode_of_care_id.name