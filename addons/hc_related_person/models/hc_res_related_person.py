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
        related="person_id.identifier_ids",
        string="Identifiers",
        help="A human identifier for this related person.")
    # identifier_ids = fields.One2many(
    #     comodel_name="hc.related.person.identifier",
    #     inverse_name="related_person_id",
    #     string="Identifiers",
    #     help="A human identifier for this related person.")
    is_active = fields.Boolean(
        string="Active",
        default="True",
        help="Whether this related person's record is in active use.")
    name_ids = fields.One2many(
        related="person_id.name_ids",
        string="Names",
        help="A name associated with the related person.")
    # name_ids = fields.One2many(
    #     comodel_name="hc.human.name",
    #     inverse_name="related_person_id",
    #     string="Names",
    #     help="A name associated with this related person.")
    telecom_ids = fields.One2many(
        related="person_id.telecom_ids",
        string="Telecoms",
        help="A contact detail for this related person.")
    # telecom_ids = fields.One2many(
    #     comodel_name="hc.related.person.telecom",
    #     inverse_name="related_person_id",
    #     string="Telecoms",
    #     help="A contact detail for this related person.")
    gender = fields.Selection(
        related="person_id.gender",
        readonly="1",
        help="The gender of a related person used for administrative purposes.")
    birth_date = fields.Date(
        related="person_id.birth_date",
        readonly="1",
        help="The birth date for the related person.")
    address_ids = fields.One2many(
        related="person_id.address_ids",
        string="Addresses",
        help="One or more addresses for this related person.")
    photo_ids = fields.One2many(
        related="person_id.photo_ids",
        string="Photos",
        help="Image of the related person.")
    # photo_ids = fields.One2many(
    #     comodel_name="hc.related.person.photo",
    #     inverse_name="related_person_id",
    #     string="Photos",
    #     help="Image of the related person.")
    patient_ids = fields.One2many(
        comodel_name="hc.related.person.patient",
        inverse_name="related_person_id",
        string="Patients",
        required="True",
        help="Patient(s) related to this person.")

    # _defaults = {
    #     "is_related_person": True,
    #     }

    # @api.model
    # def create(self, vals):
    #     vals['is_related_person'] = self.env.context.get('is_related_person', False)
    #     return super(RelatedPerson, self).create(vals)

    # Indicate that associated Person is a Related Person.
    @api.model
    def create(self, vals):
        person_obj = self.env['hc.res.person']
        if vals and vals.get('person_id'):
            person_id = person_obj.browse(vals.get('person_id'))
            if person_id:
                person_id.is_related_person = True
        return super(RelatedPerson, self).create(vals)

    # When this Related Person record is inactivated and there are no other active Related Person records associated with the Person record, indicate that the Person is not a Related Person.
    @api.multi
    def unlink(self):
        for rec in self:
            if rec.person_id:
                person_rec = self.search([('person_id', '=', rec.person_id.id),
                                          ('id','!=', self.id)])
                if not person_rec:
                    rec.person_id.is_related_person = False
        return super(RelatedPerson, self).unlink()

class RelatedPersonIdentifier(models.Model):
    _name = "hc.related.person.identifier"
    _description = "Related Person Identifier"
    _inherits = {"hc.person.identifier": "identifier_id"}

    identifier_id = fields.Many2one(
        comodel_name="hc.person.identifier",
        string="Person Identifier",
        required="True",
        ondelete="restrict",
        help="Person identifier associated with this related person.")
    related_person_id = fields.Many2one(
        comodel_name="hc.res.related.person",
        string="Related Person",
        help="Related person associated with this person identifier.")

# class RelatedPersonName(models.Model):
#     _name = "hc.related.person.name"
#     _description = "Related Person Name"
#     _inherit = ["hc.basic.association"]
#     _inherits = {"hc.human.name": "human_name_id"}

#     human_name_id = fields.Many2one(
#         comodel_name="hc.human.name",
#         string="Human Name",
#         required="True",
#         ondelete="restrict",
#         help="Human name associated with this related person name.")
#     related_person_id = fields.Many2one(
#         comodel_name="hc.res.related.person",
#         string="Related Person",
#         help="Related Person associated with this human name.")

# class RelatedPersonTelecom(models.Model):
#     _name = "hc.related.person.telecom"
#     _description = "Related Person Telecom"
#     _inherit = ["hc.contact.point.use"]
#     _inherits = {"hc.contact.point": "telecom_id"}

#     telecom_id = fields.Many2one(
#         comodel_name="hc.contact.point",
#         string="Telecom",
#         ondelete="restrict",
#         required="True",
#         help="Telecom associated with this Related Person Telecom.")
#     related_person_id = fields.Many2one(
#         comodel_name="hc.res.related.person",
#         string="Related Person",
#         help="Related Person associated with this Related Person Telecom.")

# class RelatedPersonAddress(models.Model):
#     _name = "hc.related.person.address"
#     _description = "Related Person Address"
#     _inherit = ["hc.address.use"]
#     _inherits = {"hc.address": "address_id"}

#     address_id = fields.Many2one(
#         comodel_name="hc.address",
#         string="Address",
#         required="True",
#         ondelete="restrict",
#         help="Address associated with this Related Person Address.")
#     related_person_id = fields.Many2one(
#         comodel_name="hc.res.related.person",
#         string="Related Person",
#         help="Related Person associated with this Related Person Address.")

# class RelatedPersonPhoto(models.Model):
#     _name = "hc.related.person.photo"
#     _description = "Related Person Photo"
#     _inherits = {"hc.person.photo": "photo_id"}

#     photo_id = fields.Many2one(
#         comodel_name="hc.person.photo",
#         string="Photo",
#         required="True",
#         ondelete="restrict",
#         help="Photo associated with this Related Person Photo.")
#     related_person_id = fields.Many2one(
#         comodel_name="hc.res.person",
#         string="Related Person",
#         help="Related Person associated with this Related Person Photo.")

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

class PartnerLink(models.Model):
    _inherit = ["hc.partner.link"]

    link_type = fields.Selection(
        selection_add=[
            ("related_person", "Related Person")])
    link_related_person_id = fields.Many2one(
        comodel_name="hc.res.related.person",
        string="Link Related Person",
        help="Related Person who is the resource to which this actual partner is associated.")

    @api.depends('link_type')
    def _compute_link_name(self):
        for hc_partner_link in self:
            if hc_partner_link.link_type == 'person':
                hc_partner_link.link_name = hc_partner_link.link_person_id.name
            elif hc_partner_link.link_type == 'related_person':
                hc_partner_link.link_name = hc_partner_link.link_related_person_id.name
            elif hc_partner_link.link_type == 'practitioner':
                hc_partner_link.link_name = hc_partner_link.link_practitioner_id.name

class Person(models.Model):
    _inherit = ["hc.res.person"]

    is_related_person = fields.Boolean(
        string="Is a related person",
        help="This person is a related person.")

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
            elif hc_person_link.target_type == 'related_person':
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

class Signature(models.Model):
    _inherit = ["hc.signature"]

    who_related_person_id = fields.Many2one(
        comodel_name="hc.res.related.person",
        string="Who Related Person",
        help="Related Person who signed.")
    on_behalf_of_related_person_id = fields.Many2one(
        comodel_name="hc.res.related.person",
        string="On Behalf Of Related Person",
        help="Related Person the party represented.")

    @api.depends('who_type')
    def _compute_who_name(self):
        for hc_signature in self:
            if hc_signature.who_type == 'uri':
                hc_signature.who_name = hc_signature.who_uri
            elif hc_signature.who_type == 'related_person':
                hc_signature.who_name = hc_signature.who_related_person_id.name

    @api.depends('on_behalf_of_type')
    def _compute_on_behalf_of_name(self):
        for hc_signature in self:
            if hc_signature.on_behalf_of_type == 'uri':
                hc_signature.on_behalf_of_name = hc_signature.on_behalf_of_uri
            elif hc_signature.on_behalf_of_type == 'related_person':
                hc_signature.on_behalf_of_name = hc_signature.on_behalf_of_related_person_id.name
