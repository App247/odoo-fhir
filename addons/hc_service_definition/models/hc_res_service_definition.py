# -*- coding: utf-8 -*-

from openerp import models, fields, api

class ServiceDefinition(models.Model):
    _name = "hc.res.service.definition"
    _description = "Service Definition"

    url = fields.Char(
        string="URI",
        help="Logical uri to reference this service definition (globally unique).")
    identifier_ids = fields.One2many(
        comodel_name="hc.service.definition.identifier",
        inverse_name="service_definition_id",
        string="Identifiers",
        help="Additional identifier for the service definition." )
    version = fields.Char(
        string="Version",
        help="Business version of the service definition.")
    name = fields.Char(
        string="Name",
        help="Name for this service definition (Computer friendly).")
    title = fields.Char(
        string="Title",
        help="Name for this service definition (Human friendly).")
    status = fields.Selection(
        string="Status",
        required="True",
        selection=[
            ("draft", "Draft"),
            ("active", "Active"),
            ("retired", "Retired")],
        help="The status of this service definition. Enables tracking the life-cycle of the content.")
    is_experimental = fields.Boolean(
        string="Experimental",
        help="If for testing purposes, not real usage.")
    date = fields.Datetime(
        string="Date",
        help="Date this was last changed.")
    description = fields.Text(
        string="Description",
        help="Natural language description of the service definition.")
    purpose = fields.Text(
        string="Purpose",
        help="Why this service definition is defined.")
    usage = fields.Text(
        string="Usage",
        help="Describes the clinical usage of the module.")
    approval_date = fields.Date(
        string="Approval Date",
        help="When service definition approved by publisher.")
    last_review_date = fields.Date(
        string="Last Review Date",
        help="Last review date for the service definition.")
    effective_period_start_date = fields.Datetime(
        string="Effective Period Start Date",
        help="Start of the effective date range for the service definition.")
    effective_period_end_date = fields.Datetime(
        string="Effective Period End Date",
        help="End of the effective date range for the service definition.")
    use_context_ids = fields.One2many(
        comodel_name="hc.service.definition.use.context",
        inverse_name="service_definition_id",
        string="Use Contexts",
        help="Content intends to support these contexts.")
    jurisdiction_ids = fields.Many2many(
        comodel_name="hc.vs.jurisdiction",
        relation="service_definition_jurisdiction_rel",
        string="Jurisdictions",
        help="Intended jurisdiction for service definition (if applicable).")
    topic_ids = fields.Many2many(
        comodel_name="hc.vs.definition.topic",
        relation="service_definition_topic_rel",
        string="Topics",
        help="Descriptional topics for the module.")
    contributor_ids = fields.One2many(
        comodel_name="hc.service.definition.contributor",
        inverse_name="service_definition_id",
        string="Contributors",
        help="A content contributor.")
    publisher = fields.Char(
        string="Publisher",
        help="Name of the publisher (Organization or individual).")
    contact_ids = fields.One2many(
        comodel_name="hc.service.definition.contact",
        inverse_name="service_definition_id",
        string="Contacts",
        help="Contact details for the publisher.")
    copyright = fields.Char(
        string="Copyright",
        help="Use and/or publishing restrictions.")
    related_artifact_ids = fields.One2many(
        comodel_name="hc.service.definition.related.artifact",
        inverse_name="service_definition_id",
        string="Related Artifacts",
        help="Related resources for the module.")
    trigger_ids = fields.One2many(
        comodel_name="hc.service.definition.trigger",
        inverse_name="service_definition_id",
        string="Triggers",
        help='"When" the module should be invoked.' )
    data_requirement_ids = fields.One2many(
        comodel_name="hc.service.definition.data.requirement",
        inverse_name="service_definition_id",
        string="Data Requirements",
        help="Data requirements for the module." )
    operation_definition_id = fields.Many2one(
        comodel_name="hc.res.operation.definition",
        string="Operation Definition",
        help="Operation to invoke.")

class ServiceDefinitionIdentifier(models.Model):
    _name = "hc.service.definition.identifier"
    _description = "Service Definition Identifier"
    _inherit = ["hc.basic.association", "hc.identifier"]

    service_definition_id = fields.Many2one(
        comodel_name="hc.res.service.definition",
        string="Service Definition",
        help="Service Definition associated with this Service Definition Identifier.")

class ServiceDefinitionUseContext(models.Model):
    _name = "hc.service.definition.use.context"
    _description = "Service Definition Use Context"
    _inherit = ["hc.basic.association", "hc.usage.context"]

    service_definition_id = fields.Many2one(
        comodel_name="hc.res.service.definition",
        string="Service Definition",
        help="Service Definition associated with this Service Definition Use Context.")

class ServiceDefinitionContributor(models.Model):
    _name = "hc.service.definition.contributor"
    _description = "Service Definition Contributor"
    _inherit = ["hc.basic.association"]
    _inherits = {"hc.contributor": "contributor_id"}

    contributor_id = fields.Many2one(
        comodel_name="hc.contributor",
        string="Contributor",
        ondelete="restrict",
        required="True",
        help="Contributor associated with this Service Definition Contributor.")
    service_definition_id = fields.Many2one(
        comodel_name="hc.res.service.definition",
        string="Service Definition",
        help="Service Definition associated with this Service Definition Contributor.")

class ServiceDefinitionContact(models.Model):
    _name = "hc.service.definition.contact"
    _description = "Service Definition Contact"
    _inherit = ["hc.basic.association"]
    _inherits = {"hc.contact.detail": "contact_id"}

    contact_id = fields.Many2one(
        comodel_name="hc.contact.detail",
        string="Contact",
        ondelete="restrict",
        required="True",
        help="Contact Detail associated with this Service Definition Contact.")
    service_definition_id = fields.Many2one(
        comodel_name="hc.res.service.definition",
        string="Service Definition",
        help="Service Definition associated with this Service Definition Contact.")

class ServiceDefinitionRelatedArtifact(models.Model):
    _name = "hc.service.definition.related.artifact"
    _description = "Service Definition Related Artifact"
    _inherit = ["hc.basic.association", "hc.related.artifact"]

    service_definition_id = fields.Many2one(
        comodel_name="hc.res.service.definition",
        string="Service Definition",
        help="Service Definition associated with this Service Definition Related Artifact.")

class ServiceDefinitionTrigger(models.Model):
    _name = "hc.service.definition.trigger"
    _description = "Service Definition Trigger"
    _inherit = ["hc.basic.association", "hc.trigger.definition"]

    service_definition_id = fields.Many2one(
        comodel_name="hc.res.service.definition",
        string="Service Definition",
        help="Service Definition associated with this Service Definition Trigger.")

class ServiceDefinitionDataRequirement(models.Model):
    _name = "hc.service.definition.data.requirement"
    _description = "Service Definition Data Requirement"
    _inherit = ["hc.basic.association", "hc.data.requirement"]

    service_definition_id = fields.Many2one(
        comodel_name="hc.res.service.definition",
        string="Service Definition",
        help="Service Definition associated with this Service Definition Data Requirement.")
