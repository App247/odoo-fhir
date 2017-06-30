# -*- coding: utf-8 -*-

from openerp import models, fields, api

# -*- coding: utf-8 -*-

from openerp import models, fields, api

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
    created = fields.Datetime(
        string="Enrollment Response Creation Date", 
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

class EnrollmentResponseIdentifier(models.Model):    
    _name = "hc.enrollment.response.identifier"    
    _description = "Enrollment Response Identifier"        
    _inherit = ["hc.basic.association", "hc.identifier"]

    enrollment_response_id = fields.Many2one(
        comodel_name="hc.res.enrollment.response", 
        string="Enrollment Response", 
        help="Enrollment Response associated with this Enrollment Response Identifier.")    