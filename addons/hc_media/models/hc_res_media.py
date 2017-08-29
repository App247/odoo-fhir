# -*- coding: utf-8 -*-

from openerp import models, fields, api

class Media(models.Model):
    _name = "hc.res.media"
    _description = "Media"
    _inherit = ["hc.domain.resource"]
    _rec_name = "name"

    name = fields.Char(
        string="Name",
        compute="_compute_name",
        store="True",
        help="Text representation of the media. Subject Name + Type + Occurrence.")
    identifier_ids = fields.One2many(
        comodel_name="hc.media.identifier",
        inverse_name="media_id",
        string="Identifiers",
        help="Identifier(s) for the image.")
    based_on_ids = fields.One2many(
        comodel_name="hc.media.based.on",
        inverse_name="media_id",
        string="Based Ons",
        help="Procedure that caused this media to be created.")
    type = fields.Selection(
        string="Media Type",
        required="True",
        selection=[
            ("photo", "Photo"),
            ("video", "Video"),
            ("audio", "Audio")],
        help="Whether the media is a photo (still image), an audio recording, or a video recording.")
    subtype_id = fields.Many2one(
        comodel_name="hc.vs.digital.media.subtype",
        string="Subtype",
        help="The type of acquisition equipment/process.")
    view_id = fields.Many2one(
        comodel_name="hc.vs.media.view",
        string="View",
        help="Imaging view e.g Lateral or Antero-posterior.")
    subject_type = fields.Selection(
        string="Subject Type",
        selection=[
            ("Patient", "Patient"),
            ("Practitioner", "Practitioner"),
            ("Group", "Group"),
            ("Device", "Device"),
            ("Specimen", "Specimen")],
        help="Type of patient observations supporting recommendation.")
    subject_name = fields.Char(
        string="Subject",
        compute="_compute_subject_name",
        store="True",
        help="Who/What this Media is a record of.")
    subject_patient_id = fields.Many2one(
        comodel_name="hc.res.patient",
        string="Subject Patient",
        help="Patient this media is a record of.")
    subject_practitioner_id = fields.Many2one(
        comodel_name="hc.res.practitioner",
        string="Subject Practitioner",
        help="Practitioner this media is a record of.")
    subject_group_id = fields.Many2one(
        comodel_name="hc.res.group",
        string="Subject Group",
        help="Group this media is a record of.")
    subject_device_id = fields.Many2one(
        comodel_name="hc.res.device",
        string="Subject Device",
        help="Device this media is a record of.")
    subject_specimen_id = fields.Many2one(
        comodel_name="hc.res.specimen",
        string="Subject Specimen",
        help="Specimen this media is a record of.")
    context_type = fields.Selection(
        string="Context Type",
        selection=[
            ("encounter", "Encounter"),
            ("episode_of_care", "Episode Of Care")],
        help="Type of Encounter / Episode associated with media.")
    context_name = fields.Char(
        string="Context",
        compute="_compute_context_name",
        store="True",
        help="Encounter / Episode associated with media.")
    context_encounter_id = fields.Many2one(
        comodel_name="hc.res.encounter",
        string="Context Encounter",
        help="Encounter associated with media.")
    context_episode_of_care_id = fields.Many2one(
        comodel_name="hc.res.episode.of.care",
        string="Context Episode Of Care",
        help="Episode associated with media.")
    occurrence_type = fields.Selection(
        string="Occurrence Type",
        selection=[
            ("date_time", "Date Time"),
            ("period", "Period")],
        help="Type of when Media was collected.")
    occurrence_name = fields.Char(
        string="Occurrence",
        compute="_compute_occurrence_name",
        store="True",
        help="When Media was collected.")
    occurrence_date_time = fields.Datetime(
        string="Occurrence Date Time",
        help="Date Time when Media was collected.")
    occurrence_start_date = fields.Datetime(
        string="Occurrence Start Date",
        help="Start of the period when Media was collected.")
    occurrence_end_date = fields.Datetime(
        string="Occurrence End Date",
        help="End of the period when Media was collected.")
    operator_id = fields.Many2one(
        comodel_name="hc.res.practitioner",
        string="Operator",
        help="The person who generated the image.")
    reason_code_ids = fields.Many2many(
        comodel_name="hc.vs.procedure.reason",
        string="Reason Codes",
        help="Why was event performed?")
    body_site_id = fields.Many2one(
        comodel_name="hc.vs.body.site",
        string="Body Site",
        help="Body part in media.")
    device_type = fields.Selection(
        string="Device Type",
        selection=[
            ("device", "Device"),
            ("device_metric", "Device Metric")],
        help="Type of observing Device.")
    device_name = fields.Char(
        string="Device",
        compute="_compute_device_name",
        store="True",
        help="Observing Device.")
    device_id = fields.Many2one(
        comodel_name="hc.res.device",
        string="Device",
        help="Observing Device.")
    device_metric_id = fields.Many2one(
        comodel_name="hc.res.device.metric",
        string="Device Metric",
        help="Observing Device Metric.")
    height = fields.Integer(
        string="Height",
        help="Height of the image in pixels(photo/video).")
    width = fields.Integer(
        string="Width",
        help="Width of the image in pixels (photo/video).")
    frames = fields.Integer(
        string="Frames",
        help="Number of frames if > 1 (photo).")
    duration = fields.Integer(
        string="Duration",
        help="Length in seconds (audio / video).")
    content_id = fields.Many2one(
        comodel_name="hc.media.content",
        string="Content",
        required="True",
        help="Actual Media - reference or data.")
    note_ids = fields.One2many(
        comodel_name="hc.media.note",
        inverse_name="media_id",
        string="Notes",
        help="Comments made about the media.")

    @api.depends('subject_name', 'type', 'occurrence_name')
    def _compute_name(self):
        comp_name = '/'
        for hc_res_media in self:
            if hc_res_media.subject_name:
                comp_name = hc_res_media.subject_name.name or ''
            if hc_res_media.type:
                comp_name = comp_name + ", " + hc_res_media.type or ''
            if hc_res_media.occurrence_name:
                comp_name = comp_name + ", " + hc_res_media.occurrence_name or ''
            hc_res_media.name = comp_name

    @api.multi
    def _compute_subject_name(self):
        for hc_res_media in self:
            if hc_res_media.subject_type == 'patient':
                hc_res_media.subject_name = hc_res_media.subject_patient_id.name
            elif hc_res_media.subject_type == 'practitioner':
                hc_res_media.subject_name = hc_res_media.subject_practitioner_id.name
            elif hc_res_media.subject_type == 'group':
                hc_res_media.subject_name = hc_res_media.subject_group_id.name
            elif hc_res_media.subject_type == 'device':
                hc_res_media.subject_name = hc_res_media.subject_device_id.name
            elif hc_res_media.subject_type == 'specimen':
                hc_res_media.subject_name = hc_res_media.subject_specimen_id.name

    @api.multi
    def _compute_context_name(self):
        for hc_res_media in self:
            if hc_res_media.context_type == 'encounter':
                hc_res_media.context_name = hc_res_media.context_encounter_id.name
            elif hc_res_media.context_type == 'episode_of_care':
                hc_res_media.context_name = hc_res_media.context_episode_of_care_id.name

    @api.multi
    def _compute_occurrence_name(self):
        for hc_res_media in self:
            if hc_res_media.occurrence_type == 'date_time':
                hc_res_media.occurrence_name = str(hc_res_media.occurrence_encounter_date_time)
            elif hc_res_media.occurrence_type == 'period':
                hc_res_media.occurrence_name = "Between " + str(hc_res_media.occurrence_start_date) + " and " + str(hc_res_media.occurrence_end_date)

    @api.multi
    def _compute_device_name(self):
        for hc_res_media in self:
            if hc_res_media.device_type == 'device':
                hc_res_media.device_name = hc_res_media.device_id.name
            elif hc_res_media.device_type == 'device_metric':
                hc_res_media.device_name = hc_res_media.device_metric_id.name

class MediaIdentifier(models.Model):
    _name = "hc.media.identifier"
    _description = "Media Identifier"
    _inherit = ["hc.basic.association", "hc.identifier"]

    media_id = fields.Many2one(
        comodel_name="hc.res.media",
        string="Media",
        help="Media associated with this media content identifier.")

class MediaBasedOn(models.Model):
    _name = "hc.media.based.on"
    _description = "Media Based On"
    _inherit = ["hc.basic.association"]

    media_id = fields.Many2one(
        comodel_name="hc.res.media",
        string="Media",
        help="Media associated with this Media Based On.")
    based_on_id = fields.Many2one(
        comodel_name="hc.res.procedure.request",
        string="Based On",
        help="Procedure Request associated with this Media Based On.")

class MediaContent(models.Model):
    _name = "hc.media.content"
    _description = "Media Content"
    _inherit = ["hc.basic.association", "hc.attachment"]

    media_id = fields.Many2one(
        comodel_name="hc.res.media",
        string="Media",
        help="Media associated with this Media Content.")

class MediaNote(models.Model):
    _name = "hc.media.note"
    _description = "Media Note"
    _inherit = ["hc.basic.association", "hc.annotation"]

    media_id = fields.Many2one(
        comodel_name="hc.res.media",
        string="Media",
        help="Media associated with this Media Note.")

class DigitalMediaSubtype(models.Model):
    _name = "hc.vs.digital.media.subtype"
    _description = "Digital Media Subtype"
    _inherit = ["hc.value.set.contains"]

class MediaView(models.Model):
    _name = "hc.vs.media.view"
    _description = "Media View"
    _inherit = ["hc.value.set.contains"]
