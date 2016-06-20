# -*- coding: utf-8 -*-

from openerp import models, fields, api

class Telecom(models.Model):    
    _name = "hc.telecom"    
    _description = "Telecom Contact Point"

    system = fields.Selection(
        string="Type", 
        selection=[
            ("phone", "Phone"), 
            ("fax", "Fax"), 
            ("email", "Email"), 
            ("url", "Url")], 
        default="phone",
        help="Telecommunications form for contact point - what communications system is required to make use of the contact.")   
    name = fields.Char(
        string="Value", 
        help="The actual telecom contact point details (e.g., Phone: +22 607 123 4567, Email: jdoe@isp.com, Url: www.doecorp.com).")
    natl_value = fields.Char(
        string="National Value", 
        help="The domestic format for a phone number (e.g., (607) 123 4567).")

# class ObjectTelecom(models.Model):  
#     _name = "hc.object.telecom" 
#     _description = "Object Telecom"
#     _inherit = ["hc.basic.association"]
#     _inherits = {"hc.telecom": "telecom_id"}
 
#     telecom_id = fields.Many2one(
#         comodel_name="hc.telecom", 
#         string="Telecom", 
#         required=True,
#         ondelete="restrict", 
#         help="Telecom contact point associated with this object.")
#     use = fields.Selection(string="Telecom Use", 
#         selection=[
#             ("home", "Home"), 
#             ("work", "Work"), 
#             ("temp", "Temp"), 
#             ("old", "Old"),
#             ("mobile", "Mobile")], 
#         help="Purpose of this telecom contact point.")