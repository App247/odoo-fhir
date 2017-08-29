# -*- coding: utf-8 -*-

from openerp import models, fields, api

class EventDefinition(models.Model):
    _name = "hc.res.event.definition"
    _description = "Event Definition"
    _inherit = ["hc.domain.resource"]
    _rec_name = "name"

    url = fields.Char(
        string="URI",
        help="Logical URI to reference this message definition (globally unique).")
    identifier_ids = fields.One2many(
        comodel_name="hc.event.definition.identifier",
        inverse_name="event_definition_id",
        string="Identifiers",
        help="Additional identifier for the event definition.")
    version = fields.Char(
        string="Version",
        help="Business version of the event definition.")
    name = fields.Char(
        string="Name",
        help="Name for this event definition (computer friendly).")
    title = fields.Char(
        string="Title",
        help="Name for this event definition (human friendly).")
    status_id = fields.Many2one(
        comodel_name="hc.vs.publication.status",
        string="Status",
        required="True",
        help="The status of this event definition. Enables tracking the life-cycle of the content.")
    is_experimental = fields.Boolean(
        string="Experimental",
        help="For testing purposes, not real usage.")
    date = fields.Datetime(
        string="Date Last Changed",
        help="Date this was last changed.")
    publisher = fields.Char(
        string="Publisher",
        help="Name of the publisher (organization or individual).")
    description = fields.Text(
        string="Description",
        help="Natural language description of the event definition.")
    purpose = fields.Text(
        string="Purpose",
        help="Why this event definition is defined.")
    usage = fields.Char(
        string="Usage",
        help="Describes the clinical usage of the event definition.")
    approval_date = fields.Date(
        string="Approval Date",
        help="When the event definition was approved by publisher.")
    last_review_date = fields.Date(
        string="Last Review Date",
        help="When the event definition was last reviewed.")
    effective_period_start_date = fields.Datetime(
        string="Effective Period Start Date",
        help="Start of when the event definition is expected to be used.")
    effective_period_end_date = fields.Datetime(
        string="Effective Period End Date",
        help="End of when the event definition is expected to be used.")
    use_context_ids = fields.One2many(
        comodel_name="hc.event.definition.use.context",
        inverse_name="event_definition_id",
        string="Use Contexts",
        help="Context the content is intended to support.")
    jurisdiction_ids = fields.Many2many(
        comodel_name="hc.vs.jurisdiction",
        relation="event_definition_jurisdiction_rel",
        string="Jurisdictions",
        help="Intended jurisdiction for event definition (if applicable).")
    topic_ids = fields.Many2many(
        comodel_name="hc.vs.definition.topic",
        relation="event_definition_topic_rel",
        string="Topics",
        help="E.g. Education, Treatment, Assessment, etc.")
    contributor_ids = fields.One2many(
        comodel_name="hc.event.definition.contributor",
        inverse_name="event_definition_id",
        string="Contributors",
        help="A content contributor.")
    contact_ids = fields.One2many(
        comodel_name="hc.event.definition.contact",
        inverse_name="event_definition_id",
        string="Contacts",
        help="Contact details for the publisher.")
    copyright = fields.Text(
        string="Copyright",
        help="Use and/or publishing restrictions.")
    related_artifact_ids = fields.One2many(
        comodel_name="hc.event.definition.related.artifact",
        inverse_name="event_definition_id",
        string="Related Artifacts",
        help="Additional documentation, citations, etc.")
    trigger_id = fields.Many2one(
        comodel_name="hc.event.definition.trigger",
        string="Trigger",
        required="True",
        help='"+when" the event occurs.')

class EventDefinitionIdentifier(models.Model):
    _name = "hc.event.definition.identifier"
    _description = "Event Definition Identifier"
    _inherit = ["hc.basic.association", "hc.identifier"]

    event_definition_id = fields.Many2one(
        comodel_name="hc.res.event.definition",
        string="Event Definition",
        help="Event Definition associated with this Event Definition Identifier.")

class EventDefinitionUseContext(models.Model):
    _name = "hc.event.definition.use.context"
    _description = "Event Definition Use Context"
    _inherit = ["hc.basic.association", "hc.usage.context"]

    event_definition_id = fields.Many2one(
        comodel_name="hc.res.event.definition",
        string="Event Definition",
        help="Event Definition associated with this Event Definition Use Context.")

class EventDefinitionContributor(models.Model):
    _name = "hc.event.definition.contributor"
    _description = "Event Definition Contributor"
    _inherit = ["hc.basic.association"]
    _inherits = {"hc.contributor": "contributor_id"}

    contributor_id = fields.Many2one(
        comodel_name="hc.contributor",
        string="Contributor",
        ondelete="restrict",
        required="True",
        help="Contact Detail associated with this Event Definition Contributor.")
    event_definition_id = fields.Many2one(
        comodel_name="hc.res.event.definition",
        string="Event Definition",
        help="Event Definition associated with this Event Definition Contributor.")

class EventDefinitionContact(models.Model):
    _name = "hc.event.definition.contact"
    _description = "Event Definition Contact"
    _inherit = ["hc.basic.association"]
    _inherits = {"hc.contact.detail": "contact_id"}

    contact_id = fields.Many2one(
        comodel_name="hc.contact.detail",
        string="Contact",
        ondelete="restrict",
        required="True",
        help="Contact Detail associated with this Event Definition Contact.")
    event_definition_id = fields.Many2one(
        comodel_name="hc.res.event.definition",
        string="Event Definition",
        help="Event Definition associated with this Event Definition Contact.")

class EventDefinitionRelatedArtifact(models.Model):
    _name = "hc.event.definition.related.artifact"
    _description = "Event Definition Related Artifact"
    _inherit = ["hc.basic.association", "hc.related.artifact"]

    event_definition_id = fields.Many2one(
        comodel_name="hc.res.event.definition",
        string="Event Definition",
        help="Event Definition associated with this Event Definition Related Artifact.")

class EventDefinitionTrigger(models.Model):
    _name = "hc.event.definition.trigger"
    _description = "Event Definition Trigger"
    _inherit = ["hc.basic.association", "hc.trigger.definition"]

    event_definition_id = fields.Many2one(
        comodel_name="hc.res.event.definition",
        string="Event Definition",
        help="Event Definition associated with this Event Definition Trigger.")
