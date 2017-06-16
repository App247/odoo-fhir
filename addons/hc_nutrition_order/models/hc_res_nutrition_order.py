# -*- coding: utf-8 -*-

from openerp import models, fields, api

class NutritionOrder(models.Model):
    _name = "hc.res.nutrition.order"
    _description = "Nutrition Order"

    name = fields.Char(
        string="Event Name", 
        compute="_compute_name", 
        store="True", 
        help="Text representation of the nutrition order event. Patient Name + DOB + Orderer + Date.")
    identifier_ids = fields.One2many(
        comodel_name="hc.nutrition.order.identifier", 
        inverse_name="nutrition_order_id", 
        string="Identifiers", 
        help="Identifiers assigned to this order.")
    status = fields.Selection(
        string="Status", 
        selection=[
            ("proposed", "Proposed"), 
            ("draft", "Draft"), 
            ("planned", "Planned"), 
            ("requested", "Requested"), 
            ("active", "Active"), 
            ("on-hold", "On-Hold"), 
            ("completed", "Completed"), 
            ("cancelled", "Cancelled")], 
        help="The workflow status of the nutrition order/request.")
    patient_id = fields.Many2one(
        comodel_name="hc.res.patient", 
        string="Patient", 
        required="True", 
        help="The person who requires the diet, formula or nutritional supplement.")
    encounter_id = fields.Many2one(
        comodel_name="hc.res.encounter", 
        string="Encounter", 
        help="Encounter.")
    date_time = fields.Datetime(
        string="Date Time", 
        required="True", 
        help="Date and time the nutrition order was requested.")
    orderer_id = fields.Many2one(
        comodel_name="hc.res.practitioner", 
        string="Orderer", 
        help="Who ordered the diet, formula or nutritional supplement.")
    allergy_intolerance_ids = fields.One2many(
        comodel_name="hc.nutrition.order.allergy.intolerance", 
        inverse_name="nutrition_order_id", 
        string="Allergy Intolerances", 
        help="List of the patient's food and nutrition-related allergies and intolerances.")
    food_preference_modifier_ids = fields.Many2many(
        comodel_name="hc.vs.encounter.diet", 
        relation="nutrition_order_food_preference_modifier_rel", 
        string="Food Preference Modifiers", 
        help="Order-specific modifier about the type of food that should be given.")
    exclude_food_modifier_ids = fields.Many2many(
        comodel_name="hc.vs.food.type", 
        relation="nutrition_order_exclude_food_modifier_rel", 
        string="Exclude Food Modifiers", 
        help="Order-specific modifier about the type of food that should not be given.")
    oral_diet_ids = fields.One2many(
        comodel_name="hc.nutrition.order.oral.diet", 
        inverse_name="nutrition_order_id", 
        string="Oral Diets", 
        help="Oral diet components.")
    supplement_ids = fields.One2many(
        comodel_name="hc.nutrition.order.supplement", 
        inverse_name="nutrition_order_id", 
        string="Supplements", 
        help="Supplement components.")
    enteral_formula_ids = fields.One2many(
        comodel_name="hc.nutrition.order.enteral.formula", 
        inverse_name="nutrition_order_id", 
        string="Enteral Formulas", 
        help="Enteral formula components.")

class NutritionOrderOralDiet(models.Model):
    _name = "hc.nutrition.order.oral.diet"
    _description = "Nutrition Order Oral Diet"

    nutrition_order_id = fields.Many2one(
        comodel_name="hc.res.nutrition.order", 
        string="Nutrition Order", 
        help="Nutrition Order associated with this Nutrition Order Oral Diet.")
    type_ids = fields.Many2many(
        comodel_name="hc.vs.diet.type", 
        relation="nutrition_order_oral_diet_type_rel", 
        string="Types", 
        help="Type of oral diet or diet restrictions that describe what can be consumed orally.")
    schedule_ids = fields.One2many(
        comodel_name="hc.nutrition.order.oral.diet.schedule", 
        inverse_name="oral_diet_id", 
        string="Schedules", 
        help="Scheduled frequency of diet.")
    fluid_consistency_type_ids = fields.Many2many(
        comodel_name="hc.vs.consistency.type", 
        relation="nutrition_order_oral_diet_fluid_consistency_type_rel", 
        string="Fluid Consistency Types", 
        help="The required consistency of fluids and liquids provided to the patient.")
    instruction = fields.Text(
        string="Instruction", 
        help="Instructions or additional information about the oral diet.")
    nutrient_ids = fields.One2many(
        comodel_name="hc.nutrition.order.oral.diet.nutrient", 
        inverse_name="oral_diet_id", 
        string="Nutrients", 
        help="Required nutrient modifications.")
    texture_ids = fields.One2many(
        comodel_name="hc.nutrition.order.oral.diet.texture", 
        inverse_name="oral_diet_id", 
        string="Textures", 
        help="Required texture modifications.")

class NutritionOrderOralDietNutrient(models.Model):
    _name = "hc.nutrition.order.oral.diet.nutrient"
    _description = "Nutrition Order Oral Diet Nutrient"

    oral_diet_id = fields.Many2one(
        comodel_name="hc.nutrition.order.oral.diet", 
        string="Oral Diet", 
        help="Oral Diet associated with this Nutrition Order Oral Diet Nutrient.")
    modifier_id = fields.Many2one(
        comodel_name="hc.vs.nutrient.code", 
        string="Modifier", 
        help="Type of nutrient that is being modified.")
    amount = fields.Float(
        string="Amount", 
        help="Quantity of the specified nutrient.")
    amount_uom_id = fields.Many2one(
        comodel_name="product.uom", 
        string="Amount UOM", 
        help="Quantity of the specified nutrient unit of measure.")
    
class NutritionOrderOralDietTexture(models.Model):
    _name = "hc.nutrition.order.oral.diet.texture"
    _description = "Nutrition Order Oral Diet Texture"
    
    oral_diet_id = fields.Many2one(
        comodel_name="hc.nutrition.order.oral.diet", 
        string="Oral Diet", 
        help="Oral Diet associated with this Nutrition Order Oral Diet Texture.")
    modifier_id = fields.Many2one(
        comodel_name="hc.vs.texture.code", 
        string="Modifier", 
        help="Code to indicate how to alter the texture of the foods, e.g., pureed.")
    food_type_id = fields.Many2one(
        comodel_name="hc.vs.modified.food.type", 
        string="Food Type", 
        help="Concepts that are used to identify an entity that is ingested for nutritional purposes.")
    
class NutritionOrderSupplement(models.Model):
    _name = "hc.nutrition.order.supplement"
    _description = "Nutrition Order Supplement"
    
    nutrition_order_id = fields.Many2one(
        comodel_name="hc.res.nutrition.order", 
        string="Nutrition Order", 
        help="Nutrition Order associated with this Nutrition Order Supplement.")
    type_id = fields.Many2one(
        comodel_name="hc.vs.supplement.type", 
        string="Type", 
        help="Type of supplement product requested.")
    product_name = fields.Char(
        string="Product Name", 
        help="Product or brand name of the nutritional supplement.")
    schedule_ids = fields.One2many(
        comodel_name="hc.nutrition.order.supplement.schedule", 
        inverse_name="supplement_id", 
        string="Schedules", 
        help="Scheduled frequency of supplement." )
    quantity = fields.Float(
        string="Quantity", 
        help="Amount of the nutritional supplement.")
    quantity_uom_id = fields.Many2one(
        comodel_name="product.uom", 
        string="Quantity UOM", 
        help="Amount of the nutritional supplement unit of measure.")
    instruction = fields.Text(
        string="Instruction", 
        help="Instructions or additional information about the oral supplement.")
    
class NutritionOrderEnteralFormula(models.Model):
    _name = "hc.nutrition.order.enteral.formula"
    _description = "Nutrition Order Enteral Formula"
    
    nutrition_order_id = fields.Many2one(
        comodel_name="hc.res.nutrition.order", 
        string="Nutrition Order", 
        help="Nutrition Order associated with this Nutrition Order Enteral Formula.")
    base_formula_type_id = fields.Many2one(
        comodel_name="hc.vs.ent.formula.type", 
        string="Base Formula Type", 
        help="Type of enteral or infant formula.")
    base_formula_product_name = fields.Char(
        string="Base Formula Product Name", 
        help="Product or brand name of the enteral or infant formula.")
    additive_type_id = fields.Many2one(
        comodel_name="hc.vs.ent.formula.additive", 
        string="Additive Type", 
        help="Type of modular component to add to the feeding.")
    additive_product_name = fields.Char(
        string="Additive Product Name", 
        help="Product or brand name of the modular additive.")
    caloric_density = fields.Float(
        string="Caloric Density", 
        help="Amount of energy per specified volume that is required.")
    caloric_density_uom_id = fields.Many2one(
        comodel_name="product.uom", 
        string="Caloric Density UOM", 
        help="Amount of energy per specified volume that is required unit of measure.")
    route_of_administration_id = fields.Many2one(
        comodel_name="hc.vs.enteral.route", 
        string="Route Of Administration", 
        help="How the formula should enter the patient's gastrointestinal tract.")
    max_volume_to_deliver = fields.Float(
        string="Max Volume To Deliver", 
        help="Upper limit on formula volume per unit of time.")
    max_volume_to_deliver_uom_id = fields.Many2one(
        comodel_name="product.uom", 
        string="Max Volume To Deliver UOM", 
        help="Upper limit on formula volume per unit of time unit of measure.")
    administration_instruction = fields.Text(
        string="Administration Instruction", 
        help="Formula feeding instructions expressed as text.")
    administration_ids = fields.One2many(
        comodel_name="hc.nutrition.order.enteral.formula.administration", 
        inverse_name="enteral_formula_id", 
        string="Administrations", 
        help="Formula feeding instruction as structured data.")
    
class NutritionOrderEnteralFormulaAdministration(models.Model):
    _name = "hc.nutrition.order.enteral.formula.administration"
    _description = "Nutrition Order Enteral Formula Administration"
    
    enteral_formula_id = fields.Many2one(
        comodel_name="hc.nutrition.order.enteral.formula", 
        string="Enteral Formula", 
        help="Enteral Formula associated with this Nutrition Order Enteral Formula Administration.")
    schedule_id = fields.Many2one(
        comodel_name="hc.nutrition.order.enteral.formula.administration.schedule", 
        string="Schedule", 
        help="Scheduled frequency of enteral feeding.")
    quantity = fields.Float(
        string="Quantity", 
        help="The volume of formula to provide.")
    quantity_uom_id = fields.Many2one(
        comodel_name="product.uom", 
        string="Quantity UOM", 
        help="The volume of formula to provide unit of measure.")
    rate_type = fields.Selection(
        string="Rate Type", 
        selection=[("quantity", "Quantity"), ("ratio", "Ratio")], 
        help="Type of speed with which the formula is provided per period of time.")
    rate_name = fields.Char(
        string="Rate", 
        compute="_compute_rate_name", 
        store="True", 
        help="Speed with which the formula is provided per period of time.")
    rate = fields.Float(
        string="Rate", 
        help="Quantity speed with which the formula is provided per period of time.")
    rate_quantity_uom_id = fields.Many2one(
        comodel_name="product.uom", 
        string="Rate Quantity UOM", 
        help="Speed with which the formula is provided per period of time unit of measure.")
    rate_numerator = fields.Float(
        string="Rate Numerator", 
        help="Numerator value of speed with which the formula is provided per period of time.")
    rate_numerator_uom_id = fields.Many2one(
        comodel_name="product.uom", 
        string="Rate Numerator UOM", 
        help="Rate numerator unit of measure.")
    rate_denominator = fields.Float(
        string="Rate Denominator", 
        help="Denominator value of speed with which the formula is provided per period of time.")
    rate_denominator_uom_id = fields.Many2one(
        comodel_name="product.uom", 
        string="Rate Denominator UOM", 
        help="Rate denominator unit of measure.")
    rate_ratio = fields.Float(
        string="Rate Ratio", 
        compute="_compute_rate_ratio", 
        store="True", 
        help="Ratio of speed with which the formula is provided per period of time.")
    rate_ratio_uom = fields.Char(
        string="Rate Ratio UOM", 
        compute="_compute_rate_ratio_uom", 
        store="True", 
        help="Rate Ratio unit of measure.")
    
class NutritionOrderIdentifier(models.Model):
    _name = "hc.nutrition.order.identifier"
    _description = "Nutrition Order Identifier"
    _inherit = ["hc.basic.association", "hc.identifier"]

    nutrition_order_id = fields.Many2one(
        comodel_name="hc.res.nutrition.order", 
        string="Nutrition Order", 
        help="Nutrition Order associated with this Nutrition Order Identifier.")
    
class NutritionOrderAllergyIntolerance(models.Model):
    _name = "hc.nutrition.order.allergy.intolerance"
    _description = "Nutrition Order Allergy Intolerance"
    _inherit = ["hc.basic.association"]

    nutrition_order_id = fields.Many2one(
        comodel_name="hc.res.nutrition.order", 
        string="Nutrition Order", 
        help="Nutrition Order associated with this Nutrition Order Allergy Intolerance.")
    allergy_intolerance_id = fields.Many2one(
        comodel_name="hc.res.allergy.intolerance",
        string="Allergy Intolerance", 
        help="List of the patient's food and nutrition-related allergies and intolerances.")
    
class NutritionOrderOralDietSchedule(models.Model):
    _name = "hc.nutrition.order.oral.diet.schedule"
    _description = "Nutrition Order Oral Diet Schedule"
    _inherit = ["hc.basic.association", "hc.timing"]
    
    oral_diet_id = fields.Many2one(
        comodel_name="hc.nutrition.order.oral.diet", 
        string="Oral Diet", 
        help="Oral Diet associated with this Nutrition Order Oral Diet Schedule.")
    
class NutritionOrderSupplementSchedule(models.Model):
    _name = "hc.nutrition.order.supplement.schedule"
    _description = "Nutrition Order Supplement Schedule"
    _inherit = ["hc.basic.association", "hc.timing"]
    
    supplement_id = fields.Many2one(
        comodel_name="hc.nutrition.order.supplement", 
        string="Supplement", 
        help="Supplement associated with this Nutrition Order Supplement Schedule.")
    
class NutritionOrderEnteralFormulaAdministrationSchedule(models.Model): 
    _name = "hc.nutrition.order.enteral.formula.administration.schedule"
    _description = "Nutrition Order Enteral Formula Administration Schedule"
    _inherit = ["hc.basic.association", "hc.timing"]

class ConsistencyType(models.Model):
    _name = "hc.vs.consistency.type"
    _description = "Consistency Type"
    _inherit = ["hc.value.set.contains"]
    
    name = fields.Char(
        string="Name", 
        help="Name of this consistency type.")
    code = fields.Char(
        string="Code", 
        help="Code of this consistency type.")
    contains_id = fields.Many2one(
        comodel_name="hc.vs.consistency.type", 
        string="Parent", 
        help="Parent consistency type.")
    
class DietType(models.Model):
    _name = "hc.vs.diet.type"
    _description = "Diet Type"
    _inherit = ["hc.value.set.contains"]
    
    name = fields.Char(
        string="Name", 
        help="Name of this diet type.")
    code = fields.Char(
        string="Code", 
        help="Code of this diet type.")
    contains_id = fields.Many2one(
        comodel_name="hc.vs.diet.type", 
        string="Parent", 
        help="Parent diet type.")
    
class EnteralRoute(models.Model):
    _name = "hc.vs.enteral.route"
    _description = "Enteral Route"
    _inherit = ["hc.value.set.contains"]

    name = fields.Char(
        string="Name", 
        help="Name of this enteral route.")
    code = fields.Char(
        string="Code", 
        help="Code of this enteral route.")
    contains_id = fields.Many2one(
        comodel_name="hc.vs.enteral.route", 
        string="Parent", 
        help="Parent enteral route.")
    
class EntFormulaAdditive(models.Model):
    _name = "hc.vs.ent.formula.additive"
    _description = "Enteral Formula Additive"
    _inherit = ["hc.value.set.contains"]
    
    name = fields.Char(
        string="Name", 
        help="Name of this enteral formula additive.")
    code = fields.Char(
        string="Code", 
        help="Code of this enteral formula additive.")
    contains_id = fields.Many2one(
        comodel_name="hc.vs.ent.formula.additive", 
        string="Parent", 
        help="Parent enteral formula additive.")
    
class EntFormulaType(models.Model):
    _name = "hc.vs.ent.formula.type"
    _description = "Enteral Formula Type"
    _inherit = ["hc.value.set.contains"]
    
    name = fields.Char(
        string="Name", 
        help="Name of this enteral formula type.")
    code = fields.Char(
        string="Code", 
        help="Code of this enteral formula type.")
    contains_id = fields.Many2one(
        comodel_name="hc.vs.ent.formula.type", 
        string="Parent", 
        help="Parent enteral formula type.")
    
class FoodType(models.Model):
    _name = "hc.vs.food.type"
    _description = "Food Type"
    _inherit = ["hc.value.set.contains"]

    name = fields.Char(
        string="Name", 
        help="Name of this food type.")
    code = fields.Char(
        string="Code", 
        help="Code of this food type.")
    contains_id = fields.Many2one(
        comodel_name="hc.vs.food.type", 
        string="Parent", 
        help="Parent food type.")

class ModifiedFoodType(models.Model):
    _name = "hc.vs.modified.food.type"
    _description = "Modified Food Type"
    _inherit = ["hc.value.set.contains"]
    
    name = fields.Char(
        string="Name", 
        help="Name of this modified food type.")
    code = fields.Char(
        string="Code", 
        help="Code of this modified food type.")
    contains_id = fields.Many2one(
        comodel_name="hc.vs.modified.food.type", 
        string="Parent", 
        help="Parent modified food type.")

class NutrientCode(models.Model):
    _name = "hc.vs.nutrient.code"
    _description = "Nutrient Code"
    _inherit = ["hc.value.set.contains"]

    name = fields.Char(
        string="Name", 
        help="Name of this nutrient code.")
    code = fields.Char(
        string="Code", 
        help="Code of this nutrient code.")
    contains_id = fields.Many2one(
        comodel_name="hc.vs.nutrient.code", 
        string="Parent", 
        help="Parent nutrient code.")

class SupplementType(models.Model):
    _name = "hc.vs.supplement.type"
    _description = "Supplement Type"
    _inherit = ["hc.value.set.contains"]

    name = fields.Char(
        string="Name", 
        help="Name of this supplement type.")
    code = fields.Char(
        string="Code", 
        help="Code of this supplement type.")
    contains_id = fields.Many2one(
        comodel_name="hc.vs.supplement.type", 
        string="Parent", 
        help="Parent supplement type.")

class TextureCode(models.Model):
    _name = "hc.vs.texture.code"
    _description = "Texture Code"
    _inherit = ["hc.value.set.contains"]

    name = fields.Char(
        string="Name", 
        help="Name of this texture code.")
    code = fields.Char(
        string="Code", 
        help="Code of this texture code.")
    contains_id = fields.Many2one(
        comodel_name="hc.vs.texture.code", 
        string="Parent", 
        help="Parent texture code.")

