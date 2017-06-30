# -*- coding: utf-8 -*-

from openerp import models, fields, api
from datetime import datetime
from openerp.tools import DEFAULT_SERVER_DATETIME_FORMAT as DTF

class EligibilityRequest(models.Model):    
    _name = "hc.res.eligibility.request"    
    _description = "Eligibility Request"        
    
    identifier_ids = fields.One2many(
        comodel_name="hc.eligibility.request.identifier", 
        inverse_name="eligibility_request_id", 
        string="Identifiers", 
        help="Business Identifier.")
    status_id = fields.Many2one(
        comodel_name="hc.vs.fm.status", 
        string="Status", 
        help="The status of the resource instance.")
    status_history_ids = fields.One2many(   
        comodel_name="hc.eligibility.request.status.history",
        inverse_name="eligibility_request_id",
        string="Status History",
        help="The status of the eligibility request over time.")
    priority_id = fields.Many2one(
        comodel_name="hc.vs.process.priority", 
        string="Priority", 
        help="Desired processing priority.")
    patient_id = fields.Many2one(
        comodel_name="hc.res.patient", 
        string="Patient",
        help="The subject of the Products and Services.")
    serviced_type = fields.Selection(
        string="Serviced Type", 
        selection=[
            ("date", "Date"), 
            ("period", "Period")], 
        help="Type of who recorded the sensitivity.")
    serviced_name = fields.Char(
        string="Serviced", 
        compute="_compute_serviced_name", 
        store="True", 
        help="Estimated date or dates of Service.")
    serviced_date = fields.Date(
        string="Serviced Date", 
        help="Code of estimated date or dates of service.")
    serviced_start_date = fields.Datetime(
        string="Serviced Start Date", 
        help="Start of estimated date or dates of service.")
    serviced_end_date = fields.Datetime(
        string="Serviced End Date", 
        help="End of estimated date or dates of service.")
    created = fields.Datetime(
        string="Created", 
        help="Creation date.")
    enterer_id = fields.Many2one(
        comodel_name="hc.res.practitioner", 
        string="Enterer", 
        help="Author.")
    provider_id = fields.Many2one(
        comodel_name="hc.res.practitioner", 
        string="Provider", 
        help="Responsible practitioner.")
    organization_id = fields.Many2one(
        comodel_name="hc.res.organization", 
        string="Organization", 
        help="Responsible organization.")
    insurer_id = fields.Many2one(
        comodel_name="hc.res.organization", 
        string="Insurer", 
        help="Target.")
    facility_id = fields.Many2one(
        comodel_name="hc.res.location", 
        string="Facility", 
        help="Servicing Facility.")
    coverage_id = fields.Many2one(
        comodel_name="hc.res.coverage", 
        string="Coverage", 
        help="Insurance or medical plan.")
    business_arrangement = fields.Char(
        string="Business Arrangement", 
        help="Business agreement.")
    benefit_category_id = fields.Many2one(
        comodel_name="hc.vs.benefit.category", 
        string="Benefit Category", 
        help="Benefit Category.")
    benefit_sub_category_id = fields.Many2one(
        comodel_name="hc.vs.benefit.sub.category", 
        string="Benefit Sub Category", 
        help="Benefit SubCategory.")

    @api.model                          
    def create(self, vals):                         
        status_history_obj = self.env['hc.eligibility.request.status.history']                      
        res = super(EligibilityRequest, self).create(vals)                      
        if vals and vals.get('status_id'):                      
            status_history_vals = {                 
                'eligibility_request_id': res.id,               
                'status': res.status_id.name,               
                'start_date': datetime.today()              
                }               
            if vals.get('status_id') == 'entered-in-error':                 
                status_history_vals.update({'end_date': datetime.today()})              
            status_history_obj.create(status_history_vals)                  
        return res                      
                                
    @api.multi                          
    def write(self, vals):                          
        status_history_obj = self.env['hc.eligibility.request.status.history']                      
        fm_status_obj = self.env['hc.vs.fm.status']                     
        res = super(EligibilityRequest, self).write(vals)                       
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
                    'eligibility_request_id': self.id,          
                    'status': fm_status.name,           
                    'start_date': datetime.today()          
                    }           
                if vals.get('status_id') == 'entered-in-error':             
                    status_id_history_vals.update({'end_date': datetime.today()})           
                status_history_obj.create(status_history_vals)              
        return res 

class EligibilityRequestIdentifier(models.Model):    
    _name = "hc.eligibility.request.identifier"    
    _description = "Eligibility Request Identifier"        
    _inherit = ["hc.basic.association", "hc.identifier"]

    eligibility_request_id = fields.Many2one(
        comodel_name="hc.res.eligibility.request", 
        string="Eligibility Request", 
        help="Eligibility Request associated with this Eligibility Request Identifier.")                                     

class EligibilityRequestStatusHistory(models.Model):        
    _name = "hc.eligibility.request.status.history" 
    _description = "Eligibility Request Status History" 
        
    eligibility_request_id = fields.Many2one(   
        comodel_name="hc.res.eligibility.request",
        string="Eligibility Request",
        help="Eligibility Request associated with this Eligibility Request Status History.")
    status = fields.Char(   
        string="Status",
        help="The status of the eligibility request.")
    start_date = fields.Datetime(   
        string="Start Date",
        help="Start of the period during which this eligibility request status is valid.")
    end_date = fields.Datetime( 
        string="End Date",
        help="End of the period during which this eligibility request status is valid.")
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

class ProcessPriority(models.Model):    
    _name = "hc.vs.process.priority"    
    _description = "Process Priority"        
    _inherit = ["hc.value.set.contains"]

class BenefitCategory(models.Model):    
    _name = "hc.vs.benefit.category"    
    _description = "Benefit Category"        
    _inherit = ["hc.value.set.contains"]

class BenefitSubCategory(models.Model):    
    _name = "hc.vs.benefit.sub.category"    
    _description = "Benefit Sub Category"        
    _inherit = ["hc.value.set.contains"]

class BenefitNetwork(models.Model):    
    _name = "hc.vs.benefit.network"    
    _description = "Benefit Network"        
    _inherit = ["hc.value.set.contains"]

class BenefitUnit(models.Model):    
    _name = "hc.vs.benefit.unit"    
    _description = "Benefit Unit"        
    _inherit = ["hc.value.set.contains"]

class BenefitTerm(models.Model):    
    _name = "hc.vs.benefit.term"    
    _description = "Benefit Term"        
    _inherit = ["hc.value.set.contains"]

class AdjudicationError(models.Model):    
    _name = "hc.vs.adjudication.error"    
    _description = "Adjudication Error"        
    _inherit = ["hc.value.set.contains"]