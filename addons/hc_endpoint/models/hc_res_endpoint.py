# -*- coding: utf-8 -*-

from openerp import models, fields, api

class Endpoint(models.Model):
    _name = "hc.res.endpoint"
    _description = "Endpoint"
    _inherit = "hc.domain.resource"
    _rec_name = "name"

    identifier_ids = fields.One2many(
        comodel_name="hc.endpoint.identifier",
        inverse_name="endpoint_id",
        string="Identifiers",
        help="Identifies this endpoint across multiple systems.")
    status = fields.Selection(
        string="Status",
        required="True",
        selection=[
            ("active", "Active"),
            ("suspended", "Suspended"),
            ("error", "Error"),
            ("off", "Off"),
            ("entered-in-error", "Entered-In-Error")],
        help="The status of the encounter.")
    connection_type_id = fields.Many2one(
        comodel_name="hc.vs.endpoint.connection.type",
        string="Connection Type",
        required="True",
        help="Protocol/Profile/Standard to be used with this endpoint connection.")
    name = fields.Char(
        string="Name",
        help="A name that this endpoint can be identified by.")
    managing_organization_id = fields.Many2one(
        comodel_name="hc.res.organization",
        string="Managing Organization",
        help="Organization that manages this endpoint (may not be the organization that exposes the endpoint).")
    contact_ids = fields.One2many(
        comodel_name="hc.endpoint.telecom",
        inverse_name="endpoint_id",
        string="Telecom",
        help="Contact details for source (e.g. troubleshooting).")
    period_start_date = fields.Datetime(
        string="Period Start Date",
        help="Start of the interval during responsibility is assumed.")
    period_end_date = fields.Datetime(
        string="Period End Date",
        help="End of the interval during responsibility is assumed.")
    # payload_type_ids = fields.Many2many(
        # comodel_name="hc.vs.endpoint.payload.type", # Based on FHIR Specification
        # string="Payload Types",
        # required="True",
        # help="The type of content that may be used at this endpoint (e.g. XDS Discharge summaries).")
    payload_type_ids = fields.Many2many(
        comodel_name="hc.vs.resource.type", # Based on XML Endpoint Example
        string="Payload Types",
        required="True",
        help="The type of content that may be used at this endpoint (e.g. XDS Discharge summaries).")
    payload_mime_type_ids = fields.Many2many(
        comodel_name="hc.vs.mime.type",
        string="Payload MIME Types",
        help="Mimetype to send. If not specified, the content could be anything (including no payload, if the connectionType defined this).")
    address_uri = fields.Char(
        string="Address URI",
        required="True",
        help="Where the channel points to.")
    header_ids = fields.One2many(
        comodel_name="hc.endpoint.header",
        inverse_name="endpoint_id",
        string="Headers",
        help="Usage depends on the channel type.")

class EndpointIdentifier(models.Model):
    _name = "hc.endpoint.identifier"
    _description = "Endpoint Identifier"
    _inherit = ["hc.basic.association", "hc.identifier"]

    endpoint_id = fields.Many2one(
        comodel_name="hc.res.endpoint",
        string="Endpoint",
        help="Endpoint associated with this endpoint identifier.")

class EndpointTelecom(models.Model):
    _name = "hc.endpoint.telecom"
    _description = "Endpoint Telecom"
    _inherit = ["hc.contact.point.use"]
    _inherits = {"hc.contact.point": "telecom_id"}

    telecom_id = fields.Many2one(
        comodel_name="hc.contact.point",
        string="Contact",
        ondelete="restrict",
        required="True",
        help="Contact associated with this Endpoint Telecom.")
    endpoint_id = fields.Many2one(
        comodel_name="hc.res.endpoint",
        string="Endpoint",
        help="Endpoint associated with this Endpoint Telecom.")

class EndpointHeader(models.Model):
    _name = "hc.endpoint.header"
    _description = "Endpoint Header"
    _inherit = ["hc.basic.association"]

    endpoint_id = fields.Many2one(
        comodel_name="hc.res.endpoint",
        string="Endpoint",
        help="Endpoint associated with this Endpoint Header.")
    header = fields.Char(
        string="Header",
        help="Usage depends on the channel type.")

class EndpointConnectionType(models.Model):
    _name = "hc.vs.endpoint.connection.type"
    _description = "Endpoint Connection Type"
    _inherit = ["hc.value.set.contains"]

    name = fields.Char(
        string="Name",
        help="Name of this endpoint connection type.")
    code = fields.Char(
        string="Code",
        help="Code of this endpoint connection type.")
    contains_id = fields.Many2one(
        comodel_name="hc.vs.endpoint.connection.type",
        string="Parent",
        help="Parent endpoint connection type.")

class EndpointPayloadType(models.Model):
    _name = "hc.vs.endpoint.payload.type"
    _description = "Endpoint Payload Type"
    _inherit = ["hc.value.set.contains"]

    name = fields.Char(
        string="Name",
        help="Name of this endpoint payload type.")
    code = fields.Char(
        string="Code",
        help="Code of this endpoint payload type.")
    contains_id = fields.Many2one(
        comodel_name="hc.vs.endpoint.payload.type",
        string="Parent",
        help="Parent endpoint payload type.")

# External Reference

class OrganizationEndpoint(models.Model):
    _inherit = "hc.organization.endpoint"

    endpoint_id = fields.Many2one(
        comodel_name="hc.res.endpoint",
        string="Endpoint",
        help="Endpoint associated with this Organization Endpoint.")
