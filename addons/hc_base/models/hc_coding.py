# -*- coding: utf-8 -*-

from openerp import models, fields, api

class BasicAssociation(models.Model):
    _name = "hc.basic.association"
    _description = "Basic Association"

    is_active = fields.Boolean(
        string="Active",
        default="True",
        help="Whether this record is in active use.")
    is_preferred = fields.Boolean(
        string="Preferred",
        help="Record preference indicator.")
    start_date = fields.Date(
        string="Start Date",
        help="Start of the period during which this record is valid.")
    end_date = fields.Date(
        string="End Date",
        help="End of the period during which this record is valid.")

class Coding(models.Model):
    _name = "hc.coding"
    _description = "Coding"
    _rec_name= "code"

    system = fields.Char(
        string="System URI",
        help="Identity of the terminology system.")
    version = fields.Char(
        string="Version",
        help="Version of the system - if relevant.")
    code = fields.Char(
        string="Code",
        help="Symbol in syntax defined by the system.")
    display = fields.Char(
        string="Display",
        help="Representation defined by the system.")
    is_user_selected = fields.Boolean(
        string="User Selected",
        default="True",
        help="If this coding was chosen directly by the user.")

    # Element Attribute
    identifier = fields.Char(
        string="ID",
        help="Internal id (e.g. like xml:id).")
    extension_ids = fields.One2many(
        comodel_name="hc.coding.element.extension",
        inverse_name="coding_id",
        string="Extensions",
        help="Additional Content defined by implementations.")

class CodingElementExtension(models.Model):
    _name = "hc.coding.element.extension"
    _description = "Coding Element Extension"
    _inherit = ["hc.basic.association"]

    coding_id = fields.Many2one(
        comodel_name="hc.coding",
        string="Coding",
        help="Coding associated with this Coding Element Extension.")

class CodeableConcept(models.Model):
    _name = "hc.codeable.concept"
    _description = "Codeable Concept"
    _rec_name= "text"

    coding_ids = fields.One2many(
        comodel_name="hc.codeable.concept.coding",
        inverse_name="codeable_concept_id",
        string="Coding",
        help="Code defined by a terminology system.")
    text = fields.Text(
        string="Text",
        help="Plain text representation of the concept.")

    # Element Attribute
    identifier = fields.Char(
        string="ID",
        help="Internal id (e.g. like xml:id).")
    extension_ids = fields.One2many(
        comodel_name="hc.codeable.concept.element.extension",
        inverse_name="codeable_concept_id",
        string="Extensions",
        help="Additional Content defined by implementations.")

class CodeableConceptElementExtension(models.Model):
    _name = "hc.codeable.concept.element.extension"
    _description = "Codeable Concept Element Extension"
    _inherit = ["hc.basic.association"]

    codeable_concept_id = fields.Many2one(
        comodel_name="hc.codeable.concept",
        string="Codeable Concept",
        help="Codeable Concept associated with this Codeable Concept Element Extension.")

class CodeableConceptCoding(models.Model):
    _name = "hc.codeable.concept.coding"
    _description = "Codeable Concept Coding"
    _inherit = ["hc.basic.association"]

    codeable_concept_id = fields.Many2one(
        comodel_name="hc.codeable.concept",
        string="Codeable Concept",
        help="Codeable Concept associated with this Codeable Concept Coding.")
    coding_id = fields.Many2one(
        comodel_name="hc.coding",
        string="Coding",
        help="Coding associated with this Codeable Concept Coding.")
