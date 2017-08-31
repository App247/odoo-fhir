# -*- coding: utf-8 -*-

from openerp import models, fields, api

class Communication(models.Model):
    _name = "hc.res.communication"
    _description = "Communication"

    name = fields.Char(
        string="Name",
        compute="_compute_name",
        store="True",
        help="Text representation of the communication event. Subject Name + Category + Sent Date.")
    identifier_ids = fields.One2many(
        comodel_name="hc.communication.identifier",
        inverse_name="communication_id",
        string="Identifiers",
        help="Unique identifier.")
    based_on_ids = fields.One2many(
        comodel_name="hc.communication.based.on",
        inverse_name="communication_id",
        string="Based On",
        help="Request fulfilled by this communication.")
    parent_ids = fields.One2many(
        comodel_name="hc.communication.parent",
        inverse_name="communication_id",
        string="Parents",
        help="Part of this action.")
    status = fields.Selection(
        string="Communication Status",
        selection=[
            ("in-progress", "In-Progress"),
            ("completed", "Completed"),
            ("suspended", "Suspended"),
            ("rejected", "Rejected"),
            ("failed", "Failed")],
        help="The status of the transmission.")
    category_id = fields.Many2one(
        comodel_name="hc.vs.communication.category",
        string="Category",
        help="Message category.")
    medium_ids = fields.Many2many(
        comodel_name="hc.vs.participation.mode",
        string="Mediums",
        help="Communication medium.")
    subject_id = fields.Many2one(
        comodel_name="hc.res.patient",
        string="Subject",
        help="Focus of message.")
    topic_ids = fields.One2many(
        comodel_name="hc.communication.topic",
        inverse_name="communication_id",
        string="Topics",
        help="Focal resources.")
    context_type = fields.Selection(
        string="Context Type",
        selection=[
            ("device", "Device"),
            ("organization", "Organization"),
            ("patient", "Patient"),
            ("practitioner", "Practitioner"),
            ("related_person", "Related Person")],
        help="Encounter or episode leading to message.")
    context_name = fields.Char(
        string="Context",
        compute="_compute_context_name",
        store="True",
        help="Encounter or episode leading to message.")
    context_encounter_id = fields.Many2one(
        comodel_name="hc.res.encounter",
        string="Context Encounter",
        help="Encounter leading to message.")
    context_episode_of_care_id = fields.Many2one(
        comodel_name="hc.res.episode.of.care",
        string="Context Episode Of Care",
        help="Episode leading to message.")
    sent = fields.Datetime(
        string="Sent",
        help="When sent.")
    received = fields.Datetime(
        string="Received",
        help="When received.")
    sender_type = fields.Selection(
        string="Sender Type",
        selection=[
            ("device", "Device"),
            ("organization", "Organization"),
            ("patient", "Patient"),
            ("practitioner", "Practitioner"),
            ("related_person", "Related Person")],
        help="Type of message sender.")
    sender_name = fields.Char(
        string="Sender",
        compute="_compute_sender_name",
        store="True",
        help="Message sender.")
    sender_device_id = fields.Many2one(
        comodel_name="hc.res.device",
        string="Sender Device",
        help="Device message sender.")
    sender_organization_id = fields.Many2one(
        comodel_name="hc.res.organization",
        string="Sender Organization",
        help="Organization message sender.")
    sender_patient_id = fields.Many2one(
        comodel_name="hc.res.patient",
        string="Sender Patient",
        help="Patient message sender.")
    sender_practitioner_id = fields.Many2one(
        comodel_name="hc.res.practitioner",
        string="Sender Practitioner",
        help="Practitioner message sender.")
    sender_related_person_id = fields.Many2one(
        comodel_name="hc.res.related.person",
        string="Sender Related Person",
        help="Related Person message sender.")
    recipient_ids = fields.One2many(
        comodel_name="hc.communication.recipient",
        inverse_name="communication_id",
        string="Recipients",
        help="Message recipient.")
    reason_ids = fields.Many2many(
        comodel_name="hc.vs.act.reason",
        string="Reasons",
        help="Indication for message.")
    note_ids = fields.One2many(
        comodel_name="hc.communication.note",
        inverse_name="communication_id",
        string="Notes",
        help="Comments made about the communication.")
    payload_ids = fields.One2many(
        comodel_name="hc.communication.payload",
        inverse_name="communication_id",
        string="Payloads",
        help="Message payload.")

class CommunicationPayload(models.Model):
    _name = "hc.communication.payload"
    _description = "Communication Payload"

    communication_id = fields.Many2one(
        comodel_name="hc.res.communication",
        string="Communication",
        help="Communication associated with this Communication Payload.")
    sender_type = fields.Selection(
        string="Sender Type",
        required="True",
        selection=[
            ("string", "String"),
            ("attachment", "Attachment"),
            ("code", "Code"),
            ("communication", "Communication")],
        help="Type of message sender.")
    content_name = fields.Char(
        string="Content",
        compute="_compute_content_name",
        store="True",
        help="Message part content.")
    content_string = fields.Char(
        string="Content",
        help="String of message part content.")
    content_attachment_id = fields.Many2one(
        comodel_name="hc.communication.payload.content.attachment",
        string="Content Attachment",
        help="Attachment message part content.")
    content_code_id = fields.Many2one(
        comodel_name="hc.vs.communication.content.code",
        string="Content Code",
        help="Code of message part content.")
    content_communication_id = fields.Many2one(
        comodel_name="hc.res.communication",
        string="Content Communication",
        help="Communication message part content.")

class CommunicationBasedOn(models.Model):
    _name = "hc.communication.based.on"
    _description = "Communication Based On"
    _inherit = ["hc.basic.association"]

    communication_id = fields.Many2one(
        comodel_name="hc.res.communication",
        string="Communication",
        help="Communication associated with this Communication Based On.")
    based_on_type = fields.Selection(
        string="Based On Type",
        selection=[
            ("string", "String"),
            ("code", "Code")],
        help="Type of request fulfilled by this communication.")
    based_on_name = fields.Char(
        string="Based On",
        compute="_compute_based_on_name",
        store="True",
        help="Request fulfilled by this communication.")
    based_on_string = fields.Char(
        string="Based On String",
        help="String request fulfilled by this communication.")
    based_on_code_id = fields.Many2one(
        comodel_name="hc.vs.resource.type",
        string="Based On Code",
        help="Resource type of request fulfilled by this communication.")

class CommunicationIdentifier(models.Model):
    _name = "hc.communication.identifier"
    _description = "Communication identifier"
    _inherit = ["hc.basic.association", "hc.identifier"]

    communication_id = fields.Many2one(
        comodel_name="hc.res.communication",
        string="Communication",
        help="Communication associated with this Communication identifier.")

class CommunicationNote(models.Model):
    _name = "hc.communication.note"
    _description = "Communication Note"
    _inherit = ["hc.basic.association", "hc.annotation"]

    communication_id = fields.Many2one(
        comodel_name="hc.res.communication",
        string="Communication",
        help="Communication associated with this Communication Note.")

class CommunicationParent(models.Model):
    _name = "hc.communication.parent"
    _description = "Communication Parent"
    _inherit = ["hc.basic.association"]

    communication_id = fields.Many2one(
        comodel_name="hc.res.communication",
        string="Communication",
        help="Communication associated with this Communication Parent.")
    parent_type = fields.Selection(
        string="Parent Type",
        selection=[
            ("string", "String"),
            ("code", "Code")],
        help="Type of part of this action.")
    parent_name = fields.Char(
        string="Parent",
        compute="_compute_parent_name",
        store="True",
        help="Part of this action.")
    parent_string = fields.Char(
        string="Parent Strings",
        help="String of part of this action.")
    parent_code_id = fields.Many2one(
        comodel_name="hc.vs.resource.type",
        string="Parent Code",
        help="Resource type of part of this action.")

class CommunicationTopic(models.Model):
    _name = "hc.communication.topic"
    _description = "Communication Topic"
    _inherit = ["hc.basic.association"]

    communication_id = fields.Many2one(
        comodel_name="hc.res.communication",
        string="Communication",
        help="Communication associated with this Communication Topic.")
    topic_type = fields.Selection(
        string="Topic Type",
        selection=[
            ("string", "String"),
            ("code", "Code")],
        help="Type of focal resources.")
    topic_name = fields.Char(
        string="Topic",
        compute="_compute_topic_name",
        store="True", help="Focal resources.")
    topic_string = fields.Char(
        string="Topic Strings",
        help="String of focal resources.")
    topic_code_id = fields.Many2one(
        comodel_name="hc.vs.resource.type",
        string="Topic Code",
        help="Resource type of focal resources.")

class CommunicationPayloadContentAttachment(models.Model):
    _name = "hc.communication.payload.content.attachment"
    _description = "Communication Payload Content Attachment"
    _inherit = ["hc.basic.association", "hc.attachment"]

class CommunicationRecipient(models.Model):
    _name = "hc.communication.recipient"    
    _description = "Communication Recipient"
    _inherit = ["hc.basic.association"]

    communication_id = fields.Many2one(
        comodel_name="hc.res.communication",
        string="Communication",
        help="Communication associated with this Communication Recipient.")
    recipient_type = fields.Selection(
        string="Recipient Type",
        selection=[
            ("device", "Device"),
            ("organization", "Organization"),
            ("patient", "Patient"),
            ("practitioner", "Practitioner"),
            ("related_person", "Related Person"),
            ("group", "Group")],
        help="Type of message recipient.")
    recipient_name = fields.Char(
        string="Recipient",
        compute="_compute_recipient_name",
        store="True",
        help="Message recipient.")
    recipient_device_id = fields.Many2one(
        comodel_name="hc.res.device",
        string="Recipient Device",
        help="Device message recipient.")
    recipient_organization_id = fields.Many2one(
        comodel_name="hc.res.organization",
        string="Recipient Organization",
        help="Organization message recipient.")
    recipient_patient_id = fields.Many2one(
        comodel_name="hc.res.patient",
        string="Recipient Patient",
        help="Patient message recipient.")
    recipient_practitioner_id = fields.Many2one(
        comodel_name="hc.res.practitioner",
        string="Recipient Practitioner",
        help="Practitioner message recipient.")
    recipient_related_person_id = fields.Many2one(
        comodel_name="hc.res.related.person",
        string="Recipient Related Person",
        help="Related Person message recipient.")
    recipient_group_id = fields.Many2one(
        comodel_name="hc.res.group",
        string="Recipient Group",
        help="Group message recipient.")

class CommunicationCategory(models.Model):
    _name = "hc.vs.communication.category"
    _description = "Communication Category"
    _inherit = ["hc.value.set.contains"]
