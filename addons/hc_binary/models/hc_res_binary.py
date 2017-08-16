# -*- coding: utf-8 -*-

from openerp import models, fields, api

class Binary(models.Model):
    _name = "hc.res.binary"
    _description = "Binary"
    _inherit = ["hc.resource"]

    content_type_id = fields.Many2one(
        comodel_name="hc.vs.mime.type",
        string="Content Type",
        required="True",
        help="MimeType of the binary content.")
    security_context_type = fields.Char(
        string="Security Context Type",
        compute="_compute_security_context_type",
        store="True",
        help="Type of Access Control Management.")
    security_context_name = fields.Reference(
        string="Security Context",
        selection="_reference_models",
        help="Access Control Management.")
    content = fields.Binary(
        string="Content",
        required="True",
        help="The actual content.")

    @api.model
    def _reference_models(self):
        models = self.env['ir.model'].search([('state', '!=', 'manual')])
        return [(model.model, model.name)
            for model in models
                if model.model.startswith('hc.res')]

    @api.depends('security_context_name')
    def _compute_security_context_type(self):
        for this in self:
            if this.security_context_name:
                this.security_context_type = this.security_context_name._description
