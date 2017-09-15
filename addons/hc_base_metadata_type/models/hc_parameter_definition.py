# -*- coding: utf-8 -*-

from openerp import models, fields, api

class ParameterDefinition(models.Model):
    _name = "hc.parameter.definition"
    _description = "Parameter Definition"
    _inherit = ["hc.element"]
    _rec_name = "name"

    name = fields.Char(
        string="Name",
        help="Parameter name.")
    use = fields.Selection(
        string="Use",
        required="True",
        selection=[
            ("in", "In"),
            ("out", "Out")],
        help="Whether the parameter is input or output for the module.")
    min = fields.Integer(
        string="Min",
        help="Minimum cardinality.")
    max = fields.Integer(
        string="Max",
        help="Maximum cardinality (a number of *).")
    documentation = fields.Text(
        string="Documentation",
        help="A brief description of the parameter.")
    type_id = fields.Many2one(
        comodel_name="hc.vs.fhir.all.type",
        string="Type",
        required="True",
        help="The type of the parameter.")
    # profile_id = fields.Many2one(
    #     comodel_name="hc.res.structure.definition",
    #     string="Profile",
    #     help="The profile of the parameter, any.")

class FHIRAllType(models.Model):
    _name = "hc.vs.fhir.all.type"
    _description = "FHIR All Data Types"
    _inherit = ["hc.value.set.contains"]
