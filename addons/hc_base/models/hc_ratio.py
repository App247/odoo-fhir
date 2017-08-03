# -*- coding: utf-8 -*-

from openerp import models, fields, api

class Ratio(models.Model):
    _name = "hc.ratio"
    _description = "Ratio"
    _inherit = ["hc.element"]

    numerator = fields.Float(
    	string="Numerator",
    	help="Numerator value.")
    denominator = fields.Float(
    	string="Denominator",
    	help="Denominator value.")

# Constraints

# Numerator and denominator SHALL both be present, or both are absent.
# If both are absent, there SHALL be some extension present
