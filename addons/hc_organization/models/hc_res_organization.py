# -*- coding: utf-8 -*-

from openerp import models, fields, api
from datetime import datetime

class Organization(models.Model):
    _name = "hc.res.organization"
    _description = "Organization"
    _inherit = "hc.domain.resource"
    _rec_name = "name"

    partner_id = fields.Many2one(
        comodel_name="res.partner",
        string="Partner",
        domain="[('company_type','=','company')]",
        help="Partner associated with this organization.")
    identifier_ids = fields.One2many(
        comodel_name="hc.organization.identifier",
        inverse_name="organization_id",
        string="Identifiers",
        help="Identifies this organization across multiple systems.")
    is_active = fields.Boolean(
        string="Active",
        help="Whether the organization's record is still in active use.")
    type_ids = fields.Many2many(
        comodel_name="hc.vs.organization.type",
        string="Type",
        help="Kind of organization.")
    name = fields.Char(
        string="Name",
        help="Name used for the organization.")
    telecom_ids = fields.One2many(
        comodel_name="hc.organization.telecom",
        inverse_name="organization_id",
        string="Telecoms",
        help="A contact detail for the organization.")
    address_ids = fields.One2many(
        comodel_name="hc.organization.address",
        inverse_name="organization_id",
        string="Addresses",
        help="An address for the organization.")
    part_of_id = fields.Many2one(
        comodel_name="hc.res.organization",
        string="Part Of",
        help="The organization of which this organization forms a part.")
    contact_ids = fields.One2many(
        comodel_name="hc.organization.contact",
        inverse_name="organization_id",
        string="Contacts",
        help="A location for this organization.")
    endpoint_ids = fields.One2many(
        comodel_name="hc.organization.endpoint",
        inverse_name="organization_id",
        string="Endpoints",
        help="Technical endpoints providing access to services operated for the organization.")

    # Extension not in FHIR Specification
    location_ids = fields.One2many(
        comodel_name="hc.organization.location",
        inverse_name="organization_id",
        string="Location",
        help="A location for this organization.")
    # Odoo extension
    company_id = fields.Many2one(
        comodel_name="res.company",
        string="Company",
        help="The company associated with this organization.")

    # Extension Backbone Element
    alias_ids = fields.One2many(
        comodel_name="hc.organization.alias",
        inverse_name="organization_id",
        string="Aliases",
        help="A list of alternative names that the organization is known as or was known as in the past.")
    start_date = fields.Datetime(
        string="Start Date",
        help="Start of the date range that this organization should be considered available.")
    end_date = fields.Datetime(
        string="End Date",
        help="End of the date range that this organization should be considered available.")
    accreditation_ids = fields.One2many(
        comodel_name="hc.organization.accreditation",
        inverse_name="organization_id",
        string="Accreditations",
        help="")

    # Domain Resource
    text_id = fields.Many2one(
        comodel_name="hc.organization.domain.resource.text")
    contained_ids = fields.One2many(
        comodel_name="hc.organization.domain.resource.contained",
        inverse_name="organization_id")
    extension_ids = fields.One2many(
        comodel_name="hc.organization.domain.resource.extension",
        inverse_name="organization_id")
    modifier_extension_ids = fields.One2many(
        comodel_name="hc.organization.domain.resource.modifier.extension",
        inverse_name="organization_id")

    _defaults = {
        "is_company": True,
        "customer": False,
        "company_type": "company",
        }

    # For new record, create Partner and Partner Link records.

    @api.model
    def create(self, vals):
        partner_obj = self.env['res.partner'] # Variable to create partner
        partner_link_obj = self.env['hc.partner.link'] # Variable to create partner link
        # name = self.env['hc.organization.name'].browse(vals['name_id']) # Variable to create name of an organization
        # name = vals.get('name', self.env.user.name)
        # name = self._context.copy()
        # name = name

        res = super(Organization, self).create(vals)
        if not vals.get('partner_id'):
            partner_id = partner_obj.create({
                'company_type': 'company',
                'is_company': True,
                'is_organization': True,
                'is_healthcare': True,
                'name': res.name,
                })
            vals.update({'partner_id': partner_id.id})
        vals.update({'name': res.name})

        # names_vals = {}
        link = partner_link_obj.create({
            'link_type': 'organization',
            'link_organization_id': res.id,
            'partner_id': vals.get('partner_id'),
            'start_date': datetime.today(),
            })

        return res

class OrganizationContact(models.Model):
    _name = "hc.organization.contact"
    _description = "Organization Contact"
    _inherit = "hc.backbone.element"
    _inherits = {"hc.res.person": "person_id"}
    _rec_name = "person_id"

    person_id = fields.Many2one(
        comodel_name="hc.res.person",
        string="Person",
        required="True",
        ondelete="restrict",
        help="Person associated with this Organization Contact.")
    name_id = fields.Many2one(
        related="person_id.name_id",
        string="Name",
        help="A name associated with the contact.")
    organization_id = fields.Many2one(
        comodel_name="hc.res.organization",
        string="Organization",
        help="Organization associated with this Organization Contact.")
    purpose_id = fields.Many2one(
        comodel_name="hc.vs.contact.entity.type",
        string="Purpose",
        help="The type of contact.")
    telecom_ids = fields.One2many(
        comodel_name="hc.organization.contact.telecom",
        inverse_name="contact_id",
        string="Telecoms",
        help="Contact details (telephone, email, etc.)  for a contact.")
    address_id = fields.Many2one(
        comodel_name="hc.organization.contact.address",
        string="Address",
        help="Visiting or postal addresses for the contact.")

    # Extension Backbone Element
    preferred_contact = fields.Boolean(
        string="Preferred Contact",
        help="This Contact is the preferred contact at this organization for the purpose of the contact. There can be multiple contacts on an Organizations record with this value set to true, but these should all have different purpose values.")


class OrganizationIdentifier(models.Model):
    _name = "hc.organization.identifier"
    _description = "Organization Identifier"
    _inherit = ["hc.basic.association", "hc.identifier", "hc.identifier.use"]

    organization_id = fields.Many2one(
        comodel_name="hc.res.organization",
        string="Organization",
        help="Organization associated with this Organization Identifier.")

class OrganizationAlias(models.Model):
    _name = "hc.organization.alias"
    _description = "Organization Alias"
    _inherit = ["hc.basic.association"]

    organization_id = fields.Many2one(
        comodel_name="hc.res.organization",
        string="Organization",
        help="Organization associated with this Organization Alias.")
    alias = fields.Char(
        string="Alias",
        help="Alias associated with this Organization Alias.")

class OrganizationAccreditation(models.Model):
    _name = "hc.organization.accreditation"
    _description = "Organization Accreditation"
    _inherit = ["hc.basic.association", "hc.identifier", "hc.identifier.use"]

    organization_id = fields.Many2one(
        comodel_name="hc.res.organization",
        string="Organization",
        help="Organization associated with this Organization Accreditation.")

class OrganizationTelecom(models.Model):
    _name = "hc.organization.telecom"
    _description = "Organization Telecom"
    _inherit = ["hc.contact.point.use"]
    _inherits = {"hc.contact.point": "telecom_id"}

    telecom_id = fields.Many2one(
        comodel_name="hc.contact.point",
        string="Telecom",
        ondelete="restrict",
        required="True",
        help="Telecom associated with this Organization Telecom.")
    organization_id = fields.Many2one(
        comodel_name="hc.res.organization",
        string="Organization",
        help="Organization associated with this Organization Telecom.")

class OrganizationAddress(models.Model):
    _name = "hc.organization.address"
    _description = "Organization Address"
    _inherit = ["hc.address.use"]
    _inherits = {"hc.address": "address_id"}

    address_id = fields.Many2one(
        comodel_name="hc.address",
        string="Address",
        required="True",
        ondelete="restrict",
        help="Address associated with this Organization Address.")
    organization_id = fields.Many2one(
        comodel_name="hc.res.organization",
        string="Organization",
        help="Organization associated with this Organization Address.")

class OrganizationEndpoint(models.Model):
    _name = "hc.organization.endpoint"
    _description = "Organization Endpoint"
    _inherit = ["hc.basic.association"]

    # endpoint_id = fields.Many2one(
    #     comodel_name="hc.res.endpoint",
    #     string="Endpoint",
    #     help="Endpoint associated with this Organization Endpoint.")
    organization_id = fields.Many2one(
        comodel_name="hc.res.organization",
        string="Organization",
        help="Organization associated with this Organization Endpoint.")

class OrganizationContactTelecom(models.Model):
    _name = "hc.organization.contact.telecom"
    _description = "Organization Contact Telecom"
    _inherit = ["hc.contact.point.use"]
    _inherits = {"hc.contact.point": "telecom_id"}

    telecom_id = fields.Many2one(
        comodel_name="hc.contact.point",
        string="Telecom",
        ondelete="restrict",
        required="True",
        help="Telecom associated with this Organization Contact Telecom.")
    contact_id = fields.Many2one(
        comodel_name="hc.organization.contact",
        string="Organization Contact",
        help="Organization Contact associated with this Organization Contact Telecom.")

class OrganizationContactAddress(models.Model):
    _name = "hc.organization.contact.address"
    _description = "Organization Contact Address"
    _inherit = ["hc.address.use"]
    _inherits = {"hc.address": "address_id"}
    _rec_name = "address_id"

    address_id = fields.Many2one(
        comodel_name="hc.address",
        string="Address",
        required="True",
        ondelete="restrict",
        help="Address associated with this Organization Contact Address.")
    contact_id = fields.Many2one(
        comodel_name="hc.organization.contact",
        string="Organization Contact",
        help="Organization Contact associated with this Organization Contact Address.")

class OrganizationLocation(models.Model):
    _name = "hc.organization.location"
    _description = "Organization Location"
    _inherit = ["hc.basic.association"]

    organization_id = fields.Many2one(
        comodel_name="hc.res.organization",
        string="Organization",
        help="Organization associated with this Organization Location.")
    # location_id = fields.Many2one(
    #     comodel_name="hc.res.location",
    #     string="Location",
    #     help="Location associated with this Organization Location.")

class OrganizationType(models.Model):
    _name = "hc.vs.organization.type"
    _description = "Organization Type"
    _inherit = ["hc.value.set.contains"]

    name = fields.Char(
        string="Name",
        help="Name of this organization type.")
    code = fields.Char(
        string="Code",
        help="Code of this organization type.")
    contains_id = fields.Many2one(
        comodel_name="hc.vs.organization.type",
        string="Parent",
        help="Parent organization type.")
    level_attribute = fields.Char(
        compute="_get_level",
        string="Level/Parent",
        store=True,
        help="Level associated with Parent concept.")
    level = fields.Integer(
        compute="_get_level",
        string="Level",
        store=True,
        help="Level as a parent in a hierarchy of codes.")
    parent_child_ids = fields.Many2many(
        comodel_name="hc.vs.organization.type",
        relation="base_organization_type_parent_child_rel",
        column1="parent_id",
        column2="child_id",
        string="Parents",
        help="Parent act code.")
    child_parent_ids = fields.Many2many(
        comodel_name="hc.vs.organization.type",
        compute="_calc_child",
        store="True",
        relation="organization_type_child_parent_rel",
        column1="child_id",
        column2="parent_id",
        string="Children",
        help="Child organization type.")
    child_count = fields.Integer(
        string="Child Count",
        compute="_calc_child",
        store="True",
        help="Number of child members.")

    @api.constrains('parent_child_ids')
    def _check_recursive_parent_child(self):
        for rec in self:
            if rec.id in rec.parent_child_ids.ids:
                raise ValidationError('Error! A code cannot be a child of itself.')
        return True

    @api.depends('parent_child_ids')
    def _get_level(self):
        for rec in self:
            if not rec.parent_child_ids:
                rec.level = 1
                rec.level_attribute = ''
            else:
                high = 1
                attr_str = False
                for parent in rec.parent_child_ids:
                    if not attr_str:
                        attr_str = '(' + str(parent.level + 1) + ',' + parent.name +')'
                    else:
                        attr_str = attr_str + ',' + '(' + str(parent.level + 1) + ',' + parent.name + ')'
                    if parent.level > high:
                        high = parent.level
                rec.level = high + 1

    @api.depends('code')
    def _calc_child(self):
        sub_code_obj = self.env['hc.vs.organization.type']
        for rec in self:
            rec.child_parent_ids = False
            if rec.code:
                child_ids = sub_code_obj.search([('parent_child_ids.code', '=', rec.code)])
                if child_ids:
                    rec.child_count = len(child_ids)
                    rec.child_parent_ids = [(6,0,child_ids.ids)]

class ContactEntityType(models.Model):
    _name = "hc.vs.contact.entity.type"
    _description = "Contact Entity Type"
    _inherit = ["hc.value.set.contains"]

    name = fields.Char(
        string="Name",
        help="Name of this contact entity type.")
    code = fields.Char(
        string="Code",
        help="Code of this contact entity type.")
    contains_id = fields.Many2one(
        comodel_name="hc.vs.contact.entity.type",
        string="Parent",
        help="Parent contact entity type.")

# Domain Resource
class OrganizationDomainResourceText(models.Model):
    _name = "hc.organization.domain.resource.text"
    _description = "Organization Domain Resource Text"
    _inherit = ["hc.basic.association", "hc.narrative"]

    organization_id = fields.Many2one(
        comodel_name="hc.res.organization",
        string="Organization",
        help="Organization associated with this Organization Domain Resource Text.")

class OrganizationDomainResourceContained(models.Model):
    _name = "hc.organization.domain.resource.contained"
    _description = "Organization Domain Resource Contained"
    _inherit = ["hc.basic.association", "hc.resource"]

    organization_id = fields.Many2one(
        comodel_name="hc.res.organization",
        string="Organization",
        help="Organization associated with this Organization Domain Resource Contained.")

class OrganizationDomainResourceExtension(models.Model):
    _name = "hc.organization.domain.resource.extension"
    _description = "Organization Domain Resource Extension"
    _inherit = ["hc.basic.association", "hc.extension"]

    organization_id = fields.Many2one(
        comodel_name="hc.res.organization",
        string="Organization",
        help="Organization associated with this Organization Domain Resource Extension.")

class OrganizationDomainResourceModifierExtension(models.Model):
    _name = "hc.organization.domain.resource.modifier.extension"
    _description = "Organization Domain Resource Modifier Extension"
    _inherit = ["hc.basic.association", "hc.extension"]

    organization_id = fields.Many2one(
        comodel_name="hc.res.organization",
        string="Organization",
        help="Organization associated with this Organization Domain Resource Modifier Extension.")

# External Reference

class IdentifierCode(models.Model):
    _inherit = ["hc.vs.identifier.code"]

    assigner_id = fields.Many2one(
        comodel_name="hc.res.organization",
        string="Assigner Organization",
        help="Organization that issued id (may be just text).")

class Partner(models.Model):
    _inherit = ["res.partner"]

    is_organization = fields.Boolean(
        string="Is Organization",
        help="This partner is an organization.")
    is_organization_contact = fields.Boolean(
        string="Is Organization Contact",
        help="This partner is an organization contact.")

class PartnerLink(models.Model):
    _inherit = ["hc.partner.link"]

    link_type = fields.Selection(
        selection_add=[
            ("organization", "Organization"),
            ("organization_contact", "Organization Contact")])
    link_organization_id = fields.Many2one(
        comodel_name="hc.res.organization",
        string="Link Organization",
        help="Organization who is the resource to which this actual partner is associated.")
    link_organization_contact_id = fields.Many2one(
        comodel_name="hc.organization.contact",
        string="Link Organization Contact",
        help="Organization Contact who is the resource to which this actual partner is associated.")

    @api.depends('link_type')
    def _compute_link_name(self):
        for hc_partner_link in self:
            if hc_partner_link.link_type == 'person':
                hc_partner_link.link_name = hc_partner_link.link_person_id.name
            elif hc_partner_link.link_type == 'organization':
                hc_partner_link.link_name = hc_partner_link.link_organization_id.name
            elif hc_partner_link.link_type == 'organization_contact':
                hc_partner_link.link_name = hc_partner_link.link_organization_contact_id.name

class Person(models.Model):
    _inherit = ["hc.res.person"]

    managing_organization_id = fields.Many2one(
        comodel_name="hc.res.organization",
        string="Managing Organization",
        help="Organization that is the custodian of the person record.")
    is_organization_contact = fields.Boolean(
        string="Is Organization Contact",
        help="This person is an organization contact.")

class PersonLink(models.Model):
    _inherit = ["hc.person.link"]

    target_type = fields.Selection(
        selection_add=[("organization_contact", "Organization Contact")])
    target_organization_contact_id = fields.Many2one(
        comodel_name="hc.organization.contact",
        string="Target Organization Contact",
        help="Organization Contact who is the resource to which this actual person is associated.")

    @api.depends('target_type')
    def _compute_target_name(self):
        for hc_person_link in self:
            if hc_person_link.target_type == 'person':
                hc_person_link.target_name = hc_person_link.target_person_id.name
            elif hc_person_link.target_type == 'organization_contact':
                hc_person_link.target_name = hc_person_link.target_organization_contact_id.name

class Signature(models.Model):
    _inherit = ["hc.signature"]

    who_organization_id = fields.Many2one(
        comodel_name="hc.res.organization",
        string="Who Organization",
        help="Organization who signed.")
    on_behalf_of_organization_id = fields.Many2one(
        comodel_name="hc.res.organization",
        string="On Behalf Of Organization",
        help="Organization the party represented.")

    @api.depends('who_type')
    def _compute_who_name(self):
        for hc_signature in self:
            if hc_signature.who_type == 'uri':
                hc_signature.who_name = hc_signature.who_uri
            elif hc_signature.who_type == 'organization':
                hc_signature.who_name = hc_signature.who_organization_id.name

    @api.depends('on_behalf_of_type')
    def _compute_on_behalf_of_name(self):
        for hc_signature in self:
            if hc_signature.on_behalf_of_type == 'uri':
                hc_signature.on_behalf_of_name = hc_signature.on_behalf_of_uri
            elif hc_signature.on_behalf_of_type == 'organization':
                hc_signature.on_behalf_of_name = hc_signature.on_behalf_of_organization_id.name
