# -*- coding: utf-8 -*-

from openerp import models, fields, api

class DeviceComponent(models.Model):    
    _name = "hc.res.device.component"    
    _description = "Device Component"        

    name = fields.Char(
        string="Name", 
        compute="_compute_name", 
        store="True", 
        help="Human-readable label for this device component. Type + Device + Last System Change")
    type_id = fields.Many2one(
        comodel_name="hc.vs.device.component.type", 
        string="Type", 
        required="True", 
        help="What kind of component it is.")                
    identifier_id = fields.Many2one(
        comodel_name="hc.device.component.identifier", 
        string="Identifier", 
        required="True", 
        help="Instance id assigned by the software stack.")                
    last_system_change = fields.Datetime(
        string="Last System Change", 
        required="True", 
        help="Recent system change timestamp.")                
    source_id = fields.Many2one(
        comodel_name="hc.res.device", 
        string="Source", 
        help="A source device of this component.")                
    parent_id = fields.Many2one(
        comodel_name="hc.res.device.component", 
        string="Parent", 
        help="Parent resource link.")
    operational_status_ids = fields.Many2many(
        comodel_name="hc.vs.device.operational.status", 
        relation="device_component_operational_status_rel", 
        string="Operational Status", 
        help="Component operational status.")              
    parameter_group_id = fields.Many2one(
        comodel_name="hc.vs.device.parameter.group", 
        string="Parameter Group", 
        help="Current supported parameter group.")                
    measurement_principle_id = fields.Many2one(
        comodel_name="hc.vs.device.measmnt.principle", 
        string="Measurement Principle", 
        help="Describes the physical principle of the measurement.")              
    production_specification_ids = fields.One2many(
        comodel_name="hc.device.component.production.spec", 
        inverse_name="device_component_id", 
        string="Production Specifications",
         help="Production specification of the component.")                
    language_code_id = fields.Many2one(
        comodel_name="hc.vs.language", 
        string="Language Code", 
        help="Language code for the human-readable text strings produced by the device.")                

class DeviceComponentProductionSpec(models.Model):    
    _name = "hc.device.component.production.spec"    
    _description = "Device Component Production Spec"        

    device_component_id = fields.Many2one(
        comodel_name="hc.res.device.component", 
        string="Device Component", 
        help="Device component associated with this production specification.")                
    spec_type_id = fields.Many2one(
        comodel_name="hc.vs.device.specification.type", 
        string="Spec Type", 
        help="Specification type.")                
    component_identifier_id = fields.Many2one(
        comodel_name="hc.device.spec.component.identifier", 
        string="Component Identifier", 
        help="Internal component unique identification.")                
    production_spec = fields.Char(
        string="Production Spec", 
        help="A printable string defining the component.")                

class DeviceComponentIdentifier(models.Model):    
    _name = "hc.device.component.identifier"    
    _description = "Device Component Identifier"        
    _inherit = ["hc.identifier"]

class DeviceSpecComponentIdentifier(models.Model):    
    _name = "hc.device.spec.component.identifier"    
    _description = "Device Spec Component Identifier"        
    _inherit = ["hc.basic.association", "hc.identifier"]
    
    production_specification_id = fields.Many2one(
        comodel_name="hc.device.component.production.spec", 
        string="Production Specification", 
        help="Production Specification associated with this Device Spec Component Identifier.")              

class DeviceComponentType(models.Model):    
    _name = "hc.vs.device.component.type"   
    _description = "Device Component Type"      
    _inherit = ["hc.value.set.contains"]

class DeviceParameterGroup(models.Model):    
    _name = "hc.vs.device.parameter.group"    
    _description = "Device Parameter Group"        
    _inherit = ["hc.value.set.contains"]

class DeviceSpecificationType(models.Model):    
    _name = "hc.vs.device.specification.type"    
    _description = "Device Specification Type"        
    _inherit = ["hc.value.set.contains"]

class DeviceOperationalStatus(models.Model):    
    _name = "hc.vs.device.operational.status"    
    _description = "Device Operational Status"        
    _inherit = ["hc.value.set.contains"]

class DeviceMeasurementPrinciple(models.Model): 
    _name = "hc.vs.device.measmnt.principle"    
    _description = "Device Measurement Principle"       
    _inherit = ["hc.value.set.contains"]
