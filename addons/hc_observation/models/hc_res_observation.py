# -*- coding: utf-8 -*-

from openerp import models, fields, api

class Observation(models.Model):    
    _name = "hc.res.observation"    
    _description = "Observation"

    name = fields.Char(
        string="Event Name", 
        required="True", 
        help="Text representation of the observation event. Subject Name + Code + Effective Date.")
    identifier_ids = fields.One2many(
        comodel_name="hc.observation.identifier", 
        inverse_name="observation_id", 
        string="Identifiers", 
        help="Unique Id for this particular observation.")                    
    status = fields.Selection(string="Status", 
        selection=[
            ("registered", "Registered"), 
            ("preliminary", "Preliminary"), 
            ("final", "Final"), 
            ("amended +", "Amended +")], 
        help="The status of the result value.")                  
    category_ids = fields.Many2many(
        comodel_name="hc.vs.observation.category", 
        string="Categories", 
        help="Classification of type of observation.")                    
    code_id = fields.Many2one(
        comodel_name="hc.vs.observation.code", 
        string="Code", 
        required="True", 
        help="Type of observation (code / type).")                    
    subject_type = fields.Selection(
        string="Observation Subject Type", 
        selection=[
            ("patient", "Patient"), 
            ("group", "Group"), 
            ("device", "Device"), 
            ("location", "Location")], 
        help="Type of who and/or what this is about.")                    
    subject_name = fields.Char(
        string="Subject", 
        compute="_compute_subject_name", 
        help="Who and/or what this is about.")                    
    subject_patient_id = fields.Many2one(
        comodel_name="hc.res.patient", 
        string="Subject Patient", 
        help="Patient who and/or what this is about.")                    
    subject_group_id = fields.Many2one(
        comodel_name="hc.res.group", 
        string="Subject Group", 
        help="Group who and/or what this is about.")                    
    subject_device_id = fields.Many2one(
        comodel_name="hc.res.device", 
        string="Subject Device", 
        help="Device who and/or what this is about.")                    
    subject_location_id = fields.Many2one(
        comodel_name="hc.res.location", 
        string="Subject Location", 
        help="Location who and/or what this is about.")                    
    encounter_id = fields.Many2one(
        comodel_name="hc.res.encounter", 
        string="Encounter", 
        help="Healthcare event during which this observation is made.")                    
    effective_type = fields.Selection(
        string="Effective Date Type", 
        selection=[
            ("date_time", "Datetime"), 
            ("period", "Period")], 
        help="Type of Clinically relevant time/time-period for observation.")                    
    effective_name = fields.Char(
        string="Effective Date", 
        compute="_compute_effective_name", 
        help="Clinically relevant time/time.")                    
    effective_datetime = fields.Datetime(
        string="Effective Datetime", 
        help="dateTime clinically relevant time/time-period for observation.")                    
    effective_start_date = fields.Datetime(
        string="Effective Start Date", 
        help="Start of the clinically relevant time/time-period for observation.")
    effective_end_date = fields.Datetime(
        string="Effective End Date", 
        help="End of the clinically relevant time/time-period for observation.")                   
    issued_date = fields.Datetime(
        string="Issued Date Date", 
        help="Date/Time this was made available.")                    
    performer_ids = fields.One2many(
        comodel_name="hc.observation.performer", 
        inverse_name="observation_id", 
        string="Performers", 
        help="Who is responsible for the observation.")                    
    value_type = fields.Selection(
        string="Observation Value Type", 
        selection=[
            ("missing", "Missing"), 
            ("quantity", "Quantity"), 
            ("code", "Code"), 
            ("string", "String"), 
            ("range", "Range"), 
            ("ratio", "Ratio"), 
            ("sampled_data", "Sampled Data"), 
            ("attachment", "Attachment"),
            ("time", "Time"),
            ("date_time", "Datetime"),
            ("period", "Period")],
        help="Type of result.")                    
    value_name = fields.Char(
        string="Value", 
        compute="_compute_value_name", 
        help="Actual result.")                    
    value_missing = fields.Char(
        string="Value",
        help="Missing actual result.")                    
    value_quantity = fields.Float(
        string="Value Quantity", 
        help="Quantity actual result.")                    
    value_quantity_uom_id = fields.Many2one(
        comodel_name="product.uom", 
        string="Value Quantity UOM", 
        help="Value quantity unit of measure.")                    
    value_code_id = fields.Many2one(
        comodel_name="hc.vs.observation.value.code", 
        string="Value Code", 
        help="Code of actual result.")                    
    value_string = fields.Char(
        string="Value", 
        help="String of actual result.")                    
    value_range_low = fields.Float(
        string="Value Range Low", 
        help="Low limit of actual result.")                    
    value_range_high = fields.Float(
        string="Value Range High", 
        help="High limit of actual result.")                    
    value_ratio_numerator = fields.Float(
        string="Value Ratio Numerator", 
        help="Numerator value of actual result.")                    
    value_ratio_denominator = fields.Float(
        string="Value Ratio Denominator", 
        help="Denominator value of actual result.")                    
    value_sampled_data_id = fields.Many2one(
        comodel_name="hc.observation.value.sampled.data", 
        string="Value Sampled Data", 
        help="Sampled Data actual result.")                    
    value_attachment_id = fields.Many2one(
        comodel_name="hc.observation.value.attachment", 
        string="Value Attachment", 
        help="Attachment actual result.")                    
    value_time = fields.Char(
        string="Value Time", 
        help="Time actual result.")                    
    value_datetime = fields.Datetime(
        string="Value Datetime", 
        help="DateTime actual result.")                    
    value_start_date = fields.Datetime(
        string="Value Start Date", 
        help="Start of the actual result.")
    value_end_date = fields.Datetime(
        string="Value End Date", 
        help="End of the actual result.")              
    data_absent_reason_id = fields.Many2one(
        comodel_name="hc.vs.observation.value.absent.reason", 
        string="Data Absent Reason", 
        help="Why the result is missing.")                    
    interpretation_id = fields.Many2one(
        comodel_name="hc.vs.observation.interpretation", 
        string="Interpretation", 
        help="High, low, normal, etc.")
    comment = fields.Text(
        string="Comment", 
        help="Comments about result.")
    body_site_id = fields.Many2one(
        comodel_name="hc.vs.body.site", 
        string="Body Site", 
        help="Observed body part")
    method_id = fields.Many2one(
        comodel_name="hc.vs.observation.method", 
        string="Method", 
        help="How it was done.")
    specimen_id = fields.Many2one(
        comodel_name="hc.res.specimen", 
        string="Specimen", 
        help="Specimen used for this observation.")             
    device_type = fields.Selection(
        string="Observation Device Type", 
        selection=[
            ("device", "Device"), 
            ("device_metric", "Device Metric")], 
        help="Type of device.")                    
    device_name = fields.Char(
        string="Device", 
        compute="_compute_device_name", 
        help="(Measurement) Device.")                    
    device_id = fields.Many2one(
        comodel_name="hc.res.device", 
        string="Device", 
        help="Device (measurement) device.")                    
    device_metric_id = fields.Many2one(
        comodel_name="hc.res.device.metric", 
        string="Device Metric", 
        help="Device Metric (measurement) device.")                    
    reference_range_ids = fields.One2many(
        comodel_name="hc.observation.reference.range", 
        inverse_name="observation_id", 
        string="Reference Ranges", 
        help="Provides guide for interpretation.")                    

    @api.multi            
    def _compute_subject_name(self):            
        for hc_res_observation in self:        
            if hc_res_observation.subject_type == 'patient':    
                hc_res_observation.subject_name = hc_res_observation.subject_patient_id.name
            elif hc_res_observation.subject_type == 'group':    
                hc_res_observation.subject_name = hc_res_observation.subject_group_id.name
            elif hc_res_observation.subject_type == 'device':    
                hc_res_observation.subject_name = hc_res_observation.subject_device_id.name
            elif hc_res_observation.subject_type == 'location':    
                hc_res_observation.subject_name = hc_res_observation.subject_location_id.name

    @api.multi            
    def _compute_effective_name(self):            
        for hc_res_observation in self:        
            if hc_res_observation.effective_type == 'date_time':    
                hc_res_observation.effective_name = hc_res_observation.effective_datetime
            elif hc_res_observation.effective_type == 'period':    
                hc_res_observation.effective_name = hc_res_observation.effective_period_id.name

    @api.multi            
    def _compute_value_name(self):            
        for hc_res_observation in self:        
            if hc_res_observation.value_type == 'missing':    
                hc_res_observation.value_name = hc_res_observation.value_missing
            elif hc_res_observation.value_type == 'quantity':    
                hc_res_observation.value_name = hc_res_observation.value_quantity
            elif hc_res_observation.value_type == 'code':    
                hc_res_observation.value_name = hc_res_observation.value_codeable_concept_id.name
            elif hc_res_observation.value_type == 'string':    
                hc_res_observation.value_name = hc_res_observation.value_string
            elif hc_res_observation.value_type == 'range':    
                hc_res_observation.value_name = hc_res_observation.value_range_id.name
            elif hc_res_observation.value_type == 'ratio':    
                hc_res_observation.value_name = hc_res_observation.value_ratio_id.name
            elif hc_res_observation.value_type == 'sampled_data':   
                hc_res_observation.value_name = hc_res_observation.value_sampled_data_id.name
            elif hc_res_observation.value_type == 'attachment': 
                hc_res_observation.value_name = hc_res_observation.value_attachment_id.name
            elif hc_res_observation.value_type == 'time':   
                hc_res_observation.value_name = hc_res_observation.value_time
            elif hc_res_observation.value_type == 'date_time':   
                hc_res_observation.value_name = hc_res_observation.value_datetime
            elif hc_res_observation.value_type == 'period': 
                hc_res_observation.value_name = hc_res_observation.value_period_id.name

    @api.multi          
    def _compute_device_name(self):         
        for hc_res_observation in self:     
            if hc_res_observation.device_type == 'device':  
                hc_res_observation.device_name = hc_res_observation.device_device_id.name
            elif hc_res_observation.device_type == 'device_metric': 
                hc_res_observation.device_name = hc_res_observation.device_device_metric_id.name

class ObservationReferenceRange(models.Model):    
    _name = "hc.observation.reference.range"    
    _description = "Observation Reference Range"

    observation_id = fields.Many2one(
        comodel_name="hc.res.observation", 
        string="Observation", 
        required="True", 
        help="Observation associated with this Observation Reference Range.")                    
    low = fields.Float(
        string="Low", 
        help="Low Range, if relevant.")                    
    low_uom_id = fields.Many2one(
        comodel_name="product.uom", 
        string="Low UOM", 
        help="Low unit of measure.")                    
    high = fields.Float(
        string="High", 
        help="High Range, if relevant.")                    
    high_uom_id = fields.Many2one(
        comodel_name="product.uom", 
        string="High UOM", 
        help="High unit of measure.")                    
    meaning_id = fields.Many2one(
        comodel_name="hc.vs.reference.range.meaning", 
        string="Meaning", 
        help="Indicates the meaning/use of this range of this range.")                    
    age_range_low = fields.Float(
        string="Age Range Low", 
        help="Low limit of applicable age range, if relevant.")                    
    age_range_high = fields.Float(
        string="Age Range High", 
        help="High limit of applicable age range, if relevant.")                    
    text = fields.Char(
        string="Text", 
        help="Text based reference range in an observation.")                    

class ObservationRelated(models.Model):    
    _name = "hc.observation.related"    
    _description = "Observation Related"

    observation_id = fields.Many2one(
        comodel_name="hc.res.observation", 
        string="Observation", 
        required="True", 
        help="Observation associated with this Observation Related.")                    
    type = fields.Selection(
        string="Related Type", 
        selection=[
            ("has-component", "Has-Component"), 
            ("has-member", "Has-Member"), 
            ("derived-from", "Derived-From"), 
            ("sequel-to", "Sequel-To"), 
            ("replaces", "Replaces"), 
            ("qualified-by", "Qualified-By"), 
            ("interfered-by", "Interfered-By")], 
        help="A code specifying the kind of relationship that exists with the target resource.")                    
    target_type = fields.Selection(
        string="Related Target Type",
        required="True", 
        selection=[
            ("observation", "Observation"), 
            # ("questionnaire_response", "Questionnaire Response"), 
            ("sequence", "Sequence")], 
        help="Type of resource that is related to this target.")                    
    target_name = fields.Char(
        string="Target", 
        compute="_compute_target_name", 
        required="True", 
        help="Resource that is related to this target.")                    
    target_observation_id = fields.Many2one(
        comodel_name="hc.res.observation", 
        string="Target Observation", 
        help="Observation resource that is related to this target.")                    
    # target_questionnaire_response_id = fields.Many2one(
    #     comodel_name="hc.res.questionnaire.response", 
    #     string="Target Questionnaire Response", 
    #     help="Questionnaire Response resource that is related to this target.")                    
    target_sequence_id = fields.Many2one(
        comodel_name="hc.res.sequence", 
        string="Target Sequence", 
        help="Sequence resource that is related to this target.")                    

    @api.multi          
    def _compute_target_name(self):         
        for hc_res_observation in self:     
            if hc_res_observation.target_type == 'observation': 
                hc_res_observation.target_name = hc_res_observation.target_observation_id.name
            elif hc_res_observation.target_type == 'questionnaire_response':    
                hc_res_observation.target_name = hc_res_observation.target_questionnaire_response_id.name
            elif hc_res_observation.target_type == 'sequence':  
                hc_res_observation.target_name = hc_res_observation.target_sequence_id.name

class ObservationComponent(models.Model):    
    _name = "hc.observation.component"    
    _description = "Observation Component"            

    observation_id = fields.Many2one(
        comodel_name="hc.res.observation", 
        string="Observation", 
        required="True", 
        help="Observation associated with this Observation Component.")                    
    code = fields.Float(
        string="Code", 
        required="True", 
        help="Type of component observation (code / type).")                    
    value_type = fields.Selection(
        string="Component Value Type", 
        selection=[
            ("missing", "Missing"), 
            ("quantity", "Quantity"), 
            ("code", "Code"), 
            ("string", "String"), 
            ("range", "Range"), 
            ("ratio", "Ratio"), 
            ("sampled_data", "Sampled Data"), 
            ("attachment", "Attachment"),
            ("time", "Time"),
            ("date_time", "Datetime"),
            ("period", "Period")],
        help="Type of result.")                    
    value_name = fields.Char(
        string="Value", 
        compute="_compute_value_name", 
        help="Actual result.")                    
    value_missing = fields.Char(
        string="Value",
        help="Missing actual result.")                    
    value_quantity = fields.Float(
        string="Value Quantity", 
        help="Quantity actual result.")                    
    value_quantity_uom_id = fields.Many2one(
        comodel_name="product.uom", 
        string="Value Quantity UOM", 
        help="Value quantity unit of measure.")                    
    value_code_id = fields.Many2one(
        comodel_name="hc.vs.observation.value.code", 
        string="Value Code", 
        help="Code of actual result.")                    
    value_string = fields.Char(
        string="Value", 
        help="String of actual result.")                    
    value_range_low = fields.Float(
        string="Value Range Low", 
        help="Low limit of actual result.")                    
    value_range_high = fields.Float(
        string="Value Range High", 
        help="High limit of actual result.")                    
    value_ratio_numerator = fields.Float(
        string="Value Ratio Numerator", 
        help="Numerator value of actual result.")                    
    value_ratio_denominator = fields.Float(
        string="Value Ratio Denominator", 
        help="Denominator value of actual result.")                    
    value_sampled_data_id = fields.Many2one(
        comodel_name="hc.observation.component.value.sampled.data", 
        string="Value Sampled Data", 
        help="Sampled Data actual result.")                    
    value_attachment_id = fields.Many2one(
        comodel_name="hc.observation.component.value.attachment", 
        string="Value Attachment", 
        help="Attachment actual result.")                    
    value_time = fields.Char(
        string="Value Time", 
        help="Time actual result.")                    
    value_date_time = fields.Datetime(
        string="Value Datetime", 
        help="DateTime actual result.")                    
    value_start_date = fields.Datetime(
        string="Value Start Date", 
        help="Start of the actual result.")
    value_end_date = fields.Datetime(
        string="Value End Date", 
        help="End of the actual result.")                  
    data_absent_reason_id = fields.Many2one(
        comodel_name="hc.vs.observation.value.absent.reason", 
        string="Data Absent Reason", 
        help="Why the result is missing.")                    
    interpretation_id = fields.Many2one(
        comodel_name="hc.vs.observation.interpretation", 
        string="Interpretation", 
        help="High, low, normal, etc.")
    reference_range_ids = fields.One2many(
        comodel_name="hc.observation.component.reference.range", 
        inverse_name="observation_component_id", 
        string="Reference Ranges", 
        help="Provides guide for interpretation.")                    

    @api.multi            
    def _compute_value_name(self):            
        for hc_res_observation in self:        
            if hc_res_observation.value_type == 'missing':    
                hc_res_observation.value_name = hc_res_observation.value_missing
            elif hc_res_observation.value_type == 'quantity':    
                hc_res_observation.value_name = hc_res_observation.value_quantity
            elif hc_res_observation.value_type == 'code':    
                hc_res_observation.value_name = hc_res_observation.value_codeable_concept_id.name
            elif hc_res_observation.value_type == 'string':    
                hc_res_observation.value_name = hc_res_observation.value_string
            elif hc_res_observation.value_type == 'range':    
                hc_res_observation.value_name = hc_res_observation.value_range_id.name
            elif hc_res_observation.value_type == 'ratio':    
                hc_res_observation.value_name = hc_res_observation.value_ratio_id.name
            elif hc_res_observation.value_type == 'sampled_data':   
                hc_res_observation.value_name = hc_res_observation.value_sampled_data_id.name
            elif hc_res_observation.value_type == 'Attachment': 
                hc_res_observation.value_name = hc_res_observation.value_attachment_id.name
            elif hc_res_observation.value_type == 'time':   
                hc_res_observation.value_name = hc_res_observation.value_time
            elif hc_res_observation.value_type == 'dateTime':   
                hc_res_observation.value_name = hc_res_observation.value_datetime
            elif hc_res_observation.value_type == 'Period': 
                hc_res_observation.value_name = hc_res_observation.value_period_id.name

class ObservationComponentReferenceRange(models.Model):    
    _name = "hc.observation.component.reference.range"    
    _description = "Observation Component Reference Range"            

    observation_component_id = fields.Many2one(
        comodel_name="hc.observation.component", 
        string="Component", 
        required="True", 
        help="Component associated with this Observation Component Reference Range.")                    
    low = fields.Float(
        string="Low", 
        help="Low Range, if relevant.")                    
    low_uom_id = fields.Many2one(
        comodel_name="product.uom", 
        string="Low UOM", 
        help="Low unit of measure.")                    
    high = fields.Float(
        string="High", 
        help="High Range, if relevant.")                    
    high_uom_id = fields.Many2one(
        comodel_name="product.uom", 
        string="High UOM", 
        help="High unit of measure.")                    
    meaning_id = fields.Many2one(
        comodel_name="hc.vs.reference.range.meaning", 
        string="Meaning", 
        help="Indicates the meaning/use of this range of this range.")                    
    age_range_low = fields.Float(
        string="Age Range Low", 
        help="Low limit of applicable age range, if relevant.")                    
    age_range_high = fields.Float(
        string="Age Range High", 
        help="High limit of applicable age range, if relevant.")                    
    text = fields.Char(
        string="Text", 
        help="Text based reference range in an observation.")                    

class ObservationPerformer(models.Model):    
    _name = "hc.observation.performer"    
    _description = "Observation Performer"        
    _inherit = ["hc.basic.association"]

    observation_id = fields.Many2one(
        comodel_name="hc.res.observation", 
        string="Observation", 
        required="True", 
        help="Observation associated with this Observation Performer.")                    
    performer_type = fields.Selection(
        string="Observation Performer Type", 
        selection=[
            ("practitioner", "Practitioner"), 
            ("organization", "Organization"), 
            ("patient", "Patient"), 
            ("related_person", "Related Person")], 
        help="Type of Who is responsible for the observation.")                    
    performer_name = fields.Char(
        string="Performer", 
        compute="_compute_performer_name", 
        help="Who is responsible for the observation.")                    
    performer_practitioner_id = fields.Many2one(
        comodel_name="hc.res.practitioner", 
        string="Performer Practitioner", 
        help="Practitioner who is responsible for the observation.")                    
    performer_organization_id = fields.Many2one(
        comodel_name="hc.res.organization", 
        string="Performer Organization", 
        help="Organization who is responsible for the observation.")                    
    performer_patient_id = fields.Many2one(
        comodel_name="hc.res.patient", 
        string="Performer Patient", 
        help="Patient who is responsible for the observation.")                    
    performer_related_person_id = fields.Many2one(
        comodel_name="hc.res.related.person", 
        string="Performer Related Person", 
        help="Related Person who is responsible for the observation.")                    

    @api.multi          
    def _compute_performer_name(self):          
        for hc_res_observation in self:     
            if hc_res_observation.performer_type == 'practitioner': 
                hc_res_observation.performer_name = hc_res_observation.performer_practitioner_id.name
            elif hc_res_observation.performer_type == 'organization':   
                hc_res_observation.performer_name = hc_res_observation.performer_organization_id.name
            elif hc_res_observation.performer_type == 'patient':    
                hc_res_observation.performer_name = hc_res_observation.performer_patient_id.name
            elif hc_res_observation.performer_type == 'related_person': 
                hc_res_observation.performer_name = hc_res_observation.performer_related_person_id.name

class ObservationComponentValueAttachment(models.Model):    
    _name = "hc.observation.component.value.attachment"    
    _description = "Observation Component Value Attachment"        
    _inherit = ["hc.basic.association", "hc.attachment"]    

    observation_component_id = fields.Many2one(
        comodel_name="hc.observation.component", 
        string="Component", 
        required="True", 
        help="Component associated with this Observation Component Value Attachment.")                    

class ObservationComponentValueSampledData(models.Model):    
    _name = "hc.observation.component.value.sampled.data"    
    _description = "Observation Component Value Sampled Data"        
    _inherit = ["hc.basic.association", "hc.sampled.data"]    

    observation_component_id = fields.Many2one(
        comodel_name="hc.observation.component", 
        string="Component", 
        required="True", 
        help="Component associated with this Observation Component Value Sampled Data.")                    

class ObservationIdentifier(models.Model):    
    _name = "hc.observation.identifier"    
    _description = "Observation Identifier"        
    _inherit = ["hc.basic.association", "hc.identifier"]    

    observation_id = fields.Many2one(
        comodel_name="hc.res.observation", 
        string="Observation", 
        required="True", 
        help="Observation associated with this Observation Identifier.")                    

class ObservationValueAttachment(models.Model):    
    _name = "hc.observation.value.attachment"    
    _description = "Observation Value Attachment"        
    _inherit = ["hc.basic.association", "hc.attachment"]    

    observation_id = fields.Many2one(
        comodel_name="hc.res.observation", 
        string="Observation", 
        required="True", 
        help="Observation associated with this Observation Value Attachment.")                    

class ObservationValueSampledData(models.Model):    
    _name = "hc.observation.value.sampled.data"    
    _description = "Observation Value Sampled Data"        
    _inherit = ["hc.basic.association", "hc.sampled.data"]    

    observation_id = fields.Many2one(
        comodel_name="hc.res.observation", 
        string="Observation", 
        required="True", 
        help="Observation associated with this Observation Value Sampled Data.")                    

class ObservationCategory(models.Model):    
    _name = "hc.vs.observation.category"    
    _description = "Observation Category"           
    _inherit = ["hc.value.set.contains"]

    name = fields.Char(
        string="Name", 
        help="Name of this observation category.")                    
    code = fields.Char(
        string="Code", 
        help="Code of this observation category.")                    
    contains_id = fields.Many2one(
        comodel_name="hc.vs.observation.category", 
        string="Parent", 
        help="Parent observation category.")                                      

class ObservationInterpretation(models.Model):  
    _name = "hc.vs.observation.interpretation"  
    _description = "Observation Interpretation"         
    _inherit = ["hc.value.set.contains"]

    name = fields.Char(
        string="Name", 
        help="Name of this observation interpretation.")                  
    code = fields.Char(
        string="Code", 
        help="Code of this observation interpretation.")                  
    contains_id = fields.Many2one(
        comodel_name="hc.vs.observation.interpretation", 
        string="Parent", 
        help="Parent observation interpretation.")                    

class ObservationMethod(models.Model):  
    _name = "hc.vs.observation.method"  
    _description = "Observation Method"         
    _inherit = ["hc.value.set.contains"]

    name = fields.Char(
        string="Name", 
        help="Name of this observation method.")                  
    code = fields.Char(
        string="Code", 
        help="Code of this observation method.")                  
    contains_id = fields.Many2one(
        comodel_name="hc.vs.observation.method", 
        string="Parent", 
        help="Parent observation method.")                    

class ObservationValueAbsentReason(models.Model):   
    _name = "hc.vs.observation.value.absent.reason" 
    _description = "Observation Value Absent Reason"            
    _inherit = ["hc.value.set.contains"]

    name = fields.Char(
        string="Name", 
        help="Name of this observation value absent reason.")                 
    code = fields.Char(
        string="Code", 
        help="Code of this observation value absent reason.")                 
    contains_id = fields.Many2one(
        comodel_name="hc.vs.observation.value.absent.reason", 
        string="Parent", 
        help="Parent observation value absent reason.")                  

class ObservationValueCode(models.Model):   
    _name = "hc.vs.observation.value.code"  
    _description = "Observation Value Code"         
    _inherit = ["hc.value.set.contains"]

    name = fields.Char(
        string="Name", 
        help="Name of this observation value code.")                  
    code = fields.Char(
        string="Code", 
        help="Code of this observation value code.")                  
    contains_id = fields.Many2one(
        comodel_name="hc.vs.observation.value.code", 
        string="Parent", 
        help="Parent observation value code.")                    

class ReferenceRangeMeaning(models.Model):  
    _name = "hc.vs.reference.range.meaning" 
    _description = "Reference Range Meaning"            
    _inherit = ["hc.value.set.contains"]

    name = fields.Char(
        string="Name", 
        help="Name of this reference range meaning.")                 
    code = fields.Char(
        string="Code", 
        help="Code of this reference range meaning.")                 
    contains_id = fields.Many2one(
        comodel_name="hc.vs.reference.range.meaning", 
        string="Parent", 
        help="Parent reference range meaning.")                   

# External Reference

class ConditionStageAssessment(models.Model):    
    _inherit = "hc.condition.stage.assessment"

    assessment_observation_id = fields.Many2one(
        comodel_name="hc.res.observation", 
        string="Assessment Observations", 
        help="Observation formal record of assessment.")                    

    @api.depends('assessment_type')                
    def _compute_stage_assessment_name(self):         
        for hc_condition_stage_assessment in self:       
            if hc_condition_stage_assessment.assessment_type == 'observation': 
                hc_condition_stage_assessment.assessment_name = hc_condition_stage_assessment.assessment_observation_id.name

class SequenceVariant(models.Model):    
    _inherit = "hc.sequence.variant"

    variant_pointer_id = fields.Many2one(
        comodel_name="hc.res.observation", 
        string="Variant Pointer", 
        help="A pointer to an Observation containing variant information.")
