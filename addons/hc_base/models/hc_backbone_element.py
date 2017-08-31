# -*- coding: utf-8 -*-

from openerp import models, fields, api

class BackboneElement(models.Model):
    _name = "hc.backbone.element"
    _description = "Backbone Element"
    _inherit = "hc.element"

    modifier_extension_ids = fields.One2many(
        comodel_name="hc.backbone.element.modifier.extension",
        inverse_name="backbone_element_id",
        string="Modifier Extensions",
        help="Extensions that cannot be ignored.")

class BackboneElementModifierExtension(models.Model):
    _name = "hc.backbone.element.modifier.extension"
    _description = "Backbone Element Modifier Extension"
    _inherit = ["hc.basic.association", "hc.extension"]

    backbone_element_id = fields.Many2one(
        comodel_name="hc.backbone.element",
        string="Backbone Element",
        help="Backbone associated with this Backbone Element Modifier Extension.")
