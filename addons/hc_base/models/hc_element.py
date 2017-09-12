# -*- coding: utf-8 -*-

from openerp import models, fields, api

class ElementElement(models.Model):
    _name = "hc.element"
    _description = "Element"
    _rec_name = "identifier"

    identifier = fields.Char(
        string="Identifier",
        required="True",
        help="Internal id (e.g. like xml:id).")
    extension_ids = fields.One2many(
        comodel_name="hc.element.extension",
        inverse_name="element_id",
        string="Extensions",
        help="Additional Content defined by implementations.")

class ElementExtension(models.Model):
    _name = "hc.element.extension"
    _description = "Element Extension"
    _inherit = ["hc.basic.association"]

    element_id = fields.Many2one(
        comodel_name="hc.element",
        string="Element",
        help="Element associated with this Element Extension.")

# External reference

class Coding(models.Model):
    _inherit = ["hc.element"]

class CodeableConcept(models.Model):
    _inherit = ["hc.element"]
