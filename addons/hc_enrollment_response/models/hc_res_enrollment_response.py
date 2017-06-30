# -*- coding: utf-8 -*-

from openerp import models, fields, api
from datetime import datetime
from openerp.tools import DEFAULT_SERVER_DATETIME_FORMAT as DTF

class EnrollmentResponse(models.Model):    
    _name = "hc.res.enrollment.response"    
    _description = "Enrollment Response"        
    
    identifier_ids = fields.One2many(
        comodel_name="hc.enrollment.response.identifier", 
        inverse_name="enrollment_response_id", 
        string="Identifiers", 
        help="Business Identifier.")                
    status_id = fields.Many2one(
        comodel_name="hc.vs.fm.status", 
        string="Status", 
        help="The status of the resource instance.")   
    status_history_ids = fields.One2many(   
        comodel_name="hc.enrollment.response.status.history",
        inverse_name="enrollment_response_id",
        string="Status History",
        help="The status of the enrollment response over time.")
    request_id = fields.Many2one(
        comodel_name="hc.res.enrollment.request", 
        string="Request", 
        help="Claim reference.")                
    outcome = fields.Selection(
        string="Enrollment Response Outcome", 
        selection=[
            ("complete", "Complete"), 
            ("error", "Error")], 
        help="Transaction status: error, complete.")                
    disposition = fields.Text(
        string="Disposition", 
        help="Disposition Message.")                
    ruleset_id = fields.Many2one(
        comodel_name="hc.vs.ruleset", 
        string="Ruleset", 
        help="Resource version.")                
    original_ruleset_id = fields.Many2one(
        comodel_name="hc.vs.ruleset", 
        string="Original Ruleset", 
        help="Original version.")                
    created = fields.Datetime(
        string="Creation Date", 
        help="Creation date.")                
    organization_id = fields.Many2one(
        comodel_name="hc.res.organization", 
        string="Organization", 
        help="Insurer.")                
    request_provider_id = fields.Many2one(
        comodel_name="hc.res.practitioner", 
        string="Request Provider", 
        help="Responsible practitioner.")                
    request_organization_id = fields.Many2one(
        comodel_name="hc.res.organization", 
        string="Request Organization", 
        help="Responsible organization.")                

    @api.model                          
    def create(self, vals):                         
        status_history_obj = self.env['hc.enrollment.response.status.history']                      
        res = super(EnrollmentResponse, self).create(vals)                      
        if vals and vals.get('status_id'):                      
            status_history_vals = {                 
                'enrollment_response_id': res.id,               
                'status': res.status_id.name,               
                'start_date': datetime.today()              
                }               
            if vals.get('status_id') == 'entered-in-error':                 
                status_history_vals.update({'end_date': datetime.today()})              
            status_history_obj.create(status_history_vals)                  
        return res                      
                                
    @api.multi                          
    def write(self, vals):                          
        status_history_obj = self.env['hc.enrollment.response.status.history']                      
        fm_status_obj = self.env['hc.vs.fm.status']                     
        res = super(EnrollmentResponse, self).write(vals)                       
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
                    'enrollment_response_id': self.id,          
                    'status': fm_status.name,           
                    'start_date': datetime.today()          
                    }           
                if vals.get('status_id') == 'entered-in-error':             
                    status_id_history_vals.update({'end_date': datetime.today()})           
                status_history_obj.create(status_history_vals)              
        return res                      

class EnrollmentResponseIdentifier(models.Model):    
    _name = "hc.enrollment.response.identifier"    
    _description = "Enrollment Response Identifier"        
    _inherit = ["hc.basic.association", "hc.identifier"]

    enrollment_response_id = fields.Many2one(
        comodel_name="hc.res.enrollment.response", 
        string="Enrollment Response", 
        help="Enrollment Response associated with this Enrollment Response Enrollment Response Identifier.")                

class EnrollmentResponseStatusHistory(models.Model):        
    _name = "hc.enrollment.response.status.history" 
    _description = "Enrollment Response Status History" 
        
    enrollment_response_id = fields.Many2one(   
        comodel_name="hc.res.enrollment.response",
        string="Enrollment Response",
        help="Enrollment Response associated with this Enrollment Response Status History.")
    status = fields.Char(   
        string="Status",
        help="The status of the enrollment response.")
    start_date = fields.Datetime(   
        string="Start Date",
        help="Start of the period during which this enrollment response status is valid.")
    end_date = fields.Datetime( 
        string="End Date",
        help="End of the period during which this enrollment response status is valid.")
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