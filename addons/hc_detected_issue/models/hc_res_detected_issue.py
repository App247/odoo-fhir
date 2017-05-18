# -*- coding: utf-8 -*-

from openerp import models, fields, api
from datetime import datetime
from openerp.tools import DEFAULT_SERVER_DATE_FORMAT as DF
from openerp.tools import DEFAULT_SERVER_DATETIME_FORMAT as DTF

class DetectedIssue(models.Model):
    _name = "hc.res.detected.issue"
    _description = "Detected Issue"

    name = fields.Char(
        string="Event Name", 
        compute="_compute_name", 
        store="True", 
        help="Text representation of the detected issue event. Patient + Detected Issue + Date.")
    identifier_id = fields.Many2one(
        comodel_name="hc.detected.issue.identifier", 
        string="Identifier", 
        help="Unique id for the detected issue.")
    status = fields.Selection(
        string="Status", 
        selection=[
            ("registered", "Registered"), 
            ("preliminary", "Preliminary"), 
            ("final", "Final"), 
            ("amended", "Amended")], 
        help="Indicates the status of the detected issue.")
    category_id = fields.Many2one(
        comodel_name="hc.vs.detected.issue.category", 
        string="Category",
        required="True", 
        help="Issue Category, e.g. drug-drug, duplicate therapy, etc.")
    severity = fields.Selection(
        string="Severity", 
        selection=[
            ("high", "High"), 
            ("moderate", "Moderate"), 
            ("low", "Low")], 
        help="Identifies the general type of issue identified.")
    patient_id = fields.Many2one(
        comodel_name="hc.res.patient", 
        string="Patient",
        required="True", 
        help="Associated patient.")
    date = fields.Datetime(
        string="Date",
        required="True",
        default=fields.datetime.now(), 
        help="When identified.")
    author_type = fields.Selection(
        string="Author Type", 
        selection=[
            ("practitioner", "Practitioner"), 
            ("device", "Device")], 
        help="Type of provider or device that identified the issue.")
    author_name = fields.Char(
        string="Author", 
        compute="_compute_author_name", 
        help="The provider or device that identified the issue.")
    author_practitioner_id = fields.Many2one(
        comodel_name="hc.res.practitioner", 
        string="Author Practitioner", 
        help="Practitioner that identified the issue.")
    author_device_id = fields.Many2one(
        comodel_name="hc.res.device", 
        string="Author Device", 
        help="Device that identified the issue.")
    implicated_ids = fields.One2many(
        comodel_name="hc.detected.issue.implicated", 
        inverse_name="detected_issue_id", 
        string="Implicated", 
        help="Problem resource.")
    detail = fields.Text(
        string="Detail", 
        help="Description and context.")
    reference = fields.Char(
        string="Reference URI", 
        help="Authority for issue.")
    mitigation_ids = fields.One2many(
        comodel_name="hc.detected.issue.mitigation", 
        inverse_name="detected_issue_id", 
        string="Mitigation", 
        help="taken to address.")

    @api.depends('patient_id', 'category_id', 'date')              
    def _compute_name(self):                
        comp_name = '/'         
        for hc_res_detected_issue in self:          
            if hc_res_detected_issue.patient_id:       
                comp_name = hc_res_detected_issue.patient_id.name  
                if hc_res_detected_issue.patient_id.birth_date:    
                    patient_birth_date = datetime.strftime(datetime.strptime(hc_res_detected_issue.patient_id.birth_date, DF), "%Y-%m-%d")
                    comp_name = comp_name + "("+ patient_birth_date + "),"
            if hc_res_detected_issue.category_id:       
                comp_name = comp_name + " " + hc_res_detected_issue.category_id.name + "," or ''  
            if hc_res_detected_issue.date:      
                patient_date = datetime.strftime(datetime.strptime(hc_res_detected_issue.date, DTF), "%Y-%m-%d")    
                comp_name = comp_name + " " + patient_date  
            hc_res_detected_issue.name = comp_name      

    @api.depends('author_type')         
    def _compute_author_name(self):         
        for hc_res_detected_issue in self:      
            if hc_res_detected_issue.author_type == 'practitioner': 
                hc_res_detected_issue.author_name = hc_res_detected_issue.author_practitioner_id.name
            elif hc_res_detected_issue.author_type == 'device': 
                hc_res_detected_issue.author_name = hc_res_detected_issue.author_device_id.name

class DetectedIssueMitigation(models.Model):
    _name = "hc.detected.issue.mitigation"
    _description = "Detected Issue Mitigation"

    detected_issue_id = fields.Many2one(
        comodel_name="hc.res.detected.issue", 
        string="Detected Issue", 
        help="Detected Issue associated with this Detected Issue Mitigation.")
    action_id = fields.Many2one(
        comodel_name="hc.vs.detected.issue.mitigation.action", 
        string="Action", 
        required="True", 
        help="What mitigation?")
    date = fields.Datetime(
        string="Date", 
        help="Date committed.")
    author_id = fields.Many2one(
        comodel_name="hc.res.practitioner", 
        string="Author", 
        help="Who is committing?")

class DetectedIssueImplicated(models.Model):
    _name = "hc.detected.issue.implicated"
    _description = "Detected Issue Implicated"

    detected_issue_id = fields.Many2one(
        comodel_name="hc.res.detected.issue", 
        string="Detected Issue", 
        help="Detected Issue associated with this Detected Issue Implicated.")
    implicated_type = fields.Char(
        string="Implicated Type", 
        compute="_compute_implicated_type", 
        store="True", 
        help="Type of resource representing the current activity or proposed activity that is potentially problematic.")
    implicated_name = fields.Reference(
        string="Implicated", 
        selection="_reference_models", 
        help="Problem resource.")

    @api.model          
    def _reference_models(self):            
        models = self.env['ir.model'].search([('state', '!=', 'manual')])       
        return [(model.model, model.name)       
            for model in models 
                if model.model.startswith('hc.res')]
                
    @api.depends('implicated_name')         
    def _compute_implicated_type(self):         
        for this in self:       
            if this.implicated_name:    
                this.implicated_type = this.implicated_name._description

class DetectedIssueIdentifier(models.Model):
    _name = "hc.detected.issue.identifier"
    _description = "Detected Issue Identifier"
    _inherit = ["hc.basic.association", "hc.identifier"]
    _rec_name="value"

class DetectedIssueCategory(models.Model):
    _name = "hc.vs.detected.issue.category"
    _description = "Detected Issue Category"
    _inherit = ["hc.value.set.contains"]

    name = fields.Char(
        string="Name", 
        help="Name of this detected issue category.")
    code = fields.Char(
        string="Code", 
        help="Code of this detected issue category.")
    contains_id = fields.Many2one(
        comodel_name="hc.vs.detected.issue.category", 
        string="Parent", 
        help="Parent detected issue category.")

class DetectedIssueMitigationAction(models.Model):
    _name = "hc.vs.detected.issue.mitigation.action"
    _description = "Detected Issue Mitigation Action"
    _inherit = ["hc.value.set.contains"]

    name = fields.Char(
        string="Name", 
        help="Name of this detected issue mitigation action.")
    code = fields.Char(
        string="Code", 
        help="Code of this detected issue mitigation action.")
    contains_id = fields.Many2one(
        comodel_name="hc.vs.detected.issue.mitigation.action", 
        string="Parent", 
        help="Parent detected issue mitigation action.")

class DetectedIssueImplicated(models.Model):
    _name = "hc.vs.detected.issue.implicated"
    _description = "Detected Issue Implicated"
    _inherit = ["hc.value.set.contains"]

    name = fields.Char(
        string="Name", 
        help="Name of this detected issue implicated.")
    code = fields.Char(
        string="Code", 
        help="Code of this detected issue implicated.")
    contains_id = fields.Many2one(
        comodel_name="hc.vs.detected.issue.implicated", 
        string="Parent", 
        help="Parent detected issue implicated.")

