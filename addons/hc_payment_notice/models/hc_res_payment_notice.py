# -*- coding: utf-8 -*-

from openerp import models, fields, api
from datetime import datetime
from openerp.tools import DEFAULT_SERVER_DATETIME_FORMAT as DTF

class PaymentNotice(models.Model):    
    _name = "hc.res.payment.notice"    
    _description = "Payment Notice"        

    identifier_ids = fields.One2many(
        comodel_name="hc.payment.notice.identifier", 
        inverse_name="payment_notice_id", 
        string="Identifiers", 
        help="Business Identifier.")                
    status_id = fields.Many2one(
        comodel_name="hc.vs.fm.status", 
        string="Status", 
        help="The status of the resource instance.")                
    status_history_ids = fields.One2many(   
        comodel_name="hc.payment.notice.status.history",
        inverse_name="payment_notice_id",
        string="Status History",
        help="The status of the payment notice over time.")
    ruleset_id = fields.Many2one(
        comodel_name="hc.vs.ruleset", 
        string="Ruleset", 
        help="Resource version.")                
    original_ruleset_id = fields.Many2one(
        comodel_name="hc.vs.ruleset", 
        string="Original Ruleset", 
        help="Original version.")                
    created = fields.Datetime(
        string="Payment Notice Creation Date", 
        help="Creation date.")                
    target_id = fields.Many2one(
        comodel_name="hc.res.organization", 
        string="Target", 
        help="Insurer or Regulatory body.")                
    provider_id = fields.Many2one(
        comodel_name="hc.res.practitioner", 
        string="Provider", 
        help="Responsible practitioner.")                
    organization_id = fields.Many2one(
        comodel_name="hc.res.organization", 
        string="Organization", 
        help="Responsible organization.")                
    supporting_information_type = fields.Selection(
        string="Supporting Information Type", 
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
        help="Type of resource of request reference.")                
    supporting_information_type = fields.Selection(
        string="Supporting Information Type", 
        selection=[
            ("string", "String"), 
            ("code", "Code")], 
        help="Type of response reference.")                
    response_name = fields.Char(
        string="Response", 
        compute="_compute_response_name", 
        store="True", help="Response reference.")                
    response_string = fields.Char(
        string="Response String",
        help="String of response reference.")                
    response_code_id = fields.Many2one(
        comodel_name="hc.vs.resource.type", 
        string="Response Code", 
        help="Type of resource of response reference.")                
    payment_status_id = fields.Many2one(
        comodel_name="hc.vs.payment.status", 
        string="Payment Status", 
        required="True", 
        help="Status of the payment.")                
    status_date = fields.Date(
        string="Status Date", 
        help="Payment or clearing date.")                

    @api.model                          
    def create(self, vals):                         
        status_history_obj = self.env['hc.payment.notice.status.history']                       
        res = super(PaymentNotice, self).create(vals)                       
        if vals and vals.get('status_id'):                      
            status_history_vals = {                 
                'payment_notice_id': res.id,                
                'status': res.status_id.name,               
                'start_date': datetime.today()              
                }               
            if vals.get('status_id') == 'entered-in-error':                 
                status_history_vals.update({'end_date': datetime.today()})              
            status_history_obj.create(status_history_vals)                  
        return res                      
                                
    @api.multi                          
    def write(self, vals):                          
        status_history_obj = self.env['hc.payment.notice.status.history']                       
        fm_status_obj = self.env['hc.vs.fm.status']                     
        res = super(PaymentNotice, self).write(vals)                        
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
                    'payment_notice_id': self.id,           
                    'status': fm_status.name,           
                    'start_date': datetime.today()          
                    }           
                if vals.get('status_id') == 'entered-in-error':             
                    status_id_history_vals.update({'end_date': datetime.today()})           
                status_history_obj.create(status_history_vals)              
        return res                      

class PaymentNoticeIdentifier(models.Model):    
    _name = "hc.payment.notice.identifier"    
    _description = "Payment Notice Identifier"        
    _inherit = ["hc.basic.association", "hc.identifier"]

    payment_notice_id = fields.Many2one(
        comodel_name="hc.res.payment.notice", 
        string="Payment Notice", 
        help="Payment Notice associated with this Payment Notice Identifier.")                

class PaymentNoticeStatusHistory(models.Model):     
    _name = "hc.payment.notice.status.history"  
    _description = "Payment Notice Status History"  
        
    payment_notice_id = fields.Many2one(    
        comodel_name="hc.res.payment.notice",
        string="Payment Notice",
        help="Payment Notice associated with this Payment Notice Status History.")
    status = fields.Char(   
        string="Status",
        help="The status of the payment notice.")
    start_date = fields.Datetime(   
        string="Start Date",
        help="Start of the period during which this payment notice status is valid.")
    end_date = fields.Datetime( 
        string="End Date",
        help="End of the period during which this payment notice status is valid.")
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

class PaymentStatus(models.Model):    
    _name = "hc.vs.payment.status"    
    _description = "Payment Status"        
    _inherit = ["hc.value.set.contains"]
