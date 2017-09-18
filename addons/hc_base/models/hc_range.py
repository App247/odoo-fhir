# -*- coding: utf-8 -*-

from openerp import models, fields, api

class Range(models.Model):
    _name = "hc.range"
    _description = "Range"
    _inherit = ["hc.element"]

    low_id = fields.Many2one(
        comodel_name="hc.range.low",
        string="Low",
        help="Low limit.")
    high_id = fields.Many2one(
        comodel_name="hc.range.high",
        string="High",
        help="High limit.")

class RangeLow(models.Model):
    _name = "hc.range.low"
    _description = "Range Low"
    _inherit = ["hc.simple.quantity"]

class RangeHigh(models.Model):
    _name = "hc.range.high"
    _description = "Range High"
    _inherit = ["hc.simple.quantity"]

# Constraints

# If present, low SHALL have a lower value than high.

_sql_constraints = [
	('low_less_high',
	'CHECK(low <= high)',
	'Error ! Low SHALL have a lower value than high.')
	]
