# -*- coding: utf-8 -*-

from openerp import models, fields, api
from datetime import datetime
from openerp.tools import DEFAULT_SERVER_DATETIME_FORMAT as DTF

class StructureDefinition(models.Model):
    _name = "hc.res.structure.definition"
    _description = "Structure Definition"

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
        help="Name for this structure definition (computer friendly).")
    # added
    display = fields.Char(
        string="Display",
        help="Short informal name for this Structure Definition.")
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
    status_history_ids = fields.One2many(
        comodel_name="hc.structure.definition.status.history",
        inverse_name="structure_definition_id",
        string="Status History",
        help="The status of the structure definition over time.")
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
    abstract = fields.Selection(
        string="Abstract",
        required="True",
        selection=[
            ("true", "True"),
            ("false", "False")],
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
    # type = fields.Selection(
    #     string="Type",
    #     required="True",
    #     selection=[
    #         ("type", "Type"),
    #         ("element", "Element"),
    #         ("resource", "Resource"),
    #         ("constraint", "Constraint"),
    #         ("extension", "Extension"),
    #         ("composition", "Composition"),
    #         ("carePlan", "CarePlan")],
    #     help="The type this structure is describes.")
    type_id = fields.Many2one(
        comodel_name="hc.vs.defined.type",
        string="Code",
        required="True",
        help="Type defined or constrained by this structure.")
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

    @api.model
    def create(self, vals):
        status_history_obj = self.env['hc.structure.definition.status.history']
        res = super(StructureDefinition, self).create(vals)
        if vals and vals.get('status'):
            status_history_vals = {
                'structure_definition_id': res.id,
                'status': res.status,
                'start_date': datetime.today()
                }
            status_history_obj.create(status_history_vals)
        return res

    @api.multi
    def write(self, vals):
        status_history_obj = self.env['hc.structure.definition.status.history']
        res = super(StructureDefinition, self).write(vals)
        status_history_record_ids = status_history_obj.search([('end_date','=', False)])
        if status_history_record_ids:
            if vals.get('status') and status_history_record_ids[0].status != vals.get('status'):
                for status_history in status_history_record_ids:
                    status_history.end_date = datetime.strftime(datetime.today(), DTF)
                    time_diff = datetime.today() - datetime.strptime(status_history.start_date, DTF)
                    if time_diff:
                        days = str(time_diff).split(',')
                        if days and len(days) > 1:
                            status_history.time_diff_day = str(days[0])
                            times = str(days[1]).split(':')
                            if times and times > 1:
                                status_history.time_diff_hour = str(times[0])
                                status_history.time_diff_min = str(times[1])
                                status_history.time_diff_sec = str(times[2])
                        else:
                            times = str(time_diff).split(':')
                            if times and times > 1:
                                status_history.time_diff_hour = str(times[0])
                                status_history.time_diff_min = str(times[1])
                                status_history.time_diff_sec = str(times[2])
                status_history_vals = {
                    'structure_definition_id': self.id,
                    'status': vals.get('status'),
                    'start_date': datetime.today()
                    }
                status_history_obj.create(status_history_vals)
        return res

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

    structure_definition_id = fields.Many2one(
        comodel_name="hc.res.structure.definition",
        string="Structure Definition",
        help="Structure Definition associated with this Structure Definition Snapshot.")
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

    structure_definition_id = fields.Many2one(
        comodel_name="hc.res.structure.definition",
        string="Structure Definition",
        help="Structure Definition associated with this Structure Definition Differential.")
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
        help="Structure Definition associated with this Structure Definition Identifier.")

    @api.depends('code_id', 'value')
    def _compute_name(self):
        comp_name = '/'
        for hc_structure_definition_identifier in self:
            if hc_structure_definition_identifier.code_id:
                comp_name = hc_structure_definition_identifier.code_id.name or ''
            if hc_structure_definition_identifier.value:
                comp_name = comp_name + ", " + hc_structure_definition_identifier.value or ''
            hc_structure_definition_identifier.name = comp_name

class StructureDefinitionStatusHistory(models.Model):
    _name = "hc.structure.definition.status.history"
    _description = "Structure Definition Status History"

    structure_definition_id = fields.Many2one(
        comodel_name="hc.res.structure.definition",
        string="Structure Definition",
        help="Structure Definition associated with this Structure Definition Status History.")
    status = fields.Char(
        string="Status",
        help="The status of the structure definition.")
    start_date = fields.Datetime(
        string="Start Date",
        help="Start of the period during which this structure definition status is valid.")
    end_date = fields.Datetime(
        string="End Date",
        help="End of the period during which this structure definition status is valid.")
    time_diff_day = fields.Char(
        string="Time Diff (days)",
        help="Days duration of the status.")
    time_diff_hour = fields.Char(
        string="Time Diff (hours)",
        help="Hours duration of the status.")
    time_diff_min = fields.Char(
        string="Time Diff (minutes)",
        help="Minutes duration of the status.")
    time_diff_sec = fields.Char(
        string="Time Diff (seconds)",
        help="Seconds duration of the status.")

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
        help="Structure Definition associated with this Structure Definition Contact.")

class StructureDefinitionUseContext(models.Model):
    _name = "hc.structure.definition.use.context"
    _description = "Structure Definition Use Context"
    _inherit = ["hc.basic.association", "hc.usage.context"]

    structure_definition_id = fields.Many2one(
        comodel_name="hc.res.structure.definition",
        string="Structure Definition",
        help="Structure Definition associated with this Structure Definition Use Context.")

    @api.depends('value_type')
    def _compute_value_name(self):
        for hc_structure_definition_usage_context in self:
            if hc_structure_definition_usage_context.value_type == 'code':
                hc_structure_definition_usage_context.value_name = hc_structure_definition_usage_context.value_code_id.name
            elif hc_structure_definition_usage_context.value_type == 'quantity':
                hc_structure_definition_usage_context.value_name = str(hc_structure_definition_usage_context.value_quantity) + " " + str(hc_structure_definition_usage_context.value_quantity_uom_id.name)
            elif hc_structure_definition_usage_context.value_type == 'range':
                hc_structure_definition_usage_context.value_name = "Between " + str(hc_structure_definition_usage_context.value_range_low) + " and " + str(hc_structure_definition_usage_context.value_range_high)

class StructureDefinitionContext(models.Model):
    _name = "hc.structure.definition.context"
    _description = "Structure Definition Context"
    _inherit = ["hc.basic.association"]

    structure_definition_id = fields.Many2one(
        comodel_name="hc.res.structure.definition",
        string="Structure Definition",
        help="Structure Definition associated with this Structure Definition Context.")
    context = fields.Char(
        string="Context",
        help="Context associated with this Structure Definition Context.")

class StructureDefinitionContextInvariant(models.Model):
    _name = "hc.structure.definition.context.invariant"
    _description = "Structure Definition Context Invariant"
    _inherit = ["hc.basic.association"]

    structure_definition_id = fields.Many2one(
        comodel_name="hc.res.structure.definition",
        string="Structure Definition",
        help="Structure Definition associated with this tructure Definition Context Invariant.")
    context_invariant = fields.Char(
        string="Context Invariant",
        help="Context Invariant associated with this Structure Definition Context Invariant.")

class StructureDefinitionSnapshotElement(models.Model):
    _name = "hc.structure.definition.snapshot.element"
    _description = "Structure Definition Snapshot Element"
    _inherit = ["hc.basic.association"]
    _inherits = {"hc.element.definition": "element_id"}

    element_id = fields.Many2one(
        comodel_name="hc.element.definition",
        string="Element Definition",
        ondelete="restrict",
        required="True",
        help="Element Definition associated with this Structure Definition Snapshot Element.")
    snapshot_id = fields.Many2one(
        comodel_name="hc.structure.definition.snapshot",
        string="Structure Definition Snapshot",
        help="Snapshot associated with this Structure Definition Snapshot Element.")

class StructureDefinitionDifferentialElement(models.Model):
    _name = "hc.structure.definition.differential.element"
    _description = "Structure Definition Differential Element"
    _inherit = ["hc.basic.association"]
    _inherits = {"hc.element.definition": "element_id"}

    element_id = fields.Many2one(
        comodel_name="hc.element.definition",
        string="Element Definition",
        ondelete="restrict",
        required="True",
        help="Element Definition associated with this Structure Definition Snapshot Element.")
    differential_id = fields.Many2one(
        comodel_name="hc.structure.definition.differential",
        string="Structure Definition Differential",
        help="Differential associated with this Structure Definition Snapshot Element.")

class ProfileCode(models.Model):
    _name = "hc.vs.profile.code"
    _description = "Profile Code"
    _inherit = ["hc.value.set.contains"]

    name = fields.Char(
        string="Name",
        help="Name of this profile code.")
    code = fields.Char(
        string="Code",
        help="Code of this profile code.")
    contains_id = fields.Many2one(
        comodel_name="hc.vs.element.definition.code",
        string="Parent",
        help="Parent profile code.")

# External reference

class DataRequirementProfile(models.Model):
    _inherit = "hc.data.reqt.profile"

    profile_id = fields.Many2one(
        comodel_name="hc.res.structure.definition",
        string="Profile",
        help="Profile associated with this Data Requirement Profile.")
