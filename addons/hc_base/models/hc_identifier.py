# -*- coding: utf-8 -*-

from openerp import models, fields, api

class IdentifierTypeClass(models.Model):
    _name = "hc.vs.identifier.type.class"
    _description = "Identifier Type Class"
    _inherit = ["hc.value.set.contains"]

    name = fields.Char(
        string="Name",
        help="Name of this identifier type class (e.g., Government).")
    code = fields.Char(
        string="Code",
        help="Code of this identifier type class (e.g., GOV).")

class IdentifierType(models.Model):
    _name = "hc.vs.identifier.type"
    _description = "Identifier Type"
    _inherit = ["hc.value.set.contains"]

    name = fields.Char(
        string="Name",
        help="Name of this identifier type (e.g., Driver's License Number).")
    code = fields.Char(
        string="Code",
        help="Code of this identifier type (e.g., DL).")
    class_id = fields.Many2one(
        comodel_name="hc.vs.identifier.type.class",
        string="Class",
        help="Type of grouping of identifier types (e.g. Government).")

class Identifier(models.Model):
    _name = "hc.identifier"
    _description = "Identifier"
    _inherit = ["hc.element"]

    name = fields.Char(
        string="Name",
        compute="_compute_name",
        store="True",
        help="Name of this identifier record. Code Name + Value.")
    code_id = fields.Many2one(
        comodel_name="hc.vs.identifier.code",
        string="Code",
        help="Code of this identifier (e.g., CA DL).")
    value = fields.Char(
        string="Value",
        help="The value that is unique.")
    use = fields.Selection(
        string="Use",
        selection=[
            ("usual", "Usual"),
            ("official", "Official"),
            ("temp", "Temporary"),
            ("secondary", "Secondary")],
        help="The purpose of this identifier.")
    type_id = fields.Many2one(
        string="Type",
        related="code_id.type_id",
        help="Description of identifier.")

    @api.depends('code_id', 'value')
    def _compute_name(self):
        comp_name = '/'
        for hc_identifier in self:
            if hc_identifier.code_id:
                comp_name = hc_identifier.code_id.name or ''
            if hc_identifier.value:
                comp_name = comp_name + " " + hc_identifier.value or ''
            hc_identifier.name = comp_name

class IdentifierCode(models.Model):
    _name = "hc.vs.identifier.code"
    _description = "Identifier Code"
    _inherit = ["hc.value.set.contains"]

    name = fields.Char(
        string="Name",
        help="Name of this identifier (e.g., CA Driver's License Number).")
    # name = fields.Char(
    #     string="Name",
    #     compute="_compute_name",
    #     store="True",
    #     help="Name of this identifier (e.g., CA Driver's License Number).")
    code = fields.Char(
        string="Code",
        help="Code of this identifier (e.g., CA DL).")
    contains_id = fields.Many2one(
        comodel_name="hc.vs.identifier.code",
        string="Parent",
        help="Parent identifier code.")
    type_id = fields.Many2one(
        comodel_name="hc.vs.identifier.type",
        string="Type",
        help="Description of identifier.")
    system = fields.Char(
        string="System URI",
        help="The namespace for the identifier.")
    definition = fields.Text(
        string="Definition",
        help="An explanation of the meaning of the identifier.")
    # assigner_id = fields.Many2one(
    #     comodel_name="hc.res.organization",
    #     string="Assigner",
    #     help="Organization that issued id (may be just text)")
    country_id = fields.Many2one(
        comodel_name="res.country",
        string="Country",
        help="Country associated with the identifier.")
