# -*- coding: utf-8 -*-

from openerp import models, fields, api

class AdverseEvent(models.Model):    
    _name = "hc.res.adverse.event"    
    _description = "Adverse Event"                

    name = fields.Char(
        string="Event Name", 
        compute="_compute_name", 
        store="True", 
        help="Text representation of the adverse event. Subject Name + Adverse Event + Date.")
    identifier_id = fields.Many2one(
        comodel_name="hc.adverse.event.identifier", 
        string="Identifier", 
        help="Identifier.")                        
    category = fields.Selection(
        string="Adverse Event Category", 
        selection=[
            ("ae", "AE"), 
            ("pae", "PAE")], 
        help="What occurred and caused harm to the subject, or had the potential to cause harm to the subject.")                        
    type_id = fields.Many2one(
        comodel_name="hc.vs.adverse.event.type", 
        string="Type", 
        help="This element defines the specific type of event that occurred or that was prevented from occuring.")                        
    subject_type = fields.Selection(
        string="Subject Type", 
        selection=[
            ("patient", "Patient"), 
            ("research_subject", "Research Subject"), 
            ("medication", "Medication"), 
            ("device", "Device")], 
        help="Type of subject or group impacted by event.")                        
    subject_name = fields.Char(
        string="Subject", 
        compute="_compute_subject_name", 
        store="True", 
        help="Subject or group impacted by event.")                        
    subject_patient_id = fields.Many2one(
        comodel_name="hc.res.patient", 
        string="Subject Patient", 
        help="Patient subject or group impacted by event.")                        
    subject_related_person_id = fields.Many2one(
        comodel_name="hc.res.related.person", 
        string="Subject Related Person", 
        help="Related Person subject or group impacted by event.")                        
    subject_medication_id = fields.Many2one(
        comodel_name="hc.res.medication", 
        string="Subject Medication", 
        help="Medication subject or group impacted by event.")                        
    subject_device_id = fields.Many2one(
        comodel_name="hc.res.device", 
        string="Subject Device", 
        help="Device subject or group impacted by event.")                        
    date = fields.Datetime(
        string="Date", 
        help="Date.")                        
    reaction_ids = fields.One2many(
        comodel_name="hc.adverse.event.reaction", 
        inverse_name="adverse_event_id", 
        string="Reactions", 
        help="Adverse Reaction Events linked to exposure to substance.")                        
    location_id = fields.Many2one(
        comodel_name="hc.res.location", 
        string="Location", 
        help="Location.")                        
    seriousness_id = fields.Many2one(
        comodel_name="hc.vs.adverse.event.seriousness", 
        string="Seriousness", 
        help="Overall seriousness of this event for the patient.")                        
    outcome = fields.Selection(
        string="Outcome", 
        selection=[
            ("resolved", "Resolved"), 
            ("recovering", "Recovering"), 
            ("ongoing", "Ongoing"), 
            ("resolvedwithsequelae", "Resolved with Sequelae"), 
            ("fatal", "Fatal"), 
            ("unknown", "Unknown")], 
            help="Indicates whether the care team is currently active, suspended, inactive, or entered in error.")                        
    recorder_type = fields.Selection(
        string="Recorder Type", 
        selection=[
            ("patient", "Patient"), 
            ("research_subject", "Research Subject"), 
            ("medication", "Medication"), 
            ("device", "Device")], 
        help="Type of recorder.")                        
    recorder_name = fields.Char(
        string="Recorder", 
        compute="_compute_recorder_name", 
        store="True", 
        help="Recorder.")                        
    recorder_patient_id = fields.Many2one(
        comodel_name="hc.res.patient", 
        string="Recorder Patient", 
        help="Patient recorder.")                        
    recorder_practitioner_id = fields.Many2one(
        comodel_name="hc.res.practitioner", 
        string="Recorder Practitioner", 
        help="Practitioner recorder.")                        
    recorder_related_person_id = fields.Many2one(
        comodel_name="hc.res.related.person", 
        string="Recorder Related Person", 
        help="Related Person recorder.")                        
    event_type = fields.Selection(
        string="Event Type", 
        selection=[
            ("practitioner", "Practitioner"), 
            ("device", "Device")], 
        help="Type of who was involved in the adverse event or the potential adverse event.")                        
    event_participant_name = fields.Char(
        string="Event Participant", 
        compute="_compute_event_participant_name", 
        store="True", 
        help="Who was involved in the adverse event or the potential adverse event.")                        
    event_participant_practitioner_id = fields.Many2one(
        comodel_name="hc.res.practitioner", 
        string="Event Participant Practitioner", 
        help="Practitioner who was involved in the adverse event or the potential adverse event.")                        
    event_participant_device_id = fields.Many2one(
        comodel_name="hc.res.device", 
        string="Event Participant Device", 
        help="Device who was involved in the adverse event or the potential adverse event.")                        
    description = fields.Text(
        string="Description", 
        help="Description.")                        
    subject_medical_history_ids = fields.One2many(
        comodel_name="hc.adverse.event.subject.medical.history", 
        inverse_name="adverse_event_id", 
        string="Subject Medical Histories", 
        help="Subject medical history.")                        
    reference_document_ids = fields.One2many(
        comodel_name="hc.adverse.event.reference.document", 
        inverse_name="adverse_event_id", 
        string="Reference Documents", 
        help="Reference document.")                        
    study_ids = fields.One2many(
        comodel_name="hc.adverse.event.study", 
        inverse_name="adverse_event_id", 
        string="Studies", 
        help="Study.")                        
    suspect_entity_ids = fields.One2many(
        comodel_name="hc.adverse.event.suspect.entity", 
        inverse_name="adverse_event_id", 
        string="Suspect Entities", 
        help="Suspect Entity.")                        

    @api.depends('subject_type')            
    def _compute_subject_name(self):            
        for hc_res_adverse_event in self:       
            if hc_res_adverse_event.subject_type == 'patient':  
                hc_res_adverse_event.subject_name = hc_res_adverse_event.subject_patient_id.name
            elif hc_res_adverse_event.subject_type == 'research_subject':   
                hc_res_adverse_event.subject_name = hc_res_adverse_event.subject_research_subject_id.name
            elif hc_res_adverse_event.subject_type == 'medication': 
                hc_res_adverse_event.subject_name = hc_res_adverse_event.subject_medication_id.name
            elif hc_res_adverse_event.subject_type == 'device': 
                hc_res_adverse_event.subject_name = hc_res_adverse_event.subject_device_id.name

    @api.depends('recorder_type')           
    def _compute_recorder_name(self):           
        for hc_res_adverse_event in self:       
            if hc_res_adverse_event.recorder_type == 'patient': 
                hc_res_adverse_event.recorder_name = hc_res_adverse_event.recorder_patient_id.name
            elif hc_res_adverse_event.recorder_type == 'research_subject':  
                hc_res_adverse_event.recorder_name = hc_res_adverse_event.recorder_research_subject_id.name
            elif hc_res_adverse_event.recorder_type == 'medication':    
                hc_res_adverse_event.recorder_name = hc_res_adverse_event.recorder_medication_id.name
            elif hc_res_adverse_event.recorder_type == 'device':    
                hc_res_adverse_event.recorder_name = hc_res_adverse_event.recorder_device_id.name

    @api.depends('event_type')          
    def _compute_event_name(self):          
        for hc_res_adverse_event in self:       
            if hc_res_adverse_event.event_type == 'practitioner':   
                hc_res_adverse_event.event_name = hc_res_adverse_event.event_practitioner_id.name
            elif hc_res_adverse_event.event_type == 'device':   
                hc_res_adverse_event.event_name = hc_res_adverse_event.event_device_id.name

class AdverseEventSuspectEntity(models.Model):    
    _name = "hc.adverse.event.suspect.entity"    
    _description = "Adverse Event Suspect Entity"                

    adverse_event_id = fields.Many2one(
        comodel_name="hc.res.adverse.event", 
        string="Adverse Event", 
        help="Adverse Event associated with this Adverse Event Suspect Entity.")                        
    instance_type = fields.Selection(
        string="Instance Type", 
        required="True", 
        selection=[
            ("substance", "Substance"), 
            ("medication", "Medication"), 
            ("medication_administration", "Medication Administration"), 
            ("medication_statement", "Medication Statement"), 
            ("device", "Device")], 
        help="Type of suspect entity instance.")                        
    instance_name = fields.Char(
        string="Instance", 
        compute="_compute_instance_name", 
        store="True", 
        help="Suspect entity instance.")                        
    instance_substance_id = fields.Many2one(
        comodel_name="hc.res.substance", 
        string="Instance Substance", 
        help="Substance suspect entity instance.")                        
    instance_medication_id = fields.Many2one(
        comodel_name="hc.res.medication", 
        string="Instance Medication", 
        help="Medication suspect entity instance.")                        
    instance_medication_administration_id = fields.Many2one(
        comodel_name="hc.res.medication.administration", 
        string="Instance Medication Administration", 
        help="Medication Administration suspect entity instance.")                        
    instance_medication_statement_id = fields.Many2one(
        comodel_name="hc.res.medication.statement", 
        string="Instance Medication Statement", 
        help="Medication Statement suspect entity instance.")                        
    instance_device_id = fields.Many2one(
        comodel_name="hc.res.device", 
        string="Instance Device", 
        help="Device suspect entity instance.")                        
    causality = fields.Selection(
        string="Suspect Entity Causality", 
        selection=[
            ("causality1", "Causality1"), 
            ("causality2", "Causality2")], 
        help="The type of participant in the action.")                        
    causality_assessment_id = fields.Many2one(
        comodel_name="hc.vs.adverse.event.causality.assess", 
        string="Causality Assessment", 
        help="Causality assesment.")                        
    causality_product_relatedness = fields.Text(
        string="Causality Product Relatedness", 
        help="Suspect entity causality product relatedness.")                        
    causality_method_id = fields.Many2one(
        comodel_name="hc.vs.adverse.event.causality.method", 
        string="Causality Method", 
        help="Causality method.")                        
    causality_author_type = fields.Selection(
        string="Causality Author Type", 
        selection=[
            ("practitioner", "Practitioner"), 
            ("practitioner_role", "Practitioner Role")], 
        help="Type of entity causality author.")                        
    causality_author_name = fields.Char(
        string="Causality Author", 
        compute="_compute_causality_author_name", 
        store="True", 
        help="Suspect entity causality author.")                        
    causality_author_practitioner_id = fields.Many2one(
        comodel_name="hc.res.practitioner", 
        string="Causality Author Practitioner", 
        help="Practitioner suspect entity causality author.")                        
    causality_author_practitioner_role_id = fields.Many2one(
        comodel_name="hc.res.practitioner.role", 
        string="Causality Author Practitioner Role", 
        help="Practitioner Role suspect entity causality author.")                        
    causality_result_id = fields.Many2one(
        comodel_name="hc.vs.adverse.event.causality.result", 
        string="Causality Result", 
        help="Causality result.")                        

    @api.depends('instance_type')           
    def _compute_instance_name(self):           
        for hc_adverse_event_suspect_entity in self:        
            if hc_adverse_event_suspect_entity.instance_type == 'substance':    
                hc_adverse_event_suspect_entity.instance_name = hc_adverse_event_suspect_entity.instance_substance_id.name
            elif hc_adverse_event_suspect_entity.instance_type == 'medication': 
                hc_adverse_event_suspect_entity.instance_name = hc_adverse_event_suspect_entity.instance_medication_id.name
            elif hc_adverse_event_suspect_entity.instance_type == 'medication_administration':  
                hc_adverse_event_suspect_entity.instance_name = hc_adverse_event_suspect_entity.instance_medication_administration_id.name
            elif hc_adverse_event_suspect_entity.instance_type == 'medication_statement':   
                hc_adverse_event_suspect_entity.instance_name = hc_adverse_event_suspect_entity.instance_medication_statement_id.name
            elif hc_adverse_event_suspect_entity.instance_type == 'device': 
                hc_adverse_event_suspect_entity.instance_name = hc_adverse_event_suspect_entity.instance_device_id.name

    @api.depends('causality_author_type')           
    def _compute_causality_author_name(self):           
        for hc_adverse_event_suspect_entity in self:        
            if hc_adverse_event_suspect_entity.causality_author_type == 'practitioner': 
                hc_adverse_event_suspect_entity.causality_author_name = hc_adverse_event_suspect_entity.causality_author_practitioner_id.name
            elif hc_adverse_event_suspect_entity.causality_author_type == 'practitioner_role':  
                hc_adverse_event_suspect_entity.causality_author_name = hc_adverse_event_suspect_entity.causality_author_practitioner_role_id.name

class AdverseEventIdentifier(models.Model):    
    _name = "hc.adverse.event.identifier"    
    _description = "Adverse Event Identifier"            
    _inherit = ["hc.basic.association", "hc.identifier"]    

class AdverseEventReaction(models.Model):    
    _name = "hc.adverse.event.reaction"    
    _description = "Adverse Event Reaction"            
    _inherit = ["hc.basic.association"]    

    adverse_event_id = fields.Many2one(
        comodel_name="hc.res.adverse.event", 
        string="Adverse Event", 
        help="Adverse Event associated with this Adverse Event Reaction.")                        
    reaction_id = fields.Many2one(
        comodel_name="hc.res.condition", 
        string="Reaction", 
        help="Condition associated with this Adverse Event Reaction.")                        

class AdverseEventSubjectMedicalHistory(models.Model):    
    _name = "hc.adverse.event.subject.medical.history"    
    _description = "Adverse Event Subject Medical History"            
    _inherit = ["hc.basic.association"]    

    adverse_event_id = fields.Many2one(
        comodel_name="hc.res.adverse.event", 
        string="Adverse Event", 
        help="Adverse Event associated with this Adverse Event Subject Medical History.")                        
    subject_medical_history_type = fields.Selection(
        string="Subject Medical History Type", 
        selection=[
            ("condition", "Condition"), 
            ("observation", "Observation"), 
            ("allergy_intolerance", "Allergy Intolerance"), 
            ("family_member_history", "Family Member History"), 
            ("immunization", "Immunization"), 
            ("procedure", "Procedure")], 
        help="Type of entity causality author.")                        
    subject_medical_history_name = fields.Char(
        string="Subject Medical History", 
        compute="_compute_subject_medical_history_name", 
        store="True", 
        help="Subject medical history.")                        
    subject_medical_history_condition_id = fields.Many2one(
        comodel_name="hc.res.condition", 
        string="Subject Medical History Condition", 
        help="Condition subject medical history.")                        
    subject_medical_history_observation_id = fields.Many2one(
        comodel_name="hc.res.observation", 
        string="Subject Medical History Observation", 
        help="Observation subject medical history.")                        
    subject_medical_history_allergy_intolerance_id = fields.Many2one(
        comodel_name="hc.res.allergy.intolerance", 
        string="Subject Medical History Allergy Intolerance", 
        help="Allergy Intolerance subject medical history.")                        
    subject_medical_history_family_member_history_id = fields.Many2one(
        comodel_name="hc.res.family.member.history", 
        string="Subject Medical History Family Member History", 
        help="Family Member History subject medical history.")                        
    subject_medical_history_immunization_id = fields.Many2one(
        comodel_name="hc.res.immunization", 
        string="Subject Medical History Immunization", 
        help="Immunization subject medical history.")                        
    subject_medical_history_procedure_id = fields.Many2one(
        comodel_name="hc.res.procedure", 
        string="Subject Medical History Procedure", 
        help="Procedure subject medical history.")                        

    @api.depends('subject_medical_history_type')            
    def _compute_subject_medical_history_name(self):            
        for hc_adverse_event_subject_medical_history in self:       
            if hc_adverse_event_subject_medical_history.subject_medical_history_type == 'condition':    
                hc_adverse_event_subject_medical_history.subject_medical_history_name = hc_adverse_event_subject_medical_history.subject_medical_history_condition_id.name
            elif hc_adverse_event_subject_medical_history.subject_medical_history_type == 'observation':    
                hc_adverse_event_subject_medical_history.subject_medical_history_name = hc_adverse_event_subject_medical_history.subject_medical_history_observation_id.name
            elif hc_adverse_event_subject_medical_history.subject_medical_history_type == 'allergy_intolerance':    
                hc_adverse_event_subject_medical_history.subject_medical_history_name = hc_adverse_event_subject_medical_history.subject_medical_history_allergy_intolerance_id.name
            elif hc_adverse_event_subject_medical_history.subject_medical_history_type == 'family_member_history':  
                hc_adverse_event_subject_medical_history.subject_medical_history_name = hc_adverse_event_subject_medical_history.subject_medical_history_family_member_history_id.name
            elif hc_adverse_event_subject_medical_history.subject_medical_history_type == 'immunization':   
                hc_adverse_event_subject_medical_history.subject_medical_history_name = hc_adverse_event_subject_medical_history.subject_medical_history_immunization_id.name
            elif hc_adverse_event_subject_medical_history.subject_medical_history_type == 'procedure':  
                hc_adverse_event_subject_medical_history.subject_medical_history_name = hc_adverse_event_subject_medical_history.subject_medical_history_procedure_id.name

class AdverseEventReferenceDocument(models.Model):    
    _name = "hc.adverse.event.reference.document"    
    _description = "Adverse Event Reference Document"            
    _inherit = ["hc.basic.association"]    

    adverse_event_id = fields.Many2one(
        comodel_name="hc.res.adverse.event", 
        string="Adverse Event", 
        help="Adverse Event associated with this Adverse Event Reference Document.")                        
    reference_document_id = fields.Many2one(
        comodel_name="hc.res.document.reference", 
        string="Reference Document", 
        help="Document Reference associated with this Adverse Event Reference Document.")                        

class AdverseEventStudy(models.Model):    
    _name = "hc.adverse.event.study"    
    _description = "Adverse Event Study"            
    _inherit = ["hc.basic.association"]    

    adverse_event_id = fields.Many2one(
        comodel_name="hc.res.adverse.event", 
        string="Adverse Event", 
        help="Adverse Event associated with this Adverse Event Study.")                        
    study_id = fields.Many2one(
        comodel_name="hc.res.research.study", 
        string="Study", 
        help="Research Study associated with this Adverse Event Study.")                        

class AdverseEventType(models.Model):    
    _name = "hc.vs.adverse.event.type"    
    _description = "Adverse Event Type"            
    _inherit = ["hc.value.set.contains"]    

    name = fields.Char(
        string="Name", 
        help="Name of this adverse event type.")                        
    code = fields.Char(
        string="Code", 
        help="Code of this adverse event type.")                        
    contains_id = fields.Many2one(
        comodel_name="hc.vs.adverse.event.type", 
        string="Contains", 
        help="Parent adverse event type.")                        

class AdverseEventSeriousness(models.Model):    
    _name = "hc.vs.adverse.event.seriousness"    
    _description = "Adverse Event Seriousness"            
    _inherit = ["hc.value.set.contains"]    

    name = fields.Char(
        string="Name", 
        help="Name of this adverse event seriousness.")                        
    code = fields.Char(
        string="Code", 
        help="Code of this adverse event seriousness.")                        
    contains_id = fields.Many2one(
        comodel_name="hc.vs.adverse.event.seriousness", 
        string="Contains", 
        help="Parent adverse event seriousness.")                        

class AdverseEventCausalityAssess(models.Model):    
    _name = "hc.vs.adverse.event.causality.assess"    
    _description = "Adverse Event Causality Assess"            
    _inherit = ["hc.value.set.contains"]    

    name = fields.Char(
        string="Name", 
        help="Name of this adverse event causality assess.")                        
    code = fields.Char(
        string="Code", 
        help="Code of this adverse event causality assess.")                        
    contains_id = fields.Many2one(
        comodel_name="hc.vs.adverse.event.causality.assess", 
        string="Contains", 
        help="Parent adverse event causality assess.")                        

class AdverseEventCausalityMethod(models.Model):    
    _name = "hc.vs.adverse.event.causality.method"    
    _description = "Adverse Event Causality Method"            
    _inherit = ["hc.value.set.contains"]    

    name = fields.Char(
        string="Name", 
        help="Name of this adverse event causality method.")                        
    code = fields.Char(
        string="Code", 
        help="Code of this adverse event causality method.")                        
    contains_id = fields.Many2one(
        comodel_name="hc.vs.adverse.event.causality.method", 
        string="Contains", 
        help="Parent adverse event causality method.")                        

class AdverseEventCausalityResult(models.Model):    
    _name = "hc.vs.adverse.event.causality.result"    
    _description = "Adverse Event Causality Result"            
    _inherit = ["hc.value.set.contains"]    

    name = fields.Char(
        string="Name", 
        help="Name of this adverse event causality result.")                        
    code = fields.Char(
        string="Code", 
        help="Code of this adverse event causality result.")                        
    contains_id = fields.Many2one(
        comodel_name="hc.vs.adverse.event.causality.result", 
        string="Contains", 
        help="Parent adverse event causality result.")                        
