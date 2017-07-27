# -*- coding: utf-8 -*-

from openerp import models, fields, api

class Meta(models.Model):    
    _name = "hc.meta"    
    _description = "Meta"
    _rec_name = "profile"        

    version_id = fields.Char(
        string="Version Id", 
        help="Version specific identifier.")                
    last_updated = fields.Datetime(
        string="Last Updated", 
        help="When the resource version last changed.")                
    profile = fields.Char(
        string="Profile URI", 
        help="URL of profiles this resource claims to conform to.")                
    security_ids = fields.Many2many(
        comodel_name="hc.vs.security.label", 
        string="Security Labels", 
        help="Security Labels applied to this resource.")                
    tag_ids = fields.Many2many(
        comodel_name="hc.vs.common.tag", 
        string="Tags", 
        help="Tags applied to this resource.")                

class CommonTag(models.Model):    
    _name = "hc.vs.common.tag"    
    _description = "Common Tag"        
    _inherit = ["hc.value.set.contains"]
