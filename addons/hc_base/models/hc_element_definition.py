# -*- coding: utf-8 -*-

from openerp import models, fields, api

class ElementDefinition(models.Model):    
    _name = "hc.element.definition"    
    _description = "Element Definition"    
    _rec_name = "path"            

    path = fields.Char(
        string="Path", 
        required="True", 
        help="Path of the element in the heirarchy of elements.")                        
    representation_ids = fields.One2many(
        comodel_name="hc.element.definition.representation", 
        inverse_name="element_definition_id", 
        string="Representations", 
        help="Codes that define how this element is represented in instances, when the deviation varies from the normal case.")                        
    slice_name = fields.Char(
        string="Slice Name", 
        help="Name for this particular element (in a set of slices).")                        
    identifier = fields.Char(
        string="Identifier",
        help="Identifier.")  
    label = fields.Char(
        string="Label",
        help="Name for element to display with or prompt for element.")                        
    code_ids = fields.Many2many(
        comodel_name="hc.vs.element.definition.code", 
        relation="element_definition_code_rel", 
        string="Codes", 
        help="Defining code.")                        
    short = fields.Char(
        string="Short", 
        help="Concise definition for xml presentation.")                        
    definition = fields.Text(
        string="Definition", 
        help="Full formal definition as narrative text.")                        
    comment = fields.Text(
        string="Comment", 
        help="Comments about the use of this element.")                        
    xml_sample = fields.Text(
        string="XML Sample", 
        help="Sample XML code that implements this element.") 
    requirements = fields.Text(
        string="Requirements", 
        help="Why this resource has been created.")                        
    alias_ids = fields.One2many(
        comodel_name="hc.element.definition.alias", 
        inverse_name="element_definition_id", 
        string="Aliases", 
        help="Other names.")          
    min = fields.Integer(
        string="Min", 
        help="Minimum Cardinality.")                        
    max = fields.Char(
        string="Max", 
        help="Maximum Cardinality (a number or *).")                        
    content_reference = fields.Char(
        string="Content Reference URI", 
        help="Reference to definition of content for the element.")                        
    default_value_type = fields.Selection(
        string="Default Value Type", 
        selection=[
            ("integer", "Integer"), 
            ("decimal", "Decimal"),
            ("date_time", "Date Time"),
            ("date", "Date"),
            ("instant", "Instant"),
            ("string", "String"),
            ("uri", "URI"), 
            ("boolean", "Boolean"),
            ("code", "Code"),
            ("markdown", "Markdown"),
            ("base_64_binary", "Base 64 Binary"),
            ("coding", "Coding"),
            ("codeable_concept", "Codeable Concept"), 
            ("attachment", "Attachment"),
            ("identifier", "Identifier"),
            ("quantity", "Quantity"),
            ("range", "Range"),
            ("period", "Period"),
            ("ratio", "Ratio"), 
            ("human_name", "Human Name"),
            ("address", "Address"),
            ("contact_point", "Contact Point"),
            ("timing", "Timing"),
            ("signature", "Signature"),
            ("reference", "Reference"),
            ("time", "Time"), 
            ("oid", "OID"), 
            ("id", "ID"), 
            ("unsigned_int", "Unsigned Integer"), 
            ("positive_int", "Positive Integer"), 
            ("annotation", "Annotation"), 
            ("sampled_data", "Sampled Data"), 
            ("meta", "Meta")],
        help="Type of specified value if missing from instance.")                        
    default_value_name = fields.Char(
        string="Default Value", 
        compute="_compute_default_value_name", 
        store="True", 
        help="Specified value if missing from instance.")                        
    default_value_integer = fields.Integer(
        string="Default Value Integer", 
        help="Integer value if missing from instance.")
    default_value_decimal = fields.Float(
        string="Default Value Decimal", 
        help="Decimal value if missing from instance.")
    default_value_date_time = fields.Datetime(
        string="Default Value Date Time", 
        help="Date Time value if missing from instance.")
    default_value_date = fields.Date(
        string="Default Value Date", 
        help="Date value if missing from instance.")
    default_value_instant = fields.Datetime(
        string="Default Value Instant", 
        help="Instant value if missing from instance.")
    default_value_string = fields.Char(
        string="Default Value String", 
        help="String value if missing from instance.")
    default_value_uri = fields.Char(
        string="Default Value URI", 
        help="URI value if missing from instance.")
    default_value_boolean = fields.Boolean(
        string="Default Value Boolean", 
        help="Boolean value if missing from instance.")
    default_value_code_id = fields.Many2one(
        comodel_name="hc.vs.element.definition.code", 
        string="Default Value Code", 
        help="Code value if missing from instance.")
    default_value_markdown = fields.Text(
        string="Default Value Markdown", 
        help="Markdown value if missing from instance.")
    default_value_base_64_binary = fields.Binary(
        string="Default Value Base 64 Binary", 
        help="Base 64 Binary value if missing from instance.")
    default_value_coding_id = fields.Many2one(
        comodel_name="hc.vs.element.definition.code", 
        string="Default Value Coding", 
        help="Coding value if missing from instance.")
    default_value_codeable_concept_id = fields.Many2one(
        comodel_name="hc.vs.element.definition.code", 
        string="Default Value Codeable Concept", 
        help="Codeable Concept value if missing from instance.")
    default_value_attachment_id = fields.Many2one(
        comodel_name="hc.element.definition.attachment", 
        string="Default Value Attachment", 
        help="Attachment value if missing from instance.")
    default_value_identifier_id = fields.Many2one(
        comodel_name="hc.element.definition.identifier", 
        string="Default Value Identifier", 
        help="Identifier value if missing from instance.")
    default_value_quantity = fields.Float(
        string="Default Value Quantity", 
        help="Quantity value if missing from instance.")
    default_value_quantity_uom_id = fields.Many2one(
        comodel_name="product.uom", 
        string="Default Value Quantity UOM", 
        help="Quantity unit of measure.")
    default_value_range = fields.Char(
        string="Default Value Range", 
        help="Range value if missing from instance.")
    default_value_period = fields.Char(
        string="Default Value Period", 
        help="Period value if missing from instance.")
    default_value_period_uom_id = fields.Many2one(
        comodel_name="product.uom", 
        string="Default Value Period UOM", 
        help="Period unit of measure.")
    default_value_ratio = fields.Float(
        string="Default Value Ratio",  
        help="Ratio of value if missing from instance.")
    default_value_human_name_id = fields.Many2one(
        comodel_name="hc.element.definition.human.name", 
        string="Default Value Human Name", 
        help="Human Name value if missing from instance.")
    default_value_address_id = fields.Many2one(
        comodel_name="hc.element.definition.address", 
        string="Default Value Address", 
        help="Address value if missing from instance.")
    default_value_contact_point_id = fields.Many2one(
        comodel_name="hc.element.definition.telecom", 
        string="Default Value Contact Point", 
        help="Contact Point value if missing from instance.")
    default_value_timing_id = fields.Many2one(
        comodel_name="hc.element.definition.timing", 
        string="Default Value Timing", 
        help="Timing value if missing from instance.")
    default_value_signature_id = fields.Many2one(
        comodel_name="hc.element.definition.signature", 
        string="Default Value Signature", 
        help="Signature value if missing from instance.")
    default_value_reference_id = fields.Many2one(
        comodel_name="hc.element.definition.reference", 
        string="Default Value Reference", 
        help="Reference value if missing from instance.")
    default_value_time = fields.Float(
        string="Default Value Time", 
        help="Time value if missing from instance.")
    default_value_oid = fields.Char(
        string="Default Value OID", 
        help="OID value if missing from instance.")
    default_value_id = fields.Char(
        string="Default Value ID", 
        help="ID value if missing from instance.")
    default_value_unsigned_int = fields.Integer(
        string="Default Value Unsigned Integer", 
        help="Unsigned Integer value if missing from instance.")
    default_value_positive_int = fields.Integer(
        string="Default Value Positive Integer", 
        help="Positive Integer value if missing from instance.")
    default_value_annotation_id = fields.Many2one(
        comodel_name="hc.element.definition.annotation", 
        string="Default Value Annotation", 
        help="Annotation value if missing from instance.")
    default_value_sampled_data_id = fields.Many2one(
        comodel_name="hc.element.definition.sampled.data", 
        string="Default Value Sampled Data", 
        help="Sampled Data value if missing from instance.")
    default_value_meta_id = fields.Many2one(
        comodel_name="hc.element.definition.meta", 
        string="Default Value Meta", 
        help="Meta value if missing from instance.")
    meaning_when_missing = fields.Text(
        string="Meaning When Missing", 
        help="Implicit meaning when this element is missing.")
    order_meaning = fields.Text(
        string="Order Meaning", 
        help="What the order of the elements means.")                            
    fixed_type = fields.Selection(
        string="Fixed Type",
        selection=[
            ("integer", "Integer"), 
            ("decimal", "Decimal"),
            ("date_time", "Date Time"),
            ("date", "Date"),
            ("instant", "Instant"),
            ("string", "String"),
            ("uri", "URI"), 
            ("boolean", "Boolean"),
            ("code", "Code"),
            ("markdown", "Markdown"),
            ("base_64_binary", "Base 64 Binary"),
            ("coding", "Coding"),
            ("codeable_concept", "Codeable Concept"), 
            ("attachment", "Attachment"),
            ("identifier", "Identifier"),
            ("quantity", "Quantity"),
            ("range", "Range"),
            ("period", "Period"),
            ("ratio", "Ratio"), 
            ("human_name", "Human Name"),
            ("address", "Address"),
            ("contact_point", "Contact Point"),
            ("timing", "Timing"),
            ("signature", "Signature"),
            ("reference", "Reference"),
            ("time", "Time"), 
            ("oid", "OID"), 
            ("id", "ID"), 
            ("unsigned_int", "Unsigned Integer"), 
            ("positive_int", "Positive Integer"), 
            ("annotation", "Annotation"), 
            ("sampled_data", "Sampled Data"), 
            ("meta", "Meta")],
        help="Type of value must be exactly this.")                        
    fixed_name = fields.Char(
        string="Fixed", 
        compute="_compute_fixed_name", 
        store="True", 
        help="Value must be exactly this.")
    fixed_integer = fields.Integer(
        string="Fixed Integer", 
        help="Integer value must be exactly this.")
    fixed_decimal = fields.Float(
        string="Fixed Decimal", 
        help="Decimal value must be exactly this.")
    fixed_date_time = fields.Datetime(
        string="Fixed Date Time", 
        help="Date Time value must be exactly this.")
    fixed_date = fields.Date(
        string="Fixed Date", 
        help="Date value must be exactly this.")
    fixed_instant = fields.Datetime(
        string="Fixed Instant", 
        help="Instant value must be exactly this.")
    fixed_string = fields.Char(
        string="Fixed String", 
        help="String value must be exactly this.")
    fixed_uri = fields.Char(
        string="Fixed URI", 
        help="URI value must be exactly this.")
    fixed_boolean = fields.Boolean(
        string="Fixed Boolean", 
        help="Boolean value must be exactly this.")
    fixed_code_id = fields.Many2one(
        comodel_name="hc.vs.element.definition.code",
        string="Fixed Code", 
        help="Code value must be exactly this.")
    fixed_markdown = fields.Text(
        string="Fixed Markdown", 
        help="Markdown value must be exactly this.")
    fixed_base_64_binary = fields.Binary(
        string="Fixed Base 64 Binary", 
        help="Base 64 Binary value must be exactly this.")
    fixed_coding_id = fields.Many2one(
        comodel_name="hc.vs.element.definition.code", 
        string="Fixed Coding", 
        help="Coding value must be exactly this.")
    fixed_codeable_concept_id = fields.Many2one(
        comodel_name="hc.vs.element.definition.code", 
        string="Fixed Codeable Concept", 
        help="Codeable Concept value must be exactly this.")
    fixed_attachment_id = fields.Many2one(
        comodel_name="hc.element.definition.attachment", 
        string="Fixed Attachment", 
        help="Attachment value must be exactly this.")
    fixed_identifier_id = fields.Many2one(
        comodel_name="hc.element.definition.identifier", 
        string="Fixed Identifier", 
        help="Identifier value must be exactly this.")
    fixed_quantity = fields.Float(
        string="Fixed Quantity", 
        help="Quantity value must be exactly this.")
    fixed_quantity_uom_id = fields.Many2one(
        comodel_name="product.uom", 
        string="Fixed Quantity UOM", 
        help="Quantity unit of measure.")
    fixed_range = fields.Char(
        string="Fixed Range", 
        help="Range value must be exactly this.")
    fixed_period = fields.Char(
        string="Fixed Period", 
        help="Period value must be exactly this.")
    fixed_period_uom_id = fields.Many2one(
        comodel_name="product.uom", 
        string="Fixed Period UOM", 
        help="Period unit of measure.")
    fixed_ratio = fields.Float(
        string="Fixed Ratio", 
        help="Ratio of value must be exactly this.")
    fixed_human_name_id = fields.Many2one(
        comodel_name="hc.element.definition.human.name", 
        string="Fixed Human Name", 
        help="Human Name value must be exactly this.")
    fixed_address_id = fields.Many2one(
        comodel_name="hc.element.definition.address", 
        string="Fixed Address", 
        help="Address value must be exactly this.")
    fixed_contact_point_id = fields.Many2one(
        comodel_name="hc.element.definition.telecom", 
        string="Fixed Contact Point", 
        help="Contact Point value must be exactly this.")
    fixed_timing_id = fields.Many2one(
        comodel_name="hc.element.definition.timing", 
        string="Fixed Timing", 
        help="Timing value must be exactly this.")
    fixed_signature_id = fields.Many2one(
        comodel_name="hc.element.definition.signature", 
        string="Fixed Signature", 
        help="Signature value must be exactly this.")
    fixed_reference_id = fields.Many2one(
        comodel_name="hc.element.definition.reference", 
        string="Fixed Reference", 
        help="Reference value must be exactly this.")
    fixed_time = fields.Float(
        string="Fixed Time", 
        help="Time value must be exactly this.")
    fixed_oid = fields.Char(
        string="Fixed OID", 
        help="OID value must be exactly this.")
    fixed_id = fields.Char(
        string="Fixed ID", 
        help="ID value must be exactly this.")
    fixed_unsigned_int = fields.Integer(
        string="Fixed Unsigned Integer", 
        help="Unsigned Integer value must be exactly this.")
    fixed_positive_int = fields.Integer(
        string="Fixed Positive Integer", 
        help="Positive Integer value must be exactly this.")
    fixed_annotation_id = fields.Many2one(
        comodel_name="hc.element.definition.annotation", 
        string="Fixed Annotation", 
        help="Annotation value must be exactly this.")
    fixed_sampled_data_id = fields.Many2one(
        comodel_name="hc.element.definition.sampled.data", 
        string="Fixed Sampled Data", 
        help="Sampled Data value must be exactly this.")
    fixed_meta_id = fields.Many2one(
        comodel_name="hc.element.definition.meta", 
        string="Fixed Meta", 
        help="Meta value must be exactly this.")        
    pattern_type = fields.Selection(
        string="Pattern Type", 
        selection=[
            ("integer", "Integer"), 
            ("decimal", "Decimal"),
            ("date_time", "Date Time"),
            ("date", "Date"),
            ("instant", "Instant"),
            ("string", "String"),
            ("uri", "URI"), 
            ("boolean", "Boolean"),
            ("code", "Code"),
            ("markdown", "Markdown"),
            ("base_64_binary", "Base 64 Binary"),
            ("coding", "Coding"),
            ("codeable_concept", "Codeable Concept"), 
            ("attachment", "Attachment"),
            ("identifier", "Identifier"),
            ("quantity", "Quantity"),
            ("range", "Range"),
            ("period", "Period"),
            ("ratio", "Ratio"), 
            ("human_name", "Human Name"),
            ("address", "Address"),
            ("contact_point", "Contact Point"),
            ("timing", "Timing"),
            ("signature", "Signature"),
            ("reference", "Reference"),
            ("time", "Time"), 
            ("oid", "OID"), 
            ("id", "ID"), 
            ("unsigned_int", "Unsigned Integer"), 
            ("positive_int", "Positive Integer"), 
            ("annotation", "Annotation"), 
            ("sampled_data", "Sampled Data"), 
            ("meta", "Meta")],
        help="Type of value must have at least these property values.")                        
    pattern_name = fields.Char(
        string="Pattern", 
        compute="_compute_pattern_name", 
        store="True", 
        help="Value must have at least these property values.")
    pattern_integer = fields.Integer(
        string="Pattern Integer", 
        help="Integer value must have at least these property values.")
    pattern_decimal = fields.Float(
        string="Pattern Decimal", 
        help="Decimal value must have at least these property values.")
    pattern_date_time = fields.Datetime(
        string="Pattern Date Time", 
        help="Date Time value must have at least these property values.")
    pattern_date = fields.Date(
        string="Pattern Date", 
        help="Date value must have at least these property values.")
    pattern_instant = fields.Datetime(
        string="Pattern Instant", 
        help="Instant value must have at least these property values.")
    pattern_string = fields.Char(
        string="Pattern String", 
        help="String value must have at least these property values.")
    pattern_uri = fields.Char(
        string="Pattern URI", 
        help="URI value must have at least these property values.")
    pattern_boolean = fields.Boolean(
        string="Pattern Boolean", 
        help="Boolean value must have at least these property values.")
    pattern_code_id = fields.Many2one(
        comodel_name="hc.vs.element.definition.code", 
        string="Pattern Code", 
        help="Code value must have at least these property values.")
    pattern_markdown = fields.Text(
        string="Pattern Markdown", 
        help="Markdown value must have at least these property values.")
    pattern_base_64_binary = fields.Binary(
        string="Pattern Base 64 Binary", 
        help="Base 64 Binary value must have at least these property values.")
    pattern_coding_id = fields.Many2one(
        comodel_name="hc.vs.element.definition.code", 
        string="Pattern Coding", 
        help="Coding value must have at least these property values.")
    pattern_codeable_concept_id = fields.Many2one(
        comodel_name="hc.vs.element.definition.code", 
        string="Pattern Codeable Concept", 
        help="Codeable Concept value must have at least these property values.")
    pattern_attachment_id = fields.Many2one(
        comodel_name="hc.element.definition.attachment", 
        string="Pattern Attachment", 
        help="Attachment value must have at least these property values.")
    pattern_identifier_id = fields.Many2one(
        comodel_name="hc.element.definition.identifier", 
        string="Pattern Identifier", 
        help="Identifier value must have at least these property values.")
    pattern_quantity = fields.Float(
        string="Pattern Quantity", 
        help="Quantity value must have at least these property values.")
    pattern_quantity_uom_id = fields.Many2one(
        comodel_name="product.uom", 
        string="Pattern Quantity UOM", 
        help="Quantity unit of measure.")
    pattern_range = fields.Char(
        string="Pattern Range", 
        help="Range value must have at least these property values.")
    pattern_period = fields.Char(
        string="Pattern Period", 
        help="Period value must have at least these property values.")
    pattern_period_uom_id = fields.Many2one(
        comodel_name="product.uom", 
        string="Pattern Period UOM", 
        help="Period unit of measure.")
    pattern_ratio = fields.Float(
        string="Pattern Ratio", 
        help="Ratio of value must have at least these property values.")
    pattern_human_name_id = fields.Many2one(
        comodel_name="hc.element.definition.human.name", 
        string="Pattern Human Name", 
        help="Human Name value must have at least these property values.")
    pattern_address_id = fields.Many2one(
        comodel_name="hc.element.definition.address", 
        string="Pattern Address", 
        help="Address value must have at least these property values.")
    pattern_contact_point_id = fields.Many2one(
        comodel_name="hc.element.definition.telecom", 
        string="Pattern Contact Point", 
        help="Contact Point value must have at least these property values.")
    pattern_timing_id = fields.Many2one(
        comodel_name="hc.element.definition.timing", 
        string="Pattern Timing", 
        help="Timing value must have at least these property values.")
    pattern_signature_id = fields.Many2one(
        comodel_name="hc.element.definition.signature", 
        string="Pattern Signature", 
        help="Signature value must have at least these property values.")
    pattern_reference_id = fields.Many2one(
        comodel_name="hc.element.definition.reference", 
        string="Pattern Reference", 
        help="Reference value must have at least these property values.")
    pattern_time = fields.Float(
        string="Pattern Time", 
        help="Time value must have at least these property values.")
    pattern_oid = fields.Char(
        string="Pattern OID", 
        help="OID value must have at least these property values.")
    pattern_id = fields.Char(
        string="Pattern ID", 
        help="ID value must have at least these property values.")
    pattern_unsigned_int = fields.Integer(
        string="Pattern Unsigned Integer", 
        help="Unsigned Integer value must have at least these property values.")
    pattern_positive_int = fields.Integer(
        string="Pattern Positive Integer", 
        help="Positive Integer value must have at least these property values.")
    pattern_annotation_id = fields.Many2one(
        comodel_name="hc.element.definition.annotation", 
        string="Pattern Annotation", 
        help="Annotation value must have at least these property values.")
    pattern_sampled_data_id = fields.Many2one(
        comodel_name="hc.element.definition.sampled.data", 
        string="Pattern Sampled Data", 
        help="Sampled Data value must have at least these property values.")
    pattern_meta_id = fields.Many2one(
        comodel_name="hc.element.definition.meta", 
        string="Pattern Meta", 
        help="Meta value must have at least these property values.")                        

    @api.depends('min_value_type')              
    def _compute_min_value_name(self):              
        for hc_element_definition in self:          
            if hc_element_definition.min_value_type == 'date':      
                hc_element_definition.min_value_name = str(hc_element_definition.min_value_date)    
            elif hc_element_definition.min_value_type == 'date_time':      
                hc_element_definition.min_value_name = str(hc_element_definition.min_value_date_time) 
            elif hc_element_definition.min_value_type == 'instant':      
                hc_element_definition.min_value_name = str(hc_element_definition.min_value_instant) 
            elif hc_element_definition.min_value_type == 'decimal':      
                hc_element_definition.min_value_name = str(hc_element_definition.min_value_decimal) 
            elif hc_element_definition.min_value_type == 'integer':      
                hc_element_definition.min_value_name = str(hc_element_definition.min_value_integer) 
            elif hc_element_definition.min_value_type == 'positive_int':      
                hc_element_definition.min_value_name = str(hc_element_definition.min_value_positive_int) 
            elif hc_element_definition.min_value_type == 'unsigned_int':      
                hc_element_definition.min_value_name = str(hc_element_definition.min_value_unsigned_int) 
            elif hc_element_definition.min_value_type == 'quantity':      
                hc_element_definition.min_value_name = str(hc_element_definition.min_value_quantity) 

    min_value_type = fields.Selection(
        string="Minimum Value Type", 
        selection=[
            ("date", "Date"), 
            ("date_time", "Date Time"),
            ("instant", "Instant"),
            ("decimal", "Decimal"),
            ("integer", "Integer"),
            ("positive_int", "Positive Integer"),
            ("unsigned_int", "Unsigned Integer"),
            ("quantity", "Quantity")],
        help="Type of Minimum Allowed Value (for some types).")
    min_value_name = fields.Char(
        string="Minimum Value", 
        compute="_compute_min_value_name", 
        store="True", 
        help="Minimum Allowed Value (for some types).")                        
    min_value_date = fields.Date(
        string="Minimum Value Date", 
        help="Date Minimum Allowed Value (for some types).")
    min_value_date_time = fields.Datetime(
        string="Minimum Value Date Time", 
        help="Date Time Minimum Allowed Value (for some types).")
    min_value_instant = fields.Float(
        string="Minimum Value Instant", 
        help="Instant Minimum Allowed Value (for some types).")    
    min_value_decimal = fields.Float(
        string="Minimum Value Decimal", 
        help="Decimal Minimum Allowed Value (for some types).")   
    min_value_integer = fields.Integer(
        string="Minimum Value Integer", 
        help="Integer Minimum Allowed Value (for some types).")
    min_value_positive_int = fields.Integer(
        string="Minimum Value Positive Integer", 
        help="Positive Integer Minimum Allowed Value (for some types).") 
    min_value_unsigned_int = fields.Integer(
        string="Minimum Value Unsigned Integer", 
        help="Unsigned Integer Minimum Allowed Value (for some types).")
    min_value_quantity = fields.Float(
        string="Minimum Value Quantity", 
        help="Quantity Minimum Allowed Value (for some types).")                                               
    max_length = fields.Integer(
        string="Maximum Length", 
        help="Maximum Length for strings.")                        
    
    @api.depends('max_value_type')              
    def _compute_max_value_name(self):              
        for hc_element_definition in self:          
            if hc_element_definition.max_value_type == 'date':      
                hc_element_definition.max_value_name = str(hc_element_definition.max_value_date)    
            elif hc_element_definition.max_value_type == 'date_time':      
                hc_element_definition.max_value_name = str(hc_element_definition.max_value_date_time) 
            elif hc_element_definition.max_value_type == 'instant':      
                hc_element_definition.max_value_name = str(hc_element_definition.max_value_instant) 
            elif hc_element_definition.max_value_type == 'decimal':      
                hc_element_definition.max_value_name = str(hc_element_definition.max_value_decimal) 
            elif hc_element_definition.max_value_type == 'integer':      
                hc_element_definition.max_value_name = str(hc_element_definition.max_value_integer) 
            elif hc_element_definition.max_value_type == 'positive_int':      
                hc_element_definition.max_value_name = str(hc_element_definition.max_value_positive_int) 
            elif hc_element_definition.max_value_type == 'unsigned_int':      
                hc_element_definition.max_value_name = str(hc_element_definition.max_value_unsigned_int) 
            elif hc_element_definition.max_value_type == 'quantity':      
                hc_element_definition.max_value_name = str(hc_element_definition.max_value_quantity)

    max_value_type = fields.Selection(
        string="Maximum Value Type", 
        selection=[
            ("date", "Date"), 
            ("date_time", "Date Time"),
            ("instant", "Instant"),
            ("decimal", "Decimal"),
            ("integer", "Integer"),
            ("positive_int", "Positive Integer"),
            ("unsigned_int", "Unsigned Integer"),
            ("quantity", "Quantity")],
        help="Type of Maximum Allowed Value (for some types).")
    max_value_name = fields.Char(
        string="Maximum Value", 
        compute="_compute_max_value_name", 
        store="True", 
        help="Maximum Allowed Value (for some types).")                        
    max_value_date = fields.Date(
        string="Maximum Value Date", 
        help="Date Maximum Allowed Value (for some types).")
    max_value_date_time = fields.Datetime(
        string="Maximum Value Date Time", 
        help="Date Time Maximum Allowed Value (for some types).")
    max_value_instant = fields.Float(
        string="Maximum Value Instant", 
        help="Instant Maximum Allowed Value (for some types).")    
    max_value_decimal = fields.Float(
        string="Maximum Value Decimal", 
        help="Decimal Maximum Allowed Value (for some types).")   
    max_value_integer = fields.Integer(
        string="Maximum Value Integer", 
        help="Integer Maximum Allowed Value (for some types).")
    max_value_positive_int = fields.Integer(
        string="Maximum Value Positive Integer", 
        help="Positive Integer Maximum Allowed Value (for some types).") 
    max_value_unsigned_int = fields.Integer(
        string="Maximum Value Unsigned Integer", 
        help="Unsigned Integer Maximum Allowed Value (for some types).")
    max_value_quantity = fields.Float(
        string="Maximum Value Quantity", 
        help="Quantity Maximum Allowed Value (for some types).")
    condition_ids = fields.One2many(
        comodel_name="hc.element.definition.condition", 
        inverse_name="element_definition_id", 
        string="Conditions", 
        help="Reference to invariant about presence.")                        
    is_must_support = fields.Boolean(
        string="Must Support", 
        help="If the element must supported.")                        
    is_modifier = fields.Boolean(
        string="Modifier", 
        help="If this modifies the meaning of other elements.")                        
    is_summary = fields.Boolean(
        string="Summary", 
        help="Include when _summary = true?.")                        
    slicing_id = fields.Many2one(
        comodel_name="hc.element.definition.slicing",  
        string="Slicing", 
        help="This element is sliced - slices follow.")                        
    base_id = fields.Many2one(
        comodel_name="hc.element.definition.base", 
        string="Base", 
        help="Base definition information for tools.")                        
    type_ids = fields.One2many(
        comodel_name="hc.element.definition.type", 
        inverse_name="element_definition_id", 
        string="Types", 
        help="Data type and Profile for this element.")                        
    example_ids = fields.One2many(
        comodel_name="hc.element.definition.example", 
        inverse_name="element_definition_id", 
        string="Examples", 
        help="Example value (as defined for type).")                        
    constraint_ids = fields.One2many(
        comodel_name="hc.element.definition.constraint", 
        inverse_name="element_definition_id", 
        string="Constraints", 
        help="Condition that must evaluate to true.")                        
    binding_id = fields.Many2one(
        comodel_name="hc.element.definition.binding", 
        string="Binding", 
        help="ValueSet details if this is coded.")                        
    mapping_ids = fields.One2many(
        comodel_name="hc.element.definition.mapping", 
        inverse_name="element_definition_id", 
        string="Mappings", 
        help="Map element to another set of definitions.")
    extension_ids = fields.One2many(
        comodel_name="hc.element.definition.extension",
        inverse_name="element_definition_id", 
        string="Extensions", 
        help="Additional valid requirement.")                        
         
    @api.depends('default_value_type')              
    def _compute_default_value_name(self):              
        for hc_element_definition in self:
            if hc_element_definition.default_value_type == 'integer':       
                hc_element_definition.default_value_name = str(hc_element_definition.default_value_integer)
            elif hc_element_definition.default_value_type == 'decimal':   
                hc_element_definition.default_value_name = str(hc_element_definition.default_value_decimal)
            elif hc_element_definition.default_value_type == 'date_time':  
                hc_element_definition.default_value_type = str(hc_element_definition.default_value_date_time)
            elif hc_element_definition.default_value_type == 'date':      
                hc_element_definition.default_value_name = str(hc_element_definition.default_value_date)
            elif hc_element_definition.default_value_type == 'instant':   
                hc_element_definition.default_value_name = str(hc_element_definition.default_value_instant)
            elif hc_element_definition.default_value_type == 'string':      
                hc_element_definition.default_value_name = hc_element_definition.default_value_string
            elif hc_element_definition.default_value_type == 'uri': 
                hc_element_definition.default_value_name = hc_element_definition.default_value_uri
            elif hc_element_definition.default_value_type == 'boolean': 
                hc_element_definition.default_value_name = hc_element_definition.default_value_boolean
            elif hc_element_definition.default_value_type == 'code':    
                hc_element_definition.default_value_name = hc_element_definition.default_value_code_id.name
            elif hc_element_definition.default_value_type == 'markdown':    
                hc_element_definition.default_value_name = hc_element_definition.default_value_markdown
            elif hc_element_definition.default_value_type == 'coding':    
                hc_element_definition.default_value_name = hc_element_definition.default_value_coding_id.name
            elif hc_element_definition.default_value_type == 'codeable_concept':  
                hc_element_definition.default_value_name = hc_element_definition.default_value_codeable_concept_id.name
            elif hc_element_definition.default_value_type == 'attachment':    
                hc_element_definition.default_value_name = hc_element_definition.default_value_attachment_id.name
            elif hc_element_definition.default_value_type == 'identifier':    
                hc_element_definition.default_value_name = hc_element_definition.default_value_identifier_id.name
            elif hc_element_definition.default_value_type == 'quantity':
                hc_element_definition.default_value_name = str(hc_element_definition.default_value_quantity)
            elif hc_element_definition.default_value_type == 'range':
                hc_element_definition.default_value_name = hc_element_definition.default_value_range
            elif hc_element_definition.default_value_type == 'period':
                hc_element_definition.default_value_name = hc_element_definition.default_value_period
            elif hc_element_definition.default_value_type == 'ratio':
                hc_element_definition.default_value_name = str(hc_element_definition.default_value_ratio)
            elif hc_element_definition.default_value_type == 'human_name':    
                hc_element_definition.default_value_name = hc_element_definition.default_value_human_name_id.name
            elif hc_element_definition.default_value_type == 'address':   
                hc_element_definition.default_value_name = hc_element_definition.default_value_address_id.name   
            elif hc_element_definition.default_value_type == 'contact_point':  
                hc_element_definition.default_value_name = hc_element_definition.default_value_contact_point_id.name
            elif hc_element_definition.default_value_type == 'timing':   
                hc_element_definition.default_value_name = hc_element_definition.default_value_timing_id.name
            elif hc_element_definition.default_value_type == 'signature':    
                hc_element_definition.default_value_name = hc_element_definition.default_value_signature_id.name
            elif hc_element_definition.default_value_type == 'reference':    
                hc_element_definition.default_value_name = hc_element_definition.default_value_reference_id.name
            elif hc_element_definition.default_value_type == 'time':   
                hc_element_definition.default_value_type = str(hc_element_definition.default_value_time)                
            elif hc_element_definition.default_value_type == 'oid': 
                hc_element_definition.default_value_name = hc_element_definition.default_value_oid
            elif hc_element_definition.default_value_type == 'id':  
                hc_element_definition.default_value_name = hc_element_definition.default_value_id
            elif hc_element_definition.default_value_type == 'unsigned_int':   
                hc_element_definition.default_value_type = str(hc_element_definition.default_value_unsigned_int)                 
            elif hc_element_definition.default_value_type == 'positive_int':   
                hc_element_definition.default_value_type = str(hc_element_definition.default_value_positive_int)                
            elif hc_element_definition.default_value_type == 'annotation':  
                hc_element_definition.default_value_name = hc_element_definition.default_value_annotation_id.name
            elif hc_element_definition.default_value_type == 'sampled_data':    
                hc_element_definition.default_value_name = hc_element_definition.default_value_sampled_data_id.name
            elif hc_element_definition.default_value_type == 'meta':    
                hc_element_definition.default_value_name = hc_element_definition.default_value_meta_id.name

    @api.depends('fixed_type')              
    def _compute_fixed_name(self):              
        for hc_element_definition in self:
            if hc_element_definition.fixed_type == 'integer':       
                hc_element_definition.fixed_name = str(hc_element_definition.fixed_integer)
            elif hc_element_definition.fixed_type == 'decimal':   
                hc_element_definition.fixed_name = str(hc_element_definition.fixed_decimal)
            elif hc_element_definition.fixed_type == 'date_time':  
                hc_element_definition.fixed_type = str(hc_element_definition.fixed_date_time)
            elif hc_element_definition.fixed_type == 'date':      
                hc_element_definition.fixed_name = str(hc_element_definition.fixed_date)
            elif hc_element_definition.fixed_type == 'instant':   
                hc_element_definition.fixed_name = str(hc_element_definition.fixed_instant)
            elif hc_element_definition.fixed_type == 'string':      
                hc_element_definition.fixed_name = hc_element_definition.fixed_string
            elif hc_element_definition.fixed_type == 'uri': 
                hc_element_definition.fixed_name = hc_element_definition.fixed_uri
            elif hc_element_definition.fixed_type == 'boolean': 
                hc_element_definition.fixed_name = hc_element_definition.fixed_boolean
            elif hc_element_definition.fixed_type == 'code':    
                hc_element_definition.fixed_name = hc_element_definition.fixed_code_id.name
            elif hc_element_definition.fixed_type == 'markdown':    
                hc_element_definition.fixed_name = hc_element_definition.fixed_markdown
            elif hc_element_definition.fixed_type == 'coding':    
                hc_element_definition.fixed_name = hc_element_definition.fixed_coding_id.name
            elif hc_element_definition.fixed_type == 'codeable_concept':  
                hc_element_definition.fixed_name = hc_element_definition.fixed_codeable_concept_id.name
            elif hc_element_definition.fixed_type == 'attachment':    
                hc_element_definition.fixed_name = hc_element_definition.fixed_attachment_id.name
            elif hc_element_definition.fixed_type == 'identifier':    
                hc_element_definition.fixed_name = hc_element_definition.fixed_identifier_id.name
            elif hc_element_definition.fixed_type == 'quantity':
                hc_element_definition.fixed_name = str(hc_element_definition.fixed_quantity)
            elif hc_element_definition.fixed_type == 'range':
                hc_element_definition.fixed_name = hc_element_definition.fixed_range
            elif hc_element_definition.fixed_type == 'period':
                hc_element_definition.fixed_name = hc_element_definition.fixed_period
            elif hc_element_definition.fixed_type == 'ratio':
                hc_element_definition.fixed_name = str(hc_element_definition.fixed_ratio)
            elif hc_element_definition.fixed_type == 'human_name':    
                hc_element_definition.fixed_name = hc_element_definition.fixed_human_name_id.name
            elif hc_element_definition.fixed_type == 'address':   
                hc_element_definition.fixed_name = hc_element_definition.fixed_address_id.name   
            elif hc_element_definition.fixed_type == 'contact_point':  
                hc_element_definition.fixed_name = hc_element_definition.fixed_contact_point_id.name
            elif hc_element_definition.fixed_type == 'timing':   
                hc_element_definition.fixed_name = hc_element_definition.fixed_timing_id.name
            elif hc_element_definition.fixed_type == 'signature':    
                hc_element_definition.fixed_name = hc_element_definition.fixed_signature_id.name
            elif hc_element_definition.fixed_type == 'reference':    
                hc_element_definition.fixed_name = hc_element_definition.fixed_reference_id.name
            elif hc_element_definition.fixed_type == 'time':   
                hc_element_definition.fixed_type = str(hc_element_definition.fixed_time)                
            elif hc_element_definition.fixed_type == 'oid': 
                hc_element_definition.fixed_name = hc_element_definition.fixed_oid
            elif hc_element_definition.fixed_type == 'id':  
                hc_element_definition.fixed_name = hc_element_definition.fixed_id
            elif hc_element_definition.fixed_type == 'unsigned_int':   
                hc_element_definition.fixed_type = str(hc_element_definition.fixed_unsigned_int)                 
            elif hc_element_definition.fixed_type == 'positive_int':   
                hc_element_definition.fixed_type = str(hc_element_definition.fixed_positive_int)                
            elif hc_element_definition.fixed_type == 'annotation':  
                hc_element_definition.fixed_name = hc_element_definition.fixed_annotation_id.name
            elif hc_element_definition.fixed_type == 'sampled_data':    
                hc_element_definition.fixed_name = hc_element_definition.fixed_sampled_data_id.name
            elif hc_element_definition.fixed_type == 'meta':    
                hc_element_definition.fixed_name = hc_element_definition.fixed_meta_id.name

    @api.depends('pattern_type')              
    def _compute_pattern_name(self):              
        for hc_element_definition in self:
            if hc_element_definition.pattern_type == 'integer':       
                hc_element_definition.pattern_name = str(hc_element_definition.pattern_integer)
            elif hc_element_definition.pattern_type == 'decimal':   
                hc_element_definition.pattern_name = str(hc_element_definition.pattern_decimal)
            elif hc_element_definition.pattern_type == 'date_time':  
                hc_element_definition.pattern_type = str(hc_element_definition.pattern_date_time)
            elif hc_element_definition.pattern_type == 'date':      
                hc_element_definition.pattern_name = str(hc_element_definition.pattern_date)
            elif hc_element_definition.pattern_type == 'instant':   
                hc_element_definition.pattern_name = str(hc_element_definition.pattern_instant)
            elif hc_element_definition.pattern_type == 'string':      
                hc_element_definition.pattern_name = hc_element_definition.pattern_string
            elif hc_element_definition.pattern_type == 'uri': 
                hc_element_definition.pattern_name = hc_element_definition.pattern_uri
            elif hc_element_definition.pattern_type == 'boolean': 
                hc_element_definition.pattern_name = hc_element_definition.pattern_boolean
            elif hc_element_definition.pattern_type == 'code':    
                hc_element_definition.pattern_name = hc_element_definition.pattern_code_id.name
            elif hc_element_definition.pattern_type == 'markdown':    
                hc_element_definition.pattern_name = hc_element_definition.pattern_markdown
            elif hc_element_definition.pattern_type == 'coding':    
                hc_element_definition.pattern_name = hc_element_definition.pattern_coding_id.name
            elif hc_element_definition.pattern_type == 'codeable_concept':  
                hc_element_definition.pattern_name = hc_element_definition.pattern_codeable_concept_id.name
            elif hc_element_definition.pattern_type == 'attachment':    
                hc_element_definition.pattern_name = hc_element_definition.pattern_attachment_id.name
            elif hc_element_definition.pattern_type == 'identifier':    
                hc_element_definition.pattern_name = hc_element_definition.pattern_identifier_id.name
            elif hc_element_definition.pattern_type == 'quantity':
                hc_element_definition.pattern_name = str(hc_element_definition.pattern_quantity)
            elif hc_element_definition.pattern_type == 'range':
                hc_element_definition.pattern_name = hc_element_definition.pattern_range
            elif hc_element_definition.pattern_type == 'period':
                hc_element_definition.pattern_name = hc_element_definition.pattern_period
            elif hc_element_definition.pattern_type == 'ratio':
                hc_element_definition.pattern_name = str(hc_element_definition.pattern_ratio)
            elif hc_element_definition.pattern_type == 'human_name':    
                hc_element_definition.pattern_name = hc_element_definition.pattern_human_name_id.name
            elif hc_element_definition.pattern_type == 'address':   
                hc_element_definition.pattern_name = hc_element_definition.pattern_address_id.name   
            elif hc_element_definition.pattern_type == 'contact_point':  
                hc_element_definition.pattern_name = hc_element_definition.pattern_contact_point_id.name
            elif hc_element_definition.pattern_type == 'timing':   
                hc_element_definition.pattern_name = hc_element_definition.pattern_timing_id.name
            elif hc_element_definition.pattern_type == 'signature':    
                hc_element_definition.pattern_name = hc_element_definition.pattern_signature_id.name
            elif hc_element_definition.pattern_type == 'reference':    
                hc_element_definition.pattern_name = hc_element_definition.pattern_reference_id.name
            elif hc_element_definition.pattern_type == 'time':   
                hc_element_definition.pattern_type = str(hc_element_definition.pattern_time)                
            elif hc_element_definition.pattern_type == 'oid': 
                hc_element_definition.pattern_name = hc_element_definition.pattern_oid
            elif hc_element_definition.pattern_type == 'id':  
                hc_element_definition.pattern_name = hc_element_definition.pattern_id
            elif hc_element_definition.pattern_type == 'unsigned_int':   
                hc_element_definition.pattern_type = str(hc_element_definition.pattern_unsigned_int)                 
            elif hc_element_definition.pattern_type == 'positive_int':   
                hc_element_definition.pattern_type = str(hc_element_definition.pattern_positive_int)                
            elif hc_element_definition.pattern_type == 'annotation':  
                hc_element_definition.pattern_name = hc_element_definition.pattern_annotation_id.name
            elif hc_element_definition.pattern_type == 'sampled_data':    
                hc_element_definition.pattern_name = hc_element_definition.pattern_sampled_data_id.name
            elif hc_element_definition.pattern_type == 'meta':    
                hc_element_definition.pattern_name = hc_element_definition.pattern_meta_id.name

class ElementDefinitionSlicing(models.Model):    
    _name = "hc.element.definition.slicing"    
    _description = "Element Definition Slicing"                

    element_definition_id = fields.Many2one(
        comodel_name="hc.element.definition", 
        string="Element Definition", 
        help="Element Definition associated with this Element Definition Slicing.")  
    name = fields.Char(
        string="Name", 
        help="Text representation of the slicing.")                    
    discriminator_ids = fields.One2many(
        comodel_name="hc.element.definition.slicing.discriminator", 
        inverse_name="slicing_id", 
        string="Discriminators", 
        help="Element values that are used to distinguish the slices.")                        
    description = fields.Text(
        string="Description", 
        help="Text description of how slicing works (or not).")                        
    is_ordered = fields.Boolean(
        string="Ordered", 
        help="If elements must be in same order as slices.")                        
    rules = fields.Selection(
        string="Rules", 
        required="True", 
        selection=[
            ("closed", "Closed"), 
            ("open", "Open"), 
            ("openAtEnd", "Open At End")], 
        help="Whether additional slices are allowed or not. When the slices are ordered, profile authors can also say that additional slices are only allowed at the end.")                        

class ElementDefinitionBase(models.Model):    
    _name = "hc.element.definition.base"    
    _description = "Element Definition Base"
    _rec_name = "path"                
                      
    element_definition_id = fields.Many2one(
        comodel_name="hc.element.definition", 
        string="Element Definition", 
        help="Element Definition associated with this Element Definition Base.")  
    path = fields.Char(
        string="Path", 
        required="True", 
        help="Path that identifies the base element.")                        
    min = fields.Integer(
        string="Min", 
        required="True", 
        help="Min cardinality of the base element.")                        
    max = fields.Char(
        string="Max", 
        required="True", 
        help="Max cardinality of the base element.")                        

class ElementDefinitionType(models.Model):    
    _name = "hc.element.definition.type"    
    _description = "Element Definition Type"                

    element_definition_id = fields.Many2one(
        comodel_name="hc.element.definition", 
        string="Element Definition", 
        help="Element Definition associated with this Element Definition Type.")                        
    # code = fields.Char(
    #     string="Code", 
    #     required="True", 
    #     help="Data type or Resource (reference to definition).")
    # future
    code_id = fields.Many2one(
        comodel_name="hc.vs.defined.type",
        string="Code", 
        required="True", 
        help="Data type or Resource (reference to definition).")                        
    profile = fields.Char(
        string="Profile URI", 
        help="Profile (StructureDefinition) to apply (or IG).")                        
    target_profile = fields.Char(
        string="Target Profile URI", 
        help="Profile (StructureDefinition) to apply to reference target (or IG).")                        
    aggregation_ids = fields.One2many(
        comodel_name="hc.element.definition.type.aggregation", 
        inverse_name="type_id", 
        string="Aggregations", 
        help="If the type is a reference to another resource, how the resource is or can be aggregated - is it a contained resource, or a reference, and if the context is a bundle, is it included in the bundle.")
    versioning = fields.Selection(
        string="Versioning", 
        selection=[
            ("either", "Either"), 
            ("independent", "Independent"), 
            ("specific", "Specific")], 
        help="Whether this reference needs to be version specific or version independent, or whetehr either can be used.")                        

class ElementDefinitionExample(models.Model):    
    _name = "hc.element.definition.example"    
    _description = "Element Definition Example"                

    element_definition_id = fields.Many2one(
        comodel_name="hc.element.definition", 
        string="Element Definition", 
        help="Element Definition associated with this Element Definition Example.")                        
    label = fields.Char(
        string="Label", 
        required="True", 
        help="Describes the purpose of this example.")                        
    value_ids = fields.One2many(
        comodel_name="hc.element.definition.example.value",
        inverse_name="example_id",
        string="Values",
        required="True",
        help="Value of Example (one of allowed types).")
    
class ElementDefinitionExampleValue(models.Model):
    _name = "hc.element.definition.example.value"
    _description = "Element Definition Example Value"

    example_id = fields.Many2one(
        comodel_name="hc.element.definition.example",
        string="Element Definition Example",
        help="Element Definition Exaple associated with this Element Definition Example Value.")
    value_type = fields.Selection(
        string="Value Type",
        selection=[
            ("integer", "Integer"), 
            ("decimal", "Decimal"),
            ("date_time", "Date Time"),
            ("date", "Date"),
            ("instant", "Instant"),
            ("string", "String"),
            ("uri", "URI"), 
            ("boolean", "Boolean"),
            ("code", "Code"),
            ("markdown", "Markdown"),
            ("base_64_binary", "Base 64 Binary"),
            ("coding", "Coding"),
            ("codeable_concept", "Codeable Concept"), 
            ("attachment", "Attachment"),
            ("identifier", "Identifier"),
            ("quantity", "Quantity"),
            ("range", "Range"),
            ("period", "Period"),
            ("ratio", "Ratio"), 
            ("human_name", "Human Name"),
            ("address", "Address"),
            ("contact_point", "Contact Point"),
            ("timing", "Timing"),
            ("signature", "Signature"),
            ("reference", "Reference"),
            ("time", "Time"), 
            ("oid", "OID"), 
            ("id", "ID"), 
            ("unsigned_int", "Unsigned Integer"), 
            ("positive_int", "Positive Integer"), 
            ("annotation", "Annotation"), 
            ("sampled_data", "Sampled Data"), 
            ("meta", "Meta")],
        help="Type of example value (as defined for type).")                       
    value_name = fields.Char(
        string="Value", 
        compute="_compute_value_name", 
        store="True", 
        help="Value of Example (one of allowed types).")
    value_integer = fields.Integer(
        string="Value Integer", 
        help="Integer value of example (one of allowed types).")
    value_decimal = fields.Float(
        string="Value Decimal", 
        help="Decimal value of example (one of allowed types).")
    value_date_time = fields.Datetime(
        string="Value Date Time", 
        help="Date Time value of example (one of allowed types).")
    value_date = fields.Date(
        string="Value Date", 
        help="Date value of example (one of allowed types).")
    value_instant = fields.Datetime(
        string="Value Instant", 
        help="Instant value of example (one of allowed types).")
    value_string = fields.Char(
        string="Value String", 
        help="String value of example (one of allowed types).")
    value_uri = fields.Char(
        string="Value URI", 
        help="URI value of example (one of allowed types).")
    value_boolean = fields.Boolean(
        string="Value Boolean", 
        help="Boolean value of example (one of allowed types).")
    value_code_id = fields.Many2one(
        comodel_name="hc.vs.element.definition.code",
        string="Value Code", 
        help="Code value of example (one of allowed types).")
    value_markdown = fields.Text(
        string="Value Markdown", 
        help="Markdown value of example (one of allowed types).")
    value_base_64_binary = fields.Binary(
        string="Value Base 64 Binary", 
        help="Base 64 Binary value of example (one of allowed types).")
    value_coding_id = fields.Many2one(
        comodel_name="hc.vs.element.definition.code", 
        string="Value Coding", 
        help="Coding value of example (one of allowed types).")
    value_codeable_concept_id = fields.Many2one(
        comodel_name="hc.vs.element.definition.code", 
        string="Value Codeable Concept", 
        help="Codeable Concept value of example (one of allowed types).")
    value_attachment_id = fields.Many2one(
        comodel_name="hc.element.definition.attachment", 
        string="Value Attachment", 
        help="Attachment value of example (one of allowed types).")
    value_identifier_id = fields.Many2one(
        comodel_name="hc.element.definition.identifier", 
        string="Value Identifier", 
        help="Identifier value of example (one of allowed types).")
    value_quantity = fields.Float(
        string="Value Quantity", 
        help="Quantity value of example (one of allowed types).")
    value_quantity_uom_id = fields.Many2one(
        comodel_name="product.uom", 
        string="Value Quantity UOM", 
        help="Quantity unit of measure.")
    value_range = fields.Char(
        string="Value Range", 
        help="Range value of example (one of allowed types).")
    value_period = fields.Char(
        string="Value Period", 
        help="Period value of example (one of allowed types).")
    value_period_uom_id = fields.Many2one(
        comodel_name="product.uom", 
        string="Value Period UOM", 
        help="Period unit of measure.")
    value_ratio = fields.Float(
        string="Value Ratio", 
        help="Ratio of value of example (one of allowed types).")
    value_human_name_id = fields.Many2one(
        comodel_name="hc.element.definition.human.name", 
        string="Value Human Name", 
        help="Human Name value of example (one of allowed types).")
    value_address_id = fields.Many2one(
        comodel_name="hc.element.definition.address", 
        string="Value Address", 
        help="Address value of example (one of allowed types).")
    value_contact_point_id = fields.Many2one(
        comodel_name="hc.element.definition.telecom", 
        string="Value Contact Point", 
        help="Contact Point value of example (one of allowed types).")
    value_timing_id = fields.Many2one(
        comodel_name="hc.element.definition.timing", 
        string="Value Timing", 
        help="Timing value of example (one of allowed types).")
    value_signature_id = fields.Many2one(
        comodel_name="hc.element.definition.signature", 
        string="Value Signature", 
        help="Signature value of example (one of allowed types).")
    value_reference_id = fields.Many2one(
        comodel_name="hc.element.definition.reference", 
        string="Value Reference", 
        help="Reference value of example (one of allowed types).")
    value_time = fields.Float(
        string="Value Time", 
        help="Time value of example (one of allowed types).")
    value_oid = fields.Char(
        string="Value OID", 
        help="OID value of example (one of allowed types).")
    value_id = fields.Char(
        string="Value ID", 
        help="ID value of example (one of allowed types).")
    value_unsigned_int = fields.Integer(
        string="Value Unsigned Integer", 
        help="Unsigned Integer value of example (one of allowed types).")
    value_positive_int = fields.Integer(
        string="Value Positive Integer", 
        help="Positive Integer value of example (one of allowed types).")
    value_annotation_id = fields.Many2one(
        comodel_name="hc.element.definition.annotation", 
        string="Value Annotation", 
        help="Annotation value of example (one of allowed types).")
    value_sampled_data_id = fields.Many2one(
        comodel_name="hc.element.definition.sampled.data", 
        string="Value Sampled Data", 
        help="Sampled Data value of example (one of allowed types).")
    value_meta_id = fields.Many2one(
        comodel_name="hc.element.definition.meta", 
        string="Value Meta", 
        help="Meta value of example (one of allowed types).")

    @api.depends('value_type')              
    def _compute_value_name(self):              
        for hc_element_definition_example_value in self:
            if hc_element_definition_example_value.value_type == 'integer':       
                hc_element_definition_example_value.value_name = str(hc_element_definition_example_value.value_integer)
            elif hc_element_definition_example_value.value_type == 'decimal':   
                hc_element_definition_example_value.value_name = str(hc_element_definition_example_value.value_decimal)
            elif hc_element_definition_example_value.value_type == 'date_time':  
                hc_element_definition_example_value.value_type = str(hc_element_definition_example_value.value_date_time)
            elif hc_element_definition_example_value.value_type == 'date':      
                hc_element_definition_example_value.value_name = str(hc_element_definition_example_value.value_date)
            elif hc_element_definition_example_value.value_type == 'instant':   
                hc_element_definition_example_value.value_name = str(hc_element_definition_example_value.value_instant)
            elif hc_element_definition_example_value.value_type == 'string':      
                hc_element_definition_example_value.value_name = hc_element_definition_example_value.value_string
            elif hc_element_definition_example_value.value_type == 'uri': 
                hc_element_definition_example_value.value_name = hc_element_definition_example_value.value_uri
            elif hc_element_definition_example_value.value_type == 'boolean': 
                hc_element_definition_example_value.value_name = hc_element_definition_example_value.value_boolean
            elif hc_element_definition_example_value.value_type == 'code':    
                hc_element_definition_example_value.value_name = hc_element_definition_example_value.value_code_id.name
            elif hc_element_definition_example_value.value_type == 'markdown':    
                hc_element_definition_example_value.value_name = hc_element_definition_example_value.value_markdown
            elif hc_element_definition_example_value.value_type == 'coding':    
                hc_element_definition_example_value.value_name = hc_element_definition_example_value.value_coding_id.name
            elif hc_element_definition_example_value.value_type == 'codeable_concept':  
                hc_element_definition_example_value.value_name = hc_element_definition_example_value.value_codeable_concept_id.name
            elif hc_element_definition_example_value.value_type == 'attachment':    
                hc_element_definition_example_value.value_name = hc_element_definition_example_value.value_attachment_id.name
            elif hc_element_definition_example_value.value_type == 'identifier':    
                hc_element_definition_example_value.value_name = hc_element_definition_example_value.value_identifier_id.name
            elif hc_element_definition_example_value.value_type == 'quantity':
                hc_element_definition_example_value.value_name = str(hc_element_definition_example_value.value_quantity)
            elif hc_element_definition_example_value.value_type == 'range':
                hc_element_definition_example_value.value_name = hc_element_definition_example_value.value_range
            elif hc_element_definition_example_value.value_type == 'period':
                hc_element_definition_example_value.value_name = hc_element_definition_example_value.value_period
            elif hc_element_definition_example_value.value_type == 'ratio':
                hc_element_definition_example_value.value_name = str(hc_element_definition_example_value.value_ratio)
            elif hc_element_definition_example_value.value_type == 'human_name':    
                hc_element_definition_example_value.value_name = hc_element_definition_example_value.value_human_name_id.name
            elif hc_element_definition_example_value.value_type == 'address':   
                hc_element_definition_example_value.value_name = hc_element_definition_example_value.value_address_id.name   
            elif hc_element_definition_example_value.value_type == 'contact_point':  
                hc_element_definition_example_value.value_name = hc_element_definition_example_value.value_contact_point_id.name
            elif hc_element_definition_example_value.value_type == 'timing':   
                hc_element_definition_example_value.value_name = hc_element_definition_example_value.value_timing_id.name
            elif hc_element_definition_example_value.value_type == 'signature':    
                hc_element_definition_example_value.value_name = hc_element_definition_example_value.value_signature_id.name
            elif hc_element_definition_example_value.value_type == 'reference':    
                hc_element_definition_example_value.value_name = hc_element_definition_example_value.value_reference_id.name
            elif hc_element_definition_example_value.value_type == 'time':   
                hc_element_definition_example_value.value_type = str(hc_element_definition_example_value.value_time)                
            elif hc_element_definition_example_value.value_type == 'oid': 
                hc_element_definition_example_value.value_name = hc_element_definition_example_value.value_oid
            elif hc_element_definition_example_value.value_type == 'id':  
                hc_element_definition_example_value.value_name = hc_element_definition_example_value.value_id
            elif hc_element_definition_example_value.value_type == 'unsigned_int':   
                hc_element_definition_example_value.value_type = str(hc_element_definition_example_value.value_unsigned_int)                 
            elif hc_element_definition_example_value.value_type == 'positive_int':   
                hc_element_definition_example_value.value_type = str(hc_element_definition_example_value.value_positive_int)                
            elif hc_element_definition_example_value.value_type == 'annotation':  
                hc_element_definition_example_value.value_name = hc_element_definition_example_value.value_annotation_id.name
            elif hc_element_definition_example_value.value_type == 'sampled_data':    
                hc_element_definition_example_value.value_name = hc_element_definition_example_value.value_sampled_data_id.name
            elif hc_element_definition_example_value.value_type == 'meta':    
                hc_element_definition_example_value.value_name = hc_element_definition_example_value.value_meta_id.name
 
class ElementDefinitionConstraint(models.Model):    
    _name = "hc.element.definition.constraint"    
    _description = "Element Definition Constraint"
    _rec_name = "key"                

    element_definition_id = fields.Many2one(
        comodel_name="hc.element.definition", 
        string="Element Definition", 
        help="Element Definition associated with this Element Definition Constraint.")                        
    key = fields.Char(
        string="Key", 
        required="True", 
        help="Target of 'condition' reference above.")                        
    requirements = fields.Char(
        string="Requirements", 
        help="Why this constraint is necessary or appropriate.")                        
    severity = fields.Selection(
        string="Severity", 
        required="True", 
        selection=[
            ("error", "Error"), 
            ("warning", "Warning")], 
        help="Identifies the impact constraint violation has on the conformance of the instance.")                        
    human = fields.Char(
        string="Human", 
        required="True", 
        help="Human description of constraint.")                        
    expression = fields.Char(
        string="Expression", 
        required="True", 
        help="FHIRPath expression of constraint.")                        
    xpath = fields.Char(
        string="XPath", 
        help="XPath expression of constraint.")                        
    source = fields.Char(
        string="Source URI", 
        help="Reference to original source of constraint.")                        

class ElementDefinitionExtension(models.Model):    
    _name = "hc.element.definition.extension"    
    _description = "Element Definition Extension"
    _inherit = ["hc.extension"]

    element_definition_id = fields.Many2one(
        comodel_name="hc.element.definition", 
        string="Element Definition", 
        help="Element Definition associated with this Element Definition Extension.")

class ElementDefinitionBinding(models.Model):    
    _name = "hc.element.definition.binding"    
    _description = "Element Definition Binding"               

    element_definition_id = fields.Many2one(
        comodel_name="hc.element.definition", 
        string="Element Definition", 
        help="Element Definition associated with this Element Definition Binding.")  
    name = fields.Char(
        string="Name",
        required="True", 
        help="Text representation of the binding.")                      
    strength = fields.Selection(
        string="Strength", 
        required="True", 
        selection=[
            ("required", "Required"), 
            ("extensible", "Extensible"), 
            ("preferred", "Preferred"), 
            ("example", "Example")], 
        help="Indicates the degree of conformance expectations associated with this binding - that is, the degree to which the provided value set must be adhered to in the instances.")                        
    description = fields.Text(
        string="Description", 
        help="Human explanation of the value set.")                        
    value_set_type = fields.Selection(
        string="Value Set Type", 
        selection=[
            ("uri", "URI"), 
            ("value_set", "Value Set")], 
        help="Type of what's administered/supplied.")                        
    value_set_name = fields.Char(
        string="Value Set", 
        compute="_compute_value_set_name", 
        store="True", help="Source of value set.")                        
    value_set_uri = fields.Char(
        string="Value Set URI", 
        help="URI that source of value set.")                        
    value_set = fields.Char(
        string="Value Set", 
        help="Value Set the reference to the value set.")                        

    @api.depends('value_set_type')  
    def _compute_value_set_name(self):  
        for hc_element_definition_binding in self:
            if hc_element_definition_binding.value_set_type == 'uri': 
                hc_element_definition_binding.value_set_name = hc_element_definition_binding.value_set_uri
            elif hc_element_definition_binding.value_set_type == 'value_set': 
                hc_element_definition_binding.value_set_name = hc_element_definition_binding.value_set

class ElementDefinitionBindingExtension(models.Model):    
    _name = "hc.element.definition.binding.extension"    
    _description = "Element Definition Binding Extension"
    _inherit = ["hc.basic.association", "hc.extension"]

    binding_id = fields.Many2one(
        comodel_name="hc.element.definition.binding", 
        string="Element Definition Binding", 
        help="Element Definition Binding associated with this Element Definition Binding Extension.")

class ElementDefinitionBindingExtensionValueReference(models.Model):    
    _name = "hc.element.definition.binding.extension.value.reference"    
    _description = "Element Definition Binding Extension Value Reference"

    extension_id = fields.Many2one(
        comodel_name="hc.element.definition.binding.extension", 
        string="Element Definition Binding Extension", 
        help="Element Definition Binding Extension associated with this Element Definition Binding Extension Value Reference.")
    reference = fields.Char(
        string="Reference",
        required="True", 
        help="Text representation of the binding extension value reference.")                

class ElementDefinitionMapping(models.Model):    
    _name = "hc.element.definition.mapping"    
    _description = "Element Definition Mapping"               

    element_definition_id = fields.Many2one(
        comodel_name="hc.element.definition", 
        string="Element Definition", 
        help="Element Definition associated with this Element Definition Mapping.")                        
    identity = fields.Char(
        string="Identity", 
        required="True", 
        help="Reference to mapping declaration.")                        
    language = fields.Char( 
        string="Language", 
        help="Computable language of mapping.")                        
    map = fields.Char(
        string="Map", 
        required="True", 
        help="Details of the mapping.")
    comment = fields.Text(
        string="Comment", 
        help="Comments about the mapping or its use.")                        

class ElementDefinitionRepresentation(models.Model):    
    _name = "hc.element.definition.representation"    
    _description = "Element Definition Representation"            
    _inherit = ["hc.basic.association"]    

    element_definition_id = fields.Many2one(
        comodel_name="hc.element.definition", 
        string="Element Definition", 
        help="Element Definition associated with this Element Definition Representation.")                        
    representation = fields.Selection(
        string="Representation", 
        selection=[
            ("xmlAttr", "XML Attr"), 
            ("xmlText", "XML Text"), 
            ("typeAttr", "Type Attr"), 
            ("cdaText", "CDA Text"), 
            ("xhtml", "XHTML")], 
        help="Codes that define how this element is represented in instances, when the deviation varies from the normal case.")                        

class ElementDefinitionAlias(models.Model): 
    _name = "hc.element.definition.alias"   
    _description = "Element Definition Alias"           
    _inherit = ["hc.basic.association"]

    element_definition_id = fields.Many2one(
        comodel_name="hc.element.definition", 
        string="Element Definition", 
        help="Element Definition associated with this Element Definition Alias.")                    
    alias = fields.Char(
        string="Alias", 
        help="Alias associated with this Element Definition Alias.")                    

class ElementDefinitionCondition(models.Model): 
    _name = "hc.element.definition.condition"   
    _description = "Element Definition Condition"           
    _inherit = ["hc.basic.association"]

    element_definition_id = fields.Many2one(
        comodel_name="hc.element.definition", 
        string="Element Definition", 
        help="Element Definition associated with this Element Definition Condition.")                    
    condition = fields.Char(
        string="Condition", 
        help="Condition associated with this Element Definition Condition.")                    

class ElementDefinitionSlicingDiscriminator(models.Model):  
    _name = "hc.element.definition.slicing.discriminator"   
    _description = "Element Definition Slicing Discriminator"           
    _inherit = ["hc.basic.association"]
    _rec_name = "path"

    slicing_id = fields.Many2one(
        comodel_name="hc.element.definition.slicing", 
        string="Slicing", 
        help="Slicing associated with this Element Definition Slicing Discriminator.")                 
    type = fields.Selection(
        string="Type", 
        selection=[
            ("value", "Value"), 
            ("exists", "Exists"), 
            ("pattern", "Pattern"), 
            ("type", "Type"), 
            ("profile", "Profile")], 
        help="How the element value is interpreted when discrimination is evaluated.")
    path = fields.Char(
        string="Path",
        required="True", 
        help="A FHIRPath expression, using a restricted subset of FHIRPath, that is used to identify the element on which discrimination is based.")              

class ElementDefinitionTypeAggregation(models.Model):   
    _name = "hc.element.definition.type.aggregation"    
    _description = "Element Definition Type Aggregation"            
    _inherit = ["hc.basic.association"]

    type_id = fields.Many2one(
        comodel_name="hc.element.definition.type", 
        string="Element Definition Type", 
        help="Element Definition Type associated with this Element Definition Type Aggregation.")                 
    aggregation = fields.Selection(
        string="Aggregation", 
        selection=[
            ("contained", "Contained"), 
            ("referenced", "Referenced"), 
            ("bundled", "Bundled")], 
        help="If the type is a reference to another resource, how the resource is or can be aggregated - is it a contained resource, or a reference, and if the context is a bundle, is it included in the bundle.")                 



class ElementDefinitionAddress(models.Model):
    _name = "hc.element.definition.address"
    _description = "Element Definition Address"
    _inherit = ["hc.address.use"]
    _inherits = {"hc.address": "address_id"}

    address_id = fields.Many2one(
        comodel_name="hc.address", 
        string="Address", 
        ondelete="restrict", 
        required="True", 
        help="Address associated with this Element Definition Address.")                                    

class ElementDefinitionAnnotation(models.Model):
    _name = "hc.element.definition.annotation"
    _description = "Element Definition Annotation" 
    _inherit = ["hc.basic.association", "hc.annotation"]    

class ElementDefinitionAttachment(models.Model):
    _name = "hc.element.definition.attachment"
    _description = "Element Definition Attachment" 
    _inherit = ["hc.basic.association", "hc.attachment"]

class ElementDefinitionTelecom(models.Model):
    _name = "hc.element.definition.telecom"
    _description = "Element Definition Telecom"
    _inherit = ["hc.contact.point.use"]
    _inherits = {"hc.contact.point": "telecom_id"}

    telecom_id = fields.Many2one(
        comodel_name="hc.contact.point", 
        string="Telecom", 
        ondelete="restrict", 
        required="True", 
        help="Telecom associated with this Element Definition Telecom.")                                  

class ElementDefinitionHumanName(models.Model):
    _name = "hc.element.definition.human.name"
    _description = "Element Definition Human Name"
    _inherit = ["hc.human.name.use"]
    _inherits = {"hc.human.name": "name_id"}

    name_id = fields.Many2one(
        comodel_name="hc.human.name", 
        string="Name", 
        ondelete="restrict", 
        required="True", 
        help="Name associated with this Element Definition Human Name.")                                   

class ElementDefinitionIdentifier(models.Model):
    _name = "hc.element.definition.identifier"
    _description = "Element Definition Identifier"
    _inherit = ["hc.basic.association", "hc.identifier"] 

class ElementDefinitionMeta(models.Model):
    _name = "hc.element.definition.meta"
    _description = "Element Definition Meta"
    _inherit = ["hc.basic.association", "hc.meta"]

class ElementDefinitionReference(models.Model):
    _name = "hc.element.definition.reference"
    _description = "Element Definition Reference"
    _inherit = ["hc.basic.association", "hc.reference"]

class ElementDefinitionSampledData(models.Model):
    _name = "hc.element.definition.sampled.data"
    _description = "Element Definition Sampled Data"
    _inherit = ["hc.basic.association", "hc.sampled.data"]

class ElementDefinitionSignature(models.Model):
    _name = "hc.element.definition.signature"
    _description = "Element Definition Signature"
    _inherit = ["hc.basic.association", "hc.signature"]

class ElementDefinitionTiming(models.Model):
    _name = "hc.element.definition.timing"
    _description = "Element Definition Timing"
    _inherit = ["hc.basic.association", "hc.timing"]

class ElementDefinitionCode(models.Model):
    _name = "hc.vs.element.definition.code"
    _description = "Element Definition Code"
    _inherit = ["hc.value.set.contains"]    

    name = fields.Char(
        string="Name",
        help="Name of this element definition code.")                                 
    code = fields.Char(
        string="Code",
        help="Code of this element definition code.")                                 
    contains_id = fields.Many2one(
        comodel_name="hc.vs.element.definition.code",
        string="Parent",
        help="Parent element definition code.")                                    
                                    





