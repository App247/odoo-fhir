# -*- coding: utf-8 -*-

from openerp import models, fields, api

class AttachmentType(models.Model):
    _name = "hc.vs.attachment.type"
    _description = "Attachment Type"
    _inherit = ["hc.value.set.contains"]


class MimeMediaType(models.Model):
    _name = "hc.vs.mime.media.type"
    _description = "MIME Media Type"
    _inherit = ["hc.value.set.contains"]

    name = fields.Char(
        string="MIME Media Type",
        help="Name of this MIME Media Type.")
    code = fields.Char(
        string="Code",
        help="Code of this MIME Media Type.")
    contains_id = fields.Many2one(
        comodel_name="hc.vs.mime.media.type",
        string="Parent",
        help="Parent MIME Media Type.")

class MimeType(models.Model):
    _name = "hc.vs.mime.type"
    _description = "MIME Type"
    _inherit = ["hc.value.set.contains"]

    name = fields.Char(
        string="MIME Type",
        help="Name of this MIME Type.")
    code = fields.Char(
        string="Code",
        help="Code of this MIME Type.")
    contains_id = fields.Many2one(
        comodel_name="hc.vs.mime.type",
        string="Parent",
        help="Parent MIME Type.")
    media_type_id = fields.Many2one(
        comodel_name="hc.vs.mime.media.type",
        string="MIME Media Type",
        help="Name of this MIME Media Type.")

class Attachment(models.Model):
    _name = "hc.attachment"
    _description = "Attachment"
    _inherit = ["ir.attachment", "hc.element"]
    _rec_name = "name"

    attachment_type_id = fields.Many2one(
        comodel_name="hc.vs.attachment.type",
        string="Attachment Type",
        help="Type of attachment (e.g. ADT Form)")
    # content_type = fields.Many2one( # Called "mimetype" in ir.attachment
    #     comodel_name="hc.vs.mime.type",
    #     string="MIME Type",
    #     help="Mime type of the content, with charset etc.")
    mimetype = fields.Char(
        string="MIME Type",
        help="Mime type of the content, with charset etc.")
    language_id = fields.Many2one(
        comodel_name="res.lang",
        string="Language",
        help="Human language of the content (BCP-47).")
    # data = fields.Binary( # Called "db_datas" in FHIR Specification
    #     string="Data",
    #     help="Data inline, base64ed.")
    db_datas = fields.Binary(
        attachment=True)
    url = fields.Char(
        string="URL",
        help="URI where the data can be found.")
    file_size = fields.Integer( # Called "size" in FHIR Specification
        help="Number of bytes of content (if url provided).")
    # hash = fields.Binary( # Called bin_data in ir.attachment
    #     string="Hash",
    #     help="Hash of the data (sha-1, base64ed ).")
    name = fields.Char(
        string="Title",
        help="Label to display in place of the data.")
    creation_date = fields.Datetime(
        string="Creation Date",
        help="Date attachment was first created.")

# Constraints

# If the Attachment has datas, it SHALL have a mimetype

    has_data = fields.Boolean(
        string='Has Data',
        invisible=True,
        help="Indicates if data exists. Used to enforce constraint mimetype or data.")

    @api.onchange('datas')
    def onchange_datas(self):
        if self.datas:
            self.mimetype = False
            self.has_data = True
        else:
            self.has_data = False
