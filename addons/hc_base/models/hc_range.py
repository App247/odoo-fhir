# -*- coding: utf-8 -*-

from openerp import models, fields, api

class Range(models.Model):
    _name = "hc.range"
    _description = "Range"
    _inherit = ["hc.element"]

    low = fields.Float(
        string="Low",
        help="Low limit.")
    high = fields.Float(
        string="High",
        help="High limit.")

# Constraints

# If present, low SHALL have a lower value than high.

_sql_constraints = [
	('low_less_high',
	'CHECK(low <= high)',
	'Error ! Low SHALL have a lower value than high.')
	]
