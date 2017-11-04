# -*- coding: utf-8 -*-

from openerp import models, fields, api

class ContactPoint(models.Model):
    _name = "hc.contact.point"
    _description = "Contact Point"
    _inherit = ["hc.element"]
    _rec_name = "name"

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

    # Element Attribute
    identifier = fields.Char(
        string="ID",
        help="Internal id (e.g. like xml:id).")
    extension_ids = fields.One2many(
        comodel_name="hc.contact.point.element.extension",
        inverse_name="contact_point_id",
        string="Extensions",
        help="Additional Content defined by implementations.")

    @api.depends('value', 'system')
    def _compute_name(self):
        comp_name = '/'
        for hc_contact_point in self:
            if hc_contact_point.system:
                comp_name = hc_contact_point.system or ''
            if hc_contact_point.value:
                comp_name = comp_name + ": " + hc_contact_point.value or ''
            hc_contact_point.name = comp_name

class ContactPointElementExtension(models.Model):
    _name = "hc.contact.point.element.extension"
    _description = "Contact Point Element Extension"
    _inherit = ["hc.basic.association"]

    contact_point_id = fields.Many2one(
        comodel_name="hc.contact.point",
        string="Contact Point",
        help="Contact Point associated with this Contact Point Element Extension.")

class ContactPointUse(models.Model):
    _name = "hc.contact.point.use"
    _description = "Contact Point Use"
    _inherit = ["hc.basic.association"]

    use = fields.Selection(
        string="Use",
        selection=[
            ("home", "Home"),
            ("work", "Work"),
            ("mobile", "Mobile"),
            ("vacation", "Vacation"),
            ("temp", "Temp"),
            ("old", "Old")],
        help="Purpose of this contact point.")
    rank = fields.Integer(
        string="Rank",
        help="Specify preferred order of use (1 = highest).")
