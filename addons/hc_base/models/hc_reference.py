# -*- coding: utf-8 -*-

from openerp import models, fields, api

class Reference(models.Model):
    _name = "hc.reference"
    _description = "Reference"
    _inherit = ["hc.element"]
    _rec_name = "display"

    reference = fields.Char(
        string="Reference",
        help="Relative, internal or absolute URL reference.")
    identifier_id = fields.Many2one(
        comodel_name="hc.reference.identifier",
        string="Identifier",
        help="Logical reference, when literal reference is not known.")
    display = fields.Char(
        string="Display",
        help="Text alternative for the resource.")

class ReferenceIdentifier(models.Model):
    _name = "hc.reference.identifier"
    _description = "Reference Identifier"
    _inherit = ["hc.basic.association", "hc.identifier"]
