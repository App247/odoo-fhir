# -*- coding: utf-8 -*-

from openerp import models, fields, api
from datetime import datetime
from openerp.tools import DEFAULT_SERVER_DATETIME_FORMAT as DTF

class ActivityDefinition(models.Model):
    _name = "hc.res.activity.definition"
    _description = "Activity Definition"

    url = fields.Char(
        string="URI",
        help="Logical URL to reference this asset.")
    identifier_ids = fields.One2many(
        comodel_name="hc.activity.definition.identifier",
        inverse_name="activity_definition_id",
        string="Identifiers",
        help="Logical identifier(s) for the asset.")
    version = fields.Char(
        string="Version",
        help="The version of the asset, if any.")
    name = fields.Char(
        string="Name",
        help="A machine-friendly name for the asset.")
    title = fields.Char(
        string="Title",
        help="A user-friendly title for the asset.")
    status_id = fields.Many2one(
        comodel_name="hc.vs.publication.status",
        string="Status",
        required="True",
        help="The status of this activity definition. Enables tracking the life-cycle of the content.")
    status_history_ids = fields.One2many(
        comodel_name="hc.activity.definition.status.history",
        inverse_name="activity_definition_id",
        string="Status History",
        help="The status of the activity definition over time.")
    is_experimental = fields.Boolean(
        string="Experimental",
        help="If for testing purposes, not real usage.")
    date = fields.Datetime(
        string="Date",
        help="Date this was last changed.")
    publisher = fields.Char(
        string="Publisher",
        help="Name of the publisher (Organization or individual).")
    description = fields.Text(
        string="Description",
        help="Natural language description of the activity definition.")
    purpose = fields.Text(
        string="Purpose",
        help="Why this activity definition is defined.")
    usage = fields.Text(
        string="Usage",
        help="Describes the clinical usage of the asset.")
    approval_date = fields.Date(
        string="Approval Date",
        help="When activity definition approved by publisher.")
    last_review_date = fields.Date(
        string="Last Review Date",
        help="Last review date for the activity definition.")
    effective_period_start_date = fields.Datetime(
        string="Effective Period Start Date",
        help="Start of the effective date range for the asset.")
    effective_period_end_date = fields.Datetime(
        string="Effective Period End Date",
        help="End of the effective date range for the asset.")
    use_context_ids = fields.One2many(
        comodel_name="hc.activity.definition.use.context",
        inverse_name="activity_definition_id",
        string="Use Contexts",
        help="Content intends to support these contexts.")
    jurisdiction_ids = fields.Many2many(
        comodel_name="hc.vs.jurisdiction",
        relation="activity_definition_jurisdiction_rel",
        string="Jurisdictions",
        help="Intended jurisdiction for activity definition (if applicable).")
    topic_ids = fields.Many2many(
        comodel_name="hc.vs.activity.definition.topic",
        relation="activity_definition_topic_rel",
        string="Topics",
        help="Descriptional topics for the asset.")
    contributor_ids = fields.One2many(
        comodel_name="hc.activity.definition.contributor",
        inverse_name="activity_definition_id",
        string="Contributors",
        help="A content contributor.")
    contact_ids = fields.One2many(
        comodel_name="hc.activity.definition.contact",
        inverse_name="activity_definition_id",
        string="Contacts",
        help="Contact details of the publisher.")
    copyright = fields.Text(
        string="Copyright",
        help="Use and/or publishing restrictions.")
    related_artifact_ids = fields.One2many(
        comodel_name="hc.activity.definition.related.artifact",
        inverse_name="activity_definition_id",
        string="Related Artifacts",
        help="Related artifacts for the asset.")
    library_ids = fields.One2many(
        comodel_name="hc.activity.definition.library",
        inverse_name="activity_definition_id",
        string="Libraries",
        help="Logic used by the asset.")
    kind_id = fields.Many2one(
        comodel_name="hc.vs.resource.type",
        string="Kind",
        help="Kind of resource.")
    code_id = fields.Many2one(
        comodel_name="hc.vs.activity.definition.code",
        string="Code", help="Detail type of activity.")
    timing_type = fields.Selection(
        string="Timing Type",
        selection=[
            ("code", "Code"),
            ("timing", "Timing")],
        help="Type of when activity is to occur.")
    timing_name = fields.Char(
        string="Timing",
        compute="_compute_timing_name",
        store="True",
        help="When activity is to occur.")
    timing_code_id = fields.Many2one(
        comodel_name="hc.vs.activity.definition.timing.code",
        string="Timing Code",
        help="Code of when activity is to occur.")
    timing_id = fields.Many2one(
        comodel_name="hc.activity.definition.timing",
        string="Timing",
        help="Timing when activity is to occur.")
    location_id = fields.Many2one(
        comodel_name="hc.res.location",
        string="Location",
        help="Where it should happen.")
    product_type = fields.Selection(
        string="Product Type",
        selection=[
            ("medication", "Medication"),
            ("substance", "Substance"),
            ("code", "Code")],
        help="Type of what's administered/supplied.")
    product_name = fields.Char(
        string="Product",
        compute="_compute_product_name",
        store="True",
        help="What's administered/supplied.")
    product_medication_id = fields.Many2one(
        string="Product Medication",
        comodel_name="hc.res.medication",
        help="Medication administered/supplied.")
    product_substance_id = fields.Many2one(
        comodel_name="hc.res.substance",
        string="Product Substance",
        help="Substance administered/supplied.")
    product_code_id = fields.Many2one(
        comodel_name="hc.vs.activity.definition.product",
        string="Product Code",
        help="Code of what's administered/supplied.")
    quantity = fields.Float(
        string="Quantity",
        help="How much is administered/consumed/supplied")
    quantity_uom_id = fields.Many2one(
        comodel_name="product.uom",
        string="Quantity UOM",
        help="Quantity unit of measure.")
    dosage_ids = fields.One2many(
        comodel_name="hc.activity.definition.dosage",
        inverse_name="activity_definition_id",
        string="Dosages",
        help="Detailed dosage instructions.")
    body_site_ids = fields.Many2many(
        comodel_name="hc.vs.body.site",
        relation="activity_definition_body_site_rel",
        string="Body Sites",
        help="What part of body to perform on.")
    transform_id = fields.Many2one(
        comodel_name="hc.res.structure.map",
        string="Transform",
        help="Transform to apply the template.")
    participant_ids = fields.One2many(
        comodel_name="hc.activity.definition.participant",
        inverse_name="activity_definition_id",
        string="Participants",
        help="Who should participate in the action.")
    dynamic_value_ids = fields.One2many(
        comodel_name="hc.activity.definition.dynamic.value",
        inverse_name="activity_definition_id",
        string="Dynamic Values",
        help="Dynamic aspects of the definition.")

    @api.model
    def create(self, vals):
        status_history_obj = self.env['hc.activity.definition.status.history']
        res = super(ActivityDefinition, self).create(vals)
        if vals and vals.get('status_id'):
            status_history_vals = {
                'activity_definition_id': res.id,
                'status': res.status_id.name,
                'start_date': datetime.today()
                }
            status_history_obj.create(status_history_vals)
        return res

    @api.multi
    def write(self, vals):
        status_history_obj = self.env['hc.activity.definition.status.history']
        publication_status_obj = self.env['hc.vs.publication.status']
        res = super(ActivityDefinition, self).write(vals)
        status_history_record_ids = status_history_obj.search([('end_date','=', False)])
        if status_history_record_ids:
            if vals.get('status_id') and status_history_record_ids[0].status != vals.get('status_id'):
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
                publication_status = publication_status_obj.browse(vals.get('status_id'))
                status_history_vals = {
                    'activity_definition_id': self.id,
                    'status': publication_status.name,
                    'start_date': datetime.today()
                    }
                status_history_obj.create(status_history_vals)
        return res

class ActivityDefinitionParticipant(models.Model):
    _name = "hc.activity.definition.participant"
    _description = "Activity Definition Participant"

    activity_definition_id = fields.Many2one(
        comodel_name="hc.res.activity.definition",
        string="Activity Definition",
        help="Activity Definition associated with this Participant.")
    type = fields.Selection(
        string="Participant Type",
        required="True",
        selection=[
            ("patient", "Patient"),
            ("practitioner", "Practitioner"),
            ("related-person", "Related Person")],
        help="The type of participant in the action.")
    role_id = fields.Many2one(
        comodel_name="hc.vs.action.participant.role",
        string="Role",
        help="E.g. Nurse, Surgeon, Parent, etc.")

class ActivityDefinitionDynamicValue(models.Model):
    _name = "hc.activity.definition.dynamic.value"
    _description = "Activity Definition Dynamic Value"

    activity_definition_id = fields.Many2one(
        comodel_name="hc.res.activity.definition",
        string="Activity Definition",
        help="Activity Definition associated with this Activity Definition Dynamic Value.")
    description = fields.Text(
        string="Description",
        help="Natural language description of the dynamic value.")
    path = fields.Char(
        string="Path",
        help="The path to the element to be set dynamically.")
    language = fields.Char(
        string="Language",
        help="Language of the expression.")
    expression = fields.Char(
        string="Expression",
        help="An expression that provides the dynamic value for the customization.")

class ActivityDefinitionIdentifier(models.Model):
    _name = "hc.activity.definition.identifier"
    _description = "Activity Definition Identifier"
    _inherit = ["hc.basic.association", "hc.identifier"]

    activity_definition_id = fields.Many2one(
        comodel_name="hc.res.activity.definition",
        string="Activity Definition",
        help="Activity Definition associated with this Activity Definition Identifier.")

class ActivityDefinitionStatusHistory(models.Model):
    _name = "hc.activity.definition.status.history"
    _description = "Activity Definition Status History"

    activity_definition_id = fields.Many2one(
        comodel_name="hc.res.activity.definition",
        string="Activity Definition",
        help="Activity Definition associated with this Activity Definition Status History.")
    status = fields.Char(
        string="Status",
        help="The status of the activity definition.")
    start_date = fields.Datetime(
        string="Start Date",
        help="Start of the period during which this activity definition status is valid.")
    end_date = fields.Datetime(
        string="End Date",
        help="End of the period during which this activity definition status is valid.")
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


class ActivityDefinitionUseContext(models.Model):
    _name = "hc.activity.definition.use.context"
    _description = "Activity Definition Use Context"
    _inherit = ["hc.basic.association", "hc.usage.context"]

    activity_definition_id = fields.Many2one(
        comodel_name="hc.res.activity.definition",
        string="Activity Definition",
        help="Activity Definition associated with this Activity Definition Use Context.")

class ActivityDefinitionContact(models.Model):
    _name = "hc.activity.definition.contact"
    _description = "Activity Definition Contact"
    _inherit = ["hc.basic.association"]
    _inherits = {"hc.contact.detail": "contact_id"}

    contact_id = fields.Many2one(
        comodel_name="hc.contact.detail",
        string="Contact",
        ondelete="restrict",
        required="True",
        help="Contact Detail associated with this Activity Definition Contact.")
    activity_definition_id = fields.Many2one(
        comodel_name="hc.res.activity.definition",
        string="Activity Definition",
        help="Activity Definition associated with this Activity Definition Contact.")

class ActivityDefinitionContributor(models.Model):
    _name = "hc.activity.definition.contributor"
    _description = "Activity Definition Contributor"
    _inherit = ["hc.basic.association"]
    _inherits = {"hc.contributor": "contributor_id"}

    contributor_id = fields.Many2one(
        comodel_name="hc.contributor",
        string="Contributor",
        ondelete="restrict",
        required="True",
        help="Contributor associated with this Activity Definition Contributor.")
    activity_definition_id = fields.Many2one(
        comodel_name="hc.res.activity.definition",
        string="Activity Definition",
        help="Activity Definition associated with this Activity Definition Contributor.")

class ActivityDefinitionDosage(models.Model):
    _name = "hc.activity.definition.dosage"
    _description = "Activity Definition Dosage"
    _inherit = ["hc.basic.association", "hc.dosage"]

    activity_definition_id = fields.Many2one(
        comodel_name="hc.res.activity.definition",
        string="Activity Definition",
        help="Activity Definition associated with this Activity Definition Dosage Instruction.")

class ActivityDefinitionLibrary(models.Model):
    _name = "hc.activity.definition.library"
    _description = "Activity Definition Library"
    _inherit = ["hc.basic.association"]

    activity_definition_id = fields.Many2one(
        comodel_name="hc.res.activity.definition",
        string="Activity Definition",
        help="Activity Definition associated with this Activity Definition Library.")
    library_id = fields.Many2one(
        comodel_name="hc.res.library",
        string="Library",
        help="Library associated with this Activity Definition Library.")

class ActivityDefinitionRelatedArtifact(models.Model):
    _name = "hc.activity.definition.related.artifact"
    _description = "Activity Definition Related Artifact"
    _inherit = ["hc.basic.association", "hc.related.artifact"]

    activity_definition_id = fields.Many2one(
        comodel_name="hc.res.activity.definition",
        string="Activity Definition",
        help="Activity Definition associated with this Activity Definition Related Artifact.")

class ActivityDefinitionTiming(models.Model):
    _name = "hc.activity.definition.timing"
    _description = "Activity Definition Timing"
    _inherit = ["hc.basic.association", "hc.timing"]

class ActivityDefinitionCode(models.Model):
    _name = "hc.vs.activity.definition.code"
    _description = "Activity Definition Code"
    _inherit = ["hc.value.set.contains"]

    name = fields.Char(
        string="Name",
        help="Name of this activity definition code.")
    code = fields.Char(
        string="Code",
        help="Code of this activity definition code.")
    contains_id = fields.Many2one(
        comodel_name="hc.vs.activity.definition.code",
        string="Parent",
        help="Parent activity definition code.")

class ActivityDefinitionProduct(models.Model):
    _name = "hc.vs.activity.definition.product"
    _description = "Activity Definition Product"
    _inherit = ["hc.value.set.contains"]

    name = fields.Char(
        string="Name",
        help="Name of this activity definition product.")
    code = fields.Char(
        string="Code",
        help="Code of this activity definition product.")
    contains_id = fields.Many2one(
        comodel_name="hc.vs.activity.definition.product",
        string="Parent",
        help="Parent activity definition product.")

class ActivityDefinitionTopic(models.Model):
    _name = "hc.vs.activity.definition.topic"
    _description = "Activity Definition Topic"
    _inherit = ["hc.value.set.contains"]

    name = fields.Char(
        string="Name",
        help="Name of this activity definition topic.")
    code = fields.Char(
        string="Code",
        help="Code of this activity definition topic.")
    contains_id = fields.Many2one(
        comodel_name="hc.vs.activity.definition.topic",
        string="Parent",
        help="Parent activity definition topic.")

class ActivityDefinitionTimingCode(models.Model):
    _name = "hc.vs.activity.definition.timing.code"
    _description = "Activity Definition Timing Code"
    _inherit = ["hc.value.set.contains"]

    name = fields.Char(
        string="Name",
        help="Name of this activity definition timing code.")
    code = fields.Char(
        string="Code",
        help="Code of this activity definition timing code.")
    contains_id = fields.Many2one(
        comodel_name="hc.vs.activity.definition.timing.code",
        string="Parent",
        help="Parent activity definition timing code.")

