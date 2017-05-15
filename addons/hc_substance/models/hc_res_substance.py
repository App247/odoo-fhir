# -*- coding: utf-8 -*-

from openerp import models, fields, api

class Substance(models.Model):    
    _name = "hc.res.substance"    
    _description = "Substance"        

    name = fields.Char(
        string="Event Name", 
        required="True", 
        help="Human-readable label for this substance.")
    identifier_ids = fields.One2many(
        comodel_name="hc.substance.identifier", 
        inverse_name="substance_id", 
        string="Identifiers", 
        help="Unique identifier.")                
    status = fields.Selection(
        string="Status", 
        selection=[
            ("active", "Active"), 
            ("inactive", "Inactive"), 
            ("entered-in-error", "Entered-In-Error")], 
        help="The status of this activity definition. Enables tracking the life-cycle of the content.")
    category_ids = fields.Many2many(
        comodel_name="hc.vs.substance.category", 
        string="Categories", 
        help="What class/type of substance this is.")                
    code_id = fields.Many2one(
        comodel_name="hc.vs.substance.code", 
        string="Code", 
        required="True", 
        help="What substance this is.")                
    description = fields.Text(
        string="Description", 
        help="Textual description of the substance, comments.")                
    instance_ids = fields.One2many(
        comodel_name="hc.substance.instance", 
        inverse_name="substance_id", 
        string="Instances", 
        help="If this describes a specific package/container of the substance.")
    ingredient_ids = fields.One2many(
        comodel_name="hc.substance.ingredient", 
        inverse_name="substance_id", 
        string="Ingredients", 
        help="Composition information about the substance.")

class SubstanceInstance(models.Model):    
    _name = "hc.substance.instance"    
    _description = "Substance Instance"        

    substance_id = fields.Many2one(
        comodel_name="hc.res.substance", 
        string="Substance", 
        help="Substance associated with this Instance.")                
    identifier_id = fields.Many2one(
        comodel_name="hc.substance.instance.identifier", 
        string="Identifier", 
        help="Identifier of the package/container.")
    expiry = fields.Datetime(
        string="Expiry Date", 
        help="When no longer valid to use.")                
    quantity = fields.Float(
        string="Quantity", 
        help="Amount of substance in the package.")
    quantity_uom_id = fields.Many2one(
        comodel_name="product.uom", 
        string="Quantity UOM", 
        help="Quantity unit of measure.")
                
class SubstanceIngredient(models.Model):    
    _name = "hc.substance.ingredient"   
    _description = "Substance Ingredient"       

    substance_id = fields.Many2one(
        comodel_name="hc.res.substance", 
        string="Substance", 
        help="Substance associated with this Ingredient.")                         
    quantity_numerator = fields.Float(
        string="Quantity Numerator", 
        help="Numerator value of optional amount (concentration).")              
    quantity_numerator_uom_id = fields.Many2one(
        comodel_name="product.uom", 
        string="Quantity Numerator UOM", 
        help="Quantity Numerator unit of measure.")
    quantity_denominator = fields.Float(
        string="Quantity Denominator", 
        help="Denominator value of optional amount (concentration).")                
    quantity_denominator_uom_id = fields.Many2one(
        comodel_name="product.uom", 
        string="Quantity Denominator UOM", 
        help="Quantity Denominator unit of measure.")
    quantity_ratio = fields.Float(
        string="Quantity Ratio", 
        compute="_compute_quantity_ratio",
        store="True", 
        help="Optional amount (concentration).")
    quantity_ratio_uom_id = fields.Many2one(
        comodel_name="product.uom", 
        string="Quantity Ratio UOM", 
        help="Optional amount (concentration) unit of measure.")
    substance_type = fields.Selection(
        string="Substance Type", 
        required="True", 
        selection=[
            ("code", "Code"), 
            ("substance", "Substance")], 
        help="Type of component of the substance.")               
    substance_name = fields.Char(
        string="Substance", 
        compute="_compute_substance_name", 
        store="True", 
        help="A component of the substance.")              
    substance_code_id = fields.Many2one(
        comodel_name="hc.vs.substance.code", 
        string="Substance Code", 
        help="Code of a component of the substance.")              
    substance_id = fields.Many2one(
        comodel_name="hc.res.substance", 
        string="Substance", 
        help="Substance component of the substance.")              

    @api.multi          
    def _compute_substance_name(self):          
        for hc_res_substance in self:       
            if hc_res_substance.substance_type == 'code':   
                hc_res_substance.substance_name = hc_res_substance.substance_codeable_concept_id.name
            elif hc_res_substance.substance_type == 'substance':    
                hc_res_substance.substance_name = hc_res_substance.substance_substance_id.name

class SubstanceIdentifier(models.Model):    
    _name = "hc.substance.identifier"    
    _description = "Substance Identifier"        
    _inherit = ["hc.basic.association", "hc.identifier"]

    substance_id = fields.Many2one(
        comodel_name="hc.res.substance", 
        string="Substance", 
        help="Substance associated with this identifier.")                

class SubstanceInstanceIdentifier(models.Model):    
    _name = "hc.substance.instance.identifier"    
    _description = "Substance Instance Identifier"        
    _inherit = ["hc.basic.association", "hc.identifier"]    

class SubstanceCategory(models.Model):    
    _name = "hc.vs.substance.category"    
    _description = "Substance Category"        
    _inherit = ["hc.value.set.contains"]

    name = fields.Char(
        string="Name", 
        help="Name of this substance category.")
    code = fields.Char(
        string="Code", 
        help="Code of this substance category.")
    snomed_code = fields.Char(
        string="SNOMED Code", 
        help="SNOMED code of this substance category.")
    snomed_definition = fields.Char(
        string="SNOMED Definition", 
        help="SNOMED fully-specified name of this substance category.")
    contains_id = fields.Many2one(
        comodel_name="hc.vs.substance.category", 
        string="Parent", 
        help="Parent substance category.")

class SubstanceCode(models.Model):  
    _name = "hc.vs.substance.code"  
    _description = "Substance Code"     
    _inherit = ["hc.value.set.contains"]    

    name = fields.Char(
        string="Name", 
        help="Name of this substance code.")
    code = fields.Char(
        string="Code", 
        help="Code of this substance code.")
    contains_id = fields.Many2one(
        comodel_name="hc.vs.substance.code",
        string="Parent", 
        help="Parent substance code.")
    child_ids = fields.One2many(
        comodel_name="hc.vs.substance.code", 
        inverse_name="contains_id", 
        string="Children", 
        help="Child concept.")
    # parent_substance_code_id = fields.Many2one(
    #     comodel_name="hc.parent.substance.code", 
    #     string="Parent", 
    #     help="Substance associated with this Parent Substance.")
    parent_ids = fields.One2many(
        comodel_name="hc.vs.substance.code", 
        inverse_name="contains_id", 
        string="Parents", 
        help="Parent concept.")

    # parent_ids = fields.One2many(
    #     comodel_name="hc.substance.association", 
    #     inverse_name="contains_id", 
    #     string="Parents", 
    #     help="Parent substance code.")                    
    # child_ids = fields.One2many(
    #     comodel_name="hc.substance.association", 
    #     inverse_name="child_id", 
    #     string="Children", 
    #     help="Child substance code.")

# class SubstanceAssociation(models.Model):   
#     _name = "hc.substance.association"
#     _description = "Substance Association"
#     _inherit = ["hc.basic.association"]

#     parent_id = fields.Many2one(
#         comodel_name="hc.vs.substance.code", 
#         string="Parent", 
#         help="Parent substance of this Substance.")                    
#     child_id = fields.Many2one(
#         comodel_name="hc.vs.substance.code", 
#         string="Child", 
#         help="Child substance of this substance.")                   
#     child_level = fields.Integer(
#         string="Level",
#         related="parent_id.child_level", 
#         help="Level as child in a hierarch of codes.")

# class ParentSubstanceCode(models.Model):
#     _name = "hc.parent.substance.code"
#     _description = "Parent Substance Code"
#     _inherit = ["hc.value.set.contains"]
#     # _inherits = {"hc.vs.substance.code": "substance_code_id"}

#     # substance_id = fields.Many2one(
#     #     comodel_name="hc.vs.substance.code", 
#     #     string="Substance", 
#     #     help="Substance associated with this Parent Substance.")
#     name = fields.Char(
#         string="Name", 
#         help="Name of this parent substance code.")
#     code = fields.Char(
#         string="Code", 
#         help="Code of this parent substance code.")
#     contains_id = fields.Many2one(
#         comodel_name="hc.parent.substance.code",
#         string="Parent", 
#         help="Parent of parent substance code.")
    # child_ids = fields.One2many(
    #     comodel_name="hc.vs.substance.code",
    #     inverse="parent_substance_code_id", 
    #     string="Children", 
    #     help="Child substance code.")

# class SubstanceCode(models.Model):  
#     _inherit = "hc.vs.substance.code"

    # parent_ids = fields.One2many(
    #     comodel_name="hc.parent.substance.code", 
    #     inverse_name="substance_id", 
    #     string="Parents", 
    #     help="Parent substance code.")
    # parent_substance_code_id = fields.Many2one(
    #     comodel_name="hc.parent.substance.code", 
    #     string="Substance Code", 
    #     help="Parent Substance Code associated with this Substance Code.")



# class ParentSubstanceCode(models.Model):
#     _inherit = "hc.parent.substance.code"

#     substance_id = fields.Many2one(
#         comodel_name="hc.vs.substance.code", 
#         string="Substance", 
#         help="Substance associated with this Parent Substance.")