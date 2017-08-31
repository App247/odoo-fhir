# -*- coding: utf-8 -*-

from openerp import models, fields, api

class Task(models.Model):
    _name = "hc.res.task"
    _description = "Task"

    identifier_id = fields.One2many(
        comodel_name="hc.task.identifier",
        inverse_name="task_id",
        string="Identifier",
        help="Task Instance Identifier.")
    definition_type = fields.Selection(
        string="Defintion Type",
        selection=[
            ("uri", "URI"),
            ("activity_definition", "Activity Definition")],
        help="Type of formal definition of task.")
    definition_name = fields.Char(
        string="Definition",
        help="Formal definition of task.")
    definition_uri = fields.Char(
        string="Definition URI",
        help="URI of formal definition of task.")
    definition_activity_definition_id = fields.Many2one(
        comodel_name="hc.res.activity.definition",
        string="Definition Activity Definition",
        help="Activity Definition formal definition of task.")
    based_on_ids = fields.One2many(
        comodel_name="hc.task.based.on",
        inverse_name="task_id",
        string="Based Ons",
        help="Request fulfilled by this request.")
    group_identifier_id = fields.Many2one(
        comodel_name="hc.task.group.identifier",
        string="Group Identifier",
        help="Identifier of requisition or grouper id.")
    part_of_ids = fields.One2many(
        comodel_name="hc.task.part.of",
        inverse_name="task_id",
        string="Part Of",
        help="Identifier of composite task.")
    status = fields.Selection(
        string="Task Status",
        required="True",
        selection=[
            ("draft", "Draft"),
            ("requested", "Requested"),
            ("received", "Received"),
            ("accepted", "Accepted")],
        help="The current status of the task.")
    status_history_ids = fields.One2many(
        comodel_name="hc.task.status.history",
        inverse_name="task_id",
        string="Status History",
        help="The status of the task over time.")
    status_reason_id = fields.Many2one(
        comodel_name="hc.vs.task.status.reason",
        string="Status Reason",
        help="Reason for current status.")
    business_status_id = fields.Many2one(
        comodel_name="hc.vs.task.business.status",
        string="Business Status",
        help='E.g. "Specimen collected", "IV prepped".')
    intent = fields.Selection(
        string="Intent",
        required="True",
        selection=[
            ("proposal", "Proposal"),
            ("plan", "Plan"),
            ("order", "Order")],
        help='Indicates the "level" of actionability associated with the Task. I.e. Is this a proposed task, a planned task, an actionable task, etc.')
    priority = fields.Selection(
        string="Priority",
        selection=[
            ("normal", "Normal"),
            ("urgent", "Urgent"),
            ("asap", "Asap"),
            ("stat", "Stat")],
        help="Indicates how quickly the Task should be addressed with respect to other requests.")
    code_id = fields.Many2one(
        comodel_name="hc.vs.task.type",
        string="Code",
        help="A name or code (or both) briefly describing what the task involves..")
    description = fields.Text(
        string="Description",
        help="Human-readable explanation of task.")
    focus_id = fields.Many2one(
        comodel_name="hc.task.focus",
        string="Focus",
        help="What task is acting on.")
    for_id = fields.Many2one(
        comodel_name="hc.task.for",
        string="For",
        help="Beneficiary of the Task.")
    context_type = fields.Selection(
        string="Context Type",
        selection=[
            ("encounter", "Encounter"),
            ("episode_of_care", "Episode Of Care")],
        help="Type of supplemental instruction.")
    context_name = fields.Char(
        string="Context",
        compute="_compute_context_name",
        store="True",
        help="Healthcare event during which this task originated.")
    context_encounter_id = fields.Many2one(
        comodel_name="hc.res.encounter",
        string="Context Encounter",
        help="Encounter healthcare event during which this task originated.")
    context_episode_of_care_id = fields.Many2one(
        comodel_name="hc.res.episode.of.care",
        string="Context Episode Of Care",
        help="Episode Of Care healthcare event during which this task originated.")
    execution_period_start_date = fields.Datetime(
        string="Execution Period Start Date",
        help="Start of execution.")
    execution_period_end_date = fields.Datetime(
        string="Execution Period End Date",
        help="End of execution.")
    authored_on = fields.Datetime(
        string="Authored On",
        help="Task Creation Date.")
    last_modified = fields.Datetime(
        string="Last Modified",
        required="True",
        help="Task Last Modified Date.")
    performer_type_ids = fields.Many2many(
        comodel_name="hc.vs.task.performer.type",
        string="Performer Types",
        help="The type of participant that can execute the task.")
    owner_type = fields.Selection(
        string="Owner Type",
        selection=[
            ("device", "Device"),
            ("organization", "Organization"),
            ("patient", "Patient"),
            ("practitioner", "Practitioner"),
            ("related_person", "Related Person")],
        help="Type of task owner.")
    owner_name = fields.Char(
        string="Owner",
        compute="_compute_owner_name",
        store="True",
        help="Task Owner.")
    owner_device_id = fields.Many2one(
        comodel_name="hc.res.device",
        string="Owner Device",
        help="Device responsible individual.")
    owner_organization_id = fields.Many2one(
        comodel_name="hc.res.organization",
        string="Owner Organization",
        help="Organization responsible individual.")
    owner_patient_id = fields.Many2one(
        comodel_name="hc.res.patient",
        string="Owner Patient",
        help="Patient responsible individual.")
    owner_practitioner_id = fields.Many2one(
        comodel_name="hc.res.practitioner",
        string="Owner Practitioner",
        help="Practitioner responsible individual.")
    owner_related_person_id = fields.Many2one(
        comodel_name="hc.res.related.person",
        string="Owner Related Person",
        help="Related Person responsible individual.")
    reason_id = fields.Many2one(
        comodel_name="hc.vs.task.reason",
        string="Reason",
        help="Why task is needed.")
    note_ids = fields.One2many(
        comodel_name="hc.task.note",
        inverse_name="task_id",
        string="Notes",
        help="Comments made about the task.")
    relevant_history_ids = fields.One2many(
        comodel_name="hc.task.relevant.history",
        inverse_name="task_id",
        string="Relevant Histories",
        help="Identifier of key events in history of the task.")
    requester_id = fields.Many2one(
        comodel_name="hc.task.requester",
        string="Requester",
        help="Who is asking for task to be done.")
    restriction_id = fields.Many2one(
        comodel_name="hc.task.restriction",
        string="Restriction",
        help="Constraints on fulfillment tasks.")
    input_ids = fields.One2many(
        comodel_name="hc.task.input",
        inverse_name="task_id",
        string="Inputs",
        help="Task Input.")
    output_ids = fields.One2many(
        comodel_name="hc.task.output",
        inverse_name="task_id",
        string="Outputs",
        help="Task Output.")

    @api.model
    def create(self, vals):
        business_status_history_obj = self.env['hc.task.business.status.history']
        status_history_obj = self.env['hc.task.status.history']
        res = super(Condition, self).create(vals)

        # For Status
        if vals and vals.get('status'):
            status_history_vals = {
                'task_id': res.id,
                'status': res.status,
                'start_date': datetime.today()
                }
            if vals.get('status') == 'entered-in-error':
                status_history_vals.update({'end_date': datetime.today()})
            status_history_obj.create(status_history_vals)

        # For Business Status
        if vals.get('status') != 'entered-in-error':
            if vals and vals.get('business_status_id'):
                business_status_history_vals = {
                    'task_id': res.id,
                    'business_status_id': res.business_status_id,
                    'start_date': datetime.today()
                    }
                business_status_history_obj.create(business_status_history_vals)
        return res

    @api.multi
    def write(self, vals):
        business_status_history_obj = self.env['hc.task.business.status.history']
        status_history_obj = self.env['hc.task.status.history']
        res = super(Condition, self).write(vals)

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
                    'task_id': self.id,
                    'status': vals.get('status'),
                    'start_date': datetime.today()
                    }
                if vals.get('status') == 'entered-in-error':
                    status_history_vals.update({'end_date': datetime.today()})
                status_history_obj.create(status_history_vals)

        # For Clinical Status
        business_status_history_record_ids = business_status_history_obj.search([('end_date','=', False)])
        if business_status_history_record_ids:
            if vals.get('status') == 'entered-in-error' or (vals.get('business_status_id') and business_status_history_record_ids[0].business_status_id != vals.get('business_status_id')):
                for business_status_history in business_status_history_record_ids:
                    business_status_history.end_date = datetime.strftime(datetime.today(), DTF)
                    time_diff = datetime.today() - datetime.strptime(business_status_history.start_date, DTF)
                    if time_diff:
                        days = str(time_diff).split(',')
                        if days and len(days) > 1:
                            business_status_history.time_diff_day = str(days[0])
                            times = str(days[1]).split(':')
                            if times and times > 1:
                                business_status_history.time_diff_hour = str(times[0])
                                business_status_history.time_diff_min = str(times[1])
                                business_status_history.time_diff_sec = str(times[2])
                        else:
                            times = str(time_diff).split(':')
                            if times and times > 1:
                                business_status_history.time_diff_hour = str(times[0])
                                business_status_history.time_diff_min = str(times[1])
                                business_status_history.time_diff_sec = str(times[2])
                    business_status_history_vals = {
                        'task_id': self.id,
                        'business_status_id': vals.get('business_status_id'),
                        'start_date': datetime.today()
                        }
                    if vals.get('status') == 'entered-in-error':
                        business_status_history_vals.update({'end_date': datetime.today()})
                    if vals.get('status') != 'entered-in-error':
                        business_status_history_obj.create(business_status_history_vals)
        else:
            business_status_history_vals = {
                    'task_id': self.id,
                    'business_status_id': vals.get('business_status_id'),
                    'start_date': datetime.today()
                    }
            if vals.get('status') == 'entered-in-error':
                    business_status_history_vals.update({'end_date': datetime.today()})
            business_status_history_obj.create(business_status_history_vals)
        return res

class TaskRequester(models.Model):
    _name = "hc.task.requester"
    _description = "Task Requester"

    agent_type = fields.Selection(
        string="Agent Type",
        required="True",
        selection=[
            ("device", "Device"),
            ("organization", "Organization"),
            ("patient", "Patient"),
            ("practitioner", "Practitioner"),
            ("related_person", "Related Person")],
        help="Type of individual asking for task.")
    agent_name = fields.Char(
        string="Agent",
        compute="_compute_agent_name",
        store="True",
        help="Individual asking for task.")
    agent_device_id = fields.Many2one(
        comodel_name="hc.res.device",
        string="Agent Device",
        help="Device individual asking for task.")
    agent_organization_id = fields.Many2one(
        comodel_name="hc.res.organization",
        string="Agent Organization",
        help="Organization individual asking for task.")
    agent_patient_id = fields.Many2one(
        comodel_name="hc.res.patient",
        string="Agent Patient",
        help="Patient individual asking for task.")
    agent_practitioner_id = fields.Many2one(
        comodel_name="hc.res.practitioner",
        string="Agent Practitioner",
        help="Practitioner individual asking for task.")
    agent_related_person_id = fields.Many2one(
        comodel_name="hc.res.related.person",
        string="Agent Related Person",
        help="Related Person individual asking for task.")
    on_behalf_of_id = fields.Many2one(
        comodel_name="hc.res.organization",
        string="On Behalf Of",
        help="Organization individual is acting for.")

class TaskRestriction(models.Model):
    _name = "hc.task.restriction"
    _description = "Task Restriction"

    repetitions = fields.Integer(
        string="Repetitions",
        help="How many times to repeat.")
    period_start_date = fields.Datetime(
        string="Scheduled Start Date",
        help="Start of time period when fulfillment is sought.")
    period_end_date = fields.Datetime(
        string="Scheduled End Date",
        help="End of time period when fulfillment is sought.")
    recipient_ids = fields.One2many(
        comodel_name="hc.task.restriction.recipient",
        inverse_name="restriction_id",
        string="Recipients",
        help="For whom is fulfillment sought?")
    definition = fields.Char(
        string="Definition URI",
        help="URI of task definition.")

class TaskInput(models.Model):
    _name = "hc.task.input"
    _description = "Task Input"

    task_id = fields.Many2one(
        comodel_name="hc.res.task",
        string="Task",
        help="Task associated with this Task Input.")
    name = fields.Char(
        string="Name",
        required="True",
        help="Input Name.")
    value_type = fields.Selection(
        string="Value Type",
        selection=[
            ("integer", "Integer"),
            ("decimal", "Decimal"),
            ("date_time", "Date Time"),
            ("date", "Date"),
            ("instant", "Instant"),
            ("string", "String"),
            ("uri", "URI"),
            ("boolean", "Boolean"),
            ("code", "Code"),
            ("markdown", "Markdown"),
            ("base_64_binary", "Base 64 Binary"),
            ("coding", "Coding"),
            ("codeable_concept", "Codeable Concept"),
            ("attachment", "Attachment"),
            ("identifier", "Identifier"),
            ("quantity", "Quantity"),
            ("range", "Range"),
            ("period", "Period"),
            ("ratio", "Ratio"),
            ("human_name", "Human Name"),
            ("address", "Address"),
            ("contact_point", "Contact Point"),
            ("timing", "Timing"),
            ("signature", "Signature"),
            ("reference", "Reference"),
            ("time", "Time"),
            ("oid", "OID"),
            ("id", "ID"),
            ("unsigned_int", "Unsigned Integer"),
            ("positive_int", "Positive Integer"),
            ("annotation", "Annotation"),
            ("sampled_data", "Sampled Data"),
            ("meta", "Meta")],
        help="Type of specified input value.")
    value_name = fields.Char(
        string="Value",
        compute="_compute_value_name",
        store="True",
        help="Specified input value.")
    value_integer = fields.Integer(
        string="Value Integer",
        help="Integer input value.")
    value_decimal = fields.Float(
        string="Value Decimal",
        help="Decimal input value.")
    value_date_time = fields.Datetime(
        string="Value Date Time",
        help="Date Time input value.")
    value_date = fields.Date(
        string="Value Date",
        help="Date input value.")
    value_instant = fields.Datetime(
        string="Value Instant",
        help="Instant input value.")
    value_string = fields.Char(
        string="Value String",
        help="String input value.")
    value_uri = fields.Char(
        string="Value URI",
        help="URI input value.")
    value_boolean = fields.Boolean(
        string="Value Boolean",
        help="Boolean input value.")
    value_code_id = fields.Many2one(
        comodel_name="hc.vs.task.code",
        string="Value Code",
        help="Code input value.")
    value_markdown = fields.Text(
        string="Value Markdown",
        help="Markdown input value.")
    value_base_64_binary = fields.Binary(
        string="Value Base 64 Binary",
        help="Base 64 Binary input value.")
    value_coding_id = fields.Many2one(
        comodel_name="hc.vs.task.code",
        string="Value Coding",
        help="Coding input value.")
    value_codeable_concept_id = fields.Many2one(
        comodel_name="hc.vs.task.code",
        string="Value Codeable Concept",
        help="Codeable Concept input value.")
    value_attachment_id = fields.Many2one(
        comodel_name="hc.task.attachment",
        string="Value Attachment",
        help="Attachment input value.")
    value_identifier_id = fields.Many2one(
        comodel_name="hc.task.value.identifier",
        string="Value Identifier",
        help="Identifier input value.")
    value_quantity = fields.Float(
        string="Value Quantity",
        help="Quantity input value.")
    value_quantity_uom_id = fields.Many2one(
        comodel_name="product.uom",
        string="Value Quantity UOM",
        help="Quantity unit of measure.")
    value_range = fields.Char(
        string="Value Range",
        help="Range input value.")
    value_period = fields.Char(
        string="Value Period",
        help="Period input value.")
    value_period_uom_id = fields.Many2one(
        comodel_name="product.uom",
        string="Value Period UOM",
        help="Period unit of measure.")
    value_ratio = fields.Float(
        string="Value Ratio",
        help="Ratio of input value.")
    value_human_name_id = fields.Many2one(
        comodel_name="hc.task.human.name",
        string="Value Human Name",
        help="Human Name input value.")
    value_address_id = fields.Many2one(
        comodel_name="hc.task.address",
        string="Value Address",
        help="Address input value.")
    value_contact_point_id = fields.Many2one(
        comodel_name="hc.task.telecom",
        string="Value Contact Point",
        help="Contact Point input value.")
    value_timing_id = fields.Many2one(
        comodel_name="hc.task.timing",
        string="Value Timing",
        help="Timing input value.")
    value_signature_id = fields.Many2one(
        comodel_name="hc.task.signature",
        string="Value Signature",
        help="Signature input value.")
    value_reference_id = fields.Many2one(
        comodel_name="hc.task.reference",
        string="Value Reference",
        help="Reference input value.")
    value_time = fields.Float(
        string="Value Time",
        help="Time input value.")
    value_oid = fields.Char(
        string="Value OID",
        help="OID input value.")
    value_id = fields.Char(
        string="Value ID",
        help="ID input value.")
    value_unsigned_int = fields.Integer(
        string="Value Unsigned Integer",
        help="Unsigned Integer input value.")
    value_positive_int = fields.Integer(
        string="Value Positive Integer",
        help="Positive Integer input value.")
    value_annotation_id = fields.Many2one(
        comodel_name="hc.task.annotation",
        string="Value Annotation",
        help="Annotation input value.")
    value_sampled_data_id = fields.Many2one(
        comodel_name="hc.task.sampled.data",
        string="Value Sampled Data",
        help="Sampled Data input value.")
    value_meta_id = fields.Many2one(
        comodel_name="hc.task.meta",
        string="Value Meta",
        help="Meta input value.")

class TaskOutput(models.Model):
    _name = "hc.task.output"
    _description = "Task Output"

    task_id = fields.Many2one(
        comodel_name="hc.res.task",
        string="Task",
        help="Task associated with this Task Output.")
    name = fields.Char(
        string="Name",
        required="True",
        help="Output Name.")
    value_type = fields.Selection(
        string="Value Type",
        selection=[
            ("integer", "Integer"),
            ("decimal", "Decimal"),
            ("date_time", "Date Time"),
            ("date", "Date"),
            ("instant", "Instant"),
            ("string", "String"),
            ("uri", "URI"),
            ("boolean", "Boolean"),
            ("code", "Code"),
            ("markdown", "Markdown"),
            ("base_64_binary", "Base 64 Binary"),
            ("coding", "Coding"),
            ("codeable_concept", "Codeable Concept"),
            ("attachment", "Attachment"),
            ("identifier", "Identifier"),
            ("quantity", "Quantity"),
            ("range", "Range"),
            ("period", "Period"),
            ("ratio", "Ratio"),
            ("human_name", "Human Name"),
            ("address", "Address"),
            ("contact_point", "Contact Point"),
            ("timing", "Timing"),
            ("signature", "Signature"),
            ("reference", "Reference"),
            ("time", "Time"),
            ("oid", "OID"),
            ("id", "ID"),
            ("unsigned_int", "Unsigned Integer"),
            ("positive_int", "Positive Integer"),
            ("annotation", "Annotation"),
            ("sampled_data", "Sampled Data"),
            ("meta", "Meta")],
        help="Type of specified output value.")
    value_name = fields.Char(
        string="Value",
        compute="_compute_value_name",
        store="True",
        help="Specified output value.")
    value_integer = fields.Integer(
        string="Value Integer",
        help="Integer output value.")
    value_decimal = fields.Float(
        string="Value Decimal",
        help="Decimal output value.")
    value_date_time = fields.Datetime(
        string="Value Date Time",
        help="Date Time output value.")
    value_date = fields.Date(
        string="Value Date",
        help="Date output value.")
    value_instant = fields.Datetime(
        string="Value Instant",
        help="Instant output value.")
    value_string = fields.Char(
        string="Value String",
        help="String output value.")
    value_uri = fields.Char(
        string="Value URI",
        help="URI output value.")
    value_boolean = fields.Boolean(
        string="Value Boolean",
        help="Boolean output value.")
    value_code_id = fields.Many2one(
        comodel_name="hc.vs.task.code",
        string="Value Code",
        help="Code output value.")
    value_markdown = fields.Text(
        string="Value Markdown",
        help="Markdown output value.")
    value_base_64_binary = fields.Binary(
        string="Value Base 64 Binary",
        help="Base 64 Binary output value.")
    value_coding_id = fields.Many2one(
        comodel_name="hc.vs.task.code",
        string="Value Coding",
        help="Coding output value.")
    value_codeable_concept_id = fields.Many2one(
        comodel_name="hc.vs.task.code",
        string="Value Codeable Concept",
        help="Codeable Concept output value.")
    value_attachment_id = fields.Many2one(
        comodel_name="hc.task.attachment",
        string="Value Attachment",
        help="Attachment output value.")
    value_identifier_id = fields.Many2one(
        comodel_name="hc.task.value.identifier",
        string="Value Identifier",
        help="Identifier output value.")
    value_quantity = fields.Float(
        string="Value Quantity",
        help="Quantity output value.")
    value_quantity_uom_id = fields.Many2one(
        comodel_name="product.uom",
        string="Value Quantity UOM",
        help="Quantity unit of measure.")
    value_range = fields.Char(
        string="Value Range",
        help="Range output value.")
    value_period = fields.Char(
        string="Value Period",
        help="Period output value.")
    value_period_uom_id = fields.Many2one(
        comodel_name="product.uom",
        string="Value Period UOM",
        help="Period unit of measure.")
    value_ratio = fields.Float(
        string="Value Ratio",
        help="Ratio of output value.")
    value_human_name_id = fields.Many2one(
        comodel_name="hc.task.human.name",
        string="Value Human Name",
        help="Human Name output value.")
    value_address_id = fields.Many2one(
        comodel_name="hc.task.address",
        string="Value Address",
        help="Address output value.")
    value_contact_point_id = fields.Many2one(
        comodel_name="hc.task.telecom",
        string="Value Contact Point",
        help="Contact Point output value.")
    value_timing_id = fields.Many2one(
        comodel_name="hc.task.timing",
        string="Value Timing",
        help="Timing output value.")
    value_signature_id = fields.Many2one(
        comodel_name="hc.task.signature",
        string="Value Signature",
        help="Signature output value.")
    value_reference_id = fields.Many2one(
        comodel_name="hc.task.reference",
        string="Value Reference",
        help="Reference output value.")
    value_time = fields.Float(
        string="Value Time",
        help="Time output value.")
    value_oid = fields.Char(
        string="Value OID",
        help="OID output value.")
    value_id = fields.Char(
        string="Value ID",
        help="ID output value.")
    value_unsigned_int = fields.Integer(
        string="Value Unsigned Integer",
        help="Unsigned Integer output value.")
    value_positive_int = fields.Integer(
        string="Value Positive Integer",
        help="Positive Integer output value.")
    value_annotation_id = fields.Many2one(
        comodel_name="hc.task.annotation",
        string="Value Annotation",
        help="Annotation output value.")
    value_sampled_data_id = fields.Many2one(
        comodel_name="hc.task.sampled.data",
        string="Value Sampled Data",
        help="Sampled Data output value.")
    value_meta_id = fields.Many2one(
        comodel_name="hc.task.meta",
        string="Value Meta",
        help="Meta output value.")

class TaskIdentifier(models.Model):
    _name = "hc.task.identifier"
    _description = "Task Identifier"
    _inherit = ["hc.basic.association", "hc.identifier"]

    task_id = fields.Many2one(
        comodel_name="hc.res.task",
        string="Task",
        help="Task associated with this Task Identifier.")

class TaskBasedOn(models.Model):
    _name = "hc.task.based.on"
    _description = "Task Based On"
    _inherit = ["hc.basic.association"]

    task_id = fields.Many2one(
        comodel_name="hc.res.task",
        string="Task",
        help="Task associated with this Task Based On.")
    based_on_type = fields.Char(
        string="Based On Type",
        compute="_compute_based_on_type",
        store="True",
        help="Type of request fulfilled by this request.")
    based_on_name = fields.Reference(
        string="Based On",
        selection="_reference_models",
        help="Request fulfilled by this request.")

    @api.model
    def _reference_models(self):
        models = self.env['ir.model'].search([('state', '!=', 'manual')])
        return [(model.model, model.name)
            for model in models
                if model.model.startswith('hc.res')]

    @api.depends('based_on_name')
    def _compute_based_on_type(self):
        for this in self:
            if this.based_on_name:
                this.based_on_type = this.based_on_name._description

class TaskGroupIdentifier(models.Model):
    _name = "hc.task.group.identifier"
    _description = "Task Group Identifier"
    _inherit = ["hc.basic.association", "hc.identifier"]

class TaskPartOf(models.Model):
    _name = "hc.task.part.of"
    _description = "Task Part Of"
    _inherit = ["hc.basic.association"]

    task_id = fields.Many2one(
        comodel_name="hc.res.task",
        string="Task",
        help="Task associated with this Task Parent.")
    part_of_type = fields.Char(
        string="Part Of Type",
        compute="_compute_part_of_type",
        store="True",
        help="Type of composite task.")
    part_of_name = fields.Reference(
        string="Part Of",
        selection="_reference_models",
        help="Composite task.")

    @api.model
    def _reference_models(self):
        models = self.env['ir.model'].search([('state', '!=', 'manual')])
        return [(model.model, model.name)
            for model in models
                if model.model.startswith('hc.res')]

    @api.depends('part_of_name')
    def _compute_part_of_type(self):
        for this in self:
            if this.part_of_name:
                this.part_of_type = this.part_of_name._description

class TaskStatusHistory(models.Model):
    _name = "hc.task.status.history"
    _description = "Task Status History"

    task_id = fields.Many2one(
        comodel_name="hc.res.task",
        string="Task",
        help="Task associated with this Task Status History.")
    status = fields.Char(
        string="Status",
        help="The status of the task.")
    start_date = fields.Datetime(
        string="Start Date",
        help="Start of the period during which this task status is valid.")
    end_date = fields.Datetime(
        string="End Date",
        help="End of the period during which this task status is valid.")
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

class TaskFocus(models.Model):
    _name = "hc.task.focus"
    _description = "Task Focus"
    _inherit = ["hc.basic.association"]

    focus_type = fields.Char(
        string="Focus Type",
        compute="_compute_focus_type",
        store="True",
        help="Type of what task is acting on.")
    focus_name = fields.Reference(
        string="Focus",
        selection="_reference_models",
        help="What task is acting on.")

    @api.model
    def _reference_models(self):
        models = self.env['ir.model'].search([('state', '!=', 'manual')])
        return [(model.model, model.name)
            for model in models
                if model.model.startswith('hc.res')]

    @api.depends('focus_name')
    def _compute_focus_type(self):
        for this in self:
            if this.focus_name:
                this.focus_type = this.focus_name._description

class TaskFor(models.Model):
    _name = "hc.task.for"
    _description = "Task For"
    _inherit = ["hc.basic.association"]

    for_type = fields.Char(
        string="For Type",
        compute="_compute_for_type",
        store="True",
        help="Type of beneficiary of the Task.")
    for_name = fields.Reference(
        string="For",
        selection="_reference_models",
        help="Beneficiary of the Task.")

    @api.model
    def _reference_models(self):
        models = self.env['ir.model'].search([('state', '!=', 'manual')])
        return [(model.model, model.name)
            for model in models
                if model.model.startswith('hc.res')]

    @api.depends('for_name')
    def _compute_for_type(self):
        for this in self:
            if this.for_name:
                this.for_type = this.for_name._description

class TaskNote(models.Model):
    _name = "hc.task.note"
    _description = "Task Note"
    _inherit = ["hc.basic.association", "hc.annotation"]

    task_id = fields.Many2one(
        comodel_name="hc.res.task",
        string="Task",
        help="Task associated with this Task Note.")

class TaskRelevantHistory(models.Model):
    _name = "hc.task.relevant.history"
    _description = "Task Relevant History"
    _inherit = ["hc.basic.association"]

    task_id = fields.Many2one(
        comodel_name="hc.res.task",
        string="Task",
        help="Task associated with this Task Relevant History.")
    relevant_history_id = fields.Many2one(
        comodel_name="hc.res.provenance",
        string="Relevant History",
        help="Provenance associated with this Task Relevant History.")

class TaskRestrictionRecipient(models.Model):
    _name = "hc.task.restriction.recipient"
    _description = "Task Restriction Recipient"
    _inherit = ["hc.basic.association"]

    restriction_id = fields.Many2one(
        comodel_name="hc.task.restriction",
        string="Restriction",
        help="Restriction associated with this Task Restriction Recipient.")
    recipient_type = fields.Selection(
        string="Recipient Type",
        selection=[
            ("patient", "Patient"),
            ("practitioner", "Practitioner"),
            ("related_person", "Related Person"),
            ("group", "Group"),
            ("organization", "Organization")],
        help="Type for whom is fulfillment sought.")
    recipient_name = fields.Char(
        string="Recipient",
        compute="_compute_recipient_name",
        store="True",
        help="For whom is fulfillment sought? ")
    recipient_patient_id = fields.Many2one(
        comodel_name="hc.res.patient",
        string="Recipient Patient",
        help="Patient for whom is fulfillment sought?")
    recipient_practitioner_id = fields.Many2one(
        comodel_name="hc.res.practitioner",
        string="Recipient Practitioner",
        help="Practitioner for whom is fulfillment sought?")
    recipient_related_person_id = fields.Many2one(
        comodel_name="hc.res.related.person",
        string="Recipient Related Person",
        help="Related Person for whom is fulfillment sought?")
    recipient_group_id = fields.Many2one(
        comodel_name="hc.res.group",
        string="Recipient Group",
        help="Group for whom is fulfillment sought?")
    recipient_organization_id = fields.Many2one(
        comodel_name="hc.res.organization",
        string="Recipient Organization",
        help="Organization for whom is fulfillment sought?")

class TaskAddress(models.Model):
    _name = "hc.task.address"
    _description = "Task Address"
    _inherit = ["hc.address.use"]
    _inherits = {"hc.address": "address_id"}

    address_id = fields.Many2one(
        comodel_name="hc.address",
        string="Address",
        ondelete="restrict",
        required="True",
        help="Address associated with this Task Address.")

class TaskAnnotation(models.Model):
    _name = "hc.task.annotation"
    _description = "Task Annotation"
    _inherit = ["hc.basic.association", "hc.annotation"]

class TaskAttachment(models.Model):
    _name = "hc.task.attachment"
    _description = "Task Attachment"
    _inherit = ["hc.basic.association", "hc.attachment"]

class TaskTelecom(models.Model):
    _name = "hc.task.telecom"
    _description = "Task Telecom"
    _inherit = ["hc.contact.point.use"]
    _inherits = {"hc.contact.point": "telecom_id"}

    telecom_id = fields.Many2one(
        comodel_name="hc.contact.point",
        string="Telecom",
        ondelete="restrict",
        required="True",
        help="Telecom associated with this Task Telecom.")

class TaskHumanName(models.Model):
    _name = "hc.task.human.name"
    _description = "Task Human Name"
    _inherit = ["hc.human.name.use"]
    _inherits = {"hc.human.name": "name_id"}

    name_id = fields.Many2one(
        comodel_name="hc.human.name",
        string="Name",
        ondelete="restrict",
        required="True",
        help="Name associated with this Task Human Name.")

class TaskValueIdentifier(models.Model):
    _name = "hc.task.value.identifier"
    _description = "Task Value Identifier"
    _inherit = ["hc.basic.association", "hc.identifier"]

class TaskMeta(models.Model):
    _name = "hc.task.meta"
    _description = "Task Meta"
    _inherit = ["hc.basic.association", "hc.meta"]

class TaskReference(models.Model):
    _name = "hc.task.reference"
    _description = "Task Reference"
    _inherit = ["hc.basic.association", "hc.reference"]

class TaskSampledData(models.Model):
    _name = "hc.task.sampled.data"
    _description = "Task Sampled Data"
    _inherit = ["hc.basic.association", "hc.sampled.data"]

class TaskSignature(models.Model):
    _name = "hc.task.signature"
    _description = "Task Signature"
    _inherit = ["hc.basic.association", "hc.signature"]

class TaskTiming(models.Model):
    _name = "hc.task.timing"
    _description = "Task Timing"
    _inherit = ["hc.basic.association", "hc.timing"]

class TaskCode(models.Model):
    _name = "hc.vs.task.code"
    _description = "Task Code"
    _inherit = ["hc.value.set.contains"]

    name = fields.Char(
        string="Name",
        help="Name of this task code.")
    code = fields.Char(
        string="Code",
        help="Code of this task code.")
    contains_id = fields.Many2one(
        comodel_name="hc.vs.task.code",
        string="Parent",
        help="Parent task code.")

class TaskBusinessStatus(models.Model):
    _name = "hc.vs.task.business.status"
    _description = "Task Business Status"
    _inherit = ["hc.value.set.contains"]

class TaskInputType(models.Model):
    _name = "hc.vs.task.input.type"
    _description = "Task Input Type"
    _inherit = ["hc.value.set.contains"]

class TaskOutputType(models.Model):
    _name = "hc.vs.task.output.type"
    _description = "Task Output Type"
    _inherit = ["hc.value.set.contains"]

class TaskPerformerType(models.Model):
    _name = "hc.vs.task.performer.type"
    _description = "Task Performer Type"
    _inherit = ["hc.value.set.contains"]

class TaskPriority(models.Model):
    _name = "hc.vs.task.priority"
    _description = "Task Priority"
    _inherit = ["hc.value.set.contains"]

class TaskReason(models.Model):
    _name = "hc.vs.task.reason"
    _description = "Task Reason"
    _inherit = ["hc.value.set.contains"]

class TaskStage(models.Model):
    _name = "hc.vs.task.stage"
    _description = "Task Stage"
    _inherit = ["hc.value.set.contains"]

class TaskStatus(models.Model):
    _name = "hc.vs.task.status"
    _description = "Task Status"
    _inherit = ["hc.value.set.contains"]

class TaskStatusReason(models.Model):
    _name = "hc.vs.task.status.reason"
    _description = "Task Status Reason"
    _inherit = ["hc.value.set.contains"]

class TaskType(models.Model):
    _name = "hc.vs.task.type"
    _description = "Task Type"
    _inherit = ["hc.value.set.contains"]
