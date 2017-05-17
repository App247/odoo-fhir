# -*- coding: utf-8 -*-

from openerp import models, fields, api

class Organization(models.Model):   
    _name = "hc.res.organization"   
    _description = "Organization"       
    _inherits = {"res.partner": "partner_id"}

    partner_id = fields.Many2one(
        comodel_name="res.partner", 
        string="Partner", 
        required="True", 
        ondelete="restrict", 
        help="Partner associated with this organization.")
    identifier_ids = fields.One2many(
        comodel_name="hc.organization.identifier", 
        inverse_name="organization_id", 
        string="Identifiers", 
        help="Identifies this organization across multiple systems.")             
    is_active = fields.Boolean(
        string="Active",
        default="True", 
        help="Whether the organization's record is still in active use.") 
    type_id = fields.Many2one(
        comodel_name="hc.vs.organization.type", 
        string="Type", 
        help="Kind of organization.") 
    name = fields.Char(
        string="Name", 
        help="Name used for the organization.")                      
    alias_ids = fields.One2many(
        comodel_name="hc.organization.alias", 
        inverse_name="organization_id", 
        string="Aliases", 
        help="A list of alternative names that theorganiation is knwn as or was known as in the past.")
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
    endpoint_ids = fields.One2many(
        comodel_name="hc.organization.endpoint", 
        inverse_name="organization_id", 
        string="Endpoints", 
        help="Technical endpoints providing access to services operated for the organization.")
    location_ids = fields.One2many(
        comodel_name="hc.organization.location", 
        inverse_name="organization_id", 
        string="Location", 
        help="A location for this organization.") 
    company_id = fields.Many2one(
        comodel_name="res.company", 
        string="Company", 
        help="The company associated with this organization.")                   
            
    _defaults = {
        "is_company": True,
        "customer": False,
        "company_type": "company",
        }

class OrganizationContact(models.Model):    
    _name = "hc.organization.contact"   
    _description = "Organization Contact"       
    _inherits = {"hc.res.person": "person_id"}

    person_id = fields.Many2one(
        comodel_name="hc.res.person", 
        string="Person",
        required="True",
        ondelete="restrict", 
        help="Person associated with this Organization Contact.") 
    organization_id = fields.Many2one(
        comodel_name="hc.res.organization", 
        string="Organization", 
        help="Organization associated with this Organization Contact.")
    purpose_id = fields.Many2one(
        comodel_name="hc.vs.contact.entity.type", 
        string="Purpose", 
        help="The type of contact.")              
    name_id = fields.Many2one(
        comodel_name="hc.organization.contact.name", 
        string="Name", 
        help="A name associated with the contact.")              
    telecom_ids = fields.One2many(
        comodel_name="hc.organization.contact.telecom", 
        inverse_name="contact_id", 
        string="Telecoms", 
        help="Contact details (telephone, email, etc.) for the organization contact.")             
    address_ids = fields.One2many(
        comodel_name="hc.organization.contact.address",
        inverse_name="contact_id",  
        string="Addresses", 
        help="Visiting or postal addresses for the organization contact.")

class OrganizationIdentifier(models.Model):   
    _name = "hc.organization.identifier"  
    _description = "Organization Identifier"
    _inherit = ["hc.basic.association", "hc.identifier"]

    organization_id = fields.Many2one(
        comodel_name="hc.res.organization", 
        string="Organization", 
        help="Organization associated with this identifier.")

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

    organization_id = fields.Many2one(
        comodel_name="hc.res.organization", 
        string="Organization", 
        help="Organization associated with this Organization Endpoint.")                       
    # endpoint_id = fields.Many2one(
    #     comodel_name="hc.res.endpoint", 
    #     string="Endpoint", 
    #     help="Endpoint associated with this Organization Endpoint.")                       

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

class OrganizationContactName(models.Model): 
    _name = "hc.organization.contact.name"    
    _description = "Organization Contact Name"
    _inherit = ["hc.basic.association"]
    _inherits = {"hc.human.name": "name_id"}

    name_id = fields.Many2one(
        comodel_name="hc.human.name",
        string="Human Name",
        required="True",
        ondelete="restrict", 
        help="Human Name associated with this Organization Contact Name.")

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
        string="Contact", 
        help="Contact associated with this Organization Contact Telecom.")                    

class OrganizationContactAddress(models.Model):
    _name = "hc.organization.contact.address" 
    _description = "Organization Contact Address"
    _inherit = ["hc.address.use"]
    _inherits = {"hc.address": "address_id"}

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

# External Reference

class Partner(models.Model):
    _inherit = ["res.partner"]

    is_organization = fields.Boolean(
        string="Is an Organization", 
        help="This partner is a health care-related organization record.")     
    is_organization_contact = fields.Boolean(
        string="Is an Organization Contact", 
        help="This partner is an organization contact.")

class IdentifierCode(models.Model):
    _inherit = ["hc.vs.identifier.code"]

    assigner_id = fields.Many2one(
        comodel_name="hc.res.organization", 
        string="Assigner Organization", 
        help="Organization that issued id (may be just text).")

class Person(models.Model):
    _inherit = ["hc.res.person"]

    managing_organization_id = fields.Many2one(
        comodel_name="hc.res.organization", 
        string="Managing Organization", 
        help="Organization that is the custodian of the person record.")

class Signature(models.AbstractModel):    
    _inherit = "hc.signature"

    who_organization_id = fields.Many2one(
        comodel_name="hc.res.organization", 
        string="Who Organization", 
        help="Organization who signed.") 

    on_behalf_of_organization_id = fields.Many2one(
        comodel_name="hc.res.organization", 
        string="On Behalf Of Organization", 
        help="Organization the party represented.") 
