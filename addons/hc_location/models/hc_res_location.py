# -*- coding: utf-8 -*-

from openerp import models, fields, api
from datetime import datetime

class Location(models.Model):
    _name = "hc.res.location"
    _description = "Location"
    _inherit = "hc.domain.resource"
    _rec_name = "name"

    identifier_ids = fields.One2many(
        comodel_name="hc.location.identifier",
        inverse_name="location_id",
        string="Identifiers",
        help="Unique code or number identifying the location to its users.")
    status = fields.Selection(
        string="Status",
        selection=[
            ("active", "Active"),
            ("suspended", "Suspended"),
            ("inactive", "Inactive")],
        help="Indicates whether the location is still in use.")
    operational_status_id = fields.Many2one(
        comodel_name="hc.vs.bed.status",
        string="Operational Status",
        help="The Operational status of the location (typically only for a bed/room).")
    name = fields.Char(
        string="Name",
        help="Name of the location as used by humans.")
    alias_ids = fields.One2many(
        comodel_name="hc.location.alias",
        inverse_name="location_id",
        string="Aliases",
        help="A list of alternate names that the location is known as or was known as in the past.")
    description = fields.Text(
        string="Description",
        help="Description of the Location, which helps in finding or referencing the place.")
    mode = fields.Selection(
        string="Mode",
        selection=[
            ("instance", "Instance"),
            ("kind", "Kind")],
        help="Indicates whether a resource instance represents a specific location or a class of locations.")
    type_id = fields.Many2one(
        comodel_name="hc.vs.service.delivery.location.role.type",
        string="Type",
        help="Indicates the type of function performed at the location.")
    telecom_ids = fields.One2many(
        comodel_name="hc.location.telecom",
        inverse_name="location_id",
        string="Telecom",
        help="Contact details of the location.")
    address_id = fields.Many2one(
        comodel_name="hc.address",
        string="Address",
        help="Physical location.")
    physical_type_id = fields.Many2one(
        comodel_name="hc.vs.location.physical.type",
        string="Physical Type",
        help="Physical form of the location.")
    position_id = fields.Many2one(
        comodel_name="hc.location.position",
        string="Position",
        help="absolute geographic location.")
    managing_organization_id = fields.Many2one(
        comodel_name="hc.res.organization",
        string="Managing Organization",
        help="The organization that is responsible for the provisioning and upkeep of the location.")
    part_of_id = fields.Many2one(
        comodel_name="hc.res.location",
        string="Part Of",
        help="Another Location which this Location is physically part of.")
    endpoint_ids = fields.One2many(
        comodel_name="hc.location.endpoint",
        inverse_name="location_id",
        string="Endpoints",
        help="Technical endpoints providing access to services operated for the location.")

    # Domain Resource
    text_id = fields.Many2one(
        comodel_name="hc.location.domain.resource.text")

    contained_ids = fields.One2many(
        comodel_name="hc.location.domain.resource.contained",
        inverse_name="location_id")

    extension_ids = fields.One2many(
        comodel_name="hc.location.domain.resource.extension",
        inverse_name="location_id")

    modifier_extension_ids = fields.One2many(
        comodel_name="hc.location.domain.resource.modifier.extension",
        inverse_name="location_id")

class LocationPosition(models.Model):
    _name = "hc.location.position"
    _description = "Location Position"
    _inherit = ["hc.backbone.element", "hc.address.geolocation"]
    _rec_name = "name"

    location_id = fields.Many2one(
        comodel_name="hc.res.location",
        string="Location",
        help="Location associated with this Location Position.")

class LocationIdentifier(models.Model):
    _name = "hc.location.identifier"
    _description = "Location Identifier"
    _inherit = ["hc.basic.association", "hc.identifier", "hc.identifier.use"]

    location_id = fields.Many2one(
        comodel_name="hc.res.location",
        string="Location",
        help="Location associated with this Location Identifier.")

class LocationTelecom(models.Model):
    _name = "hc.location.telecom"
    _description = "Location Telecom"
    _inherit = ["hc.contact.point.use"]
    _inherits = {"hc.contact.point": "telecom_id"}

    telecom_id = fields.Many2one(
        comodel_name="hc.contact.point",
        string="Telecom",
        ondelete="restrict",
        required="True",
        help="Telecom associated with this Location Telecom.")
    location_id = fields.Many2one(
        comodel_name="hc.res.location",
        string="Location",
        help="Location associated with this Location Telecom.")

class LocationAlias(models.Model):
    _name = "hc.location.alias"
    _description = "Location Alias"
    _inherit = ["hc.basic.association"]

    location_id = fields.Many2one(
        comodel_name="hc.res.location",
        string="Location",
        help="Location associated with this Location Alias.")
    alias = fields.Char(
        string="Alias",
        help="Alias associated with this Location Alias.")

class LocationEndpoint(models.Model):
    _name = "hc.location.endpoint"
    _description = "Location Endpoint"
    _inherit = ["hc.basic.association"]

    location_id = fields.Many2one(
        comodel_name="hc.res.location",
        string="Location",
        help="Location associated with this Location Endpoint.")
    endpoint_id = fields.Many2one(
        comodel_name="hc.res.endpoint",
        string="Endpoint",
        help="Endpoint associated with this Location Endpoint.")


class LocationDomainResourceText(models.Model):
    _name = "hc.location.domain.resource.text"
    _description = "Location Domain Resource Text"
    _inherit = ["hc.basic.association", "hc.narrative"]

    location_id = fields.Many2one(
        comodel_name="hc.res.location",
        string="Location",
        help="Location associated with this Location Domain Resource Text.")

class LocationDomainResourceContained(models.Model):
    _name = "hc.location.domain.resource.contained"
    _description = "Location Domain Resource Contained"
    _inherit = ["hc.basic.association", "hc.resource"]

    location_id = fields.Many2one(
        comodel_name="hc.res.location",
        string="Location",
        help="Location associated with this Location Domain Resource Contained.")

class LocationDomainResourceExtension(models.Model):
    _name = "hc.location.domain.resource.extension"
    _description = "Location Domain Resource Extension"
    _inherit = ["hc.basic.association", "hc.extension"]

    location_id = fields.Many2one(
        comodel_name="hc.res.location",
        string="Location",
        help="Location associated with this Location Domain Resource Extension.")

class LocationDomainResourceModifierExtension(models.Model):
    _name = "hc.location.domain.resource.modifier.extension"
    _description = "Location Domain Resource Modifier Extension"
    _inherit = ["hc.basic.association", "hc.extension"]

    location_id = fields.Many2one(
        comodel_name="hc.res.location",
        string="Location",
        help="Location associated with this Location Domain Resource Modifier Extension.")

class BedStatus(models.Model):
    _name = "hc.vs.bed.status"
    _description = "Bed Status"
    _inherit = ["hc.value.set.contains"]

    name = fields.Char(
        string="Name",
        help="Name of this bed status.")
    code = fields.Char(
        string="Code",
        help="Code of this bed status.")
    contains_id = fields.Many2one(
        comodel_name="hc.vs.bed.status",
        string="Parent",
        help="Parent bed status.")

class ServiceDeliveryLocationRoleType(models.Model):
    _name = "hc.vs.service.delivery.location.role.type"
    _description = "Service Delivery Location Role Type"
    _inherit = ["hc.value.set.contains"]

    name = fields.Char(
        string="Name",
        help="Name of this service delivery location role type.")
    code = fields.Char(
        string="Code",
        help="Code of this service delivery location role type.")
    contains_id = fields.Many2one(
        comodel_name="hc.vs.service.delivery.location.role.type",
        string="Parent",
        help="Parent service delivery location role type.")

class LocationPhysicalType(models.Model):
    _name = "hc.vs.location.physical.type"
    _description = "Location Physical Type"
    _inherit = ["hc.value.set.contains"]

    name = fields.Char(
        string="Name",
        help="Name of this location physical type.")
    code = fields.Char(
        string="Code",
        help="Code of this location physical type.")
    contains_id = fields.Many2one(
        comodel_name="hc.vs.location.physical.type",
        string="Parent",
        help="Parent location physical type.")

# External Reference

class OrganizationLocation(models.Model):
    _inherit = ["hc.organization.location"]

    location_id = fields.Many2one(
        comodel_name="hc.res.location",
        string="Location",
        help="Location associated with this Organization Location.")
