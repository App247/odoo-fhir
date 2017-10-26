# -*- coding: utf-8 -*-

from openerp import models, fields, api

class Linkage(models.Model):
    _name = "hc.res.linkage"
    _description = "Linkage"

    author_type = fields.Selection(
        string="Author Type",
        selection=[
            ("practitioner", "Practitioner"),
            ("organization", "Organization")],
        help="Type of who is responsible for linkages.")
    author_name = fields.Char(
        string="Author",
        compute="_compute_author_name",
        store="True",
        help="Who is responsible for linkage.")
    author_practitioner_id = fields.Many2one(
        comodel_name="hc.res.practitioner",
        string="Author Practitioner",
        help="Practitioner who is responsible for linkages.")
    author_organization_id = fields.Many2one(
        comodel_name="hc.res.organization",
        string="Author Organization",
        help="Organization who is responsible for linkages.")

    @api.multi
    def _compute_author_name(self):
        for hc_res_linkage in self:
            if hc_res_linkage.author_type == 'practitioner':
                hc_res_linkage.author_name = hc_res_linkage.author_practitioner_id.name
            elif hc_res_linkage.author_type == 'organization':
                hc_res_linkage.author_name = hc_res_linkage.author_organization_id.name

class LinkageItem(models.Model):
    _name = "hc.linkage.item"
    _description = "Linkage Item"

    linkage_id = fields.Many2one(
        comodel_name="hc.res.linkage",
        string="Linkage",
        help="Linkage associated with this Linkage Item.")
    type = fields.Selection(
        string="Item Type",
        required="True",
        selection=[
            ("source", "Source"),
            ("alternate", "Alternate"),
            ("historical", "Historical")],
        help='Distinguishes which item is "source of truth" (if any) and which items are no longer considered to be current representations.')
    # resource = fields.One2many(
    #     comodel_name="hc.res.resource",
    #     string = "Resource"
    #     required="True",
    #     help="Reference resource being linked.")
