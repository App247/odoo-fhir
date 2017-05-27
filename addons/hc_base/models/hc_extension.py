# -*- coding: utf-8 -*-

from openerp import models, fields, api

class Extension(models.Model): 
    _name = "hc.extension"    
    _description = "Extension"

    url = fields.Char(
        string="URI", 
        required="True", 
        help="URI that identifies the meaning of the extension.")
    value_type = fields.Selection(
        string="Value Type", 
        selection=[
            ("integer", "Integer"), 
            ("unsigned_int", "Unsigned Int"),
            ("positive_int", "Positive Int"), 
            ("decimal", "Decimal"),
            ("date_time", "Date Time"),
            ("date", "Date"),
            ("time", "Time"),
            ("instant", "Instant"),
            ("string", "String"),
            ("uri", "URI"),
            ("oid", "OID"),
            ("uuid", "UUID"),
            ("id", "ID"),
            ("boolean", "Boolean"),
            ("code", "Code"),
            ("markdown", "Markdown"),
            ("base_64_binary", "Base 64 Binary"),
            ("coding", "Coding"),
            ("codeable_concept", "Codeable Concept"), 
            ("attachment", "Attachment"),
            ("identifier", "Identifier"),
            ("quantity", "Quantity"),
            ("sample_data", "Sample Data"),
            ("range", "Range"),
            ("period", "Period"),
            ("ratio", "Ratio"), 
            ("human_name", "Human Name"),
            ("address", "Address"),
            ("contact_point", "Contact Point"),
            ("timing", "Timing"),
            ("Reference", "Reference"),
            ("annotation", "Annotation"),
            ("signature", "Signature"),
            ("meta", "Meta")],
            help="Type of value of extension.")
    value_name = fields.Char(
        string="Value", 
        compute="_compute_value_name", 
        store="True", 
        help="Value of extension.")
    value_integer = fields.Integer(
        string="Value Integer", 
        help="Integer value of extension.")
    value_unsigned_int = fields.Integer(
        string="Value Unsigned Integer", 
        help="Unsigned Integer value of extension.")
    value_positive_int = fields.Integer(
        string="Value Positive Integer", 
        help="Positive Integer value of extension.")
    value_decimal = fields.Float(
        string="Value Decimal", 
        help="Decimal value of extension.")
    value_date_time = fields.Datetime(
        string="Value Date Time", 
        help="Date Time value of extension.")
    value_date = fields.Date(
        string="Value Date", 
        help="Date value of extension.")
    value_instant = fields.Datetime(
        string="Value Instant", 
        help="Instant value of extension.")
    value_string = fields.Char(
        string="Value String", 
        help="String value of extension.")
    value_uri = fields.Char(
        string="Value URI", 
        help="URI value of extension.")
    value_oid = fields.Char(
        string="Value OID", 
        help="OID value of extension.")
    value_uuid = fields.Char(
        string="Value UUUID", 
        help="UUUID value of extension.")
    value_id = fields.Char(
        string="Value Id", 
        help="Id value of extension.")
    value_boolean = fields.Boolean(
        string="Value Boolean", 
        help="Boolean value of extension.")
    value_code_id = fields.Many2one(
        comodel_name="hc.vs.extension.code", 
        string="Value Code", 
        help="Code value of extension.")
    value_markdown = fields.Text(
        string="Value Markdown", 
        help="Markdown value of extension.")
    value_base_64_binary = fields.Binary(
        string="Value Base 64 Binary", 
        help="Base 64 Binary value of extension.")
    value_coding_id = fields.Many2one(
        comodel_name="hc.vs.extension.coding", 
        string="Value Coding", 
        help="Coding value of extension.")
    value_codeable_concept_id = fields.Many2one(
        comodel_name="hc.vs.extension.codeable.concept", 
        string="Value Codeable Concept", 
        help="Codeable Concept value of extension.")
    value_attachment_id = fields.Many2one(
        comodel_name="hc.extension.attachment", 
        string="Value Attachment", 
        help="Attachment value of extension.")
    value_identifier_id = fields.Many2one(
        comodel_name="hc.extension.identifier", 
        string="Value Identifier", 
        help="Identifier value of extension.")
    value_quantity = fields.Float(
        string="Value Quantity", 
        help="Quantity value of extension.")
    value_quantity_uom_id = fields.Many2one(
        comodel_name="product.uom", 
        string="Value Quantity UOM", 
        help="Quantity unit of measure.")
    value_sampled_data = fields.Many2one(
        comodel_name="hc.extension.sampled.data", 
        string="Value Sampled Data", 
        help="Sampled Data value of extension.")
    value_range_low = fields.Float(
        string="Value Range Low", 
        help="Low limit of range value of extension.")
    value_range_high = fields.Float(
        string="Value Range High", 
        help="High limit of range value of extension.")
    value_range_uom_id = fields.Many2one(
        comodel_name="product.uom", 
        string="Value Range UOM", 
        help="Range unit of measure.")
    value_period_start_date = fields.Datetime(
        string="Value Period Start Date", 
        help="Start of the period for value of extension.")
    value_period_end_date = fields.Datetime(
        string="Value Period End Date", 
        help="End of the period for value of extension.")
    value_period_uom_id = fields.Many2one(
        comodel_name="product.uom", 
        string="Value Period UOM", 
        help="Period unit of measure.")
    value_numerator = fields.Float(
        string="Value Numerator", 
        help="Numerator value of value of extension.")
    value_numerator_uom_id = fields.Many2one(
        comodel_name="product.uom", 
        string="Value Numerator UOM", 
        help="Value numerator unit of measure.")
    value_denominator = fields.Float(
        string="Value Denominator", 
        help="Denominator value of value of extension.")
    value_denominator_uom_id = fields.Many2one(
        comodel_name="product.uom", 
        string="Value Denominator UOM", 
        help="Value denominator unit of measure.")
    value_ratio = fields.Float(
        string="Value Ratio", 
        compute="_compute_value_ratio", 
        store="True", 
        help="Ratio of value of extension.")
    value_ratio_uom = fields.Char(
        string="Value Ratio UOM", 
        compute="_compute_value_ratio_uom", 
        store="True", 
        help="Value Ratio unit of measure.")
    value_human_name_id = fields.Many2one(
        comodel_name="hc.extension.human.name", 
        string="Value Human Name", 
        help="Human Name value of extension.")
    value_address_id = fields.Many2one(
        comodel_name="hc.extension.address", 
        string="Value Address", 
        help="Address value of extension.")
    value_contact_point_id = fields.Many2one(
        comodel_name="hc.extension.telecom", 
        string="Value Contact Point", 
        help="Contact Point (Telecom) value of extension.")
    value_timing_id = fields.Many2one(
        comodel_name="hc.extension.timing", 
        string="Value Timing", 
        help="Timing value of extension.")
    value_reference_id = fields.Many2one(
        comodel_name="hc.extension.reference", 
        string="Value Reference", 
        help="Reference value of extension.")
    value_annotation_id = fields.Many2one(
        comodel_name="hc.extension.annotation", 
        string="Value Annotation", 
        help="Annotation value of extension.")
    value_signature_id = fields.Many2one(
        comodel_name="hc.extension.signature", 
        string="Value Signature", 
        help="Signature value of extension.")
    value_meta_id = fields.Many2one(
        comodel_name="hc.extension.meta", 
        string="Value Meta", 
        help="Meta value of extension.")

class ExtensionAttachment(models.Model):    
    _name = "hc.extension.attachment"   
    _description = "Extension Attachment"           
    _inherit = ["hc.basic.association", "hc.attachment"]    

class ExtensionIdentifier(models.Model):    
    _name = "hc.extension.identifier"   
    _description = "Extension Identifier"           
    _inherit = ["hc.basic.association", "hc.identifier"]    

class ExtensionSampledData(models.Model):   
    _name = "hc.extension.sampled.data" 
    _description = "Extension Sampled Data"         
    _inherit = ["hc.basic.association", "hc.sampled.data"]  

class ExtensionHumanName(models.Model): 
    _name = "hc.extension.human.name"   
    _description = "Extension Human Name"           
    _inherit = ["hc.human.name.use"]   
    _inherits = {"hc.human.name": "name_id"}

    name_id = fields.Many2one(
        comodel_name="hc.human.name", 
        string="Name", 
        ondelete="restrict", 
        required="True", 
        help="Name associated with this Extension Human Name.")                        
                        
class ExtensionAddress(models.Model):   
    _name = "hc.extension.address"  
    _description = "Extension Address"          
    _inherit = ["hc.address.use"]   
    _inherits = {"hc.address": "address_id"}

    address_id = fields.Many2one(
        comodel_name="hc.address", 
        string="Address", 
        ondelete="restrict", 
        required="True", 
        help="Address associated with this Extension Address.")                     
                        
class ExtensionTelecom(models.Model):   
    _name = "hc.extension.telecom"  
    _description = "Extension Telecom"          
    _inherit = ["hc.contact.point.use"] 
    _inherits = {"hc.contact.point": "telecom_id"}

    telecom_id = fields.Many2one(
        comodel_name="hc.contact.point", 
        string="Telecom", 
        ondelete="restrict", 
        required="True", 
        help="Telecom associated with this Extension Telecom.")                       

class ExtensionTiming(models.Model):    
    _name = "hc.extension.timing"   
    _description = "Extension Timing"           
    _inherit = ["hc.basic.association", "hc.timing"]    

class ExtensionReference(models.Model): 
    _name = "hc.extension.reference"    
    _description = "Extension Reference"            
    _inherit = ["hc.basic.association", "hc.reference"] 

class ExtensionAnnotation(models.Model):    
    _name = "hc.extension.annotation"   
    _description = "Extension Annotation"           
    _inherit = ["hc.basic.association", "hc.annotation"]    

class ExtensionSignature(models.Model): 
    _name = "hc.extension.signature"    
    _description = "Extension Signature"            
    _inherit = ["hc.basic.association", "hc.signature"] 

class ExtensionMeta(models.Model):  
    _name = "hc.extension.meta" 
    _description = "Extension Meta"         
    _inherit = ["hc.basic.association", "hc.meta"]  

class ExtensionCoding(models.Model):    
    _name = "hc.vs.extension.coding"    
    _description = "Extension Coding"           
    _inherit = ["hc.value.set.contains"]    

class ExtensionCodeableConcept(models.Model):   
    _name = "hc.vs.extension.codeable.concept"  
    _description = "Extension Codeable Concept"         
    _inherit = ["hc.value.set.contains"]    

class ExtensionCode(models.Model):    
    _name = "hc.vs.extension.code"    
    _description = "Extension Code"
    _inherit = ["hc.value.set.contains"]

    name = fields.Char(
        string="Name", 
        help="Name of this extension code.")        
    code = fields.Char(
        string="Code", 
        help="Code of this extension code.")        
    contains_id = fields.Many2one(
        comodel_name="hc.vs.extension.code", 
        string="Contains", 
        help="Parent extension code.")

class ExtensionCoding(models.Model):    
    _name = "hc.vs.extension.coding"    
    _description = "Extension Coding"
    _inherit = ["hc.value.set.contains"]

    name = fields.Char(
        string="Name", 
        help="Name of this extension coding.")        
    code = fields.Char(
        string="Code", 
        help="Code of this extension coding.")        
    contains_id = fields.Many2one(
        comodel_name="hc.vs.extension.coding", 
        string="Contains", 
        help="Parent extension coding.")        

class ExtensionCodeableConcept(models.Model):   
    _name = "hc.vs.extension.codeable.concept"  
    _description = "Extension Codeable Concept"
    _inherit = ["hc.value.set.contains"]

    name = fields.Char(
        string="Name", 
        help="Name of this extension codeable concept.")      
    code = fields.Char(
        string="Code", 
        help="Code of this extension codeable concept.")      
    contains_id = fields.Many2one(
        comodel_name="hc.vs.extension.codeable.concept", 
        string="Contains", 
        help="Parent extension codeable concept.")        



