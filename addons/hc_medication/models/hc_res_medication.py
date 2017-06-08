# -*- coding: utf-8 -*-

from openerp import models, fields, api

class Medication(models.Model):    
    _name = "hc.res.medication"    
    _description = "Medication"            

    name = fields.Char(
        string="Name", 
        help="Common / Commercial name.")                    
    code_id = fields.Many2one(
        comodel_name="hc.vs.medication.code", 
        string="Code", 
        help="Codes that identify this medication.")                    
    is_brand = fields.Boolean(
        string="Is Brand", 
        help="True if a brand.")                    
    manufacturer_id = fields.Many2one(
        comodel_name="hc.res.organization", 
        string="Manufacturer", 
        help="Manufacturer of the item.")                    
    product_ids = fields.One2many(
        comodel_name="hc.medication.product", 
        inverse_name="medication_id", 
        string="Products", 
        help="Administrable medication details.")                    
    package_ids = fields.One2many(
        comodel_name="hc.medication.package", 
        inverse_name="medication_id", 
        string="Packages", 
        help="Details about packaged medications.")                    

class MedicationProduct(models.Model):    
    _name = "hc.medication.product"    
    _description = "Medication Product"            

    medication_id = fields.Many2one(
        comodel_name="hc.res.medication", 
        string="Product Medication", 
        help="Medication associated with this Product.")                    
    form_id = fields.Many2one(
        comodel_name="hc.vs.medication.form.code", 
        string="Product Form", 
        help="Describes the form of the item. Powder; tablets; carton.")                    
    batch_ids = fields.One2many(
        comodel_name="hc.medication.product.batch", 
        inverse_name="medication_product_id", 
        string="Batches", 
        help="A group of medication produced or packaged from one production run.")                    
    ingredient_ids = fields.One2many(
        comodel_name="hc.medication.product.ingredient", 
        inverse_name="medication_product_id", 
        string="Ingredients", 
        help="Active or inactive ingredient.")                    

class MedicationProductIngredient(models.Model):    
    _name = "hc.medication.product.ingredient"  
    _description = "Medication Product Ingredient"      

    medication_product_id = fields.Many2one(
        comodel_name="hc.medication.product", 
        string="Product", 
        help="Product associated with this Ingredient.")                     
    item_type = fields.Selection(
        string="Item Type",
        required="True",
        selection=[
            ("code", "Code"), 
            ("substance", "Substance"), 
            ("medication", "Medication")], 
        help="Type of the product contained.")                    
    item_name = fields.Char(
        string="Item", 
        compute="compute_item_name", 
        help="The product contained.")                    
    item_code_id = fields.Many2one(
        comodel_name="hc.vs.medication.ingredient.code", 
        string="Item Code", 
        help="Code of product contained.")                    
    item_substance_id = fields.Many2one(
        comodel_name="hc.res.substance", 
        string="Item Substance", 
        help="Substance product contained.")                    
    item_medication_id = fields.Many2one(
        comodel_name="hc.res.medication", 
        string="Item Medication", 
        help="Medication product contained.")                    
    amount_numerator = fields.Float(
        string="Amount Numerator", 
        help="Numerator value of quantity of ingredient present.")
    amount_numerator_uom_id = fields.Many2one(
        comodel_name="product.uom", 
        string="Amount Numerator UOM", 
        help="Amount Numerator unit of measure.")
    amount_denominator = fields.Float(
        string="Amount Denominator", 
        help="Denominator value of quantity of ingredient present.")
    amount_denominator_uom_id = fields.Many2one(
        comodel_name="product.uom", 
        string="Amount Denominator UOM", 
        help="Amount Denominator unit of measure.")
    amount = fields.Float(
        string="Amount", 
        compute="_compute_amount", 
        store="True", 
        help="Quantity of ingredient present.")
    amount_uom = fields.Char(
        string="Amount UOM", 
        compute="_compute_amount_uom", 
        store="True", 
        help="Amount unit of measure. For example, 250 mg per tablet.")
 
    has_amount_numerator = fields.Boolean(      
        string='Has Amount_Numerator',  
        invisible=True, 
        help="Indicates if amount_numerator exists. Used to enforce constraint amount_denominator and amount_numerator.")   
        
    @api.onchange('amount_numerator')       
    def onchange_amount_numerator(self):        
        if self.amount_numerator:   
            self.amount_denominator = True
            self.has_amount_numerator = True
        else:   
            self.has_amount_numerator = False

    @api.depends('amount_numerator', 'amount_denominator')        
    def _compute_amount(self):        
        if self.amount_numerator and self.amount_denominator:    
            self.amount = self.amount_numerator / self.amount_denominator
        
    @api.depends('amount_numerator_uom_id', 'amount_denominator_uom_id')        
    def _compute_amount_uom(self):        
        amount_uom = ''    
        if self.amount_numerator_uom_id:    
            amount_uom += self.amount_numerator_uom_id.name
        if self.amount_denominator_uom_id:    
            amount_uom += (' per ' + self.amount_denominator_uom_id.name) if self.amount_numerator_uom_id else self.amount_denominator_uom_id.name
        self.amount_uom = amount_uom

    @api.depends('item_type')           
    def _compute_item_name(self):           
        for hc_medication_product_ingredient in self:       
            if hc_medication_product_ingredient.item_type == 'code':    
                hc_medication_product_ingredient.item_name = hc_medication_product_ingredient.item_code_id.name
            elif hc_medication_product_ingredient.item_type == 'substance': 
                hc_medication_product_ingredient.item_name = hc_medication_product_ingredient.item_substance_id.name
            elif hc_medication_product_ingredient.item_type == 'medication':    
                hc_medication_product_ingredient.item_name = hc_medication_product_ingredient.item_medication_id.name

class MedicationProductBatch(models.Model): 
    _name = "hc.medication.product.batch"   
    _description = "Medication Product Batch"

    medication_product_id = fields.Many2one(
        comodel_name="hc.medication.product", 
        string="Product", 
        help="Product associated with this Batch.")                    
    lot_number = fields.Char(
        string="Lot Number", 
        help="The assigned lot number of a batch of the specified product.")                    
    expiration_date = fields.Date(
        string="Expiration Date", 
        help="When this specific batch of product will expire.")                    

class MedicationPackage(models.Model):    
    _name = "hc.medication.package"    
    _description = "Medication Package"

    medication_id = fields.Many2one(
        comodel_name="hc.res.medication", 
        string="Medication", 
        help="Medication associated with this Package.")                    
    container_id = fields.Many2one(
        comodel_name="hc.vs.medication.package.container", 
        string="Container", 
        help="The kind of container that this package comes as (e.g., box, vial, blister-pack).")                    
    content_ids = fields.One2many(
        comodel_name="hc.medication.package.content", 
        inverse_name="medication_package_id", 
        string="Contents", 
        help="What is in the package?")                    

class MedicationPackageContent(models.Model):   
    _name = "hc.medication.package.content" 
    _description = "Medication Package Content"

    medication_package_id = fields.Many2one(
        comodel_name="hc.medication.package", 
        string="Package", 
        help="Package associated with this Content.")                    
    item_type = fields.Selection(
        string="Item Type", 
        required="True", 
        selection=[
            ("code", "Code"), 
            ("medication", "Medication")], 
        help="Type of the item in the package.")
    item_name = fields.Char(
        string="Item", 
        compute="_compute_item_name", 
        store="True", 
        help="The item in the package.")
    item_code_id = fields.Many2one(
        comodel_name="hc.vs.medication.ingredient.code", 
        string="Item Code", 
        help="Code of the item in the package.")
    item_medication_id = fields.Many2one(
        comodel_name="hc.res.medication", 
        string="Item Medication", 
        help="Medication item in the package.")                 
    amount = fields.Float(
        string="Amount", 
        help="How many are in the package?")                    
    amount_uom_id = fields.Many2one(
        comodel_name="product.uom", 
        string="Amount UOM", 
        help="Amount unit of measure.")                    

    @api.depends('item_type')           
    def _compute_item_name(self):           
        for hc_medication_product_ingredient in self:       
            if hc_medication_product_ingredient.item_type == 'code':    
                hc_medication_product_ingredient.item_name = hc_medication_product_ingredient.item_code_id.name
            elif hc_medication_product_ingredient.item_type == 'medication':    
                hc_medication_product_ingredient.item_name = hc_medication_product_ingredient.item_medication_id.name

class MedicationCode(models.Model):    
    _name = "hc.vs.medication.code"    
    _description = "Medication Code"        
    _inherit = ["hc.value.set.contains"]

    name = fields.Char(
        string="Name", 
        help="Name of this medication.")
    code = fields.Char(
        string="Code", 
        help="Code of this medication.")
    contains_id = fields.Many2one(
        comodel_name="hc.vs.medication.code", 
        string="Parent",
        help="Parent concept.")    

class MedicationFormCode(models.Model):    
    _name = "hc.vs.medication.form.code"    
    _description = "Medication Form Code"        
    _inherit = ["hc.value.set.contains"]

    name = fields.Char(
        string="Name", 
        help="Name of this medication form.")
    code = fields.Char(
        string="Code", 
        help="Code of this medication form.")
    contains_id = fields.Many2one(
        comodel_name="hc.vs.medication.form.code", 
        string="Parent",
        help="Parent concept.")
    form_group_ids = fields.Many2many(
        comodel_name="hc.vs.medication.form.group.code", 
        relation="medication_form_code_form_group_rel", 
        string="Form Groups", 
        help="Dose Form Group associated with this Dose Form.")

class MedicationFormGroupCode(models.Model):    
    _name = "hc.vs.medication.form.group.code"  
    _description = "Medication Form Group Code"         
    _inherit = ["hc.value.set.contains"]

    name = fields.Char(
        string="Name", 
        help="Name of this medication form group.")
    code = fields.Char(
        string="Code", 
        help="Code of this medication form group.")
    contains_id = fields.Many2one(
        comodel_name="hc.vs.medication.form.group.code", 
        string="Parent",
        help="Parent concept.")

class MedicationIngredientCode(models.Model):    
    _name = "hc.vs.medication.ingredient.code"    
    _description = "Medication Ingredient Code"        
    _inherit = ["hc.value.set.contains"]

    name = fields.Char(
        string="Name", 
        help="Name of this ingredient.")
    code = fields.Char(
        string="Code", 
        help="Code of this ingredient.")
    contains_id = fields.Many2one(
        comodel_name="hc.vs.medication.ingredient.code", 
        string="Parent",
        help="Parent concept.")

class MedicationPackageContainer(models.Model):    
    _name = "hc.vs.medication.package.container"    
    _description = "Medication Package Container"        
    _inherit = ["hc.value.set.contains"]

    name = fields.Char(
        string="Name", 
        help="Name of this medication package container.")
    code = fields.Char(
        string="Code", 
        help="Code of this medication package container.")
    contains_id = fields.Many2one(
        comodel_name="hc.vs.medication.package.container", 
        string="Parent",
        help="Parent concept.")    
