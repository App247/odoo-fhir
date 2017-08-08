# -*- coding: utf-8 -*-

from openerp import models, fields, api
from datetime import datetime
from openerp.tools import DEFAULT_SERVER_DATE_FORMAT as DF
from openerp.tools import DEFAULT_SERVER_DATETIME_FORMAT as DTF

class PractitionerRole(models.Model):
    _name = "hc.res.practitioner.role"
    _description = "Practitioner Role"
    _inherit = ["hc.domain.resource"]
    _rec_name = "name"

    name = fields.Char(
        string="Name",
        compute="_compute_name",
        store="True",
        help="Text representation of the practitioner role. Practitioner + Organization + Period Start Date.")
    identifier_ids = fields.One2many(
        comodel_name="hc.practitioner.role.identifier",
        inverse_name="practitioner_role_id",
        string="Identifiers",
        help="Business Identifiers that are specific to a role/location.")
    is_active = fields.Boolean(
        string="Active",
        help="Whether this practitioner role record is in active use.")
    period_start_date = fields.Datetime(
        string="Period Start Date",
        help="Start of the the period during which the practitioner is authorized to perform in these role(s).")
    period_end_date = fields.Datetime(
        string="Period End Date",
        help="End of the the period during which the practitioner is authorized to perform in these role(s).")
    practitioner_id = fields.Many2one(
        comodel_name="hc.res.practitioner",
        string="Practitioner",
        help="Practitioner that is able to provide the defined services for the organization.")
    organization_id = fields.Many2one(
        comodel_name="hc.res.organization",
        string="Organization",
        help="Organization where the roles are performed.")
    role_ids = fields.Many2many( # named "code" in standard
        comodel_name="hc.vs.practitioner.role",
        relation="practitioner_role_role_rel",
        string="Roles",
        help="Roles which this practitioner may perform.")
    specialty_ids = fields.Many2many(
        comodel_name="hc.vs.c80.practice.code",
        relation="practitioner_role_specialty_rel",
        string="Specialties",
        help="Specific specialty of the practitioner.")
    location_ids = fields.Many2many(
        comodel_name="hc.practitioner.role.location",
        inverse_name="practitioner_role_id",
        relation="location_practitioner_role_rel",
        string="Locations",
        help="The location(s) at which this practitioner provides care.")
    healthcare_service_ids = fields.One2many(
        comodel_name="hc.practitioner.role.healthcare.service",
        inverse_name="practitioner_role_id",
        string="Healthcare Services",
        help="The list of healthcare services that this worker provides for this role's Organization/Location(s).")
    telecom_ids = fields.One2many(
        comodel_name="hc.practitioner.role.telecom",
        inverse_name="practitioner_role_id",
        string="Telecoms",
        help="Contact details that are specific to the role/location/service.")
    availability_exceptions = fields.Text(
        string="Availability Exceptions",
        help="Description of availability exceptions.")
    endpoint_ids = fields.One2many(
        comodel_name="hc.practitioner.role.endpoint",
        inverse_name="practitioner_role_id",
        string="Endpoints",
        help="Technical endpoints providing access to services operated for the practitioner with this role.")

    @api.depends('practitioner_id', 'organization_id', 'period_start_date')
    def _compute_name(self):
        comp_name = '/'
        for hc_res_practitioner_role in self:
            if hc_res_practitioner_role.practitioner_id:
                comp_name = hc_res_practitioner_role.practitioner_id.name or ''
            if hc_res_practitioner_role.organization_id:
                comp_name = comp_name + ", " + hc_res_practitioner_role.organization_id.name or ''
            if hc_res_practitioner_role.period_start_date:
                period_start_date = datetime.strftime(datetime.strptime(hc_res_practitioner_role.period_start_date, DTF), "%Y-%m-%d")
                comp_name = comp_name + ", " + period_start_date
            hc_res_practitioner_role.name = comp_name

class PractitionerRoleAvailableTime(models.Model):
    _name = "hc.practitioner.role.available.time"
    _description = "Practitioner Role Available Time"
    _inherit =["hc.available.time"]

    practitioner_role_id = fields.Many2one(
        comodel_name="hc.res.practitioner.role",
        string="Practitioner Role",
        help="Practitioner Role associated with Practitioner Role Available Time.")

class PractitionerRoleNotAvailableTime(models.Model):
    _name = "hc.practitioner.role.not.available.time"
    _description = "Practitioner Role Not Available Time"
    _inherit =["hc.not.available.time"]

    practitioner_role_id = fields.Many2one(
        comodel_name="hc.res.practitioner.role",
        string="Practitioner Role",
        help="Practitioner Role associated with Practitioner Role Not Available Time.")

class PractitionerRoleIdentifier(models.Model):
    _name = "hc.practitioner.role.identifier"
    _description = "Practitioner Role Identifier"
    _inherits = {"hc.person.identifier": "person_identifier_id"}

    person_identifier_id = fields.Many2one(
        comodel_name="hc.person.identifier",
        string="Person Identifier",
        required="True",
        ondelete="restrict",
        help="Person Identifier associated with this Practitioner Role Identifier.")
    practitioner_role_id = fields.Many2one(
        comodel_name="hc.res.practitioner.role",
        string="Practitioner Role",
        help="Practitioner Role associated with this Practitioner Role Identifier.")

class PractitionerRoleLocation(models.Model):
    _name = "hc.practitioner.role.location"
    _description = "Practitioner Role Location"
    _inherit = ["hc.basic.association"]

    practitioner_role_id = fields.Many2one(
        comodel_name="hc.res.practitioner.role",
        string="Practitioner Role",
        help="Practitioner Role associated with this Practitioner Role Location.")
    location_id = fields.Many2one(
        comodel_name="hc.res.location",
        string="Location",
        help="Location associated with this Practitioner Role Location.")

class PractitionerRoleHealthcareService(models.Model):
    _name = "hc.practitioner.role.healthcare.service"
    _description = "Practitioner Role Healthcare Service"
    _inherit = ["hc.basic.association"]

    practitioner_role_id = fields.Many2one(
        comodel_name="hc.res.practitioner.role",
        string="Practitioner Role",
        help="Practitioner Role associated with this Practitioner Role Healthcare Service.")
    healthcare_service_id = fields.Many2one(
        comodel_name="hc.res.healthcare.service",
        string="Healthcare Service",
        help="Healthcare Service associated with this Practitioner Role Healthcare Service.")

class PractitionerRoleTelecom(models.Model):
    _name = "hc.practitioner.role.telecom"
    _description = "Practitioner Role Telecom"
    _inherit = ["hc.contact.point.use"]
    _inherits = {"hc.contact.point": "telecom_id"}

    telecom_id = fields.Many2one(
        comodel_name="hc.contact.point",
        string="Telecom",
        ondelete="restrict",
        required="True",
        help="Telecom associated with this Practitioner Role Telecom.")
    practitioner_role_id = fields.Many2one(
        comodel_name="hc.res.practitioner.role",
        string="Practitioner Role",
        help="Practitioner Role associated with this Practitioner Role Telecom.")

class PractitionerRoleEndpoint(models.Model):
    _name = "hc.practitioner.role.endpoint"
    _description = "Practitioner Role Endpoint"
    _inherit = ["hc.basic.association"]

    practitioner_role_id = fields.Many2one(
        comodel_name="hc.res.practitioner.role",
        string="Practitioner Role",
        help="Practitioner Role associated with this Practitioner Role Endpoint.")
    endpoint_id = fields.Many2one(
        comodel_name="hc.res.endpoint",
        string="Endpoint",
        help="Endpoint associated with this Practitioner Role Endpoint.")

class PractitionerRoleRole(models.Model):
    _name = "hc.vs.practitioner.role"
    _description = "Practitioner Role"
    _inherit = ["hc.value.set.contains"]

# External Reference

class PractitionerPractitionerRole(models.Model):
    _inherit = "hc.practitioner.practitioner.role"

    role_id = fields.Many2one(
        comodel_name="hc.res.practitioner.role",
        string="Role",
        help="Practitioner Role associated with this Practitioner Practitioner Role.")
