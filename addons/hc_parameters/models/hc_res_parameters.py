# -*- coding: utf-8 -*-

from openerp import models, fields, api

class Parameters(models.Model):
    _name = "hc.res.parameters"
    _description = "Parameters"
    _inherit = ["hc.resource"]       

    parameter_ids = fields.One2many(
        comodel_name="hc.parameters.parameter",
        inverse_name="parameters_id",
        string="Parameters",
        help="Operation Parameter.")

class ParametersParameter(models.Model):
    _name = "hc.parameters.parameter"
    _description = "Parameters Parameter"

    parameters_id = fields.Many2one(
        comodel_name="hc.res.parameters",
        string="Parameters",
        help="Parameters associated with this Parameters Parameter.")
    name = fields.Char(
        string="Name",
        required="True",
        help="Name from the definition.")
    value_ids = fields.One2many(
        comodel_name="hc.parameters.parameter.value",
        inverse_name="parameter_id",
        string="Values",
        help="Any if parameter is a data type.")
    resource_id = fields.Many2one(
        comodel_name="hc.parameters.parameter.resource",
        string="Resource",
        help="If parameter is a whole resource.")
    part_ids = fields.One2many(
        comodel_name="hc.parameters.parameter.part",
        inverse_name="parameter_id",
        string="Parts",
        help="Named part of a parameter (e.g. Tuple).")
    parameter_id = fields.Many2one(
        comodel_name="hc.parameters.parameter",
        string="Parameter",
        help="Allows text, questions and other groups to be nested beneath a question or group.")

class ParametersParameterValue(models.Model):
    _name = "hc.parameters.parameter.value"
    _description = "Parameters Parameter Value"
    _inherit = ["hc.basic.association"]

    parameter_id = fields.Many2one(
        comodel_name="hc.parameters.parameter",
        string="Parameter",
        help="Parameter associated with this Parameters Parameter Value.")
    value_type = fields.Selection(
        string="Value Type",
        selection=[
            ("string", "String"),
            ("decimal", "Decimal"),
            ("datetime", "Datetime"),
            ("boolean", "Boolean")],
        help="Type of data type.")
    value_name = fields.Char(
        string="Value",
        ompute="_compute_value_name",
        store="True",
        help="Data type")
    value_string_id = fields.Char(
        string="Value String",
        help="String data type.")
    value_decimal_id = fields.Float(
        string="Value Decimal",
        help="Decimal data type.")
    value_datetime_id = fields.Datetime(
        string="Value Datetime",
        help="Datetime data type.")
    value_boolean_id = fields.Boolean(
        string="Value Boolean",
        help="Boolean data type.")

class ParametersParameterResource(models.Model):
    _name = "hc.parameters.parameter.resource"
    _description = "Parameters Parameter Resource"
    _inherit = ["hc.basic.association", "hc.resource"]

class ParametersParameterPart(models.Model):
    _name = "hc.parameters.parameter.part"
    _description = "Parameters Parameter Part"
    _inherit = ["hc.basic.association"]

    parameter_id = fields.Many2one(
        comodel_name="hc.parameters.parameter",
        string="Parameter",
        help="Parameter associated with this Parameters Parameter Part.")
    part_id = fields.Many2one(
        comodel_name="hc.parameters.parameter",
        string="Part",
        help="Part associated with this Parameters Parameter Part.")
