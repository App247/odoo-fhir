# -*- coding: utf-8 -*-

from openerp import models, fields, api

class ExampleScenario(models.Model):
    _name = "hc.res.example.scenario"
    _description = "Example Scenario"
    _inherit = ["hc.domain.resource"]
    _rec_name = "name"

    url = fields.Char(
        string="URI",
        help="Logical URI to reference this example scenario (globally unique).")
    identifier_ids = fields.One2many(
        comodel_name="hc.example.scenario.identifier",
        inverse_name="example_scenario_id",
        string="Identifiers",
        help="Additional identifier for the example scenario.")
    version = fields.Char(
        string="Version",
        help="Business version of the example scenario.")
    name = fields.Char(
        string="Name",
        help="Name for this example scenario (computer friendly).")
    title = fields.Char(
        string="Title",
        help="Name of example.")
    status = fields.Selection(
        string="Example Scenario Status",
        required="True",
        selection=[
            ("draft", "Draft"),
            ("active", "Active"),
            ("retired", "Retired"),
            ("unknown", "Unknown")],
        help="The status of this example scenario. Enables tracking the life-cycle of the content")
    is_experimental = fields.Boolean(
        string="Experimental",
        help="For testing purposes, not real usage.")
    date = fields.Datetime(
        string="Date",
        help="Date this was last changed.")
    publisher = fields.Char(
        string="Publisher",
        help="Name of the publisher (organization or individual).")
    contact_ids = fields.One2many(
        comodel_name="hc.example.scenario.contact",
        inverse_name="example_scenario_id",
        string="Contacts",
        help="Contact details for the publisher.")
    use_context_ids = fields.One2many(
        comodel_name="hc.example.scenario.use.context",
        inverse_name="example_scenario_id",
        string="Use Contexts",
        help="Context the content is intended to support.")
    body_site_ids = fields.Many2many(
        comodel_name="hc.vs.jurisdiction",
        relation="example_scenario_body_site_rel",
        string="Body Sites",
        help="Intended jurisdiction for example scenario (if applicable).")
    copyright = fields.Text(
        string="Copyright",
        help="Use and/or publishing restrictions.")
    description = fields.Text(
        string="Description",
        help="Description of behaviour of the workflow example.")
    purpose = fields.Text(
        string="Purpose",
        help="What is the example supposed to resolve.")
    actor_ids = fields.One2many(
        comodel_name="hc.example.scenario.actor",
        inverse_name="example_scenario_id",
        string="Actors",
        help="Actor participating in the resource.")
    instance_ids = fields.One2many(
        comodel_name="hc.example.scenario.instance",
        inverse_name="example_scenario_id",
        string="Instances",
        help="Each resource and each version that is present in the workflow.")
    process_ids = fields.One2many(
        comodel_name="hc.example.scenario.process",
        inverse_name="example_scenario_id",
        string="Processs",
        help="Each major process - a group of operations.")
    workflow_ids = fields.One2many(
        comodel_name="hc.res.example.scenario",
        inverse_name="example_scenario_id",
        string="Workflows",
        help="Another nested workflow.")
    example_scenario_id = fields.Many2one(
        comodel_name="hc.res.example.scenario",
        string="Example Scenario",
        help="Example Scenario associated with this Example Scenario Workflow.")

class ExampleScenarioActor(models.Model):
    _name = "hc.example.scenario.actor"
    _description = "Example Scenario Actor"
    _inherit = ["hc.backbone.element"]

    example_scenario_id = fields.Many2one(
        comodel_name="hc.res.example.scenario",
        string="Example Scenario",
        help="Example Scenario associated with this Example Scenario Actor.")
    actor_id = fields.Char(
        string="Actor Id",
        required="True",
        help="ID or acronym of the actor.")
    type = fields.Selection(
        string="Type",
        required="True",
        selection=[
            ("person", "Person"),
            ("entity", "Entity")],
        help="The type of actor - person or system.")
    name = fields.Char(
        string="Name",
        help="The name of the actor as shown in the page.")
    description = fields.Text(
        string="Description",
        help="The description of the actor.")

class ExampleScenarioInstance(models.Model):
    _name = "hc.example.scenario.instance"
    _description = "Example Scenario Instance"
    _inherit = ["hc.backbone.element"]

    example_scenario_id = fields.Many2one(
        comodel_name="hc.res.example.scenario",
        string="Example Scenario",
        help="Example Scenario associated with this Example Scenario Instance.")
    resource_id = fields.Char(
        string="Resource Id",
        required="True",
        help="The id of the resource for referencing.")
    resource_type_id = fields.Many2one(
        comodel_name="hc.vs.resource.type",
        string="Resource Type",
        required="True",
        help="The type of the resource.")
    name = fields.Char(
        string="Name",
        help="A short name for the resource instance.")
    description = fields.Text(
        string="Description",
        help="Human-friendly description of the resource instance.")
    version_ids = fields.One2many(
        comodel_name="hc.example.scenario.instance.version",
        inverse_name="instance_id",
        string="Versions",
        help="A specific version of the resource.")
    contained_instance_ids = fields.One2many(
        comodel_name="hc.example.scenario.instance.contained.instance",
        inverse_name="instance_id",
        string="Contained Instances",
        help="Resources contained in the instance.")

class ExampleScenarioInstanceVersion(models.Model):
    _name = "hc.example.scenario.instance.version"
    _description = "Example Scenario Instance Version"
    _inherit = ["hc.backbone.element"]

    instance_id = fields.Many2one(
        comodel_name="hc.example.scenario.instance",
        string="Instance",
        help="Instance associated with this Example Scenario Instance Version.")
    version_id = fields.Char(
        string="Version Id",
        required="True",
        help="The identifier of a specific version of a resource.")
    description = fields.Text(
        string="Description",
        required="True",
        help="The description of the resource version.")

class ExampleScenarioInstanceContainedInstance(models.Model):
    _name = "hc.example.scenario.instance.contained.instance"
    _description = "Example Scenario Instance Contained Instance"
    _inherit = ["hc.backbone.element"]

    instance_id = fields.Many2one(
        comodel_name="hc.example.scenario.instance",
        string="Instance",
        help="Instance associated with this Example Scenario Instance Version.")
    resource_id = fields.Char(
        string="Resource Id",
        required="True",
        help="Each resource contained in the instance.")
    version_id = fields.Char(
        string="Version Id",
        help="A specific version of a resource contained in the instance.")
    request_id = fields.Many2one(
        comodel_name="hc.example.scenario.process.step.operation",
        string="Request",
        help="Request associated with this Example Scenario Instance Version.")
    response_id = fields.Many2one(
        comodel_name="hc.example.scenario.process.step.operation",
        string="Response",
        help="Response associated with this Example Scenario Instance Version.")

class ExampleScenarioProcess(models.Model):
    _name = "hc.example.scenario.process"
    _description = "Example Scenario Process"
    _inherit = ["hc.backbone.element"]

    example_scenario_id = fields.Many2one(
        comodel_name="hc.res.example.scenario",
        string="Example Scenario",
        help="Example Scenario associated with this Example Scenario Process.")
    title = fields.Char(
        string="Title",
        required="True",
        help="The diagram title of the group of operations.")
    description = fields.Text(
        string="Description",
        help="A longer description of the group of operations.")
    pre_conditions = fields.Text(
        string="Pre Conditions",
        help="Description of initial status before the process starts.")
    post_conditions = fields.Text(
        string="Post Conditions",
        help="Description of final status after the process ends.")
    step_ids = fields.One2many(
        comodel_name="hc.example.scenario.process.step",
        inverse_name="process_id",
        string="Steps",
        help="Each step of the process.")
    step_id = fields.Many2one(
        comodel_name="hc.example.scenario.process.step",
        string="Step",
        help="Step associated with this Example Scenario Process.")

class ExampleScenarioProcessStep(models.Model):
    _name = "hc.example.scenario.process.step"
    _description = "Example Scenario Process Step"
    _inherit = ["hc.backbone.element"]

    process_id = fields.Many2one(
        comodel_name="hc.example.scenario.process",
        string="Process",
        help="Process associated with this Example Scenario Process Step.")
    process_ids = fields.One2many(
        comodel_name="hc.example.scenario.process",
        inverse_name="step_id",
        string="Processes",
        help="Content as for ExampleScenario.process Nested process.")
    is_pause = fields.Boolean(
        string="Pause",
        help="If there is a pause in the flow.")
    operation_id = fields.Many2one(
        comodel_name="hc.example.scenario.process.step.operation",
        string="Operation",
        help="Each interaction or action.")
    alternative_id = fields.Many2one(
        comodel_name="hc.example.scenario.process.step.alternative",
        string="Alternative",
        help="Each interaction in the process.")
    option_id = fields.Many2one(
        comodel_name="hc.example.scenario.process.step.alternative.option",
        string="Option",
        help="Option associated with this Example Scenario Process Step.")

class ExampleScenarioProcessStepOperation(models.Model):
    _name = "hc.example.scenario.process.step.operation"
    _description = "Example Scenario Process Step Operation"
    _inherit = ["hc.backbone.element"]

    step_id = fields.Many2one(
        comodel_name="hc.example.scenario.process.step",
        string="Step",
        help="Each step of the process.")
    number = fields.Char(
        string="Number",
        required="True",
        help="The sequential number of the interaction.")
    type = fields.Char(
        string="Type",
        help="The type of operation - CRUD.")
    name = fields.Char(
        string="Name",
        help="The human-friendly name of the interaction.")
    initiator = fields.Char(
        string="Initiator",
        help="Who starts the transaction.")
    receiver = fields.Char(
        string="Receiver",
        help="Who receives the transaction.")
    description = fields.Text(
        string="Description",
        help="A comment to be inserted in the diagram.")
    is_initiator_active = fields.Boolean(
        string="Initiator Active",
        help="Whether the initiator is deactivated right after the transaction.")
    is_receiver_active = fields.Boolean(
        string="Receiver Active",
        help="Whether the receiver is deactivated right after the transaction.")
    request_id = fields.Many2one(
        comodel_name="hc.example.scenario.instance.contained.instance",
        string="Request",
        help="Request associated with this Example Scenario Process Step Operation.")
    response_id = fields.Many2one(
        comodel_name="hc.example.scenario.instance.contained.instance",
        string="Response",
        help="Response associated with this Example Scenario Process Step Operation.")

class ExampleScenarioProcessStepAlternative(models.Model):
    _name = "hc.example.scenario.process.step.alternative"
    _description = "Example Scenario Process Step Alternative"
    _inherit = ["hc.backbone.element"]

    step_id = fields.Many2one(
        comodel_name="hc.example.scenario.process.step",
        string="Step",
        help="Each step of the process.")
    name = fields.Char(
        string="Name",
        help="The name of each alternative.")
    option_ids = fields.One2many(
        comodel_name="hc.example.scenario.process.step.alternative.option",
        inverse_name="alternative_id",
        string="Options",
        required="True",
        help="Each of the possible options in an alternative.")

class ExampleScenarioProcessStepAlternativeOption(models.Model):
    _name = "hc.example.scenario.process.step.alternative.option"
    _description = "Example Scenario Process Step Alternative Option"
    _inherit = ["hc.backbone.element"]

    alternative_id = fields.Many2one(comodel_name="hc.example.scenario.process.step.alternative", string="Alternative", help="Alternative associated with this Example Scenario Process Step Alternative Option.")
    description = fields.Text(string="Description", required="True", help="A human-readable description of each option.")
    step_ids = fields.One2many(comodel_name="hc.example.scenario.process.step", inverse_name="option_id", string="Steps", help="Content as for ExampleScenario.process.step What happens in each alternative option.")
    pause_ids = fields.One2many(comodel_name="hc.example.scenario.process.step.alternative.option.pause", inverse_name="option_id", string="Pause", help="If there is a pause in the flow.")

class ExampleScenarioIdentifier(models.Model):
    _name = "hc.example.scenario.identifier"
    _description = "Example Scenario Identifier"
    _inherit = ["hc.basic.association", "hc.identifier"]

    example_scenario_id = fields.Many2one(
        comodel_name="hc.res.example.scenario",
        string="Example Scenario",
        help="Example Scenario associated with this Example Scenario Identifier.")

class ExampleScenarioContact(models.Model):
    _name = "hc.example.scenario.contact"
    _description = "Example Scenario Contact"
    _inherit = ["hc.basic.association"]
    _inherits = {"hc.contact.detail": "contact_id"}

    contact_id = fields.Many2one(
        comodel_name="hc.contact.detail",
        string="Contact",
        ondelete="restrict",
        required="True",
        help="Contact Detail associated with this Example Scenario Contact.")
    example_scenario_id = fields.Many2one(
        comodel_name="hc.res.example.scenario",
        string="Example Scenario",
        help="Example Scenario associated with this Example Scenario Contact.")

class ExampleScenarioUseContext(models.Model):
    _name = "hc.example.scenario.use.context"
    _description = "Example Scenario Use Context"
    _inherit = ["hc.basic.association", "hc.usage.context"]

    example_scenario_id = fields.Many2one(
        comodel_name="hc.res.example.scenario",
        string="Example Scenario",
        help="Example Scenario associated with this Example Scenario Use Context.")

class ExampleScenarioProcessStepAlternativeOptionPause(models.Model):
    _name = "hc.example.scenario.process.step.alternative.option.pause"
    _description = "Example Scenario Process Step Alternative Option Pause"
    _inherit = ["hc.basic.association"]

    option_id = fields.Many2one(
        comodel_name="hc.example.scenario.process.step.alternative.option",
        string="Option",
        help="Option associated with this Example Scenario Process Step Alternative Option Pause.")
    is_pause = fields.Boolean(
        string="Pause",
        help="If there is a pause in the flow.")
