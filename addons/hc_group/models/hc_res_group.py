# -*- coding: utf-8 -*-

from openerp import models, fields, api

class Group(models.Model):
    _name = "hc.res.group"
    _description = "Group"

    identifier_ids = fields.One2many(
        comodel_name="hc.group.identifier",
        inverse_name="group_id",
        string="Identifiers",
        help="Unique id.")
    type = fields.Selection(
        string="Type",
        required="True",
        selection=[
            ("person", "Person"),
            ("animal", "Animal"),
            ("practitioner", "Practitioner"),
            ("device", "Device"),
            ("medication", "Medication"),
            ("substance", "Substance")],
        help="Identifies the broad classification of the kind of resources the group includes.")
    is_actual = fields.Boolean(
        string="Actual",
        default="True",
        help="Descriptive or actual.")
    is_active = fields.Boolean(
        string="Active",
        default="True",
        help="Whether this group's record is in active use.")
    code_id = fields.Many2one(
        comodel_name="hc.vs.group.code",
        string="Code",
        help="Kind of Group members.")
    name = fields.Char(
        string="Name",
        help="Label for Group.")
    quantity = fields.Integer(
        string="Quantity",
        help="Number of members.")
    characteristic_ids = fields.One2many(
        comodel_name="hc.group.characteristic",
        inverse_name="group_id",
        string="Characteristics",
        help="Trait of group members.")
    member_ids = fields.One2many(
        comodel_name="hc.group.member",
        inverse_name="group_id",
        string="Members",
        help="Who or what is in group.")

class GroupCharacteristic(models.Model):
    _name = "hc.group.characteristic"
    _description = "Group Characteristic"

    group_id = fields.Many2one(
        comodel_name="hc.res.group",
        string="Group",
        required="True",
        help="Group associated with this characteristic.")
    code_id = fields.Many2one(
        comodel_name="hc.vs.group.characteristic.code",
        string="Code",
        required="True",
        help="Kind of trait being asserted (e.g., gender, age, owner, location, etc.).")
    value_type = fields.Selection(
        string="Value Type",
        required="True",
        widget="selection",
        selection=[
            ("code", "Code"),
            ("boolean", "Boolean"),
            ("quantity", "Quantity"),
            ("range", "Range")],
        help="Type of value held by characteristic.")
    value_name = fields.Char(
        string="Value",
        help="Value held by characteristic.")
    value_code_id = fields.Many2one(
        comodel_name="hc.vs.group.characteristic.value",
        string="Value Code",
        help="Code of value held by characteristic.")
    value_boolean = fields.Boolean(
        string="Value Boolean",
        help="Boolean value held by characteristic.")
    value_quantity = fields.Float(
        string="Value Quantity",
        help="Quantity value held by characteristic.")
    value_quantity_uom_id = fields.Many2one(
        comodel_name="product.uom",
        string="Value Quantity UOM",
        help="Value Quantity unit of measure.")
    value_low_limit = fields.Float(
        string="Value Low Limit",
        help="Low limit of value held by characteristic.")
    value_high_limit = fields.Float(
        string="Value High Limit",
        help="High limit of value held by characteristic.")
    exclude = fields.Boolean(
        string="Exclude",
        help="Group includes or excludes this characteristic.")
    period_start_date = fields.Datetime(
        string="Period Start Date",
        help="Start of the period over which characteristic is tested.")
    period_end_date = fields.Datetime(
        string="Period End Date",
        help="End of the period over which characteristic is tested.")

class GroupMember(models.Model):
    _name = "hc.group.member"
    _description = "Group Member"

    group_id = fields.Many2one(
        comodel_name="hc.res.group",
        string="Group",
        required="True",
        help="Group associated with this member.")
    entity_type = fields.Selection(
        string="Type",
        required="True",
        selection=[
            ("patient", "Patient"),
            ("practitioner", "Practitioner"),
            ("device", "Device"),
            ("medication", "Medication"),
            ("substance", "Substance")],
        help="Type of reference to the group member.")
    entity_name = fields.Char(
        string="Entity",
        help="Entity reference to the group member.")
    entity_patient_id = fields.Many2one(
        comodel_name="hc.res.patient",
        string="Entity Patient",
        help="Patient reference to the group member.")
    entity_practitioner_id = fields.Many2one(
        comodel_name="hc.res.practitioner",
        string="Entity Practitioner",
        help="Practitioner reference to the group member.")
    entity_device_id = fields.Many2one(
        comodel_name="hc.res.device",
        string="Entity Device",
        help="Device reference to the group member.")
    entity_medication_id = fields.Many2one(
        comodel_name="hc.res.medication",
        string="Entity Medication",
        help="Medication reference to the group member.")
    entity_substance_id = fields.Many2one(
        comodel_name="hc.res.substance",
        string="Entity Substance",
        help="Substance reference to the group member.")
    period_start_date = fields.Datetime(
        string="Period Start Date",
        help="Start of the period member belonged to the group.")
    period_end_date = fields.Datetime(
        string="Period End Date",
        help="End of the period member belonged to the group.")
    is_member = fields.Boolean(
        string="Member",
        default="True",
        help="Uncheck if member is no longer in group.")

class GroupIdentifier(models.Model):
    _name = "hc.group.identifier"
    _description = "Group Identifier"
    _inherit = ["hc.basic.association", "hc.identifier", "hc.identifier.use"]

    group_id = fields.Many2one(
        comodel_name="hc.res.group",
        string="Group",
        help="Group associated with this Group Identifier.")

class GroupCode(models.Model):
    _name = "hc.vs.group.code"
    _description = "Group Code"
    _inherit = ["hc.value.set.contains"]

class GroupCharacteristicCode(models.Model):
    _name = "hc.vs.group.characteristic.code"
    _description = "Group Characteristic Code"
    _inherit = ["hc.value.set.contains"]

class GroupCharacteristicValueCode(models.Model):
    _name = "hc.vs.group.characteristic.value"
    _description = "Group Characteristic Value"
    _inherit = ["hc.value.set.contains"]
