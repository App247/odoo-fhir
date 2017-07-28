# -*- coding: utf-8 -*-

from openerp import models, fields, api

class DomainResource(models.Model):
    _name = "hc.domain.resource"
    _description = "Domain Resource"
    _inherit = ["hc.element"]
    _rec_name = "text_id"

    text_id = fields.Many2one(
        comodel_name="hc.domain.resource.text",
        string="Text",
        help="Text summary of the resource, for human interpretation.")
    contained_ids = fields.One2many(
        comodel_name="hc.domain.resource.contained",
        inverse_name="domain_resource_id",
        string="Contained",
        help="Contained, inline Resources.")
    extension_ids = fields.One2many(
        comodel_name="hc.domain.resource.extension",
        inverse_name="domain_resource_id",
        string="Extensions",
        help="Additional Content defined by implementations.")
    modifier_extension_ids = fields.One2many(
        comodel_name="hc.domain.resource.modifier.extension",
        inverse_name="domain_resource_id",
        string="Modifier Extensions",
        help="Extensions that cannot be ignored.")

class DomainResourceText(models.Model):
    _name = "hc.domain.resource.text"
    _description = "Domain Resource Text"
    _inherit = ["hc.basic.association", "hc.narrative"]

class DomainResourceContained(models.Model):
    _name = "hc.domain.resource.contained"
    _description = "Domain Resource Contained"
    _inherit = ["hc.basic.association", "hc.resource"]

    domain_resource_id = fields.Many2one(
        comodel_name="hc.domain.resource",
        string="Domain Resource",
        help="Domain Resource associated with this Domain Resource Contained.")

class DomainResourceExtension(models.Model):
    _name = "hc.domain.resource.extension"
    _description = "Domain Resource Extension"
    _inherit = ["hc.basic.association", "hc.extension"]

    domain_resource_id = fields.Many2one(
        comodel_name="hc.domain.resource",
        string="Domain Resource",
        help="Domain Resource associated with this Domain Resource Extension.")

class DomainResourceModifierExtension(models.Model):
    _name = "hc.domain.resource.modifier.extension"
    _description = "Domain Resource Modifier Extension"
    _inherit = ["hc.basic.association", "hc.extension"]

    domain_resource_id = fields.Many2one(
        comodel_name="hc.domain.resource",
        string="Domain Resource",
        help="Domain Resource associated with this Domain Resource Modifier Extension.")
