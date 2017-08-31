# -*- coding: utf-8 -*-

from openerp import models, fields, api

class ChargeItem(models.Model):
    _name = "hc.res.charge.item"
    _description = "Charge Item"

    identifier_id = fields.Many2one(
        comodel_name="hc.charge.item.identifier",
        string="Identifier",
        help="Business Identifer for item.")
    definition_ids = fields.One2many(
        comodel_name="hc.charge.item.definition",
        inverse_name="charge_item_id",
        string="Definition URIs",
        help="URI of defining information about the code of this charge item.")
    status = fields.Selection(
        string="Charge Item Status",
        required="True",
        selection=[
            ("planned", "Planned"),
            ("billable", "Billable"),
            ("not-billable", "Not-Billable"),
            ("aborted", "Aborted"),
            ("billed", "Billed"),
            ("entered-in-error", "Entered-In-Error"),
            ("unknown", "Unknown")],
        help="Indicates whether the account is presently used/useable or not.")
    part_of_ids = fields.One2many(
        comodel_name="hc.charge.item.part.of",
        inverse_name="charge_item_id",
        string="Part Ofs",
        help="Part of referenced ChargeItem.")
    code_id = fields.Many2one(
        comodel_name="hc.vs.charge.item.billing.code",
        string="Code",
        required="True",
        help="A code that identifies the charge, like a billing code.")
    subject_type = fields.Selection(
        string="Subject Type",
        required="True",
        selection=[
            ("patient", "Patient"),
            ("group", "Group")],
        help="Type of individual service was done for/to.")
    subject_name = fields.Char(
        string="Subject",
        compute="_compute_subject_name",
        store="True",
        help="Individual service was done for/to.")
    subject_patient_id = fields.Many2one(
        comodel_name="hc.res.patient",
        string="Subject Patient",
        help="Patient individual service was done for/to.")
    subject_organization_id = fields.Many2one(
        comodel_name="hc.res.organization",
        string="Subject Organization",
        help="Organization individual service was done for/to.")
    context_type = fields.Selection(
        string="Context Type",
        selection=[
            ("encounter", "Encounter"),
            ("episode_of_care", "Episode Of Care")],
        help="Encounter / Episode associated with event.")
    context_name = fields.Char(
        string="Context",
        compute="_compute_context_name",
        store="True",
        help="Encounter / Episode associated with event.")
    context_encounter_id = fields.Many2one(
        comodel_name="hc.res.encounter",
        string="Context Encounter",
        help="Encounter associated with event.")
    context_episode_of_care_id = fields.Many2one(
        comodel_name="hc.res.episode.of.care",
        string="Context Episode Of Care",
        help="Episode Of Care associated with event.")
    occurence_type = fields.Selection(
        string="Occurence Type",
        selection=[
            ("dateTime", "Datetime"),
            ("Period", "Period"),
            ("Timing", "Timing")],
        help="Type of when the charged service was applied.")
    occurrence_name = fields.Char(
        string="Occurrence",
        compute="_compute_occurrence_name",
        store="True",
        help="When the charged service was applied.")
    occurrence_datetime = fields.Datetime(
        string="Occurrence Datetime",
        help="Date Time when the charged service was applied.")
    occurrence_start_date = fields.Datetime(
        string="Occurrence Start Date",
        help="Start of when the charged service was applied.")
    occurrence_end_date = fields.Datetime(
        string="Occurrence End Date",
        help="End of when the charged service was applied.")
    timing_id = fields.Many2one(
        comodel_name="hc.charge.item.timing",
        string="Timing",
        help="When the charged service was applied.")
    performing_organization_id = fields.Many2one(
        comodel_name="hc.res.organization",
        string="Performing Organization",
        help="Organization providing the charged sevice.")
    requesting_organization_id = fields.Many2one(
        comodel_name="hc.res.organization",
        string="Requesting Organization",
        help="Organization requesting the charged service.")
    quantity = fields.Float(
        string="Quantity",
        help="Quantity of which the charge item has been serviced.")
    quantity_uom_id = fields.Many2one(
        comodel_name="product.uom",
        string="Quantity UOM",
        help="Quantity unit of measure.")
    body_site_ids = fields.Many2many(
        comodel_name="hc.vs.body.site",
        relation="charge_item_body_site_rel",
        string="Body Sites",
        help="Anatomical location, if relevant.")
    factor_override = fields.Float(
        string="Factor Override",
        help="Factor overriding the associated rules.")
    price_override = fields.Float(
        string="Price Override",
        help="Price overriding the associated rules")
    override_reason = fields.Char(
        string="Override Reason",
        help="Reason for overriding the list price/factor.")
    enterer_type = fields.Selection(
        string="Enterer Type",
        selection=[
            ("practitioner", "Practitioner"),
            ("organization", "Organization"),
            ("patient", "Patient"),
            ("device", "Device"),
            ("related_person", "Related Person")],
        help="Type of individual who was entering.")
    enterer_name = fields.Char(
        string="Enterer",
        compute="_compute_enterer_name",
        store="True",
        help="Individual who was entering.")
    enterer_practitioner_id = fields.Many2one(
        comodel_name="hc.res.practitioner",
        string="Enterer Practitioner",
        help="Practitioner who was entering.")
    enterer_organization_id = fields.Many2one(
        comodel_name="hc.res.organization",
        string="Enterer Organization",
        help="Organization who was entering.")
    enterer_patient_id = fields.Many2one(
        comodel_name="hc.res.patient",
        string="Enterer Patient",
        help="Patient who was entering.")
    enterer_device_id = fields.Many2one(
        comodel_name="hc.res.device",
        string="Enterer Device",
        help="Device who was entering.")
    enterer_related_person_id = fields.Many2one(
        comodel_name="hc.res.related.person",
        string="Enterer Related Person",
        help="Related Person who was entering.")
    entered_date = fields.Datetime(
        string="Entered Date",
        help="Date the charge item was entered.")
    reason_ids = fields.Many2many(
        comodel_name="hc.vs.icd.10",
        relation="charge_item_reason_rel",
        string="Reasons",
        help="Why was the charged service rendered?")
    service_ids = fields.One2many(
        comodel_name="hc.charge.item.service",
        inverse_name="charge_item_id",
        string="Services",
        help="Which rendered service is being charged?")
    account_ids = fields.One2many(
        comodel_name="hc.charge.item.account",
        inverse_name="charge_item_id",
        string="Accounts",
        help="Account to place this charge.")
    note_ids = fields.One2many(
        comodel_name="hc.charge.item.note",
        inverse_name="charge_item_id",
        string="Notes",
        help="Comments made about the ChargeItem.")
    supporting_information_ids = fields.One2many(
        comodel_name="hc.charge.item.supporting.information",
        inverse_name="charge_item_id",
        string="Supporting Information",
        help="Further information supporting the this charge.")

class ChargeItemParticipant(models.Model):
    _name = "hc.charge.item.participant"
    _description = "Charge Item Participant"

    role_id = fields.Many2one(
        comodel_name="hc.vs.performer.role",
        string="Role",
        help="What type of performance was done.")
    actor_type = fields.Selection(
        string="Actor Type",
        required="True",
        selection=[
            ("practitioner", "Practitioner"),
            ("organization", "Organization"),
            ("patient", "Patient"),
            ("device", "Device"),
            ("related_person", "Related Person")],
        help="Type of individual who was performing.")
    actor_name = fields.Char(
        string="Actor",
        compute="_compute_actor_name",
        store="True",
        help="Individual who was performing.")
    actor_practitioner_id = fields.Many2one(
        comodel_name="hc.res.practitioner",
        string="Actor Practitioner",
        help="Practitioner individual who was performing.")
    actor_organization_id = fields.Many2one(
        comodel_name="hc.res.organization",
        string="Actor Organization",
        help="Organization individual who was performing.")
    actor_patient_id = fields.Many2one(
        comodel_name="hc.res.patient",
        string="Actor Patient",
        help="Patient individual who was performing.")
    actor_device_id = fields.Many2one(
        comodel_name="hc.res.device",
        string="Actor Device",
        help="Device individual who was performing.")
    actor_imaging_study_id = fields.Many2one(
        comodel_name="hc.res.imaging.study",
        string="Actor Imaging Study",
        help="Imaging Study individual who was performing.")

class ChargeItemIdentifier(models.Model):
    _name = "hc.charge.item.identifier"
    _description = "Charge Item Identifier"
    _inherit = ["hc.basic.association", "hc.identifier"]

class ChargeItemDefinition(models.Model):
    _name = "hc.charge.item.definition"
    _description = "Charge Item Definition"
    _inherit = ["hc.basic.association"]

    charge_item_id = fields.Many2one(
        comodel_name="hc.res.charge.item",
        string="Charge Item",
        help="Charge Item associated with this Charge Item Definition.")
    definition = fields.Char(
        string="Definition URI",
        help="Definition associated with this Charge Item Definition.")

class ChargeItemPartOf(models.Model):
    _name = "hc.charge.item.part.of"
    _description = "Charge Item Part Of"
    _inherit = ["hc.basic.association"]

    charge_item_id = fields.Many2one(
        comodel_name="hc.res.charge.item",
        string="Charge Item",
        help="Charge Item associated with this Charge Item Part Of.")
    part_of_id = fields.Many2one(
        comodel_name="hc.res.charge.item",
        string="Part Of",
        help="Charge Item associated with this Charge Item Part Of.")

class ChargeItemTiming(models.Model):
    _name = "hc.charge.item.timing"
    _description = "Charge Item Timing"
    _inherit = ["hc.basic.association", "hc.timing"]

class ChargeItemService(models.Model):
    _name = "hc.charge.item.service"
    _description = "Charge Item Service"
    _inherit = ["hc.basic.association"]

    charge_item_id = fields.Many2one(
        comodel_name="hc.res.charge.item",
        string="Charge Item",
        help="Charge Item associated with this Charge Item Service.")
    service_type = fields.Selection(
        string="Service Type",
        selection=[
            ("diagnostic_report", "Diagnostic Report"),
            ("imaging_study", "Imaging Study"),
            ("immunization", "Immunization"),
            ("medication_administration", "Medication Administration"),
            ("medication_dispense", "Medication Dispense"),
            ("observation", "Observation"),
            ("procedure", "Procedure"),
            ("supply_delivery", "Supply Delivery")],
        help="Type of which rendered service is being charged?")
    service_name = fields.Char(
        string="Service",
        compute="_compute_service_name",
        store="True",
        help="Which rendered service is being charged?")
    service_diagnostic_report_id = fields.Many2one(
        comodel_name="hc.res.diagnostic.report",
        string="Service Diagnostic Report",
        help="Diagnostic Report which rendered service is being charged?")
    service_immunization_id = fields.Many2one(
        comodel_name="hc.res.immunization",
        string="Service Immunization",
        help="Immunization rendered service is being charged?")
    service_medication_administration_id = fields.Many2one(
        comodel_name="hc.res.medication.administration",
        string="Service Medication Administration",
        help="Medication Administration rendered service is being charged?")
    service_medication_dispense_id = fields.Many2one(
        comodel_name="hc.res.medication.dispense",
        string="Service Medication Dispense",
        help="Medication Dispense rendered service is being charged?")
    service_observation_id = fields.Many2one(
        comodel_name="hc.res.observation",
        string="Service Observation",
        help="Observation rendered service is being charged?")
    service_procedure_id = fields.Many2one(
        comodel_name="hc.res.procedure",
        string="Service Procedure",
        help="Procedure rendered service is being charged?")
    service_supply_delivery_id = fields.Many2one(
        comodel_name="hc.res.supply.delivery",
        string="Service Supply Delivery",
        help="Supply Delivery rendered service is being charged?")

class ChargeItemAccount(models.Model):
    _name = "hc.charge.item.account"
    _description = "Charge Item Account"
    _inherit = ["hc.basic.association"]

    charge_item_id = fields.Many2one(
        comodel_name="hc.res.charge.item",
        string="Charge Item",
        help="Charge Item associated with this Charge Item Account.")
    account_id = fields.Many2one(
        comodel_name="hc.res.account",
        string="Account",
        help="Account associated with this Charge Item Account.")

class ChargeItemNote(models.Model):
    _name = "hc.charge.item.note"
    _description = "Charge Item Note"
    _inherit = ["hc.basic.association", "hc.annotation"]

    charge_item_id = fields.Many2one(
        comodel_name="hc.res.charge.item",
        string="Charge Item",
        help="Charge Item associated with this Charge Item Note.")

class ChargeItemSupportingInformation(models.Model):
    _name = "hc.charge.item.supporting.information"
    _description = "Charge Item Supporting Information"
    _inherit = ["hc.basic.association"]

    charge_item_id = fields.Many2one(
        comodel_name="hc.res.charge.item",
        string="Charge Item",
        help="Charge Item associated with this Charge Item Supporting Information.")
    supporting_information_type = fields.Char(
        string="Supporting Information Type",
        compute="_compute_supporting_information_type",
        store="True",
        help="Type of which rendered service is being charged?")
    supporting_information_name = fields.Reference(
        string="Supporting Information",
        selection="_reference_models",
        help="Further information supporting the this charge.")

class ChargeItemBillingCode(models.Model):
    _name = "hc.vs.charge.item.billing.code"
    _description = "Charge Item Billing Code"
    _inherit = ["hc.value.set.contains"]

    name = fields.Char(
        string="Name",
        help="Name of this charge item billing code.")
    code = fields.Char(
        string="Code",
        help="Code of this charge item billing code.")
    contains_id = fields.Many2one(
        comodel_name="hc.vs.charge.item.billing.code",
        string="Parent",
        help="Parent charge item billing code.")
