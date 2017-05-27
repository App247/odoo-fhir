# -*- coding: utf-8 -*-

from openerp import models, fields, api

class ElementDefinition(models.Model):    
    _name = "hc.element.definition"    
    _description = "Element Definition"    
    _rec_name = "label"            

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
    comments = fields.Text(
        string="Comments", 
        help="Comments about the use of this element.")                        
    requirements = fields.Text(
        string="Requirements", 
        help="Why this resource has been created.")                        
    alias_ids = fields.One2many(
        comodel_name="hc.element.definition.alias", 
        inverse_name="element_definition_id", 
        string="Aliass", 
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
            ("reference", "Reference")],
        help="Type of specified value if missing from instance.")                        
    default_value_name = fields.Char(
        string="Default Value", 
        compute="_compute_default_value_name", 
        store="True", 
        help="Specified value if missing from instance.")                        
    default_value_integer = fields.Float(
        string="Default Value Integer", 
        help="Integer specified value if missing from instance.")                        
    default_value_decimal = fields.Float(
        string="Default Value Decimal", 
        help="Decimal specified value if missing from instance.")                        
    default_value_date_time = fields.Float(
        string="Default Value Date Time", 
        help="Date Time specified value if missing from instance.")                        
    default_value_date = fields.Float(
        string="Default Value Date", 
        help="Date specified value if missing from instance.")                        
    default_value_instant = fields.Float(
        string="Default Value Instant", 
        help="Instant specified value if missing from instance.")                        
    default_value_string = fields.Float(
        string="Default Value String", 
        help="String specified value if missing from instance.")                        
    default_value_uri = fields.Float(
        string="Default Value URI", help="URI specified value if missing from instance.")                        
    default_value_boolean = fields.Float(
        string="Default Value Boolean", 
        help="Boolean specified value if missing from instance.")                        
    default_value_code = fields.Float(
        string="Default Value Code", 
        help="Code specified value if missing from instance.")                        
    default_value_markdown = fields.Float(
        string="Default Value Markdown", 
        help="Markdown specified value if missing from instance.")                        
    default_value_base_64_binary = fields.Float(
        string="Default Value Base 64 Binary", 
        help="Base 64 Binary specified value if missing from instance.")                        
    default_value_coding = fields.Float(
        string="Default Value Coding", 
        help="Coding specified value if missing from instance.")                        
    default_value_codeable_concept = fields.Float(
        string="Default Value Codeable Concept", 
        help="Codeable Concept specified value if missing from instance.")                        
    default_value_attachment = fields.Float(
        string="Default Value Attachment", 
        help="Attachment specified value if missing from instance.")                        
    default_value_identifier = fields.Float(
        string="Default Value Identifier", 
        help="Identifier specified value if missing from instance.")                        
    default_value_quantity = fields.Float(
        string="Default Value Quantity", 
        help="Quantity specified value if missing from instance.")                        
    default_value_quantity_uom_id = fields.Many2one(
        comodel_name="product.uom", 
        string="Default Value Quantity UOM", 
        help="Quantity unit of measure.")                        
    default_value_range = fields.Float(
        string="Default Value Range", 
        help="Range specified value if missing from instance.")                        
    default_value_range_uom_id = fields.Many2one(
        comodel_name="product.uom", 
        string="Default Value Range UOM", 
        help="Range unit of measure.")                        
    default_value_period = fields.Float(
        string="Default Value Period", 
        help="Period specified value if missing from instance.")                        
    default_value_period_uom_id = fields.Many2one(
        comodel_name="product.uom", 
        string="Default Value Period UOM", 
        help="Period unit of measure.")                        
    default_value_numerator = fields.Float(
        string="Default Value Numerator", 
        help="Numerator value of specified value if missing from instance.")
    default_value_numerator_uom_id = fields.Many2one(
        comodel_name="product.uom", 
        string="Default Value Numerator UOM", 
        help="Default Value numerator unit of measure.")
    default_value_denominator = fields.Float(
        string="Default Value Denominator", 
        help="Denominator value of specified value if missing from instance.")
    default_value_denominator_uom_id = fields.Many2one(
        comodel_name="product.uom", 
        string="Default Value Denominator UOM", 
        help="Default Value denominator unit of measure.")
    default_value_ratio = fields.Float(
        string="Default Value Ratio", 
        compute="_compute_default_value_ratio", 
        store="True", 
        help="Ratio of specified value if missing from instance.")
    default_value_ratio_uom = fields.Char(
        string="Default Value Ratio UOM", 
        compute="_compute_default_value_ratio_uom", 
        store="True", 
        help="Default Value Ratio unit of measure.")                  
    default_value_human_name = fields.Float(
        string="Default Value Human Name", 
        help="Human Name specified value if missing from instance.")                        
    default_value_address = fields.Float(
        string="Default Value Address", 
        help="Address specified value if missing from instance.")                        
    default_value_contact_point = fields.Float(
        string="Default Value Contact Point", 
        help="Contact Point specified value if missing from instance.")                        
    default_value_timing = fields.Float(
        string="Default Value Timing", 
        help="Timing specified value if missing from instance.")                        
    default_value_signature = fields.Float(
        string="Default Value Signature", 
        help="Signature specified value if missing from instance.")                        
    default_value_reference = fields.Float(
        string="Default Value Reference", 
        help="Reference specified value if missing from instance.")                        
    meaning_when_missing = fields.Text(
        string="Meaning When Missing", 
        help="Implicit meaning when this element is missing.")                        
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
            ("reference", "Reference")],
        help="Type of value must be exactly this.")                        
    fixed_name = fields.Char(
        string="Fixed", 
        compute="_compute_fixed_name", 
        store="True", help="Value must be exactly this.")                        
    fixed_integer = fields.Float(
        string="Fixed Integer", 
        help="Integer value must be exactly this.")                        
    fixed_decimal = fields.Float(
        string="Fixed Decimal", 
        help="Decimal value must be exactly this.")                        
    fixed_date_time = fields.Float(
        string="Fixed Date Time", 
        help="Date Time value must be exactly this.")                        
    fixed_date = fields.Float(
        string="Fixed Date", 
        help="Date value must be exactly this.")                        
    fixed_instant = fields.Float(
        string="Fixed Instant", 
        help="Instant value must be exactly this.")                        
    fixed_string = fields.Float(
        string="Fixed String", 
        help="String value must be exactly this.")                        
    fixed_uri = fields.Float(
        string="Fixed URI", 
        help="URI value must be exactly this.")                        
    fixed_boolean = fields.Float(
        string="Fixed Boolean", 
        help="Boolean value must be exactly this.")                        
    fixed_code = fields.Float(
        string="Fixed Code", 
        help="Code value must be exactly this.")                        
    fixed_markdown = fields.Float(
        string="Fixed Markdown", 
        help="Markdown value must be exactly this.")                        
    fixed_base_64_binary = fields.Float(
        string="Fixed Base 64 Binary", 
        help="Base 64 Binary value must be exactly this.")                        
    fixed_coding = fields.Float(
        string="Fixed Coding", 
        help="Coding value must be exactly this.")                        
    fixed_codeable_concept = fields.Float(
        string="Fixed Codeable Concept", 
        help="Codeable Concept value must be exactly this.")                        
    fixed_attachment = fields.Float(
        string="Fixed Attachment", 
        help="Attachment value must be exactly this.")                        
    fixed_identifier = fields.Float(
        string="Fixed Identifier", 
        help="Identifier value must be exactly this.")                        
    fixed_quantity = fields.Float(
        string="Fixed Quantity", 
        help="Quantity value must be exactly this.")                        
    fixed_quantity_uom_id = fields.Many2one(
        comodel_name="product.uom", 
        string="Fixed Quantity UOM", 
        help="Quantity unit of measure.")                        
    fixed_range = fields.Float(
        string="Fixed Range", 
        help="Range value must be exactly this.")                        
    fixed_range_uom_id = fields.Many2one(
        comodel_name="product.uom", 
        string="Fixed Range UOM", 
        help="Range unit of measure.")                        
    fixed_period = fields.Float(
        string="Fixed Period", 
        help="Period value must be exactly this.")                        
    fixed_period_uom_id = fields.Many2one(
        comodel_name="product.uom", 
        string="Fixed Period UOM", 
        help="Period unit of measure.")                        
    fixed_numerator = fields.Float(
        string="Fixed Numerator", 
        help="Numerator value of value must be exactly this.")
    fixed_numerator_uom_id = fields.Many2one(
        comodel_name="product.uom", 
        string="Fixed Numerator UOM", 
        help="Fixed numerator unit of measure.")
    fixed_denominator = fields.Float(
        string="Fixed Denominator", 
        help="Denominator value of value must be exactly this.")
    fixed_denominator_uom_id = fields.Many2one(
        comodel_name="product.uom", 
        string="Fixed Denominator UOM", 
        help="Fixed denominator unit of measure.")
    fixed_ratio = fields.Float(
        string="Fixed Ratio", 
        compute="_compute_fixed_ratio", 
        store="True", 
        help="Ratio of value must be exactly this.")
    fixed_ratio_uom = fields.Char(
        string="Fixed Ratio UOM", 
        compute="_compute_fixed_ratio_uom", 
        store="True", 
        help="Fixed Ratio unit of measure.")                      
    fixed_human_name = fields.Float(
        string="Fixed Human Name", 
        help="Human Name value must be exactly this.")                        
    fixed_address = fields.Float(
        string="Fixed Address", 
        help="Address value must be exactly this.")                        
    fixed_contact_point = fields.Float(
        string="Fixed Contact Point", 
        help="Contact Point value must be exactly this.")                        
    fixed_timing = fields.Float(
        string="Fixed Timing", 
        help="Timing value must be exactly this.")                        
    fixed_signature = fields.Float(
        string="Fixed Signature", 
        help="Signature value must be exactly this.")                        
    fixed_reference = fields.Float(
        string="Fixed Reference", 
        help="Reference value must be exactly this.")                        
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
            ("reference", "Reference")],
        help="Type of value must have at least these property values.")                        
    pattern_name = fields.Char(
        string="Pattern", 
        compute="_compute_pattern_name", 
        store="True", 
        help="Value must have at least these property values.")                        
    pattern_integer = fields.Float(
        string="Pattern Integer", 
        help="Integer value must have at least these property values.")                        
    pattern_decimal = fields.Float(
        string="Pattern Decimal", 
        help="Decimal value must have at least these property values.")                        
    pattern_date_time = fields.Float(
        string="Pattern Date Time", 
        help="Date Time value must have at least these property values.")                        
    pattern_date = fields.Float(
        string="Pattern Date", 
        help="Date value must have at least these property values.")                        
    pattern_instant = fields.Float(
        string="Pattern Instant", 
        help="Instant value must have at least these property values.")                        
    pattern_string = fields.Float(
        string="Pattern String", 
        help="String value must have at least these property values.")                        
    pattern_uri = fields.Float(
        string="Pattern URI", 
        help="URI value must have at least these property values.")                        
    pattern_boolean = fields.Float(
        string="Pattern Boolean", 
        help="Boolean value must have at least these property values.")                        
    pattern_code = fields.Float(
        string="Pattern Code", 
        help="Code value must have at least these property values.")                        
    pattern_markdown = fields.Float(
        string="Pattern Markdown", 
        help="Markdown value must have at least these property values.")                        
    pattern_base_64_binary = fields.Float(
        string="Pattern Base 64 Binary", 
        help="Base 64 Binary value must have at least these property values.")                        
    pattern_coding = fields.Float(
        string="Pattern Coding", 
        help="Coding value must have at least these property values.")                        
    pattern_codeable_concept = fields.Float(
        string="Pattern Codeable Concept", 
        help="Codeable Concept value must have at least these property values.")                        
    pattern_attachment = fields.Float(
        string="Pattern Attachment", 
        help="Attachment value must have at least these property values.")                        
    pattern_identifier = fields.Float(
        string="Pattern Identifier", 
        help="Identifier value must have at least these property values.")                        
    pattern_quantity = fields.Float(
        string="Pattern Quantity", 
        help="Quantity value must have at least these property values.")                        
    pattern_quantity_uom_id = fields.Many2one(
        comodel_name="product.uom", 
        string="Pattern Quantity UOM", 
        help="Quantity unit of measure.")                        
    pattern_range = fields.Float(
        string="Pattern Range", 
        help="Range value must have at least these property values.")                        
    pattern_range_uom_id = fields.Many2one(
        comodel_name="product.uom", 
        string="Pattern Range UOM", 
        help="Range unit of measure.")                        
    pattern_period = fields.Float(
        string="Pattern Period", 
        help="Period value must have at least these property values.")                        
    pattern_period_uom_id = fields.Many2one(
        comodel_name="product.uom", 
        string="Pattern Period UOM", 
        help="Period unit of measure.")                        
    pattern_numerator = fields.Float(
        string="Pattern Numerator", 
        help="Numerator value of value must have at least these property values.")
    pattern_numerator_uom_id = fields.Many2one(
        comodel_name="product.uom", 
        string="Pattern Numerator UOM", 
        help="Pattern numerator unit of measure.")
    pattern_denominator = fields.Float(
        string="Pattern Denominator", 
        help="Denominator value of value must have at least these property values.")
    pattern_denominator_uom_id = fields.Many2one(
        comodel_name="product.uom", 
        string="Pattern Denominator UOM", 
        help="Pattern denominator unit of measure.")
    pattern_ratio = fields.Float(
        string="Pattern Ratio", 
        compute="_compute_pattern_ratio", 
        store="True", 
        help="Ratio of value must have at least these property values.")
    pattern_ratio_uom = fields.Char(
        string="Pattern Ratio UOM", 
        compute="_compute_pattern_ratio_uom", 
        store="True", help="Pattern Ratio unit of measure.")                      
    pattern_human_name = fields.Float(
        string="Pattern Human Name", 
        help="Human Name value must have at least these property values.")                        
    pattern_address = fields.Float(
        string="Pattern Address", 
        help="Address value must have at least these property values.")                        
    pattern_contact_point = fields.Float(
        string="Pattern Contact Point", 
        help="Contact Point value must have at least these property values.")                        
    pattern_timing = fields.Float(
        string="Pattern Timing", 
        help="Timing value must have at least these property values.")                        
    pattern_signature = fields.Float(
        string="Pattern Signature", 
        help="Signature value must have at least these property values.")                        
    pattern_reference = fields.Float(
        string="Pattern Reference", 
        help="Reference value must have at least these property values.")                        
    example_type = fields.Selection(
        string="Example Type", 
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
            ("reference", "Reference")],
        help="Type of example value (as defined for type).")                          
    example_name = fields.Char(
        string="Example", 
        compute="_compute_example_name", 
        store="True", 
        help="Example value (as defined for type).")                        
    example_integer = fields.Float(
        string="Example Integer", 
        help="Integer example value (as defined for type).")                        
    example_decimal = fields.Float(
        string="Example Decimal", 
        help="Decimal example value (as defined for type).")                        
    example_date_time = fields.Float(
        string="Example Date Time", 
        help="Date Time example value (as defined for type).")                        
    example_date = fields.Float(
        string="Example Date", 
        help="Date example value (as defined for type).")                        
    example_instant = fields.Float(
        string="Example Instant", 
        help="Instant example value (as defined for type).")                        
    example_string = fields.Float(
        string="Example String", 
        help="String example value (as defined for type).")                        
    example_uri = fields.Float(
        string="Example URI", 
        help="URI example value (as defined for type).")                        
    example_boolean = fields.Float(
        string="Example Boolean", 
        help="Boolean example value (as defined for type).")                        
    example_code = fields.Float(
        string="Example Code", 
        help="Code example value (as defined for type).")                        
    example_markdown = fields.Float(
        string="Example Markdown", 
        help="Markdown example value (as defined for type).")                        
    example_base_64_binary = fields.Float(
        string="Example Base 64 Binary", 
        help="Base 64 Binary example value (as defined for type).")                        
    example_coding = fields.Float(
        string="Example Coding", 
        help="Coding example value (as defined for type).")                        
    example_codeable_concept = fields.Float(
        string="Example Codeable Concept", 
        help="Codeable Concept example value (as defined for type).")                        
    example_attachment = fields.Float(
        string="Example Attachment", 
        help="Attachment example value (as defined for type).")                        
    example_identifier = fields.Float(
        string="Example Identifier", 
        help="Identifier example value (as defined for type).")                        
    example_quantity = fields.Float(
        string="Example Quantity", 
        help="Quantity example value (as defined for type).")                        
    example_quantity_uom_id = fields.Many2one(
        comodel_name="product.uom", 
        string="Example Quantity UOM", 
        help="Quantity unit of measure.")                        
    example_range = fields.Float(
        string="Example Range", 
        help="Range example value (as defined for type).")                        
    example_range_uom_id = fields.Many2one(
        comodel_name="product.uom", 
        string="Example Range UOM", 
        help="Range unit of measure.")                        
    example_period = fields.Float(
        string="Example Period", 
        help="Period example value (as defined for type).")                        
    example_period_uom_id = fields.Many2one(
        comodel_name="product.uom", 
        string="Example Period UOM", 
        help="Period unit of measure.")                        
    example_numerator = fields.Float(
        string="Example Numerator", 
        help="Numerator value of example value (as defined for type).")
    example_numerator_uom_id = fields.Many2one(
        comodel_name="product.uom", 
        string="Example Numerator UOM", help="Example numerator unit of measure.")
    example_denominator = fields.Float(
        string="Example Denominator", 
        help="Denominator value of example value (as defined for type).")
    example_denominator_uom_id = fields.Many2one(
        comodel_name="product.uom", 
        string="Example Denominator UOM", 
        help="Example denominator unit of measure.")
    example_ratio = fields.Float(
        string="Example Ratio", 
        compute="_compute_example_ratio", 
        store="True", 
        help="Ratio of example value (as defined for type).")
    example_ratio_uom = fields.Char(
        string="Example Ratio UOM", 
        compute="_compute_example_ratio_uom", 
        store="True", 
        help="Example Ratio unit of measure.")                      
    example_human_name = fields.Float(
        string="Example Human Name", 
        help="Human Name example value (as defined for type).")                        
    example_address = fields.Float(
        string="Example Address", 
        help="Address example value (as defined for type).")                        
    example_contact_point = fields.Float(
        string="Example Contact Point", 
        help="Contact Point example value (as defined for type).")                        
    example_timing = fields.Float(
        string="Example Timing", 
        help="Timing example value (as defined for type).")                        
    example_signature = fields.Float(
        string="Example Signature", 
        help="Signature example value (as defined for type).")                        
    example_reference = fields.Float(
        string="Example Reference", 
        help="Reference example value (as defined for type).")                        
    min_value_date = fields.Date(
        string="Min Value Date", 
        help="Minimum Allowed Value (for some types).")                        
    max_value_date = fields.Date(
        string="Max Value Date", 
        help="Maximum Allowed Value (for some types).")                        
    max_length = fields.Integer(
        string="Max Length", 
        help="Max length for strings.")                        
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
    slicing_ids = fields.One2many(
        comodel_name="hc.element.definition.slicing", 
        inverse_name="element_definition_id", 
        string="Slicings", 
        help="This element is sliced - slices follow.")                        
    base_ids = fields.One2many(
        comodel_name="hc.element.definition.base", 
        inverse_name="element_definition_id", 
        string="Bases", 
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
    binding_ids = fields.One2many(
        comodel_name="hc.element.definition.binding", 
        inverse_name="element_definition_id", 
        string="Bindings", 
        help="ValueSet details if this is coded.")                        
    mapping_ids = fields.One2many(
        comodel_name="hc.element.definition.mapping", 
        inverse_name="element_definition_id", 
        string="Mappings", 
        help="Map element to another set of definitions.")                        

class ElementDefinitionSlicing(models.Model):    
    _name = "hc.element.definition.slicing"    
    _description = "Element Definition Slicing"                

    element_definition_id = fields.Many2one(
        comodel_name="hc.element.definition", 
        string="Element Definition", 
        help="Element Definition associated with this Element Definition Slicing.")                        
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
            ("openatend", "Open At End")], 
        help="Whether additional slices are allowed or not. When the slices are ordered, profile authors can also say that additional slices are only allowed at the end.")                        

class ElementDefinitionBase(models.Model):    
    _name = "hc.element.definition.base"    
    _description = "Element Definition Base"                

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
    code = fields.Char(
        string="Code URI", required="True", help="Data type or Resource (reference to definition).")                        
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
    value_type = fields.Selection(
        string="Value Type", 
        required="True", 
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
            ("reference", "Reference")], 
        help="Type of value of Example (one of allowed types).")                        
    value_name = fields.Char(
        string="Value",
        compute="_compute_value_name", 
        store="True", help="Value of Example (one of allowed types).")                        
    value_integer = fields.Float(
        string="Value Integer", 
        help="Integer value of example (one of allowed types).")                        
    value_decimal = fields.Float(
        string="Value Decimal", 
        help="Decimal value of example (one of allowed types).")                        
    value_date_time = fields.Float(
        string="Value Date Time", 
        help="Date Time value of example (one of allowed types).")                        
    value_date = fields.Float(
        string="Value Date", 
        help="Date value of example (one of allowed types).")                        
    value_instant = fields.Float(
        string="Value Instant", 
        help="Instant value of example (one of allowed types).")                        
    value_string = fields.Float(
        string="Value String", 
        help="String value of example (one of allowed types).")                        
    value_uri = fields.Float(
        string="Value URI", 
        help="URI value of example (one of allowed types).")                        
    value_boolean = fields.Float(
        string="Value Boolean", 
        help="Boolean value of example (one of allowed types).")                        
    value_code = fields.Float(
        string="Value Code", 
        help="Code value of example (one of allowed types).")                        
    value_markdown = fields.Float(
        string="Value Markdown", 
        help="Markdown value of example (one of allowed types).")                        
    value_base_64_binary = fields.Float(
        string="Value Base 64 Binary",
         help="Base 64 Binary value of example (one of allowed types).")                        
    value_coding = fields.Float(
        string="Value Coding", 
        help="Coding value of example (one of allowed types).")                        
    value_codeable_concept = fields.Float(
        string="Value Codeable Concept", 
        help="Codeable Concept value of example (one of allowed types).")                        
    value_attachment = fields.Float(
        string="Value Attachment", 
        help="Attachment value of example (one of allowed types).")                        
    value_identifier = fields.Float(
        string="Value Identifier", 
        help="Identifier value of example (one of allowed types).")                        
    value_quantity = fields.Float(
        string="Value Quantity", 
        help="Quantity value of example (one of allowed types).")                        
    value_quantity_uom_id = fields.Many2one(
        comodel_name="product.uom", 
        string="Value Quantity UOM", 
        help="Quantity unit of measure.")                        
    value_range = fields.Float(
        string="Value Range", 
        help="Range value of example (one of allowed types).")                        
    value_range_uom_id = fields.Many2one(
        comodel_name="product.uom", 
        string="Value Range UOM", 
        help="Range unit of measure.")                        
    value_period = fields.Float(
        string="Value Period", 
        help="Period value of example (one of allowed types).")                        
    value_period_uom_id = fields.Many2one(
        comodel_name="product.uom", 
        string="Value Period UOM", 
        help="Period unit of measure.")                        
    value_numerator = fields.Float(
        string="Value Numerator", 
        help="Numerator value of value of example (one of allowed types).")
    value_numerator_uom_id = fields.Many2one(
        comodel_name="product.uom", 
        string="Value Numerator UOM", 
        help="Value numerator unit of measure.")
    value_denominator = fields.Float(
        string="Value Denominator", 
        help="Denominator value of value of example (one of allowed types).")
    value_denominator_uom_id = fields.Many2one(
        comodel_name="product.uom", 
        string="Value Denominator UOM", 
        help="Value denominator unit of measure.")
    value_ratio = fields.Float(
        string="Value Ratio", 
        compute="_compute_value_ratio", 
        store="True", 
        help="Ratio of value of example (one of allowed types).")
    value_ratio_uom = fields.Char(
        string="Value Ratio UOM", 
        compute="_compute_value_ratio_uom", 
        store="True", 
        help="Value Ratio unit of measure.")          
    value_human_name = fields.Float(
        string="Value Human Name", 
        help="Human Name value of example (one of allowed types).")                        
    value_address = fields.Float(
        string="Value Address", 
        help="Address value of example (one of allowed types).")                        
    value_contact_point = fields.Float(
        string="Value Contact Point", 
        help="Contact Point value of example (one of allowed types).")                        
    value_timing = fields.Float(
        string="Value Timing", 
        help="Timing value of example (one of allowed types).")                        
    value_signature = fields.Float(
        string="Value Signature", 
        help="Signature value of example (one of allowed types).")                        
    value_reference = fields.Float(
        string="Value Reference", 
        help="Reference value of example (one of allowed types).")                        

class ElementDefinitionConstraint(models.Model):    
    _name = "hc.element.definition.constraint"    
    _description = "Element Definition Constraint"                

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
        help="FluentPath expression of constraint.")                        
    xpath = fields.Char(
        string="Xpath", 
        help="XPath expression of constraint.")                        
    source = fields.Char(
        string="Source URI", 
        help="Reference to original source of constraint.")                        

class ElementDefinitionBinding(models.Model):    
    _name = "hc.element.definition.binding"    
    _description = "Element Definition Binding"                

    element_definition_id = fields.Many2one(
        comodel_name="hc.element.definition", 
        string="Element Definition", 
        help="Element Definition associated with this Element Definition Binding.")                        
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
    # value_set_id = fields.Many2one(
    #     comodel_name="hc.res.value.set", 
    #     string="Value Set", 
    #     help="Value Set the reference to the value set.")                        

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
    language_id = fields.Many2one(
        comodel_name="hc.vs.language", 
        string="Language", 
        help="Computable language of mapping.")                        
    map = fields.Char(
        string="Map", 
        required="True", 
        help="Details of the mapping.")                        

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

    slicing_id = fields.Many2one(
        comodel_name="hc.element.definition.slicing", 
        string="Slicing", 
        help="Slicing associated with this Element Definition Slicing Discriminator.")                 
    discriminator = fields.Char(
        string="Discriminator", 
        help="Discriminator associated with this Element Definition Slicing Discriminator.")                    

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

class ElementDefinitionCode(models.Model):    
    _name = "hc.vs.element.definition.code"    
    _description = "Element Definition Code"            
    _inherit = ["hc.value.set.contains"]    

