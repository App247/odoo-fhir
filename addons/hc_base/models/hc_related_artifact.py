# -*- coding: utf-8 -*-

from openerp import models, fields, api

class RelatedArtifact(models.Model):
    _name = "hc.related.artifact"
    _description = "Related Artifact"
    _inherit = ["hc.element"]

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
    display = fields.Char(
        string="Display",
        help="Brief description of the related artifact.")
    citation = fields.Char(
        string="Citation",
        help="Bibliographic citation for the artifact.")
    url = fields.Char(
        string="URI",
        help="URL for the related artifact.")
    document_id = fields.Many2one(
        comodel_name="hc.related.artifact.document",
        string="Document", help="The related document.")
    resource_type = fields.Selection(
        string="Resource Type",
        selection=[
            ("string", "String"),
            ("code", "Code")],
        help="Type of related resource.")
    resource_name = fields.Char(
        string="Resource",
        compute="_compute_resource_name",
        store="True",
        help="The related resource.")
    resource_string = fields.Char(
        string="Resource String",
        help="String of the related resource.")
    resource_code_id = fields.Many2one(
        comodel_name="hc.vs.resource.type",
        string="Resource Code",
        help="Type of resource of the related resource.")

class RelatedArtifactDocument(models.Model):
    _name = "hc.related.artifact.document"
    _description = "Related Artifact Document"
    _inherit = ["hc.basic.association", "hc.attachment"]
