# -*- coding: utf-8 -*-

from openerp import models, fields, api

class V3Confidentiality(models.Model):   
    _name = "hc.vs.v3.confidentiality"
    _description = "V3 Confidentiality"  
    _inherit = ["hc.value.set.contains"]

    name = fields.Char(
        string="Name", 
        help="Name of this confidentiality.")
    code = fields.Char(
        string="Code", 
        help="Code of this confidentiality.")
    contains_id = fields.Many2one(
        comodel_name="hc.vs.v3.confidentiality", 
        string="Parent",
        help="Parent confidentiality.")
    value_set_ids = fields.Many2many(
        comodel_name="hc.vs.v3.confidentiality.value.set",
        string="Value Sets",
        help="Value Set where this confidentiality belongs to.")    

class V3ConfidentialityValueSet(models.Model):
    _name = "hc.vs.v3.confidentiality.value.set"
    _description = "V3 Confidentiality Value Set"
    _inherit = ["hc.value.set.contains"]

    name = fields.Char(
        string="Name", 
        help="Name of this confidentiality value set.")                               
    code = fields.Char(
        string="Code", 
        help="Code of this confidentiality value set.")                               
    contains_id = fields.Many2one(
        comodel_name="hc.vs.v3.confidentiality.value.set", 
        string="Parent", 
        help="Parent confidentiality value set.") 