# -*- coding: utf-8 -*-

from openerp import models, fields, api

class OperationDefinition(models.Model):
    _name = "hc.res.operation.definition"
    _description = "Operation Definition"

    url = fields.Char(
        string="URI",
        help="Logical URI to reference this operation definition.")
    version = fields.Char(
        string="Version",
        help="Logical id for this version of the operation definition.")
    name = fields.Char(
        string="Name",
        required="True",
        help="Informal name for this profile.")
    status = fields.Selection(
        string="Status",
        required="True",
        selection=[
            ("draft", "Draft"),
            ("active", "Active"),
            ("retired", "Retired")],
        help="The status of this operation definition. Enables tracking the life-cycle of the content.")
    kind = fields.Selection(
        string="Kind",
        required="True",
        selection=[
            ("operation", "Operation"),
            ("query", "Query")],
        help="Whether this is an operation or a named query.")
    is_experimental = fields.Boolean(
        string="Experimental",
        help="If for testing purposes, not real usage.")
    date = fields.Datetime(
        string="Date",
        help="Date for this version of the operation definition.")
    publisher = fields.Char(
        string="Publisher",
        help="Name of the publisher (Organization or individual).")
    contact_ids = fields.One2many(
        comodel_name="hc.operation.definition.contact",
        inverse_name="operation_definition_id",
        string="Contacts",
        help="Contact details for the publisher.")
    description = fields.Text(
        string="Description",
        help="Natural language description of the operation.")
    use_context_ids = fields.One2many(
        comodel_name="hc.operation.definition.use.context",
        inverse_name="operation_definition_id",
        string="Use Contexts",
        help="Content intends to support these contexts.")
    jurisdiction_ids = fields.Many2many(
        comodel_name="hc.vs.jurisdiction",
        relation="operation_definition_jurisdiction_rel",
        string="Jurisdictions",
        help="Intended jurisdiction for operation definition (if applicable).")
    purpose = fields.Text(
        string="Purpose",
        help="Why this operation definition is defined.")
    is_idempotent = fields.Boolean(
        string="Idempotent",
        help="Whether operation causes changes to content.")
    code_id = fields.Many2one(
        comodel_name="hc.vs.operation.definition.code",
        string="Code",
        required="True",
        help="Name used to invoke the operation.")
    comment = fields.Text(
        string="Comment",
        help="Additional information about use.")
    base_id = fields.Many2one(
        comodel_name="hc.res.operation.definition",
        string="Base",
        help="Marks this as a profile of the base.")
    resource_ids = fields.Many2many(
        comodel_name="hc.vs.operation.definition.type",
        relation="operation_definition_resource_rel",
        string="Resources",
        help="Types this operation applies to.")
    is_system = fields.Boolean(
        string="System",
        required="True",
        help="Invoke at the system level?")
    type_ids = fields.Many2many(
        comodel_name="hc.vs.operation.definition.type",
        relation="operation_definition_type_rel",
        string="Types",
        help="Invoke at resource level for these type.")
    is_instance = fields.Boolean(
        string="Instance",
        required="True",
        help="Invoke on an instance?")
    parameter_ids = fields.One2many(
        comodel_name="hc.operation.definition.parameter",
        inverse_name="operation_definition_id",
        string="Parameters",
        help="Parameters for the operation/query.")
    overload_ids = fields.One2many(
        comodel_name="hc.operation.definition.overload",
        inverse_name="operation_definition_id",
        string="Overloads",
        help="For generating overloaded methods in code.")

class OperationDefinitionParameter(models.Model):
    _name = "hc.operation.definition.parameter"
    _description = "Operation Definition Parameter"

    operation_definition_id = fields.Many2one(
        comodel_name="hc.res.operation.definition",
        string="Operation Definition",
        help="Operation Definition associated with this Operation Definition Parameter.")
    name_id = fields.Many2one(
        comodel_name="hc.vs.operation.definition.parameter.name",
        string="Name",
        required="True",
        help="Name of the parameter.")
    use = fields.Selection(
        string="Use",
        required="True",
        selection=[
            ("in", "In"),
            ("out", "Out")],
        help="Whether this is an input or an output parameter.")
    min = fields.Integer(
        string="Min",
        required="True",
        help="Minimum Cardinality.")
    max = fields.Char(
        string="Max",
        required="True",
        help="Maximum Cardinality (a number or *).")
    documentation = fields.Text(
        string="Documentation",
        help="Description of meaning/use.")
    type_id = fields.Many2one(
        comodel_name="hc.vs.fhir.all.type",
        string="Type",
        help="What type this parameter has.")
    profile_id = fields.Many2one(
        comodel_name="hc.res.structure.definition",
        string="Profile",
        help="Profile on the type.")
    part_id = fields.Many2one(
        comodel_name="hc.operation.definition.parameter",
        string="Part",
        help="Parts of a nested Parameter.")
    binding_ids = fields.One2many(
        comodel_name="hc.operation.definition.parameter.binding",
        inverse_name="parameter_id",
        string="Bindings",
        help="ValueSet details if this is coded.")

class OperationDefinitionParameterBinding(models.Model):
    _name = "hc.operation.definition.parameter.binding"
    _description = "Operation Definition Parameter Binding"

    parameter_id = fields.Many2one(
        comodel_name="hc.operation.definition.parameter",
        string="Parameter",
        help="Parameters for the operation/query.")
    strength = fields.Selection(
        string="Strength",
        required="True",
        selection=[
            ("required", "Required"),
            ("extensible", "Extensible"),
            ("preferred", "Preferred"),
            ("example", "Example")],
        help="Indicates the degree of conformance expectations associated with this binding - that is, the degree to which the provided value set must be adhered to in the instances.")
    value_set_type = fields.Selection(
        string="Value Set Type",
        required="True",
        selection=[
            ("uri", "URI"),
            ("value set", "Value Set")],
        help="Type of source of value set.")
    value_set_name = fields.Char(
        string="Value Set",
        compute="_compute_value_set_name",
        store="True",
        help="Source of value set.")
    value_set_uri = fields.Char(
        string="Value Set URI",
        help="URI source of value set.")
    # value_set_id = fields.Many2one(
    #     comodel_name="hc.res.value.set",
    #     string="Value Set",
    #     required="True",
    #     help="Value Set source.")

class OperationDefinitionOverload(models.Model):
    _name = "hc.operation.definition.overload"
    _description = "Operation Definition Overload"

    operation_definition_id = fields.Many2one(
        comodel_name="hc.res.operation.definition",
        string="Operation Definition",
        help="Operation Definition associated with this Operation Definition Overload.")
    parameter_name_ids = fields.One2many(
        comodel_name="hc.operation.definition.overload.parameter.name",
        inverse_name="overload_id",
        string="Parameter Names",
        help="Name of parameter to include in overload.")
    comment = fields.Text(
        string="Comment",
        help="Comments to go on overload.")

class OperationDefinitionContact(models.Model):
    _name = "hc.operation.definition.contact"
    _description = "Operation Definition Contact"
    _inherit = ["hc.basic.association"]
    _inherits = {"hc.contact.detail": "contact_id"}

    contact_id = fields.Many2one(
        comodel_name="hc.contact.detail",
        string="Contact",
        ondelete="restrict",
        required="True",
        help="Contact Detail associated with this Operation Definition Contact.")
    operation_definition_id = fields.Many2one(
        comodel_name="hc.res.operation.definition",
        string="Operation Definition",
        help="Operation Definition associated with this operation definition contact.")

class OperationDefinitionUseContext(models.Model):
    _name = "hc.operation.definition.use.context"
    _description = "Operation Definition Use Context"
    _inherit = ["hc.basic.association", "hc.usage.context"]

    operation_definition_id = fields.Many2one(
        comodel_name="hc.res.operation.definition",
        string="Operation Definition",
        help="Operation Definition associated with this operation definition use context.")

class OperationDefinitionOverloadParameterName(models.Model):
    _name = "hc.operation.definition.overload.parameter.name"
    _description = "Operation Definition Overload Parameter Name"
    _inherit = ["hc.basic.association"]

    overload_id = fields.Many2one(
        comodel_name="hc.operation.definition.overload",
        string="Overload",
        help="Overload associated with this Operation Definition Overload Parameter Name.")
    parameter_name = fields.Char(
        string="Parameter Name",
        help="Parameter Name associated with this Operation Definition Overload Parameter Name.")

class OperationDefinitionCode(models.Model):
    _name = "hc.vs.operation.definition.code"
    _description = "Operation Definition Code"
    _inherit = ["hc.value.set.contains"]

class OperationDefinitionType(models.Model):
    _name = "hc.vs.operation.definition.type"
    _description = "Operation Definition Type"
    _inherit = ["hc.value.set.contains"]

class OperationDefinitionParameterName(models.Model):
    _name = "hc.vs.operation.definition.parameter.name"
    _description = "Operation Definition Parameter Name"
    _inherit = ["hc.value.set.contains"]

# class OperationDefinitionParameterType(models.Model):
#     _name = "hc.vs.operation.definition.parameter.type"
#     _description = "Operation Definition Parameter Type"
#     _inherit = ["hc.value.set.contains"]
