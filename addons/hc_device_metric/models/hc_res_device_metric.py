# -*- coding: utf-8 -*-

from openerp import models, fields, api

class DeviceMetric(models.Model):    
    _name = "hc.res.device.metric"    
    _description = "Device Metric"            

    name = fields.Char(
        string="Name", 
        compute="_compute_name", 
        store="True", 
        help="Human-readable label for this device metric. Identifier + Type + Device + Calibration Time")
    identifier_id = fields.Many2one(
        comodel_name="hc.device.metric.identifier", 
        string="Identifier", 
        required="True", 
        help="Unique identifier of this Device Metric.") 
    type_id = fields.Many2one(
        comodel_name="hc.vs.device.metric.type", 
        string="Type", 
        required="True", 
        help="Type of metric.")                                  
    unit_id = fields.Many2one(
        comodel_name="hc.vs.device.metric.unit", 
        string="Unit", 
        help="Unit of metric.")                    
    source_id = fields.Many2one(
        comodel_name="hc.res.device", 
        string="Source", 
        help="Describes the link to the source Device.")                    
    parent_id = fields.Many2one(
        comodel_name="hc.res.device.component", 
        string="Parent", 
        help="Describes the link to the parent DeviceComponent.")                    
    operational_status = fields.Selection(
        string="Operational Status", 
        selection=[
            ("on", "On"), 
            ("off", "Off"), 
            ("standby", "Standby")], 
        help="Indicates current operational state of the device.")                    
    color = fields.Selection(
        string="Color", 
        selection=[
            ("black", "Black"), 
            ("red", "Red"), 
            ("green", "Green"), 
            ("yellow", "Yellow"), 
            ("blue", "Blue"), 
            ("magenta", "Magenta"), 
            ("cyan", "Cyan"), 
            ("white", "White")], 
        help="Describes the color representation for the metric.")                    
    category = fields.Selection(
        string="Category", 
        required="True", 
        selection=[
            ("measurement", "Measurement"), 
            ("setting", "Setting"), 
            ("calculation", "Calculation"), 
            ("unspecified", "Unspecified")], 
        help="Indicates the category of the observation generation process.")                    
    measurement_period_id = fields.Many2one(
        comodel_name="hc.device.metric.measurement.period", 
        string="Measurement Period", 
        help="Describes the measurement repetition time.")
    last_calibration_time = fields.Datetime(
        string="Last Calibration Time",
        compute="_compute_last_calibration_time",
        store="True", 
        help="Describes the time last calibration has been performed.")                    
    calibration_ids = fields.One2many(
        comodel_name="hc.device.metric.calibration", 
        inverse_name="device_metric_id", 
        string="Calibrations", 
        help="Describes the calibrations that have been performed or that are required to be performed.")

    @api.depends('calibration_ids')
    def _compute_last_calibration_time(self):
        for rec in self:
            if rec.calibration_ids:
                latest_time = False
                for calibration in rec.calibration_ids:
                    if not latest_time:
                        latest_time = calibration.time
                    if calibration.time >= latest_time:
                        latest_time = calibration.time
                rec.last_calibration_time = latest_time                    

    @api.depends('identifier_id', 'type_id', 'parent_id')
    # @api.depends('identifier_id', 'type_id', 'parent_id', 'last_calibration_time')                    
    def _compute_name(self):                    
        comp_name = '/'             
        for hc_res_device_metric in self:               
            if hc_res_device_metric.identifier_id:           
                comp_name = hc_res_device_metric.identifier_id.name     
            if hc_res_device_metric.type_id:       
                comp_name = comp_name + "," + hc_res_device_metric.type_id.name or ''  
            if hc_res_device_metric.parent_id:            
                comp_name = comp_name + "," + hc_res_device_metric.parent_id.name or ''        
            # if hc_res_device_metric.last_calibration_time:          
            #     identifier_last_calibration_time = datetime.strftime(datetime.strptime(hc_res_device_metric.last_calibration_time, DTF), "%Y-%m-%d")        
            #     comp_name = comp_name + " " + identifier_last_calibration_time      
            hc_res_device_metric.name = comp_name           

class DeviceMetricCalibration(models.Model):    
    _name = "hc.device.metric.calibration"    
    _description = "Device Metric Calibration"

    device_metric_id = fields.Many2one(
        comodel_name="hc.res.device.metric", 
        string="Device Metric", 
        help="Device metric associated with this calibration.")                    
    type = fields.Selection(
        string="Calibration Type", 
        selection=[
            ("unspecified", "Unspecified"), 
            ("offset", "Offset"), 
            ("gain", "Gain"), 
            ("two-point", "Two-Point")],
        default="unspecified", 
        help="Describes the type of the calibration method.")                    
    state = fields.Selection(
        string="Calibration State", 
        selection=[
            ("not-calibrated", "Not-Calibrated"), 
            ("calibration-required", "Calibration-Required"), 
            ("calibrated", "Calibrated"), 
            ("unspecified", "Unspecified")],
        default="unspecified",     
        help="Describes the state of the calibration.")                    
    time = fields.Datetime(
        string="Time",
        default=fields.datetime.now(),
        help="Describes the time last calibration has been performed.")                    

class DeviceMetricIdentifier(models.Model):    
    _name = "hc.device.metric.identifier"    
    _description = "Device Metric Identifier"        
    _inherit = ["hc.basic.association", "hc.identifier"]    

class DeviceMetricMeasurementPeriod(models.Model):    
    _name = "hc.device.metric.measurement.period"    
    _description = "Device Metric Measurement Period"        
    _inherit = ["hc.basic.association", "hc.timing"]

class DeviceMetricType(models.Model):    
    _name = "hc.vs.device.metric.type"    
    _description = "Device Metric Type"        
    _inherit = ["hc.value.set.contains"]    

class DeviceMetricUnit(models.Model):    
    _name = "hc.vs.device.metric.unit"    
    _description = "Device Metric Unit"        
    _inherit = ["hc.value.set.contains"]    
