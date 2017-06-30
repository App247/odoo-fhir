# -*- coding: utf-8 -*-

from openerp import models, fields, api
from datetime import datetime
from openerp.tools import DEFAULT_SERVER_DATETIME_FORMAT as DTF

class EnrollmentRequest(models.Model):    
    _name = "hc.res.enrollment.request"    
    _description = "Enrollment Request"        

    identifier_ids = fields.One2many(
        comodel_name="hc.enrollment.request.identifier", 
        inverse_name="enrollment_request_id", 
        string="Identifiers", 
        help="Business Identifier.")                
    status_id = fields.Many2one(
        comodel_name="hc.vs.fm.status", 
        string="Status", 
        help="The status of the resource instance.")                
    status_history_ids = fields.One2many(   
        comodel_name="hc.enrollment.request.status.history",
        inverse_name="enrollment_request_id",
        string="Status History",
        help="The status of the enrollment request over time.")
    ruleset_id = fields.Many2one(
        comodel_name="hc.vs.ruleset", 
        string="Ruleset", 
        help="Resource version.")                
    original_ruleset_id = fields.Many2one(
        comodel_name="hc.vs.ruleset", 
        string="Original Ruleset", 
        help="Original version.")                
    created = fields.Datetime(
        string="Enrollment Request Creation Date", 
        help="Creation date.")                
    target_id = fields.Many2one(
        comodel_name="hc.res.organization", 
        string="Target", 
        help="Insurer.")                
    provider_id = fields.Many2one(
        comodel_name="hc.res.practitioner", 
        string="Provider", 
        help="Responsible practitioner.")                
    organization_id = fields.Many2one(
        comodel_name="hc.res.organization", 
        string="Organization", 
        help="Responsible organization.")                
    subject_id = fields.Many2one(
        comodel_name="hc.res.patient", 
        string="Subject", 
        required="True", 
        help="The subject of the Products and Services.")                
    coverage_id = fields.Many2one(
        comodel_name="hc.res.coverage", 
        string="Coverage", 
        required="True", 
        help="Insurance information.")                
    relationship_id = fields.Many2one(
        comodel_name="hc.vs.enrollment.relationship", 
        string="Relationship", 
        required="True", 
        help="Patient relationship to subscriber.")                

    @api.model                          
    def create(self, vals):                         
        status_history_obj = self.env['hc.enrollment.request.status.history']                       
        res = super(EnrollmentRequest, self).create(vals)                       
        if vals and vals.get('status_id'):                      
            status_history_vals = {                 
                'enrollment_request_id': res.id,                
                'status': res.status_id.name,               
                'start_date': datetime.today()              
                }               
            if vals.get('status_id') == 'entered-in-error':                 
                status_history_vals.update({'end_date': datetime.today()})              
            status_history_obj.create(status_history_vals)                  
        return res                      
                                
    @api.multi                          
    def write(self, vals):                          
        status_history_obj = self.env['hc.enrollment.request.status.history']                       
        fm_status_obj = self.env['hc.vs.fm.status']                     
        res = super(EnrollmentRequest, self).write(vals)                        
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
                    'enrollment_request_id': self.id,           
                    'status': fm_status.name,           
                    'start_date': datetime.today()          
                    }           
                if vals.get('status_id') == 'entered-in-error':             
                    status_id_history_vals.update({'end_date': datetime.today()})           
                status_history_obj.create(status_history_vals)              
        return res                      

class EnrollmentRequestIdentifier(models.Model):    
    _name = "hc.enrollment.request.identifier"    
    _description = "Enrollment Request Identifier"        
    _inherit = ["hc.basic.association", "hc.identifier"]

    enrollment_request_id = fields.Many2one(
        comodel_name="hc.res.enrollment.request", 
        string="Enrollment Request", 
        help="Enrollment Request associated with this Enrollment Request Identifier.")                

class EnrollmentRequestStatusHistory(models.Model):     
    _name = "hc.enrollment.request.status.history"  
    _description = "Enrollment Request Status History"  
        
    enrollment_request_id = fields.Many2one(    
        comodel_name="hc.res.enrollment.request",
        string="Enrollment Request",
        help="Enrollment Request associated with this Enrollment Request Status History.")
    status = fields.Char(   
        string="Status",
        help="The status of the enrollment request.")
    start_date = fields.Datetime(   
        string="Start Date",
        help="Start of the period during which this enrollment request status is valid.")
    end_date = fields.Datetime( 
        string="End Date",
        help="End of the period during which this enrollment request status is valid.")
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

class EnrollmentRelationship(models.Model):    
    _name = "hc.vs.enrollment.relationship"    
    _description = "Enrollment Relationship"        
    _inherit = ["hc.value.set.contains"]
