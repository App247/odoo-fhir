# -*- coding: utf-8 -*-

from openerp import models, fields, api

class Ratio(models.Model):
    _name = "hc.ratio"
    _description = "Ratio"
    _inherit = ["hc.element"]

    numerator_id = fields.Many2one(
        comodel_name="hc.ratio.numerator",
        string="Numerator",
        help="Numerator value.")
    denominator_id = fields.Many2one(
        comodel_name="hc.ratio.denominator",
        string="Denominator",
        help="Denominator value.")

class RatioNumerator(models.Model):
    _name = "hc.ratio.numerator"
    _description = "Ratio Numerator"
    _inherit = ["hc.basic.association", "hc.quantity"]

class RatioDenominator(models.Model):
    _name = "hc.ratio.denominator"
    _description = "Ratio Denominator"
    _inherit = ["hc.basic.association", "hc.quantity"]

# Constraints

# Numerator and denominator SHALL both be present, or both are absent.
# If both are absent, there SHALL be some extension present
