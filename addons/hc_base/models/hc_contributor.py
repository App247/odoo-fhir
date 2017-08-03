# -*- coding: utf-8 -*-

from openerp import models, fields, api

class Contributor(models.Model):
    _name = "hc.contributor"
    _description = "Contributor"
    _inherit = ["hc.element"]        

    type = fields.Selection(
        string="Type",
        required="True",
        selection=[
            ("author", "Author"),
            ("editor", "Editor"),
            ("reviewer", "Reviewer"),
            ("endorser", "Endorser")],
        help="The type of contributor.")
    name = fields.Char(
        string="Name",
        required="True",
        help="Who contributed the content.")
    contact_ids = fields.One2many(
        comodel_name="hc.contributor.contact",
        inverse_name="contributor_id",
        string="Contacts",
        help="Contact details of the contributor.")

class ContributorContact(models.Model):
    _name = "hc.contributor.contact"
    _description = "Contributor Contact"
    _inherit = ["hc.basic.association"]
    _inherits = {"hc.contact.detail": "contact_detail_id"}

    contact_detail_id = fields.Many2one(
        comodel_name="hc.contact.detail",
        string="Contact Detail",
        required="True",
        ondelete="restrict",
        help="Contact Detail associated with this contributor contact.")
    contributor_id = fields.Many2one(
        comodel_name="hc.contributor",
        string="Contributor",
        help="Contributor associated with this contributor contact.")
