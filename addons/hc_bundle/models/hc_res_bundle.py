# -*- coding: utf-8 -*-

from openerp import models, fields, api

class Bundle(models.Model):    
    _name = "hc.res.bundle"    
    _description = "Bundle"
    _inherit = ["hc.resource"]        
    
    name = fields.Char(
        string="Name", 
        # compute="_compute_name", 
        # store="True", 
        help="Text representation of the bundle.")
    identifier_id = fields.Many2one(
        comodel_name="hc.bundle.identifier", 
        string="Bundle Identifier", 
        help="Persistent identifier for the bundle.")
    type = fields.Selection(
        string="Bundle Type", 
        required="True", 
        selection=[
            ("document", "Document"), 
            ("message", "Message"), 
            ("transaction", "Transaction"), 
            ("transaction-response", "Transaction Response"),
            ("batch", "Batch"), 
            ("batch-response", "Batch Response"), 
            ("history", "History"), 
            ("searchset", "Search Set"), 
            ("collection", "Collection")], 
        help="Indicates the purpose of a bundle - how it was intended to be used.")                
    total = fields.Integer(
        string="Total", 
        help="If search, the total number of matches.")                
    signature_id = fields.Many2one(
        comodel_name="hc.bundle.signature", 
        string="Signature", 
        help="Digital Signature.")                
    link_ids = fields.One2many(
        comodel_name="hc.bundle.link", 
        inverse_name="bundle_id", 
        string="Links", 
        help="Links related to this Bundle.")                
    entry_ids = fields.One2many(
        comodel_name="hc.bundle.entry", 
        inverse_name="bundle_id", 
        string="Entries", 
        help="Entry in the bundle - will have a resource, or information.")                

class BundleLink(models.Model):    
    _name = "hc.bundle.link"    
    _description = "Bundle Link"        

    bundle_id = fields.Many2one(
        comodel_name="hc.res.bundle", 
        string="Bundle", 
        help="Bundle associated with this Bundle Link.")                
    entry_id = fields.Many2one(
        comodel_name="hc.bundle.entry", 
        string="Entry", 
        help="Entry associated with this Bundle Link.")                
    relation = fields.Char(
        string="Relation", 
        required="True", 
        help="See http://www.iana.org/assignments/link-relations/link-relations.xhtml#link-relations-1.")                
    url = fields.Char(
        string="URI", 
        required="True", 
        help="URL of reference details for the link.")                

class BundleEntry(models.Model):    
    _name = "hc.bundle.entry"    
    _description = "Bundle Entry"        

    bundle_id = fields.Many2one(
        comodel_name="hc.res.bundle", 
        string="Bundle", 
        help="Bundle associated with this Bundle Entry.")                
    full_url = fields.Char(
        string="Full URI", 
        help="Absolute URL for resource (server address, or UUID/OID).")                
    resource_id = fields.Many2one(
        comodel_name="hc.bundle.entry.resource", 
        string="Resource", 
        help="A resource in the bundle.")                
    link_ids = fields.One2many(
        comodel_name="hc.bundle.link", 
        inverse_name="entry_id", 
        string="Links", 
        help="Links related to this Bundle.")                
    search_ids = fields.One2many(
        comodel_name="hc.bundle.entry.search", 
        inverse_name="entry_id", 
        string="Searches", 
        help="Search related information.")                
    request_ids = fields.One2many(
        comodel_name="hc.bundle.entry.request", 
        inverse_name="entry_id", 
        string="Requests", 
        help="Transaction Related Information.")                
    response_ids = fields.One2many(
        comodel_name="hc.bundle.entry.response", 
        inverse_name="entry_id", 
        string="Responses", 
        help="Transaction Related Information.")                

class BundleEntrySearch(models.Model):    
    _name = "hc.bundle.entry.search"    
    _description = "Bundle Entry Search"        

    entry_id = fields.Many2one(
        comodel_name="hc.bundle.entry", 
        string="Entry", 
        help="Entry associated with this Bundle Entry Search.")                
    mode = fields.Selection(
        string="Search Mode", 
        selection=[
            ("match", "Match"), 
            ("include", "Include"),
            ("outcome", "Outcome")], 
        help="Why an entry is in the result set.")                
    score = fields.Float(
        string="Score", 
        help="Search ranking (between 0 and 1).")                

class BundleEntryRequest(models.Model):    
    _name = "hc.bundle.entry.request"    
    _description = "Bundle Entry Request"        

    entry_id = fields.Many2one(
        comodel_name="hc.bundle.entry", 
        string="Entry", 
        help="Entry associated with this Bundle Entry Request.")                
    method = fields.Selection(
        string="Request Method", 
        required="True", 
        selection=[
            ("get", "GET"), 
            ("post", "POST"), 
            ("put", "PUT"), 
            ("delete", "DELETE")], 
        help="HTTP verbs (in the HTTP command line).")                
    url = fields.Char(
        string="URI", 
        required="True", 
        help="The URL for the transaction.")                
    if_none_match = fields.Char(
        string="If None Match", 
        help="For managing cache currency.")                
    if_modified_since = fields.Datetime(
        string="If Modified Since Date", 
        help="For managing update contention.")                
    if_match = fields.Char(
        string="If Match", 
        help="For managing update contention.")                
    if_none_exist = fields.Char(
        string="If None Exist", 
        help="For conditional creates.")                

class BundleEntryResponse(models.Model):    
    _name = "hc.bundle.entry.response"    
    _description = "Bundle Entry Response"        

    entry_id = fields.Many2one(
        comodel_name="hc.bundle.entry", 
        string="Entry", 
        help="Entry in the bundle - will have a resource, or information.")                
    status = fields.Char(
        string="Status", 
        required="True", 
        help="Status response code (text optional).")                
    location = fields.Char(
        string="Location URI", 
        help="URL of the location, if the operation returns a location.")                
    etag = fields.Char(
        string="eTag", 
        help="The eTag for the resource (if relevant).")                
    last_modified = fields.Datetime(
        string="Last Modified Date", 
        help="Server's date time modified.")
    outcome_id = fields.Many2one(
        comodel_name="hc.bundle.response.outcome", 
        string="Outcome", 
        help="OperationOutcome with hints and warnings (for batch/transaction).")
                
class BundleIdentifier(models.Model):
    _name = "hc.bundle.identifier"
    _description = "Bundle Identifier"
    _inherit = ["hc.basic.association", "hc.identifier"]

class BundleSignature(models.Model):    
    _name = "hc.bundle.signature"
    _description = "Bundle Signature"
    _inherit = ["hc.basic.association", "hc.signature"]

class BundleEntryResource(models.Model):    
    _name = "hc.bundle.entry.resource"    
    _description = "Bundle Entry Resource"        
    _inherit = ["hc.basic.association", "hc.resource"]

class BundleResponseOutcome(models.Model):
    _name = "hc.bundle.response.outcome"
    _description = "Bundle Response Outcome"
    _inherit = ["hc.basic.association", "hc.resource"]

