# -*- coding: utf-8 -*-

from openerp import models, fields, api

class Basic(models.Model):    
    _name = "hc.res.basic"    
    _description = "Basic"        

    identifier_ids = fields.One2many(
        comodel_name="hc.basic.identifier", 
        inverse_name="basic_id", 
        string="Identifiers", 
        help="Business identifier.")                
    code_id = fields.Many2one(
        comodel_name="hc.vs.basic.resource.type", 
        string="Code", 
        required="True", 
        help="Kind of Resource.")                
    subject_type = fields.Char(
        string="Subject Type", 
        compute="_compute_subject_type", 
        store="True", 
        help='Type of resource instance that is the "focus" of this resource.')
    subject_name = fields.Reference(
        string="Subject", 
        selection="_reference_models", 
        help="Identifies the focus of this resource.")
    created = fields.Date(
        string="Basic Creation Date", 
        help="When created.")                
    author_type = fields.Selection(
        string="Author Type", 
        selection=[
            ("practitioner", "Practitioner"), 
            ("patient", "Patient"), 
            ("related_person", "Related Person")],
        help="Type of who created.")                
    author_name = fields.Char(
        string="Author", 
        compute="_compute_author_name", 
        store="True", 
        help="Who created.")                
    author_practitioner_id = fields.Many2one(
        comodel_name="hc.res.practitioner", 
        string="Author Practitioner", 
        help="Practitioner who created.")                
    author_patient_id = fields.Many2one(
        comodel_name="hc.res.patient", 
        string="Author Patient", 
        help="Patient who created.")                
    author_related_person_id = fields.Many2one(
        comodel_name="hc.res.related.person", 
        string="Author Related Person", 
        help="Related Person who created.")
    initiating_person_ids = fields.One2many(
        comodel_name="hc.basic.initiating.person", 
        inverse_name="basic_id", 
        string="Initiating Persons", 
        help="The person initiating the request.")
    receiving_person_ids = fields.One2many(
        comodel_name="hc.basic.receiving.person", 
        inverse_name="basic_id", 
        string="Receiving Persons", 
        help="The person in the receiving organization that will receive the response.")
                
    @api.model          
    def _reference_models(self):            
        models = self.env['ir.model'].search([('state', '!=', 'manual')])       
        return [(model.model, model.name)       
            for model in models 
                if model.model.startswith('hc.res')]
                
    @api.depends('subject_name')            
    def _compute_subject_type(self):            
        for this in self:       
            if this.subject_name:   
                this.subject_type = this.subject_name._description

    @api.depends('author_type')         
    def _compute_author_name(self):         
        for hc_res_basic in self:       
            if hc_res_basic.author_type == 'practitioner':  
                hc_res_basic.author_name = hc_res_basic.author_practitioner_id.name
            elif hc_res_basic.author_type == 'patient': 
                hc_res_basic.author_name = hc_res_basic.author_patient_id.name
            elif hc_res_basic.author_type == 'related_person':  
                hc_res_basic.author_name = hc_res_basic.author_related_person_id.name

class BasicIdentifier(models.Model):    
    _name = "hc.basic.identifier"    
    _description = "Basic Identifier"        
    _inherit = ["hc.basic.association", "hc.identifier"]
    
    basic_id = fields.Many2one(
        comodel_name="hc.res.basic", 
        string="Basic", 
        help="Basic associated with this Basic Identifier." )                


class BasicInitiatingPerson(models.Model):
    _name = "hc.basic.initiating.person"
    _description = "Basic Initiating Person"
    _inherit = ["hc.basic.association"]

    basic_id = fields.Many2one(
        comodel_name="hc.res.basic", 
        string="Basic", 
        help="Basic associated with this Basic Initiating Person." )                                
    initiating_person_type = fields.Selection(
        string="Initiating Person Type", 
        selection=[
            ("person", "Person"), 
            ("patient", "Patient"), 
            ("practitioner", "Practitioner"), 
            ("related_person", "Related Person")], 
        help="Type of person initiating the request.")                             
    initiating_person_name = fields.Char(
        string="Initiating Person", 
        compute="_compute_initiating_person_name", 
        store="True", 
        help="The person initiating the request.")                             
    initiating_person_id = fields.Many2one(
        comodel_name="hc.res.person", 
        string="Initiating Person", 
        help="Person initiating the request.")                             
    initiating_patient_id = fields.Many2one(
        comodel_name="hc.res.patient", 
        string="Initiating Patient", 
        help="Patient initiating the request.")                             
    initiating_practitioner_id = fields.Many2one(
        comodel_name="hc.res.practitioner", 
        string="Initiating Practitioner", 
        help="Practitioner initiating the request.")                             
    initiating_related_person_id = fields.Many2one(
        comodel_name="hc.res.related.person", 
        string="Initiating Related Person", 
        help="Related Person initiating the request.")                             

class BasicReceivingPerson(models.Model):
    _name = "hc.basic.receiving.person"
    _description = "Basic Receiving Person"
    _inherit = ["hc.basic.association"]

    basic_id = fields.Many2one(
        comodel_name="hc.res.basic", 
        string="Basic", 
        help="Basic associated with this Basic Receiving Person." )                             
    receiving_person_type = fields.Selection(
        string="Receiving Person Type", 
        selection=[
            ("person", "Person"), 
            ("patient", "Patient"), 
            ("practitioner", "Practitioner"), 
            ("related_person", "Related Person")], 
        help="Type of person in the receiving organization that will receive the response.")                             
    receiving_person_name = fields.Char(
        string="Receiving Person", 
        compute="_compute_receiving_person_name", 
        store="True", 
        help="The person in the receiving organization that will receive the respons.")                              
    receiving_person_id = fields.Many2one(
        comodel_name="hc.res.person", 
        string="Receiving Person", 
        help="Person in the receiving organization that will receive the response.")                             
    receiving_patient_id = fields.Many2one(
        comodel_name="hc.res.patient", 
        string="Receiving Patient", 
        help="Patient in the receiving organization that will receive the response.")                             
    receiving_practitioner_id = fields.Many2one(
        comodel_name="hc.res.practitioner", 
        string="Receiving Practitioner", 
        help="Practitioner in the receiving organization that will receive the response.")                             
    receiving_related_person_id = fields.Many2one(
        comodel_name="hc.res.related.person", 
        string="Receiving Related Person", 
        help="Related Person in the receiving organization that will receive the response.")                             

class BasicResourceType(models.Model):    
    _name = "hc.vs.basic.resource.type"    
    _description = "Basic Resource Type"        
    _inherit = ["hc.value.set.contains"]

    name = fields.Char(
        string="Name", 
        help="Name of this basic resource type.")
    code = fields.Char(
        string="Code", 
        help="Code of this basic resource type.")
    contains_id = fields.Many2one(
        comodel_name="hc.vs.basic.resource.type", 
        string="Parent", 
        help="Parent basic resource type.")

