# -*- coding: utf-8 -*-

from openerp import models, fields, api
from datetime import datetime
from openerp.tools import DEFAULT_SERVER_DATETIME_FORMAT as DTF

class StructureMap(models.Model):
    _name = "hc.res.structure.map"
    _description = "Structure Map"
    _inherit = ["hc.domain.resource"]
    _rec_name = "name"

    url = fields.Char(
        string="URL",
        required="True",
        help="Absolute URL used to reference this StructureMap.")
    identifier_ids = fields.One2many(
        comodel_name="hc.structure.map.identifier",
        inverse_name="structure_map_id",
        string="Identifiers",
        help="Other identifiers for the StructureMap.")
    version = fields.Char(
        string="Version",
        help="Logical id for this version of the StructureMap.")
    name = fields.Char(
        string="Name",
        required="True",
        help="Name for this structure map (Computer friendly).")
    title = fields.Char(
        string="Title",
        help="Name for this structure map (Human friendly).")
    status = fields.Selection(
        string="Status",
        required="True",
        selection=[
            ("draft", "Draft"),
            ("active", "Active"),
            ("retired", "Retired")],
        help="The status of the StructureMap.")
    status_history_ids = fields.One2many(
        comodel_name="hc.structure.map.status.history",
        inverse_name="structure_map_id",
        string="Status History",
        help="The status of the structure map over time.")
    is_experimental = fields.Boolean(
        string="Experimental",
        help="If for testing purposes, not real usage.")
    date = fields.Datetime(
        string="Date",
        help="Date for this version of the StructureMap.")
    publisher = fields.Char(
        string="Publisher",
        help="Name of the publisher (Organization or individual).")
    contact_ids = fields.One2many(
        comodel_name="hc.structure.map.contact",
        inverse_name="structure_map_id",
        string="Contacts",
        help="Contact details for the publisher.")
    description = fields.Text(
        string="Description",
        help="Natural language description of the Structure Map.")
    use_context_ids = fields.One2many(
        comodel_name="hc.structure.map.use.context",
        inverse_name="structure_map_id",
        string="Use Contexts",
        help="Content intends to support these contexts.")
    jurisdiction_ids = fields.Many2many(
        comodel_name="hc.vs.jurisdiction",
        relation="structure_map_jurisdiction_rel",
        string="Jurisdictions",
        help="Intended jurisdiction for structure map (if applicable).")
    purpose = fields.Text(
        string="Purpose",
        help="Why this structure map is defined.")
    copyright = fields.Text(
        string="Copyright",
        help="Use and/or publishing restrictions.")
    structure_ids = fields.One2many(
        comodel_name="hc.structure.map.structure",
        inverse_name="structure_map_id",
        string="Structures",
        help="Structure Definition used by this map.")
    import_ids = fields.One2many(
        comodel_name="hc.structure.map.import",
        inverse_name="structure_map_id",
        string="Import URIs",
        help="URI of other maps used by this map (canonical urls).")
    group_ids = fields.One2many(
        comodel_name="hc.structure.map.group",
        inverse_name="structure_map_id",
        string="Groups",
        required="True",
        help="Named sections for reader convenience.")

    @api.model
    def create(self, vals):
        status_history_obj = self.env['hc.structure.map.status.history']
        res = super(StructureMap, self).create(vals)
        if vals and vals.get('status'):
            status_history_vals = {
                'structure_map_id': res.id,
                'status': res.status,
                'start_date': datetime.today()
                }
            status_history_obj.create(status_history_vals)
        return res

    @api.multi
    def write(self, vals):
        status_history_obj = self.env['hc.structure.map.status.history']
        res = super(StructureMap, self).write(vals)
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
                    'structure_map_id': self.id,
                    'status': vals.get('status'),
                    'start_date': datetime.today()
                    }
                status_history_obj.create(status_history_vals)
        return res

class StructureMapStructure(models.Model):
    _name = "hc.structure.map.structure"
    _description = "Structure Map Structure"
    _inherit = "hc.backbone.element"

    structure_map_id = fields.Many2one(
        comodel_name="hc.res.structure.map",
        string="Structure Map",
        help="Structure Map associated with this Structure Map Structure.")
    url = fields.Char(
        string="URL",
        required="True",
        help="Canonical URL for structure definition.")
    mode = fields.Selection(
        string="Mode",
        required="True",
        selection=[
            ("source", "Source"),
            ("queried", "Queried"),
            ("target", "Target"),
            ("produced", "Produced")],
        help="How the referenced structure is used in this mapping.")
    documentation = fields.Text(
        string="Documentation",
        help="Documentation on use of structure.")

class StructureMapGroup(models.Model):
    _name = "hc.structure.map.group"
    _description = "Structure Map Group"
    _inherit = "hc.backbone.element"

    structure_map_id = fields.Many2one(
        comodel_name="hc.res.structure.map",
        string="Structure Map",
        help="Structure Map associated with this Structure Map Group.")
    name = fields.Char(
        string="Name",
        required="True",
        help="Descriptive name for a user.")
    extends = fields.Char(
        string="Extends",
        help="Another group that this group adds rules to.")
    type_mode = fields.Selection(
        string="Type Mode",
        required="True",
        selection=[
            ("none", "None"),
            ("types", "Types"),
            ("types-and-types", "Types and Types")],
        help="If this is the default, rule set to apply for this source type or this combination of types.")
    documentation = fields.Text(
        string="Documentation",
        help="Additional description/explaination for group.")
    input_ids = fields.One2many(
        comodel_name="hc.structure.map.group.input",
        inverse_name="group_id",
        string="Inputs",
        required="True",
        help="Named instance provided when invoking the map.")
    rule_ids = fields.One2many(
        comodel_name="hc.structure.map.group.rule",
        inverse_name="group_id",
        string="Rules",
        required="True",
        help="Transform Rule from source to target.")

class StructureMapGroupInput(models.Model):
    _name = "hc.structure.map.group.input"
    _description = "Structure Map Group Input"
    _inherit = "hc.backbone.element"

    group_id = fields.Many2one(
        comodel_name="hc.structure.map.group",
        string="Group",
        help="Group associated with this Structure Map Group Input.")
    name = fields.Char(
        string="Name",
        required="True",
        help="Name for this instance of data.")
    type = fields.Char(
        string="Type",
        help="Type for this instance of data.")
    mode = fields.Selection(
        string="Mode",
        required="True",
        selection=[
            ("source", "Source"),
            ("target", "Target")],
        help="Mode for this instance of data.")
    documentation = fields.Text(
        string="Documentation",
        help="Documentation for this instance of data.")

class StructureMapGroupRule(models.Model):
    _name = "hc.structure.map.group.rule"
    _description = "Structure Map Group Rule"
    _inherit = "hc.backbone.element"

    group_id = fields.Many2one(
        comodel_name="hc.structure.map.group",
        string="Group",
        help="Group associated with this Structure Map Group Rule.")
    name = fields.Char(
        string="Name",
        required="True",
        help="Name of the rule for internal references.")
    source_ids = fields.One2many(
        comodel_name="hc.structure.map.group.rule.source",
        inverse_name="rule_id",
        string="Sources",
        required="True",
        help="Source inputs to the mapping.")
    target_ids = fields.One2many(
        comodel_name="hc.structure.map.group.rule.target",
        inverse_name="rule_id",
        string="Targets",
        help="Content to create because of this mapping rule.")
    rule_ids = fields.One2many(
        comodel_name="hc.structure.map.group.rule.rule",
        inverse_name="rule_id",
        string="Rules",
        help="Rules contained in this rule.")
    dependent_ids = fields.One2many(
        comodel_name="hc.structure.map.group.rule.dependent",
        inverse_name="rule_id",
        string="Dependents",
        help="Which other rules to apply in the context of this rule.")
    documentation = fields.Text(
        string="Documentation",
        help="Documentation for this instance of data.")

class StructureMapGroupRuleSource(models.Model):
    _name = "hc.structure.map.group.rule.source"
    _description = "Structure Map Group Rule Source"
    _inherit = "hc.backbone.element"

    rule_id = fields.Many2one(
        comodel_name="hc.structure.map.group.rule",
        string="Rule",
        help="Rule associated with this Structure Map Group Rule Source.")
    context = fields.Char(
        string="Context",
        required="True",
        help="Type or variable this rule applies to.")
    min = fields.Integer(
        string="Min",
        help="Specified minimum cardinality.")
    max = fields.Char(
        string="Max",
        help="Specified maximum cardinality (number or *).")
    type = fields.Char(
        string="Type",
        help="Rule only applies if source has this type.")
    default_value_type = fields.Selection(
        string="Default Value Type",
        selection=[
            ("integer", "Integer"),
            ("decimal", "Decimal"),
            ("date_time", "Date Time"),
            ("date", "Date"),
            ("instant", "Instant"),
            ("string", "String"),
            ("uri", "URI"),
            ("boolean", "Boolean"),
            ("code", "Code"),
            ("markdown", "Markdown"),
            ("base_64_binary", "Base 64 Binary"),
            ("coding", "Coding"),
            ("codeable_concept", "Codeable Concept"),
            ("attachment", "Attachment"),
            ("identifier", "Identifier"),
            ("quantity", "Quantity"),
            ("range", "Range"),
            ("period", "Period"),
            ("ratio", "Ratio"),
            ("human_name", "Human Name"),
            ("address", "Address"),
            ("contact_point", "Contact Point"),
            ("timing", "Timing"),
            ("signature", "Signature"),
            ("reference", "Reference"),
            ("time", "Time"),
            ("oid", "OID"),
            ("id", "ID"),
            ("unsigned_int", "Unsigned Integer"),
            ("positive_int", "Positive Integer"),
            ("annotation", "Annotation"),
            ("sampled_data", "Sampled Data"),
            ("meta", "Meta")],
        help="Type of specified default value if no value exists.")
    default_value_name = fields.Char(
        string="Default Value",
        compute="_compute_default_value_name",
        store="True",
        help="Specified default value if no value exists.")
    default_value_integer = fields.Integer(
        string="Default Value Integer",
        help="Integer default value if no value exists.")
    default_value_decimal = fields.Float(
        string="Default Value Decimal",
        help="Decimal default value if no value exists.")
    default_value_date_time = fields.Datetime(
        string="Default Value Date Time",
        help="Date Time default value if no value exists.")
    default_value_date = fields.Date(
        string="Default Value Date",
        help="Date default value if no value exists.")
    default_value_instant = fields.Datetime(
        string="Default Value Instant",
        help="Instant default value if no value exists.")
    default_value_string = fields.Char(
        string="Default Value String",
        help="String default value if no value exists.")
    default_value_uri = fields.Char(
        string="Default Value URI",
        help="URI default value if no value exists.")
    default_value_boolean = fields.Boolean(
        string="Default Value Boolean",
        help="Boolean default value if no value exists.")
    default_value_code_id = fields.Many2one(
        comodel_name="hc.vs.structure.map.code",
        string="Default Value Code",
        help="Code default value if no value exists.")
    default_value_markdown = fields.Text(
        string="Default Value Markdown",
        help="Markdown default value if no value exists.")
    default_value_base_64_binary = fields.Binary(
        string="Default Value Base 64 Binary",
        help="Base 64 Binary default value if no value exists.")
    default_value_coding_id = fields.Many2one(
        comodel_name="hc.vs.structure.map.code",
        string="Default Value Coding",
        help="Coding default value if no value exists.")
    default_value_codeable_concept_id = fields.Many2one(
        comodel_name="hc.vs.structure.map.code",
        string="Default Value Codeable Concept",
        help="Codeable Concept default value if no value exists.")
    default_value_attachment_id = fields.Many2one(
        comodel_name="hc.structure.map.attachment",
        string="Default Value Attachment",
        help="Attachment default value if no value exists.")
    default_value_identifier_id = fields.Many2one(
        comodel_name="hc.structure.map.identifier",
        string="Default Value Identifier",
        help="Identifier default value if no value exists.")
    default_value_quantity = fields.Float(
        string="Default Value Quantity",
        help="Quantity default value if no value exists.")
    default_value_quantity_uom_id = fields.Many2one(
        comodel_name="product.uom",
        string="Default Value Quantity UOM",
        help="Quantity unit of measure.")
    default_value_range = fields.Char(
        string="Default Value Range",
        help="Range default value if no value exists.")
    default_value_period = fields.Char(
        string="Default Value Period",
        help="Period default value if no value exists.")
    default_value_period_uom_id = fields.Many2one(
        comodel_name="product.uom",
        string="Default Value Period UOM",
        help="Period unit of measure.")
    default_value_ratio = fields.Float(
        string="Default Value Ratio",
        help="Ratio of default value if no value exists.")
    default_value_human_name_id = fields.Many2one(
        comodel_name="hc.structure.map.human.name",
        string="Default Value Human Name",
        help="Human Name default value if no value exists.")
    default_value_address_id = fields.Many2one(
        comodel_name="hc.structure.map.address",
        string="Default Value Address",
        help="Address default value if no value exists.")
    default_value_contact_point_id = fields.Many2one(
        comodel_name="hc.structure.map.telecom",
        string="Default Value Contact Point",
        help="Contact Point default value if no value exists.")
    default_value_timing_id = fields.Many2one(
        comodel_name="hc.structure.map.timing",
        string="Default Value Timing",
        help="Timing default value if no value exists.")
    default_value_signature_id = fields.Many2one(
        comodel_name="hc.structure.map.signature",
        string="Default Value Signature",
        help="Signature default value if no value exists.")
    default_value_reference_id = fields.Many2one(
        comodel_name="hc.structure.map.reference",
        string="Default Value Reference",
        help="Reference default value if no value exists.")
    default_value_time = fields.Float(
        string="Default Value Time",
        help="Time default value if no value exists.")
    default_value_oid = fields.Char(
        string="Default Value OID",
        help="OID default value if no value exists.")
    default_value_id = fields.Char(
        string="Default Value ID",
        help="ID default value if no value exists.")
    default_value_unsigned_int = fields.Integer(
        string="Default Value Unsigned Integer",
        help="Unsigned Integer default value if no value exists.")
    default_value_positive_int = fields.Integer(
        string="Default Value Positive Integer",
        help="Positive Integer default value if no value exists.")
    default_value_annotation_id = fields.Many2one(
        comodel_name="hc.structure.map.annotation",
        string="Default Value Annotation",
        help="Annotation default value if no value exists.")
    default_value_sampled_data_id = fields.Many2one(
        comodel_name="hc.structure.map.sampled.data",
        string="Default Value Sampled Data",
        help="Sampled Data default value if no value exists.")
    default_value_meta_id = fields.Many2one(
        comodel_name="hc.structure.map.meta",
        string="Default Value Meta",
        help="Meta default value if no value exists.")
    element = fields.Char(
        string="Element",
        help="Optional field for this source.")
    list_mode = fields.Selection(
        string="List Mode",
        selection=[
            ("first", "First"),
            ("not_first", "Not First"),
            ("last", "Last"),
            ("not_last", "Not Last"),
            ("only_one", "Only One")],
        help="If field is a list, how to manage the list.")
    variable = fields.Char(
        string="Variable",
        help="Named context for field, if a field is specified.")
    condition = fields.Char(
        string="Condition",
        help="FluentPath expression - must be true or the rule does not apply.")
    check = fields.Char(
        string="Check",
        help="FluentPath expression - must be true or the mapping engine throws an error instead of completing.")

    @api.depends('default_value_type')
    def _compute_default_value_name(self):
        for hc_structure_map_group_rule_source in self:
            if hc_structure_map_group_rule_source.default_value_type == 'integer':
                hc_structure_map_group_rule_source.default_value_name = str(hc_structure_map_group_rule_source.default_value_integer)
            elif hc_structure_map_group_rule_source.default_value_type == 'decimal':
                hc_structure_map_group_rule_source.default_value_name = str(hc_structure_map_group_rule_source.default_value_decimal)
            elif hc_structure_map_group_rule_source.default_value_type == 'date_time':
                hc_structure_map_group_rule_source.default_value_type = str(hc_structure_map_group_rule_source.default_value_date_time)
            elif hc_structure_map_group_rule_source.default_value_type == 'date':
                hc_structure_map_group_rule_source.default_value_name = str(hc_structure_map_group_rule_source.default_value_date)
            elif hc_structure_map_group_rule_source.default_value_type == 'instant':
                hc_structure_map_group_rule_source.default_value_name = str(hc_structure_map_group_rule_source.default_value_instant)
            elif hc_structure_map_group_rule_source.default_value_type == 'string':
                hc_structure_map_group_rule_source.default_value_name = hc_structure_map_group_rule_source.default_value_string
            elif hc_structure_map_group_rule_source.default_value_type == 'uri':
                hc_structure_map_group_rule_source.default_value_name = hc_structure_map_group_rule_source.default_value_uri
            elif hc_structure_map_group_rule_source.default_value_type == 'boolean':
                hc_structure_map_group_rule_source.default_value_name = hc_structure_map_group_rule_source.default_value_boolean
            elif hc_structure_map_group_rule_source.default_value_type == 'code':
                hc_structure_map_group_rule_source.default_value_name = hc_structure_map_group_rule_source.default_value_code_id.name
            elif hc_structure_map_group_rule_source.default_value_type == 'markdown':
                hc_structure_map_group_rule_source.default_value_name = hc_structure_map_group_rule_source.default_value_markdown
            elif hc_structure_map_group_rule_source.default_value_type == 'coding':
                hc_structure_map_group_rule_source.default_value_name = hc_structure_map_group_rule_source.default_value_coding_id.name
            elif hc_structure_map_group_rule_source.default_value_type == 'codeable_concept':
                hc_structure_map_group_rule_source.default_value_name = hc_structure_map_group_rule_source.default_value_codeable_concept_id.name
            elif hc_structure_map_group_rule_source.default_value_type == 'attachment':
                hc_structure_map_group_rule_source.default_value_name = hc_structure_map_group_rule_source.default_value_attachment_id.name
            elif hc_structure_map_group_rule_source.default_value_type == 'identifier':
                hc_structure_map_group_rule_source.default_value_name = hc_structure_map_group_rule_source.default_value_identifier_id.name
            elif hc_structure_map_group_rule_source.default_value_type == 'quantity':
                hc_structure_map_group_rule_source.default_value_name = str(hc_structure_map_group_rule_source.default_value_quantity)
            elif hc_structure_map_group_rule_source.default_value_type == 'range':
                hc_structure_map_group_rule_source.default_value_name = hc_structure_map_group_rule_source.default_value_range
            elif hc_structure_map_group_rule_source.default_value_type == 'period':
                hc_structure_map_group_rule_source.default_value_name = hc_structure_map_group_rule_source.default_value_period
            elif hc_structure_map_group_rule_source.default_value_type == 'ratio':
                hc_structure_map_group_rule_source.default_value_name = str(hc_structure_map_group_rule_source.default_value_ratio)
            elif hc_structure_map_group_rule_source.default_value_type == 'human_name':
                hc_structure_map_group_rule_source.default_value_name = hc_structure_map_group_rule_source.default_value_human_name_id.name
            elif hc_structure_map_group_rule_source.default_value_type == 'address':
                hc_structure_map_group_rule_source.default_value_name = hc_structure_map_group_rule_source.default_value_address_id.name
            elif hc_structure_map_group_rule_source.default_value_type == 'contact_point':
                hc_structure_map_group_rule_source.default_value_name = hc_structure_map_group_rule_source.default_value_contact_point_id.name
            elif hc_structure_map_group_rule_source.default_value_type == 'timing':
                hc_structure_map_group_rule_source.default_value_name = hc_structure_map_group_rule_source.default_value_timing_id.name
            elif hc_structure_map_group_rule_source.default_value_type == 'signature':
                hc_structure_map_group_rule_source.default_value_name = hc_structure_map_group_rule_source.default_value_signature_id.name
            elif hc_structure_map_group_rule_source.default_value_type == 'reference':
                hc_structure_map_group_rule_source.default_value_name = hc_structure_map_group_rule_source.default_value_reference_id.name
            elif hc_structure_map_group_rule_source.default_value_type == 'time':
                hc_structure_map_group_rule_source.default_value_type = str(hc_structure_map_group_rule_source.default_value_time)
            elif hc_structure_map_group_rule_source.default_value_type == 'oid':
                hc_structure_map_group_rule_source.default_value_name = hc_structure_map_group_rule_source.default_value_oid
            elif hc_structure_map_group_rule_source.default_value_type == 'id':
                hc_structure_map_group_rule_source.default_value_name = hc_structure_map_group_rule_source.default_value_id
            elif hc_structure_map_group_rule_source.default_value_type == 'unsigned_int':
                hc_structure_map_group_rule_source.default_value_type = str(hc_structure_map_group_rule_source.default_value_unsigned_int)
            elif hc_structure_map_group_rule_source.default_value_type == 'positive_int':
                hc_structure_map_group_rule_source.default_value_type = str(hc_structure_map_group_rule_source.default_value_positive_int)
            elif hc_structure_map_group_rule_source.default_value_type == 'annotation':
                hc_structure_map_group_rule_source.default_value_name = hc_structure_map_group_rule_source.default_value_annotation_id.name
            elif hc_structure_map_group_rule_source.default_value_type == 'sampled_data':
                hc_structure_map_group_rule_source.default_value_name = hc_structure_map_group_rule_source.default_value_sampled_data_id.name
            elif hc_structure_map_group_rule_source.default_value_type == 'meta':
                hc_structure_map_group_rule_source.default_value_name = hc_structure_map_group_rule_source.default_value_meta_id.name

class StructureMapGroupRuleTarget(models.Model):
    _name = "hc.structure.map.group.rule.target"
    _description = "Structure Map Group Rule Target"
    _inherit = "hc.backbone.element"

    rule_id = fields.Many2one(
        comodel_name="hc.structure.map.group.rule",
        string="Rule",
        help="Rule associated with this Structure Map Group Rule Target.")
    context = fields.Char(
        string="Context",
        required="True",
        help="Type or variable this rule applies to.")
    context_type = fields.Selection(
        string="Context Type",
        required="True",
        selection=[
            ("type", "Type"),
            ("variable", "Variable")],
        help="How to interpret the context.")
    element = fields.Char(
        string="Element",
        help="Field to create in the context.")
    variable = fields.Char(
        string="Variable",
        help="Named context for field, if desired, and a field is specified.")
    list_mode_ids = fields.One2many(
        comodel_name="hc.structure.map.group.rule.target.list.mode",
        inverse_name="target_id",
        string="List Modes",
        help="If field is a list, how to manage the list.")
    list_rule_id = fields.Char(
        string="List Rule Id",
        help="Internal rule reference for shared list items.")
    transform = fields.Selection(
        string="Transform",
        selection=[
            ("create", "Create"),
            ("copy", "Copy"),
            ("evaluate", "Evaluate")],
        help="How the data is copied / created.")
    parameter_ids = fields.One2many(
        comodel_name="hc.structure.map.group.rule.target.parameter",
        inverse_name="target_id",
        string="Parameters",
        help="Parameters to the transform.")

class StructureMapGroupRuleRule(models.Model):
    _name = "hc.structure.map.group.rule.rule"
    _description = "Structure Map Group Rule Rule"

    rule_id = fields.Many2one(
        comodel_name="hc.structure.map.group.rule",
        string="Rule",
        help="Rule associated with this Structure Map Group Rule Rule.")
    rule_rule_id = fields.Many2one(
        comodel_name="hc.structure.map.group.rule",
        string="Associated Rule",
        help="Associated Rule associated with this Rule.")

class StructureMapGroupRuleDependent(models.Model):
    _name = "hc.structure.map.group.rule.dependent"
    _description = "Structure Map Group Rule Dependent"
    _inherit = "hc.backbone.element"

    rule_id = fields.Many2one(
        comodel_name="hc.structure.map.group.rule",
        string="Rule",
        help="Rule associated with this Structure Map Group Rule Dependent.")
    name = fields.Char(
        string="Name",
        required="True",
        help="Name of a rule or group to apply.")
    variable = fields.Char(
        string="Variable",
        required="True",
        help="Names of variables to pass to the rule or group.")

class StructureMapIdentifier(models.Model):
    _name = "hc.structure.map.identifier"
    _description = "Structure Map Identifier"
    _inherit = ["hc.basic.association", "hc.identifier", "hc.identifier.use"]

    structure_map_id = fields.Many2one(
        comodel_name="hc.res.structure.map",
        string="Structure Map",
        help="Structure Map associated with this Structure Map Identifier.")

class StructureMapStatusHistory(models.Model):
    _name = "hc.structure.map.status.history"
    _description = "Structure Map Status History"

    structure_map_id = fields.Many2one(
        comodel_name="hc.res.structure.map",
        string="Structure Map",
        help="Structure Map associated with this Structure Map Status History.")
    status = fields.Char(
        string="Status",
        help="The status of the structure map.")
    start_date = fields.Datetime(
        string="Start Date",
        help="Start of the period during which this structure map status is valid.")
    end_date = fields.Datetime(
        string="End Date",
        help="End of the period during which this structure map status is valid.")
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

class StructureMapContact(models.Model):
    _name = "hc.structure.map.contact"
    _description = "Structure Map Contact"
    _inherit = ["hc.basic.association"]
    _inherits = {"hc.contact.detail": "contact_id"}

    contact_id = fields.Many2one(
        comodel_name="hc.contact.detail",
        string="Contact",
        ondelete="restrict",
        required="True",
        help="Contact Detail associated with this Structure Map Contact.")
    structure_map_id = fields.Many2one(
        comodel_name="hc.res.structure.map",
        string="Structure Map",
        help="Structure Map associated with this Structure Map Contact.")

class StructureMapImport(models.Model):
    _name = "hc.structure.map.import"
    _description = "Structure Map Import"
    _inherit = ["hc.basic.association"]

    structure_map_id = fields.Many2one(
        comodel_name="hc.res.structure.map",
        string="Structure Map",
        help="Structure Map associated with this Structure Map Import.")
    import_uri = fields.Char(
        string="Import URI",
        help="URI of other maps used by this map (canonical URLs).")

class StructureMapUseContext(models.Model):
    _name = "hc.structure.map.use.context"
    _description = "Structure Map Use Context"
    _inherit = ["hc.basic.association", "hc.usage.context"]

    structure_map_id = fields.Many2one(
        comodel_name="hc.res.structure.map",
        string="Structure Map",
        help="Structure Map associated with this Structure Map Use Context.")

class StructureMapGroupRuleTargetListMode(models.Model):
    _name = "hc.structure.map.group.rule.target.list.mode"
    _description = "Structure Map Group Rule Target List Mode"
    _inherit = ["hc.basic.association"]

    target_id = fields.Many2one(
        comodel_name="hc.structure.map.group.rule.target",
        string="Target",
        help="Target associated with this Structure Map Group Rule Target List Mode.")
    list_mode = fields.Selection(
        string="List Mode",
        selection=[
            ("first", "First"),
            ("share", "Share"),
            ("last", "Last"),
            ("collate", "Collate")],
        help="If field is a list, how to manage the list.")

class StructureMapGroupRuleTargetParameter(models.Model):
    _name = "hc.structure.map.group.rule.target.parameter"
    _description = "Structure Map Group Rule Target Parameter"
    _inherit = "hc.backbone.element"

    target_id = fields.Many2one(
        comodel_name="hc.structure.map.group.rule.target",
        string="Target",
        help="Target associated with this Structure Map Group Rule Target Parameter.")
    value_type = fields.Selection(
        string="Value Type",
        required="True",
        selection=[
            ("id", "Id"),
            ("string", "String"),
            ("boolean", "Boolean"),
            ("integer", "Integer"),
            ("decimal", "Decimal")],
            help="Type of parameter value.")
    value_name = fields.Char(
        string="Value",
        compute="_compute_value_name",
        store="True",
        help="Parameter value - variable or literal.")
    value_id = fields.Char(
        string="Value Id",
        help="Id parameter value.")
    value_string = fields.Char(
        string="Value String",
        help="String parameter value.")
    value_boolean = fields.Boolean(
        string="Value Boolean",
        help="Boolean parameter value.")
    value_integer = fields.Integer(
        string="Value Integer",
        help="Integer parameter value.")
    value_decimal = fields.Float(
        string="Value Decimal",
        help="Decimal parameter value.")

    @api.depends('value_type')
    def _compute_value_name(self):
        for hc_structure_map_group_rule_target_parameter in self:
            if hc_structure_map_group_rule_target_parameter.value_type == 'id':
                hc_structure_map_group_rule_target_parameter.value_name = hc_structure_map_group_rule_target_parameter.value_id
            elif hc_structure_map_group_rule_target_parameter.value_type == 'string':
                hc_structure_map_group_rule_target_parameter.value_name = hc_structure_map_group_rule_target_parameter.value_string
            elif hc_structure_map_group_rule_target_parameter.value_type == 'boolean':
                hc_structure_map_group_rule_target_parameter.value_name = hc_structure_map_group_rule_target_parameter.value_boolean
            elif hc_structure_map_group_rule_target_parameter.value_type == 'integer':
                hc_structure_map_group_rule_target_parameter.value_name = str(hc_structure_map_group_rule_target_parameter.value_integer)
            elif hc_structure_map_group_rule_target_parameter.value_type == 'decimal':
                hc_structure_map_group_rule_target_parameter.value_name = str(hc_structure_map_group_rule_target_parameter.value_decimal)

class StructureMapAddress(models.Model):
    _name = "hc.structure.map.address"
    _description = "Structure Map Address"
    _inherit = ["hc.address.use"]
    _inherits = {"hc.address": "address_id"}

    address_id = fields.Many2one(
        comodel_name="hc.address",
        string="Address",
        ondelete="restrict",
        required="True",
        help="Address associated with this Structure Map Address.")

class StructureMapAnnotation(models.Model):
    _name = "hc.structure.map.annotation"
    _description = "Structure Map Annotation"
    _inherit = ["hc.basic.association", "hc.annotation"]

class StructureMapAttachment(models.Model):
    _name = "hc.structure.map.attachment"
    _description = "Structure Map Attachment"
    _inherit = ["hc.basic.association", "hc.attachment"]

class StructureMapTelecom(models.Model):
    _name = "hc.structure.map.telecom"
    _description = "Structure Map Telecom"
    _inherit = ["hc.contact.point.use"]
    _inherits = {"hc.contact.point": "telecom_id"}

    telecom_id = fields.Many2one(
        comodel_name="hc.contact.point",
        string="Telecom",
        ondelete="restrict",
        required="True",
        help="Telecom associated with this Structure Map Telecom.")

class StructureMapHumanName(models.Model):
    _name = "hc.structure.map.human.name"
    _description = "Structure Map Human Name"
    _inherit = ["hc.human.name.use"]
    _inherits = {"hc.human.name": "name_id"}

    name_id = fields.Many2one(
        comodel_name="hc.human.name",
        string="Name",
        ondelete="restrict",
        required="True",
        help="Name associated with this Structure Map Human Name.")

class StructureMapMeta(models.Model):
    _name = "hc.structure.map.meta"
    _description = "Structure Map Meta"
    _inherit = ["hc.basic.association", "hc.meta"]

class StructureMapReference(models.Model):
    _name = "hc.structure.map.reference"
    _description = "Structure Map Reference"
    _inherit = ["hc.basic.association", "hc.reference"]

class StructureMapSampledData(models.Model):
    _name = "hc.structure.map.sampled.data"
    _description = "Structure Map Sampled Data"
    _inherit = ["hc.basic.association", "hc.sampled.data"]

class StructureMapSignature(models.Model):
    _name = "hc.structure.map.signature"
    _description = "Structure Map Signature"
    _inherit = ["hc.basic.association", "hc.signature"]

class StructureMapTiming(models.Model):
    _name = "hc.structure.map.timing"
    _description = "Structure Map Timing"
    _inherit = ["hc.basic.association", "hc.timing"]

class StructureMapCode(models.Model):
    _name = "hc.vs.structure.map.code"
    _description = "Structure Map Code"
    _inherit = ["hc.value.set.contains"]

    name = fields.Char(
        string="Name",
        help="Name of this structure map code.")
    code = fields.Char(
        string="Code",
        help="Code of this structure map code.")
    contains_id = fields.Many2one(
        comodel_name="hc.vs.structure.map.code",
        string="Parent",
        help="Parent structure map code.")
