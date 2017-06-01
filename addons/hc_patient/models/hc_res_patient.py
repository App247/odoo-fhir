# -*- coding: utf-8 -*-

from openerp import models, fields, api

class Patient(models.Model):    
    _name = "hc.res.patient"    
    _description = "Patient"
    _inherits = {"hc.res.person": "person_id"}

    person_id = fields.Many2one(
        comodel_name="hc.res.person", 
        string="Person", 
        ondelete="restrict", 
        required="True", 
        help="Person associated with this Patient.")
    identifier_ids = fields.One2many(
        comodel_name="hc.patient.identifier", 
        inverse_name="patient_id", 
        string="Identifiers", 
        help="A human identifier for this patient.")
    type = fields.Selection(
        string="Type", 
        selection=[
            ("human", "Human"), 
            ("animal", "Animal")],
        default="human",  
        help="Patient is human or animal.")
    animal_name = fields.Char(
        string="Animal Name",
        help="Name of the animal.")
    is_active = fields.Boolean(
        string="Active", 
        help="Whether this patient's record is in active use.")
    name_ids = fields.One2many(
        comodel_name="hc.patient.name", 
        inverse_name="patient_id", 
        string="Names", 
        help="A name associated with the patient.")
    telecom_ids = fields.One2many(
        comodel_name="hc.patient.telecom", 
        inverse_name="patient_id", 
        string="Telecoms", 
        help="A contact detail for the patient.")
    gender = fields.Selection(
        related="person_id.gender",
        readonly="1",
        help="The gender that the patient is considered to have for administration and record keeping purposes.")
    # gender = fields.Selection(
    #     string="Gender", 
    #     selection=[
    #         ("male", "Male"), 
    #         ("female", "Female"), 
    #         ("other", "Other"), 
    #         ("unknown", "Unknown")], 
    #     help="The gender that the patient is considered to have for administration and record keeping purposes.")
    birth_date=fields.Date(
        related="person_id.birth_date",
        readonly="1",
        help="The date of birth for the patient.")
    birth_time = fields.Char(
        string="Birth Time", 
        help="The time when the patient was born.")
    is_deceased = fields.Boolean(
        string="Deceased",  
        help="Indicates if the patient is deceased or not.")
    deceased_date = fields.Date(
        string="Deceased Date", 
        help="The date when the patient died.")
    deceased_time = fields.Char(
        string="Deceased Time", 
        help="The time when the patient died.")
    address_ids = fields.One2many(
        comodel_name="hc.person.address", 
        inverse_name="patient_id", 
        string="Addresses", 
        help="One or more addresses for this patient.")
    marital_status_id = fields.Many2one(
        comodel_name="hc.vs.marital.status", 
        string="Marital Status", 
        help="Marital (civil) status of a patient.")
    marital_history_ids = fields.One2many(
        comodel_name="hc.patient.marital.history", 
        inverse_name="patient_id", 
        string="Marital Histories", 
        help="Marital (civil) history of a patient.")
    is_multiple_birth = fields.Boolean(
        string="Multiple Birth", 
        help="Whether patient is part of a multiple birth.")
    multiple_birth_count = fields.Integer(
        string="Multiple Birth Count", 
        size=1, 
        help="Number of births in a multiple birth.")
    multiple_birth_order = fields.Integer(
        string="Multiple Birth Order", 
        size=1, 
        help="The actual birth order in a multiple birth.")
    photo_ids = fields.One2many(
        comodel_name="hc.patient.photo", 
        inverse_name="patient_id", 
        string="Photos", 
        help="Image of the patient.")
    general_practitioner_ids = fields.One2many(
        comodel_name="hc.patient.general.practitioner", 
        inverse_name="patient_id", 
        string="General Practitioners", 
        help="Patient's nominated primary care provider.")
    managing_organization_id = fields.Many2one(
        comodel_name="hc.res.organization", 
        string="Managing Organization", 
        help="Organization that is the custodian of the patient record.")
    race_ids = fields.Many2many(
        comodel_name="hc.vs.race", 
        relation="patient_race_rel", 
        string="Races", 
        help="General race category reported by the patient - subject may have more than one.")
    ethnicity_ids = fields.Many2many(
        comodel_name="hc.vs.ethnicity", 
        relation="patient_ethnicity_rel", 
        string="Ethnicities", 
        help="General ethnicity category reported by the patient - subject may have more than one.")
    animal_species_id = fields.Many2one(
        comodel_name="hc.vs.animal.species", 
        string="Animal Species", 
        help="Identifies the high level taxonomic categorization of the kind of animal (e.g., dog, cow).")
    animal_breed_id = fields.Many2one(
        comodel_name="hc.vs.animal.breed", 
        string="Animal Breed", 
        help="Identifies the detailed categorization of the kind of animal (e.g., poodle, angus).")
    animal_gender_status_id = fields.Many2one(
        comodel_name="hc.vs.animal.gender.status", 
        string="Animal Gender Status", 
        help="Indicates the current state of the animal's reproductive organs (e.g., neutered, intact).")
    
    # Extension attribute
    birth_place_id = fields.Many2one(
        comodel_name="hc.address", 
        string="Birth Place", 
        help="The registered place of birth of the patient.")
    adoption_info_id = fields.Many2one(
        comodel_name="hc.vs.adoption.info", 
        string="Adoption Info", 
        help="Code indication the adoption status of the patient.")
    # birth_time = fields.Datetime(string="Birth Time", help="The time of day that the Patient was born.")
    is_cadaveric_donor = fields.Boolean(
        string="Cadaveric Donor", 
        help="Flag indicating whether the patient authorized the donation of body parts after death.")
    congregation = fields.Char(
        string="Congregation", 
        help="A group or place of religious practice that may provide services to the patient.")
    disability_ids = fields.Many2many(
        comodel_name="hc.vs.disability", 
        relation="patient_disability_rel", 
        string="Disabilities", 
        help="Value(s) identifying physical or mental condition(s) that limits a person's movements, senses, or activities.")
    importance_id = fields.Many2one(
        comodel_name="hc.vs.importance",  
        string="Importance",
        help="The importance of the patient (e.g. VIP).")
    is_interpreter_required = fields.Boolean(
        string="Interpreter Required", 
        help="This Patient requires an interpreter to communicate healthcare information to the practitioner.")
    mothers_maiden_name = fields.Char(
        string="Mothers Maiden Name",
        help="Mother's maiden (unmarried) name, commonly collected to help verify patient identity.")
    religion_ids = fields.Many2many(
        comodel_name="hc.vs.religion", 
        relation="patient_religion_rel", 
        string="Religions", 
        help="The patient's professed religious affiliations.")
    
    # Backbone Element
    link_ids = fields.One2many(
        comodel_name="hc.patient.link", 
        inverse_name="patient_id", 
        string="Links", 
        help="Link to another patient resource that concerns the same actual person.")
    contact_ids = fields.One2many(
        comodel_name="hc.patient.contact", 
        inverse_name="patient_id", 
        string="Contacts", 
        help="A contact party (e.g. guardian, partner, friend) for the patient.")
    communication_ids = fields.One2many(
        comodel_name="hc.patient.communication", 
        inverse_name="patient_id", 
        string="Languages", 
        help="A list of Languages which may be used to communicate with the patient about his or her health.")

    #Extension Backbone Element

    citizenship_ids = fields.One2many(
        comodel_name="hc.patient.citizenship", 
        inverse_name="patient_id", 
        string="Citizenships", 
        help="The patient's legal status as citizen of a country.")
    clinical_trial_ids = fields.One2many(
        comodel_name="hc.patient.clinical.trial", 
        inverse_name="patient_id", 
        string="Clinical Trials", 
        help="The clinical trials this patient has or is participating in.")
    nationality_ids = fields.One2many(
        comodel_name="hc.patient.nationality", 
        inverse_name="patient_id", 
        string="Nationalities", 
        help="The nationality of the patient (aka SNOMED Ethnic group (observable entity)).")

    _defaults = {
        "is_patient": True,
        }

    # @api.model
    # def create(self, vals):
    #     vals['is_patient'] = self.env.context.get('is_patient', False)
    #     return super(Patient, self).create(vals)

    # Inherit Person Addresses, Person Names, Person Identifiers, Person Telecom, Person Photos

    @api.model
    def create(self, vals):
        person_obj = self.env['hc.res.person']
        # patient_address_obj = self.env['hc.patient.address']
        patient_name_obj = self.env['hc.patient.name']
        # patient_identifier_obj = self.env['hc.patient.identifier']
        # patient_telecom_obj = self.env['hc.patient.telecom]
        # patient_photo_obj = self.env['hc.patient.photo']
        vals['is_patient'] = self.env.context.get('is_patient', False)
        res = super(Patient, self).create(vals)
        patient_address_vals = {}
        patient_name_vals = {}
        # patient_identifier_vals = {}
        # patient_telecom_vals = {}
        # patient_photo_vals = {}
        if vals and vals.get('person_id'):
            person_id = person_obj.browse(vals.get('person_id'))
            if person_id.address_ids:
                for person_add in person_id.address_ids:
                    patient_address_vals.update({
                                'address_id': person_add.id,
                                'patient_id': res.id
                                })
                    patient_address_obj.create(patient_address_vals)
            # if person_id.name_ids:
            #     for person_name in person_id.name_ids:
            #         patient_name_vals.update({
            #                         # 'human_name_id': person_name.human_name_id.id,
            #                         'human_name_id': person_name.id,
            #                         'patient_id': res.id
            #                         })
            #         patient_name_obj.create(patient_name_vals)
            
            # if person_id.identifier_ids:
            #     for person_name in person_id.identifier_ids:
            #         patient_name_vals.update({
            #                         'identifier_id': person_name.identifier_id.id,
            #                         'patient_id': res.id
            #                         })
            #         patient_identifier_obj.create(patient_identifier_vals)
            # if person_id.telecom_ids:
            #     for person_name in person_id.telecom_ids:
            #         patient_name_vals.update({
            #                         'telecom_id': person_name.telecom_id.id,
            #                         'patient_id': res.id
            #                         })
            #         patient_telecom_obj.create(patient_telecom_vals)
            # if person_id.photo_ids:
            #     for person_name in person_id.photo_ids:
            #         patient_name_vals.update({
            #                         'photo_id': person_name.photo_id.id,
            #                         'patient_id': res.id
            #                         })
            #         patient_photo_obj.create(patient_photo_vals)
        return res

class PatientCitizenship(models.Model): 
    _name = "hc.patient.citizenship"    
    _description = "Patient Citizenship"

    patient_id = fields.Many2one(
        comodel_name="hc.res.patient", 
        string="Patient", 
        help="Patient associated with this Patient Citizenship.")     
    code_id = fields.Many2one(
        comodel_name="res.country", 
        string="Code", 
        help="Nation code of citizenship.")        
    start_date = fields.Datetime(
        string="Valid from", 
        help="Start of the time period of citizenship.")      
    end_date = fields.Datetime(
        string="Valid to", 
        help="End of the time period of citizenship.")        

class PatientClinicalTrial(models.Model):
    _name = "hc.patient.clinical.trial"
    _description = "Patient Clinical Trial"

    patient_id = fields.Many2one(
        comodel_name="hc.res.patient", 
        string="Patient", 
        help="Patient associated with this Patient Clinical Trial.")      
    nct = fields.Char(
        string="NCT", 
        help="National Clinical Trial number.")     
    start_date = fields.Datetime(
        string="Valid from", 
        help="Start of the the period of participation in the clinical trial.")       
    end_date = fields.Datetime(
        string="Valid to", 
        help="End of the the period of participation in the clinical trial.")     
    reason_id = fields.Many2one(
        comodel_name="hc.vs.clinical.trial.reason", 
        string="Reason", 
        help="The reason for participation in the clinical trial.")        

class PatientNationality(models.Model):
    _name = "hc.patient.nationality"
    _description = "Patient Nationality"

    patient_id = fields.Many2one(
        comodel_name="hc.res.patient", 
        string="Patient", 
        help="Patient associated with this Patient Nationality.")     
    code_id = fields.Many2one(
        comodel_name="hc.vs.nationality", 
        string="Code", 
        help="Nationality Code.")        
    start_date = fields.Datetime(
        string="Valid from", 
        help="Start of the nationality period.")      
    end_date = fields.Datetime(
        string="Valid to", 
        help="End of the nationality period.")        

class PatientIdentifier(models.Model):  
    _name = "hc.patient.identifier" 
    _description = "Patient Identifier"         
    _inherits = {"hc.person.identifier": "identifier_id"}

    identifier_id = fields.Many2one(
        comodel_name="hc.person.identifier", 
        string="Person Identifier",
        required="True",
        ondelete="restrict", 
        help="Person Identifier associated with this Patient Identifier.")
    patient_id = fields.Many2one(
        comodel_name="hc.res.patient", 
        string="Patient", 
        help="Patient associated with this Patient Identifier.")                    

class PatientName(models.Model): 
    _name = "hc.patient.name"    
    _description = "Patient Name"
    _inherits = {"hc.person.name": "name_id"}

    name_id = fields.Many2one(
        comodel_name="hc.person.name",
        string="Human Name",
        required="True",
        ondelete="restrict", 
        help="Human Name associated with this Patient Name.")
    patient_id = fields.Many2one(
        comodel_name="hc.res.patient", 
        string="Patient", 
        help="Patient associated with this Patient Name.")

# class PatientAddress(models.Model): 
#     _name = "hc.patient.address"    
#     _description = "Patient Address"        
#     _inherits = {"hc.person.address": "address_id"}

#     address_id = fields.Many2one(
#         comodel_name="hc.person.address", 
#         string="Person Address", 
#         required="True", 
#         ondelete="restrict", 
#         help="Address associated with this Patient Address.")                 
#     patient_id = fields.Many2one(
#         comodel_name="hc.res.patient", 
#         string="Patient", 
#         help="Patient associated with this Patient Address.")                                  

class PatientTelecom(models.Model): 
    _name = "hc.patient.telecom"    
    _description = "Patient Telecom"        
    _inherits = {"hc.person.telecom": "telecom_id"}

    telecom_id = fields.Many2one(
        comodel_name="hc.person.telecom", 
        string="Person Telecom", 
        ondelete="restrict", 
        required="True", 
        help="Telecom associated with this Patient Telecom.")                 
    patient_id = fields.Many2one(
        comodel_name="hc.res.patient", 
        string="Patient", 
        help="Patient associated with this Patient Telecom.")                                               

class PatientMaritalHistory(models.Model):    
    _name = "hc.patient.marital.history" 
    _description = "Patient Marital History"     
    _inherit = ["hc.basic.association"]
    
    patient_id = fields.Many2one(
        comodel_name="hc.res.patient", 
        string="Patient", 
        help="Patient associated with this Patient Marital History.")              
    marital_status_id = fields.Many2one(
        comodel_name="hc.vs.marital.status", 
        string="Marital Status", 
        help="Marital (civil) status of a patient.")
    partner_id = fields.Many2one(
        comodel_name="hc.res.person", 
        string="Spouse", 
        help="Person married to this Patient.")
               
class PatientPhoto(models.Model):   
    _name = "hc.patient.photo"  
    _description = "Patient Photo"
    _inherits = {"hc.person.photo": "photo_id"}

    photo_id = fields.Many2one(
        comodel_name="hc.person.photo", 
        string="Photo",
        required="True",
        ondelete="restrict",  
        help="Photo associated with this Patient Photo.")
    patient_id = fields.Many2one(
        comodel_name="hc.res.patient", 
        string="Patient", 
        help="Patient associated with this Patient Photo.")      

class PatientCareProviderPractitioner(models.Model):
    _name = "hc.patient.care.provider.practitioner"    
    _description = "Patient Care Provider Practitioner"
    _inherit = ["hc.basic.association"]

    patient_id = fields.Many2one(
        comodel_name="hc.res.patient", 
        string="Patient", 
        help="Patient associated with this Patient Care Provider Practitioner.")
    practitioner_id = fields.Many2one(
        comodel_name="hc.res.practitioner", 
        string="Care Provider Practitioner", 
        help="Practitioner who is this Patient Care Provider Practitioner.")

class PatientCareProviderOrganization(models.Model):
    _name = "hc.patient.care.provider.organization"    
    _description = "Patient Care Provider Organization"
    _inherit = ["hc.basic.association"]

    patient_id = fields.Many2one(
        comodel_name="hc.res.patient", 
        string="Patient", 
        help="Patient associated with this Patient Care Provider Organization.")
    organization_id = fields.Many2one(
        comodel_name="hc.res.organization", 
        string="Care Provider Organization", 
        help="Organization that is this Patient Care Provider Organization.")

# class PatientAnimal(models.Model):  
#     _name = "hc.patient.animal" 
#     _description = "Patient Animal"
#     _rec_name = "animal" 

#     animal = fields.Char(
#         string="Animal", 
#         relate="breed_id.name", 
#         help= "Breed of animal.")
    species_id = fields.Many2one(
        comodel_name="hc.vs.animal.species", 
        string="Species",
        required="True", 
        help="Identifies the high level taxonomic categorization of the kind of animal (e.g., dog, cow).")
    breed_id = fields.Many2one(
        comodel_name="hc.vs.animal.breed", 
        string="Breed", 
        help="Identifies the detailed categorization of the kind of animal (e.g., poodle, angus).")
    gender_status_id = fields.Many2one(
        comodel_name="hc.vs.animal.gender.status", 
        string="Gender Status", 
        help="Indicates the current state of the animal's reproductive organs (e.g., neutered, intact).")

class PatientCommunication(models.Model):
    _name = "hc.patient.communication"
    _description = "Patient Communication"
    _inherit = ["hc.basic.association"]

    patient_id = fields.Many2one(
        comodel_name="hc.res.patient", 
        string="Patient", 
        help="Patient associated with this Patient Communication.")
    language_id = fields.Many2one(
        comodel_name="res.lang", 
        string="Language",
        help="Language associated with this Patient Communication.")
    proficiency_ids = fields.One2many(
        comodel_name="hc.patient.language.proficiency", 
        inverse_name="communication_id", 
        string="Proficiencies", 
        help="Patient's proficiency and skill with this Patient Language.")

class PatientLanguageProficiency(models.Model): 
    _name = "hc.patient.language.proficiency"   
    _description = "Patient Language Proficiency"           
    _inherit = ["hc.basic.association"]

    communication_id = fields.Many2one(
        comodel_name="hc.patient.communication", 
        string="Communication", 
        help="Communication associated with this Patient Language Proficiency.")                    
    language_proficiency_id = fields.Many2one(
        comodel_name="hc.vs.language.proficiency", 
        string="Language Proficiency", 
        help="Language Proficiency associated with this Patient Language Proficiency.")                 
    language_skill_id = fields.Many2one(
        comodel_name="hc.vs.language.skill", 
        string="Language Skill", 
        help="Language Skill associated with this Patient Language Proficiency.")                 

class PatientContact(models.Model): 
    _name = "hc.patient.contact"    
    _description = "Patient Contact"           
    _inherits = {"hc.res.person": "person_id"}

    person_id = fields.Many2one(
        comodel_name="hc.res.person", 
        string="Person", 
        ondelete="restrict", 
        required="True", 
        help="Person associated with this Patient Contact.")
    patient_id = fields.Many2one(
        comodel_name="hc.res.patient", 
        string="Patient", 
        help="Patient associated with this Patient Contact.")
    relationship_ids = fields.Many2many(
        comodel_name="hc.vs.v2.contact.role", 
        relation="patient_contact_role_rel", 
        string="Relationships", 
        help="The kind of relationship.")
    name_id = fields.Many2one(
        comodel_name="hc.human.name", 
        string="Name", 
        help="A name associated with the contact person.")
    telecom_ids = fields.One2many(
        comodel_name="hc.patient.contact.telecom", 
        inverse_name="contact_id", 
        string="Telecoms", 
        help="A contact detail for the contact person.")
    address_id = fields.Many2one(
        comodel_name="hc.address", 
        string="Address", 
        help="Address for the contact person.")
    gender = fields.Selection(
        string="Gender", 
        selection=[
            ("male", "Male"), 
            ("female", "Female"), 
            ("other", "Other"), 
            ("unknown", "Unknown")], 
        help="The gender that the patient contact is considered to have for administration and record keeping purposes.")
    organization_id = fields.Many2one(
        comodel_name="hc.res.organization", 
        string="Organization", 
        help="Organization that is associated with the contact.")
    start_date = fields.Datetime(
        string="Valid from", 
        help="Start of the the period during which this contact person or organization is valid to be contacted relating to this patient.")
    end_date = fields.Datetime(
        string="Valid to", 
        help="End of the the period during which this contact person or organization is valid to be contacted relating to this patient.")  

class PatientLink(models.Model):    
    _name = "hc.patient.link"   
    _description = "Patient Link"

    patient_id = fields.Many2one(
        comodel_name="hc.res.patient", 
        string="Patient",
        help="Patient associated with this Link.")
    other_type = fields.Selection(
        string="Other Type", 
        required="True", 
        selection=[
            ("patient", "Patient"), 
            ("related_person", "Related Person")], 
        help="Type of resource that the link refers to.")
    other_name = fields.Char(
        string="Other", 
        compute="_compute_other_name", 
        store="True", 
        help="The other patient or related person resource that the link refers to.")
    other_patient_id = fields.Many2one(
        comodel_name="hc.res.patient", 
        string="Other Patient", 
        help="Patient resource that the link refers to.")
    other_related_person_id = fields.Many2one(
        comodel_name="hc.res.related.person", 
        string="Other Related Person", 
        help="Related Person resource that the link refers to.")
    type = fields.Selection(
        string="Link Type", 
        selection=[
            ("replace", "Replace"), 
            ("refer", "Refer"), 
            ("seealso", "See also")], 
        help="The type of link between this patient resource and another patient resource.")

    @api.multi          
    @api.depends('other_patient_id', 'other_related_person_id')         
    def _compute_other_name(self):          
        for hc_patient_link in self:        
            if hc_patient_link.other_type == 'patient':   
                hc_patient_link.other_name = hc_patient_link.other_patient_id.name
            elif hc_patient_link.other_type == 'related_person':  
                hc_patient_link.other_name = hc_patient_link.other_related_person_id.name

class PatientContactTelecom(models.Model):  
    _name = "hc.patient.contact.telecom"    
    _description = "Patient Contact Telecom"            
    _inherit = ["hc.contact.point.use"] 
    _inherits = {"hc.contact.point": "telecom_id"}

    telecom_id = fields.Many2one(
        comodel_name="hc.contact.point", 
        string="Telecom", 
        ondelete="restrict", 
        required="True", 
        help="Telecom associated with this Patient Contact Telecom.")                     
    contact_id = fields.Many2one(
        comodel_name="hc.patient.contact", 
        string="Contact", 
        help="Contact associated with this Patient Contact Telecom.")                     

class PatientGeneralPractitioner(models.Model): 
    _name = "hc.patient.general.practitioner"   
    _description = "Patient General Practitioner"           
    _inherit = ["hc.basic.association"] 

    patient_id = fields.Many2one(
        comodel_name="hc.res.patient", 
        string="Patient", 
        help="Patient associated with this Patient General Practitioner.")                        
    general_practitioner_type = fields.Selection(
        string="General Practitioner Type", 
        selection=[
            ("organization", "Organization"), 
            ("practitioner", "Practitioner")], 
        help="Type of patient's nominated primary care provider.")                       
    general_practitioner_name = fields.Char(
        string="General Practitioner", 
        compute="_compute_general_practitioner_name", 
        store="True", 
        help="Patient's nominated primary care provider.")                        
    general_practitioner_organization_id = fields.Many2one(
        comodel_name="hc.res.organization", 
        string="General Practitioner Organization", 
        help="Organization that is patient's nominated primary care provider.")                        
    general_practitioner_practitioner_id = fields.Many2one(
        comodel_name="hc.res.practitioner", 
        string="General Practitioner Person", 
        help="Practitioner who is patient's nominated primary care provider.")                        

    @api.multi          
    @api.depends('general_practitioner_organization_id', 'general_practitioner_practitioner_id')          
    def _compute_general_practitioner_name(self):           
        for hc_patient_general_practitioner in self:        
            if hc_patient_general_practitioner.general_practitioner_type == 'organization':  
                hc_patient_general_practitioner.general_practitioner_name = hc_patient_general_practitioner.general_practitioner_organization_id.name
            elif hc_patient_general_practitioner.general_practitioner_type == 'practitioner':  
                hc_patient_general_practitioner.general_practitioner_name = hc_patient_general_practitioner.general_practitioner_practitioner_id.name

class MaritalStatus(models.Model):  
    _name = "hc.vs.marital.status"  
    _description = "Marital Status" 
    _inherit = ["hc.value.set.contains"]

    name = fields.Char(
        string="Name", 
        help="Name of this marital status.")
    code = fields.Char(
        string="Code", 
        help="Code of this marital status.")
    contains_id = fields.Many2one(
        comodel_name="hc.vs.marital.status",
        string="Parent",
        help="Parent marital status.")
    may_have_spouse = fields.Boolean(
        string="Spouse",
        help="Spouse possible?")

class ContactRelationship(models.Model):    
    _name = "hc.vs.v2.contact.role"    
    _description = "V2 Contact Role"   
    _inherit = ["hc.value.set.contains"]    

    name = fields.Char(
        string="Name", 
        help="Name of this v2 contact role.")
    code = fields.Char(
        string="Code", 
        help="Code of this v2 contact role.")
    contains_id = fields.Many2one(
        comodel_name="hc.vs.v2.contact.role", 
        string="Parent",
        help="Parent contact relationship.")

class AnimalBreed(models.Model):    
    _name = "hc.vs.animal.breed"    
    _description = "Animal Breed"   
    _inherit = ["hc.value.set.contains"]

    name = fields.Char(
        string="Name", 
        help="Name of this animal breed.")
    code = fields.Char(
        string="Code", 
        help="Code of this animal breed.")
    contains_id = fields.Many2one(
        comodel_name="hc.vs.animal.breed", 
        string="Parent",
        help="Parent breed.")
    hierarchy_id = fields.Many2one(
        comodel_name="hc.vs.animal.species", 
        string="Hierarchy",
        help="Hierarchy grouping of this animal breed.")

class AnimalGenderStatus(models.Model): 
    _name = "hc.vs.animal.gender.status"    
    _description = "Animal Gender Status"   
    _inherit = ["hc.value.set.contains"]

    name = fields.Char(
        string="Name", 
        help="Name of this animal gender status.")
    code = fields.Char(
        string="Code", 
        help="Code of this animal gender status.")
    contains_id = fields.Many2one(
        comodel_name="hc.vs.animal.gender.status", 
        string="Parent",
        help="Parent gender status.")

class AnimalSpecies(models.Model):  
    _name = "hc.vs.animal.species"  
    _description = "Animal Species" 
    _inherit = ["hc.value.set.contains"]

    name = fields.Char(
        string="Name", 
        help="Name of this animal species.")
    code = fields.Char(
        string="Code", 
        help="Code of this animal species.")
    contains_id = fields.Many2one(
        comodel_name="hc.vs.animal.species", 
        string="Parent",
        help="Parent animal species.")
    level_name = fields.Char(
        string="Level Name",
        help="Name of level (e.g., Species")

class AdoptionInfo(models.Model):
    _name = "hc.vs.adoption.info"
    _description = "Adoption Info"
    _inherit = ["hc.value.set.contains"]

    name = fields.Char(
        string="Name", 
        help="Name of this adoption info.")                               
    code = fields.Char(
        string="Code", 
        help="Code of this adoption info.")                               
    contains_id = fields.Many2one(
        comodel_name="hc.vs.adoption.info", 
        string="Parent", 
        help="Parent adoption info.")                                

class Disability(models.Model): 
    _name = "hc.vs.disability"
    _description = "Disability"
    _inherit = ["hc.value.set.contains"]

    name = fields.Char(
        string="Name", 
        help="Name of this disability.")                              
    code = fields.Char(
        string="Code", 
        help="Code of this disability.")                              
    contains_id = fields.Many2one(
        comodel_name="hc.vs.disability", 
        string="Parent", 
        help="Parent disability.")                              

class Importance(models.Model):
    _name = "hc.vs.importance"
    _description = "Importance"
    _inherit = ["hc.value.set.contains"]

    name = fields.Char(
        string="Name", 
        help="Name of this importance.")                              
    code = fields.Char(
        string="Code", 
        help="Code of this importance.")                              
    contains_id = fields.Many2one(
        comodel_name="hc.vs.importance", 
        string="Parent", 
        help="Parent importance.")                              

class Religion(models.Model):
    _name = "hc.vs.religion"
    _description = "Religion"
    _inherit = ["hc.value.set.contains"]

    name = fields.Char(
        string="Name", 
        help="Name of this religion.")                                
    code = fields.Char(
        string="Code", 
        help="Code of this religion.")                                
    contains_id = fields.Many2one(
        comodel_name="hc.vs.religion", 
        string="Parent", help="Parent religion.")                              

class ClinicalTrialReason(models.Model):
    _name = "hc.vs.clinical.trial.reason"
    _description = "Clinical Trial Reason"
    inherit = ["hc.value.set.contains"]

    name = fields.Char(
        string="Name", 
        help="Name of this clinical trial reason.")                               
    code = fields.Char(
        string="Code", 
        help="Code of this clinical trial reason.")                               
    contains_id = fields.Many2one(
        comodel_name="hc.vs.clinical.trial.reason", 
        string="Parent", 
        help="Parent clinical trial reason.")                                

class Nationality(models.Model):
    _name = "hc.vs.nationality"
    _description = "Nationality"
    _inherit = ["hc.value.set.contains"]

    name = fields.Char(
        string="Name", 
        help="Name of this nationality.")                             
    code = fields.Char(
        string="Code", 
        help="Code of this nationality.")                             
    contains_id = fields.Many2one(
        comodel_name="hc.vs.nationality", 
        string="Parent", 
        help="Parent nationality.")                                

# External Reference

class Partner(models.Model):
    _inherit = ["res.partner"]

    is_patient = fields.Boolean(
        string="Is a patient", 
        help="This partner is a patient.")

class PersonLink(models.Model):
    _inherit = ["hc.person.link"]

    target_patient_id = fields.Many2one(
        comodel_name="hc.res.patient", 
        string="Target Patient", 
        help="Patient who is the resource to which this actual person is associated.")

    @api.depends('target_type')          
    def _compute_target_name(self):         
        for hc_person_link in self:      
            if hc_person_link.target_type == 'person': 
                hc_person_link.target_name = hc_person_link.target_person_id.name
            elif hc_person_link.target_type == 'practitioner':   
                hc_person_link.target_name = hc_person_link.target_practitioner_id.name
            elif hc_person_link.target_type == 'related_person': 
                hc_person_link.target_name = hc_person_link.target_related_person_id.name
            elif hc_person_link.target_type == 'patient':  
                hc_person_link.target_name = hc_person_link.target_patient_id.name

class RelatedPersonPatient(models.Model): 
    _inherit = ["hc.related.person.patient"]

    patient_id = fields.Many2one(
        comodel_name="hc.res.patient",
        string="Patient",
        help="Patient associated with this Related Person Patient.")

class Annotation(models.Model):
    _inherit = ["hc.annotation"]

    author_patient_id = fields.Many2one(
        comodel_name="hc.res.patient", 
        string="Author Patient", 
        help="Patient responsible for the annotation.")

    @api.depends('author_type')
    def _compute_author_name(self):
        for hc_annotation in self:
            if hc_annotation.author_type == 'string':
                hc_annotation.author_name = hc_annotation.author_string
            elif hc_annotation.author_type == 'practitioner':
                hc_annotation.author_name = hc_annotation.author_practitioner_id.name
            elif hc_annotation.author_type == 'related_person':
                hc_annotation.author_name = hc_annotation.author_related_person_id.name
            elif hc_annotation.author_type == 'patient':
                hc_annotation.author_name = hc_annotation.author_patient_id.name

class Signature(models.AbstractModel):    
    _inherit = "hc.signature"
    
    who_patient_id = fields.Many2one(
        comodel_name="hc.res.patient", 
        string="Who Patient", 
        help="Patient who signed.")

    on_behalf_of_patient_id = fields.Many2one(
        comodel_name="hc.res.patient", 
        string="On Behalf Of Patient", 
        help="Patient the party represented.")
