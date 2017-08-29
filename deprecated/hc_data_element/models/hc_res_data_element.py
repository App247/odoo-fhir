# -*- coding: utf-8 -*-

from openerp import models, fields, api

class DataElement(models.Model):    
    _name = "hc.res.data.element"    
    _description = "Data Element"    
    _rec_name = "title"            

    url = fields.Char(
        string="URI", 
        help="Globally unique logical id for data element.")                        
    identifier_id = fields.Many2one(
        comodel_name="hc.data.element.identifier", 
        string="Identifier", 
        help="Logical id to reference this data element.")                        
    version = fields.Char(
        string="Version", 
        help="Logical id for this version of the data element.")                        
    status = fields.Selection(
        string="Status", 
        required="True", 
        selection=[
            ("draft", "Draft"), 
            ("active", "Active"), 
            ("retired", "Retired")], 
        help="The status of this data element. Enables tracking the life-cycle of the content.")                        
    is_experimental = fields.Boolean(
        string="Experimental", 
        help="If for testing purposes, not real usage.")                        
    publisher = fields.Char(
        string="Publisher", 
        help="Name of the publisher (Organization or individual).")                        
    date = fields.Datetime(
        string="Date", 
        help="Date for this version of the data element.")                        
    name = fields.Text(
        string="Name", 
        help="Descriptive label for this element definition.")                        
    title = fields.Char(
        string="Title", 
        help="Name for this data element (Human friendly).")                        
    contact_ids = fields.One2many(
        comodel_name="hc.data.element.contact", 
        inverse_name="data_element_id", 
        string="Contacts", 
        help="Contact details for the publisher.")                        
    use_context_ids = fields.One2many(
        comodel_name="hc.data.element.use.context", 
        inverse_name="data_element_id", 
        string="Use Contexts", 
        help="Content intends to support these contexts.")                        
    jurisdiction_ids = fields.Many2many(
        comodel_name="hc.vs.jurisdiction", 
        relation="data_element_jurisdiction_rel", 
        string="Jurisdictions", 
        help="Intended jurisdiction for data element (if applicable).")                        
    copyright = fields.Text(
        string="Copyright", 
        help="Use and/or Publishing restrictions.")                        
    stringency = fields.Selection(
        string="Stringency", 
        selection=[
            ("comparable", "Comparable"), 
            ("fully-specified", "Fully Specified"), 
            ("equivalent", "Equivalent"), 
            ("convertable", "Convertable"), 
            ("scaleable", "Scaleable"), 
            ("flexible", "Flexible")], 
        help="Identifies how precise the data element is in its definition.")                        
    element_ids = fields.One2many(
        comodel_name="hc.data.element.element", 
        inverse_name="data_element_id", 
        string="Elements", 
        required="True", 
        help="Definition of element.")                        
    mapping_ids = fields.One2many(
        comodel_name="hc.data.element.mapping", 
        inverse_name="data_element_id", 
        string="Mappings", 
        help="External specification mapped to.")                        

class DataElementMapping(models.Model):    
    _name = "hc.data.element.mapping"    
    _description = "Data Element Mapping"                

    data_element_id = fields.Many2one(
        comodel_name="hc.res.data.element", 
        string="Data Element", 
        help="Data Element associated with this Data Element Mapping.")                        
    identity = fields.Char(
        string="Identity", 
        required="True", 
        help="Internal id when this mapping is used.")                        
    uri = fields.Char(
        string="URI", 
        help="Identifies what this mapping refers to.")                        
    name = fields.Char(
        string="Name", 
        help="Names what this mapping refers to.")                        
    comment = fields.Text(
        string="Comment", 
        help="Versions, Issues, Scope limitations etc.")                        

class DataElementIdentifier(models.Model):    
    _name = "hc.data.element.identifier"    
    _description = "Data Element Identifier"            
    _inherit = ["hc.basic.association", "hc.identifier"]    

class DataElementContact(models.Model):    
    _name = "hc.data.element.contact"    
    _description = "Data Element Contact"            
    _inherit = ["hc.basic.association"]    
    _inherits = {"hc.contact.detail": "contact_id"}

    contact_id = fields.Many2one(
        comodel_name="hc.contact.detail", 
        string="Contact", 
        ondelete="restrict", 
        required="True", 
        help="Contact Detail associated with this Data Element Contact.")                        
    data_element_id = fields.Many2one(
        comodel_name="hc.res.data.element", 
        string="Data Element", 
        help="Data Element associated with this Data Element Contact.")                        

class DataElementUseContext(models.Model):    
    _name = "hc.data.element.use.context"    
    _description = "Data Element Use Context"            
    _inherit = ["hc.basic.association", "hc.usage.context"]    

    data_element_id = fields.Many2one(
        comodel_name="hc.res.data.element", 
        string="Data Element", 
        help="Data Element associated with this Data Element Use Context.")                        

class DataElementElement(models.Model):    
    _name = "hc.data.element.element"    
    _description = "Data Element Element"            
    _inherit = ["hc.basic.association", "hc.element.definition"]    

    data_element_id = fields.Many2one(
        comodel_name="hc.res.data.element", 
        string="Data Element", 
        help="Data Element associated with this Data Element Element.")
