# -*- coding: utf-8 -*-

from openerp import models, fields, api

class PlanDefinition(models.Model):
    _name = "hc.res.plan.definition"
    _description = "Plan Definition"

    url = fields.Char(
        string="URI",
        help="Logical URI to reference this plan definition (globally unique).")
    identifier_ids = fields.One2many(
        comodel_name="hc.plan.definition.identifier",
        inverse_name="plan_definition_id",
        string="Identifiers",
        help="Additional identifier for the plan definition.")
    version = fields.Char(
        string="Version",
        help="Business version of the plan definition.")
    name = fields.Char(
        string="Name",
        help="Name for this plan definition (Computer friendly).")
    title = fields.Char(
        string="Title",
        help="Name for this plan definition (Human friendly).")
    type = fields.Selection(
        string="Type",
        selection=[
            ("order-set", "Order Set"),
            ("protocol", "Protocol"),
            ("eca-rule", "Eca Rule")],
        help="The type of action to perform (create, update, remove).")
    status = fields.Selection(
        string="Status",
        required="True",
        selection=[
            ("draft", "Draft"),
            ("active", "Active"),
            ("retired", "Retired")],
        help="The status of this plan definition. Enables tracking the life-cycle of the content.")
    is_experimental = fields.Boolean(
        string="Experimental",
        help="If for testing purposes, not real usage.")
    date = fields.Datetime(
        string="Date",
        help="Date this was last changed.")
    publisher = fields.Char(
        string="Publisher",
        help="Name of the publisher (Organization or individual).")
    description = fields.Text(
        string="Description",
        help="Natural language description of the plan definition.")
    purpose = fields.Text(
        string="Purpose",
        help="Why this plan definition is defined.")
    usage = fields.Text(
        string="Usage",
        help="Describes the clinical usage of the asset.")
    approval_date = fields.Date(
        string="Approval Date",
        help="When plan definition approved by publisher.")
    last_review_date = fields.Date(
        string="Last Review Date",
        help="Last review date for the plan definition.")
    effective_period_start_date = fields.Datetime(
        string="Effective Period Start Date",
        help="Start of the effective date range for the plan definition.")
    effective_period_end_date = fields.Datetime(
        string="Effective Period End Date",
        help="End of the effective date range for the service definition.")
    use_context_ids = fields.One2many(
        comodel_name="hc.plan.definition.use.context",
        inverse_name="plan_definition_id",
        string="Use Contexts",
        help="Content intends to support these contexts.")
    jurisdiction_ids = fields.Many2many(
        comodel_name="hc.vs.jurisdiction",
        relation="plan_definition_jurisdiction_rel",
        string="Jurisdictions",
        help="Intended jurisdiction for plan definition (if applicable).")
    topic_ids = fields.Many2many(
        comodel_name="hc.vs.definition.topic", 
        relation="plan_definition_topic_rel",
        string="Topics",
        help="Descriptional topics for the asset.")
    contributor_ids = fields.One2many(
        comodel_name="hc.plan.definition.contributor",
        inverse_name="plan_definition_id",
        string="Contributors",
        help="A content contributor.")
    contact_ids = fields.One2many(
        comodel_name="hc.plan.definition.contact",
        inverse_name="plan_definition_id",
        string="Contacts",
        help="Contact details for the publisher.")
    copyright = fields.Text(
        string="Copyright",
        help="Use and/or publishing restrictions.")
    related_artifact_ids = fields.One2many(
        comodel_name="hc.plan.definition.related.artifact",
        inverse_name="plan_definition_id",
        string="Related Artifacts",
        help="Related artifacts for the asset.")
    library_ids = fields.One2many(
        comodel_name="hc.plan.definition.library",
        inverse_name="plan_definition_id",
        string="Libraries",
        help="Logic used by the plan definition.")
    goal_definition_ids = fields.One2many(
        comodel_name="hc.plan.definition.goal.definition",
        inverse_name="plan_definition_id",
        string="Goal Definitions",
        help="What the plan is trying to accomplish.")
    action_definition_ids = fields.One2many(
        comodel_name="hc.plan.definition.action.definition",
        inverse_name="plan_definition_id",
        string="Action Definitions",
        help="Action defined by the plan.")

class PlanDefinitionGoalDefinition(models.Model):
    _name = "hc.plan.definition.goal.definition"
    _description = "Plan Definition Goal Definition"

    plan_definition_id = fields.Many2one(
        comodel_name="hc.res.plan.definition",
        string="Plan Definition",
        help="Plan Definition associated with this Plan Definition Goal Definition.")
    category_id = fields.Many2one(
        comodel_name="hc.vs.goal.category",
        string="Category",
        help="E.g. Treatment, dietary, behavioral, etc.")
    description_id = fields.Many2one(
        comodel_name="hc.vs.clinical.finding",
        string="Description",
        required="True",
        help="Code or text describing the goal.")
    priority = fields.Selection(
        string="Priority",
        selection=[
            ("high-priority", "High Priority"),
            ("medium-priority", "Medium Priority"),
            ("low-priority", "Low Priority")],
        help="Identifies the expected level of importance associated with reaching/sustaining the defined goal.")
    start_id = fields.Many2one(
        comodel_name="hc.vs.goal.start.event",
        string="Start",
        help="When goal pursuit begins.")
    addresses_ids = fields.Many2many(
        comodel_name="hc.vs.condition.code",
        relation="plan_definition_goal_definition_addresses_rel",
        string="Addresses",
        help="What does the goal address.")
    documentation_ids = fields.One2many(
        comodel_name="hc.plan.definition.goal.definition.documentation",
        inverse_name="goal_definition_id",
        string="Documentations",
        help="Supporting documentation for the goal.")
    target_ids = fields.One2many(
        comodel_name="hc.plan.definition.goal.definition.target",
        inverse_name="goal_definition_id",
        string="Targets",
        help="Target outcome for the goal.")

class PlanDefinitionGoalDefinitionTarget(models.Model):
    _name = "hc.plan.definition.goal.definition.target"
    _description = "Plan Definition Goal Definition Target"

    goal_definition_id = fields.Many2one(
        comodel_name="hc.plan.definition.goal.definition",
        string="Goal Definition",
        help="What the plan is trying to accomplish.")
    measure_id = fields.Many2one(
        comodel_name="hc.vs.observation.code",
        string="Measure",
        help="The parameter whose value is to be tracked.")
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
        help="Quantity the target value to be achieved.")
    detail_quantity_uom_id = fields.Many2one(
        comodel_name="product.uom",
        string="Detail Quantity UOM",
        help="Detail Quantity unit of measure.")
    detail_range_low = fields.Float(
        string="Detail Range Low",
        help="Low limit of the target value to be achieved.")
    detail_range_high = fields.Float(
        string="Detail Range High",
        help="High limit of the target value to be achieved.")
    detail_range_uom_id = fields.Many2one(
        comodel_name="product.uom",
        string="Detail Range UOM",
        help="Detail Range unit of measure.")
    detail_code_id = fields.Many2one(
        comodel_name="hc.vs.goal.definition.target",
        string="Detail Code",
        help="Code of the target value to be achieved.")
    due = fields.Float(
        string="Due",
        help="Indicates the timeframe after the start of the goal in which the goal should be met.")
    due_uom_id = fields.Many2one(
        comodel_name="product.uom",
        string="UOM",
        domain="[('category_id','=','Time (UCUM)')]",
        help="Due unit of measure.")

class PlanDefinitionActionDefinition(models.Model):
    _name = "hc.plan.definition.action.definition"
    _description = "Plan Definition Action Definition"

    plan_definition_id = fields.Many2one(
        comodel_name="hc.res.plan.definition",
        string="Plan Definition",
        help="Action defined by the plan.")
    action_identifier_id = fields.Many2one(
        comodel_name="hc.plan.definition.action.definition.action.identifier",
        string="Action Identifier",
        help="Unique identifier.")
    label = fields.Char(
        string="Label",
        help="User-visible label for the action (e.g. 1. or A.).")
    title = fields.Char(
        string="Title",
        help="User-visible title.")
    description = fields.Text(
        string="Description",
        help="Short description of the action.")
    text_equivalent = fields.Text(
        string="Text Equivalent",
        help="Static text equivalent of the action, used if the dynamic aspects cannot be interpreted by the receiving system.")
    code_ids = fields.Many2many(
        comodel_name="hc.vs.action.code",
        relation="plan_definition_action_definition_code_rel",
        string="Codes",
        help="The meaning of the action or its sub-actions.")
    reason_ids = fields.Many2many(
        comodel_name="hc.vs.action.code",
        relation="plan_definition_action_definition_reason_rel",
        string="Reasons",
        help="Why the action should be performed.")
    documentation_ids = fields.One2many(
        comodel_name="hc.plan.definition.action.definition.documentation",
        inverse_name="action_definition_id",
        string="Documentation",
        help="Supporting documentation for the intended performer of the action.")
    goal_id_ids = fields.One2many(
        comodel_name="hc.plan.definition.action.definition.goal.id",
        inverse_name="action_definition_id",
        string="Goal Ids",
        help="What goals this action supports.")
    trigger_definition_ids = fields.One2many(
        comodel_name="hc.plan.definition.action.definition.trigger.definition",
        inverse_name="action_definition_id",
        string="Trigger Definitions",
        help="When the action should be triggered.")
    input_ids = fields.One2many(
        comodel_name="hc.plan.definition.action.definition.input",
        inverse_name="action_definition_id",
        string="Inputs",
        help="Input data requirements.")
    output_ids = fields.One2many(
        comodel_name="hc.plan.definition.action.definition.output",
        inverse_name="action_definition_id",
        string="Outputs",
        help="Output data definition.")
    timing_type = fields.Selection(
        string="Timing Type",
        selection=[
            ("date_time", "Date Time"),
            ("period", "Period"),
            ("duration", "Duration"),
            ("range", "Range"),
            ("timing", "Timing")],
        help="Type of when the action should take place.")
    timing_name = fields.Char(
        string="Timing",
        compute="_compute_timing_name",
        store="True",
        help="When the action should take place.")
    timing_date_time = fields.Datetime(
        string="Timing Date Time",
        help="When the action should take place.")
    timing_start_date = fields.Datetime(
        string="Timing Start Date",
        help="Start of when the action should take place.")
    timing_end_date = fields.Datetime(
        string="Timing End Date",
        help="End of when the action should take place.")
    timing_duration = fields.Float(
        string="Timing Duration",
        help="Duration when the action should take place.")
    timing_duration_uom_id = fields.Many2one(
        comodel_name="product.uom",
        string="Timing Duration UOM",
        domain="[('category_id','=','Time (UCUM)')]",
        help="Timing Duration unit of measure.")
    timing_range_low = fields.Float(
        string="Timing Range Low",
        help="Low limit of when the action should take place.")
    timing_range_high = fields.Float(
        string="Timing Range High",
        help="High limit of when the action should take place.")
    timing_range_uom_id = fields.Many2one(
        comodel_name="product.uom",
        string="Timing Range UOM",
        help="Timing Range unit of measure.")
    timing_id = fields.Many2one(
        comodel_name="hc.plan.definition.action.definition.timing",
        string="Timing",
        help="When the action should take place.")
    type = fields.Selection(
        string="Type",
        selection=[
            ("create", "Create"),
            ("update", "Update"),
            ("remove", "Remove"),
            ("fire-event", "Fire Event")],
        help="The type of action to perform (create, update, remove).")
    grouping_behavior = fields.Selection(
        string="Grouping Behavior",
        selection=[
            ("visual-group", "Visual Group"),
            ("logical-group", "Logical Group"),
            ("sentence-group", "Sentence Group")],
        help="Defines the grouping behavior for the action and its children.")
    selection_behavior = fields.Selection(
        string="Selection Behavior",
        selection=[
            ("any", "Any"),
            ("all", "All"),
            ("all-or-none", "All Or None"),
            ("exactly-one", "Exactly One"),
            ("at-most-one", "At Most One"),
            ("one-or-more", "One Or More")],
        help="Defines the selection behavior for the action and its children.")
    required_behavior = fields.Selection(
        string="Required Behavior",
        selection=[
            ("must", "Must"),
            ("could", "Could"),
            ("must-unless-documented", "Must Unless Documented")],
        help="Defines the requiredness behavior for the action.")
    precheck_behavior = fields.Selection(
        string="Precheck Behavior",
        selection=[
            ("yes", "Yes"),
            ("no", "No")],
        help="Defines whether the action should usually be preselected.")
    cardinality_behavior = fields.Selection(
        string="Cardinality Behavior",
        selection=[
            ("single", "Single"),
            ("multiple", "Multiple")],
        help="Defines whether the action can be selected multiple times.")
    definition_type = fields.Selection(
        string="Definition Type",
        selection=[
            ("activity_definition", "Activity Definition"),
            ("plan_definition", "Plan Definition")],
        help="Type of time offset for the relationship.")
    definition_name = fields.Char(
        string="Definition",
        compute="_compute_definition_name",
        store="True",
        help="Description of the activity to be performed.")
    definition_activity_definition_id = fields.Many2one(
        comodel_name="hc.res.activity.definition",
        string="Definition Activity Definition",
        help="Activity Definition description of the activity to be performed.")
    definition_plan_definition_id = fields.Many2one(
        comodel_name="hc.res.plan.definition",
        string="Definition Plan Definition",
        help="Plan Definition description of the activity to be performed.")
    transform_id = fields.Many2one(
        comodel_name="hc.res.structure.map",
        string="Transform",
        help="Transform to apply the template.")
    action_definition_id = fields.Many2one(
        comodel_name="hc.plan.definition.action.definition",
        string="Action Definition",
        help="A sub-action.")
    condition_ids = fields.One2many(
        comodel_name="hc.plan.definition.action.definition.condition",
        inverse_name="action_definition_id",
        string="Conditions",
        help="Whether or not the action is applicable.")
    related_action_ids = fields.One2many(
        comodel_name="hc.plan.definition.action.definition.related.action",
        inverse_name="action_definition_id",
        string="Related Actions",
        help="Relationship to another action.")
    participant_ids = fields.One2many(
        comodel_name="hc.plan.definition.action.definition.participant",
        inverse_name="action_definition_id",
        string="Participants",
        help="Who should participate in the action.")
    dynamic_value_ids = fields.One2many(
        comodel_name="hc.plan.definition.action.definition.dynamic.value",
        inverse_name="action_definition_id",
        string="Dynamic Values",
        help="Dynamic aspects of the definition.")

class PlanDefinitionActionDefinitionCondition(models.Model):
    _name = "hc.plan.definition.action.definition.condition"
    _description = "Plan Definition Action Definition Condition"

    action_definition_id = fields.Many2one(
        comodel_name="hc.plan.definition.action.definition",
        string="Action Definition",
        help="Action defined by the plan.")
    kind = fields.Selection(
        string="Kind",
        required="True",
        selection=[
            ("applicability", "Applicability"),
            ("start", "Start"),
            ("stop", "Stop")],
        help="The kind of condition.")
    description = fields.Text(
        string="Description",
        help="Natural language description of the condition.")
    language = fields.Char(
        string="Language",
        help="Language of the expression.")
    expression = fields.Text(
        string="Expression",
        help="Boolean-valued expression.")

class PlanDefinitionActionDefinitionRelatedAction(models.Model):
    _name = "hc.plan.definition.action.definition.related.action"
    _description = "Plan Definition Action Definition Related Action"

    action_definition_id = fields.Many2one(
        comodel_name="hc.plan.definition.action.definition",
        string="Action Definition",
        help="Action defined by the plan.")
    action_identifier_id = fields.Many2one(
        comodel_name="hc.plan.defn.action.defn.related.action.action.identifier",
        string="Action Identifier",
        required="True",
        help="Identifier of the related action.")
    relationship = fields.Selection(
        string="Relationship",
        required="True",
        selection=[
            ("before-start", "Before Start"),
            ("before", "Before"),
            ("before-end", "Before End"),
            ("concurrent-with-start", "Concurrent With Start"),
            ("concurrent", "Concurrent"),
            ("concurrent-with-end", "Concurrent With End"),
            ("after-start", "After-Start"),
            ("after", "After"),
            ("after-end", "After End")],
        help="The relationship of this action to the related action.")
    offset_type = fields.Selection(
        string="Offset Type",
        selection=[
            ("duration", "Duration"),
            ("range", "Range")],
        help="Type of time offset for the relationship.")
    offset_name = fields.Char(
        string="Offset",
        compute="_compute_offset_name",
        store="True",
        help="Time offset for the relationship.")
    offset_duration = fields.Float(
        string="Offset Duration",
        help="Duration time offset for the relationship.")
    offset_duration_uom_id = fields.Many2one(
        comodel_name="product.uom",
        string="Offset Duration UOM",
        domain="[('category_id','=','Time (UCUM)')]",
        help="Offset Duration unit of measure.")
    offset_range_low = fields.Float(
        string="Offset Range Low",
        help="Low limit of time offset for the relationship.")
    offset_range_high = fields.Float(
        string="Offset Range High",
        help="High limit of time offset for the relationship.")
    offset_range_uom_id = fields.Many2one(
        comodel_name="product.uom",
        string="Offset Range UOM",
        help="Offset Range unit of measure.")

class PlanDefinitionActionDefinitionParticipant(models.Model):
    _name = "hc.plan.definition.action.definition.participant"
    _description = "Plan Definition Action Definition Participant"

    action_definition_id = fields.Many2one(
        comodel_name="hc.plan.definition.action.definition",
        string="Action Definition",
        help="Action defined by the plan.")
    type = fields.Selection(
        string="Participant Type",
        required="True",
        selection=[
            ("patient", "Patient"),
            ("practitioner", "Practitioner"),
            ("related-person", "Related Person")],
        help="The type of participant in the action.")
    role_id = fields.Many2one(
        comodel_name="hc.vs.action.participant.role",
        string="Role",
        help="E.g. Nurse, Surgeon, Parent, etc.")

class PlanDefinitionActionDefinitionDynamicValue(models.Model):
    _name = "hc.plan.definition.action.definition.dynamic.value"
    _description = "Plan Definition Action Definition Dynamic Value"

    action_definition_id = fields.Many2one(
        comodel_name="hc.plan.definition.action.definition",
        string="Action Definition",
        help="Action defined by the plan.")
    description = fields.Text(
        string="Description",
        help="Natural language description of the dynamic value.")
    path = fields.Char(
        string="Path",
        help="The path to the element to be set dynamically.")
    language = fields.Char(
        string="Language",
        help="Language of the expression.")
    expression = fields.Text(
        string="Expression",
        help="An expression that provides the dynamic value for the customization.")

class PlanDefinitionIdentifier(models.Model):
    _name = "hc.plan.definition.identifier"
    _description = "Plan Definition Identifier"
    _inherit = ["hc.basic.association", "hc.identifier"]

    plan_definition_id = fields.Many2one(
        comodel_name="hc.res.plan.definition",
        string="Plan Definition",
        help="Plan Definition associated with this Plan Definition Identifier.")

class PlanDefinitionUseContext(models.Model):
    _name = "hc.plan.definition.use.context"
    _description = "Plan Definition Use Context"
    _inherit = ["hc.basic.association", "hc.usage.context"]

    plan_definition_id = fields.Many2one(
        comodel_name="hc.res.plan.definition",
        string="Plan Definition",
        help="Plan Definition associated with this Plan Definition Use Context.")

class PlanDefinitionContributor(models.Model):
    _name = "hc.plan.definition.contributor"
    _description = "Plan Definition Contributor"
    _inherit = ["hc.basic.association"]
    _inherits = {"hc.contributor": "contributor_id"}

    contributor_id = fields.Many2one(
        comodel_name="hc.contributor",
        string="Contributor",
        ondelete="restrict",
        required="True",
        help="Contributor associated with this Plan Definition Contributor.")
    plan_definition_id = fields.Many2one(
        comodel_name="hc.res.plan.definition",
        string="Plan Definition",
        help="Plan Definition associated with this Plan Definition Contributor.")

class PlanDefinitionContact(models.Model):
    _name = "hc.plan.definition.contact"
    _description = "Plan Definition Contact"
    _inherit = ["hc.basic.association"]
    _inherits = {"hc.contact.detail": "contact_id"}

    contact_id = fields.Many2one(
        comodel_name="hc.contact.detail",
        string="Contact",
        ondelete="restrict",
        required="True",
        help="Contact Detail associated with this Plan Definition Contact.")
    plan_definition_id = fields.Many2one(
        comodel_name="hc.res.plan.definition",
        string="Plan Definition",
        help="Plan Definition associated with this Plan Definition Contact.")

class PlanDefinitionRelatedArtifact(models.Model):
    _name = "hc.plan.definition.related.artifact"
    _description = "Plan Definition Related Artifact"
    _inherit = ["hc.basic.association", "hc.related.artifact"]

    plan_definition_id = fields.Many2one(
        comodel_name="hc.res.plan.definition",
        string="Plan Definition",
        help="Plan Definition associated with this Plan Definition Related Artifact.")

class PlanDefinitionLibrary(models.Model):
    _name = "hc.plan.definition.library"
    _description = "Plan Definition Library"
    _inherit = ["hc.basic.association"]

    plan_definition_id = fields.Many2one(
        comodel_name="hc.res.plan.definition",
        string="Plan Definition",
        help="Plan Definition associated with this Plan Definition Library.")
    library_id = fields.Many2one(
        comodel_name="hc.res.library",
        string="Library",
        help="Library associated with this Plan Definition Library.")

class PlanDefinitionActionDefinitionActionIdentifier(models.Model):
    _name = "hc.plan.definition.action.definition.action.identifier"
    _description = "Plan Definition Action Definition Action Identifier"
    _inherit = ["hc.basic.association", "hc.identifier"]

class PlanDefinitionGoalDefinitionDocumentation(models.Model):
    _name = "hc.plan.definition.goal.definition.documentation"
    _description = "Plan Definition Goal Definition Documentation"
    _inherit = ["hc.basic.association", "hc.related.artifact"]

    goal_definition_id = fields.Many2one(
        comodel_name="hc.plan.definition.goal.definition",
        string="Goal Definition",
        help="Goal Definition associated with this Plan Definition Goal Definition Documentation.")

class PlanDefinitionActionDefinitionDocumentation(models.Model):
    _name = "hc.plan.definition.action.definition.documentation"
    _description = "Plan Definition Action Definition Documentation"
    _inherit = ["hc.basic.association", "hc.related.artifact"]

    action_definition_id = fields.Many2one(
        comodel_name="hc.plan.definition.action.definition",
        string="Action Definition",
        help="Action Definition associated with this Plan Definition Action Definition Documentation.")

class PlanDefinitionActionDefinitionGoalId(models.Model):
    _name = "hc.plan.definition.action.definition.goal.id"
    _description = "Plan Definition Action Definition Goal Id"
    _inherit = ["hc.basic.association"]

    action_definition_id = fields.Many2one(
        comodel_name="hc.plan.definition.action.definition",
        string="Action Definition",
        help="Action Definition associated with this Plan Definition Action Definition Goal Id.")
    goal_id = fields.Text(
        string="Goal Id",
        help="Goal Id associated with this Plan Definition Action Definition Goal Id.")

class PlanDefinitionActionDefinitionTriggerDefinition(models.Model):
    _name = "hc.plan.definition.action.definition.trigger.definition"
    _description = "Plan Definition Action Definition Trigger Definition"
    _inherit = ["hc.basic.association", "hc.trigger.definition"]

    action_definition_id = fields.Many2one(
        comodel_name="hc.plan.definition.action.definition",
        string="Action Definition",
        help="Action Definition associated with this Plan Definition Action Definition Trigger Definition.")

class PlanDefinitionActionDefinitionInput(models.Model):
    _name = "hc.plan.definition.action.definition.input"
    _description = "Plan Definition Action Definition Input"
    _inherit = ["hc.basic.association", "hc.data.requirement"]

    action_definition_id = fields.Many2one(
        comodel_name="hc.plan.definition.action.definition",
        string="Action Definition",
        help="Action Definition associated with this Plan Definition Action Definition Input.")

class PlanDefinitionActionDefinitionOutput(models.Model):
    _name = "hc.plan.definition.action.definition.output"
    _description = "Plan Definition Action Definition Output"
    _inherit = ["hc.basic.association", "hc.data.requirement"]

    action_definition_id = fields.Many2one(
        comodel_name="hc.plan.definition.action.definition",
        string="Action Definition",
        help="Action Definition associated with this Plan Definition Action Definition Output.")

class PlanDefinitionActionDefinitionTiming(models.Model):
    _name = "hc.plan.definition.action.definition.timing"
    _description = "Plan Definition Action Definition Timing"
    _inherit = ["hc.basic.association", "hc.timing"]

class PlanDefnActionDefnRelatedActionActionIdentifier(models.Model):
    _name = "hc.plan.defn.action.defn.related.action.action.identifier"
    _description = "Plan Definition Action Definition Related Action Action Identifier"
    _inherit = ["hc.basic.association", "hc.identifier"]

class GoalDefinitionTarget(models.Model):
    _name = "hc.vs.goal.definition.target"
    _description = "Goal Definition Target"
    _inherit = ["hc.value.set.contains"]

    name = fields.Char(
        string="Name",
        help="Name of this goal definition target.")
    code = fields.Char(
        string="Code",
        help="Code of this goal definition target.")
    contains_id = fields.Many2one(
        comodel_name="hc.vs.goal.definition.target",
        string="Parent",
        help="Parent goal definition target.")
