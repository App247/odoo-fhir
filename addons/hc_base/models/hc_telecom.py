# -*- coding: utf-8 -*-

from openerp import models, fields, api

class ContactPoint(models.Model):   
    _name = "hc.contact.point"   
    _description = "Contact Point"
    _rec_name = "value"

    system = fields.Selection(
        string="Contact Point System", 
        selection=[
            ("phone", "Phone"),
            ("mobile","Mobile"),  
            ("fax", "Fax"), 
            ("email", "Email"), 
            ("pager", "Pager"),
            ("other", "Other")], 
        help="Telecommunications form for contact point - what communications system is required to make use of the contact.")     
    value = fields.Char(
        string="Value", 
        help="The actual contact point details.")
    natl_number = fields.Char(
        string="National Number", 
        help="The domestic format for a phone number (e.g., (607) 123 4567).")
      
class ContactPointUse(models.Model):    
    _name = "hc.contact.point.use"  
    _description = "Contact Point Use"
    _inherit = ["hc.basic.association"]

    use = fields.Selection(
        string="Use", 
        selection=[
            ("home", "Home"), 
            ("work", "Work"),
            ("vacation", "Vacation"),
            ("temp", "Temp"), 
            ("old", "Old")], 
        help="Purpose of this contact point.")     
    rank = fields.Integer(
        string="Rank", 
        default="1", 
        help="Specify preferred order of use (1 = highest).")       

