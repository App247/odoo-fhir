# -*- coding: utf-8 -*-

from openerp import models, fields, api

class MedicationDispense(models.Model): 
    _name = "hc.res.medication.dispense"    
    _description = "Medication Dispense"        

    name = fields.Char(
        string="Event Name", 
        compute="_compute_name", 
        store="True", 
        help="Text representation of the medication dispense event. Subject Name + Medication + Handed Over Date.")
    identifier_id = fields.Many2one(
        comodel_name="hc.medication.dispense.identifier", 
        string="Identifier", 
        help="External identifier.")             
    part_of_ids = fields.One2many(
        comodel_name="hc.medication.dispense.part.of", 
        inverse_name="medication_dispense_id", 
        string="Part Of", 
        help="Event that dispense is part of.")
    status = fields.Selection(
        string="Status", 
        selection=[
            ("in-progress", "In-Progress"), 
            ("on-hold", "On-Hold"), 
            ("completed", "Completed"), 
            ("entered-in-error", "Entered-In-Error"), 
            ("stopped", "Stopped")], 
        help="A code specifying the state of the set of dispense events.")         
    category_id = fields.Many2one(
        comodel_name="hc.vs.medication.dispense.category", 
        string="Category", 
        help="Type of medication dispense")
    medication_type = fields.Selection(
        string="Medication Type", 
        required="True", 
        selection=[
            ("code", "Code"), 
            ("medication", "Medication")], 
        help="Type of what medication was supplied.")             
    medication_name = fields.Char(
        string="Medication", 
        compute="_compute_medication_name", 
        store="True", 
        help="What medication was supplied.")              
    medication_code_id = fields.Many2one(
        comodel_name="hc.vs.medication.code", 
        string="Medication Code", 
        help="Code of what medication was supplied.")              
    medication_id = fields.Many2one(
        comodel_name="hc.res.medication", 
        string="Medication", 
        help="What medication was supplied.")              
    subject_type = fields.Selection(
        string="Subject Type", 
        selection=[
            ("patient", "Patient"), 
            ("group", "Group")], 
        help="Type of who the dispense is for.")
    subject_name = fields.Char(
        string="Subject", 
        compute="_compute_subject_name", 
        store="True", 
        help="Who the dispense is for.")
    subject_patient_id = fields.Many2one(
        comodel_name="hc.res.patient", 
        string="Subject Patient", 
        help="Who the dispense is for.")
    subject_group_id = fields.Many2one(
        comodel_name="hc.res.group", 
        string="Subject Group", 
        help="Group who the dispense is for.")              
    context_type = fields.Selection(
        string="Context Type", 
        selection=[
            ("encounter", "Encounter"), 
            ("episode_of_care", "Episode Of Care")], 
        help="Encounter / Episode associated with event.")
    context_name = fields.Char(
        string="Context", 
        compute="_compute_context_name", 
        store="True", 
        help="Encounter / Episode associated with event.")
    context_encounter_id = fields.Many2one(
        comodel_name="hc.res.encounter", 
        string="Context Encounter", 
        help="Encounter associated with event.")
    context_episode_of_care_id = fields.Many2one(
        comodel_name="hc.res.episode.of.care", 
        string="Context Episode Of Care", 
        help="Episode Of Care associated with event.")
    supporting_information_ids = fields.One2many(
        comodel_name="hc.medication.dispense.supporting.information", 
        inverse_name="medication_dispense_id", 
        string="Supporting Informations", 
        help="Information that supports the dispensing of the medication.")                 
    authorizing_prescription_ids = fields.One2many(
        comodel_name="hc.medication.dispense.authorizing.prescription", 
        inverse_name="medication_dispense_id", 
        string="Authorizing Prescriptions", 
        help="Medication order that authorizes the dispense.")                
    type_id = fields.Many2one(
        comodel_name="hc.vs.act.pharmacy.supply.type", 
        string="Type", 
        help="Trial fill, partial fill, emergency fill, etc.")              
    quantity = fields.Float(
        string="Quantity", 
        help="Amount dispensed.")                
    quantity_uom_id = fields.Many2one(
        comodel_name="product.uom", 
        string="Quantity UOM", 
        help="Quantity unit of measure.")              
    days_supply = fields.Float(
        string="Days Supply", 
        help="Amount of medication expressed as a timing amount.")             
    when_prepared = fields.Datetime(
        string="When Prepared Date", 
        help="When product was packaged and reviewed.")              
    when_handed_over = fields.Datetime(
        string="When product was given out.", 
        help="Handover time.")               
    destination_id = fields.Many2one(
        comodel_name="hc.res.location", 
        string="Destination", 
        help="Where the medication was sent.")               
    receiver_ids = fields.One2many(
        comodel_name="hc.medication.dispense.receiver", 
        inverse_name="medication_dispense_id", 
        string="Receivers", 
        help="Who collected the medication.")             
    note_ids = fields.One2many(
        comodel_name="hc.medication.dispense.note", 
        inverse_name="medication_dispense_id", 
        string="Notes", 
        help="Information about the dispense.")               
    dosage_instruction_ids = fields.One2many(
        comodel_name="hc.medication.dispense.dosage.instruction", 
        inverse_name="medication_dispense_id", 
        string="Dosage Instructions", 
        help="Medicine administration instructions to the patient/caregiver.")              
    detected_issue_ids = fields.One2many(
        comodel_name="hc.medication.dispense.detected.issue", 
        inverse_name="medication_dispense_id", 
        string="Supporting Information", 
        help="Clinical Issue with action.")
    is_not_done = fields.Boolean(
        string="Is Not Done", 
        help="Whether the dispense was or was not performed.")
    not_done_reason_type = fields.Selection(
        string="Not Done Reason Type", 
        selection=[
            ("code", "Code"), 
            ("detected_issue", "Detected Issue")], 
        help="Type of why a dispense was not performed.")
    not_done_reason_name = fields.Char(
        string="Not Done Reason", 
        compute="_compute_not_done_reason_name", 
        store="True", 
        help="Why a dispense was not performed.")
    not_done_reason_code_id = fields.Many2one(
        comodel_name="hc.vs.medication.not.done.reason", 
        string="Not Done Reason Code", 
        help="Code of why a dispense was not performed.")
    not_done_reason_detected_issue_id = fields.Many2one(
        comodel_name="hc.res.detected.issue", 
        string="Not Done Reason Detected Issue", 
        help="Detected Issue why a dispense was not performed.")
    event_history_ids = fields.One2many(
        comodel_name="hc.medication.dispense.event.history", 
        inverse_name="medication_dispense_id", 
        string="Event Histories", 
        help="A list of events of interest in the lifecycle.")                
    performer_ids = fields.One2many(
        comodel_name="hc.medication.dispense.performer", 
        inverse_name="medication_dispense_id", 
        string="Performers", 
        help="Who performed event.")
    substitution_ids = fields.One2many(
        comodel_name="hc.medication.dispense.substitution", 
        inverse_name="medication_dispense_id", 
        string="Substitutions", 
        help="Deals with substitution of one medicine for another.")              

class MedicationDispensePerformer(models.Model):    
    _name = "hc.medication.dispense.performer"  
    _description = "Medication Dispense Performer"

    medication_dispense_id = fields.Many2one(
        comodel_name="hc.res.medication.dispense", 
        string="Medication Dispense", 
        help="Medication Dispense associated with this Medication Dispense Performer.")
    actor_type = fields.Selection(
        string="Actor Type", 
        required="True", 
        selection=[
            ("practitioner", "Practitioner"), 
            ("organization", "Organization"), 
            ("patient", "Patient"), 
            ("device", "Device"), 
            ("related_person", "Related Person")], 
        help="Type of individual who was performing.")
    actor_name = fields.Char(
        string="Actor", 
        compute="_compute_actor_name", 
        store="True", 
        help="Individual who was performing.")
    actor_practitioner_id = fields.Many2one(
        comodel_name="hc.res.practitioner", 
        string="Actor Practitioner", 
        required="True", 
        help="Practitioner who was performing.")
    actor_organization_id = fields.Many2one(
        comodel_name="hc.res.organization", 
        string="Actor Organization", 
        help="Organization who was performing.")
    actor_patient_id = fields.Many2one(
        comodel_name="hc.res.patient", 
        string="Actor Patient", 
        help="Patient who was performing.")
    actor_device_id = fields.Many2one(
        comodel_name="hc.res.device", 
        string="Actor Device", 
        help="Device that was performing.")
    actor_related_person_id = fields.Many2one(
        comodel_name="hc.res.related.person", 
        string="Actor Related Person", 
        help="Related Person who was performing.")
    on_behalf_of_id = fields.Many2one(
        comodel_name="hc.res.organization", 
        string="On Behalf Of", 
        help="Organization was acting for.")

class MedicationDispenseSubstitution(models.Model): 
    _name = "hc.medication.dispense.substitution"   
    _description = "Medication Dispense Substitution"       

    medication_dispense_id = fields.Many2one(
        comodel_name="hc.res.medication.dispense", 
        string="Medication Dispense", 
        help="Medication Dispense associated with this Medication Dispense Substitution.")                
    was_substituted = fields.Boolean(
        string="Was Substituted", 
        required="True", 
        help="Whether a substitution was or was not performed on the dispense.")
    type_id = fields.Many2one(
        comodel_name="hc.vs.act.substance.admin.substitution.code", 
        string="Type", 
        required="True", 
        help="Code signifying whether a different drug was dispensed from what was prescribed.")              
    reason_ids = fields.Many2many(
        comodel_name="hc.vs.substance.admin.substitution.reason", 
        relation="medication_dispense_substitution_reason_rel", 
        string="Reasons", 
        help="Why was substitution made.")                
    responsible_party_ids = fields.One2many(
        comodel_name="hc.medication.dispense.substitution.responsible.party", 
        inverse_name="substitution_id", 
        string="Responsible Parties", 
        help="Who is responsible for the substitution.")                

class MedicationDispenseIdentifier(models.Model):   
    _name = "hc.medication.dispense.identifier" 
    _description = "Medication Dispense Identifier"     
    _inherit = ["hc.basic.association", "hc.identifier"]

class MedicationDispensePartOf(models.Model):   
    _name = "hc.medication.dispense.part.of"    
    _description = "Medication Dispense Part Of"

    medication_dispense_id = fields.Many2one(
        comodel_name="hc.res.medication.dispense", 
        string="Medication Dispense", 
        help="Medication Dispense associated with this Medication Dispense Receiver.")        
    part_of_id = fields.Many2one(
        comodel_name="hc.res.procedure", 
        string="Part Of", 
        help="Procedure associated with this Medication Dispense Part Of.")     

class MedicationDispenseSupportingInformation(models.Model):    
    _name = "hc.medication.dispense.supporting.information" 
    _description = "Medication Dispense Supporting Information"     
    _inherit = ["hc.basic.association"]

    medication_dispense_id = fields.Many2one(
        comodel_name="hc.res.medication.dispense", 
        string="Medication Dispense", 
        help="Medication Dispense associated with this Medication Dispense Note.")                
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
        help="Information that supports the dispensing of the medication.")                
    supporting_info_string = fields.Char(
        string="Supporting Info String", 
        help="String of information that supports the dispensing of the medication.")             
    supporting_information_code_id = fields.Many2one(
        comodel_name="hc.vs.resource.type", 
        string="Supporting Information Code", 
        help="Type of resource of information that supports the dispensing of the medication.")              

class MedicationDispenseAuthorizingPrescription(models.Model):  
    _name = "hc.medication.dispense.authorizing.prescription"   
    _description = "Medication Dispense Authorizing Prescription"       
    _inherit = ["hc.basic.association"]

    medication_dispense_id = fields.Many2one(
        comodel_name="hc.res.medication.dispense", 
        string="Medication Dispense", 
        help="Medication Dispense associated with this Medication Dispense Authorizing Prescription.")                
    authorizing_prescription_id = fields.Many2one(
        comodel_name="hc.res.medication.request", 
        string="Authorizing Prescription", 
        help="Authorizing Prescription associated with this Medication Dispense Authorizing Prescription.")              

class MedicationDispenseReceiver(models.Model): 
    _name = "hc.medication.dispense.receiver"   
    _description = "Medication Dispense Receiver"       
    _inherit = ["hc.basic.association"]
    
    medication_dispense_id = fields.Many2one(
        comodel_name="hc.res.medication.dispense", 
        string="Medication Dispense", 
        help="Medication Dispense associated with this Medication Dispense Receiver.")                
    receiver_type = fields.Selection(
        string="Receiver Type", 
        selection=[
            ("patient", "Patient"), 
            ("practitioner", "Practitioner")], 
        help="Type of who collected the medication.")                
    receiver_name = fields.Char(
        string="Receiver", 
        compute="_compute_receiver_name", 
        store="True", 
        help="Who collected the medication.")                
    receiver_patient_id = fields.Many2one(
        comodel_name="hc.res.patient", 
        string="Receiver Patient", 
        help="Patient who collected the medication.")               
    receiver_practitioner_id = fields.Many2one(
        comodel_name="hc.res.practitioner", 
        string="Receiver Practitioner", 
        help="Practitioner who collected the medication.")               

class MedicationDispenseDetectedIssue(models.Model):    
    _name = "hc.medication.dispense.detected.issue" 
    _description = "Medication Dispense Detected Issue"

    medication_dispense_id = fields.Many2one(
        comodel_name="hc.res.medication.dispense", 
        string="Medication Dispense", 
        help="Medication Dispense associated with this .")        
    detected_issue_id = fields.Many2one(
        comodel_name="hc.res.detected.issue", 
        string="Detected Issue", 
        help="Detected Issue associated with this Medication Dispense Detected Issue.")      

class MedicationDispenseNote(models.Model): 
    _name = "hc.medication.dispense.note"   
    _description = "Medication Dispense Note"       
    _inherit = ["hc.basic.association", "hc.annotation"]

    medication_dispense_id = fields.Many2one(
        comodel_name="hc.res.medication.dispense", 
        string="Medication Dispense", 
        help="Medication Dispense associated with this Medication Dispense Note.")                

class MedicationDispenseDosageInstruction(models.Model):    
    _name = "hc.medication.dispense.dosage.instruction" 
    _description = "Medication Dispense Dosage Instruction"     
    _inherit = ["hc.basic.association", "hc.dosage"]

    medication_dispense_id = fields.Many2one(
        comodel_name="hc.res.medication.dispense", 
        string="Medication Dispense", 
        help="Medication Dispense associated with this Medication Dispense Dosage Instruction.")             

class MedicationDispenseEventHistory(models.Model): 
    _name = "hc.medication.dispense.event.history"  
    _description = "Medication Dispense Event History"      
    _inherit = ["hc.basic.association"]

    medication_dispense_id = fields.Many2one(
        comodel_name="hc.res.medication.dispense", 
        string="Medication Dispense", 
        help="Medication Dispense associated with this Medication Dispense Event History.")               
    event_history_id = fields.Many2one(
        comodel_name="hc.res.provenance", 
        string="Event History", 
        help="Event History associated with this Medication Dispense Event History.")              

class MedicationDispenseSubstitutionResponsibleParty(models.Model): 
    _name = "hc.medication.dispense.substitution.responsible.party" 
    _description = "Medication Dispense Substitution Responsible Party"     
    _inherit = ["hc.basic.association"]

    substitution_id = fields.Many2one(
        comodel_name="hc.medication.dispense.substitution", 
        string="Substitution", 
        help="Substitution associated with this Medication Dispense Substitution Responsible Party.")              
    responsible_party_id = fields.Many2one(
        comodel_name="hc.res.practitioner", 
        string="Responsible Party", 
        help="Responsible Party associated with this Medication Dispense Substitution Responsible Party.")               

class MedicationDispenseCategory(models.Model): 
    _name = "hc.vs.medication.dispense.category"    
    _description = "Medication Dispense Category"           
    _inherit = ["hc.value.set.contains"]

    name = fields.Char(
        string="Name", 
        help="Name of this medication dispense category.")                    
    code = fields.Char(
        string="Code", 
        help="Code of this medication dispense category.")                    
    contains_id = fields.Many2one(
        comodel_name="hc.vs.medication.dispense.category", 
        string="Parent", 
        help="Parent medication dispense category.")                    

class ActPharmacySupplyType(models.Model):  
    _name = "hc.vs.act.pharmacy.supply.type"    
    _description = "Act Pharmacy Supply Type"           
    _inherit = ["hc.value.set.contains"]

    name = fields.Char(
        string="Name", 
        help="Name of this act pharmacy supply type.")                    
    code = fields.Char(
        string="Code", 
        help="Code of this act pharmacy supply type.")                    
    contains_id = fields.Many2one(
        comodel_name="hc.vs.act.pharmacy.supply.type", 
        string="Parent", 
        help="Parent act pharmacy supply type.")                    

class MedicationNotDoneReason(models.Model):    
    _name = "hc.vs.medication.not.done.reason"  
    _description = "Medication Not Done Reason"         
    _inherit = ["hc.value.set.contains"]

    name = fields.Char(
        string="Name", 
        help="Name of this medication not done reason.")                  
    code = fields.Char(
        string="Code", 
        help="Code of this medication not done reason.")                  
    contains_id = fields.Many2one(
        comodel_name="hc.vs.medication.not.done.reason", 
        string="Parent", 
        help="Parent medication not done reason.")                    

class ActSubstanceAdminSubstitutionCode(models.Model): 
    _name = "hc.vs.act.substance.admin.substitution.code"  
    _description = "Act Substance Admin Substitution Code"         
    _inherit = ["hc.value.set.contains"]

    name = fields.Char(
        string="Name", 
        help="Name of this act substance admin substitution code.")                  
    code = fields.Char(
        string="Code", 
        help="Code of this act substance admin substitution code.")                  
    contains_id = fields.Many2one(
        comodel_name="hc.vs.act.substance.admin.substitution.code", 
        string="Parent", 
        help="Parent act substance admin substitution code.")                    