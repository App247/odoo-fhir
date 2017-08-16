# -*- coding: utf-8 -*-

from openerp import models, fields, api

class CatalogEntry(models.Model):
    _name = "hc.res.catalog.entry"
    _description = "Catalog Entry"
    _inherit = ["hc.domain.resource"]
    _rec_name = "name"

    name = fields.Char(string="Name", compute="_compute_name", store="True", help="Text representation of the catalog entry. Reference Item + Type + Valid Period.")
    type_id = fields.Many2one(comodel_name="hc.vs.catalog.entry.type", string="Type", help="The type of item - medication, device, service, protocol or other.")
    purpose_id = fields.Many2one(comodel_name="hc.vs.catalog.entry.purpose", string="Purpose", required="True", help="Whether the entry represents an orderable item, or other.")
    reference_item_type = fields.Selection(
        string="Reference Item Type",
        selection=[
            ("medication", "Medication"),
            ("device", "Device"),
            ("procedure", "Procedure"),
            ("care_plan", "Care Plan"),
            ("organization", "Organization"),
            ("practitioner", "Practitioner"),
            ("healthcare_service", "Healthcare Service"),
            ("service_definition", "Service Definition")],
        required="True",
        help="Type of the item itself.")
    reference_item_name = fields.Char(
        string="Reference Item",
        compute="_compute_reference_item_name",
        store="True",
        help="The item itself.")
    reference_item_medication_id = fields.Many2one(
        comodel_name="hc.res.medication",
        string="Reference Item Medication",
        help="Medication reference.")
    reference_item_device_id = fields.Many2one(
        comodel_name="hc.res.device",
        string="Reference Item Device",
        help="Device reference.")
    reference_item_procedure_id = fields.Many2one(
        comodel_name="hc.res.procedure",
        string="Reference Item Procedure",
        help="Procedure reference.")
    reference_item_care_plan_id = fields.Many2one(
        comodel_name="hc.res.care.plan",
        string="Reference Item Care Plan",
        help="Care Plan reference.")
    reference_item_organization_id = fields.Many2one(
        comodel_name="hc.res.organization",
        string="Reference Item Organization",
        help="Organization reference.")
    reference_item_practitioner_id = fields.Many2one(
        comodel_name="hc.res.practitioner",
        string="Reference Item Practitioner",
        help="Practitioner reference.")
    reference_item_healthcare_service_id = fields.Many2one(
        comodel_name="hc.res.healthcare.service",
        string="Reference Item Healthcare Service",
        help="Healthcare Service reference.")
    reference_item_service_definition_id = fields.Many2one(
        comodel_name="hc.res.service.definition",
        string="Reference Item Service Definition",
        help="Service Definition reference.")
    identifier_id = fields.Many2one(comodel_name="hc.catalog.entry.identifier", string="Identifier", help="Unique identifier of the catalog item.")
    additional_identifier_ids = fields.One2many(comodel_name="hc.catalog.entry.additional.identifier", inverse_name="catalog_entry_id", string="Additional Identifiers", help="Any additional identifier(s) for the catalog item, in the same granularity or concept.")
    classification_ids = fields.One2many(comodel_name="hc.catalog.entry.classification", inverse_name="catalog_entry_id", string="Classifications", help="Classification (category or class) of the item entry.")
    status_id= fields.Many2one(comodel_name="hc.vs.catalog.entry.status", string="Status", help="The status of the item, e.g. active, approved, deleted.")
    valid_period_start_date = fields.Datetime(string="Valid Period Start Date", help="Start of the time period in which this catalog entry is expected to be active.")
    valid_period_end_date = fields.Datetime(string="Valid Period End Date", help="End of the time period in which this catalog entry is expected to be active.")
    last_updated = fields.Datetime(string="Last Updated", help="When was this catalog last updated.")
    additional_characteristic_ids = fields.One2many(comodel_name="hc.catalog.entry.additional.characteristic", inverse_name="catalog_entry_id", string="Additional Characteristics", help="Additional characteristics of the catalog entry.")
    additional_classification_ids = fields.One2many(comodel_name="hc.catalog.entry.additional.classification", inverse_name="catalog_entry_id", string="Additional Classifications", help="Additional classification of the catalog entry.")
    related_item_ids = fields.One2many(comodel_name="hc.catalog.entry.related.item", inverse_name="catalog_entry_id", string="Related Items", help="An item that this catalog entry is related to.")

class CatalogEntryRelatedItem(models.Model):
    _name = "hc.catalog.entry.related.item"
    _description = "Catalog Entry Related Item"

    catalog_entry_id = fields.Many2one(comodel_name="hc.res.catalog.entry", string="Catalog Entry", help="Catalog Entry associated with this Catalog Entry Related Item.")
    relation_type_id = fields.Many2one(comodel_name="hc.vs.catalog.entry.relation.type", string="Relation Type", required="True", help="The type of relation to the related item.")
    type_id = fields.Many2one(comodel_name="hc.vs.catalog.entry.type", string="Type", help="The type of item - medication, device, service, protocol or other.")
    item_type = fields.Selection(
        string="Item Type",
        selection=[
            ("medication", "Medication"),
            ("device", "Device"),
            ("procedure", "Procedure"),
            ("care_plan", "Care Plan"),
            ("organization", "Organization"),
            ("practitioner", "Practitioner"),
            ("healthcare_service", "Healthcare Service"),
            ("service_definition", "Service Definition"),
            ("catalog_entry", "Catalog Entry")],
        required="True",
        help="Type of the item itself.")
    item_name = fields.Char(
        string="Item",
        compute="_compute_item_name",
        store="True",
        help="The item itself.")
    item_medication_id = fields.Many2one(
        comodel_name="hc.res.medication",
        string="Item Medication",
        help="Medication reference to the related item.")
    item_device_id = fields.Many2one(
        comodel_name="hc.res.device",
        string="Item Device",
        help="Device reference to the related item.")
    item_procedure_id = fields.Many2one(
        comodel_name="hc.res.procedure",
        string="Item Procedure",
        help="Procedure reference to the related item.")
    item_care_plan_id = fields.Many2one(
        comodel_name="hc.res.care.plan",
        string="Item Care Plan",
        help="Care Plan reference to the related item.")
    item_organization_id = fields.Many2one(
        comodel_name="hc.res.organization",
        string="Item Organization",
        help="Organization reference to the related item.")
    item_practitioner_id = fields.Many2one(
        comodel_name="hc.res.practitioner",
        string="Item Practitioner",
        help="Practitioner reference to the related item.")
    item_healthcare_service_id = fields.Many2one(
        comodel_name="hc.res.healthcare.service",
        string="Item Healthcare Service",
        help="Healthcare Service reference to the related item.")
    item_service_definition_id = fields.Many2one(
        comodel_name="hc.res.service.definition",
        string="Item Service Definition",
        help="Service Definition reference to the related item.")
    item_catalog_entry_id = fields.Many2one(
        comodel_name="hc.res.catalog.entry",
        string="Item Catalog Entry",
        help="Catalog Entry reference to the related item.")

class CatalogEntryIdentifier(models.Model):
    _name = "hc.catalog.entry.identifier"
    _description = "Catalog Entry Identifier"
    _inherit = ["hc.basic.association", "hc.identifier"]

    catalog_entry_id = fields.Many2one(comodel_name="hc.res.catalog.entry", string="Catalog Entry", help="Catalog Entry associated with this Catalog Entry Identifier.")

class CatalogEntryAdditionalIdentifier(models.Model):
    _name = "hc.catalog.entry.additional.identifier"
    _description = "Catalog Entry Additional Identifier"
    _inherit = ["hc.basic.association", "hc.identifier"]

    catalog_entry_id = fields.Many2one(comodel_name="hc.res.catalog.entry", string="Catalog Entry", help="Catalog Entry associated with this Catalog Entry Additional Identifier.")

class CatalogEntryClassification(models.Model):
    _name = "hc.catalog.entry.classification"
    _description = "Catalog Entry Classification"
    _inherit = ["hc.basic.association", "hc.identifier"]

    catalog_entry_id = fields.Many2one(comodel_name="hc.res.catalog.entry", string="Catalog Entry", help="Catalog Entry associated with this Catalog Entry Classification.")

class CatalogEntryAdditionalCharacteristic(models.Model):
    _name = "hc.catalog.entry.additional.characteristic"
    _description = "Catalog Entry Additional Characteristic"
    _inherit = ["hc.basic.association"]

    catalog_entry_id = fields.Many2one(comodel_name="hc.res.catalog.entry", string="Catalog Entry", help="Catalog Entry associated with this Catalog Entry Classification.")
    additional_characteristic_id = fields.Many2one(comodel_name="hc.vs.catalog.entry.characteristic", string="Additional Characteristic", help="Additional Characteristic associated with this Catalog Entry Additional Characteristic.")

class CatalogEntryAdditionalClassification(models.Model):
    _name = "hc.catalog.entry.additional.classification"
    _description = "Catalog Entry Additional Classification"
    _inherit = ["hc.basic.association"]

    catalog_entry_id = fields.Many2one(comodel_name="hc.res.catalog.entry", string="Catalog Entry", help="Catalog Entry associated with this Catalog Entry Classification.")
    additional_classification_id = fields.Many2one(comodel_name="hc.vs.catalog.entry.classification", string="Additional Classification", help="Additional Classification associated with this Catalog Entry Additional Characteristic.")

class CatalogEntryStatus(models.Model):
    _name = "hc.vs.catalog.entry.status"
    _description = "Catalog Entry Status"
    _inherit = ["hc.value.set.contains"]

    name = fields.Char(
        string="Name",
        help="Name of this catalog entry status.")
    code = fields.Char(
        string="Code",
        help="Code of this catalog entry status.")
    contains_id = fields.Many2one(
        comodel_name="hc.vs.catalog.entry.status",
        string="Parent",
        help="Parent concept.")

class CatalogEntryType(models.Model):
    _name = "hc.vs.catalog.entry.type"
    _description = "Catalog Entry Type"
    _inherit = ["hc.value.set.contains"]

    name = fields.Char(
        string="Name",
        help="Name of this catalog entry type.")
    code = fields.Char(
        string="Code",
        help="Code of this catalog entry type.")
    contains_id = fields.Many2one(
        comodel_name="hc.vs.catalog.entry.type",
        string="Parent",
        help="Parent concept.")

class CatalogEntryPurpose(models.Model):
    _name = "hc.vs.catalog.entry.purpose"
    _description = "Catalog Entry Purpose"
    _inherit = ["hc.value.set.contains"]

    name = fields.Char(
        string="Name",
        help="Name of this catalog entry purpose.")
    code = fields.Char(
        string="Code",
        help="Code of this catalog entry purpose.")
    contains_id = fields.Many2one(
        comodel_name="hc.vs.catalog.entry.purpose",
        string="Parent",
        help="Parent concept.")

class CatalogEntryRelationType(models.Model):
    _name = "hc.vs.catalog.entry.relation.type"
    _description = "Catalog Entry Relation Type"
    _inherit = ["hc.value.set.contains"]

    name = fields.Char(
        string="Name",
        help="Name of this catalog entry relation type.")
    code = fields.Char(
        string="Code",
        help="Code of this catalog entry relation type.")
    contains_id = fields.Many2one(
        comodel_name="hc.vs.catalog.entry.relation.type",
        string="Parent",
        help="Parent concept.")

class CatalogEntryType(models.Model):
    _name = "hc.vs.catalog.entry.type"
    _description = "Catalog Entry Type"
    _inherit = ["hc.value.set.contains"]

    name = fields.Char(
        string="Name",
        help="Name of this catalog entry type.")
    code = fields.Char(
        string="Code",
        help="Code of this catalog entry type.")
    contains_id = fields.Many2one(
        comodel_name="hc.vs.catalog.entry.type",
        string="Parent",
        help="Parent concept.")

class CatalogEntryCharacteristic(models.Model):
    _name = "hc.vs.catalog.entry.characteristic"
    _description = "Catalog Entry Characteristic"
    _inherit = ["hc.value.set.contains"]

    name = fields.Char(
        string="Name",
        help="Name of this catalog entry characteristic.")
    code = fields.Char(
        string="Code",
        help="Code of this catalog entry characteristic.")
    contains_id = fields.Many2one(
        comodel_name="hc.vs.catalog.entry.characteristic",
        string="Parent",
        help="Parent concept.")

class CatalogEntryClassification(models.Model):
    _name = "hc.vs.catalog.entry.classification"
    _description = "Catalog Entry Classification"
    _inherit = ["hc.value.set.contains"]

    name = fields.Char(
        string="Name",
        help="Name of this catalog entry classification.")
    code = fields.Char(
        string="Code",
        help="Code of this catalog entry classification.")
    contains_id = fields.Many2one(
        comodel_name="hc.vs.catalog.entry.classification",
        string="Parent",
        help="Parent concept.")
