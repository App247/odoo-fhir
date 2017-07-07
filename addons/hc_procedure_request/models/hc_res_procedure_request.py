# -*- coding: utf-8 -*-

from openerp import models, fields, api

class ProcedureRequest(models.Model):    
    _name = "hc.res.procedure.request"    
    _description = "Procedure Request"            

    name = fields.Char(
        string="Event Name", 
        compute="_compute_name", 
        store="True", 
        help="Text representation of the procedure request event. Subject Name + Type + Ordered Date.")
    identifier_ids = fields.One2many(
        comodel_name="hc.procedure.request.identifier", 
        inverse_name="procedure_request_id", 
        string="Identifiers", 
        help="Identifier.")                    
    subject_type = fields.Selection(
        string="Subject Type", 
        required="True", 
        selection=[
            ("patient", "Patient"), 
            ("group", "Group")], 
        help="Type of who the procedure should be done to.")
    subject_name = fields.Char(
        string="Subject", 
        compute="_compute_subject_name", 
        store="True", 
        help="Who the procedure should be done to.")  
    subject_patient_id = fields.Many2one(
        comodel_name="hc.res.patient", 
        string="Subject Patient", 
        required="True", 
        help="Who the procedure should be done to.")                    
    subject_group_id = fields.Many2one(
        comodel_name="hc.res.group", 
        string="Subject Group", 
        required="True", 
        help="The reference to the group.")                    
    type_id = fields.Many2one(
        comodel_name="hc.vs.procedure.code", 
        string="Type", 
        required="True", 
        help="What procedure to perform.")                    
    body_site_ids = fields.Many2many(
        comodel_name="hc.vs.body.site", 
        string="Body Sites", 
        help="What part of body to perform on.")                    
    reason_type = fields.Selection(
        string="Reason Type", 
        selection=[
            ("code", "Code"), 
            ("Condition", "Condition")], 
        help="Type of why procedure should occur.")
    reason_name = fields.Char(
        string="Reason", 
        compute="_compute_reason_name", 
        store="True", 
        help="Why procedure should occur.")
    reason_code_id = fields.Many2one(
        comodel_name="hc.vs.procedure.reason", 
        string="Reason Code", 
        help="Code of why procedure should occur.")
    reason_condition_id = fields.Many2one(
        comodel_name="hc.res.condition", 
        string="Reason Condition", 
        help="The reference to the condition.")                    
    scheduled_type = fields.Selection(
        string="Scheduled Type", 
        selection=[
            ("date_time", "Date Time"), 
            ("period", "Period"), 
            ("timing", "Timing")], 
        help="Type of when procedure should occur.")
    scheduled_name = fields.Char(
        string="Scheduled", 
        compute="_compute_scheduled_name", 
        store="True", 
        help="When procedure should occur.")
    scheduled_date_time = fields.Datetime(
        string="Scheduled Date Time", 
        help="Date Time when procedure should occur.")            
    scheduled_start_date = fields.Datetime(
        string="Scheduled Start Date", 
        help="Start of the when procedure should occur.")
    scheduled_end_date = fields.Datetime(
        string="Scheduled End Date", 
        help="End of the when procedure should occur.")
    scheduled_timing_id = fields.Many2one(
        comodel_name="hc.procedure.request.scheduled.timing", 
        string="Scheduled Timing", 
        help="Timing when procedure should occur.")                    
    encounter_id = fields.Many2one(
        comodel_name="hc.res.encounter", 
        string="Encounter", 
        help="Encounter.")                    
    performer_type = fields.Selection(
        string="Performer Type", 
        selection=[
            ("practitioner", "Practitioner"), 
            ("organization", "Organization"), 
            ("patient", "Patient"), 
            ("related_person", "Related Person")], 
        help="Type of who should perform the procedure.")
    performer_name = fields.Char(
        string="Performer", 
        compute="_compute_performer_name", 
        store="True", 
        help="Who should perform the procedure.")
    performer_practitioner_id = fields.Many2one(
        comodel_name="hc.res.practitioner", 
        string="Performer Practitioner", 
        help="Practitioner who should perform the procedure.")                    
    performer_organization_id = fields.Many2one(
        comodel_name="hc.res.organization", 
        string="Performer Organization", 
        help="The reference to the organization.")                    
    performer_patient_id = fields.Many2one(
        comodel_name="hc.res.patient", 
        string="Performer Patient", 
        help="The reference to the patient.")                    
    performer_related_person_id = fields.Many2one(
        comodel_name="hc.res.related.person", 
        string="Performer Related Person", 
        help="The reference to the related person.")                    
    status = fields.Selection(
        string="Procedure Request Status", 
        selection=[
            ("proposed", "Proposed"), 
            ("draft", "Draft"), 
            ("requested", "Requested"), 
            ("received", "Received"), 
            ("accepted", "Accepted"), 
            ("in-progress", "In-Progress"), 
            ("completed", "Completed"), 
            ("suspended", "Suspended"), 
            ("rejected", "Rejected"), 
            ("aborted", "Aborted")], 
        help="The status of the order.")                    
    supporting_info_ids = fields.One2many(
        comodel_name="hc.procedure.request.supporting.info",
        inverse_name="procedure_request_id", 
        string="Supporting Infos", 
        help="Extra information to use in performing request.")
    notes_ids = fields.One2many(
        comodel_name="hc.procedure.request.notes", 
        inverse_name="procedure_request_id", 
        string="Notes", 
        help="Additional information about desired procedure.")                    
    as_needed_type = fields.Selection(
        string="As Needed Type", 
        selection=[
            ("boolean", "Boolean"), 
            ("code", "Code")], 
        help="Type of preconditions for procedure.")
    as_needed_name = fields.Char(
        string="As Needed", 
        compute="_compute_as_needed_name", 
        store="True", 
        help="Preconditions for procedure.")  
    is_as_needed = fields.Boolean(
        string="As Needed Boolean", 
        help="Boolean of preconditions for procedure.")                    
    as_needed_code_id = fields.Many2one(
        comodel_name="hc.vs.procedure.request.as.needed", 
        string="As Needed Code", 
        help="Code of preconditions for procedure.")                    
    ordered_on = fields.Datetime(
        string="Ordered On Date", 
        help="When Requested.")                    
    orderer_type = fields.Selection(
        string="Orderer Type", 
        selection=[
            ("practitioner", "Practitioner"), 
            ("patient", "Patient"), 
            ("related_person", "Related Person"), 
            ("device", "Device")], 
        help="Type of Ordering Party.")
    orderer_name = fields.Char(
        string="Orderer", 
        compute="_compute_orderer_name", 
        store="True", 
        help="Ordering Party.")
    orderer_practitioner_id = fields.Many2one(
        comodel_name="hc.res.practitioner", 
        string="Orderer Practitioner", 
        help="Practitioner ordering party.")                    
    orderer_patient_id = fields.Many2one(
        comodel_name="hc.res.patient", 
        string="Orderer Patient", 
        help="The reference to the patient.")                    
    orderer_related_person_id = fields.Many2one(
        comodel_name="hc.res.related.person", 
        string="Orderer Related Person", 
        help="The reference to the related person.")                    
    orderer_device_id = fields.Many2one(
        comodel_name="hc.res.device", 
        string="Orderer Device", 
        help="The reference to the device.")                    
    priority = fields.Selection(
        string="Procedure Request Priority", 
        selection=[
            ("routine", "Routine"), 
            ("urgent", "Urgent"), 
            ("stat", "Stat"), 
            ("asap", "Asap")], 
        help="The clinical priority associated with this order.")                    

    @api.multi          
    def _compute_subject_name(self):            
        for hc_res_procedure in self:       
            if hc_res_procedure.subject_type == 'patient':  
                hc_res_procedure.subject_name = hc_res_procedure.subject_patient_id.name
            elif hc_res_procedure.subject_type == 'group':  
                hc_res_procedure.subject_name = hc_res_procedure.subject_group_id.name

    @api.multi          
    def _compute_reason_name(self):         
        for hc_res_procedure in self:       
            if hc_res_procedure.reason_type == 'code':  
                hc_res_procedure.reason_name = hc_res_procedure.reason_code_id.name
            elif hc_res_procedure.reason_type == 'condition':   
                hc_res_procedure.reason_name = hc_res_procedure.reason_condition_id.name

    @api.multi          
    def _compute_scheduled_name(self):          
        for hc_procedure_used_request in self:      
            if hc_procedure_used_request.scheduled_type == 'date_time':  
                hc_procedure_used_request.scheduled_name = hc_procedure_used_request.scheduled_date_time_id.name
            elif hc_procedure_used_request.scheduled_type == 'period':  
                hc_procedure_used_request.scheduled_name = hc_procedure_used_request.scheduled_period_id.name
            elif hc_procedure_used_request.scheduled_type == 'timing':  
                hc_procedure_used_request.scheduled_name = hc_procedure_used_request.scheduled_timing_id.name

    @api.multi          
    def _compute_performer_name(self):          
        for hc_res_procedure in self:       
            if hc_res_procedure.performer_type == 'practitioner':   
                hc_res_procedure.performer_name = hc_res_procedure.performer_practitioner_id.name
            elif hc_res_procedure.performer_type == 'organization': 
                hc_res_procedure.performer_name = hc_res_procedure.performer_organization_id.name
            elif hc_res_procedure.performer_type == 'patient':  
                hc_res_procedure.performer_name = hc_res_procedure.performer_patient_id.name
            elif hc_res_procedure.performer_type == 'related_person':   
                hc_res_procedure.performer_name = hc_res_procedure.performer_related_person_id.name

    @api.multi          
    def _compute_as_needed_name(self):          
        for hc_res_procedure in self:       
            if hc_res_procedure.as_needed_type == 'boolean':    
                hc_res_procedure.as_needed_name = hc_res_procedure.as_needed_boolean_id.name
            elif hc_res_procedure.as_needed_type == 'code': 
                hc_res_procedure.as_needed_name = hc_res_procedure.as_needed_code_id.name

    @api.multi          
    def _compute_orderer_name(self):            
        for hc_res_procedure in self:       
            if hc_res_procedure.orderer_type == 'practitioner': 
                hc_res_procedure.orderer_name = hc_res_procedure.orderer_practitioner_id.name
            elif hc_res_procedure.orderer_type == 'patient':    
                hc_res_procedure.orderer_name = hc_res_procedure.orderer_patient_id.name
            elif hc_res_procedure.orderer_type == 'related_person': 
                hc_res_procedure.orderer_name = hc_res_procedure.orderer_related_person_id.name
            elif hc_res_procedure.orderer_type == 'device': 
                hc_res_procedure.orderer_name = hc_res_procedure.orderer_device_id.name                    

class ProcedureRequestIdentifier(models.Model):    
    _name = "hc.procedure.request.identifier"    
    _description = "Procedure Request Identifier"        
    _inherit = ["hc.basic.association", "hc.identifier"]    

    procedure_request_id = fields.Many2one(
        comodel_name="hc.res.procedure.request", 
        string="Procedure Request", 
        help="Procedure Request associated with this Procedure Request Identifier.")                    

class ProcedureRequestNotes(models.Model):    
    _name = "hc.procedure.request.notes"    
    _description = "Procedure Request Notes"        
    _inherit = ["hc.basic.association", "hc.annotation"]    

    procedure_request_id = fields.Many2one(
        comodel_name="hc.res.procedure.request", 
        string="Procedure Request", 
        help="Procedure Request associated with this Procedure Request Note.")                    

class ProcedureRequestScheduledTiming(models.Model):    
    _name = "hc.procedure.request.scheduled.timing"    
    _description = "Procedure Request Scheduled Timing"        
    _inherit = ["hc.basic.association", "hc.timing"]    

class ProcedureRequestSupportingInfo(models.Model):
    _name = "hc.procedure.request.supporting.info"  
    _description = "Procedure Request Supporting Info"     
    _inherit = ["hc.basic.association"]

    procedure_request_id = fields.Many2one(
        comodel_name="hc.res.procedure.request", 
        string="Procedure Request", 
        help="Procedure Request associated with this Procedure Request Supporting Info.")
    supporting_info_type = fields.Selection(
        string="Supporting Info Type", 
        selection=[
            ("string", "String"), 
            ("code", "Code")], 
        help="Type of extra information to use in performing request.")
    supporting_info_name = fields.Char(
        string="Supporting Info", 
        compute="_compute_supporting_info_name", 
        store="True", 
        help="Extra information to use in performing request.")
    supporting_info_string = fields.Char(
        string="Supporting Info String", 
        help="Extra information to use in performing request.")
    supporting_info_code_id = fields.Many2one(
        comodel_name="hc.vs.resource.type", 
        string="Supporting Info Code", 
        help="Type of extra information to use in performing request.")
    
class ProcedureCode(models.Model):  
    _name = "hc.vs.procedure.code"  
    _description = "Procedure Code"     
    _inherit = ["hc.value.set.contains"]

class ProcedureReasonCode(models.Model):    
    _name = "hc.vs.procedure.reason"   
    _description = "Procedure Reason"      
    _inherit = ["hc.value.set.contains"] 

class ProcedureRequestAsNeeded(models.Model):    
    _name = "hc.vs.procedure.request.as.needed"    
    _description = "Procedure Request As Needed"        
    _inherit = ["hc.value.set.contains"]

# External Reference

class EncounterIncomingReferral(models.Model):
    _inherit = "hc.encounter.incoming.referral"

    incoming_referral_id = fields.Many2one(
        comodel_name="hc.res.procedure.request",
        string="Incoming Referral",
        help="Procedure Request associated with this Encounter Incoming Referral.")
