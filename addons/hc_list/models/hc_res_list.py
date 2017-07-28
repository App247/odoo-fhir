# -*- coding: utf-8 -*-

from openerp import models, fields, api

class List(models.Model):
    _name = "hc.res.list"
    _description = "List"

    identifier_ids = fields.One2many(
        comodel_name="hc.list.identifier",
        inverse_name="list_id",
        string="Identifiers",
        help="Business identifier.")
    status = fields.Selection(
        string="Status",
        required="True",
        selection=[
            ("current", "Current"),
            ("retired", "Retired"),
            ("entered-in-error", "Entered In Error")],
        help="Indicates the current state of this list.")
    mode = fields.Many2one(
        comodel_name="hc.vs.list.mode",
        string="Mode",
        required="True",
        help="How this list was prepared.")
    title = fields.Text(
        string="Title",
        help="Descriptive name for the list.")
    code_id = fields.Many2one(
        comodel_name="hc.vs.list.code",
        string="Code",
        help="What the purpose of this list is.")
    subject_type = fields.Selection(
        string="Subject Type",
        selection=[
            ("Patient", "Patient"),
            ("Group", "Group"),
            ("Device", "Device"),
            ("Location", "Location")],
        help="Type of resources that have the same subject.")
    subject_name = fields.Char(
        string="Subject",
        compute="_compute_subject_name",
        store="True",
        help="If all resources have the same subject.")
    subject_patient_id = fields.Many2one(
        comodel_name="hc.res.patient",
        string="Subject Patient",
        help="Patient same subject.")
    subject_group_id = fields.Many2one(
        comodel_name="hc.res.group",
        string="Subject Group",
        help="Group same subject.")
    subject_device_id = fields.Many2one(
        comodel_name="hc.res.device",
        string="Subject Device",
        help="Device same subject.")
    subject_location_id = fields.Many2one(
        comodel_name="hc.res.location",
        string="Subject Location",
        help="Location same subject.")
    encounter_id = fields.Many2one(
        comodel_name="hc.res.encounter",
        string="Encounter",
        help="Context in which list created.")
    list_date = fields.Datetime(
        string="List Date",
        help="When the list was prepared.")
    source_type = fields.Selection(
        string="Source Type",
        selection=[
            ("Practitioner", "Practitioner"),
            ("Patient", "Patient"),
            ("Device", "Device")],
        help="Type of who and/or what defined the list contents.")
    source_name = fields.Char(
        string="Source",
        compute="_compute_source_name",
        store="True",
        help="Who and/or what defined the list contents.")
    source_practitioner_id = fields.Many2one(
        comodel_name="hc.res.practitioner",
        string="Source Practitioner",
        help="Practitioner who and/or what defined the list contents.")
    source_patient_id = fields.Many2one(
        comodel_name="hc.res.patient",
        string="Source Patient",
        help="Patient who and/or what defined the list contents.")
    source_device_id = fields.Many2one(
        comodel_name="hc.res.device",
        string="Source Device",
        help="Device who and/or what defined the list contents.")
    ordered_by_id = fields.Many2one(
        comodel_name="hc.vs.list.order",
        string="Ordered By",
        help="What order the list has.")
    note_ids = fields.One2many(
        comodel_name="hc.list.note",
        inverse_name="list_id",
        string="Notes",
        help="Comments about the list.")
    empty_reason_id = fields.Many2one(
        comodel_name="hc.vs.list.empty.reason",
        string="Empty Reason",
        help="Why list is empty.")
    entry_ids = fields.One2many(
        comodel_name="hc.list.entry",
        inverse_name="list_id",
        string="Entries",
        help="Entries in the list.")

class ListEntry(models.Model):
    _name = "hc.list.entry"
    _description = "List Entry"

    list_id = fields.Many2one(
        comodel_name="hc.res.list",
        string="List",
        help="List associated with this List Entry.")
    flag_ids = fields.Many2many(
        comodel_name="hc.vs.list.entry.flag",
        string="Flags",
        help="Workflow information about this item.")
    is_deleted = fields.Boolean(
        string="Deleted",
        help="If this item is actually marked as deleted.")
    entry_date = fields.Datetime(
        string="Entry Date",
        help="When item added to list.")
    item_type = fields.Selection(
        string="Item Type",
        selection=[
            ("Family Member History", "Family Member History"),
            ("Medication Request", "Medication Request"),
            ("Allergy Intolerance", "Allergy Intolerance"),
            ("Condition", "Condition"),
            ("Procedure", "Procedure")],
        help="Type of actual entry.")
    item_name = fields.Char(
        string="Item",
        compute="_compute_item_name",
        store="True",
        help="Actual entry.")
    item_family_member_history_id = fields.Many2one(
        comodel_name="hc.res.family.member.history",
        string="Item Family Member History",
        help="Family Member History actual entry.")
    item_medication_request_id = fields.Many2one(
        comodel_name="hc.res.medication.request",
        string="Item Medication Request",
        help="Medication Request actual entry.")
    item_allergy_intolerance_id = fields.Many2one(
        comodel_name="hc.res.allergy.intolerance",
        string="Item Allergy Intolerance",
        help="Allergy Intolerance actual entry.")
    item_condition_id = fields.Many2one(
        comodel_name="hc.res.condition",
        string="Item Condition",
        help="Condition actual entry.")
    item_procedure_id = fields.Many2one(
        comodel_name="hc.res.procedure",
        string="Item Procedure",
        help="Procedure actual entry.")

class ListIdentifier(models.Model):
    _name = "hc.list.identifier"
    _description = "List Identifier"
    _inherit = ["hc.basic.association", "hc.identifier"]

    list_id = fields.Many2one(
        comodel_name="hc.res.list",
        string="List",
        help="List associated with this List Identifier.")

class ListNote(models.Model):
    _name = "hc.list.note"
    _description = "List Note"
    _inherit = ["hc.basic.association", "hc.annotation"]

    list_id = fields.Many2one(
        comodel_name="hc.res.list",
        string="List",
        help="List associated with this List Note.")

class ListMode(models.Model):
    _name = "hc.vs.list.mode"
    _description = "List Mode"
    _inherit = ["hc.value.set.contains"]

class ListCode(models.Model):
    _name = "hc.vs.list.code"
    _description = "List Code"
    _inherit = ["hc.value.set.contains"]

class ListOrder(models.Model):
    _name = "hc.vs.list.order"
    _description = "List Order"
    _inherit = ["hc.value.set.contains"]

class ListEmptyReason(models.Model):
    _name = "hc.vs.list.empty.reason"
    _description = "List Empty Reason"
    _inherit = ["hc.value.set.contains"]

class ListEntryFlag(models.Model):
    _name = "hc.vs.list.entry.flag"
    _description = "List Entry Flag"
    _inherit = ["hc.value.set.contains"]
