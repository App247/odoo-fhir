# -*- coding: utf-8 -*-

from openerp import models, fields, api
from datetime import datetime
from openerp.tools import DEFAULT_SERVER_DATETIME_FORMAT as DTF

class EligibilityResponse(models.Model):    
    _name = "hc.res.eligibility.response"    
    _description = "Eligibility Response"        

    identifier_ids = fields.One2many(
        comodel_name="hc.eligibility.response.identifier", 
        inverse_name="eligibility_response_id", 
        string="Identifiers", 
        help="Business Identifier.")                
    status_id = fields.Many2one(
        comodel_name="hc.vs.fm.status", 
        string="Status", 
        help="The status of the resource instance.")                
    status_history_ids = fields.One2many(   
        comodel_name="hc.eligibility.response.status.history",
        inverse_name="eligibility_response_id",
        string="Status History",
        help="The status of the eligibility response over time.")
    request_id = fields.Many2one(
        comodel_name="hc.res.eligibility.request", 
        string="Request", 
        help="Claim reference.")                
    outcome = fields.Selection(
        string="Eligibility Response Outcome", 
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
        string="Eligibility Response Creation Date", 
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
    is_inforce = fields.Boolean(
        string="Inforce", 
        help="Coverage inforce.")                
    # contract_id = fields.Many2one(
    #     comodel_name="hc.res.contract", 
    #     string="Contract", 
    #     help="Contract details.")                
    form_id = fields.Many2one(
        comodel_name="hc.vs.forms", 
        string="Form", 
        help="Printed Form Identifier.")                
    benefit_balance_ids = fields.One2many(
        comodel_name="hc.eligibility.response.benefit.balance", 
        inverse_name="eligibility_response_id", 
        string="Benefit Balances", 
        help="Benefits by Category.")                
    error_ids = fields.One2many(
        comodel_name="hc.eligibility.response.error", 
        inverse_name="eligibility_response_id", 
        string="Errors", 
        help="Processing errors.")                

    @api.model                          
    def create(self, vals):                         
        status_history_obj = self.env['hc.eligibility.response.status.history']                     
        res = super(EligibilityResponse, self).create(vals)                     
        if vals and vals.get('status_id'):                      
            status_history_vals = {                 
                'eligibility_response_id': res.id,              
                'status': res.status_id.name,               
                'start_date': datetime.today()              
                }               
            if vals.get('status_id') == 'entered-in-error':                 
                status_history_vals.update({'end_date': datetime.today()})              
            status_history_obj.create(status_history_vals)                  
        return res                      
                                
    @api.multi                          
    def write(self, vals):                          
        status_history_obj = self.env['hc.eligibility.response.status.history']                     
        fm_status_obj = self.env['hc.vs.fm.status']                     
        res = super(EligibilityResponse, self).write(vals)                      
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
                    'eligibility_response_id': self.id,         
                    'status': fm_status.name,           
                    'start_date': datetime.today()          
                    }           
                if vals.get('status_id') == 'entered-in-error':             
                    status_id_history_vals.update({'end_date': datetime.today()})           
                status_history_obj.create(status_history_vals)              
        return res                      

class EligibilityResponseBenefitBalance(models.Model):    
    _name = "hc.eligibility.response.benefit.balance"    
    _description = "Eligibility Response Benefit Balance"        

    eligibility_response_id = fields.Many2one(
        comodel_name="hc.res.eligibility.response", 
        string="Eligibility Response", 
        help="Eligibility Response associated with this Eligibility Response Benefit Balance.")                
    category_id = fields.Many2one(
        comodel_name="hc.vs.benefit.category", 
        string="Category", 
        required="True", 
        help="Benefit Category.")                
    sub_category_id = fields.Many2one(
        comodel_name="hc.vs.benefit.sub.category", 
        string="Sub Category", 
        help="Benefit SubCategory.")                
    name = fields.Char(
        string="Name", 
        help="Short name for the benefit.")                
    description = fields.Text(
        string="Description", 
        help="Description of the benefit.")                
    network_id = fields.Many2one(
        comodel_name="hc.vs.benefit.network", 
        string="Network", 
        help="In or out of network.")                
    unit_id = fields.Many2one(
        comodel_name="hc.vs.benefit.unit", 
        string="Unit", 
        help="Individual or family.")                
    term_id = fields.Many2one(
        comodel_name="hc.vs.benefit.term", 
        string="Term", 
        help="Annual or lifetime.")                
    financial_ids = fields.One2many(
        comodel_name="hc.eligibility.response.benefit.balance.financial", 
        inverse_name="benefit_balance_id", 
        string="Financials", 
        help="Benefit Summary.")                

class EligibilityResponseBenefitBalanceFinancial(models.Model):    
    _name = "hc.eligibility.response.benefit.balance.financial"    
    _description = "Eligibility Response Benefit Balance Financial"        

    benefit_balance_id = fields.Many2one(
        comodel_name="hc.eligibility.response.benefit.balance", 
        string="Benefit Balance", 
        help="Benefit Balance associated with this Eligibility Response Benefit Balance Financial.")                
    type_id = fields.Many2one(
        comodel_name="hc.vs.benefit.code", 
        string="Type", 
        required="True", 
        help="Deductable, visits, benefit amount.")                
    benefit_type = fields.Selection(
        string="Benefit Type", 
        selection=[
            ("unsigned Int", "Unsigned Int"), 
            ("string", "String"), 
            ("Money", "Money")], 
        help="Type of benefits allowed.")                
    benefit_name = fields.Char(
        string="Benefit Name", 
        help="Benefits allowed.")                
    benefit_unsigned_int = fields.Integer(
        string="Benefit Unsigned Int", 
        help="Code of benefits allowed.")                
    benefit_string = fields.Char(
        string="Benefit String", 
        help="String of content of this set of documents.")                
    benefit_money = fields.Float(
        string="Benefit Money", 
        help="Money content of this set of documents.")                
    benefit_used_type = fields.Selection(
        string="Benefit Used Type", 
        selection=[
            ("unsigned Int", "Unsigned Int"), 
            ("Money", "Money")], 
        help="Type of benefits used.")                
    benefit_used_name = fields.Char(
        string="Benefit Used Name", 
        help="Benefits used.")                
    benefit_used_unsigned_int = fields.Integer(
        string="Benefit Used Unsigned Int", 
        help="Code of benefits used.")                
    benefit_used_money = fields.Float(
        string="Benefit Used Money", 
        help="Money content of this set of documents.")                

class EligibilityResponseError(models.Model):    
    _name = "hc.eligibility.response.error"    
    _description = "Eligibility Response Error"        

    eligibility_response_id = fields.Many2one(
        comodel_name="hc.res.eligibility.response", 
        string="Eligibility Response", 
        help="Eligibility Response associated with this Eligibility Response Error.")                
    code_id = fields.Many2one(
        comodel_name="hc.vs.adjudication.error", 
        string="Code", required="True", 
        help="Error code detailing processing issues.")                

class EligibilityResponseIdentifier(models.Model):    
    _name = "hc.eligibility.response.identifier"    
    _description = "Eligibility Response Identifier"        
    _inherit = ["hc.basic.association", "hc.identifier"]

    eligibility_response_id = fields.Many2one(
        comodel_name="hc.res.eligibility.response", 
        string="Eligibility Response", 
        help="Eligibility Response associated with this Eligibility Response Identifier.")                

class EligibilityResponseStatusHistory(models.Model):       
    _name = "hc.eligibility.response.status.history"    
    _description = "Eligibility Response Status History"    
        
    eligibility_response_id = fields.Many2one(  
        comodel_name="hc.res.eligibility.response",
        string="Eligibility Response",
        help="Eligibility Response associated with this Eligibility Response Status History.")
    status = fields.Char(   
        string="Status",
        help="The status of the eligibility response.")
    start_date = fields.Datetime(   
        string="Start Date",
        help="Start of the period during which this eligibility response status is valid.")
    end_date = fields.Datetime( 
        string="End Date",
        help="End of the period during which this eligibility response status is valid.")
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

class BenefitCode(models.Model):    
    _name = "hc.vs.benefit.code"    
    _description = "Benefit Code"        
    _inherit = ["hc.value.set.contains"]
