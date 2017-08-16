# -*- coding: utf-8 -*-

from openerp import models, fields, api

class GraphDefinition(models.Model):
    _name = "hc.res.graph.definition"
    _description = "Graph Definition"
    _inherit = ["hc.domain.resource"]
    _rec_name = "name"

    url = fields.Char(
        string="URI",
        help="Logical URI to reference this graph definition (globally unique).")
    version = fields.Char(
        string="Version",
        help="Business version of the graph definition.")
    name = fields.Char(
        string="Name",
        required="True",
        help="Name for this graph definition (Computer friendly).")
    status = fields.Selection(
        string="Graph Definition Status",
        required="True",
        selection=[
            ("draft", "Draft"),
            ("active", "Active"),
            ("retired", "Retired")],
        help="The status of this graph definition. Enables tracking the life-cycle of the content.")
    is_experimental = fields.Boolean(
        string="Experimental",
        help="If for testing purposes, not real usage.")
    date = fields.Datetime(
        string="Date",
        help="Date this was last changed.")
    publisher = fields.Char(
        string="Publisher",
        help="Name of the publisher (Organization or individual).")
    contact_ids = fields.One2many(
        comodel_name="hc.graph.definition.contact",
        inverse_name="graph_definition_id",
        string="Contacts",
        help="Contact details for the publisher.")
    description = fields.Text(
        string="Description",
        help="Natural language description of the graph definition.")
    use_context_ids = fields.One2many(
        comodel_name="hc.graph.definition.use.context",
        inverse_name="graph_definition_id",
        string="Use Contexts",
        help="Content intends to support these contexts.")
    jurisdiction_ids = fields.Many2many(
        comodel_name="hc.vs.jurisdiction",
        relation="graph_definition_jurisdiction_rel",
        string="Jurisdictions",
        help="Intended jurisdiction for graph definition (if applicable).")
    purpose = fields.Text(
        string="Purpose",
        help="Why this graph definition is defined.")
    start_id = fields.Many2one(
        comodel_name="hc.vs.resource.type",
        string="Start",
        required="True",
        help="Type of resource at which the graph starts.")
    profile = fields.Char(
        string="URI",
        help="Profile on base resource.")
    link_ids = fields.One2many(
        comodel_name="hc.graph.definition.link",
        inverse_name="graph_definition_id",
        string="Links",
        help="Links this graph makes rules about.")

class GraphDefinitionLink(models.Model):
    _name = "hc.graph.definition.link"
    _description = "Graph Definition Link"

    graph_definition_id = fields.Many2one(
        comodel_name="hc.res.graph.definition",
        string="Graph Definition",
        help="Graph Definition associated with this Graph Definition Link.")
    target_id = fields.Many2one(
        comodel_name="hc.graph.definition.link.target",
        string="Target",
        help="Potential target for the link.")
    path = fields.Char(
        string="Path",
        required="True",
        help="Path in the resource that contains the link.")
    slice_name = fields.Char(
        string="Slice Name",
        help="Which slice (if profiled).")
    min = fields.Integer(
        string="Min",
        help="Minimum occurences for this link.")
    max = fields.Integer(
        string="Max",
        help="Maximum occurences for this link.")
    description = fields.Text(
        string="Description",
        help="Why this link is specified.")
    target_ids = fields.One2many(
        comodel_name="hc.graph.definition.link.target",
        inverse_name="link_id",
        string="Targets",
        required="True", help="Potential target for the link.")

class GraphDefinitionLinkTarget(models.Model):
    _name = "hc.graph.definition.link.target"
    _description = "Graph Definition Link Target"

    link_id = fields.Many2one(
        comodel_name="hc.graph.definition.link",
        string="Link",
        help="Links this graph makes rules about.")
    type_id = fields.Many2one(
        comodel_name="hc.vs.resource.type",
        string="Type",
        help="Type of resource this link refers to.")
    profile = fields.Char(
        string="URI",
        help="Profile for the target resource.")
    link_ids = fields.One2many(
        comodel_name="hc.graph.definition.link",
        inverse_name="target_id",
        string="Links",
        help="Content as for GraphDefinition.link Additional links from target resource.")
    compartment_ids = fields.One2many(
        comodel_name="hc.graph.definition.link.target.compartment",
        inverse_name="target_id",
        string="Compartments",
        help="Compartment Consistency Rules.")

class GraphDefinitionLinkTargetCompartment(models.Model):
    _name = "hc.graph.definition.link.target.compartment"
    _description = "Graph Definition Link Target Compartment"

    target_id = fields.Many2one(
        comodel_name="hc.graph.definition.link.target",
        string="Target",
        help="Potential target for the link.")
    code_id = fields.Many2one(
        comodel_name="hc.vs.compartment.type",
        string="Code",
        required="True",
        help="Identifies the compartment.")
    rule = fields.Selection(
        string="Rule",
        required="True",
        selection=[
            ("identical", "Identical"),
            ("matching", "Matching"),
            ("different", "Different"),
            ("custom", "Custom")],
        help="How a compartment must be linked.")
    expression = fields.Text(
        string="Expression",
        help="Custom rule, as a FHIRPath expression.")
    description = fields.Text(
        string="Description",
        help="Documentation for FHIRPath expression.")

class GraphDefinitionContact(models.Model):
    _name = "hc.graph.definition.contact"
    _description = "Graph Definition Contact"
    _inherit = ["hc.basic.association"]
    _inherits = {"hc.contact.detail": "contact_id"}

    contact_id = fields.Many2one(
        comodel_name="hc.contact.detail",
        string="Contact",
        ondelete="restrict",
        required="True",
        help="Contact Detail associated with this Graph Definition Contact.")
    graph_definition_id = fields.Many2one(
        comodel_name="hc.res.graph.definition",
        string="Graph Definition",
        help="Graph Definition associated with this Graph Definition Contact.")

class GraphDefinitionUseContext(models.Model):
    _name = "hc.graph.definition.use.context"
    _description = "Graph Definition Use Context"
    _inherit = ["hc.basic.association", "hc.usage.context"]

    graph_definition_id = fields.Many2one(
        comodel_name="hc.res.graph.definition",
        string="Graph Definition",
        help="Graph Definition associated with this Graph Definition Use Context.")

class CompartmentType(models.Model):
    _name = "hc.vs.compartment.type"
    _description = "Compartment Type"
    _inherit = ["hc.value.set.contains"]

    name = fields.Char(
        string="Name",
        help="Name of this compartment type.")
    code = fields.Char(
        string="Code",
        help="Code of this compartment type.")
    contains_id = fields.Many2one(
        comodel_name="hc.vs.compartment.type",
        string="Contains",
        help="Parent compartment type.")
