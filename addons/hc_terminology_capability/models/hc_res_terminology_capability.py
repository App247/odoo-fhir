# -*- coding: utf-8 -*-

from openerp import models, fields, api

class TerminologyCapability(models.Model):
    _name = "hc.res.terminology.capability"
    _description = "Terminology Capability"
    _inherit = ["hc.domain.resource"]
    _rec_name = "name"

    url = fields.Char(
        string="URI",
        help="Logical URI to reference this terminology capabilities (globally unique).")
    version = fields.Char(
        string="Version",
        help="Business version of the terminology capabilities.")
    name = fields.Char(
        string="Name",
        help="Name for this terminology capabilities (computer friendly).")
    title = fields.Char(
        string="Title",
        help="Name for this terminology capabilities (human friendly).")
    status_id = fields.Many2one(
        comodel_name="hc.vs.publication.status",
        string="Status",
        required="True",
        help="The status of this terminology capabilities. Enables tracking the life-cycle of the content.")
    is_experimental = fields.Boolean(
        string="Experimental",
        help="For testing purposes, not real usage.")
    date = fields.Datetime(
        string="Date",
        required="True",
        help="Date this was last changed.")
    publisher = fields.Char(
        string="Publisher",
        help="Name of the publisher (organization or individual).")
    contact_ids = fields.One2many(
        comodel_name="hc.terminology.capability.contact",
        inverse_name="terminology_capability_id",
        string="Contacts",
        help="Contact details for the publisher.")
    description = fields.Text(
        string="Description",
        help="Natural language description of the terminology capabilities.")
    use_context_ids = fields.One2many(
        comodel_name="hc.terminology.capability.use.context",
        inverse_name="terminology_capability_id",
        string="Use Contexts",
        help="Context the content is intended to support.")
    jurisdiction_ids = fields.Many2many(
        comodel_name="hc.vs.jurisdiction",
        relation="terminology_capability_jurisdiction_rel",
        string="Jurisdictions",
        help="Intended jurisdiction for terminology capabilities (if applicable).")
    purpose = fields.Text(
        string="Purpose",
        help="Why this terminology capabilities is defined.")
    copyright = fields.Text(
        string="Copyright",
        help="Use and/or publishing restrictions.")
    is_locked_date = fields.Boolean(
        string="Locked Date",
        help="Whether locked Date is supported.")
    code_system_ids = fields.One2many(
        comodel_name="hc.terminology.capability.code.system",
        inverse_name="terminology_capability_id",
        string="Code Systems",
        help="A code system supported by the server.")
    expansion_ids = fields.One2many(
        comodel_name="hc.terminology.capability.expansion",
        inverse_name="terminology_capability_id",
        string="Expansions",
        help="Information about the $expansion operation.")
    lookup_ids = fields.One2many(
        comodel_name="hc.terminology.capability.lookup",
        inverse_name="terminology_capability_id",
        string="Lookups",
        help="Information about the $lookup operation.")
    validation_ids = fields.One2many(
        comodel_name="hc.terminology.capability.validation",
        inverse_name="terminology_capability_id",
        string="Validations",
        help="Information about the $validation operation.")
    translation_ids = fields.One2many(
        comodel_name="hc.terminology.capability.translation",
        inverse_name="terminology_capability_id",
        string="Translations",
        help="Information about the $translation operation.")
    closure_ids = fields.One2many(
        comodel_name="hc.terminology.capability.closure",
        inverse_name="terminology_capability_id",
        string="Closures",
        help="Information about the $closure operation.")

class TerminologyCapabilityCodeSystem(models.Model):
    _name = "hc.terminology.capability.code.system"
    _description = "Terminology Capability Code System"
    _inherit = ["hc.backbone.element"]

    terminology_capability_id = fields.Many2one(
        comodel_name="hc.res.terminology.capability",
        string="Terminology Capability", help="Terminology Capability associated with this Terminology Capability Code System.")
    uri = fields.Char(string="URI", help="URI for the Code System.")
    version = fields.Char(string="Version", help="Version of Code System supported.")
    is_compositional = fields.Boolean(string="Compositional", help="If compositional grammar is supported.")
    language_ids = fields.Many2many(comodel_name="hc.vs.resource.type", relation="terminology_capability_code_system_language_rel", string="Languages", help="Displays supported.")
    filter_ids = fields.One2many(comodel_name="hc.terminology.capability.code.system.filter", inverse_name="code_system_id", string="Filters", help="Filter Properties supported.")
    property_ids = fields.Many2many(comodel_name="hc.vs.resource.type", relation="terminology_capability_code_system_property_rel", string="Propertys", help="supported for $lookup.")

class TerminologyCapabilityCodeSystemFilter(models.Model):
    _name = "hc.terminology.capability.code.system.filter"
    _description = "Terminology Capability Code System Filter"
    _inherit = ["hc.backbone.element"]

    code_system_id = fields.Many2one(comodel_name="hc.terminology.capability.code.system", string="Code System", help="A code system supported by the server.")
    code_id = fields.Many2one(comodel_name="hc.vs.terminology.capability.filter", string="Code", required="True", help="Code of the property supported.")
    op_ids = fields.Many2many(comodel_name="hc.vs.resource.type", relation="terminology_capability_code_system_filter_op_rel", string="Ops", required="True", help="supported for the property.")

class TerminologyCapabilityExpansion(models.Model):
    _name = "hc.terminology.capability.expansion"
    _description = "Terminology Capability Expansion"
    _inherit = ["hc.backbone.element"]

    terminology_capability_id = fields.Many2one(comodel_name="hc.res.terminology.capability", string="Terminology Capability", help="Terminology Capability associated with this Terminology Capability Expansion.")
    is_supported = fields.Boolean(string="Supported", required="True", help="Whether operation is supported.")
    is_hierarchical = fields.Boolean(string="Hierarchical", help="Whether the server can return nested value sets.")
    is_paging = fields.Boolean(string="Paging", help="Whether the server supports paging on expansion.")
    is_incomplete = fields.Boolean(string="Incomplete", help="Allow request for incomplete expansions?")
    profile_id = fields.Many2one(comodel_name="hc.res.structure.definition", string="Profile", help="Structure Definition associated with this Terminology Capability Expansion.")
    text_filter = fields.Text(string="Text Filter", help="Documentation about text searching works.")

class TerminologyCapabilityLookup(models.Model):
    _name = "hc.terminology.capability.lookup"
    _description = "Terminology Capability Lookup"
    _inherit = ["hc.backbone.element"]

    terminology_capability_id = fields.Many2one(comodel_name="hc.res.terminology.capability", string="Terminology Capability", help="Terminology Capability associated with this Terminology Capability Lookup.")
    is_supported = fields.Boolean(string="Supported", required="True", help="Whether $lookup is supported.")

class TerminologyCapabilityValidation(models.Model):
    _name = "hc.terminology.capability.validation"
    _description = "Terminology Capability Validation"
    _inherit = ["hc.backbone.element"]

    terminology_capability_id = fields.Many2one(comodel_name="hc.res.terminology.capability", string="Terminology Capability", help="Terminology Capability associated with this Terminology Capability Validation.")
    is_supported = fields.Boolean(string="Supported", required="True", help="Whether $validation is supported.")
    is_translations = fields.Boolean(string="Translations", required="True", help="Whether translations are validated.")

class TerminologyCapabilityTranslation(models.Model):
    _name = "hc.terminology.capability.translation"
    _description = "Terminology Capability Translation"
    _inherit = ["hc.backbone.element"]

    terminology_capability_id = fields.Many2one(comodel_name="hc.res.terminology.capability", string="Terminology Capability", help="Terminology Capability associated with this Terminology Capability Translation.")
    is_supported = fields.Boolean(string="Supported", required="True", help="Whether $translation is supported.")
    is_need_map = fields.Boolean(string="Need Map", required="True", help="Whether the client must identify the map.")

class TerminologyCapabilityClosure(models.Model):
    _name = "hc.terminology.capability.closure"
    _description = "Terminology Capability Closure"
    _inherit = ["hc.backbone.element"]

    terminology_capability_id = fields.Many2one(comodel_name="hc.res.terminology.capability", string="Terminology Capability", help="Terminology Capability associated with this Terminology Capability Closure.")
    is_supported = fields.Boolean(string="Supported", required="True", help="Whether the closure operation is supported.")
    is_translation = fields.Boolean(string="Translation", help="If cross-system closure is supported.")

class TerminologyCapabilityContact(models.Model):
    _name = "hc.terminology.capability.contact"
    _description = "Terminology Capability Contact"
    _inherit = ["hc.basic.association"]
    _inherits = {"hc.contact.detail": "contact_id"}

    contact_id = fields.Many2one(comodel_name="hc.contact.detail", string="Contact", ondelete="restrict", required="True", help="Contact Detail associated with this Terminology Capability Contact.")
    terminology_capability_id = fields.Many2one(comodel_name="hc.res.terminology.capability", string="Terminology Capability", help="Terminology Capability associated with this Terminology Capability Contact.")

class TerminologyCapabilityUseContext(models.Model):
    _name = "hc.terminology.capability.use.context"
    _description = "Terminology Capability Use Context"
    _inherit = ["hc.basic.association", "hc.usage.context"]

    terminology_capability_id = fields.Many2one(comodel_name="hc.res.terminology.capability", string="Terminology Capability", help="Terminology Capability associated with this Terminology Capability Use Context.")

class TerminologyCapabilityFilter(models.Model):
    _name = "hc.vs.terminology.capability.filter"
    _description = "Terminology Capability Filter"
    _inherit = ["hc.value.set.contains"]

    name = fields.Char(string="Name", help="Name of this terminology capability filter.")
    code = fields.Char(string="Code", help="Code of this terminology capability filter.")
    contains_id = fields.Many2one(comodel_name="hc.vs.terminology.capability.filter", string="Parent", help="Parent terminology capability filter.")
