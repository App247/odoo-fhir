# -*- coding: utf-8 -*-

from openerp import models, fields, api

class Partner(models.Model):
    _inherit = ["res.partner"]

    is_healthcare = fields.Boolean(
        string="Healthcare",
        help="This partner is a health care-related record.")
    is_organization = fields.Boolean(
        string="Is an Organization",
        help="This partner is a health care-related organization record.")
    is_organization_contact = fields.Boolean(
        string="Is an Organization Contact",
        help="This partner is an organization contact.")

class res_partner_title(models.Model):
    _inherit = ["res.partner.title"]

    code = fields.Char(
        string="Code",
        translate=True,
        help="Symbol in syntax defined by the system.")
    long_name = fields.Char(
        string="Prefix Name",
        translate=True,
        help="Full text of prefix abbreviation (e.g., Mister for Mr.)")
    definition = fields.Text(
        string="Definition",
        translate=True,
        help="An explanation of the meaning of the concept.")
    type = fields.Selection(
        string="Type",
        selection=[
            ("academic", "Academic"),
            ("generational", "Generational"),
            ("medical", "Medical"),
            ("honorary", "Honorary"),
            ("legal", "Legal"),
            ("monarchical", "Monarchical"),
            ("organizational", "Organizational"),
            ("person", "Person"),
            ("professional", "Professional"),
            ("religious", "Religious")],
        help="Category of title.")
    system = fields.Char(
        string="System URI",
        help="Identity of the terminology system.")
    source_id = fields.Many2one(
        comodel_name="res.partner",
        string="Source",
        help="The source of the definition of the code.")
