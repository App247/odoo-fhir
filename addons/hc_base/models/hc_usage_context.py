# -*- coding: utf-8 -*-

from openerp import models, fields, api

class UsageContext(models.Model):
    _name = "hc.usage.context"
    _description = "Usage Context"
    _inherit = ["hc.element"]
    _rec_name = "value_name"

    code_id = fields.Many2one(
        comodel_name="hc.vs.usage.context.type",
        string="Code",
        required="True",
        help="Type of context being specified.")
    value_type = fields.Selection(
        string="Value Type",
        required="True",
        selection=[
            ("code", "Code"),
            ("quantity", "Quantity"),
            ("range", "Range")],
        help="Type of value that defines the context.")
    value_name = fields.Char(
        string="Value",
        compute="_compute_value_name",
        store="True",
        help="Value that defines the context.")
    value_code_id = fields.Many2one(
        comodel_name="hc.vs.usage.context.value",
        string="Value Code",
        help="Value that defines the context.")
    value_quantity = fields.Float(
        string="Value Quantity",
        required="True",
        help="Value that defines the context.")
    value_quantity_uom_id = fields.Many2one(
        comodel_name="product.uom",
        string="Value Quantity UOM",
        help="Value quantity unit of measure.")
    value_range_low = fields.Float(
        string="Value Range Low",
        help="Low limit of value that defines the context.")
    value_range_high = fields.Float(
        string="Value Range High",
        help="High limit of value that defines the context.")
    value_range_uom_id = fields.Many2one(
        comodel_name="product.uom",
        string="Value Range UOM",
        help="Value range unit of measure.")

    @api.depends('value_type')
    def _compute_value_name(self):
        for hc_usage_context in self:
            if hc_usage_context.value_type == 'code':
                hc_usage_context.value_name = hc_usage_context.value_code_id.name
            elif hc_usage_context.value_type == 'quantity':
                hc_usage_context.value_name = str(hc_usage_context.value_quantity) + " " + str(hc_usage_context.value_quantity_uom_id.name)
            elif hc_usage_context.value_type == 'range':
                hc_usage_context.value_name = "Between " + str(hc_usage_context.value_range_low) + " and " + str(hc_usage_context.value_range_high) + " " + str(hc_usage_context.value_range_uom_id.name)

class UsageContextType(models.Model):
    _name = "hc.vs.usage.context.type"
    _description = "Usage Context Type"
    _inherit = ["hc.value.set.contains"]

class UsageContextValue(models.Model):
    _name = "hc.vs.usage.context.value"
    _description = "Usage Context Value"
    _inherit = ["hc.value.set.contains"]
