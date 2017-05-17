# -*- coding: utf-8 -*-

from openerp import models, fields, api

class RelatedPerson(models.Model):  
    _name = "hc.res.related.person" 
    _description = "Related Person"
    _inherits = {"hc.res.person": "person_id"}

    person_id = fields.Many2one(
        comodel_name="hc.res.person",
        string="Person",
        required="True",
        ondelete="restrict",
        help="Person who is this related person.")
    identifier_ids = fields.One2many(
        comodel_name="hc.related.person.identifier", 
        inverse_name="related_person_id", 
        string="Identifiers", 
        help="A human identifier for this related person.")     
    name_id = fields.Many2one(
        comodel_name="hc.human.name", 
        string="Name", 
        help="A name associated with this related person.")
    telecom_ids = fields.One2many(
        comodel_name="hc.related.person.telecom", 
        inverse_name="related_person_id", 
        string="Telecoms", 
        help="A contact detail for this related person.")
    gender = fields.Selection(
        related="person_id.gender",
        readonly="1",       
        help="The gender of a related person used for administrative purposes.")
    birth_date = fields.Date(
        related="person_id.birth_date",
        readonly="1", 
        help="The birth date for the related person.")
    photo_ids = fields.One2many(
        comodel_name="hc.related.person.photo", 
        inverse_name="related_person_id", 
        string="Photos", 
        help="Image of the related person.")
    patient_ids = fields.One2many(
        comodel_name="hc.related.person.patient",
        inverse_name="related_person_id", 
        string="Patients", 
        required="True", 
        help="Patient(s) related to this person.")

    _defaults = {
        "is_related_person": True,
        }
    
    @api.model
    def create(self, vals):
        vals['is_related_person'] = self.env.context.get('is_related_person', False)
        return super(RelatedPerson, self).create(vals)

class RelatedPersonIdentifier(models.Model):  
    _name = "hc.related.person.identifier" 
    _description = "Related Person Identifier"         
    _inherits = {"hc.person.identifier": "person_identifier_id"}

    person_identifier_id = fields.Many2one(
        comodel_name="hc.person.identifier", 
        string="Person Identifier",
        required="True",
        ondelete="restrict", 
        help="Person identifier associated with this related person.")
    related_person_id = fields.Many2one(
        comodel_name="hc.res.related.person", 
        string="Related Person", 
        help="Related person associated with this person identifier.")

class RelatedPersonName(models.Model): 
    _name = "hc.related.person.name"    
    _description = "Related Person Name"
    _inherit = ["hc.basic.association"]
    _inherits = {"hc.human.name": "human_name_id"}

    human_name_id = fields.Many2one(
        comodel_name="hc.human.name",
        string="Human Name",
        required="True",
        ondelete="restrict", 
        help="Human name associated with this related person name.")
    related_person_id = fields.Many2one(
        comodel_name="hc.res.related.person", 
        string="Related Person", 
        help="Related Person associated with this human name.")

class RelatedPersonTelecom(models.Model):   
    _name = "hc.related.person.telecom" 
    _description = "Related Person Telecom"     
    _inherit = ["hc.contact.point.use"] 
    _inherits = {"hc.contact.point": "telecom_id"}

    telecom_id = fields.Many2one(
        comodel_name="hc.contact.point", 
        string="Telecom", 
        ondelete="restrict", 
        required="True", 
        help="Telecom associated with this Related Person Telecom.")                  
    related_person_id = fields.Many2one(
        comodel_name="hc.res.related.person", 
        string="Related Person", 
        help="Related Person associated with this Related Person Telecom.")                  
        
class RelatedPersonAddress(models.Model):
    _name = "hc.related.person.address" 
    _description = "Related Person Address"
    _inherit = ["hc.address.use"]
    _inherits = {"hc.address": "address_id"}

    address_id = fields.Many2one(
        comodel_name="hc.address", 
        string="Address", 
        required="True",
        ondelete="restrict", 
        help="Address associated with this Related Person Address.") 
    related_person_id = fields.Many2one(
        comodel_name="hc.res.related.person", 
        string="Related Person", 
        help="Related Person associated with this Related Person Address.")

class RelatedPersonPhoto(models.Model):   
    _name = "hc.related.person.photo"  
    _description = "Related Person Photo"
    _inherits = {"hc.person.photo": "photo_id"}

    photo_id = fields.Many2one(
        comodel_name="hc.person.photo", 
        string="Photo",
        required="True",
        ondelete="restrict",  
        help="Photo associated with this Related Person Photo.")
    related_person_id = fields.Many2one(
        comodel_name="hc.res.person", 
        string="Related Person", 
        help="Related Person associated with this Related Person Photo.")      

class RelatedPersonPatient(models.Model): 
    _name = "hc.related.person.patient"    
    _description = "Related Person Patient"
    _inherit = ["hc.basic.association"]

    related_person_id = fields.Many2one(
        comodel_name="hc.res.related.person", 
        string="Related Person", 
        help="Related Person associated with this Related Person Patient.")
    # patient_id = fields.Many2one(
    #     comodel_name="hc.res.patient",
    #     string="Patient",
    #     help="Patient associated with this Related Person Patient.")
    relationship_id = fields.Many2one(
        comodel_name="hc.vs.related.person.relationship.type", 
        string="Relationship", 
        help="The nature of the relationship.")
    start_date = fields.Date(
        string="Start Date", 
        help="Start of the period of time that this relationship is considered valid.")
    end_date = fields.Date(
        string="End Date", 
        help="End of the period of time that this relationship is considered valid.")

class RelatedPersonRelationshipType(models.Model):  
    _name = "hc.vs.related.person.relationship.type"    
    _description = "Related Person Relationship Type"
    _inherit = ["hc.value.set.contains"]

    name = fields.Char(
        string="Name", 
        help="Name of this related person relationship type.")
    code = fields.Char(
        string="Code", 
        help="Code of this related person relationship type.")
    contains_id = fields.Many2one(
        comodel_name="hc.vs.related.person.relationship.type", 
        string="Parent",
        help="Parent concept.")    

# External Reference

class Partner(models.Model):
    _inherit = ["res.partner"]

    is_related_person = fields.Boolean(
        string="Is a related person", 
        help="This partner is a health care related person.")

class PersonLink(models.Model):
    _inherit = ["hc.person.link"]

    target_related_person_id = fields.Many2one(
        comodel_name="hc.res.related.person", 
        string="Target Related Person", 
        help="Related Person who is the resource to which this actual person is associated.")

    @api.depends('target_type')          
    def _compute_target_name(self):         
        for hc_person_link in self:      
            if hc_person_link.target_type == 'person': 
                hc_person_link.target_name = hc_person_link.target_person_id.name
            elif hc_person_link.target_type == 'practitioner':   
                hc_person_link.target_name = hc_person_link.target_practitioner_id.name
            elif hc_person_link.target_type == 'related Person': 
                hc_person_link.target_name = hc_person_link.target_related_person_id.name

class Annotation(models.Model):
    _inherit = ["hc.annotation"]

    author_related_person_id = fields.Many2one(
        comodel_name="hc.res.related.person", 
        string="Author Related Person", 
        help="Related person responsible for the annotation.")

    @api.depends('author_type')
    def _compute_author_name(self):
        for hc_annotation in self:
            if hc_annotation.author_type == 'string':
                hc_annotation.author_name = hc_annotation.author_string
            elif hc_annotation.author_type == 'practitioner':
                hc_annotation.author_name = hc_annotation.author_practitioner_id.name
            elif hc_annotation.author_type == 'related_person':
                hc_annotation.author_name = hc_annotation.author_related_person_id.name

class Signature(models.AbstractModel):    
    _inherit = "hc.signature"

    who_related_person_id = fields.Many2one(
        comodel_name="hc.res.related.person", 
        string="Who Related Person", 
        help="Related Person who signed.")

    on_behalf_of_related_person_id = fields.Many2one(
        comodel_name="hc.res.related.person", 
        string="On Behalf Of Related Person", 
        help="Related Person the party represented.")
