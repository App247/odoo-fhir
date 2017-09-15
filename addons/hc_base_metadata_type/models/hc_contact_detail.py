# -*- coding: utf-8 -*-

from openerp import models, fields, api

class ContactDetail(models.Model):
    _name = "hc.contact.detail"
    _description = "Contact Detail"
    _inherit = ["hc.element"]
    _rec_name = "name"
    # _inherits = {"hc.res.person": "person_id"}

    # person_id = fields.Many2one(
    #     comodel_name="hc.res.person",
    #     string="Person",
    #     ondelete="restrict",
    #     required="True",
    #     help="Person who is this Contact Detail.")
    name = fields.Char(
        string="Name",
        help="Name of an individual to contact.")
    telecom_ids = fields.One2many(
        comodel_name="hc.contact.detail.telecom",
        inverse_name="contact_detail_id",
        string="Telecoms",
        help="Contact details for individual or organization.")

class ContactDetailTelecom(models.Model):
    _name = "hc.contact.detail.telecom"
    _description = "Contact Detail Telecom"
    _inherit = ["hc.contact.point.use"]
    _inherits = {"hc.contact.point": "telecom_id"}

    telecom_id = fields.Many2one(
        comodel_name="hc.contact.point",
        string="Telecom",
        ondelete="restrict",
        required="True",
        help="Telecom associated with this Contact Detail Telecom.")
    contact_detail_id = fields.Many2one(
        comodel_name="hc.contact.detail",
        string="Contact Detail",
        help="Contact Detail associated with this Contact Detail Telecom.")
