# -*- coding: utf-8 -*-

from openerp import models, fields, api

class Goal(models.Model):    
    _name = "hc.res.goal"    
    _description = "Goal"        

    name = fields.Char(
        string="Event Name", 
        compute="_compute_name", 
        store="True", 
        help="Text representation of the goal event. Subject Name + Description + Start Date.")
    identifier_ids = fields.One2many(
        comodel_name="hc.goal.identifier", 
        inverse_name="goal_id", 
        string="Identifiers", 
        help="External IDs for this goal.")                
    status = fields.Selection(
        string="Goal Status", 
        required="True", 
        selection=[
            ("proposed", "Proposed"), 
            ("planned", "Planned"), 
            ("accepted", "Accepted"), 
            ("rejected", "Rejected"), 
            ("in-progress", "In Progress"), 
            ("achieved", "Achieved"), 
            ("sustaining", "Sustaining"), 
            ("on-hold", "On Hold"), 
            ("cancelled", "Cancelled"), 
            ("on-target", "On Target"), 
            ("ahead-of-target", "Ahead Of Target"), 
            ("behind-target", "Behind-Target")],
        help="Indicates whether the goal has been reached and is still considered relevant.")
    category_ids = fields.Many2many(
        comodel_name="hc.vs.goal.category", 
        relation="goal_category_rel", 
        string="Categories", 
        help="E.g. Treatment, dietary, behavioral, etc.")               
    priority = fields.Selection(
        string="Goal Priority", 
        selection=[
            ("high", "High"), 
            ("medium", "Medium"), 
            ("low", "Low")], 
        help="Identifies the mutually agreed level of importance associated with reaching/sustaining the goal.")
    description_id = fields.Many2one(
        comodel_name="hc.vs.clinical.finding", 
        string="Description", 
        required="True", 
        help="Code or text describing goal.")
    subject_type = fields.Selection(
        string="Subject Type", 
        selection=[
            ("patient", "Patient"), 
            ("group", "Group"), 
            ("organization", "Organization")], 
        help="Type of who this goal is intended for.")                
    subject_name = fields.Char(
        string="Subject", 
        compute="_compute_subject_name", 
        store="True", 
        help="Who this goal is intended for.")                
    subject_patient_id = fields.Many2one(
        comodel_name="hc.res.patient", 
        string="Subject Patient", 
        help="Patient who this goal is intended for.")                
    subject_group_id = fields.Many2one(
        comodel_name="hc.res.group", 
        string="Subject Group", 
        help="Group who this goal is intended for.")                
    subject_organization_id = fields.Many2one(
        comodel_name="hc.res.organization", 
        string="Subject Organization", 
        help="Organization who this goal is intended for.")                
    start_type = fields.Selection(
        string="Start Type", 
        selection=[
            ("date", "Date"), 
            ("code", "Code")], 
        help="Type of when goal pursuit begins.")                
    start_name = fields.Char(
        string="Start", 
        compute="_compute_start_name", 
        store="True", 
        help="When goal pursuit begins.")                
    start_date = fields.Date(
        string="Start Date", 
        help="When goal pursuit begins.")                
    start_code_id = fields.Many2one(
        comodel_name="hc.vs.goal.start.event", 
        string="Start Code", 
        help="Code of when goal pursuit begins.")                                              
    status_date = fields.Date(
        string="Status Date", 
        help="When goal status took effect.")                
    status_reason_ids = fields.Many2many(
        comodel_name="hc.vs.goal.status.reason", 
        relation="goal_status_reason_rel", 
        string="Categories", 
        help="Reason for current status.")                
    expressed_by_type = fields.Selection(
        string="Expressed By Type", 
        selection=[
            ("patient", "Patient"), 
            ("practitioner", "Practitioner"), 
            ("related_person", "Related Person")], 
        help="Type of who is responsible for creating goal.")                
    expressed_by_name = fields.Char(
        string="Expressed By", 
        compute="_compute_expressed_by_name", 
        store="True", 
        help="Who's responsible for creating Goal?")                
    expressed_by_patient_id = fields.Many2one(
        comodel_name="hc.res.patient", 
        string="Expressed By Patient", 
        help="Patient who's responsible for creating goal?")                
    expressed_by_practitioner_id = fields.Many2one(
        comodel_name="hc.res.practitioner", 
        string="Expressed By Practitioner", 
        help="Practitioner who's responsible for creating goal?")                
    expressed_by_related_person_id = fields.Many2one(
        comodel_name="hc.res.related.person", 
        string="Expressed By Related Person", 
        help="Related Person who's responsible for creating goal?")                                
    addresses_ids = fields.One2many(
        comodel_name="hc.goal.addresses", 
        inverse_name="goal_id", 
        string="Addressess", 
        help="Issues addressed by this goal.")                
    note_ids = fields.One2many(
        comodel_name="hc.goal.note", 
        inverse_name="goal_id", 
        string="Notes", 
        help="Comments about the goal.")                                               
    outcome_code_ids = fields.Many2many(
        comodel_name="hc.vs.clinical.finding", 
        relation="goal_outcome_code_rel", 
        string="Categories", 
        help="What result was achieved regarding the goal?")
    outcome_reference_ids = fields.One2many(
        comodel_name="hc.goal.outcome.reference", 
        inverse_name="goal_id", 
        string="Outcome References", 
        help="Observation that resulted from goal.")
    target_ids = fields.One2many(
        comodel_name="hc.goal.target", 
        inverse_name="goal_id", 
        string="Targets", 
        help="Target outcome for the goal.")

class GoalTarget(models.Model): 
    _name = "hc.goal.target"    
    _description = "Goal Target"

    goal_id = fields.Many2one(
        comodel_name="hc.res.goal", 
        string="Goal", 
        help="Goal associated with this target.")
    measure_id = fields.Many2one(
        comodel_name="hc.vs.observation.code", 
        string="Measure", 
        help="The parameter whose value is being tracked.")
    detail_type = fields.Selection(
        string="Detail Type", 
        selection=[
            ("quantity", "Quantity"), 
            ("range", "Range"), 
            ("codeable_concept", "Codeable Concept")], 
        help="Type of the target value to be achieved.")
    detail_name = fields.Char(
        string="Detail", 
        compute="_compute_detail_name", 
        store="True", 
        help="The target value to be achieved.")
    detail_quantity = fields.Float(
        string="Detail Quantity", 
        help="The target value to be achieved.")
    detail_quantity_uom_id = fields.Many2one(
        comodel_name="product.uom", 
        string="Detail Start Date UOM", 
        help="Detail Quantity unit of measure.")
    detail_start_date = fields.Datetime(
        string="Detail Start Date", 
        help="Start of the target value to be achieved.")
    detail_end_date = fields.Datetime(
        string="Detail End Date", 
        help="End of the target value to be achieved.")
    detail_code_id = fields.Many2one(
        comodel_name="hc.vs.goal.target.detail", 
        string="Detail Code", 
        help="Code of the target value to be achieved.")
    due_type = fields.Selection(
        string="Due Type", 
        selection=[
            ("date", "Date"), 
            ("duration", "Duration")], 
            help="Type of reach goal on or before.")
    due_name = fields.Char(
        string="Due", 
        compute="_compute_due_name", 
        store="True", 
        help="Reach goal on or before.")
    due_date = fields.Date(
        string="Due Date", 
        help="Reach goal on or before.")
    due_duration = fields.Float(
        string="Due Duration", 
        help="Duration reach goal on or before.")
    due_duration_uom_id = fields.Many2one(
        comodel_name="product.uom", 
        string="Due Duration UOM", 
        domain="[('category_id','=','Time (UCUM)')]", 
        help="Due Duration unit of measure.") 

class GoalIdentifier(models.Model):    
    _name = "hc.goal.identifier"    
    _description = "Goal Identifier"        
    _inherit = ["hc.basic.association", "hc.identifier"]

    goal_id = fields.Many2one(
        comodel_name="hc.res.goal", 
        string="Goal", 
        help="Goal associated with this Goal Identifier.")  

class GoalAddresses(models.Model):    
    _name = "hc.goal.addresses"    
    _description = "Goal Addresses"        
    _inherit = ["hc.basic.association"]

    goal_id = fields.Many2one(
        comodel_name="hc.res.goal", 
        string="Goal", 
        help="Goal associated with this Goal Addresses.")                
    addresses_type = fields.Selection(
        string="Addresses Type", 
        selection=[
            ("condition", "Condition"), 
            ("observation", "Observation"),
            ("medication_statement", "Medication Statement"), 
            ("nutrition_order", "Nutrition Order"),
            ("procedure_request", "Procedure Request"), 
            ("risk_assessment", "Risk Assessment")],
        help="Type of issues addressed by this goal.")                
    addresses_name = fields.Char(
        string="Addresses", 
        compute="_compute_addresses_name", 
        store="True", 
        help="Issues addressed by this goal.")                
    addresses_condition_ids = fields.Many2one(
        comodel_name="hc.res.condition", 
        string="Addresses Conditions", 
        help="Condition issues addressed by this goal.")                
    addresses_observation_ids = fields.Many2one(
        comodel_name="hc.res.observation", 
        string="Addresses Observations", 
        help="Observation issues addressed by this goal.")                
    addresses_medication_statement_ids = fields.Many2one(
        comodel_name="hc.res.medication.statement", 
        string="Addresses Medication Statements", 
        help="Medication Statement issues addressed by this goal.")                
    addresses_nutrition_order_id = fields.Many2one(
        comodel_name="hc.res.nutrition.order", 
        string="Addresses Nutrition Order", 
        help="Nutrition Order issues addressed by this goal.")               
    addresses_procedure_request_ids = fields.Many2one(
        comodel_name="hc.res.procedure.request", 
        string="Addresses Procedure Requests", 
        help="Procedure Request issues addressed by this goal.")                
    addresses_risk_assessment_ids = fields.Many2one(
        comodel_name="hc.res.risk.assessment", 
        string="Addresses Risk Assessments", 
        help="Risk Assessment issues addressed by this goal.")                                          

class GoalNote(models.Model):    
    _name = "hc.goal.note"    
    _description = "Goal Note"        
    _inherit = ["hc.basic.association", "hc.annotation"]

    goal_id = fields.Many2one(
        comodel_name="hc.res.goal", 
        string="Goal", 
        help="Goal associated with this Goal Note.")                               

class GoalOutcomeReference(models.Model):
    _name = "hc.goal.outcome.reference"
    _description = "Goal Outcome Reference"
    _inherit = ["hc.basic.association"]

    goal_id = fields.Many2one(
        comodel_name="hc.res.goal", 
        string="Goal", 
        help="Goal associated with this Goal Outcome Reference.")                  
    outcome_reference_id = fields.Many2one(
        comodel_name="hc.res.observation", 
        string="Outcome Reference", 
        help="Observation associated with this Goal Outcome Reference.")

class GoalStatusReason(models.Model):    
    _name = "hc.vs.goal.status.reason"    
    _description = "Goal Status Reason"        
    _inherit = ["hc.value.set.contains"]

    name = fields.Char(
        string="Name", 
        help="Name of this goal status reason.")
    code = fields.Char(
        string="Code", 
        help="Code of this goal status reason.")
    contains_id = fields.Many2one(
        comodel_name="hc.vs.goal.status.reason", 
        string="Parent", 
        help="Parent goal status reason.")

class GoalTargetDetail(models.Model):
    _name = "hc.vs.goal.target.detail"
    _description = "Goal Target Detail"
    _inherit = ["hc.value.set.contains"]

    name = fields.Char(
        tring="Name", 
        help="Name of this goal target detail.")                  
    code = fields.Char(
        string="Code", 
        help="Code of this goal target detail.")                  
    contains_id = fields.Many2one(
        comodel_name="hc.vs.goal.target.detail", 
        string="Parent", 
        help="Parent goal target detail.")                  

# External reference

# class CarePlanGoal(models.Model):    
#     _inherit = "hc.care.plan.goal"    
#     _description = "Care Plan Goal"        
#     _inherit = ["hc.basic.association"]
                
#     goal_id = fields.Many2one(
#         comodel_name="hc.res.goal", 
#         string="Goal", 
#         help="Goal associated with this Care Plan Goal.")

# class CarePlanActivityDetailGoal(models.Model):    
#     _inherit = "hc.care.plan.activity.detail.goal"    
              
#     goal_id = fields.Many2one(
#         comodel_name="hc.res.goal", 
#         string="Goal", 
#         help="Goal associated with this Care Plan Activity Detail Goal.")

# class CarePlanActivityDetail(models.Model):    
#     _inherit = "hc.care.plan.activity.detail"

#     status_reason_id = fields.Many2one(
#         comodel_name="hc.vs.goal.status.reason", 
#         string="Status Reason", 
#         help="Reason for current status.")