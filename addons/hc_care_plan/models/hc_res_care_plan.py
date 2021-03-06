# -*- coding: utf-8 -*-

from openerp import models, fields, api
from datetime import datetime
from openerp.tools import DEFAULT_SERVER_DATETIME_FORMAT as DTF

class CarePlan(models.Model):
    _name = "hc.res.care.plan"
    _description = "Care Plan"
    _rec_name = "title"

    identifier_ids = fields.One2many(
        comodel_name="hc.care.plan.identifier",
        inverse_name="care_plan_id",
        string="Identifiers",
        help="External Ids for this plan.")
    definition_ids = fields.One2many(
        comodel_name="hc.care.plan.definition",
        inverse_name="care_plan_id",
        string="Definitions",
        help="Protocol or definition")
    based_on_ids = fields.One2many(
        comodel_name="hc.care.plan.based.on",
        inverse_name="care_plan_id",
        string="Based Ons",
        help="Fulfills care plan")
    replaces_ids = fields.One2many(
        comodel_name="hc.care.plan.replaces",
        inverse_name="care_plan_id",
        string="Replace",
        help="CarePlan replaced by this CarePlan")
    part_of_ids = fields.One2many(
        comodel_name="hc.care.plan.part.of",
        inverse_name="care_plan_id",
        string="Part Ofs",
        help="Part of referenced CarePlan")
    status = fields.Selection(
        string="Status",
        required="True",
        selection=[
            ("draft", "Draft"),
            ("active", "Active"),
            ("suspended", "Suspended"),
            ("completed", "Completed"),
            ("entered-in-error", "Entered in Error"),
            ("cancelled", "Cancelled"),
            ("unknown", "Unknown")],
        help="Indicates whether the plan is currently being acted upon, represents future intentions or is now a historical record.")
    status_history_ids = fields.One2many(
        comodel_name="hc.care.plan.status.history",
        inverse_name="care_plan_id",
        string="Status History",
        help="The status of the care plan over time.")
    intent = fields.Selection(
        string="Intent",
        required="True",
        selection=[
            ("proposal", "Proposal"),
            ("plan", "Plan"),
            ("order", "Order"),
            ("option", "Option")],
        help="Assertion about certainty associated with the propensity, or potential risk, of a reaction to the identified substance (including pharmaceutical product).")
    intent_history_ids = fields.One2many(
        comodel_name="hc.care.plan.intent.history",
        inverse_name="care_plan_id",
        string="Intent History",
        help="The intent of the care plan over time.")
    category_ids = fields.Many2many(
        comodel_name="hc.vs.care.plan.category",
        relation="care_plan_category_rel",
        string="Categories",
        help="Type of plan.")
    title = fields.Char(
        string="Title",
        help="Human-friendly name for the CarePlan.")
    description = fields.Text(
        string="Description",
        help="Summary of nature of plan.")
    subject_type = fields.Selection(
        string="Subject Type",
        required="True",
        selection=[
            ("patient", "Patient"),
            ("group", "Group")],
        help="Type of who care plan is for.")
    subject_name = fields.Char(
        string="Subject",
        compute="_compute_subject_name",
        store="True",
        help="Who care plan is for.")
    subject_patient_id = fields.Many2one(
        comodel_name="hc.res.patient",
        string="Subject Patient",
        help="Patient who care plan is for.")
    subject_group_id = fields.Many2one(
        comodel_name="hc.res.group",
        string="Subject Group",
        help="Group who care plan is for.")
    context_type = fields.Selection(
        string="Context Type",
        selection=[
            ("encounter", "Encounter"),
            ("episode_of_care", "Episode Of Care")],
        help="Type created in context of.")
    context_name = fields.Char(
        string="Context",
        compute="_compute_context_name",
        store="True",
        help="Created in context of.")
    context_encounter_id = fields.Many2one(
        comodel_name="hc.res.encounter",
        string="Context Encounter",
        help="Encounter created in context of.")
    context_episode_of_care_id = fields.Many2one(
        comodel_name="hc.res.episode.of.care",
        string="Context Episode Of Care",
        help="Episode Of Care created in context of.")
    start_date = fields.Datetime(
        string="Start Date",
        help="Start of the time period plan covers.")
    end_date = fields.Datetime(
        string="End Date",
        help="End of the time period plan covers.")
    author_ids = fields.One2many(
        comodel_name="hc.care.plan.author",
        inverse_name="care_plan_id",
        string="Authors",
        help="Who is responsible for contents of the plan.")
    care_team_ids = fields.One2many(
        comodel_name="hc.care.plan.care.team",
        inverse_name="care_plan_id",
        string="Care Teams",
        help="Who's involved in plan?")
    addresses_ids = fields.One2many(
        comodel_name="hc.care.plan.addresses",
        inverse_name="care_plan_id",
        string="Addresses",
        help="Health issues this plan addresses.")
    supporting_info_ids = fields.One2many(
        comodel_name="hc.care.plan.supporting.info",
        inverse_name="care_plan_id",
        string="Supporting Info",
        help="Information considered as part of plan.")
    goal_ids = fields.One2many(
        comodel_name="hc.care.plan.goal",
        inverse_name="care_plan_id",
        string="Goals",
        help="Desired outcome of plan.")
    note_ids = fields.One2many(
        comodel_name="hc.care.plan.note",
        inverse_name="care_plan_id",
        string="Notes",
        help="Comments about the plan.")
    activity_ids = fields.One2many(
        comodel_name="hc.care.plan.activity",
        inverse_name="care_plan_id",
        string="Activities",
        help="Action to occur as part of plan.")

    @api.model
    def create(self, vals):
        status_history_obj = self.env['hc.care.plan.status.history']
        intent_history_obj = self.env['hc.care.plan.intent.history']
        res = super(CarePlan, self).create(vals)

        # For Status
        if vals and vals.get('status'):
            status_history_vals = {
                'care_plan_id': res.id,
                'status': res.status,
                'start_date': datetime.today()
                }
            if vals.get('status') == 'entered-in-error':
                status_history_vals.update({'end_date': datetime.today()})
            status_history_obj.create(status_history_vals)

        # For Intent
        if vals.get('status') != 'entered-in-error':
            if vals and vals.get('intent'):
                intent_history_vals = {
                    'care_plan_id': res.id,
                    'intent': res.intent,
                    'start_date': datetime.today()
                    }
                intent_history_obj.create(intent_history_vals)

        return res

    @api.multi
    def write(self, vals):
        status_history_obj = self.env['hc.care.plan.status.history']
        intent_history_obj = self.env['hc.care.plan.intent.history']
        res = super(CarePlan, self).write(vals)

        # For Status
        status_history_record_ids = status_history_obj.search([('end_date','=', False)])
        if status_history_record_ids:
            if vals.get('status') and status_history_record_ids[0].status != vals.get('status'):
                for status_history in status_history_record_ids:
                    status_history.end_date = datetime.strftime(datetime.today(), DTF)
                    time_diff = datetime.today() - datetime.strptime(status_history.start_date, DTF)
                    if time_diff:
                        days = str(time_diff).split(',')
                        if days and len(days) > 1:
                            status_history.time_diff_day = str(days[0])
                            times = str(days[1]).split(':')
                            if times and times > 1:
                                status_history.time_diff_hour = str(times[0])
                                status_history.time_diff_min = str(times[1])
                                status_history.time_diff_sec = str(times[2])
                        else:
                            times = str(time_diff).split(':')
                            if times and times > 1:
                                status_history.time_diff_hour = str(times[0])
                                status_history.time_diff_min = str(times[1])
                                status_history.time_diff_sec = str(times[2])
                status_history_vals = {
                    'care_plan_id': self.id,
                    'status': vals.get('status'),
                    'start_date': datetime.today()
                    }
                if vals.get('status') == 'entered-in-error':
                    status_history_vals.update({'end_date': datetime.today()})
                status_history_obj.create(status_history_vals)

        # For Intent
        intent_history_record_ids = intent_history_obj.search([('end_date','=', False)])
        if intent_history_record_ids:
            if vals.get('status') == 'entered-in-error' or (vals.get('intent') and intent_history_record_ids[0].intent != vals.get('intent')):
                for intent_history in intent_history_record_ids:
                    intent_history.end_date = datetime.strftime(datetime.today(), DTF)
                    time_diff = datetime.today() - datetime.strptime(intent_history.start_date, DTF)
                    if time_diff:
                        days = str(time_diff).split(',')
                        if days and len(days) > 1:
                            intent_history.time_diff_day = str(days[0])
                            times = str(days[1]).split(':')
                            if times and times > 1:
                                intent_history.time_diff_hour = str(times[0])
                                intent_history.time_diff_min = str(times[1])
                                intent_history.time_diff_sec = str(times[2])
                        else:
                            times = str(time_diff).split(':')
                            if times and times > 1:
                                intent_history.time_diff_hour = str(times[0])
                                intent_history.time_diff_min = str(times[1])
                                intent_history.time_diff_sec = str(times[2])
                    intent_history_vals = {
                        'care_plan_id': self.id,
                        'intent': vals.get('intent'),
                        'start_date': datetime.today()
                        }
                    if vals.get('status') == 'entered-in-error':
                        intent_history_vals.update({'end_date': datetime.today()})
                    if vals.get('status') != 'entered-in-error':
                        intent_history_obj.create(intent_history_vals)
        else:
            intent_history_vals = {
                    'care_plan_id': self.id,
                    'intent': vals.get('intent'),
                    'start_date': datetime.today()
                    }
            if vals.get('status') == 'entered-in-error':
                    intent_history_vals.update({'end_date': datetime.today()})
            intent_history_obj.create(intent_history_vals)

        return res

    @api.depends('subject_type')
    def _compute_subject_name(self):
        for hc_res_care_plan in self:
            if hc_res_care_plan.subject_type == 'patient':
                hc_res_care_plan.subject_name = hc_res_care_plan.subject_patient_id.name
            elif hc_res_care_plan.subject_type == 'group':
                hc_res_care_plan.subject_name = hc_res_care_plan.subject_group_id.name

    @api.depends('context_type')
    def _compute_context_name(self):
        for hc_res_care_plan in self:
            if hc_res_care_plan.context_type == 'encounter':
                hc_res_care_plan.context_name = hc_res_care_plan.context_encounter_id.name
            elif hc_res_care_plan.context_type == 'episode_of_care':
                hc_res_care_plan.context_name = hc_res_care_plan.context_episode_of_care_id.name

class CarePlanActivity(models.Model):
    _name = "hc.care.plan.activity"
    _description = "Care Plan Activity"

    care_plan_id = fields.Many2one(
        comodel_name="hc.res.care.plan",
        string="Care Plan",
        help="Care Plan associated with this activity.")
    outcome_codeable_concept_ids = fields.Many2many(
        comodel_name="hc.vs.care.plan.activity.outcome",
        relation="care_plan_activity_outcome_codeable_concept_rel",
        string="Categories",
        help="Results of the activity.")
    outcome_reference_ids = fields.One2many(
        comodel_name="hc.care.plan.activity.outcome.reference",
        inverse_name="activity_id",
        string="Outcome References",
        help="Appointment, Encounter, Procedure, etc..")
    progress_ids = fields.One2many(
        comodel_name="hc.care.plan.activity.progress",
        inverse_name="activity_id",
        string="Progress",
        help="Comments about the activity status/progress.")
    reference_type = fields.Selection(
        string="Reference Type",
        selection=[
            ("appointment", "Appointment"),
            ("communication_request", "Communication Request"),
            ("device_request", "Device Request"),
            ("medication_request", "Medication Request"),
            ("nutrition_order", "Nutrition Order"),
            ("task", "Task"),
            ("procedure_request", "Procedure Request"),
            ("vision_prescription", "Vision Prescription"),
            ("request_group", "Request Group")],
        help="Type of activity details defined in specific resource.")
    reference_name = fields.Char(
        string="Reference",
        compute="_compute_reference_name",
        store="True",
        help="Activity details defined in specific resource.")
    reference_appointment_id = fields.Many2one(
        comodel_name="hc.res.appointment",
        string="Reference Appointment",
        help="Appointment activity details defined in specific resource.")
    reference_communication_request_id = fields.Many2one(
        comodel_name="hc.res.communication.request",
        string="Reference Communication Request",
        help="Communication Request activity details defined in specific resource.")
    reference_device_request_id = fields.Many2one(
        comodel_name="hc.res.device.request",
        string="Reference Device Request",
        help="Device Request activity details defined in specific resource.")
    reference_medication_request_id = fields.Many2one(
        comodel_name="hc.res.medication.request",
        string="Reference Medication Request",
        help="Medication Request activity details defined in specific resource.")
    reference_nutrition_order_id = fields.Many2one(
        comodel_name="hc.res.nutrition.order",
        string="Reference Nutrition Order",
        help="Nutrition Order activity details defined in specific resource.")
    reference_task_id = fields.Many2one(
        comodel_name="hc.res.task",
        string="Reference Task",
        help="Task activity details defined in specific resource.")
    reference_procedure_request_id = fields.Many2one(
        comodel_name="hc.res.procedure.request",
        string="Reference Procedure Request",
        help="Procedure Request activity details defined in specific resource.")
    reference_vision_prescription_id = fields.Many2one(
        comodel_name="hc.res.vision.prescription",
        string="Reference Vision Prescription",
        help="Vision Prescription activity details defined in specific resource.")
    reference_request_group_id = fields.Many2one(
        comodel_name="hc.res.request.group",
        string="Reference Request Group",
        help="Request Group activity details defined in specific resource.")
    detail_id = fields.Many2one(
        comodel_name="hc.care.plan.activity.detail",
        string="Detail",
        help="In-line definition of activity.")

class CarePlanActivityDetail(models.Model):
    _name = "hc.care.plan.activity.detail"
    _description = "Care Plan Activity Detail"

    name = fields.Char(
        string="Name",
        required="True",
        help="Human-friendly name for the Care Plan Activity Detail.")
    category = fields.Selection(
        string="Category",
        required="True",
        selection=[
            ("diet", "Diet"),
            ("drug", "Drug"),
            ("encounter", "Encounter"),
            ("observation", "Observation"),
            ("procedure", "Procedure"),
            ("supply", "Supply"),
            ("other", "Other")],
        help="High-level categorization of the type of activity in a care plan.")
    definition_type = fields.Selection(
        string="Definition Type",
        selection=[
            ("plan_definition", "Plan Definition"),
            ("activity_definition", "Activity Definition"),
            ("questionnaire", "Questionnaire")],
        help="Type created in context of.")
    definition_name = fields.Char(
        string="Definition",
        compute="_compute_definition_name",
        store="True",
        help="Protocol or definition.")
    definition_plan_definition_id = fields.Many2one(
        comodel_name="hc.res.plan.definition",
        string="Definition Plan Definition",
        help="Plan Definition protocol or definition.")
    definition_activity_definition_id = fields.Many2one(
        comodel_name="hc.res.activity.definition",
        string="Definition Activity Definition",
        help="Activity Definition protocol or definition.")
    definition_questionnaire_id = fields.Many2one(
        comodel_name="hc.res.questionnaire",
        string="Definition Questionnaire",
        help="Questionnaire protocol or definition.")
    code_id = fields.Many2one(
        comodel_name="hc.vs.care.plan.activity",
        string="Code",
        help="Detail type of activity.")
    reason_code_ids = fields.Many2many(
        comodel_name="hc.vs.activity.reason",
        relation="care_plan_activity_detail_reason_code_rel",
        string="Reason Codes",
        help="Why activity should be done.")
    reason_reference_ids = fields.One2many(
        comodel_name="hc.care.plan.activity.detail.reason.reference",
        inverse_name="detail_id",
        string="Reason References",
        help="Condition triggering need for activity.")
    goal_ids = fields.One2many(
        comodel_name="hc.care.plan.activity.detail.goal",
        inverse_name="detail_id",
        string="Goals",
        help="Goals this activity relates to.")
    status = fields.Selection(
        string="Status",
        required="True",
        selection=[
            ("not-started", "Not-Started"),
            ("scheduled", "Scheduled"),
            ("in-progress", "In-Progress"),
            ("on-hold", "On-Hold"),
            ("completed", "Completed"),
            ("cancelled", "Cancelled"),
            ("stopped", "Stopped"),
            ("unknown", "Unknown")],
        help="The status of this activity definition. Enables tracking the life-cycle of the content.")
    status_history_ids = fields.One2many(
        comodel_name="hc.care.plan.activity.detail.status.history",
        inverse_name="detail_id",
        string="Status History",
        help="The status of the care plan activity detail over time.")
    status_reason = fields.Text(
        string="Status Reason",
        help="Reason for current status.")
    is_prohibited = fields.Boolean(
        string="Prohibited",
        required="True",
        help="Do NOT do.")
    scheduled_type = fields.Selection(
        string="Scheduled Type",
        selection=[
            ("timing", "Timing"),
            ("period", "Period"),
            ("string", "String")],
        help="Type of when activity is to occur.")
    scheduled_name = fields.Char(
        string="Scheduled",
        compute="_compute_scheduled_name",
        store="True",
        help="When activity is to occur.")
    scheduled_timing_id = fields.Many2one(
        comodel_name="hc.care.plan.activity.detail.scheduled.timing",
        string="Scheduled Timing",
        help="Timing when activity is to occur.")
    scheduled_start_date = fields.Datetime(
        string="Scheduled Start Date",
        help="Start of the when activity is to occur.")
    scheduled_end_date = fields.Datetime(
        string="Scheduled End Date",
        help="End of the when activity is to occur.")
    scheduled = fields.Char(
        string="Scheduled",
        help="string when activity is to occur.")
    location_id = fields.Many2one(
        comodel_name="hc.res.location",
        string="Location",
        help="Where it should happen.")
    performer_ids = fields.One2many(
        comodel_name="hc.care.plan.activity.detail.performer",
        inverse_name="detail_id",
        string="Performers",
        help="Who will be responsible?")
    product_type = fields.Selection(
        string="Product Type",
        selection=[
            ("code", "Code"),
            ("medication", "Medication"),
            ("substance", "Substance")],
        help="Type of what is to be administered/supplied.")
    product_name = fields.Char(
        string="Product",
        compute="_compute_product_name",
        store="True",
        help="What is to be administered/supplied.")
    product_code_id = fields.Many2one(
        comodel_name="hc.vs.medication.code",
        string="Product Code",
        help="What is to be administered/supplied.")
    product_medication_id = fields.Many2one(
        comodel_name="hc.res.medication",
        string="Product Medication",
        help="Medication what is to be administered/supplied.")
    product_substance_id = fields.Many2one(
        comodel_name="hc.res.substance",
        string="Product Substance",
        help="Substance what is to be administered/supplied.")
    daily_amount = fields.Float(
        string="Daily Amount",
        help="How to consume/day?")
    daily_amount_uom_id = fields.Many2one(
        comodel_name="product.uom",
        string="Daily Amount UOM",
        help="Daily amount unit of measure.")
    quantity = fields.Float(
        string="Quantity",
        help="How much to administer/supply/consume.")
    quantity_uom_id = fields.Many2one(
        comodel_name="product.uom",
        string="Quantity UOM",
        help="Quantity unit of measure.")
    description = fields.Text(
        string="Description",
        help="Extra info describing activity to perform.")

    @api.model
    def create(self, vals):
        status_history_obj = self.env['hc.care.plan.activity.detail.status.history']
        res = super(CarePlanActivityDetail, self).create(vals)
        if vals and vals.get('status'):
            status_history_vals = {
                'detail_id': res.id,
                'status': res.status,
                'start_date': datetime.today()
                }
            status_history_obj.create(status_history_vals)
        return res

    @api.multi
    def write(self, vals):
        status_history_obj = self.env['hc.care.plan.activity.detail.status.history']
        res = super(CarePlanActivityDetail, self).write(vals)
        status_history_record_ids = status_history_obj.search([('end_date','=', False)])
        if status_history_record_ids:
            if vals.get('status') and status_history_record_ids[0].status != vals.get('status'):
                for status_history in status_history_record_ids:
                    status_history.end_date = datetime.strftime(datetime.today(), DTF)
                    time_diff = datetime.today() - datetime.strptime(status_history.start_date, DTF)
                    if time_diff:
                        days = str(time_diff).split(',')
                        if days and len(days) > 1:
                            status_history.time_diff_day = str(days[0])
                            times = str(days[1]).split(':')
                            if times and times > 1:
                                status_history.time_diff_hour = str(times[0])
                                status_history.time_diff_min = str(times[1])
                                status_history.time_diff_sec = str(times[2])
                        else:
                            times = str(time_diff).split(':')
                            if times and times > 1:
                                status_history.time_diff_hour = str(times[0])
                                status_history.time_diff_min = str(times[1])
                                status_history.time_diff_sec = str(times[2])
                status_history_vals = {
                    'detail_id': self.id,
                    'status': vals.get('status'),
                    'start_date': datetime.today()
                    }
                status_history_obj.create(status_history_vals)
        return res

    @api.depends('definition_type')
    def _compute_definition_name(self):
        for hc_care_plan_activity_detail in self:
            if hc_care_plan_activity_detail.definition_type == 'encounter':
                hc_care_plan_activity_detail.definition_name = hc_care_plan_activity_detail.definition_encounter_id.name
            elif hc_care_plan_activity_detail.definition_type == 'episode_of_care':
                hc_care_plan_activity_detail.definition_name = hc_care_plan_activity_detail.definition_episode_of_care_id.name

    @api.depends('scheduled_type')
    def _compute_scheduled_name(self):
        for hc_care_plan_activity_detail in self:
            if hc_care_plan_activity_detail.scheduled_type == 'timing':
                hc_care_plan_activity_detail.scheduled_name = hc_care_plan_activity_detail.scheduled_timing_id.name
            elif hc_care_plan_activity_detail.scheduled_type == 'period':
                hc_care_plan_activity_detail.scheduled_name = "Between " + str(hc_care_plan_activity_detail.scheduled_start_date) + " and " + str(hc_care_plan_activity_detail.scheduled_end_date)
            elif hc_care_plan_activity_detail.scheduled_type == 'string':
                hc_care_plan_activity_detail.scheduled_type = hc_care_plan_activity_detail.hc_care_plan_activity_detail_string

    @api.depends('product_type')
    def _compute_product_name(self):
        for hc_care_plan_activity_detail in self:
            if hc_care_plan_activity_detail.product_type == 'code':
                hc_care_plan_activity_detail.product_name = hc_care_plan_activity_detail.product_code_id.name
            elif hc_care_plan_activity_detail.product_type == 'medication':
                hc_care_plan_activity_detail.product_name = hc_care_plan_activity_detail.product_medication_id.name
            elif hc_care_plan_activity_detail.product_type == 'substance':
                hc_care_plan_activity_detail.product_name = hc_care_plan_activity_detail.product_substance_id.name


class CarePlanIdentifier(models.Model):
    _name = "hc.care.plan.identifier"
    _description = "Care Plan Identifier"
    _inherit = ["hc.basic.association", "hc.identifier"]

    care_plan_id = fields.Many2one(
        comodel_name="hc.res.care.plan",
        string="Care Plan",
        help="Care Plan associated with this care plan identifier.")

class CarePlanDefinition(models.Model):
    _name = "hc.care.plan.definition"
    _description = "Care Plan Definition"
    _inherit = ["hc.basic.association"]

    care_plan_id = fields.Many2one(
        comodel_name="hc.res.care.plan",
        string="Care Plan",
        help="Care Plan associated with this Care Plan Definition.")
    definition_type = fields.Selection(
        string="Definition Type",
        selection=[
            ("plan_definition", "Plan Definition"),
            ("questionnaire", "Questionnaire")],
        help="Protocol or definition.")
    definition_name = fields.Char(
        string="Definition",
        compute="_compute_definition_name",
        store="True",
        help="Protocol or definition.")
    definition_plan_definition_id = fields.Many2one(
        comodel_name="hc.res.plan.definition",
        string="Definition Plan Definition",
        help="Plan Definition protocol or definition.")
    definition_questionnaire_id = fields.Many2one(
        comodel_name="hc.res.questionnaire",
        string="Definition Questionnaire",
        help="Questionnaire protocol or definition.")

    @api.depends('definition_type')
    def _compute_definition_name(self):
        for hc_care_plan_definition in self:
            if hc_care_plan_definition.definition_type == 'plan_definition':
                hc_care_plan_definition.definition_name = hc_care_plan_definition.definition_plan_definition_id.name
            elif hc_care_plan_definition.definition_type == 'questionnaire':
                hc_care_plan_definition.definition_name = hc_care_plan_definition.definition_questionnaire_id.name

class CarePlanBasedOn(models.Model):
    _name = "hc.care.plan.based.on"
    _description = "Care Plan Based On"
    _inherit = ["hc.basic.association"]

    care_plan_id = fields.Many2one(
        comodel_name="hc.res.care.plan",
        string="Care Plan",
        help="Care Plan associated with this Care Plan Based On.")
    based_on_id = fields.Many2one(
        comodel_name="hc.res.care.plan",
        string="Based On",
        help="Care Plan associated with this Care Plan Based On.")

class CarePlanReplaces(models.Model):
    _name = "hc.care.plan.replaces"
    _description = "Care Plan Replaces"
    _inherit = ["hc.basic.association"]

    care_plan_id = fields.Many2one(
        comodel_name="hc.res.care.plan",
        string="Care Plan",
        help="Care Plan associated with this Care Plan Replaces.")
    replaces_id = fields.Many2one(
        comodel_name="hc.res.care.plan",
        string="Replaces",
        help="Care Plan associated with this Care Plan Replaces.")

class CarePlanPartOf(models.Model):
    _name = "hc.care.plan.part.of"
    _description = "Care Plan Part Of"
    _inherit = ["hc.basic.association"]

    care_plan_id = fields.Many2one(
        comodel_name="hc.res.care.plan",
        string="Care Plan",
        help="Care Plan associated with this Care Plan Part Of.")
    part_of_id = fields.Many2one(
        comodel_name="hc.res.care.plan",
        string="Part Of",
        help="Care Plan associated with this Care Plan Part Of.")

class CarePlanStatusHistory(models.Model):
    _name = "hc.care.plan.status.history"
    _description = "Care Plan Status History"

    care_plan_id = fields.Many2one(
        comodel_name="hc.res.care.plan",
        string="Care Plan",
        help="Care Plan associated with this Care Plan Status History.")
    status = fields.Char(
        string="Status",
        help="The status of the care plan.")
    start_date = fields.Datetime(
        string="Start Date",
        help="Start of the period during which this care plan status is valid.")
    end_date = fields.Datetime(
        string="End Date",
        help="End of the period during which this care plan status is valid.")
    time_diff_day = fields.Char(
        string="Time Diff (days)",
        help="Days duration of the status.")
    time_diff_hour = fields.Char(
        string="Time Diff (hours)",
        help="Hours duration of the status.")
    time_diff_min = fields.Char(
        string="Time Diff (minutes)",
        help="Minutes duration of the status.")
    time_diff_sec = fields.Char(
        string="Time Diff (seconds)",
        help="Seconds duration of the status.")

class CarePlanIntentHistory(models.Model):
    _name = "hc.care.plan.intent.history"
    _description = "Care Plan Intent History"

    care_plan_id = fields.Many2one(
        comodel_name="hc.res.care.plan",
        string="Care Plan",
        help="Care Plan associated with this Care Plan Intent History.")
    intent = fields.Char(
        string="Intent",
        help="The intent of the care plan.")
    start_date = fields.Datetime(
        string="Start Date",
        help="Start of the period during which this care plan intent is valid.")
    end_date = fields.Datetime(
        string="End Date",
        help="End of the period during which this care plan intent is valid.")
    time_diff_day = fields.Char(
        string="Time Diff (days)",
        help="Days duration of the intent.")
    time_diff_hour = fields.Char(
        string="Time Diff (hours)",
        help="Hours duration of the intent.")
    time_diff_min = fields.Char(
        string="Time Diff (minutes)",
        help="Minutes duration of the intent.")
    time_diff_sec = fields.Char(
        string="Time Diff (seconds)",
        help="Seconds duration of the intent.")

class CarePlanAuthor(models.Model):
    _name = "hc.care.plan.author"
    _description = "Care Plan Author"
    _inherit = ["hc.basic.association"]

    care_plan_id = fields.Many2one(
        comodel_name="hc.res.care.plan",
        string="Care Plan",
        help="Care Plan associated with this Care Plan Author.")
    author_type = fields.Selection(
        string="Author Type",
        selection=[
            ("patient", "Patient"),
            ("practitioner", "Practitioner"),
            ("related_person", "Related Person"),
            ("organization", "Organization"),
            ("care_team", "Care Team")],
        help="Type of who is responsible for contents of the plan.")
    author_name = fields.Char(
        string="Author",
        compute="_compute_author_name",
        store="True",
        help="Who is responsible for contents of the plan.")
    author_patient_id = fields.Many2one(
        comodel_name="hc.res.patient",
        string="Author Patient",
        help="Patient who is responsible for contents of the plan.")
    author_practitioner_id = fields.Many2one(
        comodel_name="hc.res.practitioner",
        string="Author Practitioner",
        help="Practitioner who is responsible for contents of the plan.")
    author_related_person_id = fields.Many2one(
        comodel_name="hc.res.related.person",
        string="Author Related Person",
        help="Related Person who is responsible for contents of the plan.")
    author_organization_id = fields.Many2one(
        comodel_name="hc.res.organization",
        string="Author Organization",
        help="Organization who is responsible for contents of the plan.")
    author_care_team_id = fields.Many2one(
        comodel_name="hc.res.care.team",
        string="Author Care Team",
        help="Care Team who is responsible for contents of the plan.")

    @api.depends('author_type')
    def _compute_author_name(self):
        for hc_care_plan_author in self:
            if hc_care_plan_author.author_type == 'patient':
                hc_care_plan_author.author_name = hc_care_plan_author.author_patient_id.name
            elif hc_care_plan_author.author_type == 'practitioner':
                hc_care_plan_author.author_name = hc_care_plan_author.author_practitioner_id.name
            elif hc_care_plan_author.author_type == 'related_person':
                hc_care_plan_author.author_name = hc_care_plan_author.author_related_person_id.name
            elif hc_care_plan_author.author_type == 'organization':
                hc_care_plan_author.author_name = hc_care_plan_author.author_organization_id.name
            elif hc_care_plan_author.author_type == 'care_team':
                hc_care_plan_author.author_name = hc_care_plan_author.author_care_team_id.name

class CarePlanCareTeam(models.Model):
    _name = "hc.care.plan.care.team"
    _description = "Care Plan Care Team"
    _inherit = ["hc.basic.association"]

    care_plan_id = fields.Many2one(
        comodel_name="hc.res.care.plan",
        string="Care Plan",
        help="Care Plan associated with this Care Plan Care Team.")
    care_team_id = fields.Many2one(
        comodel_name="hc.res.care.team",
        string="Care Team",
        help="Care Team associated with this Care Plan Care Team.")

class CarePlanAddresses(models.Model):
    _name = "hc.care.plan.addresses"
    _description = "Care Plan Addresses"
    _inherit = ["hc.basic.association"]

    care_plan_id = fields.Many2one(
        comodel_name="hc.res.care.plan",
        string="Care Plan",
        help="Care Plan associated with this Care Plan Addresses.")
    addresses_id = fields.Many2one(
        comodel_name="hc.res.condition",
        string="Addresses",
        help="Condition associated with this Care Plan Addresses.")

class CarePlanSupportingInfo(models.Model):
    _name = "hc.care.plan.supporting.info"
    _description = "Care Plan Supporting Info"
    _inherit = ["hc.basic.association"]

    care_plan_id = fields.Many2one(
        comodel_name="hc.res.care.plan",
        string="Care Plan",
        help="Care Plan associated with this Care Plan Supporting Info.")
    supporting_info_type = fields.Char(
        string="Supporting Info Type",
        compute="_compute_supporting_info_type",
        store="True",
        help="Type of information considered as part of plan.")
    supporting_info_name = fields.Reference(
        string="Supporting Info",
        selection="_reference_models",
        help="Information considered as part of plan.")

    @api.model
    def _reference_models(self):
        models = self.env['ir.model'].search([('state', '!=', 'manual')])
        return [(model.model, model.name)
            for model in models
                if model.model.startswith('hc.res')]

    @api.depends('supporting_info_name')
    def _compute_supporting_info_type(self):
        for this in self:
            if this.supporting_info_name:
                this.supporting_info_type = this.supporting_info_name._description

class CarePlanGoal(models.Model):
    _name = "hc.care.plan.goal"
    _description = "Care Plan Goal"
    _inherit = ["hc.basic.association"]

    care_plan_id = fields.Many2one(
        comodel_name="hc.res.care.plan",
        string="Care Plan",
        help="Care Plan associated with this Care Plan Goal.")
    goal_id = fields.Many2one(
        comodel_name="hc.res.goal",
        string="Goal",
        help="Goal associated with this Care Plan Goal.")

class CarePlanNote(models.Model):
    _name = "hc.care.plan.note"
    _description = "Care Plan Note"
    _inherit = ["hc.basic.association", "hc.annotation"]

    care_plan_id = fields.Many2one(
        comodel_name="hc.res.care.plan",
        string="Care Plan",
        help="Care Plan associated with this Care Plan Note.")

class CarePlanActivityOutcomeReference(models.Model):
    _name = "hc.care.plan.activity.outcome.reference"
    _description = "Care Plan Activity Outcome Reference"
    _inherit = ["hc.basic.association"]

    activity_id = fields.Many2one(
        comodel_name="hc.care.plan.activity",
        string="Activity",
        help="Activity associated with this Care Plan Activity Outcome Reference.")
    outcome_reference_type = fields.Char(
        string="Outcome Reference Type",
        compute="_compute_outcome_reference_type",
        store="True",
        help="Appointment, Encounter, Procedure, etc..")
    outcome_reference_name = fields.Reference(
        string="Outcome Reference",
        selection="_reference_models",
        help="Appointment, Encounter, Procedure, etc..")

    @api.model
    def _reference_models(self):
        models = self.env['ir.model'].search([('state', '!=', 'manual')])
        return [(model.model, model.name)
            for model in models
                if model.model.startswith('hc.res')]

    @api.depends('outcome_reference_name')
    def _compute_outcome_reference_type(self):
        for this in self:
            if this.outcome_reference_name:
                this.outcome_reference_type = this.outcome_reference_name._description

class CarePlanActivityProgress(models.Model):
    _name = "hc.care.plan.activity.progress"
    _description = "Care Plan Activity Progress"
    _inherit = ["hc.basic.association", "hc.annotation"]

    activity_id = fields.Many2one(
        comodel_name="hc.care.plan.activity",
        string="Activity",
        help="Activity associated with this Care Plan Activity Progress.")

class CarePlanActivityDetailReasonReference(models.Model):
    _name = "hc.care.plan.activity.detail.reason.reference"
    _description = "Care Plan Activity Detail Reason Reference"
    _inherit = ["hc.basic.association"]

    detail_id = fields.Many2one(
        comodel_name="hc.care.plan.activity.detail",
        string="Detail",
        help="Detail associated with this Care Plan Activity Detail Reason Reference.")
    reason_reference_id = fields.Many2one(
        comodel_name="hc.res.condition",
        string="Reason Reference",
        help="Condition associated with this Care Plan Activity Detail Reason Reference.")

class CarePlanActivityDetailGoal(models.Model):
    _name = "hc.care.plan.activity.detail.goal"
    _description = "Care Plan Activity Detail Goal"
    _inherit = ["hc.basic.association"]

    detail_id = fields.Many2one(
        comodel_name="hc.care.plan.activity.detail",
        string="Detail",
        help="Detail associated with this Care Plan Activity Detail Goal.")
    goal_id = fields.Many2one(
        comodel_name="hc.care.plan.goal",
        string="Goal",
        help="Goal associated with this Care Plan Activity Detail Goal.")

class CarePlanActivityDetailStatusHistory(models.Model):
    _name = "hc.care.plan.activity.detail.status.history"
    _description = "Care Plan Activity Detail Status History"

    detail_id = fields.Many2one(
        comodel_name="hc.care.plan.activity.detail",
        string="Detail",
        help="Detail associated with this Care Plan Activity Detail Status History.")
    status = fields.Char(
        string="Status",
        help="The status of the care plan activity detail.")
    start_date = fields.Datetime(
        string="Start Date",
        help="Start of the period during which this care plan activity detail status is valid.")
    end_date = fields.Datetime(
        string="End Date",
        help="End of the period during which this care plan activity detail status is valid.")
    time_diff_day = fields.Char(
        string="Time Diff (days)",
        help="Days duration of the status.")
    time_diff_hour = fields.Char(
        string="Time Diff (hours)",
        help="Hours duration of the status.")
    time_diff_min = fields.Char(
        string="Time Diff (minutes)",
        help="Minutes duration of the status.")
    time_diff_sec = fields.Char(
        string="Time Diff (seconds)",
        help="Seconds duration of the status.")

class CarePlanActivityDetailPerformer(models.Model):
    _name = "hc.care.plan.activity.detail.performer"
    _description = "Care Plan Activity Detail Performer"
    _inherit = ["hc.basic.association"]

    detail_id = fields.Many2one(
        comodel_name="hc.care.plan.activity.detail",
        string="Detail",
        help="Detail associated with this Care Plan Activity Detail Performer.")
    performer_type = fields.Selection(
        string="Performer Type",
        selection=[
            ("practitioner", "Practitioner"),
            ("organization", "Organization"),
            ("related_person", "Related Person"),
            ("patient", "Patient"),
            ("care_team", "Care Team")],
        help="Type of entity assessed.")
    performer_name = fields.Char(
        string="Performer",
        compute="_compute_performer_name",
        store="True",
        help="Who will be responsible?")
    performer_practitioner_id = fields.Many2one(
        comodel_name="hc.res.practitioner",
        string="Performer Practitioner",
        help="Practitioner who will be responsible?")
    performer_organization_id = fields.Many2one(
        comodel_name="hc.res.organization",
        string="Performer Organization",
        help="Organization who will be responsible?")
    performer_related_person_id = fields.Many2one(
        comodel_name="hc.res.related.person",
        string="Performer Related Person",
        help="Related Person who will be responsible?")
    performer_patient_id = fields.Many2one(
        comodel_name="hc.res.patient",
        string="Performer Patient",
        help="Patient who will be responsible?")
    performer_care_team_id = fields.Many2one(
        comodel_name="hc.res.care.team",
        string="Performer Care Team",
        help="Care Team who will be responsible?")

    @api.depends('performer_type')
    def _compute_performer_name(self):
        for hc_care_plan_activity_detail_performer in self:
            if hc_care_plan_activity_detail_performer.performer_type == 'practitioner':
                hc_care_plan_activity_detail_performer.performer_name = hc_care_plan_activity_detail_performer.performer_practitioner_id.name
            elif hc_care_plan_activity_detail_performer.performer_type == 'organization':
                hc_care_plan_activity_detail_performer.performer_name = hc_care_plan_activity_detail_performer.performer_organization_id.name
            elif hc_care_plan_activity_detail_performer.performer_type == 'related_person':
                hc_care_plan_activity_detail_performer.performer_name = hc_care_plan_activity_detail_performer.performer_related_person_id.name
            elif hc_care_plan_activity_detail_performer.performer_type == 'patient':
                hc_care_plan_activity_detail_performer.performer_name = hc_care_plan_activity_detail_performer.performer_patient_id.name
            elif hc_care_plan_activity_detail_performer.performer_type == 'care_team':
                hc_care_plan_activity_detail_performer.performer_name = hc_care_plan_activity_detail_performer.performer_care_team_id.name

class CarePlanActivityDetailScheduledTiming(models.Model):
    _name = "hc.care.plan.activity.detail.scheduled.timing"
    _description = "Care Plan Activity Detail Scheduled Timing"
    _inherit = ["hc.basic.association", "hc.timing"]

class CarePlanCategory(models.Model):
    _name = "hc.vs.care.plan.category"
    _description = "Care Plan Category"
    _inherit = ["hc.value.set.contains"]

    name = fields.Char(
        string="Name",
        help="Name of this care plan category.")
    code = fields.Char(
        string="Code",
        help="Code of this care plan category.")
    contains_id = fields.Many2one(
        comodel_name="hc.vs.care.plan.category",
        string="Parent",
        help="Parent care plan category.")

class CarePlanActivityOutcome(models.Model):
    _name = "hc.vs.care.plan.activity.outcome"
    _description = "Care Plan Activity Outcome"
    _inherit = ["hc.value.set.contains"]

    name = fields.Char(
        string="Name",
        help="Name of this care plan activity outcome.")
    code = fields.Char(
        string="Code",
        help="Code of this care plan activity outcome.")
    contains_id = fields.Many2one(
        comodel_name="hc.vs.care.plan.activity.outcome",
        string="Parent",
        help="Parent care plan activity outcome.")

class CarePlanActivity(models.Model):
    _name = "hc.vs.care.plan.activity"
    _description = "Care Plan Activity"
    _inherit = ["hc.value.set.contains"]

    name = fields.Char(
        string="Name",
        help="Name of this care plan activity.")
    code = fields.Char(
        string="Code",
        help="Code of this care plan activity.")
    contains_id = fields.Many2one(
        comodel_name="hc.vs.care.plan.activity",
        string="Parent",
        help="Parent care plan activity.")

class ActivityReason(models.Model):
    _name = "hc.vs.activity.reason"
    _description = "Activity Reason"
    _inherit = ["hc.value.set.contains"]

    name = fields.Char(
        string="Name",
        help="Name of this activity reason.")
    code = fields.Char(
        string="Code",
        help="Code of this activity reason.")
    contains_id = fields.Many2one(
        comodel_name="hc.vs.activity.reason",
        string="Parent",
        help="Parent activity reason.")


# External Reference

class MedicationRequestBasedOn(models.Model):
    _inherit= "hc.medication.request.based.on"

    based_on_type = fields.Selection(
        string="Based On Type",
        selection_add=[
            ("care_plan", "Care Plan")],
        help="Type of what request fulfills.")
    based_on_care_plan_id = fields.Many2one(
        comodel_name="hc.res.care.plan",
        string="Based On Care Plan",
        help="Care Plan request fulfills.")

class MedicationStatementBasedOn(models.Model):
    _inherit = "hc.medication.statement.based.on"

    based_on_type = fields.Selection(
        string="Based On Type",
        selection_add=[
            ("care_plan", "Care Plan")],
        help="Type of fulfils plan, proposal or order.")
    based_on_care_plan_id = fields.Many2one(
        comodel_name="hc.res.care.plan",
        string="Based On Care Plan",
        help="Care Plan that is fulfilled in whole or in part by this event.")

class ProcedureBasedOn(models.Model):
    _inherit = "hc.procedure.based.on"

    based_on_type = fields.Selection(
        selection_add=[
            ("care_plan", "Care Plan")])
    based_on_care_plan_id = fields.Many2one(
        comodel_name="hc.res.care.plan",
        string="Based On Care Plan",
        help="Care Plan for this procedure.")

class ProcedureRequestBasedOn(models.Model):
    _inherit = "hc.procedure.request.based.on"

    based_on_type = fields.Selection(
        selection_add=[
            ("care_plan", "Care Plan"),
            ("medication_request", "Medication Request")])
    based_on_care_plan_id = fields.Many2one(
        comodel_name="hc.res.care.plan",
        string="Based On Care Plan",
        help="Care Plan fulfills.")
    based_on_medication_request_id = fields.Many2one(
        comodel_name="hc.res.medication.request",
        string="Based On Medication Request",
        help="Medication Request fulfills.")

    @api.multi
    def _compute_based_on_name(self):
        for hc_procedure_request in self:
            if hc_procedure_request.based_on_type == 'procedure_request':
                hc_procedure_request.based_on_name = hc_procedure_request.based_on_procedure_request_id.name
            elif hc_procedure_request.based_on_type == 'care_plan':
                hc_procedure_request.based_on_name = hc_procedure_request.based_on_care_plan_id.name
            elif hc_procedure_request.based_on_type == 'medication_request':
                hc_procedure_request.based_on_name = hc_procedure_request.based_on_medication_request_id.name

class ObservationBasedOn(models.Model):
    _inherit = "hc.observation.based.on"

    based_on_type = fields.Selection(
        selection_add=[
            ("care_plan", "Care Plan"),
            ("device_request", "Device Request"),
            ("medication_request", "Medication Request"),
            ("nutrition_order", "Nutrition Order")])
    based_on_care_plan_id = fields.Many2one(
        comodel_name="hc.res.care.plan",
        string="Based On Care Plan",
        help="Care Plan fulfills plan, proposal or order.")
    based_on_device_request_id = fields.Many2one(
        comodel_name="hc.res.device.request",
        string="Based On Device Request",
        help="Device Request fulfills plan, proposal or order.")
    based_on_medication_request_id = fields.Many2one(
        comodel_name="hc.res.medication.request",
        string="Based On Medication Request",
        help="Medication Request fulfills plan, proposal or order.")
    based_on_nutrition_order_id = fields.Many2one(
        comodel_name="hc.res.nutrition.order",
        string="Based On Nutrition Order",
        help="Nutrition Order fulfills plan, proposal or order.")

    @api.depends('based_on_type')
    def _compute_based_on_name(self):
        for hc_observation_based_on in self:
            if hc_observation_based_on.based_on_type == 'procedure_request':
                hc_observation_based_on.based_on_name = hc_observation_based_on.based_on_procedure_request_id.name
            elif hc_observation_based_on.based_on_type == 'care_plan':
                hc_observation_based_on.based_on_name = hc_observation_based_on.based_on_care_plan_id.name
            elif hc_observation_based_on.based_on_type == 'device_request':
                hc_observation_based_on.based_on_name = hc_observation_based_on.based_on_device_request_id.name
            elif hc_observation_based_on.based_on_type == 'medication_request':
                hc_observation_based_on.based_on_name = hc_observation_based_on.based_on_medication_request_id.name
            elif hc_observation_based_on.based_on_type == 'nutrition_order':
                hc_observation_based_on.based_on_name = hc_observation_based_on.based_on_nutrition_order_id.name
