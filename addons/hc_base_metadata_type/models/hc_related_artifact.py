# -*- coding: utf-8 -*-

from openerp import models, fields, api

class RelatedArtifact(models.Model):
    _name = "hc.related.artifact"
    _description = "Related Artifact"
    _inherit = ["hc.element"]
    _rec_name = "identifier"

    type = fields.Selection(string="Type",
        required="True",
        selection=[
            ("documentation", "Documentation"),
            ("justification", "Justification"),
            ("citation", "Citation"),
            ("predecessor", "Predecessor"),
            ("successor", "Successor"),
            ("derived-from", "Derived From"),
            ("depends-on", "Depends On"),
            ("composed-of", "Composed Of")],
        help="The type of relationship to the related artifact.")
    display = fields.Text(
        string="Display",
        help="Brief description of the related artifact.")
    citation = fields.Text(
        string="Citation",
        help="Bibliographic citation for the artifact.")
    url = fields.Char(
        string="URI",
        help="URL for the related artifact.")
    document_id = fields.Many2one(
        comodel_name="hc.related.artifact.document",
        string="Document", help="The related document.")
    resource_type = fields.Char(
        string="Resource Type",
        compute="_compute_resource_type",
        store="True",
        help="Type of related resource.")
    resource_name = fields.Reference(
        string="Resource",
        selection="_reference_models",
        help="The related resource.")

    @api.model
    def _reference_models(self):
        models = self.env['ir.model'].search([('state', '!=', 'manual')])
        return [(model.model, model.name)
            for model in models
                if model.model.startswith('hc.res')]

    @api.depends('resource_name')
    def _compute_resource_type(self):
        for this in self:
            if this.resource_name:
                this.resource_type = this.resource_name._description

class RelatedArtifactDocument(models.Model):
    _name = "hc.related.artifact.document"
    _description = "Related Artifact Document"
    _inherit = ["hc.basic.association", "hc.attachment"]
