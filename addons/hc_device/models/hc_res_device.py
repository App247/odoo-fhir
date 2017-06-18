# -*- coding: utf-8 -*-

from openerp import models, fields, api

class Device(models.Model): 
    _name = "hc.res.device" 
    _description = "Device"

    name = fields.Char(
        string="Name", 
        compute="_compute_name", 
        store="True", 
        help="Human-readable label for this device. UDI ID + Name.")
    identifier_ids = fields.One2many(
        comodel_name="hc.device.identifier", 
        inverse_name="device_id", 
        string="Identifiers", 
        help="Instance id from manufacturer, owner, and others.")          
    status = fields.Selection(
        string="Device Status", 
        selection=[
            ("available", "Available"), 
            ("not-available", "Not-Available"), 
            ("entered-in-error", "Entered-In-Error"), 
            ("unknown", "Unknown")],
        help="Status of the Device availability.")      
    type_id = fields.Many2one(
        comodel_name="hc.vs.device.kind", 
        string="Type", 
        required="True", 
        help="What kind of device this is.")        
    lot_number = fields.Char(
        string="Lot Number", 
        help="Lot number of manufacture.")        
    manufacturer_id = fields.Many2one(
        comodel_name="hc.res.organization", 
        string="Manufacturer", 
        help="Name of device manufacturer.")       
    manufacture_date = fields.Datetime(
        string="Manufacture Date", 
        help="Manufacture date.")     
    expiration_date = fields.Datetime(
        string="Expiration Date", 
        help="Date and time of expiry of this device (if applicable).")      
    model = fields.Char(
        string="Model", 
        help="Model id assigned by the manufacturer.")      
    version = fields.Char(
        string="Version", 
        help="Version number (i.e. software).")     
    patient_id = fields.Many2one(
        comodel_name="hc.res.patient", 
        string="Patient", 
        help="Patient to whom Device is affixed.")       
    owner_organization_id = fields.Many2one(
        comodel_name="hc.res.organization", 
        string="Owner Organization", 
        help="Organization responsible for device.")      
    contact_ids = fields.One2many(
        comodel_name="hc.device.telecom", 
        inverse_name="device_id", 
        string="Telecoms", 
        help="Details for human/organization for support.")        
    location_id = fields.Many2one(
        comodel_name="hc.res.location", 
        string="Location", 
        help="Where the resource is found.")       
    url = fields.Char(
        string="URI", 
        help="Network address to contact device.")      
    note_ids = fields.One2many(
        comodel_name="hc.device.note", 
        inverse_name="device_id", 
        string="Notes", 
        help="Device notes and comments.")
    safety_ids = fields.Many2many(
        comodel_name="hc.vs.device.safety", 
        relation="device_safety_rel", 
        string="Safety", 
        help="Safety Characteristics of Device.")
    udi_id = fields.Many2one(
        comodel_name="hc.device.udi", 
        string="UDI", 
        help="Unique Device Identifier (UDI) Barcode string.")                     

class DeviceUDI(models.Model):  
    _name = "hc.device.udi"
    _description = "Device UDI"

    device_identifier = fields.Char(
        string="Device Identifier", 
        help="Mandatory fixed portion of UDI.")     
    name = fields.Char(
        string="Name", 
        help="Device Name as appears on UDI label.")      
    jurisdiction = fields.Char(
        string="Jurisdiction URI", 
        help="Regional UDI authority.")        
    carrier_hrf = fields.Char(
        string="Carrier HRF", 
        help="UDI Human Readable Barcode String.")      
    carrier_aidc = fields.Binary(
        string="Carrier AIDC", 
        help="UDI Machine Readable Barcode String.")        
    issuer = fields.Char(
        string="Issuer URI", 
        help="UDI Issuing Organization.")
    entry_type = fields.Selection(
        string="UDI Entry Type", 
        selection=[
            ("barcode", "Barcode"), 
            ("rfid", "RfID"), 
            ("manual +", "Manual +")], 
        help="Status of the Device availability.")        

class DeviceIdentifier(models.Model):    
    _name = "hc.device.identifier"    
    _description = "Device Identifier"        
    _inherit = ["hc.basic.association", "hc.identifier"]    

    device_id = fields.Many2one(
        comodel_name="hc.res.device", 
        string="Device", 
        help="Device associated with this Device Identifier.")                    

class DeviceTelecom(models.Model):  
    _name = "hc.device.telecom" 
    _description = "Device Telecom"     
    _inherit = ["hc.contact.point.use"] 
    _inherits = {"hc.contact.point": "contact_id"}

    contact_id = fields.Many2one(
        comodel_name="hc.contact.point", 
        string="Contact", 
        ondelete="restrict", 
        required="True", 
        help="Telecom associated with this Device Telecom.")                  
    device_id = fields.Many2one(
        comodel_name="hc.res.device", 
        string="Device", 
        help="Device associated with this Device Telecom.")                       

class DeviceNote(models.Model):    
    _name = "hc.device.note"    
    _description = "Device Note"        
    _inherit = ["hc.basic.association", "hc.annotation"]
    
    device_id = fields.Many2one(
        comodel_name="hc.res.device", 
        string="Device", 
        help="Device associated with this device telecom.")                    

class DeviceKind(models.Model):
    _name = "hc.vs.device.kind"
    _description = "Device Kind"
    _inherit = ["hc.value.set.contains"]
    
    name = fields.Char(
        string="Name", 
        help="Name of this device kind.")
    code = fields.Char(
        string="Code", 
        help="Code of this device kind.")
    contains_id = fields.Many2one(
        comodel_name="hc.vs.device.kind", 
        string="Parent", 
        help="Parent device kind.")

class DeviceSafety(models.Model):
    _name = "hc.vs.device.safety"
    _description = "Device Safety"
    _inherit = ["hc.value.set.contains"]

    name = fields.Char(
        string="Name", 
        help="Name of this device safety.")       
    code = fields.Char(
        string="Code", 
        help="Code of this device safety.")       
    contains_id = fields.Many2one(
        comodel_name="hc.vs.device.safety", 
        string="Parent", 
        help="Parent device safety.")        

# External Reference

class Signature(models.AbstractModel):    
    _inherit = "hc.signature"

    who_device_id = fields.Many2one(
            comodel_name="hc.res.device", 
            string="Who Device", 
            help="Device who signed.")

    on_behalf_of_device_id = fields.Many2one(
        comodel_name="hc.res.device", 
        string="On Behalf Of Device", 
        help="Device the party represented.")
