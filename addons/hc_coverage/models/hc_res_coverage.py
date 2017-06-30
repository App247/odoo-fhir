# -*- coding: utf-8 -*-

from openerp import models, fields, api
from datetime import datetime
from openerp.tools import DEFAULT_SERVER_DATETIME_FORMAT as DTF

class Coverage(models.Model):
    _name = "hc.res.coverage"
    _description = "Coverage"

    name = fields.Char(
        string="Name", 
        compute="_compute_name", 
        store="True", 
        help="Text representation of the coverage. Network + Policy Holder + Subscriber + Beneficiary + Type + Start Date.")
    identifier_ids = fields.One2many(
        comodel_name="hc.coverage.identifier", 
        inverse_name="coverage_id", 
        string="Identifiers", 
        help="The primary coverage ID.")
    status_id = fields.Many2one(
        comodel_name="hc.vs.fm.status", 
        string="Status", 
        help="Indicates whether the account is presently used/useable or not.")
    status_history_ids = fields.One2many(   
        comodel_name="hc.coverage.status.history",
        inverse_name="coverage_id",
        string="Status History",
        help="The status of the coverage over time.")
    type_id = fields.Many2one(
        comodel_name="hc.vs.coverage.type", 
        string="Type", 
        required="True", 
        help="Type of coverage.")
    policy_holder_type = fields.Selection(
        string="Policy Holder Type", 
        required="True", 
        selection=[
            ("patient", "Patient"), 
            ("related_person", "Related Person"), 
            ("organization", "Organization")], 
        help="Type of owner of the policy.")
    policy_holder_name = fields.Char(
        string="Policy Holder", 
        compute="_compute_policy_holder_name", 
        store="True", 
        help="Owner of the policy.")
    policy_holder_patient_id = fields.Many2one(
        comodel_name="hc.res.patient", 
        string ="Policy Holder Patient", 
        help="Patient owner of the policy.")
    policy_holder_related_person_id = fields.Many2one(
        comodel_name="hc.res.related.person", 
        string="Policy Holder Related Person", 
        help="Related Person owner of the policy.")
    policy_holder_organization_id = fields.Many2one(
        comodel_name="hc.res.organization", 
        string="Policy Holder Organization", 
        help="Organization owner of the policy.")
    subscriber_type = fields.Selection(
        string="Subscriber Type", 
        required="True", 
        selection=[
            ("patient", "Patient"), 
            ("related_person", "Related Person")], 
            help="Type of owner of the policy.")
    subscriber_name = fields.Char(
        string="Subscriber", 
        compute="_compute_subscriber_name", 
        store="True", 
        help="Subscriber to the polic.")
    subscriber_patient_id = fields.Many2one(
        comodel_name="hc.res.patient", 
        string="Subscriber Patient", 
        help="Patient subscriber to the policy.")
    subscriber_related_person_id = fields.Many2one(
        comodel_name="hc.res.related.person", 
        string="Subscriber Related Person", 
        help="Related Person subscriber to the policy.")
    subscriber_id = fields.Char(
        string="Subscriber Id", 
        help="ID assigned to the Subscriber.")
    beneficiary_id = fields.Many2one(
        comodel_name="hc.res.patient", 
        string="Beneficiary", 
        required="True", 
        help="Plan Beneficiary.")
    relationship_id = fields.Many2one(
        comodel_name="hc.vs.policyholder.relationship", 
        string="Relationship", 
        help="Beneficiary relationship to the Subscriber.")
    start_date = fields.Datetime(
        string="Start Date", 
        required="True", 
        help="Start of the coverage.")
    end_date = fields.Datetime(
        string="End Date", 
        required="True", 
        help="End of the coverage.")
    payor_type = fields.Selection(
        string="Payor Type", 
        selection=[
            ("organization", "Organization"), 
            ("patient", "Patient"), 
            ("related_person", "Related Person")], 
        help="Type of identifier for the plan or agreement issuer.")
    payor_name = fields.Char(
        string="Payor", 
        compute="_compute_payor_name", 
        store="True", 
        help="Identifier for the plan or agreement issue.")
    payor_organization_id = fields.Many2one(
        comodel_name="hc.res.organization", 
        string="Payor Organization", 
        help="Organization identifier for the plan or agreement issuer.")
    payor_patient_id = fields.Many2one(
        comodel_name="hc.res.patient", 
        string="Payor Patient", 
        help="Patient identifier for the plan or agreement issuer.")
    payor_related_person_id = fields.Many2one(
        comodel_name="hc.res.related.person", 
        string="Payor Related Person", 
        help="Related Person identifier for the plan or agreement issuer.")
    dependent = fields.Integer(
        string="Dependent", 
        help="The dependent number.")
    sequence = fields.Integer(
        string="Sequence", 
        help="The plan instance or sequence counter.")
    order = fields.Integer(
        string="Order", 
        help="Relative order of the coverage.")
    network_id = fields.Many2one(
        comodel_name="hc.res.organization", 
        string="Network", 
        required="True", 
        help="Insurer network.")
    contract_ids = fields.One2many(
        comodel_name="hc.coverage.contract", 
        inverse_name="coverage_id", 
        string="Contracts", 
        help="Contract details.")
    grouping_id = fields.Many2one(
        comodel_name="hc.coverage.grouping", 
        string="Grouping", 
        help="Grouping associated with this Coverage Resource.")

    @api.depends('network_id', 'policy_holder_name', 'subscriber_name','beneficiary_id','type_id','start_date')         
    def _compute_name(self):            
        comp_name = '/'     
        for hc_coverage in self:        
            if hc_coverage.network_id:  
                comp_name = hc_coverage.network_id.name or ''
            if hc_coverage.policy_holder_name:  
                comp_name = comp_name + ", " + hc_coverage.policy_holder_name or ''
            if hc_coverage.subscriber_name: 
                comp_name = comp_name + ", " + hc_coverage.subscriber_name or ''
            if hc_coverage.beneficiary_id:  
                comp_name = comp_name + ", " + hc_coverage.beneficiary_id.name or ''
            if hc_coverage.type_id: 
                comp_name = comp_name + ", " + hc_coverage.type_id.name or ''
            if hc_coverage.start_date:  
                comp_name = comp_name + ", " + datetime.strftime(datetime.strptime(hc_coverage.start_date, DTF), "%Y-%m-%d")
            hc_coverage.name = comp_name    

    @api.model                          
    def create(self, vals):                         
        status_history_obj = self.env['hc.coverage.status.history']                     
        res = super(Coverage, self).create(vals)                        
        if vals and vals.get('status_id'):                      
            status_history_vals = {                 
                'coverage_id': res.id,              
                'status': res.status_id.name,              
                'start_date': datetime.today()              
                }               
            if vals.get('status_id') == 'entered-in-error':                 
                status_history_vals.update({'end_date': datetime.today()})              
            status_history_obj.create(status_history_vals)                  
        return res                      
                                
    @api.multi                          
    def write(self, vals):                          
        status_history_obj = self.env['hc.coverage.status.history']                     
        fm_status_obj = self.env['hc.vs.fm.status']                     
        res = super(Coverage, self).write(vals)                     
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
                    'coverage_id': self.id,         
                    'status': fm_status.name,           
                    'start_date': datetime.today()          
                    }           
                if vals.get('status_id') == 'entered-in-error':             
                    status_id_history_vals.update({'end_date': datetime.today()})           
                status_history_obj.create(status_history_vals)              
        return res                      
                     
    @api.depends('policy_holder_type')          
    def _compute_policy_holder_name(self):          
        for hc_res_coverage in self:        
            if hc_res_coverage.policy_holder_type == 'patient': 
                hc_res_coverage.policy_holder_name = hc_res_coverage.policy_holder_patient_id.name
            elif hc_res_coverage.policy_holder_type == 'related_person':    
                hc_res_coverage.policy_holder_name = hc_res_coverage.policy_holder_related_person_id.name
            elif hc_res_coverage.policy_holder_type == 'organization':  
                hc_res_coverage.policy_holder_name = hc_res_coverage.policy_holder_organization_id.name

class coverage_grouping(models.Model):
    _name = "hc.coverage.grouping"
    _description = "coverage_grouping"

    name = fields.Char(
        string="Name", 
        compute="_compute_name", 
        store="True", 
        help="Text representation of the grouping. Group + Plan + Class.")     
    group = fields.Char(
        string="Group", 
        required="True", 
        help="An identifier for the group.")        
    group_display = fields.Char(
        string="Group Display", 
        help="Display text for an identifier for the group.")       
    sub_group = fields.Char(
        string="Sub Group", 
        help="An identifier for the subsection of the group.")      
    sub_group_display = fields.Char(
        string="Sub Group Display", 
        help="Display text for the subsection of the group.")       
    plan = fields.Char(
        string="Plan", 
        required="True", 
        help="An identifier for the plan.")       
    plan_display = fields.Char(
        string="Plan Display", 
        help="Display text for the plan.")        
    sub_plan = fields.Char(
        string="Sub Plan", 
        help="An identifier for the subsection of the plan.")     
    sub_plan_display = fields.Char(
        string="Sub Plan Display", 
        help="Display text for the subsection of the plan.")      
    coverage_class = fields.Char(
        string="Class", 
        required="True", 
        help="An identifier for the class.")        
    class_display = fields.Char(
        string="Class Display", 
        help="Display text for the class.")     
    sub_class = fields.Char(
        string="Sub Class", 
        help="An identifier for the subsection of the class.")      
    sub_class_display = fields.Char(
        string="Sub Class Display", 
        help="Display text for the subsection of the subclass.")        

    @api.depends('group', 'plan', 'coverage_class')             
    def _compute_name(self):                
        comp_name = '/'         
        for hc_coverage_grouping in self:           
            if hc_coverage_grouping.group:      
                comp_name = hc_coverage_grouping.group or ''   
            if hc_coverage_grouping.plan:       
                comp_name = comp_name + ", " + hc_coverage_grouping.plan or '' 
            if hc_coverage_grouping.coverage_class:     
                comp_name = comp_name + ", " + hc_coverage_grouping.coverage_class or ''   
            hc_coverage_grouping.name = comp_name       

class CoverageIdentifier(models.Model):
    _name = "hc.coverage.identifier"
    _description = "Coverage Identifier"
    _inherit = ["hc.basic.association", "hc.identifier"]

    coverage_id = fields.Many2one(
        comodel_name="hc.res.coverage", 
        string="Coverage", 
        help="Coverage associated with this Coverage Identifier.")

class CoverageStatusHistory(models.Model):      
    _name = "hc.coverage.status.history"    
    _description = "Coverage Status History"    
        
    coverage_id = fields.Many2one(  
        comodel_name="hc.res.coverage",
        string="Coverage",
        help="Coverage associated with this Coverage Status History.")
    status = fields.Char(   
        string="Status",
        help="The status of the coverage.")
    start_date = fields.Datetime(   
        string="Start Date",
        help="Start of the period during which this coverage status is valid.")
    end_date = fields.Datetime( 
        string="End Date",
        help="End of the period during which this coverage status is valid.")
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

class CoverageContract(models.Model):
    _name = "hc.coverage.contract"
    _description = "Coverage Contract"
    _inherit = ["hc.basic.association"]

    coverage_id = fields.Many2one(
        comodel_name="hc.res.coverage", 
        string="Coverage", 
        help="Coverage associated with this Coverage Contract.")
    # contract_id = fields.Many2one(
    #     comodel_name="hc.res.contract", 
    #     string="Contract", 
    #     help="Contract associated with this Coverage Contract.")

class CoverageNetwork(models.Model):    
    _name = "hc.coverage.network"   
    _description = "Coverage Network"       
    _inherit = ["hc.basic.association"]

    coverage_id = fields.Many2one(
        comodel_name="hc.res.coverage", 
        string="Coverage",
        help="Coverage associated with this Coverage Network.")
    organization_id = fields.Many2one(
        comodel_name="hc.res.organization", 
        string="Organization", 
        help="Organization associated with this Coverage Network.")             

class CoverageType(models.Model):
    _name = "hc.vs.coverage.type"
    _description = "Coverage Type"
    _inherit = ["hc.value.set.contains"]

    name = fields.Char(
        string="Name", 
        help="Name of this coverage type.")                               
    code = fields.Char(
        string="Code", 
        help="Code of this coverage type.")                               
    contains_id = fields.Many2one(
        comodel_name="hc.vs.coverage.type", 
        string="Parent", 
        help="Parent coverage type.")                                

class PolicyholderRelationship(models.Model):
    _name = "hc.vs.policyholder.relationship"
    _description = "Policyholder Relationship"
    _inherit = ["hc.value.set.contains"]

    name = fields.Char(
        string="Name", 
        help="Name of this policyholder relationship.")                               
    code = fields.Char(
        string="Code", 
        help="Code of this policyholder relationship.")                               
    contains_id = fields.Many2one(
        comodel_name="hc.vs.policyholder.relationship", 
        string="Parent", 
        help="Parent policyholder relationship.")                                

