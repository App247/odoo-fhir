# -*- coding: utf-8 -*-

from openerp import models, fields, api
from openerp import _, exceptions

class Timing(models.Model):    
    _name = "hc.timing"    
    _description = "Timing"        

    name = fields.Char(
        string="Timing Name", 
        required="True", 
        help="Human-readable label for this timing definition.")
    event_ids = fields.One2many(
        comodel_name="hc.timing.event.date", 
        inverse_name="timing_id", 
        string="Event Dates", 
        help="When the event occurs.")                
    code_id = fields.Many2one(
        comodel_name="hc.vs.timing.abbreviation", 
        string="Code", 
        help="Timing abbreviation.")               
    repeat_ids = fields.One2many(
        comodel_name="hc.timing.repeat", 
        inverse_name="timing_id", 
        string="Repeats", 
        help="When the event is to occur.")                

class TimingRepeat(models.Model):   
    _name = "hc.timing.repeat"  
    _description = "Timing Repeat"
    
    timing_id = fields.Many2one(
        comodel_name="hc.timing", 
        string="Timing", 
        required="True", 
        help="Timing associated with this repeat.")        
    bounds_type = fields.Selection(
        string="Bounds Type",  
        selection=[
            ("duration", "Duration"), 
            ("range", "Range"), 
            ("period", "Period")], 
        help="Type of bounds.")       
    bounds_name = fields.Char(
        string="Bounds", 
        compute="_compute_bounds_name",
        store="True",
        help="Length/Range of lengths, or (Start and/or end) limit.")        
    bounds_duration = fields.Float(
        string="Bounds Duration", 
        help="Bounds length of time.")
    bounds_duration_uom_id = fields.Many2one(
        comodel_name="product.uom", 
        string="Bounds Duration UOM", 
        domain="[('category_id','=','Time (UCUM)')]", 
        help="Bounds Duration unit of measure.")     
    bounds_range_low = fields.Float(
        string="Bounds Range Low", 
        help="Low limit of bounds range.")       
    bounds_range_high = fields.Float(
        string="Bounds Range High", 
        help="High limit of bounds range.")        
    bounds_period_start_date = fields.Datetime(
        string="Bounds Period Start Date", 
        help="Start of the bounds period.")       
    bounds_period_end_date = fields.Datetime(
        string="Bounds Period End Date", 
        help="End of the bounds period.")     
    count = fields.Integer(
        string="Count", 
        help="Number of times to repeat.")       
    
    def _get_default_count_max(self):
        for hc_timing_repeat in self:      
            hc_timing_repeat.count_max = hc_timing_repeat.count
        
    count_max = fields.Integer(
        string="Count Max",
        default=_get_default_count_max, 
        help="Maximum number of times to repeat.")       
    duration = fields.Float(
        string="Duration", 
        help="How long when it happens.")     
    duration_max = fields.Float(
        string="Duration Max", 
        help="How long when it happens (Max).")
    duration_unit_id = fields.Many2one(
        comodel_name="product.uom", 
        string="Duration UOM",
        domain="[('category_id','=','Time (UCUM)')]", 
        help="Unit of time (UCUM).")            
    frequency = fields.Integer(
        string="Frequency", 
        help="Event occurs frequency times per duration.")       
    frequency_max = fields.Integer(
        string="Frequency Max", 
        help="Event occurs frequency times per duration.")       
    period = fields.Float(
        string="Period", 
        help="Event occurs frequency times per period.")     
    period_max = fields.Float(
        string="Period Max",
        help="Upper limit of period (3-4 hours).")
    period_unit_id = fields.Many2one(
        comodel_name="product.uom", 
        string="Period UOM",
        domain="[('category_id','=','Time (UCUM)')]",  
        help="Unit of time (UCUM).")              
    day_of_week_ids = fields.Many2many(
        comodel_name="hc.vs.days.of.week", 
        relation="timing_repeat_day_of_week_rel", 
        string="Days of Week", 
        help="If one or more days of week is provided, then the action happens only on the specified day(s).")
    time_of_day_ids = fields.One2many(
        comodel_name="hc.timing.repeat.time.of.day", 
        inverse_name="repeat_id", 
        string="Time Of Days", 
        help="Time of day for action.")
    when_ids = fields.Many2many(
        comodel_name="hc.vs.timing.event", 
        relation="timing_repeat_when_rel", 
        string="When", 
        help="Regular life events the event is tied to.")
    offset = fields.Integer(
        string="Offset Minutes", 
        help="Minutes from event (before or after).")                      

    # @api.depends('count')

    
    # @api.multi
    # @api.constrains('bounds_duration')
    # def _check_bounds_duration(self):
    #     for record in self:
    #         if record < 0:
    #             raise exceptions.ValidationError(_('Bounds Duration1 SHALL be a non-negative value.'))

    _sql_constraints = [    
        ('bounds_duration_gt_zero',
        'CHECK(bounds_duration >= 0.0)',
        'Bounds Duration SHALL be a non-negative value.'),

        ('bounds_range_low_gt_zero',              
        'CHECK(bounds_range_low >= 0.0)',                
        'Range Low SHALL be a non-negative value.'),

        ('bounds_range_high_gt_low',
        'CHECK(bounds_range_high >= bounds_range_low)',
        'Range High SHALL not be lower than Range Low.'),

        ('bounds_period_end_gt_start',
        'CHECK(bounds_period_end_date >= bounds_period_start_date)',
        'Period End Date SHALL not be lower than Period Start Date.'),

        ('count_max_gt_count',
        'CHECK(count_max >= count)',
        'Maximum Count SHALL not be lower than Count.'),

        ('duration_gt_zero',
        'CHECK(duration >= 0.0)',
        'Duration SHALL be a non-negative value.'),

        ('duration_max_gt_duration',
        'CHECK(duration_max >= duration)',
        'Maximum Duration SHALL not be lower than Duration.'),

        ('frequency_gt_zero',
        'CHECK(frequency >= 0.0)',
        'Frequency SHALL be a non-negative value.'),

        ('frequency_max_gt_frequency',
        'CHECK(frequency_max >= frequency)',
        'Maximum Frequency SHALL not be lower than Frequency.'),

        ('period_gt_zero',
        'CHECK(period >= 0.0)',
        'Period SHALL be a non-negative value.'),

        ('period_max_gt_period',
        'CHECK(period_max >= period)',
        'Maximum Period SHALL not be lower than Period.')  
        ]

    # Default for max
    
    @api.onchange('count')
    def _onchange_count(self):
        for rec in self:
            if rec.count and not rec.count_max > rec.count:
                rec.count_max = rec.count

    @api.onchange('duration')
    def _onchange_duration(self):
        for rec in self:
            if rec.duration and not rec.duration_max > rec.duration:
                rec.duration_max = rec.duration

    @api.onchange('frequency')
    def _onchange_frequency(self):
        for rec in self:
            if rec.frequency and not rec.frequency_max > rec.frequency:
                rec.frequency_max = rec.frequency

    @api.onchange('period')
    def _onchange_period(self):
        for rec in self:
            if rec.period and not rec.period_max > rec.period:
                rec.period_max = rec.period

    @api.depends('bounds_type')         
    def _compute_bounds_name(self):         
        for hc_timing_repeat in self:
            if hc_timing_repeat.bounds_type == 'duration':  
                hc_timing_repeat.bounds_name = str(hc_timing_repeat.bounds_duration) + " " + str(hc_timing_repeat.bounds_duration_uom_id.name)
            elif hc_timing_repeat.bounds_type == 'period':    
                hc_timing_repeat.bounds_name = "Between " + str(hc_timing_repeat.bounds_period_start_date) + " and " + str(hc_timing_repeat.bounds_period_end_date)
            elif hc_timing_repeat.bounds_type == 'range': 
                hc_timing_repeat.bounds_name = "Between " + str(hc_timing_repeat.bounds_range_low) + " and " + str(hc_timing_repeat.bounds_range_high)

# Constraints (reference: http://build.fhir.org/datatypes.html#timing)

# tim-1: On Timing.repeat: if there's a duration, there needs to be duration units (expression on Timing.repeat: duration.empty() or durationUnit.exists())
# Implemented in view as <field name="duration_unit_id" attrs="{'invisible': [('duration','=',0)]}"/>

# tim-2: On Timing.repeat: if there's a period, there needs to be period units (expression on Timing.repeat: period.empty() or periodUnit.exists())
# Implemented in view as <field name="period_unit_id" attrs="{'invisible': [('period','=',0.0)]}"/>

# tim-4: On Timing.repeat: duration SHALL be a non-negative value (expression on Timing.repeat: duration.exists() implies duration >= 0)
# Implemented in SQL constraint

# tim-5: On Timing.repeat: period SHALL be a non-negative value (expression on Timing.repeat: period.exists() implies period >= 0)
# Implemented in SQL constraint

# tim-6: On Timing.repeat: If there's a periodMax, there must be a period (expression on Timing.repeat: periodMax.empty() or period.exists())
# Implemented in view as <field name="period_uom_id" attrs="{'invisible': [('period_max','=','')]}"/>

# tim-7: On Timing.repeat: If there's a durationMax, there must be a duration (expression on Timing.repeat: durationMax.empty() or duration.exists())
# Implemented in view as <field name="duration_unit_id" attrs="{'invisible': [('duration_max','=','')]}"/>

# tim-8: On Timing.repeat: If there's a countMax, there must be a count (expression on Timing.repeat: countMax.empty() or count.exists())
# Implemented in view as <field name="count_max" attrs="{'invisible': [('count','=',0)]}"/>

# tim-9: On Timing.repeat: If there's an offset, there must be a when (and not C, CM, CD, CV) (expression on Timing.repeat: offset.empty() or (when.exists() and ((when in ('C' | 'CM' | 'CD' | 'CV')).not())))
# Implemented in view as <field name="when_ids" attrs="{'invisible': [('offset','=',0)]}" widget="many2many_tags"/>

# tim-10: On Timing.repeat: If there's a timeOfDay, there cannot be be a when, or vice versa (expression on Timing.repeat: timeOfDay.empty() or when.empty())
# Implemented in view as <page string="Times of Day" attrs="{'invisible': [('offset','&gt;',0)]}">
                   

class TimingEventDate(models.Model):  
    _name = "hc.timing.event.date"   
    _description = "Timing Event Date"           
    _inherit = ["hc.basic.association"]       

    timing_id = fields.Many2one(
        comodel_name="hc.timing", 
        string="Timing", 
        required="True", 
        help="Timing associated with this Timing Event Date.")    
    event_date = fields.Datetime(
        string="Event Date", 
        help="Event Date associated with this Timing Event Date.")                

class TimingRepeatTimeOfDay(models.Model):
    _name = "hc.timing.repeat.time.of.day"
    _description = "Timing Repeat Time Of Day"
    _inherit = ["hc.basic.association"]

    repeat_id = fields.Many2one(
        comodel_name="hc.timing.repeat", 
        string="Repeat", 
        help="Repeat associated with this Timing Repeat Time Of Day.")                    
    time_of_day = fields.Float(
        string="Time Of Day", 
        help="Time Of Day associated with this Timing Repeat Time Of Day.")                    

class TimingAbbreviation(models.Model):
    _name = "hc.vs.timing.abbreviation"
    _description = "Timing Abbreviation"
    _inherit = ["hc.value.set.contains"]

    name = fields.Char(
        string="Name", 
        help="Name of this timing abbreviation.")                 
    code = fields.Char(
        string="Code", 
        help="Code of this timing abbreviation.")                 
    contains_id = fields.Many2one(
        comodel_name="hc.vs.timing.abbreviation", 
        string="Parent", 
        help="Parent timing abbreviation.")                    

class TimingEvent(models.Model):
    _name = "hc.vs.timing.event"
    _description = "Timing Event"
    _inherit = ["hc.value.set.contains"]

    name = fields.Char(
        string="Name", 
        help="Name of this timing event.")                    
    code = fields.Char(
        string="Code", 
        help="Code of this timing event.")                    
    contains_id = fields.Many2one(
        comodel_name="hc.vs.timing.event", 
        string="Parent", 
        help="Parent timing event.")          



