# -*- coding: utf-8 -*-

from openerp import models, fields, api

class StructureDefinition(models.Model):
    _name = "hc.res.structure.definition"
    _description = "Structure Definition"
    _rec_name = "title"

    url = fields.Char(
        string="URI",
        required="True",
        help="Literal URL used to reference this Structure Definition.")
    identifier_ids = fields.One2many(
        comodel_name="hc.structure.definition.identifier",
        inverse_name="structure_definition_id",
        string="Identifiers",
        help="Other identifiers for the Structure Definition.")
    version = fields.Char(
        string="Version",
        help="Logical id for this version of the Structure Definition.")
    name = fields.Char(
        string="Name",
        required="True",
        help="Informal name for this Structure Definition.")
    title = fields.Char(
        string="Title",
        help="Name for this structure definition (Human friendly).")
    status = fields.Selection(
        string="Status",
        required="True",
        selection=[
            ("draft", "Draft"),
            ("active", "Active"),
            ("retired", "Retired"),
            ("unknown", "Unknown")],
        default="draft",
        help="The status of this structure definition. Enables tracking the life-cycle of the content.")
    is_experimental = fields.Boolean(
        string="Experimental",
        help="If for testing purposes, not real usage.")
    date = fields.Datetime(
        string="Date",
        help="Date for this version of the StructureDefinition.")
    publisher = fields.Char(
        string="Publisher",
        help="Name of the publisher (Organization or individual).")
    contact_ids = fields.One2many(
        comodel_name="hc.structure.definition.contact",
        inverse_name="structure_definition_id",
        string="Contacts",
        help="Contact details for the publisher.")
    description = fields.Text(
        string="Description",
        help="Natural language description of the StructureDefinition.")
    use_context_ids = fields.One2many(
        comodel_name="hc.structure.definition.use.context",
        inverse_name="structure_definition_id",
        string="Use Contexts",
        help="Content intends to support these contexts.")
    jurisdiction_ids = fields.Many2many(
        comodel_name="hc.vs.jurisdiction",
        relation="structure_definition_jurisdiction_rel",
        string="Jurisdictions",
        help="Intended jurisdiction for structure definition (if applicable).")
    purpose = fields.Text(
        string="Purpose",
        help="Why this structure definition is defined.")
    copyright = fields.Text(
        string="Copyright",
        help="Use and/or Publishing restrictions.")
    keyword_ids = fields.Many2many(
        comodel_name="hc.vs.profile.code",
        relation="structure_definition_keyword_rel",
        string="Keywords",
        help="Assist with indexing and finding.")
    fhir_version = fields.Char(
        string="FHIR Version",
        help="FHIR Version this Structure Definition targets.")
    kind = fields.Selection(
        string="Kind",
        required="True",
        selection=[
            ("primitive-type", "Primitive Type"),
            ("complex-type", "Complex Type"),
            ("resource", "Resource"),
            ("logical", "Logical")],
        help="Defines the kind of structure that this definition is describing.")
    is_abstract = fields.Boolean(
        string="Abstract",
        required="True",
        help="Whether the structure is abstract.")
    context_type = fields.Selection(
        string="Context Type",
        selection=[
            ("resource", "Resource"),
            ("datatype", "Datatype"),
            ("extension", "Extension")],
        help="If this is an extension, Identifies the context within FHIR resources where the extension can be used.")
    context_ids = fields.One2many(
        comodel_name="hc.structure.definition.context",
        inverse_name="structure_definition_id",
        string="Contexts",
        help="Where the extension can be used in instances.")
    context_invariant_ids = fields.One2many(
        comodel_name="hc.structure.definition.context.invariant",
        inverse_name="structure_definition_id",
        string="Context Invariants",
        help="FHIRPath invariants - when the extension can be used.")
    type = fields.Selection(
        string="Type",
        required="True",
        selection=[
            ("type", "Type"),
            ("resource", "Resource"),
            ("constraint", "Constraint"),
            ("extension", "Extension")],
        help="The type this structure is describes.")
    base_definition = fields.Char(
        string="Base Definition URI",
        help="Definition that this type is constrained/specialized from.")
    derivation = fields.Selection(
        string="Derivation",
        selection=[
            ("specialization", "Specialization"),
            ("constraint", "Constraint")],
        help="How relates to base definition.")
    mapping_ids = fields.One2many(
        comodel_name="hc.structure.definition.mapping",
        inverse_name="structure_definition_id",
        string="Mappings",
        help="External specification that the content is mapped to.")
    snapshot_id = fields.Many2one(
        comodel_name="hc.structure.definition.snapshot",
        string="Snapshot",
        help="Snapshot view of the structure.")
    differential_id = fields.Many2one(
        comodel_name="hc.structure.definition.differential",
        string="Differential",
        help="Differential view of the structure.")

class StructureDefinitionMapping(models.Model):
    _name = "hc.structure.definition.mapping"
    _description = "Structure Definition Mapping"

    structure_definition_id = fields.Many2one(
        comodel_name="hc.res.structure.definition",
        string="Structure Definition",
        help="Structure Definition associated with this Structure Definition Mapping.")
    identity = fields.Char(
        string="Identity",
        required="True",
        help="Internal id when this mapping is used.")
    uri = fields.Char(
        string="URI",
        help="Identifies what this mapping refers to.")
    name = fields.Char(
        string="Name",
        help="Names what this mapping refers to.")
    comment = fields.Text(
        string="Comment",
        help="Versions, Issues, Scope limitations etc.")

class StructureDefinitionSnapshot(models.Model):
    _name = "hc.structure.definition.snapshot"
    _description = "Structure Definition Snapshot"

    name = fields.Char(
        string="Name",
        help="Text representation of the snapshot.")
    element_ids = fields.One2many(
        comodel_name="hc.structure.definition.snapshot.element",
        inverse_name="snapshot_id",
        string="Elements",
        required="True",
        help="Definition of elements in the resource (if no StructureDefinition).")

class StructureDefinitionDifferential(models.Model):
    _name = "hc.structure.definition.differential"
    _description = "Structure Definition Differential"

    name = fields.Char(
        string="Name",
        help="Text representation of the differential.")
    element_ids = fields.One2many(
        comodel_name="hc.structure.definition.differential.element",
        inverse_name="differential_id",
        string="Elements",
        required="True",
        help="Definition of elements in the resource (if no StructureDefinition).")

class StructureDefinitionIdentifier(models.Model):
    _name = "hc.structure.definition.identifier"
    _description = "Structure Definition Identifier"
    _inherit = ["hc.basic.association", "hc.identifier"]

    structure_definition_id = fields.Many2one(
        comodel_name="hc.res.structure.definition",
        string="Structure Definition",
        help="Structure Definition associated with this structure definition identifier.")

class StructureDefinitionContact(models.Model):
    _name = "hc.structure.definition.contact"
    _description = "Structure Definition Contact"
    _inherit = ["hc.basic.association"]
    _inherits = {"hc.contact.detail": "contact_id"}

    contact_id = fields.Many2one(
        comodel_name="hc.contact.detail",
        string="Contact",
        ondelete="restrict",
        required="True",
        help="Contact Detail associated with this Structure Definition Contact.")
    structure_definition_id = fields.Many2one(
        comodel_name="hc.res.structure.definition",
        string="Structure Definition",
        help="Structure Definition associated with this structure definition contact.")

class StructureDefinitionUseContext(models.Model):
    _name = "hc.structure.definition.use.context"
    _description = "Structure Definition Use Context"
    _inherit = ["hc.basic.association", "hc.usage.context"]

    structure_definition_id = fields.Many2one(
        comodel_name="hc.res.structure.definition",
        string="Structure Definition",
        help="Structure Definition associated with this structure definition use context.")

class StructureDefinitionContext(models.Model):
    _name = "hc.structure.definition.context"
    _description = "Structure Definition Context"
    _inherit = ["hc.basic.association"]

    structure_definition_id = fields.Many2one(
        comodel_name="hc.res.structure.definition",
        string="Structure Definition",
        help="Structure Definition associated with this structure definition context.")
    context = fields.Char(string="Context",
        help="Context associated with this Structure Definition Context.")

class StructureDefinitionContextInvariant(models.Model):
    _name = "hc.structure.definition.context.invariant"
    _description = "Structure Definition Context Invariant"
    _inherit = ["hc.basic.association"]

    structure_definition_id = fields.Many2one(
        comodel_name="hc.res.structure.definition",
        string="Structure Definition",
        help="Structure Definition associated with this structure definition context invariant.")
    context_invariant = fields.Char(
        string="Context Invariant",
        help="Context Invariant associated with this Structure Definition Context Invariant.")

class StructureDefinitionSnapshotElement(models.Model):
    _name = "hc.structure.definition.snapshot.element"
    _description = "Structure Definition Snapshot Element"
    _inherit = ["hc.basic.association", "hc.element.definition"]

    snapshot_id = fields.Many2one(
        comodel_name="hc.structure.definition.snapshot.element")
    representation_ids = fields.One2many(
        comodel_name="hc.structure.definition.snapshot.element.representation")
    alias_ids = fields.One2many(
        comodel_name="hc.structure.definition.snapshot.element.alias")
    condition_ids = fields.One2many(
        comodel_name="hc.structure.definition.snapshot.element.condition")
    slicing_id = fields.Many2one(
        comodel_name="hc.structure.definition.snapshot.element.slicing")
    base_id = fields.Many2one(
        comodel_name="hc.structure.definition.snapshot.element.base")
    type_ids = fields.One2many(
        comodel_name="hc.structure.definition.snapshot.element.type")
    example_ids = fields.One2many(
        comodel_name="hc.structure.definition.snapshot.element.example")
    constraint_ids = fields.One2many(
        comodel_name="hc.structure.definition.snapshot.element.constraint")
    binding_id = fields.Many2one(
        comodel_name="hc.structure.definition.snapshot.element.binding")
    mapping_ids = fields.One2many(
        comodel_name="hc.structure.definition.snapshot.element.mapping")

class StructureDefinitionSnapshotElementSlicing(models.Model):
    _name = "hc.structure.definition.snapshot.element.slicing"
    _description = "Structure Definition Snapshot Element Slicing"
    _inherit = ["hc.element.definition.slicing"]

    discriminator_ids = fields.One2many(
        comodel_name="hc.structure.definition.snapshot.element.slicing.discriminator")

class StructureDefinitionSnapshotElementSlicingDiscriminator(models.Model):
    _name = "hc.structure.definition.snapshot.element.slicing.discriminator"
    _description = "Structure Definition Snapshot Element Slicing Discriminator"
    _inherit = ["hc.element.definition.slicing.discriminator"]

    slicing_id = fields.Many2one(
        comodel_name="hc.structure.definition.snapshot.element.slicing")

class StructureDefinitionSnapshotElementBase(models.Model):
    _name = "hc.structure.definition.snapshot.element.base"
    _description = "Structure Definition Snapshot Element Base"
    _inherit = ["hc.element.definition.base"]

class StructureDefinitionSnapshotElementType(models.Model):
    _name = "hc.structure.definition.snapshot.element.type"
    _description = "Structure Definition Snapshot Element Type"
    _inherit = ["hc.element.definition.type"]

    element_definition_id = fields.Many2one(
        comodel_name="hc.structure.definition.snapshot.element")

class StructureDefinitionSnapshotElementExample(models.Model):
    _name = "hc.structure.definition.snapshot.element.example"
    _description = "Structure Definition Snapshot Element Example"
    _inherit = ["hc.element.definition.example"]

    element_definition_id = fields.Many2one(
        comodel_name="hc.structure.definition.snapshot.element")

class StructureDefinitionSnapshotElementConstraint(models.Model):
    _name = "hc.structure.definition.snapshot.element.constraint"
    _description = "Structure Definition Snapshot Element Constraint"
    _inherit = ["hc.element.definition.constraint"]

    element_definition_id = fields.Many2one(
        comodel_name="hc.structure.definition.snapshot.element")

class StructureDefinitionSnapshotElementMapping(models.Model):
    _name = "hc.structure.definition.snapshot.element.mapping"
    _description = "Structure Definition Snapshot Element Mapping"
    _inherit = ["hc.element.definition.mapping"]

    element_definition_id = fields.Many2one(
        comodel_name="hc.structure.definition.snapshot.element")

class StructureDefinitionSnapshotElementRepresentation(models.Model):
    _name = "hc.structure.definition.snapshot.element.representation"
    _description = "Structure Definition Snapshot Element Representation"
    _inherit = ["hc.element.definition.representation"]

    element_definition_id = fields.Many2one(
        comodel_name="hc.structure.definition.snapshot.element")

class StructureDefinitionSnapshotElementAlias(models.Model):
    _name = "hc.structure.definition.snapshot.element.alias"
    _description = "Structure Definition Snapshot Element Alias"
    _inherit = ["hc.element.definition.alias"]

    element_definition_id = fields.Many2one(
        comodel_name="hc.structure.definition.snapshot.element")

class StructureDefinitionSnapshotElementCondition(models.Model):
    _name = "hc.structure.definition.snapshot.element.condition"
    _description = "Structure Definition Snapshot Element Condition"
    _inherit = ["hc.element.definition.condition"]

    element_definition_id = fields.Many2one(
        comodel_name="hc.structure.definition.snapshot.element")

class StructureDefinitionSnapshotElementTypeAggregation(models.Model):
    _name = "hc.structure.definition.snapshot.element.type.aggregation"
    _description = "Structure Definition Snapshot Element Type Aggregation"
    _inherit = ["hc.element.definition.type.aggregation"]

    type_id = fields.Many2one(
        comodel_name="hc.structure.definition.snapshot.element.type")

class StructureDefinitionSnapshotElementBinding(models.Model):
    _name = "hc.structure.definition.snapshot.element.binding"
    _description = "Structure Definition Snapshot Element Binding"
    _inherit = ["hc.element.definition.binding"]

class StructureDefinitionDifferentialElement(models.Model):
    _name = "hc.structure.definition.differential.element"
    _description = "Structure Definition Differential Element"
    _inherit = ["hc.basic.association", "hc.element.definition"]

    differential_id = fields.Many2one(
        comodel_name="hc.structure.definition.differential.element")
    representation_ids = fields.One2many(
        comodel_name="hc.structure.definition.differential.element.representation")
    alias_ids = fields.One2many(
        comodel_name="hc.structure.definition.differential.element.alias")
    condition_ids = fields.One2many(
        comodel_name="hc.structure.definition.differential.element.condition")
    slicing_id = fields.Many2one(
        comodel_name="hc.structure.definition.differential.element.slicing")
    base_id = fields.Many2one(
        comodel_name="hc.structure.definition.differential.element.base")
    type_ids = fields.One2many(
        comodel_name="hc.structure.definition.differential.element.type")
    example_ids = fields.One2many(
        comodel_name="hc.structure.definition.differential.element.example")
    constraint_ids = fields.One2many(
        comodel_name="hc.structure.definition.differential.element.constraint")
    binding_id = fields.Many2one(
        comodel_name="hc.structure.definition.differential.element.binding")
    mapping_ids = fields.One2many(
        comodel_name="hc.structure.definition.differential.element.mapping")

class StructureDefinitionDifferentialElementSlicing(models.Model):
    _name = "hc.structure.definition.differential.element.slicing"
    _description = "Structure Definition Differential Element Slicing"
    _inherit = ["hc.element.definition.slicing"]

    discriminator_ids = fields.One2many(
        comodel_name="hc.structure.defn.differential.element.slicing.discriminator")

class StructureDefnDifferentialElementSlicingDiscriminator(models.Model):
    _name = "hc.structure.defn.differential.element.slicing.discriminator"
    _description = "Structure Definition Differential Element Slicing Discriminator"
    _inherit = ["hc.element.definition.slicing.discriminator"]

    slicing_id = fields.Many2one(
        comodel_name="hc.structure.definition.differential.element.slicing")

class StructureDefinitionDifferentialElementBase(models.Model):
    _name = "hc.structure.definition.differential.element.base"
    _description = "Structure Definition Differential Element Base"
    _inherit = ["hc.element.definition.base"]

class StructureDefinitionDifferentialElementBinding(models.Model):
    _name = "hc.structure.definition.differential.element.binding"
    _description = "Structure Definition Differential Element Binding"
    _inherit = ["hc.element.definition.binding"]

class StructureDefinitionDifferentialElementType(models.Model):
    _name = "hc.structure.definition.differential.element.type"
    _description = "Structure Definition Differential Element Type"
    _inherit = ["hc.element.definition.type"]

    element_definition_id = fields.Many2one(
        comodel_name="hc.structure.definition.differential.element")

class StructureDefinitionDifferentialElementExample(models.Model):
    _name = "hc.structure.definition.differential.element.example"
    _description = "Structure Definition Differential Element Example"
    _inherit = ["hc.element.definition.example"]

    element_definition_id = fields.Many2one(
        comodel_name="hc.structure.definition.differential.element")

class StructureDefinitionDifferentialElementConstraint(models.Model):
    _name = "hc.structure.definition.differential.element.constraint"
    _description = "Structure Definition Differential Element Constraint"
    _inherit = ["hc.element.definition.constraint"]

    element_definition_id = fields.Many2one(
        comodel_name="hc.structure.definition.differential.element")

class StructureDefinitionDifferentialElementMapping(models.Model):
    _name = "hc.structure.definition.differential.element.mapping"
    _description = "Structure Definition Differential Element Mapping"
    _inherit = ["hc.element.definition.mapping"]

    element_definition_id = fields.Many2one(
        comodel_name="hc.structure.definition.differential.element")

class StructureDefinitionDifferentialElementRepresentation(models.Model):
    _name = "hc.structure.definition.differential.element.representation"
    _description = "Structure Definition Differential Element Representation"
    _inherit = ["hc.element.definition.representation"]

    element_definition_id = fields.Many2one(
        comodel_name="hc.structure.definition.differential.element")

class StructureDefinitionDifferentialElementAlias(models.Model):
    _name = "hc.structure.definition.differential.element.alias"
    _description = "Structure Definition Differential Element Alias"
    _inherit = ["hc.element.definition.alias"]

    element_definition_id = fields.Many2one(
        comodel_name="hc.structure.definition.differential.element")

class StructureDefinitionDifferentialElementCondition(models.Model):
    _name = "hc.structure.definition.differential.element.condition"
    _description = "Structure Definition Differential Element Condition"
    _inherit = ["hc.element.definition.condition"]

    element_definition_id = fields.Many2one(
        comodel_name="hc.structure.definition.differential.element")

class StructureDefinitionDifferentialElementTypeAggregation(models.Model):
    _name = "hc.structure.definition.differential.element.type.aggregation"
    _description = "Structure Definition Differential Element Type Aggregation"
    _inherit = ["hc.element.definition.type.aggregation"]

    type_id = fields.Many2one(
        comodel_name="hc.structure.definition.differential.element.type")

class ProfileCode(models.Model):
    _name = "hc.vs.profile.code"
    _description = "Profile Code"
    _inherit = ["hc.value.set.contains"]

# External reference

class DataRequirementProfile(models.Model):
    _inherit = "hc.data.reqt.profile"

    profile_id = fields.Many2one(
        comodel_name="hc.res.structure.definition",
        string="Profile",
        help="Profile associated with this Data Requirement Profile.")