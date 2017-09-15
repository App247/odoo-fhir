# -*- coding: utf-8 -*-

from openerp import models, fields, api
from datetime import datetime
from openerp.tools import DEFAULT_SERVER_DATETIME_FORMAT as DTF

class Annotation(models.Model):
    _name = "hc.annotation"
    _description = "Annotation"
    _inherit = ["hc.element"]
    _rec_name = "name"

    name = fields.Char(
        string="Name",
        required="True",
        help="The name of the annotation.")
    text = fields.Text(
        string="Text",
        required="True",
        help="The annotation - text content.")
    recorded_date = fields.Datetime(
        string="Recorded Date",
        default=fields.datetime.now(),
        help="When the annotation was made.")
    author_type = fields.Selection(
        string="Author Type",
        selection=[
            ("string", "String"),
            ("practitioner", "Practitioner"),
            ("patient", "Patient"),
            ("related_person", "Related Person")],
        help="Type of individual responsible for the annotation.")
    author_name = fields.Char(
        string="Author",
        compute="_compute_author_name",
        store="True",
        help="Individual responsible for the annotation.")
    author_string = fields.Char(
        string="Author String",
        help="Individual responsible for the annotation.")
    # author_practitioner_id = fields.Many2one(
    #     comodel_name="hc.res.practitioner",
    #     string="Author Practitioner",
    #     help="Practitioner responsible for the annotation.")
    # author_patient_id = fields.Many2one(
    #     comodel_name="hc.res.patient",
    #     string="Author Patient",
    #     help="Patient responsible for the annotation.")
    # author_related_person_id = fields.Many2one(
    #     comodel_name="hc.res.related.person",
    #     string="Author Related Person",
    #     help="Related Person responsible for the annotation.")

    # def _get_default_date(self):
    #     return datetime.strftime(datetime.strptime(date.today(), DTF), "%Y-%m-%d %H:%M:%S")
        # return date.today().strftime('%Y-%m-%d %H:%M:%S')

    @api.depends('author_type')
    def _compute_author_name(self):
        for hc_annotation in self:
            if hc_annotation.author_type == 'string':
                hc_annotation.author_name = hc_annotation.author_string

    # @api.multi
    # def _compute_author_name(self):
    #     for hc_annotation in self:
    #         if hc_annotation.author_type == 'string':
    #             hc_annotation.author_name = hc_annotation.author_string
    #         elif hc_annotation.author_type == 'practitioner':
    #             hc_annotation.author_name = hc_annotation.author_practitioner_id.name
    #         elif hc_annotation.author_type == 'patient':
    #             hc_annotation.author_name = hc_annotation.author_patient_id.name
    #         elif hc_annotation.author_type == 'related_person':
    #             hc_annotation.author_name = hc_annotation.author_related_person_id.name
