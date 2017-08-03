# -*- coding: utf-8 -*-

from openerp import models, fields, api

class Extension(models.Model):
    _name = "hc.extension"
    _description = "Extension"
    _inherit = ["hc.element"]

    url = fields.Char(
        string="URI",
        required="True",
        help="URI that identifies the meaning of the extension.")
    value_type = fields.Selection(
        string="Value Type",
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
        help="Type of example value (as defined for type).")
    value_name = fields.Char(
        string="Value",
        compute="_compute_value_name",
        store="True",
        help="Value.")
    value_integer = fields.Integer(
        string="Value Integer",
        help="Integer value.")
    value_decimal = fields.Float(
        string="Value Decimal",
        help="Decimal value.")
    value_date_time = fields.Datetime(
        string="Value Date Time",
        help="Date Time value.")
    value_date = fields.Date(
        string="Value Date",
        help="Date value.")
    value_instant = fields.Datetime(
        string="Value Instant",
        help="Instant value.")
    value_string = fields.Char(
        string="Value String",
        help="String value.")
    value_uri = fields.Char(
        string="Value URI",
        help="URI value.")
    value_boolean = fields.Boolean(
        string="Value Boolean",
        help="Boolean value.")
    value_code_id = fields.Many2one(
        comodel_name="hc.vs.extension.code",
        string="Value Code",
        help="Code value.")
    value_markdown = fields.Text(
        string="Value Markdown",
        help="Markdown value.")
    value_base_64_binary = fields.Binary(
        string="Value Base 64 Binary",
        help="Base 64 Binary value.")
    value_coding_id = fields.Many2one(
        comodel_name="hc.vs.extension.code",
        string="Value Coding",
        help="Coding value.")
    value_codeable_concept_id = fields.Many2one(
        comodel_name="hc.vs.extension.code",
        string="Value Codeable Concept",
        help="Codeable Concept value.")
    value_attachment_id = fields.Many2one(
        comodel_name="hc.extension.attachment",
        string="Value Attachment",
        help="Attachment value.")
    value_identifier_id = fields.Many2one(
        comodel_name="hc.extension.identifier",
        string="Value Identifier",
        help="Identifier value.")
    value_quantity = fields.Float(
        string="Value Quantity",
        help="Quantity value.")
    value_quantity_uom_id = fields.Many2one(
        comodel_name="product.uom",
        string="Value Quantity UOM",
        help="Quantity unit of measure.")
    value_range = fields.Char(
        string="Value Range",
        help="Value of Range.")
    value_period = fields.Char(
        string="Value Period",
        help="Value of Period.")
    value_period_uom_id = fields.Many2one(
        comodel_name="product.uom",
        string="Value Period UOM",
        help="Period unit of measure.")
    value_ratio = fields.Float(
        string="Value Ratio",
        help="Ratio of value.")
    value_human_name_id = fields.Many2one(
        comodel_name="hc.extension.human.name",
        string="Value Human Name",
        help="Human Name value.")
    value_address_id = fields.Many2one(
        comodel_name="hc.extension.address",
        string="Value Address",
        help="Address value.")
    value_contact_point_id = fields.Many2one(
        comodel_name="hc.extension.telecom",
        string="Value Contact Point",
        help="Value of Contact Point.")
    value_timing_id = fields.Many2one(
        comodel_name="hc.extension.timing",
        string="Value Timing",
        help="Timing value.")
    value_signature_id = fields.Many2one(
        comodel_name="hc.extension.signature",
        string="Value Signature",
        help="Signature value.")
    value_reference_id = fields.Many2one(
        comodel_name="hc.extension.reference",
        string="Value Reference",
        help="Reference value.")
    value_time = fields.Float(
        string="Value Time",
        help="Time value.")
    value_oid = fields.Char(
        string="Value OID",
        help="OID value.")
    value_id = fields.Char(
        string="Value ID",
        help="ID value.")
    value_unsigned_int = fields.Integer(
        string="Value Unsigned Integer",
        help="Unsigned Integer value.")
    value_positive_int = fields.Integer(
        string="Value Positive Integer",
        help="Positive Integer value.")
    value_annotation_id = fields.Many2one(
        comodel_name="hc.extension.annotation",
        string="Value Annotation",
        help="Annotation value.")
    value_sampled_data_id = fields.Many2one(
        comodel_name="hc.extension.sampled.data",
        string="Value Sampled Data",
        help="Sampled Data value.")
    value_meta_id = fields.Many2one(
        comodel_name="hc.extension.meta",
        string="Value Meta",
        help="Meta value.")

    @api.depends('value_type')
    def _compute_value_name(self):
        for hc_extension in self:
            if hc_extension.value_type == 'integer':
                hc_extension.value_name = str(hc_extension.value_integer)
            elif hc_extension.value_type == 'decimal':
                hc_extension.value_name = str(hc_extension.value_decimal)
            elif hc_extension.value_type == 'date_time':
                hc_extension.value_type = str(hc_extension.value_date_time)
            elif hc_extension.value_type == 'date':
                hc_extension.value_name = str(hc_extension.value_date)
            elif hc_extension.value_type == 'instant':
                hc_extension.value_name = str(hc_extension.value_instant)
            elif hc_extension.value_type == 'string':
                hc_extension.value_name = hc_extension.value_string
            elif hc_extension.value_type == 'uri':
                hc_extension.value_name = hc_extension.value_uri
            elif hc_extension.value_type == 'boolean':
                hc_extension.value_name = hc_extension.value_boolean
            elif hc_extension.value_type == 'code':
                hc_extension.value_name = hc_extension.value_code_id.name
            elif hc_extension.value_type == 'markdown':
                hc_extension.value_name = hc_extension.value_markdown
            elif hc_extension.value_type == 'coding':
                hc_extension.value_name = hc_extension.value_coding_id.name
            elif hc_extension.value_type == 'codeable_concept':
                hc_extension.value_name = hc_extension.value_codeable_concept_id.name
            elif hc_extension.value_type == 'attachment':
                hc_extension.value_name = hc_extension.value_attachment_id.name
            elif hc_extension.value_type == 'identifier':
                hc_extension.value_name = hc_extension.value_identifier_id.name
            elif hc_extension.value_type == 'quantity':
                hc_extension.value_name = str(hc_extension.value_quantity)
            elif hc_extension.value_type == 'range':
                hc_extension.value_name = hc_extension.value_range
            elif hc_extension.value_type == 'period':
                hc_extension.value_name = hc_extension.value_period
            elif hc_extension.value_type == 'ratio':
                hc_extension.value_name = str(hc_extension.value_ratio)
            elif hc_extension.value_type == 'human_name':
                hc_extension.value_name = hc_extension.value_human_name_id.name
            elif hc_extension.value_type == 'address':
                hc_extension.value_name = hc_extension.value_address_id.name
            elif hc_extension.value_type == 'contact_point':
                hc_extension.value_name = hc_extension.value_contact_point_id.name
            elif hc_extension.value_type == 'timing':
                hc_extension.value_name = hc_extension.value_timing_id.name
            elif hc_extension.value_type == 'signature':
                hc_extension.value_name = hc_extension.value_signature_id.name
            elif hc_extension.value_type == 'reference':
                hc_extension.value_name = hc_extension.value_reference_id.display
            elif hc_extension.value_type == 'time':
                hc_extension.value_type = str(hc_extension.value_time)
            elif hc_extension.value_type == 'oid':
                hc_extension.value_name = hc_extension.value_oid
            elif hc_extension.value_type == 'id':
                hc_extension.value_name = hc_extension.value_id
            elif hc_extension.value_type == 'unsigned_int':
                hc_extension.value_type = str(hc_extension.value_unsigned_int)
            elif hc_extension.value_type == 'positive_int':
                hc_extension.value_type = str(hc_extension.value_positive_int)
            elif hc_extension.value_type == 'annotation':
                hc_extension.value_name = hc_extension.value_annotation_id.name
            elif hc_extension.value_type == 'sampled_data':
                hc_extension.value_name = hc_extension.value_sampled_data_id.name
            elif hc_extension.value_type == 'meta':
                hc_extension.value_name = hc_extension.value_meta_id.name

class ExtensionAttachment(models.Model):
    _name = "hc.extension.attachment"
    _description = "Extension Attachment"
    _inherit = ["hc.basic.association", "hc.attachment"]

class ExtensionIdentifier(models.Model):
    _name = "hc.extension.identifier"
    _description = "Extension Identifier"
    _inherit = ["hc.basic.association", "hc.identifier"]

class ExtensionSampledData(models.Model):
    _name = "hc.extension.sampled.data"
    _description = "Extension Sampled Data"
    _inherit = ["hc.basic.association", "hc.sampled.data"]

class ExtensionHumanName(models.Model):
    _name = "hc.extension.human.name"
    _description = "Extension Human Name"
    _inherit = ["hc.human.name.use"]
    _inherits = {"hc.human.name": "name_id"}

    name_id = fields.Many2one(
        comodel_name="hc.human.name",
        string="Name",
        ondelete="restrict",
        required="True",
        help="Name associated with this Extension Human Name.")

class ExtensionAddress(models.Model):
    _name = "hc.extension.address"
    _description = "Extension Address"
    _inherit = ["hc.address.use"]
    _inherits = {"hc.address": "address_id"}

    address_id = fields.Many2one(
        comodel_name="hc.address",
        string="Address",
        ondelete="restrict",
        required="True",
        help="Address associated with this Extension Address.")

class ExtensionTelecom(models.Model):
    _name = "hc.extension.telecom"
    _description = "Extension Telecom"
    _inherit = ["hc.contact.point.use"]
    _inherits = {"hc.contact.point": "telecom_id"}

    telecom_id = fields.Many2one(
        comodel_name="hc.contact.point",
        string="Telecom",
        ondelete="restrict",
        required="True",
        help="Telecom associated with this Extension Telecom.")

class ExtensionTiming(models.Model):
    _name = "hc.extension.timing"
    _description = "Extension Timing"
    _inherit = ["hc.basic.association", "hc.timing"]

class ExtensionReference(models.Model):
    _name = "hc.extension.reference"
    _description = "Extension Reference"
    _inherit = ["hc.basic.association", "hc.reference"]

class ExtensionAnnotation(models.Model):
    _name = "hc.extension.annotation"
    _description = "Extension Annotation"
    _inherit = ["hc.basic.association", "hc.annotation"]

class ExtensionSignature(models.Model):
    _name = "hc.extension.signature"
    _description = "Extension Signature"
    _inherit = ["hc.basic.association", "hc.signature"]

class ExtensionMeta(models.Model):
    _name = "hc.extension.meta"
    _description = "Extension Meta"
    _inherit = ["hc.basic.association", "hc.meta"]

class ExtensionCoding(models.Model):
    _name = "hc.vs.extension.coding"
    _description = "Extension Coding"
    _inherit = ["hc.value.set.contains"]

class ExtensionCodeableConcept(models.Model):
    _name = "hc.vs.extension.codeable.concept"
    _description = "Extension Codeable Concept"
    _inherit = ["hc.value.set.contains"]

class ExtensionCode(models.Model):
    _name = "hc.vs.extension.code"
    _description = "Extension Code"
    _inherit = ["hc.value.set.contains"]

    name = fields.Char(
        string="Name",
        help="Name of this extension code.")
    code = fields.Char(
        string="Code",
        help="Code of this extension code.")
    contains_id = fields.Many2one(
        comodel_name="hc.vs.extension.code",
        string="Contains",
        help="Parent extension code.")

class ExtensionCoding(models.Model):
    _name = "hc.vs.extension.coding"
    _description = "Extension Coding"
    _inherit = ["hc.value.set.contains"]

    name = fields.Char(
        string="Name",
        help="Name of this extension coding.")
    code = fields.Char(
        string="Code",
        help="Code of this extension coding.")
    contains_id = fields.Many2one(
        comodel_name="hc.vs.extension.coding",
        string="Contains",
        help="Parent extension coding.")

class ExtensionCodeableConcept(models.Model):
    _name = "hc.vs.extension.codeable.concept"
    _description = "Extension Codeable Concept"
    _inherit = ["hc.value.set.contains"]

    name = fields.Char(
        string="Name",
        help="Name of this extension codeable concept.")
    code = fields.Char(
        string="Code",
        help="Code of this extension codeable concept.")
    contains_id = fields.Many2one(
        comodel_name="hc.vs.extension.codeable.concept",
        string="Contains",
        help="Parent extension codeable concept.")

# External reference

class ElementExtension(models.Model):
    _inherit = ["hc.extension"]
