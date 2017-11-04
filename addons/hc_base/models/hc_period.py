# -*- coding: utf-8 -*-

from openerp import models, fields, api

class Period(models.Model):
    _name = "hc.period"
    _description = "Period"
    _inherit = ["hc.element"]

    start = fields.Datetime(
        string="Start Datetime",
        help="Starting time with inclusive boundary.")
    end = fields.Datetime(
        string="End Datetime",
        help="End time with inclusive boundary, if not ongoing.")

    # Element Attribute
    identifier = fields.Char(
        string="ID",
        help="Internal id (e.g. like xml:id).")
    extension_ids = fields.One2many(
        comodel_name="hc.period.element.extension",
        inverse_name="period_id",
        string="Extensions",
        help="Additional Content defined by implementations.")

class PeriodElementExtension(models.Model):
    _name = "hc.period.element.extension"
    _description = "Period Element Extension"
    _inherit = ["hc.basic.association"]

    period_id = fields.Many2one(
        comodel_name="hc.period",
        string="Period",
        help="Period associated with this Period Element Extension.")

# Constraints

# If present, start SHALL have a lower value than end.
