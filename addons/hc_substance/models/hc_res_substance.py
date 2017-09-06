# -*- coding: utf-8 -*-

from openerp import models, fields, api
from openerp.exceptions import ValidationError
from datetime import datetime
from openerp.tools import DEFAULT_SERVER_DATETIME_FORMAT as DTF

class Substance(models.Model):
    _name = "hc.res.substance"
    _description = "Substance"
    _inherit = ["hc.domain.resource"]
    _rec_name = "name"

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
    status_history_ids = fields.One2many(
        comodel_name="hc.substance.status.history",
        inverse_name="substance_id",
        string="Status History",
        help="The status of the substance over time.")
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

    @api.model
    def create(self, vals):
        status_history_obj = self.env['hc.substance.status.history']
        res = super(Substance, self).create(vals)
        if vals and vals.get('status'):
            status_history_vals = {
                'substance_id': res.id,
                'status': res.status,
                'start_date': datetime.today()
                }
            if vals.get('status') == 'entered-in-error':
                status_history_vals.update({'end_date': datetime.today()})
            status_history_obj.create(status_history_vals)
        return res

    @api.multi
    def write(self, vals):
        status_history_obj = self.env['hc.substance.status.history']
        res = super(Substance, self).write(vals)
        status_history_record_ids = status_history_obj.search([('end_date','=', False)])
        if status_history_record_ids:
            if vals.get('status') and status_history_record_ids[0].status != vals.get('status'):
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
                status_history_vals = {
                    'substance_id': self.id,
                    'status': vals.get('status'),
                    'start_date': datetime.today()
                    }
                if vals.get('status') == 'entered-in-error':
                    status_history_vals.update({'end_date': datetime.today()})
                status_history_obj.create(status_history_vals)
        return res

class SubstanceInstance(models.Model):
    _name = "hc.substance.instance"
    _description = "Substance Instance"
    _inherit = ["hc.backbone.element"]

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
    _inherit = ["hc.backbone.element"]

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
    quantity = fields.Float(
        string="Quantity Ratio",
        compute="_compute_quantity",
        store="True",
        help="Optional amount (concentration).")
    quantity_uom = fields.Char(
        string="Quantity Ratio UOM",
        compute="_compute_quantity_uom",
        store="True",
        help="Optional amount (concentration) unit of measure.")
    quantity_name = fields.Char(
        string="Quantity",
        compute="_compute_quantity_name",
        store="True",
        help="Numerator + Numerator UOM / Denominator + Denominator UOM.")
    substance_type = fields.Selection(
        string="Substance Type",
        required="True",
        selection=[
            ("codeable_concept", "Codeable Concept"),
            ("substance", "Substance")],
        help="Type of component of the substance.")
    substance_name = fields.Char(
        string="Substance",
        compute="_compute_substance_name",
        store="True",
        help="A component of the substance.")
    substance_codeable_concept_id = fields.Many2one(
        comodel_name="hc.vs.substance.code",
        string="Substance Codeable Concept",
        help="Codeable concept of a component of the substance.")
    substance_id = fields.Many2one(
        comodel_name="hc.res.substance",
        string="Substance",
        help="Substance component of the substance.")
    # technical attribute
    has_quantity_numerator = fields.Boolean(
        string="Has Quantity Numerator",
        invisible=True,
        help="Indicates if quantity_numerator exists. Used to enforce constraint quantity_numerator and quantity_denominator.")

    _sql_constraints = [
        ('quantity_numerator_gt_zero',
        'CHECK(quantity_numerator >= 0.0)',
        'Quantity Numerator SHALL be a non-negative value.'),

        ('quantity_denominator_gt_zero',
        'CHECK(quantity_denominator >= 0.0)',
        'Quantity Denominator SHALL be a non-negative value.')]

    @api.depends('substance_type')
    def _compute_substance_name(self):
        for hc_substance_ingredient in self:
            if hc_substance_ingredient.substance_type == 'codeable_concept':
                hc_substance_ingredient.substance_name = hc_substance_ingredient.substance_codeable_concept_id.name
            elif hc_substance_ingredient.substance_type == 'substance':
                hc_substance_ingredient.substance_name = hc_substance_ingredient.substance_id.name

    @api.onchange('quantity_numerator')
    def _onchange_quantity_numerator(self):
        if self.quantity_numerator:
            self.has_quantity_numerator = True
        else:
            self.has_quantity_numerator = False

    @api.depends('quantity_numerator', 'quantity_denominator')
    def _compute_quantity(self):
        if self.quantity_numerator and self.quantity_denominator:
            self.quantity = self.quantity_numerator / self.quantity_denominator

    @api.depends('quantity_numerator_uom_id', 'quantity_denominator_uom_id')
    def _compute_quantity_uom(self):
        quantity_uom = '/'
        if self.quantity_numerator_uom_id:
            quantity_uom = self.quantity_numerator_uom_id.code
        if self.quantity_denominator_uom_id:
            quantity_uom = quantity_uom + ' per ' + self.quantity_denominator_uom_id.code
        self.quantity_uom = quantity_uom

    @api.depends('quantity_numerator', 'quantity_denominator', 'quantity_numerator_uom_id', 'quantity_denominator_uom_id')
    def _compute_quantity_name(self):
        quantity_name = '/'
        if self.quantity_numerator and self.quantity_denominator:
            self.quantity_name = str(self.quantity_numerator) + ' ' + str(self.quantity_numerator_uom_id.code) + '/' + str(self.quantity_denominator) + ' ' + str(self.quantity_denominator_uom_id.code)

    @api.depends('item_type')
    def _compute_item_name(self):
        for hc_product_ingredient in self:
            if hc_product_ingredient.item_type == 'code':
                hc_product_ingredient.item_name = hc_product_ingredient.item_code_id.name
            elif hc_product_ingredient.item_type == 'substance':
                hc_product_ingredient.item_name = hc_product_ingredient.item_substance_id.name
            elif hc_product_ingredient.item_type == 'medication':
                hc_product_ingredient.item_name = hc_product_ingredient.item_medication_id.name

class SubstanceIdentifier(models.Model):
    _name = "hc.substance.identifier"
    _description = "Substance Identifier"
    _inherit = ["hc.basic.association", "hc.identifier"]

    substance_id = fields.Many2one(
        comodel_name="hc.res.substance",
        string="Substance",
        help="Substance associated with this identifier.")

class SubstanceStatusHistory(models.Model):
    _name = "hc.substance.status.history"
    _description = "Substance Status History"

    substance_id = fields.Many2one(
        comodel_name="hc.res.substance",
        string="Substance",
        help="Substance associated with this Substance Status History.")
    status = fields.Char(
        string="Status",
        help="The status of the substance.")
    start_date = fields.Datetime(
        string="Start Date",
        help="Start of the period during which this substance status is valid.")
    end_date = fields.Datetime(
        string="End Date",
        help="End of the period during which this substance status is valid.")
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
        required=True,
        help="Code of this substance code.")
    contains_id = fields.Many2one(
        comodel_name="hc.vs.substance.code",
        string="Parent",
        help="Parent substance code.")
    level_attribute = fields.Char(
        compute="_get_level",
        string="Level/Parent",
        store=True,
        help="Level associated with Parent concept.")
    level = fields.Integer(
        compute="_get_level",
        string="Level",
        store=True,
        help="Level as a parent in a hierarchy of codes.")
    parent_child_ids = fields.Many2many(
        comodel_name="hc.vs.substance.code",
        relation="parent_child_rel",
        column1="parent_id",
        column2="child_id",
        string="Parents",
        help="Parent substance code.")

    @api.constrains('parent_child_ids')
    def _check_recursive_parent_child(self):
        for rec in self:
            if rec.id in rec.parent_child_ids.ids:
                raise ValidationError('Error! A code cannot be a child of itself.')
        return True

    @api.depends('parent_child_ids')
    def _get_level(self):
        for rec in self:
            if not rec.parent_child_ids:
                rec.level = 1
                rec.level_attribute = ''
            else:
                high = 1
                attr_str = False
                for parent in rec.parent_child_ids:
                    if not attr_str:
                        attr_str = '(' + str(parent.level + 1) + ',' + parent.name +')'
                    else:
                        attr_str = attr_str + ',' + '(' + str(parent.level + 1) + ',' + parent.name + ')'
                    if parent.level > high:
                        high = parent.level
                rec.level = high + 1

    # @api.multi
    # def write(self, vals):
    #     res = super(SubstanceCode, self).write(vals)
    #     for rec in self:
    #         if rec.parent_child_ids:
    #             if rec.id in rec.parent_child_ids.ids:
    #                 raise ValidationError(
    #                     "Error! A code cannot be a child of itself.")
    #             return res


    @api.model
    def create(self, vals):
        res = super(SubstanceCode, self).create(vals)
        level_attr = False
        if res.parent_child_ids:
            for code in res.parent_child_ids:
                res.level = code.level + 1
                if not level_attr:
                    level_attr = '(' + str(res.level) + ',' + code.name +')'
                else:
                    level_attr = level_attr + ',' + '(' + str(res.level) + ',' + code.name +')'
        else:
            res.level = 1
        res.level_attribute = level_attr or ''
        return res

    @api.multi
    def write(self, vals):
        res = super(SubstanceCode, self).write(vals)
        level_attr = False
        for rec in self:
            if rec.parent_child_ids:
                if rec.id in rec.parent_child_ids.ids:
                    raise ValidationError(
                        "Error! A code cannot be a child of itself.")
                for code in rec.parent_child_ids:
                    vals.update({'level': code.level + 1})
                    if not level_attr:
                        level_attr = '(' + str(rec.level) + ',' + code.name +')'
                    else:
                        level_attr = level_attr + ',' + '(' + str(rec.level) + ',' + code.name +')'
            else:
                vals.update({'level': 1})
            vals.update({'level_attribute' : level_attr or ''})
        return super(SubstanceCode, self).write(vals)
