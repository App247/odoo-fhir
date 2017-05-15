# -*- coding: utf-8 -*-

from openerp import models, fields, api

class CommunicationRequest(models.Model):    
    _name = "hc.res.communication.request"    
    _description = "Communication Request"        

    name = fields.Char(
        string="Name", 
        compute="_compute_name", 
        store="True", 
        help="Text representation of the communication request event. Sender Name + Communication Request Category + Ordered Date.")
    identifier_ids = fields.One2many(
        comodel_name="hc.communication.request.identifier", 
        inverse_name="communication_request_id", 
        string="Identifiers", 
        help="Unique identifier.")                
    category_id = fields.Many2one(
        comodel_name="hc.vs.communication.request.category", 
        string="Category", help="Message category.")                
    sender_type = fields.Selection(string="Sender Type", 
        selection=[
            ("Device", "Device"), 
            ("Organization", "Organization"), 
            ("Patient", "Patient"), 
            ("Practitioner", "Practitioner"), 
            ("Related Person", "Related Person")], 
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
    sender_organization_id = fields.Many2one(comodel_name="hc.res.organization", string="Sender Organization", help="Organization message sender.")                
    sender_patient_id = fields.Many2one(comodel_name="hc.res.patient", string="Sender Patient", help="Patient message sender.")                
    sender_practitioner_id = fields.Many2one(comodel_name="hc.res.practitioner", string="Sender Practitioner", help="Practitioner message sender.")                
    sender_related_person_id = fields.Many2one(comodel_name="hc.res.related.person", string="Sender Related Person", help="Related Person message sender.")                
    recipient_ids = fields.One2many(comodel_name="hc.communication.request.recipient", inverse_name="communication_request_id", string="Recipients", help="Message recipient.")                
    medium_ids = fields.Many2many(comodel_name="hc.vs.participation.mode", string="Mediums", help="Communication medium.")               
    requester_type = fields.Selection(
        string="Requester Type", 
        selection=[
            ("Practitioner", "Practitioner"), 
            ("Patient", "Patient"), 
            ("Related Person", "Related Person")], 
        help="Type of message recipient.")                
    requester_name = fields.Char(string="Requester", compute="_compute_requester_name", store="True", help="An individual who requested a communication.")                
    requester_practitioner_id = fields.Many2one(comodel_name="hc.res.practitioner", string="Requester Practitioner", help="Practitioner who requested a communication.")                
    requester_patient_id = fields.Many2one(comodel_name="hc.res.patient", string="Requester Patient", help="Patient who requested a communication.")                
    requester_related_person_id = fields.Many2one(comodel_name="hc.res.related.person", string="Requester Related Person", help="Related Person who requested a communication.")                
    status = fields.Selection(string="Communication Request Status", selection=[("proposed", "Proposed"), ("planned", "Planned"), ("requested", "Requested"), ("received", "Received"), ("accepted", "Accepted"), ("in-progress", "In-Progress"), ("completed", "Completed"), ("suspended", "Suspended"), ("rejected", "Rejected") ], help="The status of the proposal or order.")                
    encounter_id = fields.Many2one(comodel_name="hc.res.encounter", string="Encounter", help="Encounter leading to message.")                
    scheduled_type = fields.Selection(
        string="Scheduled Type", 
        selection=[
            ("date_time", "Date Time"), 
            ("Period", "Period")], 
        help="Type of when scheduled.")                
    scheduled_name = fields.Char(
        string="Scheduled", 
        compute="_compute_scheduled_name", 
        store="True", 
        help="When scheduled.")                
    scheduled_date_time = fields.Datetime(
        string="Scheduled Date Time", 
        help="dateTime when scheduled.")                
    scheduled_start_date = fields.Datetime(
        string="Scheduled Start Date", 
        help="Start of the when scheduled.")                
    scheduled_end_date = fields.Datetime(
        string="Scheduled End Date", 
        help="End of the when scheduled.")                
    reason_ids = fields.Many2many(
        comodel_name="hc.vs.act.reason", 
        string="Reasons", 
        help="Indication for message.")               
    ordered_on = fields.Datetime(
        string="Ordered On Date", 
        help="When ordered or proposed.")                
    subject_id = fields.Many2one(
        comodel_name="hc.res.patient", 
        string="Subject", 
        help="Focus of message.")                
    priority_id = fields.Many2one(
        comodel_name="hc.vs.request.priority", 
        string="Priority", 
        help="Message urgency.")                
    payload_ids = fields.One2many(
        comodel_name="hc.communication.request.payload", 
        inverse_name="communication_request_id", 
        string="Payloads", help="Message payload.")                

class CommunicationRequestPayload(models.Model):    
    _name = "hc.communication.request.payload"    
    _description = "Communication Request Payload"        

    communication_request_id = fields.Many2one(
        comodel_name="hc.res.communication.request", 
        string="Communication Request", 
        help="Communication Request associated with this Communication Request Payload.")                
    content_type = fields.Selection(
        string="Content Type", 
        required="True", 
        selection=[
            ("string", "String"), 
            ("attachment", "Attachment"), 
            ("code", "Code"), 
            ("communication_request", "Communication Request")], 
        help="Type of message part content.")                
    content_name = fields.Char(
        string="Content", 
        compute="_compute_content_name", 
        store="True", 
        help="Message part content.")                
    content_string = fields.Char(
        string="Content", 
        help="String of message part content.")                
    content_attachment_id = fields.Many2one(
        comodel_name="hc.communication.request.payload.content.attachment", 
        string="Content Attachment", 
        help="Attachment message part content.")                
    content_code_id = fields.Many2one(
        comodel_name="hc.vs.communication.content.code", 
        string="Content Code", help="Code of message part content.")                
    content_communication_request_id = fields.Many2one(
        comodel_name="hc.res.communication.request", 
        string="Content Communication Request", 
        help="Communication Request message part content.")                

class CommunicationRequestIdentifier(models.Model):    
    _name = "hc.communication.request.identifier"    
    _description = "Communication Request identifier"        
    _inherit = ["hc.basic.association", "hc.identifier"]

    communication_request_id = fields.Many2one(
        comodel_name="hc.res.communication.request", 
        string="Communication Request", 
        help="Communication Request associated with this Communication Request Identifier.")                

class CommunicationRequestRecipient(models.Model):   
    _name = "hc.communication.request.recipient"    
    _description = "Communication Request Recipient"
    _inherit = ["hc.basic.association"]    

    communication_request_id = fields.Many2one(
        comodel_name="hc.res.communication.request", 
        string="Communication Request", 
        help="Communication Request associated with this Communication Request Recipient.")                
    recipient_type = fields.Selection(
        string="Recipient Type", 
        selection=[
            ("Device", "Device"), 
            ("Organization", "Organization"), 
            ("Patient", "Patient"), 
            ("Practitioner", "Practitioner"), 
            ("Related Person", "Related Person"), 
            ("Group", "Group"), 
            ("Care Team", "Care Team")], 
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
    recipient_care_team_id = fields.Many2one(
        comodel_name="hc.res.care.team", 
        string="Recipient Care Team", 
        help="Care Team message recipient.")                              

class CommunicationRequestPayloadContentAttachment(models.Model):    
    _name = "hc.communication.request.payload.content.attachment"    
    _description = "Communication Request Payload Content Attachment"        
    _inherit = ["hc.basic.association", "hc.attachment"]

class CommunicationContentCode(models.Model):    
    _name = "hc.vs.communication.content.code"    
    _description = "Communication Content Code"        
    _inherit = ["hc.value.set.contains"]

class CommunicationRequestCategory(models.Model):    
    _name = "hc.vs.communication.request.category"    
    _description = "Communication Request Category"        
    _inherit = ["hc.value.set.contains"]

class ParticipationMode(models.Model):    
    _name = "hc.vs.participation.mode"    
    _description = "Participation Mode"        
    _inherit = ["hc.value.set.contains"]