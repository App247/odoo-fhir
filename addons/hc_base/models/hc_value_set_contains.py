# -*- coding: utf-8 -*-

from openerp import models, fields, api

class ValueSetContains(models.AbstractModel):

    _name = "hc.value.set.contains"
    _description = "Value Set Contains"
    _parent_name = "contains_id"  
    _parent_store = "True"  
    _parent_order = "name"
    _order = "parent_left"
    _order = "parent_left"
    _inherit = ["hc.codeable.concept.coding"]


    is_abstract = fields.Boolean(
        string="Abstract", 
        help="If user cannot select this entry.")
    name = fields.Char(
        string="Name", 
        help="User display for the concept.")
    level = fields.Integer(
        string="Level", 
        help="Level as a parent in a hierarchy of codes.")
    child_level = fields.Integer(
        string="Child Level",
        compute="_compute_child_level", 
        help="Level as child in a hierarchy of codes.")
    source_id = fields.Many2one(
        comodel_name="res.partner", 
        string="Source", 
        help="The source of the definition of the code.")
    definition = fields.Text(
        string="Definition", 
        help="An explanation of the meaning of the concept.")
    comments = fields.Text(
        string="Comments", 
        help="Additional notes about how to use the code.")
    contains_id = fields.Many2one(
        comodel_name="hc.value.set.contains", 
        string="Parent",
        ondelete="restrict",
        index="True",
        help="Parent concept.")
    child_ids = fields.One2many(
        comodel_name="hc.value.set.contains", 
        inverse_name="contains_id", 
        string="Children concepts", 
        help="Child concept.")
    parent_left = fields.Integer(
        string="Left Parent", 
        index="True", 
        help="Special field related to the contains_id field. Makes queries execute efficiently.")
    parent_right = fields.Integer(
        string="Right Parent", 
        index="True", 
        help="Special field related to the contains_id field. Makes queries execute efficiently.")

    _sql_constraints = [
        ('code_unique',
        'UNIQUE(code)',
        "The concept code must be unique.")
        ]

    @api.depends('level')
    def _compute_child_level(self):
        self.child_level = self.level + 1

    # @api.one
    # @api.constrains('name', 'description')
    # def _check_description(self):
    #     if self.name == self.description:
    #         raise ValidationError("Concept name and description must be different")

    @api.constrains('contains_id')
    def _check_hierarchy(self):
        if not self._check_recursion():
            raise models.ValidationError(
                'Error! You cannot create recursive categories.')

class ActCode(models.Model):   
    _name = "hc.vs.act.code"
    _description = "Act Code"  
    _inherit = ["hc.value.set.contains"]

    name = fields.Char(
        string="Name", 
        help="Name of this act.")
    code = fields.Char(
        string="Code", 
        help="Code of this act.")
    contains_id = fields.Many2one(
        comodel_name="hc.vs.act.code", 
        string="Parent",
        help="Parent art code.")

class ActionCode(models.Model):    
    _name = "hc.vs.action.code"    
    _description = "Action Code"        
    _inherit = ["hc.value.set.contains"]

    name = fields.Char(
        string="Name", 
        help="Name of this action.")
    code = fields.Char(
        string="Code", 
        help="Code of this action.")
    contains_id = fields.Many2one(
        comodel_name="hc.vs.action.code", 
        string="Parent",
        help="Parent action code.")

class ActionParticipantRole(models.Model):  
    _name = "hc.vs.action.participant.role" 
    _description = "Action Participant Role"            
    _inherit = ["hc.value.set.contains"]
    
    name = fields.Char(
        string="Name", 
        help="Name of this action participant role.")                 
    code = fields.Char(
        string="Code", 
        help="Code of this action participant role.")                 
    contains_id = fields.Many2one(
        comodel_name="hc.vs.action.participant.role", 
        string="Contains", 
        help="Parent action participant role.") 

class ActReason(models.Model):    
    _name = "hc.vs.act.reason"    
    _description = "Act Reason"        
    _inherit = ["hc.value.set.contains"]

    name = fields.Char(
        string="Name", 
        help="Name of this act reason.")
    code = fields.Char(
        string="Code", 
        help="Code of this act reason.")
    contains_id = fields.Many2one(
        comodel_name="hc.vs.act.reason", 
        string="Parent",
        help="Parent act reason.")

class AdministrativeGender(models.Model):   
    _name = "hc.vs.administrative.gender"   
    _description = "Administrative Gender"      
    _inherit = ["hc.value.set.contains"]

    name = fields.Char(
        string="Name", 
        help="Name of this administrative gender.")
    code = fields.Char(
        string="Code", 
        help="Code of this administrative gender.")
    contains_id = fields.Many2one(
        comodel_name="hc.vs.administrative.gender", 
        string="Parent",
        help="Parent concept.")

class AdministrationMethodCode(models.Model):    
    _name = "hc.vs.administration.method.code"    
    _description = "Administration Method Code"        
    _inherit = ["hc.value.set.contains"]

    name = fields.Char(
        string="Name", 
        help="Name of this administration method.")
    code = fields.Char(
        string="Code", 
        help="Code of this administration method.")
    contains_id = fields.Many2one(
        comodel_name="hc.vs.administration.method.code", 
        string="Parent",
        help="Parent concept.")

class ApproachSiteCode(models.Model):    
    _name = "hc.vs.approach.site.code"    
    _description = "Approach Site Code"        
    _inherit = ["hc.value.set.contains"]

    name = fields.Char(
        string="Name", 
        help="Name of this approach site code.")
    code = fields.Char(
        string="Code", 
        help="Code of this approach site code.")
    contains_id = fields.Many2one(
        comodel_name="hc.vs.approach.site.code", 
        string="Parent",
        help="Parent approach site code.")

class BodySite(models.Model):   
    _name = "hc.vs.body.site"   
    _description = "Body Site"      
    _inherit = ["hc.value.set.contains"]

    name = fields.Char(
        string="Name", 
        help="Name of this body site.")
    code = fields.Char(
        string="Code", 
        help="Code of this body site.")
    contains_id = fields.Many2one(
        comodel_name="hc.vs.body.site", 
        string="Parent",
        help="Parent body site.")

class C80DocClassCode(models.Model):    
    _name = "hc.vs.c80.doc.class.code"    
    _description = "C80 Doc Class Code"        
    _inherit = ["hc.value.set.contains"]

    name = fields.Char(
        string="Name", 
        help="Name of this C80 doc class.")
    code = fields.Char(
        string="Code", 
        help="Code of this C80 Doc Class.")
    contains_id = fields.Many2one(
        comodel_name="hc.vs.c80.doc.class.code", 
        string="Parent",
        help="Parent c80 doc class.")

class C80DocTypeCode(models.Model):    
    _name = "hc.vs.c80.doc.type.code"    
    _description = "C80 Doc Type Code"        
    _inherit = ["hc.value.set.contains"]

    name = fields.Char(
        string="Name", 
        help="Name of this C80 doc type.")
    code = fields.Char(
        string="Code", 
        help="Code of this C80 doc type.")
    contains_id = fields.Many2one(
        comodel_name="hc.vs.c80.doc.type.code", 
        string="Parent",
        help="Parent C80 doc type.")

class C80FacilityCode(models.Model):    
    _name = "hc.vs.c80.facility.code"    
    _description = "C80 Facility Code"        
    _inherit = ["hc.value.set.contains"]

    name = fields.Char(
        string="Name", 
        help="Name of this C80 facility code.")
    code = fields.Char(
        string="Code", 
        help="Code of this C80 facility code.")
    contains_id = fields.Many2one(
        comodel_name="hc.vs.c80.facility.code", 
        string="Parent",
        help="Parent C80 facility code.")

class C80PracticeCode(models.Model):   
    _name = "hc.vs.c80.practice.code"  
    _description = "C80 Practice Code"     
    _inherit = ["hc.value.set.contains"]  

    name = fields.Char(
        string="Name", 
        help="Name of this C80 practice code.")
    code = fields.Char(
        string="Code", 
        help="Code of this C80 practice code.")
    contains_id = fields.Many2one(
        comodel_name="hc.vs.c80.practice.code", 
        string="Parent",
        help="Parent C80 practice code.")

class ClinicalConcept(models.Model):    
    _name = "hc.vs.clinical.concept"    
    _description = "Clinical Concept"       
    _inherit = ["hc.value.set.contains"]

    name = fields.Char(
        string="Name", 
        help="Name of this clinical concept.")
    code = fields.Char(
        string="Code", 
        help="Code of this clinical concept.")
    contains_id = fields.Many2one(
        comodel_name="hc.vs.clinical.concept", 
        string="Parent",
        help="Parent clinical concept.")

class ConditionCode(models.Model):
    _name = "hc.vs.condition.code"
    _description = "Condition"
    _inherit = ["hc.value.set.contains"]

    name = fields.Char(
        string="Name", 
        help="Name of this condition code.")
    code = fields.Char(
        string="Code", 
        help="Code of this condition code.")
    contains_id = fields.Many2one(
        comodel_name="hc.vs.condition.code", 
        string="Parent",
        help="Parent condition code.")

class ConditionOutcome(models.Model):
    _name = "hc.vs.condition.outcome"
    _description = "Condition Outcome"
    _inherit = ["hc.value.set.contains"]        

    name = fields.Char(
        string="Name", 
        help="Name of this condition outcome.")
    code = fields.Char(
        string="Code", 
        help="Code of this condition outcome.")
    contains_id = fields.Many2one(
        comodel_name="hc.vs.condition.outcome", 
        string="Parent",
        help="Parent condition outcome.")

class DaysOfWeek(models.Model):  
    _name = "hc.vs.days.of.week"  
    _description = "Days Of Week"     
    _inherit = ["hc.value.set.contains"]

    name = fields.Char(
        string="Name", 
        help="Name of this day of week.")
    code = fields.Char(
        string="Code", 
        help="Code of this day of week.")
    contains_id = fields.Many2one(
        comodel_name="hc.vs.days.of.week", 
        string="Parent",
        help="Parent day of week.")

class DefinedType(models.Model):    
    _name = "hc.vs.defined.type"    
    _description = "Defined Type"            
    _inherit = ["hc.value.set.contains"]    

    name = fields.Char(
        string="Name", 
        help="Name of this defined type.")
    code = fields.Char(
        string="Code", 
        help="Code of this defined type.")
    contains_id = fields.Many2one(
        comodel_name="hc.vs.defined.type", 
        string="Parent",
        help="Parent defined type.")

class DemographicAgeGroup(models.Model):    
    _name = "hc.vs.demographic.age.group"   
    _description = "Demographic Age Group"      
    _inherit = ["hc.value.set.contains"]

    name = fields.Char(
        string="Name", 
        help="Name of this demographic age group.")
    code = fields.Char(
        string="Code", 
        help="Code of this demographic age group.")
    contains_id = fields.Many2one(
        comodel_name="hc.vs.demographic.age.group", 
        string="Parent",
        help="Parent demographic age group.")

class DesignationUse(models.Model):    
    _name = "hc.vs.designation.use"    
    _description = "Designation Use"            
    _inherit = ["hc.value.set.contains"] 

    name = fields.Char(
        string="Name", 
        help="Name of this designation use.")
    code = fields.Char(
        string="Code", 
        help="Code of this designation use.")
    contains_id = fields.Many2one(
        comodel_name="hc.vs.designation.use",
        string="Parent",
        help="Parent designation use.")

class ClinicalFinding(models.Model):    
    _name = "hc.vs.clinical.finding"    
    _description = "Clinical Finding"        
    _inherit = ["hc.value.set.contains"]

    name = fields.Char(
        string="Name", 
        help="Name of this clinical finding.")
    code = fields.Char(
        string="Code", 
        help="Code of this clinical finding.")
    contains_id = fields.Many2one(
        comodel_name="hc.vs.clinical.finding", 
        string="Contains", 
        help="Parent clinical finding.")

class EncounterParticipantType(models.Model):   
    _name = "hc.vs.encounter.participant.type"  
    _description = "Encounter Participant Type"     
    _inherit = ["hc.value.set.contains"]

    name = fields.Char(
        string="Name", 
        help="Name of this encounter participant type.")
    code = fields.Char(
        string="Code", 
        help="Code of this encounter participant type.")
    contains_id = fields.Many2one(
        comodel_name="hc.vs.encounter.participant.type",
        string="Parent",
        help="Parent participant type.")

class EncounterReason(models.Model):    
    _name = "hc.vs.encounter.reason"    
    _description = "Encounter Reason"       
    _inherit = ["hc.value.set.contains"]

    name = fields.Char(
        string="Name", 
        help="Name of this encounter reason.")
    code = fields.Char(
        string="Code", 
        help="Code of this encounter reason.")
    contains_id = fields.Many2one(
        comodel_name="hc.vs.encounter.reason",
        string="Parent",
        help="Parent encounter reason.")

class Ethnicity(models.Model):  
    _name = "hc.vs.ethnicity"  
    _description = "Ethnicity" 
    _inherit = ["hc.value.set.contains"]

    name = fields.Char(
        string="Name", 
        help="Name of this ethnicity.")
    code = fields.Char(
        string="Code", 
        help="Code of this ethnicity.")
    contains_id = fields.Many2one(
        comodel_name="hc.vs.ethnicity",
        string="Parent",
        help="Parent ethnicity.")

class FormatCode(models.Model): 
    _name = "hc.vs.format.code" 
    _description = "Format Code"        
    _inherit = ["hc.value.set.contains"]

    name = fields.Char(
        string="Name", 
        help="Name of this format code.")
    code = fields.Char(
        string="Code", 
        help="Code of this format code.")
    contains_id = fields.Many2one(
        comodel_name="hc.vs.format.code",
        string="Parent",
        help="Parent format code.")

class FormCode(models.Model):   
    _name = "hc.vs.form.code"   
    _description = "Form Code"      
    _inherit = ["hc.value.set.contains"]

    name = fields.Char(
        string="Name", 
        help="Name of this form code.")
    code = fields.Char(
        string="Code", 
        help="Code of this form code.")
    contains_id = fields.Many2one(
        comodel_name="hc.vs.form.code",
        string="Parent",
        help="Parent concept.")

class Forms(models.Model):    
    _name = "hc.vs.forms"    
    _description = "Forms"        
    _inherit = ["hc.value.set.contains"]

    name = fields.Char(
        string="Name", 
        help="Name of this form.")
    code = fields.Char(
        string="Code", 
        help="Code of this form.")
    contains_id = fields.Many2one(
        comodel_name="hc.vs.forms",
        string="Parent",
        help="Parent form.")

class GoalCategory(models.Model):    
    _name = "hc.vs.goal.category"    
    _description = "Goal Category"        
    _inherit = ["hc.value.set.contains"]

    name = fields.Char(
        string="Name", 
        help="Name of this goal category.")
    code = fields.Char(
        string="Code", 
        help="Code of this goal category.")
    contains_id = fields.Many2one(
        comodel_name="hc.vs.goal.category", 
        string="Contains", 
        help="Parent goal category.")

class GoalStartEvent(models.Model):    
    _name = "hc.vs.goal.start.event"    
    _description = "Goal Start Event"        
    _inherit = ["hc.value.set.contains"]

    name = fields.Char(
        string="Name", 
        help="Name of this goal start event.")
    code = fields.Char(
        string="Code", 
        help="Code of this goal start event.")
    contains_id = fields.Many2one(
        comodel_name="hc.vs.goal.start.event", 
        string="Contains", 
        help="Parent goal start event.")

class Jurisdiction(models.Model):   
    _name = "hc.vs.jurisdiction"    
    _description = "Jurisdiction"       
    _inherit = ["hc.value.set.contains"]

    name = fields.Char(
        string="Name", 
        help="Name of this jurisdiction.")
    code = fields.Char(
        string="Code", 
        help="Code of this jurisdiction.")
    contains_id = fields.Many2one(
        comodel_name="hc.vs.jurisdiction",
        string="Parent",
        help="Parent jurisdiction.")  

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

class MedicationAsNeededReason(models.Model):    
    _name = "hc.vs.medication.as.needed.reason"    
    _description = "Medication As Needed Reason"        
    _inherit = ["hc.value.set.contains"]

    name = fields.Char(
        string="Name", 
        help="Name of this medication as needed reason.")
    code = fields.Char(
        string="Code", 
        help="Code of this medication as needed reason.")
    contains_id = fields.Many2one(
        comodel_name="hc.vs.medication.as.needed.reason",
        string="Parent",
        help="Parent medication as needed reason.")

class MessageEvent(models.Model):    
    _name = "hc.vs.message.event"    
    _description = "Message Event"        
    _inherit = ["hc.value.set.contains"] 

    name = fields.Char(
        string="Name", 
        help="Name of this message event.")
    code = fields.Char(
        string="Code", 
        help="Code of this message event.")
    contains_id = fields.Many2one(
        comodel_name="hc.vs.message.event",
        string="Parent",
        help="Parent message event.")
    
class ObservationCode(models.Model):    
    _name = "hc.vs.observation.code"    
    _description = "Observation Code"           
    _inherit = ["hc.value.set.contains"]

    name = fields.Char(
        string="Name", 
        help="Name of this observation code.")                    
    code = fields.Char(
        string="Code", 
        help="Code of this observation code.")                    
    contains_id = fields.Many2one(
        comodel_name="hc.vs.observation.code", 
        string="Contains", 
        help="Parent observation code.")  

class OccupationCode(models.Model):  
    _name = "hc.vs.occupation.code"  
    _description = "Occupation Code" 
    _inherit = ["hc.value.set.contains"]

    name = fields.Char(
        string="Name", 
        help="Name of this occupation code.")
    code = fields.Char(
        string="Code", 
        help="Code of this occupation code.")
    contains_id = fields.Many2one(
        comodel_name="hc.vs.occupation.code",
        string="Parent",
        help="Parent occupation code.")

class ParticipantRole(models.Model):    
    _name = "hc.vs.participant.role"    
    _description = "Participant Role"      
    _inherit = ["hc.value.set.contains"]

    name = fields.Char(
        string="Name", 
        help="Name of this participant role.")
    code = fields.Char(
        string="Code", 
        help="Code of this participant role.")
    contains_id = fields.Many2one(
        comodel_name="hc.vs.participant.role",
        string="Parent",
        help="Parent participant role.")

class ParticipationType(models.Model): 
    _name = "hc.vs.participation.type" 
    _description = "Participation Type"
    _inherit = ["hc.value.set.contains"]

    name = fields.Char(
        string="Name", 
        help="Name of this participation type (e.g., admitter).")
    code = fields.Char(
        string="Code", 
        help="Code of this participation type (e.g., ADM).")
    contains_id = fields.Many2one(
        comodel_name="hc.vs.participation.type", 
        string="Parent",
        help="Parent participation type.")

class PurposeOfUse(models.Model):    
    _name = "hc.vs.purpose.of.use"    
    _description = "Purpose Of Use"        
    _inherit = ["hc.value.set.contains"]

    name = fields.Char(
        string="Name", 
        help="Name of this purpose of use.")
    code = fields.Char(
        string="Code", 
        help="Code of this purpose of use.")
    contains_id = fields.Many2one(
        comodel_name="hc.vs.purpose.of.use",
        string="Parent",
        help="Parent purpose of use")

class Race(models.Model):  
    _name = "hc.vs.race"  
    _description = "Race" 
    _inherit = ["hc.value.set.contains"]

    name = fields.Char(
        string="Name", 
        help="Name of this race.")
    code = fields.Char(
        string="Code", 
        help="Code of this race.")
    contains_id = fields.Many2one(
        comodel_name="hc.vs.race",
        string="Parent",
        help="Parent race.")  

class RequestPriority(models.Model):    
    _name = "hc.vs.request.priority"    
    _description = "Request Priority"        
    _inherit = ["hc.value.set.contains"]

    name = fields.Char(
        string="Name", 
        help="Name of this request priority.")
    code = fields.Char(
        string="Code", 
        help="Code of this request priority.")
    contains_id = fields.Many2one(
        comodel_name="hc.vs.request.priority",
        string="Parent",
        help="Parent request priority.")

class ResourceType(models.Model):   
    _name = "hc.vs.resource.type"   
    _description = "Resource Type"      
    _inherit = ["hc.value.set.contains"]   

    name = fields.Char(
        string="Name", 
        help="Name of this resource type.")
    code = fields.Char(
        string="Code", 
        help="Code of this resource type.")
    contains_id = fields.Many2one(
        comodel_name="hc.vs.resource.type",
        string="Parent",
        help="Parent resource type.")

class RouteCode(models.Model): 
    _name = "hc.vs.route.code" 
    _description = "Route Code"        
    _inherit = ["hc.value.set.contains"]  

    name = fields.Char(
        string="Name", 
        help="Name of this route code.")
    code = fields.Char(
        string="Code", 
        help="Code of this route code.")
    contains_id = fields.Many2one(
        comodel_name="hc.vs.route.code",
        string="Parent",
        help="Parent route code.")

class Ruleset(models.Model):    
    _name = "hc.vs.ruleset"    
    _description = "Ruleset"        
    _inherit = ["hc.value.set.contains"]

    name = fields.Char(
        string="Name", 
        help="Name of this ruleset.")
    code = fields.Char(
        string="Code", 
        help="Code of this ruleset.")
    contains_id = fields.Many2one(
        comodel_name="hc.vs.ruleset",
        string="Parent",
        help="Parent ruleset.")

class SecurityLabel(models.Model):  
    _name = "hc.vs.security.label"  
    _description = "Security Label"     
    _inherit = ["hc.value.set.contains"]

    name = fields.Char(
        string="Name", 
        help="Name of this security label.")
    code = fields.Char(
        string="Code", 
        help="Code of this security label.")
    contains_id = fields.Many2one(
        comodel_name="hc.vs.security.label",
        string="Parent",
        help="Parent security label.")
   
class TimeUOM(models.Model): 
    _name = "hc.vs.time.uom" 
    _description = "Time Unit of Measure"            
    _inherit = ["hc.value.set.contains", "product.uom"]

    name = fields.Char(
        string="Name", 
        help="Name of time unit of measure.")
    code = fields.Char(
        string="Code", 
        help="Code of this time unit of measure.")
    contains_id = fields.Many2one(
        comodel_name="hc.vs.time.uom",
        string="Parent",
        help="Parent time unit of measure.")

class UserType(models.Model):   
    _name = "hc.vs.user.type"   
    _description = "User Type"      
    _inherit = ["hc.value.set.contains"]

    name = fields.Char(
        string="Name", 
        help="Name of this user type.")
    code = fields.Char(
        string="Code", 
        help="Code of this user type.")
    contains_id = fields.Many2one(
        comodel_name="hc.vs.user.type",
        string="Parent",
        help="Parent user type.")

class WorkflowSetting(models.Model):    
    _name = "hc.vs.workflow.setting"    
    _description = "Workflow Setting"       
    _inherit = ["hc.value.set.contains"]

    name = fields.Char(
        string="Name", 
        help="Name of this workflow setting.")
    code = fields.Char(
        string="Code", 
        help="Code of this workflow setting.")
    contains_id = fields.Many2one(
        comodel_name="hc.vs.workflow.setting",
        string="Parent",
        help="Parent workflow setting.")

class WorkflowTask(models.Model):   
    _name = "hc.vs.workflow.task"   
    _description = "Workflow Task"      
    _inherit = ["hc.value.set.contains"]

    name = fields.Char(
        string="Name", 
        help="Name of this workflow task.")
    code = fields.Char(
        string="Code", 
        help="Code of this workflow task.")
    contains_id = fields.Many2one(
        comodel_name="hc.vs.workflow.task",
        string="Parent",
        help="Parent workflow task.")

# Standard Data Set

class EntityNameUse(models.Model):
    _name = "hc.vs.entity.name.use"
    _description = "Entity Name Use"
    _inherit = ["hc.value.set.contains"]

    name = fields.Char(
        string="Name", 
        help="Name of this entity name use.")                 
    code = fields.Char(
        string="Code", 
        help="Code of this entity name use.")                 
    contains_id = fields.Many2one(
        comodel_name="hc.vs.entity.name.use", 
        string="Parent", 
        help="Parent entity name use.")                    

