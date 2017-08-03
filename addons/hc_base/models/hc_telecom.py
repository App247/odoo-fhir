# -*- coding: utf-8 -*-

from openerp import models, fields, api

class ContactPoint(models.Model):
    _name = "hc.contact.point"
    _description = "Contact Point"
    _inherit = ["hc.element"]

    name = fields.Char(
        string="Contact Point",
        compute="_compute_name",
        store="True",
        help="A full text representation of the contact point. System + Value")
    system = fields.Selection(
        string="Contact Point System",
        required = "True",
        selection=[
            ("phone", "Phone"),
            ("fax", "Fax"),
            ("email", "Email"),
            ("pager", "Pager"),
            ("url", "URL"),
            ("sms", "SMS"),
            ("other", "Other")],
        help="Telecommunications form for contact point - what communications system is required to make use of the contact.")
    value = fields.Char(
        string="Value",
        required = "True",
        help="The actual contact point details.")
    natl_number = fields.Char(
        string="National Number",
        help="The domestic format for a phone number (e.g., (607) 123 4567).")

    @api.depends('value', 'system')
    def _compute_name(self):
        comp_name = '/'
        for hc_contact_point in self:
            if hc_contact_point.system:
                comp_name = hc_contact_point.system or ''
            if hc_contact_point.value:
                comp_name = comp_name + ": " + hc_contact_point.value or ''
            hc_contact_point.name = comp_name

class ContactPointUse(models.Model):
    _name = "hc.contact.point.use"
    _description = "Contact Point Use"
    _inherit = ["hc.basic.association"]

    use = fields.Selection(
        string="Use",
        selection=[
            ("home", "Home"),
            ("work", "Work"),
            ("vacation", "Vacation"),
            ("temp", "Temp"),
            ("old", "Old")],
        help="Purpose of this contact point.")
    rank = fields.Integer(
        string="Rank",
        default="1",
        help="Specify preferred order of use (1 = highest).")
