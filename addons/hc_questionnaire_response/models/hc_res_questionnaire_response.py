# -*- coding: utf-8 -*-

from openerp import models, fields, api

class QuestionnaireResponse(models.Model):
    _name = "hc.res.questionnaire.response"
    _description = "Questionnaire Response"

    name = fields.Char(
        string="Event Name",
        compute="_compute_name",
        store="True",
        help="Text representation of the questionnaire response event. Subject Name + Questionnaire + Authored Date.")
    identifier_id = fields.Many2one(
        comodel_name="hc.questionnaire.response.identifier",
        string="Identifier",
        help="Unique id for this set of answers.")
    based_on_ids = fields.One2many(
        comodel_name="hc.questionnaire.response.based.on",
        inverse_name="questionnaire_response_id",
        string="Based Ons",
        help="Request fulfilled by this Questionnaire.")
    parent_ids = fields.One2many(
        comodel_name="hc.questionnaire.response.parent",
        inverse_name="questionnaire_response_id",
        string="Parents",
        help="Part of this action.")
    questionnaire_id = fields.Many2one(
        comodel_name="hc.res.questionnaire",
        string="Questionnaire",
        help="Form being answered.")
    status = fields.Selection(
        string="Questionnaire Response Status",
        required="True",
        selection=[
            ("in-progress", "In-Progress"),
            ("completed", "Completed"),
            ("amended", "Amended")],
        help="The lifecycle status of the questionnaire response as a whole.")
    subject_type = fields.Char(
        string="Subject Type",
        compute="_compute_subject_type",
        store="True",
        help="Type of subject of the questions.")
    subject_name = fields.Reference(
        string="Subject",
        selection="_reference_models",
        help="The subject of the questions.")
    context_type = fields.Selection(
        string="Context Type",
        required="True",
        selection=[
            ("encounter", "Encounter"),
            ("episode_of_care", "Episode Of Care")],
        help="Encounter or Episode during which questionnaire was completed.")
    context_name = fields.Char(
        string="Context",
        compute="_compute_context_name",
        store="True",
        help="Encounter or Episode during which questionnaire was completed.")
    context_encounter_id = fields.Many2one(
        comodel_name="hc.res.encounter",
        string="Context Encounter",
        help="Encounter during which questionnaire was completed.")
    context_episode_of_care_id = fields.Many2one(
        comodel_name="hc.res.episode.of.care",
        string="Context Episode Of Care",
        help="Episode during which questionnaire was completed.")
    author_type = fields.Selection(
        string="Author Type",
        required="True",
        selection=[
            ("device", "Device"),
            ("practitioner", "Practitioner"),
            ("patient", "Patient"),
            ("related_person", "Related Person")],
        help="Type of person or device who received and recorded the answers.")
    author_name = fields.Char(
        string="Author",
        compute="_compute_author_name",
        store="True",
        help="Person who received and recorded the answers.")
    author_device_id = fields.Many2one(
        comodel_name="hc.res.device",
        string="Author Device",
        help="Device who received and recorded the answers.")
    author_practitioner_id = fields.Many2one(
        comodel_name="hc.res.practitioner",
        string="Author Practitioner",
        help="Practitioner who received and recorded the answers.")
    author_patient_id = fields.Many2one(
        comodel_name="hc.res.patient",
        string="Author Patient",
        help="Patient who received and recorded the answers.")
    author_related_person_id = fields.Many2one(
        comodel_name="hc.res.related.person",
        string="Author Related Person",
        help="Related Person who received and recorded the answers.")
    authored = fields.Datetime(
        string="Authored Date",
        help="Date this version was authored.")
    source_type = fields.Selection(
        string="Source Type",
        selection=[
            ("patient", "Patient"),
            ("practitioner", "Practitioner"),
            ("related_person", "Related Person")],
        help="Type of person who answered the questions.")
    source_name = fields.Char(
        string="Source",
        compute="_compute_source_name",
        store="True",
        help="The person who answered the questions.")
    source_patient_id = fields.Many2one(
        comodel_name="hc.res.patient",
        string="Source Patient",
        help="Patient who answered the questions.")
    source_practitioner_id = fields.Many2one(
        comodel_name="hc.res.practitioner",
        string="Source Practitioner",
        help="Practitioner who answered the questions.")
    source_related_person_id = fields.Many2one(
        comodel_name="hc.res.related.person",
        string="Source Related Person",
        help="Related Person who answered the questions.")
    item_ids = fields.One2many(
        comodel_name="hc.questionnaire.response.item",
        inverse_name="questionnaire_response_id",
        string="Items", help="Groups and questions.")

    @api.model
    def _reference_models(self):
        models = self.env['ir.model'].search([('state', '!=', 'manual')])
        return [(model.model, model.name)
            for model in models
                if model.model.startswith('hc.res')]

    @api.depends('subject_name')
    def _compute_subject_type(self):
        for this in self:
            if this.subject_name:
                this.subject_type = this.subject_name._description

    @api.depends('context_type')
    def _compute_context_name(self):
        for hc_res_questionnaire_response in self:
            if hc_res_questionnaire_response.context_type == 'encounter':
                hc_res_questionnaire_response.context_name = hc_res_questionnaire_response.context_encounter_id.name
            elif hc_res_questionnaire_response.context_type == 'episode_of_care':
                hc_res_questionnaire_response.context_name = hc_res_questionnaire_response.context_episode_of_care_id.name

    @api.depends('author_type')
    def _compute_author_name(self):
        for hc_res_questionnaire_response in self:
            if hc_res_questionnaire_response.author_type == 'device':
                hc_res_questionnaire_response.author_name = hc_res_questionnaire_response.author_device_id.name
            elif hc_res_questionnaire_response.author_type == 'practitioner':
                hc_res_questionnaire_response.author_name = hc_res_questionnaire_response.author_practitioner_id.name
            elif hc_res_questionnaire_response.author_type == 'patient':
                hc_res_questionnaire_response.author_name = hc_res_questionnaire_response.author_patient_id.name
            elif hc_res_questionnaire_response.author_type == 'related_person':
                hc_res_questionnaire_response.author_name = hc_res_questionnaire_response.author_related_person_id.name

    @api.depends('source_type')
    def _compute_source_name(self):
        for hc_res_questionnaire_response in self:
            if hc_res_questionnaire_response.source_type == 'patient':
                hc_res_questionnaire_response.source_name = hc_res_questionnaire_response.source_patient_id.name
            elif hc_res_questionnaire_response.source_type == 'practitioner':
                hc_res_questionnaire_response.source_name = hc_res_questionnaire_response.source_practitioner_id.name
            elif hc_res_questionnaire_response.source_type == 'related_person':
                hc_res_questionnaire_response.source_name = hc_res_questionnaire_response.source_related_person_id.name

class QuestionnaireResponseItem(models.Model):
    _name = "hc.questionnaire.response.item"
    _description = "Questionnaire Response Item"

    questionnaire_response_id = fields.Many2one(
        comodel_name="hc.res.questionnaire.response",
        string="Questionnaire Response",
        help="Questionnaire Response associated with this Questionnaire Response Item.")
    link_id = fields.Char(
        string="Link Id",
        help="Corresponding group within Questionnaire.")
    title = fields.Char(
        string="Title",
        help="Name for group or question text.")
    subject_type = fields.Char(
        string="Subject Type",
        compute="_compute_subject_type",
        store="True",
        help="Type of the subject this group's answers are about.")
    subject_name = fields.Reference(
        string="Subject",
        selection="_reference_models",
        help="The subject this group's answers are about.")
    item_id = fields.Many2one(
        comodel_name="hc.questionnaire.response.item",
        string="Item",
        help="Allows text, questions and other groups to be nested beneath a question or group.")
    answer_ids = fields.One2many(
        comodel_name="hc.questionnaire.response.item.answer",
        inverse_name="item_id",
        string="Answers",
        help="The response(s) to the question.")
    answer_id = fields.Many2one(
        comodel_name="hc.questionnaire.response.item.answer",
        string="Answer",
        help="Answer associated with this Questionnaire Response Item.")

    @api.model
    def _reference_models(self):
        models = self.env['ir.model'].search([('state', '!=', 'manual')])
        return [(model.model, model.name)
            for model in models
                if model.model.startswith('hc.res')]

    @api.depends('subject_name')
    def _compute_subject_type(self):
        for this in self:
            if this.subject_name:
                this.subject_type = this.subject_name._description

class QuestionnaireResponseItemAnswer(models.Model):
    _name = "hc.questionnaire.response.item.answer"
    _description = "Questionnaire Response Item Answer"

    item_id = fields.Many2one(
        comodel_name="hc.questionnaire.response.item",
        string="Item",
        help="Item associated with this Questionnaire Response Item Answer.")
    value_type = fields.Selection(
        string="Value Type",
        selection=[
            ("boolean", "Boolean"),
            ("decimal", "Decimal"),
            ("integer", "Integer"),
            ("date", "Date"),
            ("dateTime", "Datetime"),
            ("instant", "Instant"),
            ("time", "Time"),
            ("string", "String"),
            ("uri", "URL"),
            ("attachment", "Attachment"),
            ("coding", "Coding"),
            ("quantity", "Quantity")],
        help="Type of single-valued answer to the question.")
    value_name = fields.Char(
        string="Value",
        compute="_compute_value_name",
        store="True",
        help="Single-valued answer to the question.")
    value_boolean = fields.Boolean(
        string="Value",
        help="Boolean single-valued answer to the question.")
    value_decimal = fields.Float(
        string="Single Value Answer",
        help="Decimal single-valued answer to the question.")
    value_integer = fields.Integer(
        string="Value Integer",
        help="Integer single-valued answer to the question.")
    value_date = fields.Date(
        string="Value Date",
        help="Date single-valued answer to the question.")
    value_datetime = fields.Datetime(
        string="Value Datetime",
        help="Datetime single-valued answer to the question.")
    value_instant = fields.Datetime(
        string="Value Instant",
        help="Instant single-valued answer to the question.")
    value_time = fields.Float(
        string="Value Time",
        help="Time single-valued answer to the question.")
    value_string = fields.Char(
        string="Value",
        help="String of single-valued answer to the question.")
    value_uri = fields.Char(
        string="Value URL",
        help="URL of answer to the question")
    value_attachment_id = fields.Many2one(
        comodel_name="hc.questionnaire.response.item.answer.value.attachment",
        string="Value Attachment",
        help="Attachment single-valued answer to the question.")
    value_coding_id = fields.Many2one(
        comodel_name="hc.vs.answer.value",
        string="Value Coding",
        help="Coding of single-valued answer to the question.")
    value_quantity = fields.Float(
        string="Value Quantity",
        help="Single-valued answer to the question.")
    value_quantity_uom_id = fields.Many2one(
        comodel_name="product.uom",
        string="Value Quantity UOM",
        help="Value Quantity unit of measure.")
    item_ids = fields.One2many(
        comodel_name="hc.questionnaire.response.item",
        inverse_name="answer_id",
        string="Items",
        help="Groups and questions.")

    @api.depends('value_type')
    def _compute_value_name(self):
        for hc_questionnaire_response_item_answer in self:
            if hc_questionnaire_response_item_answer.value_type == 'boolean':
                hc_questionnaire_response_item_answer.value_name = str(hc_questionnaire_response_item_answer.value_boolean)
            elif hc_questionnaire_response_item_answer.value_type == 'decimal':
                hc_questionnaire_response_item_answer.value_name = str(hc_questionnaire_response_item_answer.value_decimal)
            elif hc_questionnaire_response_item_answer.value_type == 'integer':
                hc_questionnaire_response_item_answer.value_name = str(hc_questionnaire_response_item_answer.value_integer)
            elif hc_questionnaire_response_item_answer.value_type == 'date':
                hc_questionnaire_response_item_answer.value_name = str(hc_questionnaire_response_item_answer.value_date)
            elif hc_questionnaire_response_item_answer.value_type == 'dateTime':
                hc_questionnaire_response_item_answer.value_name = str(hc_questionnaire_response_item_answer.value_datetime)
            elif hc_questionnaire_response_item_answer.value_type == 'instant':
                hc_questionnaire_response_item_answer.value_name = str(hc_questionnaire_response_item_answer.value_instant)
            elif hc_questionnaire_response_item_answer.value_type == 'time':
                hc_questionnaire_response_item_answer.value_name = str(hc_questionnaire_response_item_answer.value_time)
            elif hc_questionnaire_response_item_answer.value_type == 'string':
                hc_questionnaire_response_item_answer.value_name = hc_questionnaire_response_item_answer.value_string
            elif hc_questionnaire_response_item_answer.value_type == 'uri':
                hc_questionnaire_response_item_answer.value_name = hc_questionnaire_response_item_answer.value_uri
            elif hc_questionnaire_response_item_answer.value_type == 'attachment':
                hc_questionnaire_response_item_answer.value_name = hc_questionnaire_response_item_answer.value_attachment_id.name
            elif hc_questionnaire_response_item_answer.value_type == 'coding':
                hc_questionnaire_response_item_answer.value_name = hc_questionnaire_response_item_answer.value_coding_id.name
            elif hc_questionnaire_response_item_answer.value_type == 'quantity':
                hc_questionnaire_response_item_answer.value_name = str(hc_questionnaire_response_item_answer.value_quantity)

class QuestionnaireResponseIdentifier(models.Model):
    _name = "hc.questionnaire.response.identifier"
    _description = "Questionnaire Response Identifier"
    _inherit = ["hc.basic.association", "hc.identifier"]

class QuestionnaireResponseBasedOn(models.Model):
    _name = "hc.questionnaire.response.based.on"
    _description = "Questionnaire Response Based On"
    _inherit = ["hc.basic.association"]

    questionnaire_response_id = fields.Many2one(
        comodel_name="hc.res.questionnaire.response",
        string="Questionnaire Response",
        help="Questionnaire Response associated with this Questionnaire Response Based On.")
    based_on_type = fields.Selection(
        string="Based On Type",
        selection=[
            ("care_plan", "Care Plan"),
            ("procedure_request", "Procedure Request")],
        help="Type of request fulfilled by this Questionnaire.")
    based_on_name = fields.Char(
        string="Based On",
        compute="_compute_based_on_name",
        store="True",
        help="Request fulfilled by this Questionnaire.")
    based_on_care_plan_id = fields.Many2one(
        comodel_name="hc.res.care.plan",
        string="Based On Care Plan",
        help="Care Plan which was fulfilled by this questionnaire.")
    based_on_procedure_request_id = fields.Many2one(
        comodel_name="hc.res.procedure.request",
        string="Based On Procedure Request",
        help="Procedure Request which was fulfilled by this questionnaire.")

    @api.depends('based_on_type')
    def _compute_based_on_name(self):
        for hc_questionnaire_response_based_on in self:
            if hc_questionnaire_response_based_on.based_on_type == 'care_plan':
                hc_questionnaire_response_based_on.based_on_name = hc_questionnaire_response_based_on.based_on_care_plan_id.name
            elif hc_questionnaire_response_based_on.based_on_type == 'procedure_request':
                hc_questionnaire_response_based_on.based_on_name = hc_questionnaire_response_based_on.based_on_procedure_request_id.name

class QuestionnaireResponseParent(models.Model):
    _name = "hc.questionnaire.response.parent"
    _description = "Questionnaire Response Parent"
    _inherit = ["hc.basic.association"]

    questionnaire_response_id = fields.Many2one(
        comodel_name="hc.res.questionnaire.response",
        string="Questionnaire Response",
        help="Questionnaire Response associated with this Questionnaire Response Parent.")
    parent_type = fields.Selection(
        string="Parent Type",
        selection=[
            ("observation", "Observation"),
            ("procedure", "Procedure")],
        help="Type of part of this action.")
    parent_name = fields.Char(
        string="Parent",
        compute="_compute_parent_name",
        store="True",
        help="Part of this action.")
    parent_observation_id = fields.Many2one(
        comodel_name="hc.res.observation",
        string="Parent Observation",
        help="Observation part of this action.")
    parent_procedure_id = fields.Many2one(
        comodel_name="hc.res.procedure",
        string="Parent Procedure",
        help="Procedure part of this action.")

    @api.depends('parent_type')
    def _compute_parent_name(self):
        for hc_questionnaire_response_parent in self:
            if hc_questionnaire_response_parent.parent_type == 'observation':
                hc_questionnaire_response_parent.parent_name = hc_questionnaire_response_parent.parent_observation_id.name
            elif hc_questionnaire_response_parent.parent_type == 'procedure':
                hc_questionnaire_response_parent.parent_name = hc_questionnaire_response_parent.parent_procedure_id.name

class QuestionnaireResponseItemAnswerValueAttachment(models.Model):
    _name = "hc.questionnaire.response.item.answer.value.attachment"
    _description = "Questionnaire Response Item Answer Value Attachment"
    _inherit = ["hc.basic.association", "hc.attachment"]

class AnswerValue(models.Model):
    _name = "hc.vs.answer.value"
    _description = "Answer Value"
    _inherit = ["hc.value.set.contains"]

    name = fields.Char(
        string="Name",
        help="Name of this answer value.")
    code = fields.Char(
        string="Code",
        help="Code of this answer value.")
    contains_id = fields.Many2one(
        comodel_name="hc.vs.answer.value",
        string="Parent",
        help="Parent answer value.")
