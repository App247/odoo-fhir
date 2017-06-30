# -*- coding: utf-8 -*-

from openerp import models, fields, api
from datetime import datetime
from openerp.tools import DEFAULT_SERVER_DATETIME_FORMAT as DTF

class ProcessRequest(models.Model):    
    _name = "hc.res.process.request"    
    _description = "Process Request"            

    identifier_ids = fields.One2many(
        comodel_name="hc.process.request.identifier", 
        inverse_name="process_request_id", 
        string="Identifiers", 
        help="Business Identifier.")                    
    status_id = fields.Many2one(
        comodel_name="hc.vs.fm.status", 
        string="Status", 
        help="The status of the resource instance.")                    
    status_history_ids = fields.One2many(   
        comodel_name="hc.process.request.status.history",
        inverse_name="process_request_id",
        string="Status History",
        help="The status of the process request over time.")
    action = fields.Selection(
        string="Action", 
        required="True", 
        selection=[
            ("cancel", "Cancel"), 
            ("poll", "Poll"), 
            ("reprocess", "Reprocess"), 
            ("status", "Status")], 
        help="The type of processing action being requested, for example Reversal, Readjudication, StatusRequest,PendedRequest.")                    
    target_id = fields.Many2one(
        comodel_name="hc.res.organization", 
        string="Target", 
        help="Target of the request.")                    
    created = fields.Datetime(
        string="Creation Date", 
        help="Creation date.")                    
    provider_id = fields.Many2one(
        comodel_name="hc.res.practitioner", 
        string="Provider", 
        help="Responsible practitioner.")                    
    organization_id = fields.Many2one(
        comodel_name="hc.res.organization", 
        string="Organization", 
        help="Responsible organization.")                    
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
    response_type = fields.Selection(
        string="Response Type", 
        selection=[
            ("string", "String"), 
            ("code", "Code")], 
        help="Type of response reference.")                    
    response_name = fields.Char(
        string="Response", 
        compute="_compute_response_name", 
        store="True", 
        help="Response reference.")                    
    response_string = fields.Char(
        string="Response String", 
        help="String of response reference.")                    
    response_code_id = fields.Many2one(
        comodel_name="hc.vs.resource.type", 
        string="Response Code", 
        help="Code response reference.")                    
    is_nullify = fields.Boolean(
        string="Nullify", 
        help="Nullify.")                    
    reference = fields.Char(
        string="Reference", 
        help="Reference number/string.")                    
    include_ids = fields.One2many(
        comodel_name="hc.process.request.include", 
        inverse_name="process_request_id", 
        string="Includes", 
        help="Resource type(s) to include.")                    
    exclude_ids = fields.One2many(
        comodel_name="hc.process.request.exclude", 
        inverse_name="process_request_id", 
        string="Excludes", 
        help="Resource type(s) to exclude.")                    
    start_date = fields.Datetime(
        string="Start Date", 
        help="Start of the period.")                    
    end_date = fields.Datetime(
        string="End Date", 
        help="End of the period.")
    item_ids = fields.One2many(
        comodel_name="hc.process.request.item", 
        inverse_name="process_request_id", 
        string="Items", 
        help="Items to re-adjudicate.")                    

    @api.model                          
    def create(self, vals):                         
        status_history_obj = self.env['hc.process.request.status.history']                      
        res = super(ProcessRequest, self).create(vals)                      
        if vals and vals.get('status_id'):                      
            status_history_vals = {                 
                'process_request_id': res.id,               
                'status': res.status_id.name,               
                'start_date': datetime.today()              
                }               
            if vals.get('status_id') == 'entered-in-error':                 
                status_history_vals.update({'end_date': datetime.today()})              
            status_history_obj.create(status_history_vals)                  
        return res                      
                                
    @api.multi                          
    def write(self, vals):                          
        status_history_obj = self.env['hc.process.request.status.history']                      
        fm_status_obj = self.env['hc.vs.fm.status']                     
        res = super(ProcessRequest, self).write(vals)                       
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
                    'process_request_id': self.id,          
                    'status': fm_status.name,           
                    'start_date': datetime.today()          
                    }           
                if vals.get('status_id') == 'entered-in-error':             
                    status_id_history_vals.update({'end_date': datetime.today()})           
                status_history_obj.create(status_history_vals)              
        return res                      

class ProcessRequestItem(models.Model):    
    _name = "hc.process.request.item"    
    _description = "Process Request Item"            

    process_request_id = fields.Many2one(
        comodel_name="hc.res.process.request", 
        string="Process Request", 
        help="Process Request associated with this Item.")
    sequence_link_id = fields.Integer(
        string="Sequence Link Id", 
        required="True", 
        help="Service instance.")                    

class ProcessRequestIdentifier(models.Model):    
    _name = "hc.process.request.identifier"    
    _description = "Process Request Identifier"            
    _inherit = ["hc.basic.association", "hc.identifier"]

    process_request_id = fields.Many2one(
        comodel_name="hc.res.process.request", 
        string="Process Request", 
        help="Process Request associated with this Process Request Identifier.")                    

class ProcessRequestStatusHistory(models.Model):        
    _name = "hc.process.request.status.history" 
    _description = "Process Request Status History" 
        
    process_request_id = fields.Many2one(   
        comodel_name="hc.res.process.request",
        string="Process Request",
        help="Process Request associated with this Process Request Status History.")
    status = fields.Char(   
        string="Status",
        help="The status of the process request.")
    start_date = fields.Datetime(   
        string="Start Date",
        help="Start of the period during which this process request status is valid.")
    end_date = fields.Datetime( 
        string="End Date",
        help="End of the period during which this process request status is valid.")
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

class ProcessRequestInclude(models.Model):    
    _name = "hc.process.request.include"    
    _description = "Process Request Include"            
    _inherit = ["hc.basic.association"]

    process_request_id = fields.Many2one(
        comodel_name="hc.res.process.request", 
        string="Process Request", 
        help="Process Request associated with this Process Request Include.")                    
    include = fields.Char(
        string="Include", 
        help="String associated with this Process Request Include.")                    

class ProcessRequestExclude(models.Model):    
    _name = "hc.process.request.exclude"    
    _description = "Process Request Exclude"            
    _inherit = ["hc.basic.association"]

    process_request_id = fields.Many2one(
        comodel_name="hc.res.process.request", 
        string="Process Request", 
        help="Process Request associated with this Process Request Exclude.")                    
    exclude = fields.Char(
        string="Exclude", 
        help="String associated with this Process Request Exclude.")                    
