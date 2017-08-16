# -*- coding: utf-8 -*-

from openerp import models, fields, api

class BodyStructure(models.Model):
    _name = "hc.res.body.structure"
    _description = "Body Structure"
    _inherit = ["hc.domain.resource"]
    _rec_name = "name"

    name = fields.Char(
        string="Name",
        compute="_compute_name",
        store="True",
        help="Text representation of the body structure. Patient + Morphology + Location.")
    identifier_ids = fields.One2many(
        comodel_name="hc.body.structure.identifier",
        inverse_name="body_structure_id",
        string="Identifiers",
        help="Body structure identifier.")
    is_active = fields.Boolean(
        string="Active",
        help="Whether this record is in active use.")
    morphology_id = fields.Many2one(
        comodel_name="hc.vs.body.structure.code",
        string="Morphology",
        help="Kind of structure.")
    location_id = fields.Many2one(
        comodel_name="hc.vs.body.site",
        string="Location",
        help="Body Site.")
    location_qualifier_ids = fields.One2many(
        comodel_name="hc.body.structure.location.qualifier",
        inverse_name="body_structure_id",
        string="Location Qualifiers",
        help="Body site modifier.")
    description = fields.Text(
        string="Description",
        help="Text description.")
    image_ids = fields.One2many(
        comodel_name="hc.body.structure.image",
        inverse_name="body_structure_id",
        string="Images",
        help="Attached images.")
    patient_id = fields.Many2one(
        comodel_name="hc.res.patient",
        string="Patient",
        help="Who this is about.")

class BodyStructureIdentifier(models.Model):
    _name = "hc.body.structure.identifier"
    _description = "Body Structure Identifier"
    _inherit = ["hc.basic.association", "hc.identifier"]

    body_structure_id = fields.Many2one(
        comodel_name="hc.res.body.structure",
        string="Body Structure",
        help="Body Structure associated with this Body Structure Identifier.")

class BodyStructureLocationQualifier(models.Model):
    _name = "hc.body.structure.location.qualifier"
    _description = "Body Structure Location Qualifier"
    _inherit = ["hc.basic.association"]

    body_structure_id = fields.Many2one(
        comodel_name="hc.res.body.structure",
        string="Body Structure",
        help="Body Structure associated with this Body Structure Location Qualifier.")
    location_qualifier_id = fields.Many2one(
        comodel_name="hc.vs.body.structure.relative.location",
        string="Location Qualifier",
        help="Location Qualifier associated with this Body Structure Location Qualifier.")

class BodyStructureImage(models.Model):
    _name = "hc.body.structure.image"
    _description = "Body Structure Image"
    _inherit = ["hc.basic.association", "hc.attachment"]

    body_structure_id = fields.Many2one(
        comodel_name="hc.res.body.structure",
        string="Body Structure",
        help="Body Structure associated with this Body Structure Image.")

class BodyStructureCode(models.Model):
    _name = "hc.vs.body.structure.code"
    _description = "Body Structure Code"
    _inherit = ["hc.value.set.contains"]

    name = fields.Char(
        string="Name",
        help="Name of this body structure code.")
    code = fields.Char(
        string="Code",
        help="Code of this body structure code.")
    contains_id = fields.Many2one(
        comodel_name="hc.vs.body.structure.code",
        string="Parent",
        help="Parent concept.")

class BodyStructureRelativeLocation(models.Model):
    _name = "hc.vs.body.structure.relative.location"
    _description = "Body Structure Relative Location"
    _inherit = ["hc.value.set.contains"]

    name = fields.Char(
        string="Name",
        help="Name of this body structure relative location.")
    code = fields.Char(
        string="Code",
        help="Code of this body structure relative location.")
    contains_id = fields.Many2one(
        comodel_name="hc.vs.body.structure.relative.location",
        string="Parent",
        help="Parent concept.")
