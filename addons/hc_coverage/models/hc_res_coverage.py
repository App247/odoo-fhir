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
    status = fields.Selection(
        string="Coverage Status", 
        selection=[
            ("active", "Active"), 
            ("cancelled", "Cancelled"), 
            ("draft", "Draft"), 
            ("entered-in-error", "Entered-In-Error")], 
        help="Indicates whether the account is presently used/useable or not.")
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

