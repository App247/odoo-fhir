# -*- coding: utf-8 -*-

from openerp import models, fields, api
from datetime import datetime
from openerp.tools import DEFAULT_SERVER_DATETIME_FORMAT as DTF

class ProcessResponse(models.Model):    
    _name = "hc.res.process.response"    
    _description = "Process Response"            

    identifier_ids = fields.One2many(
        comodel_name="hc.process.response.identifier", 
        inverse_name="process_response_id", 
        string="Identifiers", 
        help="Business Identifier.")                    
    status_id = fields.Many2one(
        comodel_name="hc.vs.fm.status", 
        string="Status", 
        help="The status of the resource instance.")                   
    status_history_ids = fields.One2many(       
        comodel_name="hc.process.response.status.history",  
        inverse_name="process_response_id", 
        string="Status History",    
        help="The status of the process response over time.")   
    created = fields.Datetime(
        string="Creation Date", 
        help="Creation date.")                    
    organization_id = fields.Many2one(
        comodel_name="hc.res.organization", 
        string="Organization", 
        help="Authoring Organization.")                    
    request_type = fields.Selection(
        string="Request Type", 
        selection=[
            ("string", "String"), 
            ("code", "Code")], 
        help="Type of request reference.")                    
    request_name = fields.Char(
        string="Request", 
        compute="_compute_request_name", 
        store="True", 
        help="Request reference.")                    
    request_string = fields.Char(
        string="Request String", 
        help="String of request reference.")                    
    request_code_id = fields.Many2one(
        comodel_name="hc.vs.resource.type", 
        string="Request Code", 
        help="Code request reference.")                    
    outcome_id = fields.Many2one(
        comodel_name="hc.vs.process.outcome", 
        string="Outcome", 
        help="Processing outcome.")                    
    disposition = fields.Char(
        string="Disposition", 
        help="Disposition Message.")                    
    request_provider_id = fields.Many2one(
        comodel_name="hc.res.practitioner", 
        string="Request Provider", 
        help="Responsible Practitioner.")                    
    request_organization_id = fields.Many2one(
        comodel_name="hc.res.organization", 
        string="Request Organization", 
        help="Responsible organization.")                    
    form_id = fields.Many2one(
        comodel_name="hc.vs.forms", 
        string="Form", 
        help="Printed Form Identifier.")                    
    error_ids = fields.Many2many(
        comodel_name="hc.vs.adjudication.error", 
        relation="process_response_error_rel", 
        string="Errors", 
        help="Error code.")                    
    communication_request_ids = fields.One2many(
        comodel_name="hc.process.response.communication.request", 
        inverse_name="process_response_id", 
        string="Communication Requests", 
        help="Request for additional information.")                    
    process_note_ids = fields.One2many(
        comodel_name="hc.process.response.process.note", 
        inverse_name="process_response_id", 
        string="Process Notes", 
        help="Processing comments or additional requirements.")                    

    @api.model                          
    def create(self, vals):                         
        status_history_obj = self.env['hc.process.response.status.history']                     
        res = super(ProcessResponse, self).create(vals)                     
        if vals and vals.get('status_id'):                      
            status_history_vals = {                 
                'process_response_id': res.id,              
                'status': res.status_id.name,              
                'start_date': datetime.today()              
                }               
            if vals.get('status_id') == 'entered-in-error':                 
                status_history_vals.update({'end_date': datetime.today()})              
            status_history_obj.create(status_history_vals)                  
        return res                      
                                
    @api.multi                          
    def write(self, vals):                          
        status_history_obj = self.env['hc.process.response.status.history']                     
        fm_status_obj = self.env['hc.vs.fm.status']                     
        res = super(ProcessResponse, self).write(vals)                      
        status_history_record_ids = status_history_obj.search([('end_date','=', False)])                        
        if status_history_record_ids:                       
            if vals.get('status_id') and status_history_record_ids[0].status != vals.get('status_id'):                  
                for status_history in status_history_record_ids:                
                    status_history.end_date = datetime.strftime(datetime.today(), DTF)          
                    time_diff = datetime.today() - datetime.strptime(status_history.start_date, DTF)            
                    if time_diff:           
                        days = str(time_diff).split(',')        
                        if days and len(days) > 1:      
                            status_history.time_diff_day = str(days[0]) 
                            times = str(days[1]).split(':') 
                            if times and times > 1: 
                                status_history.time_diff_hour = str(times[0])
                                status_history.time_diff_min = str(times[1])
                                status_history.time_diff_sec = str(times[2])
                        else:       
                            times = str(time_diff).split(':')   
                            if times and times > 1: 
                                status_history.time_diff_hour = str(times[0])
                                status_history.time_diff_min = str(times[1])
                                status_history.time_diff_sec = str(times[2])
                fm_status = fm_status_obj.browse(vals.get('status_id'))             
                status_history_vals = {             
                    'process_response_id': self.id,         
                    'status': fm_status.name,           
                    'start_date': datetime.today()          
                    }           
                if vals.get('status_id') == 'entered-in-error':             
                    status_id_history_vals.update({'end_date': datetime.today()})           
                status_history_obj.create(status_history_vals)              
        return res                      

class ProcessResponseProcessNote(models.Model):    
    _name = "hc.process.response.process.note"    
    _description = "Process Response Process Note"            

    process_response_id = fields.Many2one(
        comodel_name="hc.res.process.response", 
        string="Process Response", 
        help="Process Response associated with this Process Response Process Note.")                    
    type = fields.Selection(
        string="Type", 
        selection=[
            ("display", "Display"), 
            ("print", "Print"), 
            ("printoper", "Printoper")], 
        help="The note purpose: Print/Display.")                    
    text = fields.Char(
        string="Text", 
        help="Notes text.")                    

class ProcessResponseIdentifier(models.Model):    
    _name = "hc.process.response.identifier"    
    _description = "Process Response Identifier"            
    _inherit = ["hc.basic.association", "hc.identifier"]

    process_response_id = fields.Many2one(
        comodel_name="hc.res.process.response", 
        string="Process Response", 
        help="Process Response associated with this Process Response Identifier.")                    

class ProcessResponseStatusHistory(models.Model):       
    _name = "hc.process.response.status.history"    
    _description = "Process Response Status History"    
        
    process_response_id = fields.Many2one(  
        comodel_name="hc.res.process.response",
        string="Process Response",
        help="Process Response associated with this Process Response Status History.")
    status = fields.Char(   
        string="Status",
        help="The status of the process response.")
    start_date = fields.Datetime(   
        string="Start Date",
        help="Start of the period during which this process response status is valid.")
    end_date = fields.Datetime( 
        string="End Date",
        help="End of the period during which this process response status is valid.")
    time_diff_day = fields.Char(    
        string="Time Diff (days)",
        help="Days duration of the status.")
    time_diff_hour = fields.Char(   
        string="Time Diff (hours)",
        help="Hours duration of the status.")
    time_diff_min = fields.Char(    
        string="Time Diff (minutes)",
        help="Minutes duration of the status.")
    time_diff_sec = fields.Char(    
        string="Time Diff (seconds)",
        help="Seconds duration of the status.")

class ProcessResponseCommunicationRequest(models.Model):    
    _name = "hc.process.response.communication.request"    
    _description = "Process Response Communication Request"            
    _inherit = ["hc.basic.association"]

    process_response_id = fields.Many2one(
        comodel_name="hc.res.process.response", 
        string="Process Response", 
        help="Process Response associated with this Process Response Communication Request.")                    
    communication_request_id = fields.Many2one(
        comodel_name="hc.res.communication.request", 
        string="Communication Request", 
        help="CommunicationRequest associated with this Process Response Communication Request.")                    

class ProcessOutcome(models.Model):    
    _name = "hc.vs.process.outcome"    
    _description = "Process Outcome"            
    _inherit = ["hc.value.set.contains"]
