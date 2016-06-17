# -*- coding: utf-8 -*-

from openerp import models, fields, api

class Person(models.Model): 

    _name = "hc.res.person" 
    _description = "Person"
    _inherits = {"res.partner": "partner_id"}

    name_id = fields.Many2one(
        comodel_name="hc.human.name",
        string="Full Name",
        help="Person's First Name and Last Name")
    identifier_ids = fields.One2many(
        comodel_name="hc.person.identifier", 
        inverse_name="person_id", 
        string="Identifiers", 
        help="A human identifier for this person.")
    name_ids = fields.One2many(
        comodel_name="hc.person.name", 
        inverse_name="person_id", 
        string="Names", 
        help="A name associated with the person.")
    telecom_contact_ids = fields.One2many(
        comodel_name="hc.person.telecom", 
        inverse_name="person_id", 
        string="Telecom Contacts", 
        help="A contact detail for the person.")
    gender = fields.Selection(
        string="Gender", 
        selection=[
            ("male", "Male"), 
            ("female", "Female"), 
            ("other", "Other"), 
            ("unknown", "Unknown")],          
        help="The gender of a person used for administrative purposes.")
    birthdate = fields.Date(
        string="Birth Date", 
        help="The birth date for the person.")
    address_ids = fields.One2many(
        comodel_name="hc.person.address", 
        inverse_name="person_id", 
        string="Addresses", 
        help="One or more addresses for the person.")
    attachment_ids = fields.One2many(
        comodel_name="hc.person.attachment", 
        inverse_name="person_id", 
        string="Attachments", 
        help="Image of the Person.")
#     managing_organization_id = fields.Many2one(comodel_name="hc.res.organization", string="Managing Organization", help="The Organization that is the custodian of the person record.")
    is_active = fields.Boolean(
        string="Active", 
        help="This person's record is in active use.")
    link_ids = fields.One2many(
        comodel_name="hc.person.link", 
        inverse_name="person_id", 
        string="Person Links", 
        help="Link to a resource that concerns the same actual person.")
    partner_id = fields.Many2one(
        comodel_name="res.partner", 
        string="Partner", 
        required=True, 
        ondelete="restrict", 
        help="Partner associated with this person.")

    @api.model
    def create(self, vals):
        name = self.env['hc.human.name'].browse(vals['name_id'])
        vals['name'] = name.first_id.name+' '+name.surname_id.name
        return super(Person, self).create(vals)

class PersonLink(models.Model): 

    _name = "hc.person.link"    
    _description = "Person Link"

    person_id = fields.Many2one(
        comodel_name="hc.res.person", 
        string="Person", 
        help="Person associated with this person link.")
#    target_patient_id = fields.Many2one(comodel_name="hc.res.patient", string="Target Patient", required=True, help="Patient who is the resource to which this actual person is associated.")
#    target_related_practitioner_id = fields.Many2one(comodel_name="hc.res.practitioner", string="Target Practitioner", help="Practitioner who is the resource to which this actual person is associated.")
#    target_related_person_id = fields.Many2one(comodel_name="hc.res.related.person", string="Target Related Person", help="Related Person who is the resource to which this actual person is associated.")
    target_person_id = fields.Many2one(
        comodel_name="hc.res.person", 
        string="Target Person", 
        help="Person who is the resource to which this actual person is associated.")
    assurance_level = fields.Selection(
        string="Link Assurance Level", 
        selection=[
            ("level1", "Level1"), 
            ("level2", "Level2"), 
            ("level3", "Level3"), 
            ("level4", "Level4")], 
        help="Level of assurance that this link is actually associated with the target resource.")

class PersonAddress(models.Model):

    _name = "hc.person.address" 
    _description = "Person Address"
    _inherit = ["hc.basic.association"]
    _inherits = {"hc.address": "address_id"}

    person_id = fields.Many2one(
        comodel_name="hc.res.person", 
        string="Person", 
        help="Entity associated with this address.")
    address_id = fields.Many2one(
        comodel_name="hc.address", 
        string="Address", 
        required=True,
        ondelete="restrict", 
        help="Address associated with this entity.") 
    use = fields.Selection(string="Use",
        selection=[
            ("home", "Home"), 
            ("work", "Work"), 
            ("temp", "Temp"), 
            ("old", "Old")],
        default="home",  
        help="The purpose of this address.")
    type = fields.Selection(string="Type", 
        selection=[
            ("postal", "Postal"), 
            ("physical", "Physical"), 
            ("both", "Both")], 
        default="both", 
        help="Distinguishes between physical addresses (those you can visit) and mailing addresses (e.g. PO Boxes and care-of addresses). Most addresses are both.")

class PersonIdentifier(models.Model):   
    _name = "hc.person.identifier"  
    _description = "Person Identifier"
    _inherit = ["hc.basic.association"]

    person_id = fields.Many2one(
        comodel_name="hc.res.person", 
        string="Person", 
        help="Person associated with this identifier.")
    identifier_id = fields.Many2one(
        comodel_name="hc.identifier", 
        string="Identifier", 
        required=True,
        ondelete="restrict", 
        help="Identifier associated with this person.")
    value = fields.Char(
        string="Value", 
        help="The value of this identifier that is unique.")

class PersonName(models.Model): 
    _name = "hc.person.name"    
    _description = "Person Name"
    _inherit = ["hc.basic.association"]
    _inherits = {"hc.human.name": "human_name_id"}

    person_id = fields.Many2one(
        comodel_name="hc.res.person", 
        string="Person", 
        help="Entity associated with this name.")
    human_name_id = fields.Many2one(
        comodel_name="hc.human.name", 
        string="Human Name", 
        required=True,
        ondelete="restrict", 
        help="Name associated with this entity.")
        
class PersonTelecom(models.Model):  
    _name = "hc.person.telecom" 
    _description = "Person Telecom"
    _inherit = ["hc.entity.telecom"]
 
    person_id = fields.Many2one(
        comodel_name="hc.res.person", 
        string="Person", 
        help="Entity associated with this telecom contact point.")

    telecom_id = fields.Many2one(
        help="Telecom contact point associated with this person.")
     
class PersonAttachment(models.Model):   
    _name = "hc.person.attachment"  
    _description = "Person Attachment"
    _inherit = ["hc.basic.association"]
    _inherits = {"hc.attachment": "attachment_id"}

    person_id = fields.Many2one(
        comodel_name="hc.res.person", 
        string="Person", 
        help="Entity associated with this attachment.")      
    attachment_id = fields.Many2one(
        comodel_name="hc.attachment", 
        string="Attachment",
        required=True,
        ondelete="restrict",  
        help="Attachment associated with this entity.")