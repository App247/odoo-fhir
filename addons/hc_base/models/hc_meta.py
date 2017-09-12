# -*- coding: utf-8 -*-

from openerp import models, fields, api

class Meta(models.Model):
    _name = "hc.meta"
    _description = "Meta"
    _inherit = ["hc.element"]

    version_id = fields.Char(
        string="Version Id",
        help="Version specific identifier.")
    last_updated = fields.Datetime(
        string="Last Updated",
        help="When the resource version last changed.")
    profile_ids = fields.One2many(
        comodel_name="hc.meta.profile",
        inverse_name="meta_id",
        string="Profile URIs",
        help="URL of profiles this resource claims to conform to.")
    security_ids = fields.Many2many(
        comodel_name="hc.vs.security.label",
        string="Security Labels",
        help="Security Labels applied to this resource.")
    tag_ids = fields.Many2many(
        comodel_name="hc.vs.common.tag",
        string="Tags",
        help="Tags applied to this resource.")

class MetaProfile(models.Model):
    _name = "hc.meta.profile"
    _description = "Meta Profile"
    _inherit = ["hc.basic.association"]

    meta_id = fields.Many2one(
        comodel_name="hc.meta",
        string="Meta",
        help="Meta associated with this Meta Profile.")
    profile = fields.Char(
        string="Profile URI",
        help="URI associated with this Meta Profile.")

class CommonTag(models.Model):
    _name = "hc.vs.common.tag"
    _description = "Common Tag"
    _inherit = ["hc.value.set.contains"]
