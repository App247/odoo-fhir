# -*- coding: utf-8 -*-

from openerp import models, fields, api
from datetime import datetime
from openerp.tools import DEFAULT_SERVER_DATE_FORMAT as DF
from openerp.tools import DEFAULT_SERVER_DATETIME_FORMAT as DTF

class Questionnaire(models.Model):    
    _name = "hc.res.questionnaire"    
    _description = "Questionnaire"            

    name = fields.Char(
        string="Event Name", 
        compute="_compute_name", 
        store="True", 
        help="Text representation of the questionnaire. Title + Publisher + Date.")
    url = fields.Char(
        string="URI", 
        help="Globally unique logical identifier for questionnaire.")                    
    identifier_ids = fields.One2many(
        comodel_name="hc.questionnaire.identifier", 
        inverse_name="questionnaire_id", 
        string="Identifiers", 
        help="External Ids for this questionnaire.")                    
    version = fields.Char(
        string="Version", 
        help="Logical id for this version of Questionnaire.")
    status = fields.Selection(
        string="Status", 
        required="True", 
        selection=[
            ("draft", "Draft"), 
            ("published", "Published"), 
            ("retired", "Retired")], 
        help="The lifecycle status of the questionnaire as a whole.")
    date = fields.Datetime(
        string="Date", 
        help="Date this version was authored.")                    
    publisher = fields.Char(
        string="Publisher", 
        help="Organization/individual who designed the questionnaire.")                    
    telecom_ids = fields.One2many(
        comodel_name="hc.questionnaire.telecom", 
        inverse_name="questionnaire_id", 
        string="Telecoms", 
        help="Contact information of the publisher.")                    
    use_context_ids = fields.Many2many(
        comodel_name="hc.vs.use.context", 
        string="Use Contexts", 
        help="Questionnaire intends to support these contexts.")                    
    title = fields.Char(
        string="Title", 
        help="Name for the questionnaire.")                    
    concept_ids = fields.Many2many(
        comodel_name="hc.vs.questionnaire.question", 
        string="Concepts", 
        help="Concept that represents the overall questionnaire.")                    
    subject_type_ids = fields.Many2many(
        comodel_name="hc.vs.resource.type", 
        string="Subject Types", 
        help="Resource that can be subject of QuestionnaireResponse.")                    
    item_ids = fields.One2many(
        comodel_name="hc.questionnaire.item", 
        inverse_name="questionnaire_id", 
        string="Items", 
        help="Questions and sections within the Questionnaire.")                    

    @api.depends('title', 'publisher', 'date')                
    def _compute_name(self):                
        comp_name = '/'            
        for hc_res_questionnaire in self:            
            if hc_res_questionnaire.title:        
                comp_name = hc_res_questionnaire.title  
            if hc_res_questionnaire.publisher:        
                comp_name = comp_name + " " + hc_res_questionnaire.publisher or ''    
            if hc_res_questionnaire.date:        
                title_date = datetime.strftime(datetime.strptime(hc_res_questionnaire.date, DTF), "%Y-%m-%d")    
                comp_name = comp_name + " " + title_date    
            hc_res_questionnaire.name = comp_name        

class QuestionnaireItem(models.Model):    
    _name = "hc.questionnaire.item"    
    _description = "Questionnaire Item"            

    questionnaire_id = fields.Many2one(
        comodel_name="hc.res.questionnaire", 
        string="Questionnaire", 
        help="Questionnaire associated with this Questionnaire Item.")                    
    link_id = fields.Char(
        string="Link ID", 
        help="To link questionnaire with questionnaire answers.")                    
    concept_ids = fields.Many2many(
        comodel_name="hc.vs.questionnaire.question", 
        string="Concepts", 
        help="Concept that represents this section on a questionnaire.")                    
    prefix = fields.Char(
        string="Prefix", 
        help='E.g. "1(a)", "2.5.3".')                    
    text = fields.Char(
        string="Text", 
        help="Primary text for the item.")                    
    type = fields.Selection(
        string="Type", 
        required="True", 
        selection=[
            ("group", "Group"), 
            ("display", "Display"), 
            ("question", "Question"), 
            ("boolean", "Boolean"), 
            ("decimal", "Decimal"), 
            ("integer", "Integer"), 
            ("date", "Date"), 
            ("dateTime +", "Datetime +")], 
        help="Identifies the type of questionnaire item this is - whether text for display, a grouping of other items or a particular type of data to be captured (string, integer, coded choice, etc.).")                    
    required = fields.Boolean(
        string="Required", 
        help="Must group be included in data results?.")                    
    repeats = fields.Boolean(
        string="Repeats", 
        help="Whether the group may repeat.")                    
    read_only = fields.Boolean(
        string="Read Only", 
        help="Don't allow human editing.")                    
    max_length = fields.Integer(
        string="Max Length", 
        help="No more than this many characters.")                    
    options_id = fields.Many2one(
        comodel_name="hc.res.value.set", 
        string="Options", 
        help="Valueset containing permitted answers.")                    
    initial_type = fields.Selection(
        string="Initial Type", 
        selection=[
            ("boolean", "Boolean"), 
            ("decimal", "Decimal"),
            ("integer", "Integer"),
            ("date", "Date"),
            ("dateTime", "Datetime"),
            ("instant", "Instant"),
            ("time", "Time"), 
            ("string", "String"),
            ("uri", "Uri"),
            ("Attachment", "Attachment"),
            ("Coding", "Coding"),
            ("Quantity", "Quantity")], 
        help="Type of value that should be pre-populated when rendering the questionnaire for user input.")                    
    initial_name = fields.Char(
        string="Initial", 
        compute="_compute_initial_name", 
        store="True", 
        help="Initial presumed answer for question.")                    
    initial_boolean = fields.Boolean(
        string="Initial Boolean", 
        help="Boolean initial presumed answer for question.")                    
    initial_decimal = fields.Float(
        string="Initial Decimal", 
        help="Decimal initial presumed answer for question.")                    
    initial_integer = fields.Integer(
        string="Initial Integer", 
        help="Integer initial presumed answer for question.")                    
    initial_date = fields.Date(
        string="Initial Date", 
        help="Date initial presumed answer for question.")                    
    initial_datetime = fields.Datetime(
        string="Initial Datetime", 
        help="Datetime initial presumed answer for question.")                    
    initial_instant = fields.Datetime(
        string="Initial Instant", 
        help="Instant initial presumed answer for question.")                    
    initial_time = fields.Float(
        string="Initial Time", 
        help="Time initial presumed answer for question.")                    
    initial_string = fields.Char(
        string="Initial", 
        help="String of initial presumed answer for question.")                    
    initial_uri = fields.Char(
        string="Initial URL", 
        help="URL of initial presumed answer for question.")                    
    initial_attachment_id = fields.Many2one(
        comodel_name="hc.questionnaire.item.initial.attachment", 
        string="Initial Attachment", 
        help="Attachment initial presumed answer for question.")                    
    initial_coding_id = fields.Many2one(
        comodel_name="hc.questionnaire.item.initial.coding", 
        string="Initial Coding", 
        help="Coding initial presumed answer for question.")                    
    initial_quantity = fields.Float(
        string="Initial Quantity", 
        help="Quantity initial presumed answer for question.")                    
    initial_uom_id = fields.Many2one(
        comodel_name="product.uom", 
        string="Initial UOM", 
        help="Code initial presumed answer for question.")                    
    item_id = fields.Many2one(
        comodel_name="hc.questionnaire.item", 
        string="Item", 
        help="Allows text, questions and other groups to be nested beneath a question or group.")                    
    enable_when_ids = fields.One2many(
        comodel_name="hc.questionnaire.item.enable.when", 
        inverse_name="item_id", 
        string="Enable Whens", 
        help="Only allow data when:")                    
    option_ids = fields.One2many(
        comodel_name="hc.questionnaire.item.option", 
        inverse_name="item_id", 
        string="Options", 
        help="Permitted answer.")                    

class QuestionnaireItemEnableWhen(models.Model):    
    _name = "hc.questionnaire.item.enable.when"    
    _description = "Questionnaire Item Enable When"            

    item_id = fields.Many2one(
        comodel_name="hc.questionnaire.item", 
        string="Item", 
        help="Item associated with this Questionnaire Item Enable When.")                    
    question = fields.Char(
        string="Question", 
        required="True", 
        help="Question that determines whether item is enabled.")                    
    has_answer = fields.Boolean(
        string="Has Answer", 
        help="Enable when answered or not.")                    
    answer_type = fields.Selection(
        string="Answer Type", 
        selection=[
            ("boolean", "Boolean"), 
            ("decimal", "Decimal"),
            ("integer", "Integer"),
            ("date", "Date"),
            ("dateTime", "Datetime"),
            ("instant", "Instant"),
            ("time", "Time"), 
            ("string", "String"),
            ("uri", "Uri"),
            ("Attachment", "Attachment"),
            ("Coding", "Coding"),
            ("Quantity", "Quantity")], 
        help="Type of answer.")                    
    answer_name = fields.Char(
        string="Answer", 
        compute="_compute_answer_name", 
        store="True", 
        help="Value question must have.")                    
    answer_boolean = fields.Boolean(
        string="Answer Boolean", 
        help="Boolean value question must have.")                    
    answer_decimal = fields.Float(
        string="Answer Decimal", 
        help="Decimal value question must have.")                    
    answer_integer = fields.Integer(
        string="Answer Integer", 
        help="Integer value question must have.")                    
    answer_date = fields.Date(
        string="Answer Date", 
        help="Date value question must have.")                    
    answer_datetime = fields.Datetime(
        string="Answer Datetime", 
        help="Datetime value question must have.")                    
    answer_instant = fields.Datetime(
        string="Answer Instant", 
        help="Instant value question must have.")                    
    answer_time = fields.Float(
        string="Answer Time", 
        help="Time value question must have.")                    
    answer_string = fields.Char(
        string="Answer", 
        help="String of value question must have.")                    
    answer_uri = fields.Char(
        string="Answer URL", 
        help="URL value question must have.")                    
    answer_attachment_id = fields.Many2one(
        comodel_name="hc.questionnaire.item.enable.when.answer.attachment", 
        string="Answer Attachment", 
        help="Attachment value question must have.")                    
    answer_coding_id = fields.Many2one(
        comodel_name="hc.questionnaire.item.enable.when.answer.coding", 
        string="Answer Coding", 
        help="Coding value question must have.")                    
    answer = fields.Float(
        string="Answer", 
        help="Quantity value question must have.")                    
    answer_uom_id = fields.Many2one(
        comodel_name="product.uom", 
        string="Answer UOM", 
        help="Code value question must have.")                    

class QuestionnaireItemOption(models.Model):    
    _name = "hc.questionnaire.item.option"    
    _description = "Questionnaire Item Option"            

    item_id = fields.Many2one(
        comodel_name="hc.questionnaire.item", 
        string="Item", 
        help="Item associated with this Questionnaire Item Option.")                    
    value_type = fields.Selection(
        string="Value Type", 
        selection=[
            ("integer", "Integer"), 
            ("date", "Date"), 
            ("time", "Time"), 
            ("string", "String"), 
            ("Coding", "Coding")], 
        help="Type of answer value.")                    
    value_name = fields.Char(
        string="Value", 
        compute="_compute_value_name", 
        store="True", 
        help="Answer value.")                    
    value_integer = fields.Integer(
        string="Value Integer", 
        required="True", 
        help="Identifies a specific answer that's allowed as the answer to a question.")                    
    value_date = fields.Date(
        string="Value Date", 
        help="Date answer value")                    
    value_time = fields.Float(
        string="Value Time", 
        help="Time answer value")                    
    value_string = fields.Char(
        string="Value", 
        help="String of answer value")                    
    value_coding_id = fields.Many2one(
        comodel_name="hc.questionnaire.item.option.value.coding", 
        string="Value Coding", 
        help="Coding answer value")                    

class QuestionnaireIdentifier(models.Model):    
    _name = "hc.questionnaire.identifier"    
    _description = "Questionnaire Identifier"        
    _inherit = ["hc.basic.association", "hc.identifier"]    

    questionnaire_id = fields.Many2one(
        comodel_name="hc.res.questionnaire", 
        string="Questionnaire", 
        help="Questionnaire associated with this Questionnaire Identifier.")                    

class QuestionnaireTelecom(models.Model):    
    _name = "hc.questionnaire.telecom"    
    _description = "Questionnaire Telecom"        
    _inherit = ["hc.contact.point.use"]    
    _inherits = {"hc.contact.point": "telecom_id"}

    telecom_id = fields.Many2one(
        comodel_name="hc.contact.point", 
        string="Telecom", 
        ondelete="restrict", 
        required="True", 
        help="Telecom associated with this Questionnaire Telecom.")                    
    questionnaire_id = fields.Many2one(
        comodel_name="hc.res.questionnaire", 
        string="Questionnaire", 
        help="Questionnaire associated with this Questionnaire Telecom.")                    

class QuestionnaireItemInitialAttachment(models.Model):    
    _name = "hc.questionnaire.item.initial.attachment"    
    _description = "Questionnaire Item Initial Attachment"        
    _inherit = ["hc.basic.association", "hc.attachment"]    

class QuestionnaireItemInitialCoding(models.Model):    
    _name = "hc.questionnaire.item.initial.coding"    
    _description = "Questionnaire Item Initial Coding"    
    _inherit = ["hc.basic.association", "hc.coding"]    

class QuestionnaireItemEnableWhenAnswerAttachment(models.Model):    
    _name = "hc.questionnaire.item.enable.when.answer.attachment"    
    _description = "Questionnaire Item Enable When Answer Attachment"        
    _inherit = ["hc.basic.association", "hc.attachment"]    

class QuestionnaireItemEnableWhenAnswerCoding(models.Model):    
    _name = "hc.questionnaire.item.enable.when.answer.coding"    
    _description = "Questionnaire Item Enable When Answer Coding"        
    _inherit = ["hc.basic.association", "hc.coding"]    

class QuestionnaireItemOptionValueCoding(models.Model):    
    _name = "hc.questionnaire.item.option.value.coding"    
    _description = "Questionnaire Item Option Value Coding"        
    _inherit = ["hc.basic.association", "hc.coding"]    

class QuestionnaireQuestion(models.Model):    
    _name = "hc.vs.questionnaire.question"    
    _description = "Questionnaire Question"        
    _inherit = ["hc.value.set.contains"]    

class UseContext(models.Model):    
    _name = "hc.vs.use.context"    
    _description = "Use Context"        
    _inherit = ["hc.value.set.contains"]    
