# -*- coding: utf-8 -*-

from openerp import models, fields, api

class DiagnosticRequest(models.Model):    
    _name = "hc.res.diagnostic.request"    
    _description = "Diagnostic Request"

    name = fields.Char(
        string="Event Name", 
        required="True", 
        help="Name for this diagnostic request. Subject Name + Code + Occurrence.")
    identifier_ids = fields.One2many(
        comodel_name="hc.diagnostic.request.identifier", 
        inverse_name="diagnostic_request_id", 
        string="Identifiers", 
        help="Identifiers assigned to this order.")                    
    definition_ids = fields.One2many(
        comodel_name="hc.diagnostic.request.definition", 
        inverse_name="diagnostic_request_id", 
        string="Definitions", 
        help="Protocol or definition.")                    
    based_on_ids = fields.One2many(
        comodel_name="hc.diagnostic.request.based.on", 
        inverse_name="diagnostic_request_id", 
        string="Based On", 
        help="What request fulfills.")                    
    replaces_ids = fields.One2many(
        comodel_name="hc.diagnostic.request.replaces", 
        inverse_name="diagnostic_request_id", 
        string="Replaces", 
        help="What request replaces.")                    
    requisition_id = fields.Many2one(
        comodel_name="hc.diagnostic.request.requisition", 
        string="Requisition Identifier", 
        help="Identifier of composite request.")                    
    status = fields.Selection(
        string="Diagnostic Request Status", 
        selection=[
            ("requested", "Requested"), 
            ("received", "Received"), 
            ("accepted", "Accepted"), 
            ("in progress", "In Progress"), 
            ("review", "Review"), 
            ("completed", "Completed"), 
            ("suspended", "Suspended"), 
            ("rejected", "Rejected"), 
            ("failed", "Failed")], 
        help="The status of the order.")                    
    stage_id = fields.Many2one(
        comodel_name="hc.vs.diagnostic.request.stage", 
        string="Diagnostic Request Stage", 
        required="True", 
        help="Whether the request is a proposal, plan, an original order or a reflex order.")
    # stage = fields.Selection(
    #     string="Diagnostic Request Stage", 
    #     required="True", 
    #     selection=[("proposal", "Proposal"), ("plan", "Plan"), ("original-order", "Original-Order"), ("reflex-order", "Reflex-Order")], 
    #     help="Whether the request is a proposal, plan, an original order or a reflex order.")                    
    intent = fields.Selection(
        string="Intent", 
        required="True", 
        selection=[
            ("logic-library", "Logic Library"), 
            ("model-definition", "Model Definition"), 
            ("asset-collection", "Asset Collection"), 
            ("module-definition", "Module Definition")], 
        help="Identifies the type of library such as a Logic Library, Model Definition, Asset Collection, or Module Definition.")
    priority = fields.Selection(
        string="Priority",
        selection=[
            ("routine", "Routine"), 
            ("urgent", "Urgent"), 
            ("asap", "Asap"), 
            ("stat", "Stat")],
        help="Indicates how quickly the title should be addressed with respect to other requests.")
    code_id = fields.Many2one(
        comodel_name="hc.vs.diagnostic.request", 
        string="Code", 
        required="True", 
        help="What's being requested/ordered.")                    
    subject_type = fields.Selection(
        string="Subject Type", 
        required="True", 
        selection=[
            ("patient", "Patient"), 
            ("group", "Group"), 
            ("location", "Location"), 
            ("device", "Device")], 
        help="Type of who and/or what test is about.")                    
    subject_name = fields.Char(
        string="Subject", 
        compute="compute_subject_name", 
        help="Who and/or what test is about.")                    
    subject_patient_id = fields.Many2one(
        comodel_name="hc.res.patient", 
        string="Subject Patient", 
        help="Patient who and/or what test is about.")
    subject_group_id = fields.Many2one(
        comodel_name="hc.res.group", 
        string="Subject Group", 
        help="Group who and/or what test is about.")
    subject_location_id = fields.Many2one(
        comodel_name="hc.res.location", 
        string="Subject Location", 
        help="Location who and/or what test is about.")
    subject_device_id = fields.Many2one(
        comodel_name="hc.res.device", 
        string="Subject Device", 
        help="Device who and/or what test is about.")                  
    context_type = fields.Selection(
        string="Context Type", 
        selection=[
            ("Encounter", "Encounter"), 
            ("Episode Of Care", "Episode of Care")], 
        help="Encounter or Episode during which request was created.")                    
    context_name = fields.Char(
        string="Context", 
        compute="compute_context_name", 
        help="Encounter or Episode during which request was created.")
    context_encounter_id = fields.Many2one(
        comodel_name="hc.res.encounter", 
        string="Context Encounter", 
        help="Encounter during which request was created.")                    
    context_episode_of_care_id = fields.Many2one(
        comodel_name="hc.res.episode.of.care", 
        string="Context Episode Of Care", 
        help="Episode Of Care during which request was created.")                                       
    occurence_type = fields.Selection(
        string="Occurence Type", 
        selection=[
            ("datetime", "Datetime"), 
            ("period", "Period"), 
            ("timing", "Timing")], 
        help="Type of when testing should occur.")                    
    occurrence_name = fields.Char(
        string="Occurrence", 
        compute="compute_occurrence_name", 
        help="When testing should occur.")             
    occurrence_datetime = fields.Datetime(
        string="Occurrence Datetime", 
        help="dateTime when testing should occur.")                    
    occurence_start_date = fields.Datetime(
        string="Occurrence Start Date", 
        help="Start of the when testing should occur.")                    
    occurence_end_date = fields.Datetime(
        string="Occurence End Date", 
        help="End of the when testing should occur.")                    
    occurrence_timing_id = fields.Many2one(
        comodel_name="hc.diagnostic.request.occurrence.timing", 
        string="Occurrence Timing", 
        help="Timing when testing should occur.")             
    authored_on = fields.Datetime(
        tring="Authored On", 
        help="Date request signed.")                   
    requester_type = fields.Selection(
        string="Requester Type", 
        selection=[
            ("device", "Device"), 
            ("practitioner", "Practitioner"), 
            ("organization", "Organization")], 
        help="Type of who/what is requesting diagnostics.")                    
    requester_name = fields.Char(
        string="Requester", 
        compute="compute_requester_name", 
        help="Who/what is requesting diagnostics.")                    
    requester_device_id = fields.Many2one(
        comodel_name="hc.res.device", 
        string="Requester Device", 
        help="Device who/what is requesting diagnostics.")
    requester_practitioner_id = fields.Many2one(
        comodel_name="hc.res.practitioner", 
        string="Requester Practitioner", 
        help="Practitioner who/what is requesting diagnostics.")                    
    requester_organization_id = fields.Many2one(
        comodel_name="hc.res.organization", 
        string="Requester Organization", 
        help="Organization who/what is requesting diagnostics.")                     
    performer_type_id = fields.Many2one(
        comodel_name="hc.vs.participant.role", 
        string="Performer Type", 
        help="Performer role.")                    
    requested_performer_type = fields.Selection(
        string="Requested Performer Type", 
        selection=[
            ("Practitioner", "Practitioner"), 
            ("Organization", "Organization"), 
            ("Patient", "Patient"), 
            ("Device", "Device"), 
            ("Related Person", "Related Person")], 
        help="Type of requested perfomer.")
    requested_performer_name = fields.Char(
        string="Requested Performer", 
        compute="_compute_requested_performer_name", 
        store="True", 
        help="Requested perfomer.")
    requested_performer_practitioner_id = fields.Many2one(
        comodel_name="hc.res.practitioner", 
        string="Requested Performer Practitioner", 
        help="Practitioner requested perfomer.")
    requested_performer_organization_id = fields.Many2one(
        comodel_name="hc.res.organization", 
        string="Requested Performer Organization", 
        help="Organization requested perfomer.")
    requested_performer_patient_id = fields.Many2one(
        comodel_name="hc.res.patient", 
        string="Requested Performer Patient", 
        help="Patient requested perfomer.")
    requested_performer_device_id = fields.Many2one(
        comodel_name="hc.res.device", 
        string="Requested Performer Device", 
        help="Device requested perfomer.")
    requested_performer_related_person_id = fields.Many2one(
        comodel_name="hc.res.related.person", 
        string="Requested Performer Related Person", 
        help="Related Person requested perfomer.")
    reason_code_ids = fields.Many2many(
        comodel_name="hc.vs.condition.code", 
        relation="diagnostic_request_reason_code_rel", 
        string="Reason Codes", 
        help="Explanation/Justification for test.")
    supporting_info_ids = fields.One2many(
        comodel_name="hc.diagnostic.request.supporting.info", 
        inverse_name="diagnostic_request_id", 
        string="Supporting Info", 
        help="Additional clinical information.")     
    note_ids = fields.One2many(
        comodel_name="hc.diagnostic.request.note", 
        inverse_name="diagnostic_request_id", 
        string="Notes", 
        help="Comments.")                    
    relevant_history_ids = fields.One2many(
        comodel_name="hc.diagnostic.request.relevant.history", 
        inverse_name="diagnostic_request_id", 
        string="Relevant Histories", 
        help="Request provenance.")                    

    @api.depends('subject_type')            
    def _compute_subject_name(self):            
        for hc_res_diagnostic_request in self:      
            if hc_res_diagnostic_request.subject_type == 'patient': 
                hc_res_diagnostic_request.subject_name = hc_res_diagnostic_request.subject_patient_id.name
            elif hc_res_diagnostic_request.subject_type == 'group': 
                hc_res_diagnostic_request.subject_name = hc_res_diagnostic_request.subject_group_id.name
            elif hc_res_diagnostic_request.subject_type == 'location':  
                hc_res_diagnostic_request.subject_name = hc_res_diagnostic_request.subject_location_id.name
            elif hc_res_diagnostic_request.subject_type == 'device':    
                hc_res_diagnostic_request.subject_name = hc_res_diagnostic_request.subject_device_id.name

    @api.depends('context_type')            
    def _compute_context_name(self):            
        for hc_res_diagnostic_request in self:      
            if hc_res_diagnostic_request.context_type == 'encounter':   
                hc_res_diagnostic_request.context_name = hc_res_diagnostic_request.context_encounter_id.name
            elif hc_res_diagnostic_request.context_type == 'episode_of_care':   
                hc_res_diagnostic_request.context_name = hc_res_diagnostic_request.context_episode_of_care_id.name

    @api.depends('occurrence_type')         
    def _compute_occurrence_name(self):         
        for hc_res_diagnostic_report in self:       
            if hc_res_diagnostic_report.occurrence_type == 'datetime':  
                hc_res_diagnostic_report.occurrence_name = str(hc_res_diagnostic_report.occurrence_datetime)
            elif hc_res_diagnostic_report.occurrence_type == 'period':  
                hc_res_diagnostic_report.occurrence_name = 'Between' + str(hc_res_diagnostic_report.occurrence_start_date) + ' and ' + str(hc_res_diagnostic_report.occurrence_end_date)
            elif hc_res_diagnostic_report.occurrence_type == 'timing':  
                hc_res_diagnostic_report.occurrence_name = hc_res_diagnostic_report.occurrence_timing_id.name

    @api.depends('requester_type')          
    def _compute_requester_name(self):          
        for hc_res_diagnostic_request in self:      
            if hc_res_diagnostic_request.requester_type == 'device':    
                hc_res_diagnostic_request.requester_name = hc_res_diagnostic_request.requester_device_id.name
            elif hc_res_diagnostic_request.requester_type == 'practitioner':    
                hc_res_diagnostic_request.requester_name = hc_res_diagnostic_request.requester_practitioner_id.name
            elif hc_res_diagnostic_request.requester_type == 'organization':    
                hc_res_diagnostic_request.requester_name = hc_res_diagnostic_request.requester_organization_id.name

    @api.depends('requested_performer_type')            
    def _compute_requested_performer_name(self):            
        for hc_res_diagnostic_request in self:      
            if hc_res_diagnostic_request.requested_performer_type == 'practitioner':    
                hc_res_diagnostic_request.requested_performer_name = hc_res_diagnostic_request.requested_performer_practitioner_id.name
            elif hc_res_diagnostic_request.requested_performer_type == 'organization':  
                hc_res_diagnostic_request.requested_performer_name = hc_res_diagnostic_request.requested_performer_organization_id.name
            elif hc_res_diagnostic_request.requested_performer_type == 'patient':   
                hc_res_diagnostic_request.requested_performer_name = hc_res_diagnostic_request.requested_performer_patient_id.name
            elif hc_res_diagnostic_request.requested_performer_type == 'device':    
                hc_res_diagnostic_request.requested_performer_name = hc_res_diagnostic_request.requested_performer_device_id.name
            elif hc_res_diagnostic_request.requested_performer_type == 'related_person':    
                hc_res_diagnostic_request.requested_performer_name = hc_res_diagnostic_request.requested_performer_related_person_id.name

class DiagnosticRequestIdentifier(models.Model):    
    _name = "hc.diagnostic.request.identifier"    
    _description = "Diagnostic Request Identifier"        
    _inherit = ["hc.basic.association", "hc.identifier"]    

    diagnostic_request_id = fields.Many2one(
        comodel_name="hc.res.diagnostic.request", 
        string="Diagnostic Request", 
        help="Diagnostic Request associated with this Diagnostic Request Identifier.")                    

class DiagnosticRequestRequisition(models.Model): 
    _name = "hc.diagnostic.request.requisition"  
    _description = "Diagnostic Request Requisition"      
    _inherit = ["hc.basic.association", "hc.identifier"]

    diagnostic_request_id = fields.Many2one(
        comodel_name="hc.res.diagnostic.request", 
        string="Diagnostic Request", 
        help="Diagnostic Request associated with this Diagnostic Request Requisition." )              

class DiagnosticRequestBasedOn(models.Model):    
    _name = "hc.diagnostic.request.based.on"    
    _description = "Diagnostic Request Based On"        
    _inherit = ["hc.basic.association"]    
    
    diagnostic_request_id = fields.Many2one(
        comodel_name="hc.res.diagnostic.request", 
        string="Diagnostic Request", 
        help="Diagnostic Request associated with this Diagnostic Request Based On.")                    
    based_on_type = fields.Char(
        string="Based On Type", 
        compute="_compute_based_on_type", 
        store="True", 
        help="Type of what request fulfills.")
    based_on_name = fields.Reference(
        string="Based On", 
        selection="_reference_models", 
        help="What request fulfills.")

    @api.model          
    def _reference_models(self):            
        models = self.env['ir.model'].search([('state', '!=', 'manual')])       
        return [(model.model, model.name)       
            for model in models 
                if model.model.startswith('hc.res')]
                
    @api.depends('based_on_name')           
    def _compute_based_on_type(self):           
        for this in self:       
            if this.based_on_name:  
                this.based_on_type = this.based_on_name._description

class DiagnosticRequestDefinition(models.Model):    
    _name = "hc.diagnostic.request.definition"    
    _description = "Diagnostic Request Definition"        
    _inherit = ["hc.basic.association"]    
    
    diagnostic_request_id = fields.Many2one(
        comodel_name="hc.res.diagnostic.request", 
        string="Diagnostic Request", 
        help="Diagnostic Request associated with this Diagnostic Request Definition.")                    
    definition_type = fields.Char(
        string="Definition Type", 
        compute="_compute_definition_type", 
        store="True", 
        help="Type of protocol or definition.")
    definition_name = fields.Reference(
        string="Definition", 
        selection="_reference_models", 
        help="Protocol or definition.")

    @api.model          
    def _reference_models(self):            
        models = self.env['ir.model'].search([('state', '!=', 'manual')])       
        return [(model.model, model.name)       
            for model in models 
                if model.model.startswith('hc.res')]
                
    @api.depends('definition_name')         
    def _compute_definition_type(self):         
        for this in self:       
            if this.definition_name:    
                this.definition_type = this.definition_name._description
                
class DiagnosticRequestNote(models.Model):    
    _name = "hc.diagnostic.request.note"    
    _description = "Diagnostic Request Note"        
    _inherit = ["hc.basic.association", "hc.annotation"]    
    
    diagnostic_request_id = fields.Many2one(
        comodel_name="hc.res.diagnostic.request", 
        string="Diagnostic Request", 
        help="Diagnostic Request associated with this Diagnostic Request Note.")                    

class DiagnosticRequestRelevantHistory(models.Model):    
    _name = "hc.diagnostic.request.relevant.history"   
    _description = "Diagnostic Request Relevant History"        
    _inherit = ["hc.basic.association"]    
    
    diagnostic_request_id = fields.Many2one(
        comodel_name="hc.res.diagnostic.request", 
        string="Diagnostic Request", 
        help="Diagnostic Request associated with this Diagnostic Request Relevant History.")                    
    relevant_history_id = fields.Many2one(
        comodel_name="hc.res.provenance", 
        string="Relevant History", 
        help="Provenance associated with this Diagnostic Request Relevant History.")                    

class DiagnosticRequestReplaces(models.Model):    
    _name = "hc.diagnostic.request.replaces"    
    _description = "Diagnostic Request Replaces"        
    _inherit = ["hc.basic.association"]

    diagnostic_request_id = fields.Many2one(
        comodel_name="hc.res.diagnostic.request", 
        string="Diagnostic Request", 
        help="Diagnostic Request associated with this Diagnostic Request Replaces.")                    
    replaces_type = fields.Char(
        string="Replaces Type", 
        compute="_compute_replaces_type", 
        store="True", 
        help="Type of what request replaces.")
    replaces_name = fields.Reference(
        string="Replaces", 
        selection="_reference_models", 
        help="What request replaces.")

    @api.model          
    def _reference_models(self):            
        models = self.env['ir.model'].search([('state', '!=', 'manual')])       
        return [(model.model, model.name)       
            for model in models 
                if model.model.startswith('hc.res')]
                
    @api.depends('replaces_name')           
    def _compute_replaces_type(self):           
        for this in self:       
            if this.replaces_name:  
                this.replaces_type = this.replaces_name._description
                   
class DiagnosticRequestSupportingInfo(models.Model):    
    _name = "hc.diagnostic.request.supporting.info"    
    _description = "Diagnostic Request Supporting Information"        
    _inherit = ["hc.basic.association"]    

    diagnostic_request_id = fields.Many2one(
        comodel_name="hc.res.diagnostic.request", 
        string="Diagnostic Request", 
        help="Diagnostic Request associated with this Diagnostic Request Supporting Information.")                    
    supporting_info_type = fields.Char(
        string="Supporting Info Type", 
        compute="_compute_supporting_info_type", 
        store="True", 
        help="Type of additional clinical information.")
    supporting_info_name = fields.Reference(
        string="Supporting Info", 
        selection="_reference_models", 
        help="Additional clinical information.")

    @api.model          
    def _reference_models(self):            
        models = self.env['ir.model'].search([('state', '!=', 'manual')])       
        return [(model.model, model.name)       
            for model in models 
                if model.model.startswith('hc.res')]
                
    @api.depends('supporting_info_name')            
    def _compute_supporting_info_type(self):            
        for this in self:       
            if this.supporting_info_name:   
                this.supporting_info_type = this.supporting_info_name._description
                
class DiagnosticRequestOccurrenceTiming(models.Model):  
    _name = "hc.diagnostic.request.occurrence.timing"    
    _description = "Diagnostic Request Occurrence Timing"       
    _inherit = ["hc.basic.association", "hc.timing"]

class DiagnosticRequest(models.Model):    
    _name = "hc.vs.diagnostic.request"    
    _description = "Diagnostic Request"        
    _inherit = ["hc.value.set.contains"]      

class DiagnosticRequestStage(models.Model): 
    _name = "hc.vs.diagnostic.request.stage"    
    _description = "Diagnostic Request Stage"       
    _inherit = ["hc.value.set.contains"]

# External Reference

# class Procedure(models.Model):  
#     _inherit = "hc.res.procedure"

#     request_diagnostic_request_id = fields.Many2one(
#         comodel_name="hc.res.diagnostic.request", 
#         string="Request Diagnostic Request", 
#         help="Diagnostic Request for this procedure.")

# class SpecimenRequest(models.Model):    
#     _inherit = "hc.specimen.request"
    
#     request_diagnostic_request_id = fields.Many2one(
#         comodel_name="hc.res.diagnostic.request", 
#         string="Request Diagnostic Request", 
#         help="Diagnostic Request why the specimen was collected.")
