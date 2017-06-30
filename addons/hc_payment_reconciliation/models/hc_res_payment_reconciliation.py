# -*- coding: utf-8 -*-

from openerp import models, fields, api
from datetime import datetime
from openerp.tools import DEFAULT_SERVER_DATETIME_FORMAT as DTF

class PaymentReconciliation(models.Model):  
    _name = "hc.res.payment.reconciliation" 
    _description = "Payment Reconciliation"     

    identifier_ids = fields.One2many(
        comodel_name="hc.payment.reconciliation.identifier", 
        inverse_name="payment_reconciliation_id", 
        string="Identifiers", 
        help="Business Identifier.")              
    status_id = fields.Many2one(
        comodel_name="hc.vs.fm.status", 
        string="Status",  
        help="The status of the resource instance.")             
    status_history_ids = fields.One2many(       
        comodel_name="hc.payment.reconciliation.status.history",    
        inverse_name="payment_reconciliation_id",   
        string="Status History",    
        help="The status of the payment reconciliation over time.")
    period_start_date = fields.Datetime(
        string="Period Start Date", 
        help="Start of the period covered.")                
    period_end_date = fields.Datetime(
        string="Period End Date", 
        help="End of the period covered.")              
    created = fields.Datetime(
        string="Created", 
        help="Creation date.")              
    organization_id = fields.Many2one(
        comodel_name="hc.res.organization", 
        string="Organization", 
        help="Insurer.")               
    request_id = fields.Many2one(
        comodel_name="hc.res.process.request", 
        string="Request", 
        help="Claim reference.")              
    outcome = fields.Selection(
        string="Outcome", 
        selection=[
            ("complete", "Complete"), 
            ("error", "Error"), 
            ("partial", "Partial")], 
        help="Transaction status: error, complete.")             
    disposition = fields.Text(
        string="Disposition", 
        help="Disposition Message.")                
    request_provider_id = fields.Many2one(
        comodel_name="hc.res.practitioner", 
        string="Request Provider", 
        help="Responsible practitioner.")              
    request_organization_id = fields.Many2one(
        comodel_name="hc.res.organization", 
        string="Request Organization", 
        help="Responsible organization.")              
    form_id = fields.Many2one(
        comodel_name="hc.vs.forms", 
        string="Form", 
        help="Printed Form Identifier.")               
    total = fields.Float(
        string="Total", 
        required="True", 
        help="Total amount of Payment.")              
    detail_ids = fields.One2many(
        comodel_name="hc.payment.reconciliation.detail", 
        inverse_name="payment_reconciliation_id", 
        string="Details", 
        help="Details.")              
    note_ids = fields.One2many(
        comodel_name="hc.payment.reconciliation.note", 
        inverse_name="payment_reconciliation_id", 
        string="Notes", 
        help="Note text.")              

    @api.model                          
    def create(self, vals):                         
        status_history_obj = self.env['hc.payment.reconciliation.status.history']                       
        res = super(PaymentReconciliation, self).create(vals)                       
        if vals and vals.get('status_id'):                      
            status_history_vals = {                 
                'payment_reconciliation_id': res.id,                
                'status': res.status_id.name,              
                'start_date': datetime.today()              
                }               
            if vals.get('status_id') == 'entered-in-error':                 
                status_history_vals.update({'end_date': datetime.today()})              
            status_history_obj.create(status_history_vals)                  
        return res                      
                                
    @api.multi                          
    def write(self, vals):                          
        status_history_obj = self.env['hc.payment.reconciliation.status.history']                       
        fm_status_obj = self.env['hc.vs.fm.status']                     
        res = super(PaymentReconciliation, self).write(vals)                        
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
                    'payment_reconciliation_id': self.id,           
                    'status': fm_status.name,           
                    'start_date': datetime.today()          
                    }           
                if vals.get('status_id') == 'entered-in-error':             
                    status_id_history_vals.update({'end_date': datetime.today()})           
                status_history_obj.create(status_history_vals)              
        return res                      
              
class PaymentReconciliationDetail(models.Model):    
    _name = "hc.payment.reconciliation.detail"    
    _description = "Payment Reconciliation Detail"        

    payment_reconciliation_id = fields.Many2one(
        comodel_name="hc.res.payment.reconciliation", 
        string="Payment Reconciliation", 
        help="Payment Reconciliation associated with this Payment Reconciliation Detail.")                
    type_id = fields.Many2one(
        comodel_name="hc.vs.payment.type", 
        string="Type", 
        required="True", 
        help="Type code.")                
    request_type = fields.Selection(
        string="Request Type", 
        selection=[
            ("string", "String"), 
            ("code", "Code")], 
        help="Type of claim.")                
    request_name = fields.Char(
        string="Request", 
        compute="_compute_request_name", 
        store="True", 
        help="Claim.")                
    request_string = fields.Char(
        string="Request String", 
        help="String of claim.")                
    request_code_id = fields.Many2one(
        comodel_name="hc.vs.resource.type", 
        string="Request Code", 
        help="Type of resource of claim.")                
    response_type = fields.Selection(
        string="Response Type", 
        selection=[
            ("string", "String"), 
            ("code", "Code")], 
        help="Type of claim response.")                
    response_name = fields.Char(
        string="Response", 
        compute="_compute_response_name", 
        store="True", 
        help="Claim Response.")                
    response_string = fields.Char(
        string="Response String", 
        help="String of claim response.")                
    response_code_id = fields.Many2one(
        comodel_name="hc.vs.resource.type", 
        string="Response Code", 
        help="Type of resource of claim response.")                
    submitter_id = fields.Many2one(
        comodel_name="hc.res.organization", 
        string="Submitter", 
        help="Submitter.")                
    payee_id = fields.Many2one(
        comodel_name="hc.res.organization", 
        string="Payee", 
        help="Payee.")                
    date = fields.Date(
        string="Date", 
        help="Invoice date.")                
    amount = fields.Float(
        string="Amount", 
        help="Detail amount.")                

class PaymentReconciliationNote(models.Model):    
    _name = "hc.payment.reconciliation.note"    
    _description = "Payment Reconciliation Note"        

    payment_reconciliation_id = fields.Many2one(
        comodel_name="hc.res.payment.reconciliation", 
        string="Payment Reconciliation", 
        help="Payment Reconciliation associated with this Payment Reconciliation Note.")                
    type = fields.Selection(
        string="Type", 
        selection=[
            ("display", "Display"), 
            ("print", "Print"), 
            ("printoper", "Printoper")], 
        help="The note purpose: Print/Display.")                
    text = fields.Text(
        string="Text", 
        help="Notes text.")                

class PaymentReconciliationIdentifier(models.Model):    
    _name = "hc.payment.reconciliation.identifier"    
    _description = "Payment Reconciliation Identifier"        
    _inherit = ["hc.basic.association", "hc.identifier"]

    payment_reconciliation_id = fields.Many2one(
        comodel_name="hc.res.payment.reconciliation", 
        string="Payment Reconciliation", 
        help="Payment Reconciliation associated with this Payment Reconciliation Identifier.")                

class PaymentReconciliationStatusHistory(models.Model):     
    _name = "hc.payment.reconciliation.status.history"  
    _description = "Payment Reconciliation Status History"  
        
    payment_reconciliation_id = fields.Many2one(    
        comodel_name="hc.res.payment.reconciliation",
        string="Payment Reconciliation",
        help="Payment Reconciliation associated with this Payment Reconciliation Status History.")
    status = fields.Char(   
        string="Status",
        help="The status of the payment reconciliation.")
    start_date = fields.Datetime(   
        string="Start Date",
        help="Start of the period during which this payment reconciliation status is valid.")
    end_date = fields.Datetime( 
        string="End Date",
        help="End of the period during which this payment reconciliation status is valid.")
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

class PaymentType(models.Model):    
    _name = "hc.vs.payment.type"    
    _description = "Payment Type"       
    _inherit = ["hc.value.set.contains"]

