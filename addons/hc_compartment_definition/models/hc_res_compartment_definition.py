# -*- coding: utf-8 -*-

from openerp import models, fields, api
from datetime import datetime
from openerp.tools import DEFAULT_SERVER_DATETIME_FORMAT as DTF

class CompartmentDefinition(models.Model):    
    _name = "hc.res.compartment.definition"    
    _description = "Compartment Definition"
    _rec_name = "title"                

    url = fields.Char(
        string="URI", 
        required="True", 
        help="Absolute URL used to reference this compartment definition.")
    name = fields.Char(
        string="Name", 
        required="True", 
        help="Informal name for this compartment definition.")                       
    title = fields.Char(
        string="Title", 
        help="Name for this compartment definition (Human friendly).")                        
    status_id = fields.Many2one(
        comodel_name="hc.vs.publication.status",
        string="Status",
        required="True",
        help="The status of this message definition. Enables tracking the life-cycle of the content.")
    status_history_ids = fields.One2many(   
        comodel_name="hc.compartment.definition.status.history",
        inverse_name="compartment_definition_id",
        string="Status History",
        help="The status of the compartment definition over time.")                       
    is_experimental = fields.Boolean(
        string="Experimental", 
        help="If for testing purposes, not real usage.")
    publisher = fields.Char(
        string="Publisher", 
        help="Name of the publisher (Organization or individual).")                  
    contact_ids = fields.One2many(
        comodel_name="hc.compartment.definition.contact", 
        inverse_name="compartment_definition_id", 
        string="Contacts", 
        help="Contact details for the publisher.")                        
    date = fields.Datetime(
        string="Date", 
        help="Publication Date(/time).")                        
    description = fields.Text(
        string="Description", 
        help="Natural language description of the CompartmentDefinition.")   
    purpose = fields.Text(
        string="Purpose", 
        help="Why this compartment definition is defined.")                  
    use_context_ids = fields.One2many(
        comodel_name="hc.compartment.definition.use.context", 
        inverse_name="compartment_definition_id", 
        string="Use Contexts", 
        help="Content intends to support these contexts.")                        
    jurisdiction_ids = fields.Many2many(
        comodel_name="hc.vs.jurisdiction", 
        relation="compartment_definition_jurisdiction_rel", 
        string="Jurisdictions", 
        help="Intended jurisdiction for compartment definition (if applicable).")                        
    code = fields.Selection(
        string="Code", 
        required="True", 
        selection=[
            ("patient", "Patient"), 
            ("encounter", "Encounter"), 
            ("related person", "Related Person"), 
            ("practitioner", "Practitioner"), 
            ("Device", "Device")], 
        help="Which compartment this definition describes.")                        
    is_search = fields.Boolean(
        string="Search", 
        required="True", 
        help="Whether the search syntax is supported.")                        
    resource_ids = fields.One2many(
        comodel_name="hc.compartment.definition.resource", 
        inverse_name="compartment_definition_id", 
        string="Software", 
        help="How resource is related to the compartment.")                        

    @api.model                          
    def create(self, vals):                         
        status_history_obj = self.env['hc.compartment.definition.status.history']                       
        res = super(CompartmentDefinition, self).create(vals)                       
        if vals and vals.get('status_id'):                      
            status_history_vals = {                 
                'compartment_definition_id': res.id,                
                'status' : res.status_id.name,                                              
                'start_date': datetime.today()              
                }               
            status_history_obj.create(status_history_vals)                  
        return res                      
                                
    @api.multi                          
    def write(self, vals):                          
        status_history_obj = self.env['hc.compartment.definition.status.history']                       
        publication_status_obj = self.env['hc.vs.publication.status']                       
        res = super(CompartmentDefinition, self).write(vals)                        
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
                publication_status = publication_status_obj.browse(vals.get('status_id'))               
                status_history_vals = {             
                    'compartment_definition_id': self.id,           
                    'status': publication_status.name,          
                    'start_date': datetime.today()          
                    }           
                status_history_obj.create(status_history_vals)              
        return res                      

class CompartmentDefinitionResource(models.Model):    
    _name = "hc.compartment.definition.resource"    
    _description = "Compartment Definition Resource"                

    compartment_definition_id = fields.Many2one(
        comodel_name="hc.res.compartment.definition", 
        string="Compartment Definition", 
        help="Compartment Definition associated with this Compartment Definition Resource.")                        
    code_id = fields.Many2one(
        comodel_name="hc.vs.resource.type", 
        string="Code", 
        required="True", 
        help="Name of resource type.")                        
    param_ids = fields.One2many(
        comodel_name="hc.compartment.definition.resource.param", 
        inverse_name="resource_id", 
        string="Params", 
        help="Search Parameter Name, or chained params.")                        
    documentation = fields.Text(
        string="Documentation", 
        help="Additional documentation about the resource and compartment.")

class CompartmentDefinitionStatusHistory(models.Model):     
    _name = "hc.compartment.definition.status.history"  
    _description = "Compartment Definition Status History"  
        
    compartment_definition_id = fields.Many2one(    
        comodel_name="hc.res.compartment.definition",
        string="Compartment Definition",
        help="Compartment Definition associated with this Compartment Definition Status History.")
    status = fields.Char(   
        string="Status",
        help="The status of the compartment definition.")
    start_date = fields.Datetime(   
        string="Start Date",
        help="Start of the period during which this compartment definition status is valid.")
    end_date = fields.Datetime( 
        string="End Date",
        help="End of the period during which this compartment definition status is valid.")
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

class CompartmentDefinitionContact(models.Model):    
    _name = "hc.compartment.definition.contact"    
    _description = "Compartment Definition Contact"            
    _inherit = ["hc.basic.association"]    
    _inherits = {"hc.contact.detail": "contact_id"}

    contact_id = fields.Many2one(
        comodel_name="hc.contact.detail", 
        string="Contact", 
        ondelete="restrict", 
        required="True", help="Contact Detail associated with this Compartment Definition Contact.")                        
    compartment_definition_id = fields.Many2one(
        comodel_name="hc.res.compartment.definition", 
        string="Compartment Definition", 
        help="Compartment Definition associated with this Compartment Definition Contact.")                        

class CompartmentDefinitionUseContext(models.Model):    
    _name = "hc.compartment.definition.use.context"    
    _description = "Compartment Definition Use Context"            
    _inherit = ["hc.basic.association", "hc.usage.context"]    

    compartment_definition_id = fields.Many2one(
        comodel_name="hc.res.compartment.definition", 
        string="Compartment Definition", 
        help="Compartment Definition associated with this Compartment Definition Use Context.")                        

class CompartmentDefinitionResourceParam(models.Model):    
    _name = "hc.compartment.definition.resource.param"    
    _description = "Compartment Definition Resource Param"            
    _inherit = ["hc.basic.association"]    

    resource_id = fields.Many2one(
        comodel_name="hc.compartment.definition.resource", 
        string="Resource", 
        help="Resource associated with this Compartment Definition Resource Param.")                        
    param = fields.Char(
        string="Param", 
        help="Param associated with this Compartment Definition Resource Param.")                        
