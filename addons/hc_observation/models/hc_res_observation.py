attrs="{'invisible': [('has_assessment','!=',True)]}"# -*- coding: utf-8 -*-

from openerp import models, fields, api

class Observation(models.Model):
    _name = "hc.res.observation"
    _description = "Observation"
    _inherit = ["hc.domain.resource"]
    _rec_name = "name"

    name = fields.Char(
        string="Event Name",
        required="True",
        help="Text representation of the observation event. Subject Name + Code + Effective Date.")
    identifier_ids = fields.One2many(
        comodel_name="hc.observation.identifier",
        inverse_name="observation_id",
        string="Identifiers",
        help="Unique Id for this particular observation.")
    based_on_ids = fields.One2many(
        comodel_name="hc.observation.based.on",
        inverse_name="observation_id",
        string="Based On",
        help="Fulfills plan, proposal or order.")
    status = fields.Selection(string="Status",
        selection=[
            ("registered", "Registered"),
            ("preliminary", "Preliminary"),
            ("final", "Final"),
            ("amended", "Amended")],
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
    context_type = fields.Selection(
        tring="Context Type",
        selection=[
            ("encounter", "Encounter"),
            ("episode_of_care", "Episode Of Care")],
        help="Healthcare event during which this observation is made.")
    context_name = fields.Char(
        string="Context",
        compute="_compute_context_name",
        store="True",
        help="Healthcare event during which this observation is made.")
    context_encounter_id = fields.Many2one(
        comodel_name="hc.res.encounter",
        string="Context Encounter",
        help="Encounter during which this observation is made.")
    context_episode_of_care_id = fields.Many2one(
        comodel_name="hc.res.episode.of.care",
        string="Context Episode Of Care",
        help="Episode Of Care during which this observation is made.")
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
    effective_date_time = fields.Datetime(
        string="Effective Datetime",
        help="Date time clinically relevant time/time-period for observation.")
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
            ("quantity", "Quantity"),
            ("code", "Code"),
            ("string", "String"),
            ("range", "Range"),
            ("ratio", "Ratio"),
            ("sampled_data", "Sampled Data"),
            ("attachment", "Attachment"),
            ("time", "Time"),
            ("date_time", "Date Time"),
            ("period", "Period")],
        help="Type of result.")
    value_name = fields.Char(
        string="Value",
        compute="_compute_value_name",
        help="Actual result.")
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
    value_numerator = fields.Float(
        string="Value Numerator",
        help="Numerator value of actual result.")
    value_numerator_uom_id = fields.Many2one(
        comodel_name="product.uom",
        string="Value Numerator UOM",
        help="Value numerator unit of measure.")
    value_denominator = fields.Float(
        string="Value Denominator",
        help="Denominator value of actual result.")
    value_denominator_uom_id = fields.Many2one(
        comodel_name="product.uom",
        string="Value Denominator UOM",
        help="Value denominator unit of measure.")
    value_ratio = fields.Float(
        string="Value Ratio",
        compute="_compute_value_ratio",
        store="True",
        help="Ratio of actual result.")
    value_ratio_uom = fields.Char(
        string="Value Ratio UOM",
        compute="_compute_value_ratio_uom",
        store="True", help="Value Ratio unit of measure.")
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
    value_date_time = fields.Datetime(
        string="Value Date Time",
        help="Date Time actual result.")
    value_start_date = fields.Datetime(
        string="Value Start Date",
        help="Start of the actual result.")
    value_end_date = fields.Datetime(
        string="Value End Date",
        help="End of the actual result.")
    is_data_absent = fields.Boolean(
        string="Data Absent",
        help="Result is missing?")
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
    related_ids = fields.One2many(
        comodel_name="hc.observation.related",
        inverse_name="observation_id",
        string="Related",
        help="Observations related to this observation.")
    component_ids = fields.One2many(
        comodel_name="hc.observation.component",
        inverse_name="observation_id",
        string="Components",
        help="Component results.")

    # Extension Attribute
    id = fields.Char(
        string="Id",
        help="Logical id of this artifact.")
    meta_id = fields.Many2one(
        comodel_name="hc.observation.meta",
        string="Meta",
        help="Metadata about the resource.")
    implicit_rules = fields.Char(
        string="Implicit Rules URI",
        help="A set of rules under which this content was created.")
    language_id = fields.Many2one(
        comodel_name="res.lang",
        string="Language",
        help="of the resource content.")
    text_id = fields.Many2one(
        comodel_name="hc.observation.text",
        string="Text",
        help="Text summary of the resource, for human interpretation.")
    contained_ids = fields.One2many(
        comodel_name="hc.observation.contained",
        inverse_name="observation_id",
        string="Contained",
        help="Contained, inline Resources.")
    modifier_extension_ids = fields.One2many(
        comodel_name="hc.observation.modifier.extension",
        inverse_name="observation_id",
        string="Modifier Extensions",
        help="Extensions that cannot be ignored.")

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
                hc_res_observation.effective_name = str(hc_res_observation.effective_date_time)
            elif hc_res_observation.effective_type == 'period':
                hc_res_observation.effective_name = "Between " + str(hc_res_observation.effective_start_date) + " and " + str(hc_res_observation.effective_end_date)

    @api.multi
    def _compute_value_name(self):
        for hc_res_observation in self:
            if hc_res_observation.value_type == 'quantity':
                hc_res_observation.value_name = str(hc_res_observation.value_quantity)
            elif hc_res_observation.value_type == 'code':
                hc_res_observation.value_name = hc_res_observation.value_codeable_concept_id.name
            elif hc_res_observation.value_type == 'string':
                hc_res_observation.value_name = hc_res_observation.value_string
            elif hc_res_observation.value_type == 'range':
                hc_res_observation.value_name = "Between " + str(hc_res_observation.value_range_low) + " and " + str(hc_res_observation.value_range_high)
            elif hc_res_observation.value_type == 'ratio':
                hc_res_observation.value_name = str(hc_res_observation.value_ratio) + " " + str(hc_res_observation_.value_ratio_uom)
            elif hc_res_observation.value_type == 'sampled_data':
                hc_res_observation.value_name = hc_res_observation.value_sampled_data_id.name
            elif hc_res_observation.value_type == 'attachment':
                hc_res_observation.value_name = hc_res_observation.value_attachment_id.name
            elif hc_res_observation.value_type == 'time':
                hc_res_observation.value_name = hc_res_observation.value_time
            elif hc_res_observation.value_type == 'date_time':
                hc_res_observation.value_name = str(hc_res_observation.value_date_time)
            elif hc_res_observation.value_type == 'period':
                hc_res_observation.value_name = "Between " + str(hc_res_observation.value_start_date) + " and " + str(hc_res_observation.value_end_date)

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
    _inherit = ["hc.backbone.element"]

    observation_id = fields.Many2one(
        comodel_name="hc.res.observation",
        string="Observation",
        required="True",
        help="Observation associated with this Observation Reference Range.")
    component_id = fields.Many2one(
        comodel_name="hc.observation.component",
        string="Component",
        required="True",
        help="Component associated with this Observation Reference Range.")
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
    type_id = fields.Many2one(
        comodel_name="hc.vs.reference.range.meaning",
        string="Type",
        help="Reference range qualifier.")
    applies_to_ids = fields.Many2many(
        comodel_name="hc.vs.reference.range.applies.to",
        relation="observation_reference_range_applies_to_rel",
        string="Applies To",
        help="Reference range population.")
    age_range_low = fields.Float(
        string="Age Range Low",
        help="Low limit of applicable age range, if relevant.")
    age_range_high = fields.Float(
        string="Age Range High",
        help="High limit of applicable age range, if relevant.")
    text = fields.Char(
        string="Text",
        help="Text based reference range in an observation.")

    # Extension attribute
    modifier_extension_ids = fields.One2many(
        comodel_name="hc.observation.reference.range.modifier.extension",
        inverse_name="reference_range_id",
        string="Modifier Extensions",
        help="Extensions that cannot be ignored.")

class ObservationRelated(models.Model):
    _name = "hc.observation.related"
    _description = "Observation Related"
    _inherit = ["hc.backbone.element"]

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

    # Extension attribute
    modifier_extension_ids = fields.One2many(
        comodel_name="hc.observation.related.modifier.extension",
        inverse_name="related_id",
        string="Modifier Extensions",
        help="Extensions that cannot be ignored.")

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
    _inherit = ["hc.backbone.element"]

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
            ("quantity", "Quantity"),
            ("code", "Code"),
            ("string", "String"),
            ("range", "Range"),
            ("ratio", "Ratio"),
            ("sampled_data", "Sampled Data"),
            ("attachment", "Attachment"),
            ("time", "Time"),
            ("date_time", "Date Time"),
            ("period", "Period")],
        help="Type of result.")
    value_name = fields.Char(
        string="Value",
        compute="_compute_value_name",
        help="Actual result.")
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
    value_numerator = fields.Float(
        string="Value Numerator",
        help="Numerator value of actual result.")
    value_numerator_uom_id = fields.Many2one(
        comodel_name="product.uom",
        string="Value Numerator UOM",
        help="Value numerator unit of measure.")
    value_denominator = fields.Float(
        string="Value Denominator",
        help="Denominator value of actual result.")
    value_denominator_uom_id = fields.Many2one(
        comodel_name="product.uom",
        string="Value Denominator UOM",
        help="Value denominator unit of measure.")
    value_ratio = fields.Float(
        string="Value Ratio",
        compute="_compute_value_ratio",
        store="True",
        help="Ratio of actual result.")
    value_ratio_uom = fields.Char(
        string="Value Ratio UOM",
        compute="_compute_value_ratio_uom",
        store="True",
        help="Value Ratio unit of measure.")
    value_component = fields.Float(
        string="Value Component",
        compute="_compute_value_component",
        store="True",
        help="Actual result.")
    value_component_uom_id = fields.Many2one(
        comodel_name="product.uom",
        string="Value Component UOM",
        help="Actual result unit of measure.")
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
        string="Value Date Time",
        help="Date Time actual result.")
    value_start_date = fields.Datetime(
        string="Value Start Date",
        help="Start of the actual result.")
    value_end_date = fields.Datetime(
        string="Value End Date",
        help="End of the actual result.")
    is_data_absent = fields.Boolean(
        string="Data Absent",
        help="Result is missing?")
    data_absent_reason_id = fields.Many2one(
        comodel_name="hc.vs.observation.value.absent.reason",
        string="Data Absent Reason",
        help="Why the result is missing.")
    interpretation_id = fields.Many2one(
        comodel_name="hc.vs.observation.interpretation",
        string="Interpretation",
        help="High, low, normal, etc.")
    reference_range_ids = fields.One2many(
        comodel_name="hc.observation.reference.range",
        inverse_name="component_id",
        string="Reference Ranges",
        help="Provides guide for interpretation.")

    # Extension attribute
    modifier_extension_ids = fields.One2many(
        comodel_name="hc.observation.component.modifier.extension",
        inverse_name="component_id",
        string="Modifier Extensions",
        help="Extensions that cannot be ignored.")
    value_quantity_id = fields.Many2one(
        comodel_name="hc.observation.component.value.quantity",
        string="Value Quantity",
        required="True",
        help="Value Quantity associated with this Component.")

    @api.multi
    def _compute_value_name(self):
        for hc_observation_component in self:
            if hc_observation_component.value_type == 'quantity':
                hc_observation_component.value_name = str(hc_observation_component.value_quantity)
            elif hc_observation_component.value_type == 'code':
                hc_observation_component.value_name = hc_observation_component.value_codeable_concept_id.name
            elif hc_observation_component.value_type == 'string':
                hc_observation_component.value_name = hc_observation_component.value_string
            elif hc_observation_component.value_type == 'range':
                hc_observation_component.value_name = "Between " + str(hc_observation_component.value_range_low) + " and " + str(hc_observation_component.value_range_high)
            elif hc_observation_component.value_type == 'ratio':
                hc_observation_component.value_name = str(hc_observation_component.value_ratio) + " " + str(hc_observation_component.value_ratio_uom)
            elif hc_observation_component.value_type == 'sampled_data':
                hc_observation_component.value_name = hc_observation_component.value_sampled_data_id.name
            elif hc_observation_component.value_type == 'attachment':
                hc_observation_component.value_name = hc_observation_component.value_attachment_id.name
            elif hc_observation_component.value_type == 'time':
                hc_observation_component.value_name = hc_observation_component.value_time
            elif hc_observation_component.value_type == 'date_time':
                hc_observation_component.value_name = str(hc_observation_component.value_date_time)
            elif hc_observation_component.value_type == 'period':
                hc_observation_component.value_name = "Between " + str(hc_observation_component.value_start_date) + " and " + str(hc_observation_component.value_end_date)

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

class ObservationComponentValueQuantity(models.Model):
    _name = "hc.observation.component.value.quantity"
    _description = "Observation Component Value Quantity"
    _inherit = ["hc.basic.association"]

    value = fields.Float(
        string="Value",
        required="True",
        help="Numerical value (with implicit precision).")
    comparator = fields.Selection(
        string="Comparator",
        selection=[
            ("<", "<"),
            ("<=", "<="),
            (">=", ">="),
            (">", ">")],
        help="How to understand the value.")
    unit = fields.Char(
        string="Unit",
        required="True",
        help="Unit representation.")
    system = fields.Char(
        string="System",
        required="True",
        help="System that defines coded unit form.")
    code_id = fields.Many2one(
        comodel_name="hc.vs.vital.sign.result",
        string="Code",
        required="True",
        help="responses from the common UCUM units for vital signs value set..")


class ObservationIdentifier(models.Model):
    _name = "hc.observation.identifier"
    _description = "Observation Identifier"
    _inherit = ["hc.basic.association", "hc.identifier"]

    observation_id = fields.Many2one(
        comodel_name="hc.res.observation",
        string="Observation",
        required="True",
        help="Observation associated with this Observation Identifier.")

class ObservationBasedOn(models.Model):
    _name = "hc.observation.based.on"
    _description = "Observation Based On"
    _inherit = ["hc.basic.association"]

    observation_id = fields.Many2one(
        comodel_name="hc.res.observation",
        string="Observation",
        required="True",
        help="Observation associated with this observation based on observation.")
    based_on_type = fields.Selection(
        string="Based On Type",
        selection=[
            # ("care_plan", "Care Plan"),
            # ("device_request", "Device Request"),
            # ("immunization_recommendation", "Immunization Recommendation"),
            # ("medication_request", "Medication Request"),
            # ("nutrition_order", "Nutrition Order"),
            ("procedure_request", "Procedure Request")],
        help="Type of fulfills plan, proposal or order.")
    based_on_name = fields.Char(
        string="Based On",
        compute="_compute_based_on_name",
        store="True",
        help="Fulfills plan, proposal or order.")
    # based_on_care_plan_id = fields.Many2one(
    #     comodel_name="hc.res.care.plan",
    #     string="Based On Care Plan",
    #     help="Care Plan fulfills plan, proposal or order.")
    # based_on_device_request_id = fields.Many2one(
    #     comodel_name="hc.res.device.request",
    #     string="Based On Device Request",
    #     help="Device Request fulfills plan, proposal or order.")
    # based_on_immunization_recommendation_id = fields.Many2one(
    #     comodel_name="hc.res.immunization.recommendation",
    #     string="Based On Immunization Recommendation",
    #     help="Immunization Recommendation fulfills plan, proposal or order.")
    # based_on_medication_request_id = fields.Many2one(
    #     comodel_name="hc.res.medication.request",
    #     string="Based On Medication Request",
    #     help="Medication Request fulfills plan, proposal or order.")
    # based_on_nutrition_order_id = fields.Many2one(
    #     comodel_name="hc.res.nutrition.order",
    #     string="Based On Nutrition Order",
    #     help="Nutrition Order fulfills plan, proposal or order.")
    based_on_procedure_request_id = fields.Many2one(
        comodel_name="hc.res.procedure.request",
        string="Based On Procedure Request",
        help="Procedure Request fulfills plan, proposal or order.")

    @api.depends('based_on_type')
    def _compute_based_on_name(self):
        for hc_observation_based_on in self:
            if hc_observation_based_on.based_on_type == 'procedure_request':
                hc_observation_based_on.based_on_name = hc_observation_based_on.based_on_procedure_request_id.name



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

# Extension Association Class
class ObservationMeta(models.Model):
    _name = "hc.observation.meta"
    _description = "Observation Meta"
    _inherit = ["hc.basic.association", "hc.meta"]

class ObservationText(models.Model):
    _name = "hc.observation.text"
    _description = "Observation Text"
    _inherit = ["hc.basic.association", "hc.narrative"]

class ObservationContained(models.Model):
    _name = "hc.observation.contained"
    _description = "Observation Contained"
    _inherit = ["hc.basic.association", "hc.resource"]

    observation_id = fields.Many2one(
        comodel_name="hc.res.observation",
        string="Observation",
        required="True",
        help="Observation associated with this Observation Contained.")

class ObservationModifierExtension(models.Model):
    _name = "hc.observation.modifier.extension"
    _description = "Observation Modifier Extension"
    _inherit = ["hc.basic.association", "hc.extension"]

    observation_id = fields.Many2one(
        comodel_name="hc.res.observation",
        string="Observation",
        required="True",
        help="Observation associated with this Observation Modifier Extension.")

class ObservationReferenceRangeModifierExtension(models.Model):
    _name = "hc.observation.reference.range.modifier.extension"
    _description = "Observation Reference Range Modifier Extension"
    _inherit = ["hc.basic.association", "hc.extension"]

    reference_range_id = fields.Many2one(
        comodel_name="hc.observation.reference.range",
        string="Reference Range",
        help="Reference Range associated with this Observation Reference Range Modifier Extension.")

class ObservationRelatedModifierExtension(models.Model):
    _name = "hc.observation.related.modifier.extension"
    _description = "Observation Related Modifier Extension"
    _inherit = ["hc.basic.association", "hc.extension"]

    related_id = fields.Many2one(
        comodel_name="hc.observation.related",
        string="Related",
        help="Related associated with this Observation Related Modifier Extension.")

class ObservationComponentModifierExtension(models.Model):
    _name = "hc.observation.component.modifier.extension"
    _description = "Observation Component Modifier Extension"
    _inherit = ["hc.basic.association", "hc.extension"]

    component_id = fields.Many2one(
        comodel_name="hc.observation.component",
        string="Component",
        help="Component associated with this Observation Component Modifier Extension.")

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

class ReferenceRangeAppliesTo(models.Model):
    _name = "hc.vs.reference.range.applies.to"
    _description = "Reference Range Applies To"
    _inherit = ["hc.value.set.contains"]

    name = fields.Char(
        string="Name",
        help="Name of this reference range applies to.")
    code = fields.Char(
        string="Code",
        help="Code of this reference range applies to.")
    contains_id = fields.Many2one(
        comodel_name="hc.vs.reference.range.applies.to",
        string="Parent",
        help="Parent reference range applies to.")

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

class VitalSignResult(models.Model):
    _name = "hc.vs.vital.sign.result"
    _description = "Vital Sign Result"
    _inherit = ["hc.value.set.contains"]

    name = fields.Char(
        string="Name",
        help="Name of this vital sign result.")
    code = fields.Char(
        string="Code",
        help="Code of this vital sign result.")
    contains_id = fields.Many2one(
        comodel_name="hc.vs.vital.sign.result",
        string="Parent",
        help="Parent vital sign result.")

# External Reference

class ConditionStageAssessment(models.Model):
    _inherit = "hc.condition.stage.assessment"

    assessment_type = fields.Selection(
        string="Assessment Type",
        selection=[
            ("observation", "Observation")],
        help="Type of assessment.")
    assessment_name = fields.Char(
        string="Assessment",
        compute="_compute_assessment_name",
        store="True",
        help="Formal record of assessment.")
    assessment_observation_id = fields.Many2one(
        comodel_name="hc.res.observation",
        string="Assessment Observations",
        help="Observation formal record of assessment.")

    @api.depends('assessment_type')
    def _compute_stage_assessment_name(self):
        for hc_condition_stage_assessment in self:
            if hc_condition_stage_assessment.assessment_type == 'observation':
                hc_condition_stage_assessment.assessment_name = hc_condition_stage_assessment.assessment_observation_id.name

class ProcedureRequestReasonReference(models.Model):
    _inherit = "hc.procedure.request.reason.reference"

    reason_reference_type = fields.Selection(
        selection=[
            ("observation", "Observation")])
    reason_reference_observation_id = fields.Many2one(
        comodel_name="hc.res.observation",
        string="Reason Reference Observation",
        help="Observation explanation/justification for procedure or service.")

    @api.multi
    def _compute_reason_reference_name(self):
        for hc_res_procedure_request in self:
            if hc_res_procedure_request.reason_type == 'condition':
                hc_res_procedure_request.reason_name = hc_res_procedure_request.reason_condition_id.name
            elif hc_res_procedure_request.reason_type == 'observation':
                hc_res_procedure_request.reason_name = hc_res_procedure_request.reason_observation_id.name
            elif hc_res_procedure_request.reason_type == 'document_reference':
                hc_res_procedure_request.reason_name = hc_res_procedure_request.reason_document_reference_id.name

class SequenceVariant(models.Model):
    _inherit = "hc.sequence.variant"

    variant_pointer_id = fields.Many2one(
        comodel_name="hc.res.observation",
        string="Variant Pointer",
        help="A pointer to an Observation containing variant information.")
