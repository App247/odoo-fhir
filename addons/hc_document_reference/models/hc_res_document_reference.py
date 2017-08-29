# -*- coding: utf-8 -*-

from openerp import models, fields, api

class DocumentReference(models.Model):
    _name = "hc.res.document.reference"
    _description = "Document Reference"

    master_identifier_id = fields.Many2one(
        comodel_name="hc.document.reference.master.identifier",
        string="Master Identifier",
        help="Master Version Specific Identifier.")
    identifier_ids = fields.One2many(
        comodel_name="hc.document.reference.identifier",
        inverse_name="document_reference_id",
        string="Identifiers",
        help="Other identifiers for the document.")


    subject_type = fields.Selection(
        string="Subject Type",
        selection=[
            ("patient", "Patient"),
            ("practitioner", "Practitioner"),
            ("group", "Group"),
            ("device", "Device")],
        help="Type of who/what is the subject of the document.")
    subject_name = fields.Char(
        string="Subject",
        compute="_compute_subject_name",
        store="True",
        help="Who/what is the subject of the document.")
    subject_patient_id = fields.Many2one(
        comodel_name="hc.res.patient",
        string="Subject Patient",
        help="Patient who/what is the subject of the document.")
    subject_practitioner_id = fields.Many2one(
        comodel_name="hc.res.practitioner",
        string="Subject Practitioner",
        help="Practitioner who/what is the subject of the document.")
    subject_group_id = fields.Many2one(
        comodel_name="hc.res.group",
        string="Subject Group",
        help="Group who/what is the subject of the document.")
    subject_device_id = fields.Many2one(
        comodel_name="hc.res.device",
        string="Subject Device",
        help="Device who/what is the subject of the document.")
    type_id = fields.Many2one(
        comodel_name="hc.vs.c80.doc.type.code",
        string="Type",
        required="True",
        help="Kind of document.")
    class_id = fields.Many2one(
        comodel_name="hc.vs.c80.doc.class.code",
        string="Class",
        help="Categorization of document.")
    format_ids = fields.One2many(
        comodel_name="hc.document.reference.format",
        inverse_name="document_reference_id",
        string="Format URIs",
        help="URI of format/content rules for the document.")
    author_ids = fields.One2many(
        comodel_name="hc.document.reference.author",
        inverse_name="document_reference_id",
        string="Authors",
        help="Who and/or what authored the document.")
    custodian_id = fields.Many2one(
        comodel_name="hc.res.organization",
        string="Custodian",
        help="Org which maintains the document.")
    authenticator_type = fields.Selection(
        string="Authenticator Type",
        selection=[
            ("Practitioner", "Practitioner"),
            ("Organization", "Organization")],
        help="Type of who/what is the subject of the document.")
    authenticator_name = fields.Char(
        string="Authenticator",
        compute="_compute_authenticator_name",
        store="True",
        help="Who/what authenticated the document.")
    authenticator_practitioner_id = fields.Many2one(
        comodel_name="hc.res.practitioner",
        string="Authenticator Practitioner",
        help="Practitioner who/what authenticated the document.")
    authenticator_organization_id = fields.Many2one(
        comodel_name="hc.res.organization",
        string="Authenticator Organization",
        help="Organization who/what authenticated the document.")
    created = fields.Datetime(
        string="Created",
        help="Document creation time.")
    indexed = fields.Datetime(
        string="Indexed",
        required="True",
        help="When this document reference created.")
    status = fields.Selection(
        string="Status",
        required="True",
        selection=[
            ("current", "Current"),
            ("superceded", "Superceded"),
            ("entered-in-error", "Entered-In-Error")],
        help="The status of this document reference.")
    doc_status = fields.Selection(
        string="Doc Status",
        selection=[
            ("preliminary", "Preliminary"),
            ("final", "Final"),
            ("appended", "Appended"),
            ("amended", "Amended"),
            ("entered-in-error", "Entered-In-Error")],
        help="The status of the underlying document.")
    description = fields.Text(
        string="Description",
        help="Human-readable description (title).")
    security_label_ids = fields.Many2many(
        comodel_name="hc.vs.security.label",
        relation="document_reference_security_label_rel",
        string="Confidentialities",
        help="Document security-tags.")
    relates_to_ids = fields.One2many(
        comodel_name="hc.document.reference.relates.to",
        inverse_name="document_reference_id",
        string="Relates Tos",
        help="Relationships to other documents.")
    content_ids = fields.One2many(
        comodel_name="hc.document.reference.content",
        inverse_name="document_reference_id",
        string="Contents",
        required="True",
        help="Document referenced.")
    context_ids = fields.One2many(
        comodel_name="hc.document.reference.context",
        inverse_name="document_reference_id",
        string="Contexts",
        help="Clinical context of document.")

class DocumentReferenceRelatesTo(models.Model):
    _name = "hc.document.reference.relates.to"
    _description = "Document Reference Relates To"

    document_reference_id = fields.Many2one(
        comodel_name="hc.res.document.reference",
        string="Document Reference",
        help="Document Reference associated with this Document Reference Relates To.")
    code = fields.Selection(
        string="Code",
        required="True",
        selection=[
            ("replaces", "Replaces"),
            ("transforms", "Transforms"),
            ("signs", "Signs"),
            ("appends", "Appends")],
        help="The type of relationship that this document has with another document.")
    target_id = fields.Many2one(
        comodel_name="hc.res.document.reference",
        string="Target",
        required="True",
        help="Target of the relationship.")

class DocumentReferenceContent(models.Model):
    _name = "hc.document.reference.content"
    _description = "Document Reference Content"

    document_reference_id = fields.Many2one(
        comodel_name="hc.res.document.reference",
        string="Document Reference",
        help="Document Reference associated with this Document Reference Content.")
    attachment_id = fields.Many2one(
        comodel_name="hc.document.reference.content.attachment",
        string="Attachment",
        required="True",
        help="Where to access the document.")
    format_ids = fields.Many2many(
        comodel_name="hc.vs.format.code",
        relation="document_reference_content_format_rel",
        string="Formats",
        help="Format/content rules for the document.")

class DocumentReferenceContext(models.Model):
    _name = "hc.document.reference.context"
    _description = "Document Reference Context"

    document_reference_id = fields.Many2one(
        comodel_name="hc.res.document.reference",
        string="Document Reference",
        help="Document Reference associated with this Document Reference Context.")
    encounter_id = fields.Many2one(
        comodel_name="hc.res.encounter",
        string="Encounter",
        help="Context of the document content.")
    event_ids = fields.Many2many(
        comodel_name="hc.vs.act.code",
        relation="document_reference_context_event_rel",
        string="Events",
        help="Main Clinical Acts Documented.")
    period = fields.Datetime(
        string="Period",
        help="Start of the time of service that is being documented.")
    period = fields.Datetime(
        string="Period",
        help="End of the time of service that is being documented.")
    facility_type_id = fields.Many2one(
        comodel_name="hc.vs.c80.facility.code",
        string="Facility Type",
        help="Kind of facility where patient was seen.")
    practice_setting_id = fields.Many2one(
        comodel_name="hc.vs.c80.practice.code",
        string="Practice Setting",
        help="Additional details about where the content was created (e.g. clinical specialty).")
    source_patient_info_id = fields.Many2one(
        comodel_name="hc.res.patient",
        string="Source Patient Info",
        help="Source patient info.")
    related_ids = fields.One2many(
        comodel_name="hc.document.reference.context.related",
        inverse_name="context_id",
        string="Related",
        help="Related things.")

class DocumentReferenceContextRelated(models.Model):
    _name = "hc.document.reference.context.related"
    _description = "Document Reference Context Related"

    context_id = fields.Many2one(
        comodel_name="hc.document.reference.context",
        string="Context",
        help="Context associated with this Document Reference Context Related.")
    identifier_id = fields.Many2one(
        comodel_name="hc.document.reference.context.related.identifier",
        string="Identifier",
        help="Related Identifier.")
    ref_id = fields.Many2one(
        comodel_name="hc.document.reference.context.related.ref",
        string="Ref",
        help="Related Resource.")

class DocumentReferenceIdentifier(models.Model):
    _name = "hc.document.reference.identifier"
    _description = "Document Reference Identifier"
    _inherit = ["hc.basic.association", "hc.identifier"]

    document_reference_id = fields.Many2one(
        comodel_name="hc.res.document.reference",
        string="Document Reference",
        help="Document Reference associated with this Document Reference Identifier.")

class DocumentReferenceFormat(models.Model):
    _name = "hc.document.reference.format"
    _description = "Document Reference Format"
    _inherit = ["hc.basic.association"]

    document_reference_id = fields.Many2one(
        comodel_name="hc.res.document.reference",
        string="Document Reference",
        help="Document Reference associated with this Document Reference Format.")
    format = fields.Char(
        string="Format URI",
        help="URI of Format associated with this Document Reference Format.")

class DocumentReferenceAuthor(models.Model):
    _name = "hc.document.reference.author"
    _description = "Document Reference Author"
    _inherit = ["hc.basic.association"]

    document_reference_id = fields.Many2one(
        comodel_name="hc.res.document.reference",
        string="Document Reference",
        help="Document Reference associated with this Document Reference Author.")
    author_type = fields.Selection(
        string="Author Type",
        selection=[
            ("Practitioner", "Practitioner"),
            ("Organization", "Organization"),
            ("Device", "Device"),
            ("Patient", "Patient"),
            ("Related Person", "Related Person")],
        required="True",
        help="Type of who and/or what authored the document.")
    author_name = fields.Char(
        string="Author",
        compute="_compute_author_name",
        store="True",
        help="Who and/or what authored the document.")
    author_practitioner_id = fields.Many2one(
        comodel_name="hc.res.practitioner",
        string="Author Practitioner",
        help="Practitioner who and/or what authored the document.")
    author_organization_id = fields.Many2one(
        comodel_name="hc.res.organization",
        string="Author Organization",
        help="Organization who and/or what authored the document.")
    author_device_id = fields.Many2one(
        comodel_name="hc.res.device",
        string="Author Device",
        help="Device who and/or what authored the document.")
    author_patient_id = fields.Many2one(
        comodel_name="hc.res.patient",
        string="Author Patient",
        help="Patient who and/or what authored the document.")
    author_related_person_id = fields.Many2one(
        comodel_name="hc.res.related.person",
        string="Author Related Person",
        help="Related Person who and/or what authored the document.")

class DocumentReferenceMasterIdentifier(models.Model):
    _name = "hc.document.reference.master.identifier"
    _description = "Document Reference Master Identifier"
    _inherit = ["hc.basic.association", "hc.identifier"]

class DocumentReferenceContentAttachment(models.Model):
    _name = "hc.document.reference.content.attachment"
    _description = "Document Reference Content Attachment"
    _inherit = ["hc.basic.association", "hc.attachment"]

class DocumentReferenceContextRelatedIdentifier(models.Model):
    _name = "hc.document.reference.context.related.identifier"
    _description = "Document Reference Context Related Identifier"
    _inherit = ["hc.basic.association", "hc.identifier"]

class DocumentReferenceContextRelatedRef(models.Model):
    _name = "hc.document.reference.context.related.ref"
    _description = "Document Reference Context Related Ref"
    _inherit = ["hc.basic.association"]

    ref_type = fields.Selection(
        string="Ref Type",
        required="True",
        selection=[
            ("string", "String"),
            ("encounter", "Encounter"),
            # ("clinical_impression", "Clinical Impression"),
            ("episode_of_care", "Episode Of Care")],
        help="Type of related resource.")
    ref_name = fields.Char(
        string="Ref",
        compute="_compute_ref_name",
        store="True",
        help="Related Resource.")
    ref_string = fields.Char(
        string="Ref String",
        help="String related resource.")
    ref_encounter_id = fields.Many2one(
        comodel_name="hc.res.encounter",
        string="Ref Encounter",
        help="Encounter related resource.")
    ref_episode_of_care_id = fields.Many2one(
        comodel_name="hc.res.episode.of.care",
        string="Ref Episode Of Care",
        help="Episode Of Care related resource.")
    # ref_clinical_impression_id = fields.Many2one(
    #     comodel_name="hc.res.clinical.impression",
    #     string="Ref Clinical Impression",
    #     help="Clinical Impression related resource.")
