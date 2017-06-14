# -*- coding: utf-8 -*-

from openerp import models, fields, api

class DocumentManifest(models.Model):    
    _name = "hc.res.document.manifest"    
    _description = "Document Manifest"        

    master_identifier_id = fields.Many2one(
        comodel_name="hc.document.manifest.master.identifier", 
        string="Master Identifier", 
        help="Unique Identifier for the set of documents.")                
    identifier_ids = fields.One2many(
        comodel_name="hc.document.manifest.identifier", 
        inverse_name="document_manifest_id", 
        string="Identifiers", 
        help="Other identifiers for the manifest.")                
    subject_type = fields.Selection(
        string="Subject Type", 
        selection=[
            ("string", "String"), 
            ("encounter", "Encounter"), 
            ("episode_of_care", "Episode Of Care"), 
            ("clinical_impression", "Clinical Impression")],
        help="Type of the subject of the set of documents.")                
    subject_name = fields.Char(
        string="Subject", 
        compute="_compute_subject_name", 
        store="True", 
        help="The subject of the set of documents.")                
    subject_patient_id = fields.Many2one(
        comodel_name="hc.res.patient", 
        string="Subject Patient", 
        help="Patient the subject of the set of documents.")                
    subject_practitioner_id = fields.Many2one(
        comodel_name="hc.res.practitioner", 
        string="Subject Practitioner", 
        help="Practitioner the subject of the set of documents.")                
    subject_group_id = fields.Many2one(
        comodel_name="hc.res.group", 
        string="Subject Group", 
        help="Group the subject of the set of documents.")                
    subject_device_id = fields.Many2one(
        comodel_name="hc.res.device", 
        string="Subject Device", 
        help="Device the subject of the set of documents.")                
    recipient_ids = fields.One2many(
        comodel_name="hc.document.manifest.recipient", 
        inverse_name="document_manifest_id", 
        string="Recipients", 
        help="Intended to get notified about this set of documents.")                
    type_id = fields.Many2one(
        comodel_name="hc.vs.document.manifest.type", 
        string="Type", 
        help="What kind of document set this is.")                
    author_ids = fields.One2many(
        comodel_name="hc.document.manifest.author", 
        inverse_name="document_manifest_id", 
        string="Authors", 
        help="Who and/or what authored the document.")                
    created = fields.Datetime(
        string="Created", 
        help="When this document manifest created.")                
    source = fields.Char(
        string="Source URI", 
        help="The source system/application/software.")                
    status = fields.Selection(
        string="Document Manifest Status", 
        required="True", 
        selection=[
            ("current", "Current"), 
            ("superceded", "Superceded"), 
            ("entered-in-error", "Entered-In-Error")], 
        help="The status of this document manifest.")                
    description = fields.Text(
        string="Description", 
        help="Human-readable description (title).")                
    content_ids = fields.One2many(
        comodel_name="hc.document.manifest.content", 
        inverse_name="document_manifest_id", 
        string="Contents", 
        required="True", 
        help="Contents of the manifest.")                
    related_ids = fields.One2many(
        comodel_name="hc.document.manifest.related", 
        inverse_name="document_manifest_id", 
        string="Related", 
        help="Related things.")                

class DocumentManifestContent(models.Model):    
    _name = "hc.document.manifest.content"    
    _description = "Document Manifest Content"        

    document_manifest_id = fields.Many2one(
        comodel_name="hc.res.document.manifest", 
        string="Document Manifest", 
        help="Document Manifest associated with this Document Manifest Content.")                
    p_type = fields.Selection(
        string="P Type", 
        required="True", 
        selection=[
            ("string", "String"),
            ("encounter", "Encounter"),
            ("episode_of_care", "Episode Of Care"),
            ("clinical_impression", "Clinical Impression")],
        help="Type of contents of this set of documents.")                
    p_name = fields.Char(
        string="P", 
        compute="_compute_p_name", 
        store="True", 
        help="Contents of this set of documents.")                
    p_attachment_id = fields.Many2one(
        comodel_name="hc.document.manifest.content.attachment", 
        string="P Attachment", 
        required="True", 
        help="Attachment content of this set of documents.")                
    p_document_reference_id = fields.Many2one(
        comodel_name="hc.res.document.reference", 
        string="P Document Reference", 
        required="True", 
        help="Document Reference content of this set of documents.")                
    p_media_id = fields.Many2one(
        comodel_name="hc.res.media", 
        string="P Media", 
        required="True", 
        help="Media content of this set of documents.")                

class DocumentManifestRelated(models.Model):    
    _name = "hc.document.manifest.related"    
    _description = "Document Manifest Related"        

    document_manifest_id = fields.Many2one(
        comodel_name="hc.res.document.manifest", 
        string="Document Manifest", 
        help="Document Manifest associated with this Document Manifest Related.")                
    identifier_id = fields.Many2one(
        comodel_name="hc.document.manifest.related.identifier", 
        string="Identifier", 
        help="Related Identifier.")                
    ref_id = fields.Many2one(
        comodel_name="hc.document.manifest.related.ref", 
        string="Ref", 
        help="Related Resource.")                

class DocumentManifestMasterIdentifier(models.Model):    
    _name = "hc.document.manifest.master.identifier"    
    _description = "Document Manifest Master Identifier"        
    _inherit = ["hc.basic.association", "hc.identifier"]

class DocumentManifestIdentifier(models.Model):    
    _name = "hc.document.manifest.identifier"    
    _description = "Document Manifest Identifier"        
    _inherit = ["hc.basic.association", "hc.identifier"]

    document_manifest_id = fields.Many2one(
        comodel_name="hc.res.document.manifest", 
        string="Document Manifest", 
        help="Document Manifest associated with this Document Manifest Identifier.")                

class DocumentManifestRecipient(models.Model):    
    _name = "hc.document.manifest.recipient"    
    _description = "Document Manifest Recipient"        
    _inherit = ["hc.basic.association"]

    document_manifest_id = fields.Many2one(
        comodel_name="hc.res.document.manifest", 
        string="Document Manifest", 
        help="Document Manifest associated with this Document Manifest Recipient.")                
    recipient_type = fields.Selection(
        string="Recipient Type", 
        selection=[
            ("string", "String"), 
            ("encounter", "Encounter"), 
            ("episode_of_care", "Episode Of Care"), 
            ("clinical_impression", "Clinical Impression")],
        help="Type of intended to get notified about this set of documents.")                
    recipient_name = fields.Char(
        string="Recipient", 
        compute="_compute_recipient_name", 
        store="True", 
        help="Intended to get notified about this set of documents.")                
    recipient_patient_id = fields.Many2one(
        comodel_name="hc.res.patient", 
        string="Recipient Patient", 
        help="Patient intended to get notified about this set of documents.")                
    recipient_practitioner_id = fields.Many2one(
        comodel_name="hc.res.practitioner", 
        string="Recipient Practitioner", 
        help="Practitioner intended to get notified about this set of documents.")                
    recipient_organization_id = fields.Many2one(
        comodel_name="hc.res.organization", 
        string="Recipient Organization", 
        help="Organization intended to get notified about this set of documents.")                

class DocumentManifestAuthor(models.Model):    
    _name = "hc.document.manifest.author"    
    _description = "Document Manifest Author"        
    _inherit = ["hc.basic.association"]

    document_manifest_id = fields.Many2one(
        comodel_name="hc.res.document.manifest", 
        string="Document Manifest", 
        help="Document Manifest associated with this Document Manifest Author.")                
    author_type = fields.Selection(
        string="Author Type", 
        selection=[
            ("string", "String"),
            ("encounter", "Encounter"),
            ("episode_of_care", "Episode Of Care"),
            ("clinical_impression", "Clinical Impression")], 
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

class DocumentManifestRelatedIdentifier(models.Model):    
    _name = "hc.document.manifest.related.identifier"    
    _description = "Document Manifest Related Identifier"        
    _inherit = ["hc.basic.association", "hc.identifier"]

class DocumentManifestRelatedRef(models.Model):    
    _name = "hc.document.manifest.related.ref"    
    _description = "Document Manifest Related Ref"        
    _inherit = ["hc.basic.association"]

    # Need to define Reference Type

class DocumentManifestContentAttachment(models.Model):
    _name = "hc.document.manifest.content.attachment"   
    _description = "Document Manifest Content Attachment"       
    _inherit = ["hc.basic.association", "hc.attachment"]    

class DocumentManifestType(models.Model):    
    _name = "hc.vs.document.manifest.type"    
    _description = "Document Manifest Type"        
    _inherit = ["hc.value.set.contains"]
