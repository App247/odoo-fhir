# -*- coding: utf-8 -*-

from openerp import models, fields, api

class Library(models.Model):    
    _name = "hc.res.library"    
    _description = "Library"  

    url = fields.Char(
        string="URI", 
        help="Logical URL to reference this library.")                    
    identifier_ids = fields.One2many(
        comodel_name="hc.library.identifier", 
        inverse_name="library_id", 
        string="Identifiers", 
        help="Logical identifier(s) for the library.")                    
    version = fields.Char(
        string="Version", 
        help="The version of the library, if any.")                    
    name = fields.Char(
        string="Name", 
        help="Name for this library (computer friendly).")                    
    title = fields.Char(
        string="Title", 
        help="Name for this library (human friendly).")                    
    status = fields.Selection(
        string="Status", 
        required="True", 
        selection=[
            ("draft", "Draft"), 
            ("active", "Active"), 
            ("inactive", "Inactive")], 
        help="The status of the library.")  
    is_experimental = fields.Boolean(
        string="Experimental", 
        help="If for testing purposes, not real usage.")    
    type = fields.Selection(
        string="Type", 
        required="True", 
        selection=[
            ("logic-library", "Logic Library"), 
            ("model-definition", "Model Definition"), 
            ("asset-collection", "Asset Collection"), 
            ("module-definition", "Module Definition")], 
        help="Identifies the type of library such as a Logic Library, Model Definition, Asset Collection, or Module Definition.")                    
    date = fields.Datetime(
        string="Date", 
        help="Date this was last changed.")
    publisher = fields.Char(
        string="Publisher", 
        help="Name of the publisher (organization or individual).")      
    description = fields.Text(
        string="Description", 
        help="Natural language description of the library.")                    
    purpose = fields.Text(
        string="Purpose", 
        help="Why this library is defined.")                    
    usage = fields.Text(
        string="Usage", 
        help="Describes the clinical usage of the library.")                    
    approval_date = fields.Date(
        string="Approval Date", 
        help="When library approved by publisher.")                    
    last_review_date = fields.Date(
        string="Last Review Date", 
        help="Last review date for the library.")                    
    effective_period_start_date = fields.Datetime(
        string="Effective Period Start Date", 
        help="Start of the period when the library is expected to be used.")                    
    effective_period_end_date = fields.Datetime(
        string="Effective Period End Date", 
        help="End of the period when the library is expected to be used.")                    
    use_context_ids = fields.One2many(
        comodel_name="hc.library.use.context", 
        inverse_name="library_id", 
        string="Use Contexts", 
        help="Context the content is intended to support.")                    
    jurisdiction_ids = fields.Many2many(
        comodel_name="hc.vs.jurisdiction", 
        relation="library_jurisdiction_rel", 
        string="Jurisdictions", 
        help="Intended jurisdiction for library (if applicable).")                    
    topic_ids = fields.Many2many(
        comodel_name="hc.vs.library.topic", 
        relation="library_topic_rel", 
        string="Topics", 
        help="E.g. Education, Treatment, Assessment, etc.")                    
    contributor_ids = fields.One2many(
        comodel_name="hc.library.contributor", 
        inverse_name="library_id", 
        string="Contributors", 
        help="A content contributor.")                                       
    contact_ids = fields.One2many(
        comodel_name="hc.library.contact", 
        inverse_name="library_id", 
        string="Contacts", 
        help="Contact details of the publisher.")                    
    copyright = fields.Text(
        string="Copyright", 
        help="Use and/or publishing restrictions.")                    
    related_artifact_ids = fields.One2many(
        comodel_name="hc.library.related.artifact", 
        inverse_name="library_id", 
        string="Related Artifacts", 
        help="Additional documentation, citations, etc.")                    
    parameter_ids = fields.One2many(
        comodel_name="hc.library.parameter", 
        inverse_name="library_id", 
        string="Parameters", 
        help="Parameters defined by the library.")                    
    data_requirement_ids = fields.One2many(
        comodel_name="hc.library.data.requirement", 
        inverse_name="library_id", 
        string="Data Requirements", 
        help="What data is referenced by this library.")                    
    content_ids = fields.One2many(
        comodel_name="hc.library.content", 
        inverse_name="library_id",
        string="Contents",  
        help="Contents of the library, either embedded or referenced.")                    

class LibraryIdentifier(models.Model):    
    _name = "hc.library.identifier"    
    _description = "Library Identifier"        
    _inherit = ["hc.basic.association", "hc.identifier"]    

    library_id = fields.Many2one(
        comodel_name="hc.res.library", 
        string="Library", 
        help="Library associated with this Library Identifier.")    

class LibraryUseContext(models.Model):    
    _name = "hc.library.use.context"    
    _description = "Library Use Context"        
    _inherit = ["hc.basic.association", "hc.usage.context"]    

    library_id = fields.Many2one(
        comodel_name="hc.res.library", 
        string="Library", 
        help="Library associated with this Library Use Context.")                    

class LibraryContributor(models.Model):    
    _name = "hc.library.contributor"    
    _description = "Library Contributor"        
    _inherit = ["hc.basic.association"]    
    _inherits = {"hc.contributor": "contributor_id"}

    contributor_id = fields.Many2one(
        comodel_name="hc.contributor", 
        string="Contributor", 
        ondelete="restrict", 
        required="True", 
        help="Contributor associated with this Library Contributor.")                    
    library_id = fields.Many2one(
        comodel_name="hc.res.library", 
        string="Library", 
        help="Library associated with this Library Contributor.")                    

class LibraryContact(models.Model):    
    _name = "hc.library.contact"    
    _description = "Library Contact"        
    _inherit = ["hc.basic.association"]    
    _inherits = {"hc.contact.detail": "contact_id"}

    contact_id = fields.Many2one(
        comodel_name="hc.contact.detail", 
        string="Contact Detail", 
        ondelete="restrict", 
        required="True", 
        help="Contact Detail associated with this Library Contact.")                    
    library_id = fields.Many2one(
        comodel_name="hc.res.library", 
        string="Library", 
        help="Library associated with this Library Contact.")                    

class LibraryRelatedArtifact(models.Model):    
    _name = "hc.library.related.artifact"    
    _description = "Library Related Artifact"        
    _inherit = ["hc.basic.association", "hc.related.artifact"]    

    library_id = fields.Many2one(
        comodel_name="hc.res.library", 
        string="Library", 
        help="Library associated with this Library Related Artifact.")                    

class LibraryParameter(models.Model):    
    _name = "hc.library.parameter"    
    _description = "Library Parameter"        
    _inherit = ["hc.basic.association", "hc.parameter.definition"]    

    library_id = fields.Many2one(
        comodel_name="hc.res.library", 
        string="Library", 
        help="Library associated with this Library Parameter.")                    

class LibraryDataRequirement(models.Model):    
    _name = "hc.library.data.requirement"    
    _description = "Library Data Requirement"        
    _inherit = ["hc.basic.association", "hc.data.requirement"]    

    library_id = fields.Many2one(
        comodel_name="hc.res.library", 
        string="Library", 
        help="Library associated with this Library Data Requirement.")                    

class LibraryContent(models.Model):    
    _name = "hc.library.content"    
    _description = "Library Content"        
    _inherit = ["hc.basic.association", "hc.attachment"]

    library_id = fields.Many2one(
        comodel_name="hc.res.library", 
        string="Library", 
        help="Library associated with this Library Content.")   

class LibraryTopic(models.Model):    
    _name = "hc.vs.library.topic"    
    _description = "Library Topic"        
    _inherit = ["hc.value.set.contains"]    
