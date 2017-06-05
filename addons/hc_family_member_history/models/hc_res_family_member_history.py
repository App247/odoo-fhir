# -*- coding: utf-8 -*-

from openerp import models, fields, api
from datetime import datetime
from openerp.tools import DEFAULT_SERVER_DATE_FORMAT as DF
from openerp.tools import DEFAULT_SERVER_DATETIME_FORMAT as DTF

class FamilyMemberHistory(models.Model):    
    _name = "hc.res.family.member.history"  
    _description = "Family Member History"
    _rec_name="record_name"          

    record_name = fields.Char(
        string="Record Name", 
        compute="_compute_record_name", 
        store="True", 
        help="Human-readable label for this family member history definition. Patient Name + DOB + Family Member Name + Relationship + Update Date.")
    identifier_ids = fields.One2many(
        comodel_name="hc.family.member.history.identifier", 
        inverse_name="family_member_history_id", 
        string="Identifiers", 
        help="External Id(s) for this record.")                 
    definition_ids = fields.One2many(
        comodel_name="hc.family.member.history.definition", 
        inverse_name="family_member_history_id", 
        string="Definitions", 
        help="Instantiates protocol or definition.")
    status = fields.Selection(
        string="Status", 
        required="True", 
        selection=[
            ("partial", "Partial"), 
            ("completed", "Completed"), 
            ("entered-in-error", "Entered-In-Error"), 
            ("health-unknown", "Health-Unknown")],
        default="partial", 
        help="A code specifying the status of the record of the family history of a specific family member.")
    data_absent_reason = fields.Selection(
        string="Data Absent Reason", 
        selection=[
            ("subject-unknown", "Subject-Unknown"), 
            ("withheld", "Withheld"), 
            ("unable-to-obtain", "Unable-To-Obtain"), 
            ("deferred", "Deferred")],
        help="Describes why the family member history did not occur in coded and/or textual form.")
    patient_id = fields.Many2one(
        comodel_name="hc.res.patient", 
        string="Patient", 
        required="True", 
        help="Patient history is about.")                                       
    date = fields.Datetime(
        string="Date",
        required="True",
        default=fields.datetime.now(), 
        help="When history was captured/updated.")                                        
    family_member_name_type = fields.Selection(
        string="Family Member Name Type", 
        required="True", 
        selection=[
            ("string", "String"),
            ("related_person", "Related Person")], 
        help="Type of name of family member.")                
    family_member_name = fields.Char(
        string="Family Member", 
        compute="_compute_family_member_name", 
        store="True", 
        help="The family member described.")
    family_member_name_string = fields.Char(
        string="Family Member Name String", 
        help="String value of the family member described (e.g., 'My aunt Agatha', 'uncle'.")                  
    family_member_name_related_person_id = fields.Many2one(
        comodel_name="hc.res.related.person", 
        string="Family Member Related Person Name", 
        help="Related Person who is a family member of this patient.")
    relationship_id = fields.Many2one(
        comodel_name="hc.vs.v3.family.member", 
        string="Relationship", 
        required="True", 
        help="Relationship to the subject.")
    # gender = fields.Selection(
    #     related="person_id.gender",
    #     readonly="1",
    #     help="The gender a family member used for administrative purposes.")
    # born = fields.Char(
    #     string="Birth Date",
    #     related="person_id.born_name",
    #     readonly="1",
    #     help="(approximate) date of birth.")
    # age = fields.Char(
    #     string="Age",
    #     related="person_id.age_name", 
    #     readonly="1", 
    #     help="(approximate) age.")
    # deceased = fields.Char(
    #     string="Deceased Age",
    #     related="person_id.deceased_name", 
    #     readonly="1", 
    #     help="Dead? How old/when?")
    gender = fields.Selection(
        string="Gender", 
        selection=[
            ("male", "Male"), 
            ("female", "Female"), 
            ("other", "Other"), 
            ("unknown", "Unknown")], 
        help="The gender of a family member used for administrative purposes.")                 
    born_type = fields.Selection(
        string="Born Type",
        selection=[
            ("period", "Period"), 
            ("date", "Date"), 
            ("string", "String")], 
        help="Type of date of birth.")                  
    born_name = fields.Char(
        string="Born", 
        compute="_compute_born_name", 
        help="Date of birth.")                 
    earliest_born_date = fields.Date(
        string="Earliest Born Date", 
        help="Earliest approximate date of birth.")                   
    latest_born_date = fields.Date(
        string="Latest Born Date", 
        help="Latest approximate date of birth.")                 
    born_date = fields.Date(
        string="Born Date", 
        help="Date of birth.")                  
    born_string = fields.Char(
        string="Born", 
        help="String of approximate date of birth.")                                 
    age_type = fields.Selection(
        string="Age Type", 
        selection=[
            ("age", "Age"), 
            ("range", "Range"), 
            ("string", "String")], 
        help="Type of age.")                  
    age_name = fields.Char(
        string="Age", 
        compute="_compute_age_name", 
        help="Age.")                  
    age = fields.Integer(
        string="Age Integer", 
        size=3, 
        help="Approximate age.")                   
    age_uom_id = fields.Many2one(
        comodel_name="product.uom", 
        string="Age UOM", 
        domain="[('category_id','=','Time (UCUM)')]", 
        default="a", 
        help="Age unit of measure.")
    age_range_low = fields.Float(
        string="Age Range Low", 
        help="Low limit of approximate age.")                    
    age_range_high = fields.Float(
        string="Age Range High", 
        help="High limit of approximate age.")                 
    age_string = fields.Char(
        string="Age", 
        help="String of approximate age.")                    
    is_estimated_age = fields.Boolean(
        string="Estimated Age", 
        help="Age is estimated?")
    is_deceased = fields.Boolean(
        string="Deceased", 
        help="Dead? How old/when?")                    
    # is_deceased_age_known = fields.Boolean(
    #     string="Is Deceased Age Known", 
    #     help="Deceased age known?")  
    deceased_age_type = fields.Selection(
        string="Deceased Age Type", 
        selection=[
            ("age", "Age"), 
            ("range", "Range"), 
            ("date", "Date"), 
            ("string", "String")], 
        default="date",
        help="Type of dead? how old/when?")                   
    deceased_age_name = fields.Char(
        string="Deceased Age", 
        compute="_compute_deceased_age_name", 
        help="Dead? How old/when?")                                  
    deceased_age = fields.Integer(
        string="Deceased Age Integer", 
        size=3, 
        help="Dead? How old/when?")
    deceased_age_uom_id = fields.Many2one(
        comodel_name="product.uom", 
        string="Deceased Age UOM", 
        domain="[('category_id','=','Time (UCUM)')]", 
        default="a", 
        help="Deceased age unit of measure.")
    deceased_age_range_low = fields.Float(
        string="Deceased Age Range Low", 
        help="Low limit of dead? how old/when?")                    
    deceased_age_range_high = fields.Float(
        string="Deceased Age Range High", 
        help="High limit of dead? how old/when?")                 
    deceased_age_date = fields.Date(
        string="Deceased Age Date", 
        help="Deceased date.")                 
    deceased_age_string = fields.Char(
        string="Deceased Age String", 
        help="String of dead? how old/when?")
    reason_code_ids = fields.Many2many(
        comodel_name="hc.vs.clinical.finding", 
        relation="family_member_history_reason_code_rel", 
        string="Reason Codes", 
        help="Why was family member history performed?")
    reason_reference_ids = fields.One2many(
        comodel_name="hc.family.member.history.reason.reference", 
        inverse_name="family_member_history_id", 
        string="Reason References", 
        help="Why was family member history performed?")
    note_ids = fields.One2many(
        comodel_name="hc.family.member.history.note", 
        inverse_name="family_member_history_id", 
        string="Notes", 
        help="General note about related person.")
    condition_ids = fields.One2many(
        comodel_name="hc.family.member.history.condition", 
        inverse_name="family_member_history_id", 
        string="Conditions", 
        help="Condition that the related person had.")
        
    @api.depends('patient_id', 'family_member_name', 'date')             
    def _compute_record_name(self):                
        comp_name = '/'         
        for hc_res_family_member_history in self:           
            if hc_res_family_member_history.patient_id:     
                comp_name = hc_res_family_member_history.patient_id.name    
                if hc_res_family_member_history.patient_id.birth_date:  
                    patient_birth_date = datetime.strftime(datetime.strptime(hc_res_family_member_history.patient_id.birth_date, DF), "%Y-%m-%d")
                    comp_name = comp_name + "("+ patient_birth_date + "),"
            if hc_res_family_member_history.family_member_name:     
                comp_name = comp_name + " " + hc_res_family_member_history.family_member_name + ", " + hc_res_family_member_history.relationship_id.name + "," or ''           
            if hc_res_family_member_history.date:        
                patient_date = datetime.strftime(datetime.strptime(hc_res_family_member_history.date, DTF), "%Y-%m-%d")   
                comp_name = comp_name + " " + patient_date   
            hc_res_family_member_history.record_name = comp_name       

    @api.depends('family_member_name_type')         
    def _compute_family_member_name(self):          
        for hc_res_family_member_history in self:       
            if hc_res_family_member_history.family_member_name_type == 'string':    
                hc_res_family_member_history.family_member_name = hc_res_family_member_history.family_member_name_string
            elif hc_res_family_member_history.family_member_name_type == 'related_person':  
                hc_res_family_member_history.family_member_name = hc_res_family_member_history.family_member_name_related_person_id.name

    @api.depends('born_type')           
    def _compute_born_name(self):           
        for hc_res_family_member_history in self:      
            if hc_res_family_member_history.born_type == 'period':   
                hc_res_family_member_history.born_name = 'Between ' + str(hc_res_family_member_history.earliest_born_date) + ' and ' + str(hc_res_family_member_history.latest_born_date)
            elif hc_res_family_member_history.born_type == 'date': 
                hc_res_family_member_history.born_name = str(hc_res_family_member_history.born_date)
            elif hc_res_family_member_history.born_type == 'string':   
                hc_res_family_member_history.born_name = hc_res_family_member_history.born_string
          
    @api.depends('age_type')            
    def _compute_age_name(self):            
        for hc_res_family_member_history in self:      
            if hc_res_family_member_history.age_type == 'age': 
                hc_res_family_member_history.age_name = str(hc_res_family_member_history.age) + ' ' + str(hc_res_family_member_history.age_uom_id.name) + 's old'
            elif hc_res_family_member_history.age_type == 'range': 
                hc_res_family_member_history.age_name = 'Between ' + str(hc_res_family_member_history.age_range_low) + ' and ' + str(hc_res_family_member_history.age_range_high)
            elif hc_res_family_member_history.age_type == 'string':    
                hc_res_family_member_history.age_name = hc_res_family_member_history.age_string

    # @api.multi          
    @api.depends('deceased_age_type')         
    def _compute_deceased_age_name(self):           
        for hc_res_family_member_history in self:      
            if hc_res_family_member_history.deceased_age_type == 'age':  
                hc_res_family_member_history.deceased_age_name = str(hc_res_family_member_history.deceased_age) + ' ' + str(hc_res_family_member_history.deceased_age_uom_id.name) + 's old'
            elif hc_res_family_member_history.deceased_age_type == 'range':    
                hc_res_family_member_history.deceased_age_name = 'Between ' + str(hc_res_family_member_history.deceased_age_range_low) + ' and ' + str(hc_res_family_member_history.deceased_age_range_high)
            elif hc_res_family_member_history.deceased_age_type == 'date': 
                hc_res_family_member_history.deceased_age_name = str(hc_res_family_member_history.deceased_age_date)
            elif hc_res_family_member_history.deceased_age_type == 'string': 
                hc_res_family_member_history.deceased_age_name = hc_res_family_member_history.deceased_age_string

# Constraints

# fhs-1: Can have age[x] or born[x], but not both (expression : age.empty() or born.empty())
# fhs-2: Can only have estimatedAge if age[x] is present (expression : age.exists() or estimatedAge.empty())




class FamilyMemberHistoryCondition(models.Model):   
    _name = "hc.family.member.history.condition"    
    _description = "Family Member History Condition"            

    family_member_history_id = fields.Many2one(
        comodel_name="hc.res.family.member.history", 
        string="Family Member History", 
        help="Family Member History associated with this Condition.")                   
    code_id = fields.Many2one(
        comodel_name="hc.vs.condition.code", 
        string="Code", 
        required="True", 
        help="Condition suffered by relation.")                  
    outcome = fields.Selection(
        string="Condition Outcome", 
        selection=[
            ("deceased", "Deceased"), 
            ("permanent disability", "Permanent Disability"), 
            ("etc.", "Etc.")], 
        help="Indicates what happened as a result of this condition. If the condition resulted in death, deceased date is captured on the relation.")                  
    onset_type = fields.Selection(
        string="Onset Type", 
        selection=[
            ("age", "Age"), 
            ("range", "Range"), 
            ("string", "String")], 
        help="Type of when condition first manifested.")                  
    onset_name = fields.Char(
        string="Onset", 
        compute="_compute_onset_name", 
        help="When condition first manifested.")                    
    onset_age = fields.Integer(
        string="Onset Age", 
        size=3, 
        help="When condition first manifested.")                 
    onset_age_uom_id = fields.Many2one(
        comodel_name="product.uom", 
        string="Onset Age UOM", 
        domain="[('category_id','=','Time (UCUM)')]", 
        default="a", 
        help="Onset age unit of measure.")
    onset_range_low = fields.Float(
        string="Onset Range Low", 
        help="Low limit of when condition first manifested.")                  
    onset_range_high = fields.Float(
        string="Onset Range High", 
        help="High limit of when condition first manifested.")                   
    onset_string = fields.Char(
        string="Onset", 
        help="String of when condition first manifested.")                    
    note_ids = fields.One2many(
        comodel_name="hc.family.member.history.condition.note", 
        inverse_name="condition_id", 
        string="Notes", 
        help="Extra information about condition.")              

    @api.depends('onset_type')          
    def _compute_onset_name(self):          
        for hc_family_member_history_condition in self:
            if hc_family_member_history_condition.onset_type == 'age':
                hc_family_member_history_condition.onset_name = str(hc_family_member_history_condition.onset_age) + " " + str(hc_family_member_history_condition.onset_age_uom_id.name) + "s old"
            elif hc_family_member_history_condition.onset_type == 'string':  
                hc_family_member_history_condition.onset_name = hc_family_member_history_condition.onset_string
            elif hc_family_member_history_condition.onset_type == 'range':  
                hc_family_member_history_condition.onset_name = "Between " + str(hc_family_member_history_condition.onset_range_low) + " and " + str(hc_family_member_history_condition.onset_range_high)

class FamilyMemberHistoryIdentifier(models.Model): 
    _name = "hc.family.member.history.identifier"   
    _description = "Family Member History Identifier"           
    _inherits = {"hc.person.identifier": "identifier_id"}
    
    identifier_id = fields.Many2one(
        comodel_name="hc.person.identifier", 
        string="Identifier", 
        ondelete="restrict", 
        required="True", 
        help="Person Identifier associated with this Family Member Identifier.")
    family_member_history_id = fields.Many2one(
        comodel_name="hc.res.family.member.history", 
        string="Family Member History", 
        help="Family Member History associated with this Family Member Identifier.")              
                 
class FamilyMemberHistoryDefinition(models.Model):
    _name = "hc.family.member.history.definition"
    _description = "Family Member History Definition"
    _inherit = ["hc.basic.association"]

    family_member_history_id = fields.Many2one(
        comodel_name="hc.res.family.member.history", 
        string="Family Member History", 
        help="Family Member History associated with this Family Member History Definition.")                                
    definition_type = fields.Selection(
        string="Definition Type", 
        selection=[
            ("plan_definition", "Plan Definition"), 
            ("questionnaire", "Questionnaire")], 
        help="Type of instantiates protocol or definition.")                               
    definition_name = fields.Char(
        string="Definition", 
        compute="_compute_definition_name", 
        store="True", 
        help="Instantiates protocol or definitio.")                                
    definition_plan_definition_id = fields.Many2one(
        comodel_name="hc.res.plan.definition", 
        string="Definition Plan Definition", 
        help="Plan Definition instantiates protocol or definition.")                                
    definition_questionnaire_id = fields.Many2one(
        comodel_name="hc.res.questionnaire", 
        string="Definition Questionnaire", 
        help="Questionnaire instantiates protocol or definition.")                                

    @api.depends('definition_type')            
    def _compute_definition_name(self):         
        for hc_family_member_history_definition in self:       
            if hc_family_member_history_definition.definition_type == 'plan_definition':   
                hc_family_member_history_definition.definition_name = hc_family_member_history_definition.definition_plan_definition_id.name
            elif hc_family_member_history_definition.definition_type == 'questionnaire':   
                hc_family_member_history_definition.definition_name = hc_family_member_history_definition.definition_questionnaire_id.name

class FamilyMemberHistoryReasonReference(models.Model):  
    _name = "hc.family.member.history.reason.reference"   
    _description = "Family Member History Reason Reference"           
    _inherit = ["hc.basic.association"] 
    
    family_member_history_id = fields.Many2one(
        comodel_name="hc.res.family.member.history", 
        string="Family Member History", 
        help="Family Member History associated with this Family Member History Reason Reference.")                      
    reason_reference_type = fields.Selection(
        string="Reason Reference Type", 
        selection=[
            ("condition", "Condition"), 
            ("observation", "Observation"), 
            ("allergy_intolerance", "Allergy Intolerance"), 
            ("questionnaire_response", "Questionnaire Response")], 
        help="Type of what is account tied to.")                     
    reason_reference_name = fields.Char(
        string="Reason Reference", 
        compute="_compute_reason_reference_name", 
        store="True", 
        help="Why was family member history performed.")                     
    reason_reference_condition_id = fields.Many2one(
        comodel_name="hc.res.condition", 
        string="Reason Reference Condition", 
        help="Condition account tied to.")                        
    reason_reference_observation_id = fields.Many2one(
        comodel_name="hc.res.observation", 
        string="Reason Reference Observation", 
        help="Observation account tied to.")                        
    reason_reference_allergy_intolerance_id = fields.Many2one(
        comodel_name="hc.res.allergy.intolerance", 
        string="Reason Reference Allergy Intolerance", 
        help="Allergy Intolerance account tied to.")                        
    reason_reference_questionnaire_response_id = fields.Many2one(
        comodel_name="hc.res.questionnaire.response", 
        string="Reason Reference Questionnaire Response", 
        help="Questionnaire Response account tied to.")                        
         
    @api.depends('reason_reference_type')           
    def _compute_reason_reference_name(self):           
        for hc_family_member_history_reason_reference in self:      
            if hc_family_member_history_reason_reference.reason_reference_type == 'condition':  
                hc_family_member_history_reason_reference.reason_reference_name = hc_family_member_history_reason_reference.reason_reference_condition_id.name
            elif hc_family_member_history_reason_reference.reason_reference_type == 'observation':  
                hc_family_member_history_reason_reference.reason_reference_name = hc_family_member_history_reason_reference.reason_reference_observation_id.name
            elif hc_family_member_history_reason_reference.reason_reference_type == 'allergy_intolerance':  
                hc_family_member_history_reason_reference.reason_reference_name = hc_family_member_history_reason_reference.reason_reference_allergy_intolerance_id.name
            elif hc_family_member_history_reason_reference.reason_reference_type == 'questionnaire_response':   
                hc_family_member_history_reason_reference.reason_reference_name = hc_family_member_history_reason_reference.reason_reference_questionnaire_response_id.name

class FamilyMemberHistoryNote(models.Model):  
    _name = "hc.family.member.history.note"  
    _description = "Family Member History Note"     
    _inherit = ["hc.basic.association", "hc.annotation"]

    family_member_history_id = fields.Many2one(
        comodel_name="hc.res.family.member.history", 
        string="Family Member History", 
        help="Family Member History associated with this Family Member History Note.")

    @api.depends('author_type')
    def _compute_author_name(self):
        for hc_family_member_history_note in self:
            if hc_family_member_history_note.author_type == 'string':
                hc_family_member_history_note.author_name = hc_family_member_history_note.author_string
            elif hc_family_member_history_note.author_type == 'practitioner':
                hc_family_member_history_note.author_name = hc_family_member_history_note.author_practitioner_id.name
            elif hc_family_member_history_note.author_type == 'patient':
                hc_family_member_history_note.author_name = hc_family_member_history_note.author_patient_id.name
            elif hc_family_member_history_note.author_type == 'related_person':
                hc_family_member_history_note.author_name = hc_family_member_history_note.author_related_person_id.name

class FamilyMemberHistoryConditionNote(models.Model):   
    _name = "hc.family.member.history.condition.note"   
    _description = "Family Member History Condition Note"           
    _inherit = ["hc.basic.association", "hc.annotation"]

    condition_id = fields.Many2one(
        comodel_name="hc.family.member.history.condition", 
        string="Condition", 
        help="Condition associated with this Family Member History Condition Note.")

    @api.depends('author_type')
    def _compute_author_name(self):
        for hc_family_member_history_note in self:
            if hc_family_member_history_note.author_type == 'string':
                hc_family_member_history_note.author_name = hc_family_member_history_note.author_string
            elif hc_family_member_history_note.author_type == 'practitioner':
                hc_family_member_history_note.author_name = hc_family_member_history_note.author_practitioner_id.name
            elif hc_family_member_history_note.author_type == 'patient':
                hc_family_member_history_note.author_name = hc_family_member_history_note.author_patient_id.name
            elif hc_family_member_history_note.author_type == 'related_person':
                hc_family_member_history_note.author_name = hc_family_member_history_note.author_related_person_id.name

class V3FamilyMember(models.Model): 
    _name = "hc.vs.v3.family.member"    
    _description = "V3 Family Member"       
    _inherit = ["hc.value.set.contains"]

    name = fields.Char(
        string="Name", 
        help="Name of this family member.")
    code = fields.Char(
        string="Code", 
        help="Code of this family member.")
    contains_id = fields.Many2one(
        comodel_name="hc.vs.v3.family.member", 
        string="Parent", 
        help="Parent family member.")


# External Reference

# class Patient(models.Model):
#     _inherit = ["hc.res.patient"]

#     family_member_history_ids = fields.One2many(
#         comodel_name="hc.res.family.member.history",
#         inverse_name="patient_id", 
#         string="Family Members", 
#         help="Relation with this patient.")
