# -*- coding: utf-8 -*-

from openerp import models, fields, api

class DataRequirement(models.Model):
    _name = "hc.data.requirement"
    _description = "Data Requirement"
    _inherit = ["hc.element"]        

    type_id = fields.Many2one(
        comodel_name="hc.vs.fhir.all.type",
        string="Type",
        required="True",
        help="The type of the required data.")
    profile_ids = fields.One2many(
        comodel_name="hc.data.reqt.profile",
        inverse_name="data_requirement_id",
        string="Profiles",
        help="The profile of the required data.")
    must_support_ids = fields.One2many(
        comodel_name="hc.data.reqt.must.support",
        inverse_name="data_requirement_id",
        string="Must Supports",
        help="Indicates that specific structure elements are referenced by the knowledge module.")
    code_filter_ids = fields.One2many(
        comodel_name="hc.data.reqt.code.filter",
        inverse_name="data_requirement_id",
        string="Code Filters",
        help="Code filters for the data.")
    date_filter_ids = fields.One2many(
        comodel_name="hc.data.reqt.data.filter",
        inverse_name="data_requirement_id",
        string="Date Filters",
        help="Date filters for the data.")

class DataRequirementCodeFilter(models.Model):
    _name = "hc.data.reqt.code.filter"
    _description = "Data Requirement Code Filter"

    data_requirement_id = fields.Many2one(
        comodel_name="hc.data.requirement",
        string="Data Requirement",
        help="Data Requirement associated with this code filter.")
    path = fields.Char(
        string="Path",
        required="True",
        help="The code-valued attribute of the filter.")
    value_set_type = fields.Selection(
        string="Value Set Type",
        required="True",
        selection=[
            ("string", "String"),
            ("value set", "Value Set")],
        help="Type of value set for the filter.")
    value_set_name = fields.Char(
        string="Value Set",
        compute="compute_value_set_name",
        help="Value set for the filter.")
    value_set_string = fields.Char(
        string="Value Set String",
        help="String value set for the filter.")
    # value_set_id = fields.Many2one(
    #     comodel_name="hc.res.value.set",
    #     string="Value Set",
    #     help="Value set for the filter")
    value_code_ids = fields.Many2many(
        comodel_name="hc.vs.value.code",
        string="Value Codes",
        help="Code value of the filter." )
    value_coding_ids = fields.Many2many(
        comodel_name="hc.vs.value.coding",
        string="Value Codings",
        help="Coding value of the filter." )
    value_code_concept_ids = fields.Many2many(
        comodel_name="hc.vs.value.code.concept",
        string="Value Codeable Concepts",
        help="Codeable Concept value of the filter." )

class DataRequirementDataFilter(models.Model):
    _name = "hc.data.reqt.data.filter"
    _description = "Data Requirement Data Filter"

    data_requirement_id = fields.Many2one(
        comodel_name="hc.data.requirement",
        string="Data Requirement",
        help="Data Requirement associated with this data filter.")
    path = fields.Char(
        string="Path",
        required="True",
        help="The date-valued attribute of the filter.")
    value_type = fields.Selection(
        string="Value Type",
        required="True",
        selection=[
            ("datetime", "Datetime"),
            ("period", "Period"),
            ("duration", "Duration")],
        help="Type of the value of the filter.")
    value_name = fields.Char(
        string="Value",
        compute="compute_value_name",
        help="The value of the filter, as a Period, DateTime, or Duration value.")
    value_datetime = fields.Datetime(
        string="Value Datetime",
        help="Datetime value of the filter.")
    value_start_date = fields.Datetime(
        string="Value Start Date",
        help="Start of the filter period.")
    value_end_date = fields.Datetime(
        string="Value End Date",
        help="End of the filter period.")
    value_duration = fields.Float(
        string="Value Duration",
        help="Duration value of the filter.")
    value_duration_uom_id = fields.Many2one(
        comodel_name="product.uom",
        string="Value Duration UOM",
        domain="[('category_id','=','Time (UCUM)')]",
        help="Value Duration unit of measure.")

class DataRequirementProfile(models.Model):
    _name = "hc.data.reqt.profile"
    _description = "Data Requirement Profile"
    _inherit = ["hc.basic.association"]

    data_requirement_id = fields.Many2one(
        comodel_name="hc.data.requirement",
        string="Data Requirement",
        help="Data Requirement associated with this Data Requirement Profile.")
    # profile_id = fields.Many2one(
    #     comodel_name="hc.res.structure.definition",
    #     string="Profile",
    #     help="Profile associated with this Data Requirement Profile.")

class DataRequirementMustSupport(models.Model):
    _name = "hc.data.reqt.must.support"
    _description = "Data Requirement Must Support"
    _inherit = ["hc.basic.association"]

    data_requirement_id = fields.Many2one(
        comodel_name="hc.data.requirement",
        string="Data Requirement",
        help="Data Requirement associated with this data requirement must support.")
    must_support = fields.Char(
        string="Must Support",
        help="Must Support associated with this data requirement must support.")

class ValueCode(models.Model):
    _name = "hc.vs.value.code"
    _description = "Value Code"
    _inherit = ["hc.value.set.contains"]

class ValueCodeableConcept(models.Model):
    _name = "hc.vs.value.code.concept"
    _description = "Value Codeable Concept"
    _inherit = ["hc.value.set.contains"]

class ValueCoding(models.Model):
    _name = "hc.vs.value.coding"
    _description = "Value Coding"
    _inherit = ["hc.value.set.contains"]
