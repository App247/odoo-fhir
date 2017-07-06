# -*- coding: utf-8 -*-

from openerp import models, fields, api
from datetime import datetime
from openerp.tools import DEFAULT_SERVER_DATE_FORMAT as DF
from openerp.tools import DEFAULT_SERVER_DATETIME_FORMAT as DTF

class Encounter(models.Model):
    _name = "hc.res.encounter"
    _description = "Encounter"

    name = fields.Char(
        string="Name",
        compute="_compute_name",
        store="True",
        help="Text representation of the encounter event. Subject Name + Class + Start Date.")
    identifier_ids = fields.One2many(
        comodel_name="hc.encounter.identifier",
        inverse_name="encounter_id",
        string="Identifiers",
        help="Identifier(s) by which this encounter is known.")
    status = fields.Selection(
        string="Status",
        required="True",
        selection=[
            ("planned", "Planned"),
            ("arrived", "Arrived"),
            ("triaged", "Triaged"),
            ("in-progress", "In-Progress"),
            ("onleave", "On Leave"),
            ("finished", "Finished"),
            ("cancelled", "Cancelled"),
            ("entered-in-error", "Entered-In-Error"),
            ("unknown", "Unknown")],
        help="Current state of the encounter.")    
    class_id = fields.Many2one(
        comodel_name="hc.vs.act.code",
        string="Class",
        required="True",
        domain="[('subset_ids.name','=','Encounter Code')]",
        help="Classification of the encounter.")
    type_ids = fields.Many2many(
        comodel_name="hc.vs.encounter.type",
        relation="encounter_type_rel",
        string="Types",
        help="Specific type of encounter.")
    priority_id = fields.Many2one(
        comodel_name="hc.vs.act.priority",
        string="Priority",
        help="Indicates the urgency of the encounter.")
    subject_type = fields.Selection(
        string="Subject Type",
        required="True",
        selection=[
            ("patient", "Patient"),
            ("group", "Group")],
        help="The patient or group present at the encounter.")
    subject_name = fields.Char(
        string="Subject",
        compute="_compute_subject_name",
        store="True",
        help="The patient ro group present at the encounter.")
    subject_patient_id = fields.Many2one(
        comodel_name="hc.res.patient",
        string="Subject Patient",
        help="Patient present at the encounter.")
    subject_group_id = fields.Many2one(
        comodel_name="hc.res.group",
        string="Subject Group",
        help="Group present at the encounter.")
    episode_of_care_ids = fields.One2many(
        comodel_name="hc.encounter.episode.of.care",
        inverse_name="encounter_id",
        string="Episodes of Care",
        help="Episode(s) of care that this encounter should be recorded against.")
    incoming_referral_ids = fields.One2many(
        comodel_name="hc.encounter.incoming.referral",
        inverse_name="encounter_id",
        string="Incoming Referrals",
        help="The ProcedureRequest that initiated this encounter.")
    appointment_id = fields.Many2one(
        comodel_name="hc.res.appointment",
        string="Appointment",
        help="The appointment that scheduled this encounter.")
    start_date = fields.Datetime(
        string="Start Date",
        required="True",
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
    reason_ids = fields.One2many(
        comodel_name="hc.encounter.reason",
        inverse_name="encounter_id",
        string="Reasons",
        help="Reason the encounter takes place (code).")
    account_ids = fields.One2many(
        comodel_name="hc.encounter.account",
        inverse_name="encounter_id",
        string="Accounts",
        help="The set of accounts that may be used for billing for this Encounter.")
    service_provider_id = fields.Many2one(
        comodel_name="hc.res.organization",
        string="Service Provider",
        help="The custodian organization of this Encounter record.")
    
    # Extension attribute
    associated_encounter_id = fields.Many2one(
        comodel_name="hc.res.encounter", 
        string="Associated Encounter", 
        help="This encounter occurs within the scope of the referenced encounter.")
    mode_of_arrival_id = fields.Many2one(
        comodel_name="hc.vs.v2.mode.of.arrival", 
        string="Mode Of Arrival", 
        help="Identifies whether a patient arrives at the reporting facility via ambulance and the type of ambulance that was used.")
    reason_cancelled_id = fields.Many2one(
        comodel_name="hc.vs.encounter.reason.cancelled", 
        string="Reason Cancelled", 
        help="If the encountered was cancelled after it was planned, why? Applies only if the status is cancelled.")

    part_of_id = fields.Many2one(
        comodel_name="hc.res.encounter",
        string="Part Of",
        help="Another Encounter this encounter is part of.")
    status_history_ids = fields.One2many(
        comodel_name="hc.encounter.status.history",
        inverse_name="encounter_id",
        string="Status History",
        help="List of Encounter statuses.")
    class_history_ids = fields.One2many(
        comodel_name="hc.encounter.class.history",
        inverse_name="encounter_id",
        string="Class Histories",
        help="List of past encounter classes.")
    participant_ids = fields.One2many(
        comodel_name="hc.encounter.participant",
        inverse_name="encounter_id",
        string="Participants",
        help="List of participants involved in the encounter.")
    diagnosis_ids = fields.One2many(
        comodel_name="hc.encounter.diagnosis",
        inverse_name="encounter_id",
        string="Diagnosis",
        help="The list of diagnosis relevant to this encounter.")
    hospitalization_id = fields.Many2one(
        comodel_name="hc.encounter.hospitalization",
        string="Hospitalizations",
        help="Details about an admission to a clinic.")
    location_ids = fields.One2many(
        comodel_name="hc.encounter.location",
        inverse_name="encounter_id",
        string="Locations",
        help="List of locations the patient has been at.")

    @api.model                          
    def create(self, vals):                         
        status_history_obj = self.env['hc.encounter.status.history']                        
        class_history_obj = self.env['hc.encounter.class.history']                      
        res = super(Encounter, self).create(vals)                       
                                
        # For Status                        
        if vals and vals.get('status'):                     
            status_history_vals = {                 
                'encounter_id': res.id,             
                'status': res.status,               
                'start_date': datetime.today()              
                }               
            if vals.get('status') == 'entered-in-error':                    
                status_history_vals.update({'end_date': datetime.today()})              
            status_history_obj.create(status_history_vals)                  
                                
        # For Class                     
        if vals.get('status') != 'entered-in-error':                        
            if vals and vals.get('class_id'):                   
                class_history_vals = {              
                    'encounter_id': res.id,         
                    'encounter_class': res.class_id.name,           
                    'start_date': datetime.today()          
                    }           
                class_history_obj.create(class_history_vals)                
                                
        return res                      
                                
    @api.multi                          
    def write(self, vals):                          
        status_history_obj = self.env['hc.encounter.status.history']                        
        class_history_obj = self.env['hc.encounter.class.history']                      
        res = super(Encounter, self).write(vals)                        
                                
        # For Status                        
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
                    'encounter_id': self.id,            
                    'status': vals.get('status'),           
                    'start_date': datetime.today()          
                    }           
                if vals.get('status') == 'entered-in-error':                
                    status_history_vals.update({'end_date': datetime.today()})          
                status_history_obj.create(status_history_vals)              
                                
        # For Class                     
        class_history_record_ids = class_history_obj.search([('end_date','=', False)])                      
        if class_history_record_ids:                        
            if vals.get('status') == 'entered-in-error' or (vals.get('class_id') and class_history_record_ids[0].encounter_class != vals.get('class_id')):                 
                for class_history in class_history_record_ids:              
                    class_history.end_date = datetime.strftime(datetime.today(), DTF)           
                    time_diff = datetime.today() - datetime.strptime(class_history.start_date, DTF)         
                    if time_diff:           
                        days = str(time_diff).split(',')        
                        if days and len(days) > 1:      
                            class_history.time_diff_day = str(days[0])  
                            times = str(days[1]).split(':') 
                            if times and times > 1: 
                                class_history.time_diff_hour = str(times[0])
                                class_history.time_diff_min = str(times[1])
                                class_history.time_diff_sec = str(times[2])
                        else:       
                            times = str(time_diff).split(':')   
                            if times and times > 1: 
                                class_history.time_diff_hour = str(times[0])
                                class_history.time_diff_min = str(times[1])
                                class_history.time_diff_sec = str(times[2])
                    class_history_vals = {          
                        'encounter_id': self.id,        
                        'encounter_class': vals.get('class_id'),       
                        'start_date': datetime.today()      
                        }       
                    if vals.get('status') == 'entered-in-error':            
                        class_history_vals.update({'end_date': datetime.today()})       
                    if vals.get('status') != 'entered-in-error':            
                        class_history_obj.create(class_history_vals)        
        else:                       
            class_history_vals = {                  
                    'encounter_id': self.id,            
                    'encounter_class': vals.get('class_id'),           
                    'start_date': datetime.today()          
                    }           
            if vals.get('status') == 'entered-in-error':                    
                    class_history_vals.update({'end_date': datetime.today()})           
            class_history_obj.create(class_history_vals)                    
                                
        return res                      
                      
    @api.depends('subject_type')            
    def _compute_subject_name(self):            
        for hc_res_encounter in self:       
            if hc_res_encounter.subject_type == 'patient':  
                hc_res_encounter.subject_name = hc_res_encounter.subject_patient_id.name
            elif hc_res_encounter.subject_type == 'group':  
                hc_res_encounter.subject_name = hc_res_encounter.subject_group_id.name
 
    @api.depends('subject_name', 'start_date')          
    def _compute_name(self):            
        comp_name = '/'     
        for hc_res_encounter in self:
            if hc_res_encounter.subject_type == 'patient':
                comp_name = hc_res_encounter.subject_patient_id.name
                if hc_res_encounter.subject_patient_id.birth_date:
                    subject_patient_birth_date = datetime.strftime(datetime.strptime(hc_res_encounter.subject_patient_id.birth_date, DF), "%Y-%m-%d")
                    comp_name = comp_name + "("+ subject_patient_birth_date + ")"
            if hc_res_encounter.subject_type == 'group':
                    comp_name = hc_res_encounter.subject_group_id.name
            # if hc_res_encounter.type_id:   
            #     comp_name = comp_name + ", " + hc_res_encounter.type_id.name or ''
            if hc_res_encounter.start_date:
                subject_start_date =  datetime.strftime(datetime.strptime(hc_res_encounter.start_date, DTF), "%Y-%m-%d")
                comp_name = comp_name + ", " + subject_start_date
            hc_res_encounter.name = comp_name   

class EncounterStatusHistory(models.Model):
    _name = "hc.encounter.status.history"
    _description = "Encounter Status History"

    encounter_id = fields.Many2one(
        comodel_name="hc.res.encounter",
        string="Encounter",
        help="Encounter associated with this Encounter Status History.")
    status = fields.Char(
        string="Status",
        compute="_compute_status",
        store="True",
        help="Status of the encounter.")
    start_date = fields.Datetime(
        string="Start Date",
        required="True",
        help="Start of the the time that the episode was in the specified status.")
    end_date = fields.Datetime(
        string="End Date",
        help="End of the the time that the episode was in the specified status.")
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

class EncounterClassHistory(models.Model):
    _name = "hc.encounter.class.history"
    _description = "Encounter Class History"

    encounter_id = fields.Many2one(
        comodel_name="hc.res.encounter",
        string="Encounter",
        help="Encounter associated with this Encounter Class History.")
    encounter_class = fields.Char(
        string="Class",
        help="Class of the encounter.")
    start_date = fields.Datetime(
        string="Start Date",
        required="True",
        help="Start of the the time that the episode was in the specified class.")
    end_date = fields.Datetime(
        string="End Date",
        help="End of the the time that the episode was in the specified class.")
    time_diff_day = fields.Char(
        string="Time Diff (days)",
        help="Days duration of the class.")
    time_diff_hour = fields.Char(
        string="Time Diff (hours)",
        help="Hours duration of the class.")
    time_diff_min = fields.Char(
        string="Time Diff (minutes)",
        help="Minutes duration of the class.")
    time_diff_sec = fields.Char(
        string="Time Diff (seconds)",
        help="Seconds duration of the class.")

class EncounterParticipant(models.Model):
    _name = "hc.encounter.participant"
    _description = "Encounter Participant"

    encounter_id = fields.Many2one(
        comodel_name="hc.res.encounter",
        string="Encounter",
        help="Encounter associated with this Encounter Participant.")
    type_ids = fields.Many2many(
        comodel_name="hc.vs.encounter.participant.type",
        relation="encounter_participant_type_rel",
        string="Types",
        help="Role of participant in encounter.")
    start_date = fields.Datetime(
        string="Start Date",
        help="Start of the period of time during the encounter participant was present.")
    end_date = fields.Datetime(
        string="End Date",
        help="End of the period of time during the encounter participant was present.")
    individual_type = fields.Selection(
        string="Individual Type",
        selection=[
            ("practitioner", "Practitioner"),
            ("related_person", "Related Person")],
        help="Persons involved in the encounter other than the patient.")
    individual_name = fields.Char(
        string="Individual",
        compute="_compute_individual_name",
        store="True",
        help="Persons involved in the encounter other than the patient.")
    individual_practitioner_id = fields.Many2one(
        comodel_name="hc.res.practitioner",
        string="Individual Practitioner",
        help="Practitioner involved in the encounter other than the patient.")
    individual_related_person_id = fields.Many2one(
        comodel_name="hc.res.related.person",
        string="Individual Related Person",
        help="Related Person involved in the encounter other than the patient.")

    @api.depends('individual_type')         
    def _compute_individual_name(self):         
        for hc_encounter_participant in self:       
            if hc_encounter_participant.individual_type == 'practitioner':  
                hc_encounter_participant.individual_name = hc_encounter_participant.individual_practitioner_id.name
            elif hc_encounter_participant.individual_type == 'related_person':  
                hc_encounter_participant.individual_name = hc_encounter_participant.individual_related_person_id.name

class EncounterDiagnosis(models.Model):
    _name = "hc.encounter.diagnosis"
    _description = "Encounter Diagnosis"

    encounter_id = fields.Many2one(
        comodel_name="hc.res.encounter",
        string="Encounter",
        help="Encounter associated with this Encounter Diagnosis.")
    condition_type = fields.Selection(
        string="Condition Type",
        required="True",
        selection=[
            ("condition", "Condition")],
        help="Type of reason the encounter takes place (resource).")
    condition_name = fields.Char(
        string="Condition",
        compute="_compute_condition_name",
        store="True",
        help="Reason the encounter takes place (resource).")
    condition_condition_id = fields.Many2one(
        comodel_name="hc.res.condition",
        string="Condition Condition",
        help="Condition reason the encounter takes place (resource).")
    # condition_procedure_id = fields.Many2one(
    #     comodel_name="hc.res.procedure",
    #     string="Condition Procedure",
    #     help="Procedure reason the encounter takes place (resource).")
    role_id = fields.Many2one(
        comodel_name="hc.vs.diagnosis.role",
        string="Role",
        help="Role that this diagnosis has within the encounter (e.g. admission, billing, discharge _).")
    rank = fields.Integer(
        string="Rank",
        help="Ranking of the diagnosis (for each role type).")

    @api.depends('condition_type')          
    def _compute_condition_name(self):          
        for hc_encounter_diagnosis in self:     
            if hc_encounter_diagnosis.condition_type == 'condition':    
                hc_encounter_diagnosis.condition_name = hc_encounter_diagnosis.condition_condition_id.name
            # elif hc_encounter_diagnosis.condition_type == 'procedure':  
            #     hc_encounter_diagnosis.condition_name = hc_encounter_diagnosis.condition_procedure_id.name

class EncounterHospitalization(models.Model):
    _name = "hc.encounter.hospitalization"
    _description = "Encounter Hospitalization"

    name = fields.Char(
        string="Name",
        compute="_compute_name",
        store="True",
        help="Text representation of the encounter event. Admit Source + Pre-Admission Identifier + Origin.")
    pre_admission_identifier_id = fields.Many2one(
        comodel_name="hc.encounter.hospitalization.pre.admission.identifier",
        string="Encounter Hospitalization Pre-Admission Identifier",
        help="Pre-admission identifier.")
    origin_id = fields.Many2one(
        comodel_name="hc.res.location",
        string="Origin",
        help="The location from which the patient came before admission.")
    admit_source_id = fields.Many2one(
        comodel_name="hc.vs.encounter.admit.source",
        string="Admit Source",
        help="From where patient was admitted (physician referral, transfer).")
    re_admission_id = fields.Many2one(
        comodel_name="hc.vs.v2.readmission.indicator",
        string="Re-Admission",
        help="The type of hospital re-admission that has occurred (if any). If the value is absent, then this is not identified as a readmission.")
    diet_preference_ids = fields.Many2many(
        comodel_name="hc.vs.encounter.diet",
        relation="encounter_hospitalization_diet_preference_rel",
        string="Diet Preferences",
        help="Diet preferences reported by the patient.")
    special_courtesy_ids = fields.Many2many(
        comodel_name="hc.vs.encounter.special.courtesy",
        relation="encounter_hospitalization_special_courtesy_rel",
        string="Special Courtesies",
        help="Special courtesies (VIP, board member).")
    special_arrangement_ids = fields.Many2many(
        comodel_name="hc.vs.encounter.special.arrangements",
        relation="encounter_hospitalization_special_arrangement_rel",
        string="Special Arrangements",
        help="Wheelchair, translator, stretcher, etc.")
    destination_id = fields.Many2one(
        comodel_name="hc.res.location",
        string="Destination",
        help="Location to which the patient is discharged.")
    discharge_disposition_id = fields.Many2one(
        comodel_name="hc.vs.encounter.discharge.disposition",
        string="Discharge Disposition",
        help="Category or kind of location after discharge.")

    @api.depends('admit_source_id', 'origin_id', 'pre_admission_identifier_id')         
    def _compute_name(self):            
        comp_name = '/'     
        for hc_encounter_hospitalization in self:       
            if hc_encounter_hospitalization.admit_source_id:    
                comp_name = hc_encounter_hospitalization.admit_source_id.name or ''
            if hc_encounter_hospitalization.pre_admission_identifier_id:    
                comp_name = comp_name + ", " + hc_encounter_hospitalization.pre_admission_identifier_id.name or ''
            if hc_encounter_hospitalization.origin_id:  
                comp_name = comp_name + ", " + hc_encounter_hospitalization.origin_id.name or ''
            hc_encounter_hospitalization.name = comp_name   

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
            ("reserved", "Reserved"),
            ("completed", "Completed")],
        help="The status of the participants' presence at the specified location during the period specified.")
    start_date = fields.Datetime(
        string="Start Date",
        help="Start of the time period during which the patient was present at the location.")
    end_date = fields.Datetime(
        string="End Date",
        help="End of the time period during which the patient was present at the location.")
    status_history_ids = fields.One2many(
        comodel_name="hc.encounter.location.status.history",
        inverse_name="location_id",
        string="Location Status History",
        help="List of Encounter Location statuses.")

class EncounterLocationStatusHistory(models.Model):
    _name = "hc.encounter.location.status.history"
    _description = "Encounter Location Status History"

    location_id = fields.Many2one(
        comodel_name="hc.encounter.location",
        string="Location",
        help="List of locations the patient has been at.")
    status = fields.Char(
        string="Status",
        help="The status of the encounter location.")
    start_date = fields.Datetime(
        string="Start Date",
        help="Start of the the time that the episode was in the specified class.")
    end_date = fields.Datetime(
        string="End Date",
        help="End of the the time that the episode was in the specified class.")
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

class EncounterIncomingReferral(models.Model):
    _name = "hc.encounter.incoming.referral"
    _description = "Encounter Incoming Referral"
    _inherit = ["hc.basic.association"]

    encounter_id = fields.Many2one(
        comodel_name="hc.res.encounter",
        string="Encounter",
        help="Encounter associated with this Encounter Incoming Referral.")
    # incoming_referral_id = fields.Many2one(
    #     comodel_name="hc.res.procedure.request",
    #     string="Incoming Referral",
    #     help="Procedure Request associated with this Encounter Incoming Referral.")

class EncounterReason(models.Model):
    _name = "hc.encounter.reason"
    _description = "Encounter Reason"
    _inherit = ["hc.basic.association"]

    encounter_id = fields.Many2one(
        comodel_name="hc.res.encounter",
        string="Encounter",
        help="Encounter associated with this Encounter Reason.")
    reason_id = fields.Many2one(
        comodel_name="hc.vs.encounter.reason",
        string="Reason",
        help="Reason associated with this Encounter Reason.")
    primary_diagnosis = fields.Integer(
        string="Primary Diagnosis", 
        help="The order of diagnosis importance (1 = highest in importance), from the clinical perspective, may be used in billing.")

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

class EncounterHospitalizationPreAdmissionIdentifier(models.Model):
    _name = "hc.encounter.hospitalization.pre.admission.identifier"
    _description = "Encounter Hospitalization Pre-Admission Identifier"
    _inherit = ["hc.basic.association", "hc.identifier"]

class ActEncounterCode(models.Model):
    _name = "hc.vs.act.encounter.code"
    _description = "Act Encounter Code"
    _inherit = ["hc.value.set.contains"]

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

class EncounterType(models.Model):
    _name = "hc.vs.encounter.type"
    _description = "Encounter Type"
    _inherit = ["hc.value.set.contains"]

class EncounterDiet(models.Model):
    _name = "hc.vs.encounter.diet"
    _description = "Encounter Diet"
    _inherit = ["hc.value.set.contains"]

class EncounterSpecialCourtesy(models.Model):
    _name = "hc.vs.encounter.special.courtesy"
    _description = "Encounter Special Courtesy"
    _inherit = ["hc.value.set.contains"]

class V2ReadmissionIndicator(models.Model):
    _name = "hc.vs.v2.readmission.indicator"
    _description = "V2 Readmission Indicator"
    _inherit = ["hc.value.set.contains"]

class EncounterSpecialArrangements(models.Model):
    _name = "hc.vs.encounter.special.arrangements"
    _description = "Encounter Special Arrangements"
    _inherit = ["hc.value.set.contains"]

class EncounterDischargeDisposition(models.Model):
    _name = "hc.vs.encounter.discharge.disposition"
    _description = "Encounter Discharge Disposition"
    _inherit = ["hc.value.set.contains"]

class V2ModeOfArrival(models.Model):
    _name = "hc.vs.v2.mode.of.arrival"
    _description = "V2 Mode Of Arrival"
    _inherit = ["hc.value.set.contains"]

    name = fields.Char(
        string="Name", 
        help="Name of this v2 mode of arrival.")                              
    code = fields.Char(
        string="Code", 
        help="Code of this v2 mode of arrival.")                              
    contains_id = fields.Many2one(
        comodel_name="hc.vs.v2.mode.of.arrival", 
        string="Parent", 
        help="Parent v2 mode of arrival.")                              

class EncounterReasonCancelled(models.Model):
    _name = "hc.vs.encounter.reason.cancelled"
    _description = "Encounter Reason Cancelled"
    _inherit = ["hc.value.set.contains"]

    name = fields.Char(
        string="Name", 
        help="Name of this encounter reason cancelled.")                              
    code = fields.Char(
        string="Code", 
        help="Code of this encounter reason cancelled.")                              
    contains_id = fields.Many2one(
        comodel_name="hc.vs.encounter.reason.cancelled", 
        string="Parent", 
        help="Parent encounter reason cancelled.")                              

# External Reference

class Condition(models.Model):
    _inherit = "hc.res.condition"

    context_type = fields.Selection(
        string="Condition Context Type",
        selection_add=[
            ("encounter", "Encounter")],
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