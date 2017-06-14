# -*- coding: utf-8 -*-

from openerp import models, fields, api

class Composition(models.Model):    
    _name = "hc.res.composition"    
    _description = "Composition"        

    identifier_id = fields.Many2one(
        comodel_name="hc.composition.identifier", 
        string="Identifier", 
        help="Logical identifier of composition (version-independent).")                
    composition_date = fields.Datetime(
        string="Composition Date", 
        required="True", 
        help="Composition editing time.")                
    type_id = fields.Many2one(
        comodel_name="hc.vs.doc.type.code", 
        string="Type", 
        required="True", 
        help="Kind of composition (LOINC if possible).")                
    class_id = fields.Many2one(
        comodel_name="hc.vs.doc.class.code", 
        string="Class", 
        help="Categorization of Composition.")                
    title = fields.Char(
        string="Title", 
        help="Human Readable name/title.")                
    status = fields.Selection(
        string="Composition Status", 
        required="True", 
        selection=[
            ("preliminary", "Preliminary"), 
            ("final", "Final"), 
            ("appended", "Appended"), 
            ("amended", "Amended"), 
            ("entered-in-error", "Entered-In-Error")], 
        help="The workflow/clinical status of this composition.")                
    confidentiality_id = fields.Many2one(
        comodel_name="hc.vs.confidential.classification", 
        string="Confidentiality", 
        help="As defined by affinity domain.")                
    subject_type = fields.Selection(
        string="Subject Type", 
        required="True", 
        selection=[
            ("patient", "Patient"),
            ("practitioner", "Practitioner"),
            ("group", "Group"),
            ("device", "Device")],
        help="Type of who and/or what the composition is about.")                
    subject_name = fields.Char(
        string="Subject", 
        compute="_compute_subject_name", 
        store="True", 
        help="Who and/or what the composition is about.")                
    subject_patient_id = fields.Many2one(
        comodel_name="hc.res.patient", 
        string="Subject Patient", 
        help=" who and/or what the composition is about.")               
    subject_practitioner_id = fields.Many2one(
        comodel_name="hc.res.practitioner", 
        string="Subject Practitioner", 
        help="Practitioner who and/or what the composition is about.")                
    subject_group_id = fields.Many2one(
        comodel_name="hc.res.group", 
        string="Subject Group", 
        help="Group who and/or what the composition is about.")                
    subject_device_id = fields.Many2one(
        comodel_name="hc.res.device", 
        string="Subject Device", 
        help="Device who and/or what the composition is about.")                
    author_ids = fields.One2many(
        comodel_name="hc.composition.author", 
        inverse_name="composition_id", 
        string="Authors", 
        required="True", 
        help="Who and/or what authored the composition.")                
    custodian_id = fields.Many2one(
        comodel_name="hc.res.organization", 
        string="Custodian", 
        help="Organization which maintains the composition.")                
    encounter_id = fields.Many2one(
        comodel_name="hc.res.encounter", 
        string="Encounter", 
        help="Context of the Composition.")                
    attester_ids = fields.One2many(
        comodel_name="hc.composition.attester", 
        inverse_name="composition_id", 
        string="Attesters", 
        help="Attests to accuracy of composition.")                
    event_ids = fields.One2many(
        comodel_name="hc.composition.event", 
        inverse_name="composition_id", 
        string="Events", 
        help="The clinical service(s) being documented.")                
    section_ids = fields.One2many(
        comodel_name="hc.composition.section", 
        inverse_name="composition_id", 
        string="Sections", 
        help="Composition is broken into sections.")                

class CompositionAttester(models.Model):    
    _name = "hc.composition.attester"    
    _description = "Composition Attester"        

    composition_id = fields.Many2one(
        comodel_name="hc.res.composition", 
        string="Composition", 
        help="Composition associated with this Composition Attester.")                
    mode_ids = fields.Many2many(
        comodel_name="hc.vs.composition.attestation.mode", 
        string="Modes", 
        required="True", 
        help="The type of attestation the authenticator offers.")                
    attester_time = fields.Datetime(
        string="Attester Time", 
        help="When composition attested.")                
    party_type = fields.Selection(
        string="Party Type", 
        selection=[
            ("patient", "Patient"), 
            ("practitioner", "Practitioner"), 
            ("organization", "Organization")], 
        help="Type of who attested the composition.")                
    party_name = fields.Char(
        string="Party", 
        compute="_compute_party_name", 
        store="True", 
        help="Who attested the composition.")                
    party_patient_id = fields.Many2one(
        comodel_name="hc.res.patient", 
        string="Party Patient", 
        help="Patient who attested the composition.")                
    party_practitioner_id = fields.Many2one(
        comodel_name="hc.res.practitioner", 
        string="Party Practitioner", 
        help="Practitioner who attested the composition.")                
    party_organization_id = fields.Many2one(
        comodel_name="hc.res.organization", 
        string="Party Organization", 
        help="Organization who attested the composition.")                

class CompositionEvent(models.Model):    
    _name = "hc.composition.event"    
    _description = "Composition Event"        

    composition_id = fields.Many2one(
        comodel_name="hc.res.composition", 
        string="Composition", 
        help="Composition associated with this Composition Event.")                
    code_ids = fields.Many2many(
        comodel_name="hc.vs.act.code", 
        string="Codes", 
        help="Code(s) that apply to the event being documented.")                
    start_date = fields.Datetime(
        string="Start Date", 
        help="Start of the the period covered by the documentation.")                
    end_date = fields.Datetime(
        string="End Date", 
        help="End of the the period covered by the documentation.")                
    detail_ids = fields.One2many(
        comodel_name="hc.composition.event.detail", 
        inverse_name="event_id", 
        string="Details", 
        help="Full details for the event(s) the composition consents.")                

class CompositionSection(models.Model):    
    _name = "hc.composition.section"    
    _description = "Composition Section"        

    composition_id = fields.Many2one(
        comodel_name="hc.res.composition", 
        string="Composition", 
        help="Composition associated with this Composition Section.")                
    title = fields.Char(
        string="Title", 
        help="Label for section (e.g. for ToC).")                
    code_id = fields.Many2one(
        comodel_name="hc.vs.doc.section.code", 
        string="Code", 
        help="Classification of section (recommended).")                
    text_id = fields.Many2one(
        comodel_name="hc.vs.composition.section.text", 
        string="Text", 
        help="Text summary of the section, for human interpretation.")                
    mode = fields.Selection(
        string="Mode", 
        selection=[
            ("working", "Working"), 
            ("snapshot", "Snapshot"), 
            ("changes", "Changes")], 
        help="How the entry list was prepared.")                
    ordered_by_id = fields.Many2one(
        comodel_name="hc.vs.list.order", 
        string="Ordered By", 
        help="Order of section entries.")                
    entry_ids = fields.One2many(
        comodel_name="hc.composition.section.entry", 
        inverse_name="section_id", 
        string="Entries", 
        help="A reference to data that supports this section.")                
    empty_reason_id = fields.Many2one(
        comodel_name="hc.vs.list.empty.reason", 
        string="Empty Reason", 
        help="Why the section is empty.")                
    section_id = fields.Many2one(
        comodel_name="hc.composition.section", 
        string="Section", 
        help="A nested sub-section within this section.")                

class CompositionAuthor(models.Model):    
    _name = "hc.composition.author"    
    _description = "Composition Author"        
    _inherit = ["hc.basic.association"]

    composition_id = fields.Many2one(
        comodel_name="hc.res.composition", 
        string="Composition", 
        help="Composition associated with this Composition Author.")                
    author_type = fields.Selection(
        string="Author Type", 
        selection=[
            ("practitioner", "Practitioner"),
            ("device", "Device"),
            ("patient", "Patient"),
            ("related_person", "Related Person")],
        help="Type of who and/or what authored the composition.")                
    author_name = fields.Char(
        string="Author", 
        compute="_compute_author_name", 
        store="True", 
        help="Who and/or what authored the composition.")                
    author_practitioner_id = fields.Many2one(
        comodel_name="hc.res.practitioner", 
        string="Author Practitioner", 
        help="Practitioner who and/or what authored the composition.")                
    author_device_id = fields.Many2one(
        comodel_name="hc.res.device", 
        string="Author Device", 
        help="Device who and/or what authored the composition.")                
    author_patient_id = fields.Many2one(
        comodel_name="hc.res.patient", 
        string="Author Patient", 
        help="Patient who and/or what authored the composition.")                
    author_related_person_id = fields.Many2one(
        comodel_name="hc.res.related.person", 
        string="Author Related Person", 
        help="Related Person who and/or what authored the composition.")                

class CompositionIdentifier(models.Model):    
    _name = "hc.composition.identifier"    
    _description = "Composition Identifier"        
    _inherit = ["hc.basic.association", "hc.identifier"]

class CompositionEventDetail(models.Model):    
    _name = "hc.composition.event.detail"    
    _description = "Composition Event Detail"        
    _inherit = ["hc.basic.association"]
    
    event_id = fields.Many2one(
        comodel_name="hc.composition.event", 
        string="Event", 
        help="Event associated with this Composition Event Detail.")                
    detail_type = fields.Selection(
        string="Detail Type", 
        selection=[
            ("practitioner", "Practitioner"),
            ("device", "Device"),
            ("patient", "Patient"),
            ("related_person", "Related Person")],
        help="Type of full details for the event(s) the composition consent.")                
    detail_name = fields.Char(
        string="Detail", 
        compute="_compute_detail_name", 
        store="True", 
        help="Full details for the event(s) the composition consents.")                
    detail_practitioner_id = fields.Many2one(
        comodel_name="hc.res.practitioner", 
        string="Detail Practitioner", 
        help="Practitioner full details for the event(s) the composition consents.")                
    detail_device_id = fields.Many2one(
        comodel_name="hc.res.device", 
        string="Detail Device", 
        help="Device full details for the event(s) the composition consents.")                
    detail_patient_id = fields.Many2one(
        comodel_name="hc.res.patient", 
        string="Detail Patient", 
        help="Patient full details for the event(s) the composition consents.")                
    detail_related_person_id = fields.Many2one(
        comodel_name="hc.res.related.person", 
        string="Detail Related Person", 
        help="Related Person full details for the event(s) the composition consents.")                

class CompositionSectionEntry(models.Model):    
    _name = "hc.composition.section.entry"    
    _description = "Composition Section Entry"        
    _inherit = ["hc.basic.association"]

    section_id = fields.Many2one(
        comodel_name="hc.composition.section", 
        string="Section", 
        help="Section associated with this Composition Section Entry.")                
    entry_type = fields.Selection(
        string="Entry Type", 
        selection=[
            ("encounter", "Encounter"),
            ("episode_of_care", "Episode Of Care"),
            ("observation", "Observation"),
            ("diagnostic_report", "Diagnostic Report")],
        help="Type of reference to data that supports this section.")                
    entry_name = fields.Char(
        string="Entry", 
        compute="_compute_entry_name", 
        store="True", 
        help="A reference to data that supports this section.")                
    entry_encounter_id = fields.Many2one(
        comodel_name="hc.res.encounter", 
        string="Entry Encounter", 
        help="Encounter reference to data that supports this section.")                
    entry_episode_of_care_id = fields.Many2one(
        comodel_name="hc.res.episode.of.care", 
        string="Entry Episode Of Care", 
        help="Episode Of Care reference to data that supports this section.")                
    entry_observation_id = fields.Many2one(
        comodel_name="hc.res.observation", 
        string="Entry Observation", 
        help="Observation reference to data that supports this section.")                
    entry_diagnostic_report_id = fields.Many2one(
        comodel_name="hc.res.diagnostic.report", 
        string="Entry Diagnostic Report", 
        help="Diagnostic Report reference to data that supports this section.")                

class CompositionAttestationMode(models.Model):    
    _name = "hc.vs.composition.attestation.mode"    
    _description = "Composition Attestation Mode"        
    _inherit = ["hc.value.set.contains"]

class CompositionSectionText(models.Model):    
    _name = "hc.vs.composition.section.text"    
    _description = "Composition Section Text"        
    _inherit = ["hc.value.set.contains"]

class ConfidentialClassification(models.Model):    
    _name = "hc.vs.confidential.classification"    
    _description = "Confidential Classification"        
    _inherit = ["hc.value.set.contains"]

class DocClassCode(models.Model):    
    _name = "hc.vs.doc.class.code"    
    _description = "Doc Class Code"        
    _inherit = ["hc.value.set.contains"]

class DocSectionCode(models.Model):    
    _name = "hc.vs.doc.section.code"    
    _description = "Doc Section Code"        
    _inherit = ["hc.value.set.contains"]

class DocTypeCode(models.Model):    
    _name = "hc.vs.doc.type.code"    
    _description = "Doc Type Code"        
    _inherit = ["hc.value.set.contains"]
