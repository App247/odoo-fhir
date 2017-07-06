# -*- coding: utf-8 -*-

from openerp import models, fields, api
from datetime import datetime
from openerp.tools import DEFAULT_SERVER_DATE_FORMAT as DF
from openerp.tools import DEFAULT_SERVER_DATETIME_FORMAT as DTF

class Procedure(models.Model):
    _name = "hc.res.procedure"
    _description = "Procedure"

    name = fields.Char(
        string="Event Name",
        compute="_compute_name",
        store="True",
        help="Text representation of the procedure event. Subject Name + Procedure + Performed Date/Period.")
    identifier_ids = fields.One2many(
        comodel_name="hc.procedure.identifier",
        inverse_name="procedure_id",
        string="Identifiers",
        help="External Ids for this procedure.")
    definition_ids = fields.One2many(
        comodel_name="hc.procedure.definition",
        inverse_name="procedure_id",
        string="Definitions",
        help="Instantiates protocol or definition.")
    based_on_ids = fields.One2many(
        comodel_name="hc.procedure.based.on",
        inverse_name="procedure_id",
        string="Based Ons",
        help="A request for this procedure.")
    part_of_ids = fields.One2many(
        comodel_name="hc.procedure.part.of",
        inverse_name="procedure_id",
        string="Part Ofs",
        help="Part of referenced event.")
    status = fields.Selection(
        string="Status",
        required="True",
        selection=[
            ("in-progress", "In-Progress"),
            ("aborted", "Aborted"),
            ("completed", "Completed"),
            ("entered-in-error", "Entered-In-Error")],
        default = "in-progress",
        help="State of the procedure.")
    status_history_ids = fields.One2many(
        comodel_name="hc.procedure.status.history",
        inverse_name="procedure_id",
        string="Status History",
        help="The status of the procedure over time.")
    is_not_done = fields.Boolean(
        string="Not Done",
        help="True if procedure was not performed as scheduled.")
    not_done_reason_ids = fields.Many2many(
        comodel_name="hc.vs.procedure.not.performed.reason",
        relation="procedure_not_done_reason_rel",
        string="Reasons Not Performed",
        help="Reason procedure was not performed.")
    category_id = fields.Many2one(
        comodel_name="hc.vs.procedure.category",
        string="Category",
        help="Classification of the procedure.")
    code_id = fields.Many2one(
        comodel_name="hc.vs.procedure.code",
        string="Code",
        required="True",
        help="Identification of the procedure.")
    subject_type = fields.Selection(
        string="Subject Type",
        required="True",
        selection=[
            ("patient", "Patient"),
            ("group", "Group")],
        default = "patient",
        help="Type of subject the procedure was performed on.")
    subject_name = fields.Char(
        string="Subject",
        compute="_compute_subject_name",
        store="True",
        help="Who the procedure was performed on.")
    subject_patient_id = fields.Many2one(
        comodel_name="hc.res.patient",
        string="Subject Patient",
        help="Patient who the procedure was performed on.")
    subject_group_id = fields.Many2one(
        comodel_name="hc.res.group",
        string="Subject Group",
        help="Group who the procedure was performed on.")
    context_type = fields.Selection(
        string="Context Type",
        selection=[
            ("encounter", "Encounter"),
            ("episode_of_care", "Episode Of Care")],
        help="Encounter or episode associated with the procedure.")
    context_name = fields.Char(
        string="Context",
        compute="_compute_context_name",
        store="True",
        help="Encounter or episode associated with the procedure.")
    context_encounter_id = fields.Many2one(
        comodel_name="hc.res.encounter",
        string="Context Encounter",
        help="Encounter associated with this procedure.")
    context_episode_of_care_id = fields.Many2one(
        comodel_name="hc.res.episode.of.care",
        string="Context Episode Of Care",
        help="Episode Of Care associated with this procedure.")
    performed_date_type = fields.Selection(
        string="Performed Date Type",
        selection=[
            ("date_time", "Date Time"),
            ("period", "Period"),
            ("string", "String"),
            ("age", "Age"),
            ("range", "Range")],
        help="Type of when the procedure was performed.")
    performed_date_name = fields.Char(
        string="Performed Date",
        compute="_compute_performed_date_name",
        store="True",
        help="When the procedure was performed.")
    performed_date_date_time = fields.Datetime(
        string="Performed Date Time",
        help="Date when the procedure was performed.")
    performed_date_start_date = fields.Datetime(
        string="Performed Date Start Date",
        help="Start of the when the procedure was performed.")
    performed_date_end_date = fields.Datetime(
        string="Performed End Date",
        help="End of the when the procedure was performed.")
    performed_date_string = fields.Char(
        string="Performed Date String",
        help="String of when the procedure was performed.")
    performed_date_age = fields.Integer(
        string="Performed Date Age",
        size=3,
        help="Age when the procedure was performed.")
    performed_date_age_uom_id = fields.Many2one(
        comodel_name="product.uom",
        string="Performed Date Age UOM",
        domain="[('category_id','=','Time (UCUM)')]",
        default="a",
        help="Performed age unit of measure.")
    performed_date_range_low = fields.Float(
        string="Performed Date Range Low",
        help="Low limit of performed date range.")
    performed_date_range_high = fields.Float(
        string="Performed Date Range High",
        help="High limit of performed date range.")
    performed_date_range_uom_id = fields.Many2one(
        comodel_name="product.uom",
        string="Performed Date Range UOM",
        domain="[('category_id','=','Time (UCUM)')]",
        help="Performed date range unit of measure.")
    location_id = fields.Many2one(
        comodel_name="hc.res.location",
        string="Location",
        help="Where the procedure happened.")
    reason_reference_ids = fields.One2many(
        comodel_name="hc.procedure.reason.reference",
        inverse_name="procedure_id",
        string="Reason References",
        help="Condition that is the reason the procedure performed.")
    reason_code_ids = fields.Many2many(
        comodel_name="hc.vs.procedure.reason",
        relation="procedure_reason_code_rel",
        string="Reason Codes",
        help="Coded reason procedure performed.")
    body_site_ids = fields.Many2many(
        comodel_name="hc.vs.body.site",
        string="Body Sites",
        help="Target body sites.")
    outcome_id = fields.Many2one(
        comodel_name="hc.vs.procedure.outcome",
        string="Outcome",
        help="The result of procedure")
    report_ids = fields.One2many(
        comodel_name="hc.procedure.report",
        inverse_name="procedure_id",
        string="Reports",
        help="Any report resulting from the procedure.")
    complication_ids = fields.Many2many(
        comodel_name="hc.vs.condition.code",
        string="Complications",
        help="Complication following the procedure.")
    complication_detail_ids = fields.One2many(
        comodel_name="hc.procedure.complication.detail",
        inverse_name="procedure_id",
        string="Complication Details",
        help="A condition that_is a result of the procedure.")
    follow_up_ids = fields.Many2many(
        comodel_name="hc.vs.procedure.follow.up",
        string="Follow Ups",
        help="Instructions for follow up.")
    notes_ids = fields.One2many(
        comodel_name="hc.procedure.note",
        inverse_name="procedure_id",
        string="Notes",
        help="Additional information about the procedure.")
    used_reference_ids = fields.One2many(
        comodel_name="hc.procedure.used.reference",
        inverse_name="procedure_id",
        string="Used References",
        help="Device used during procedure.")
    used_code_ids = fields.Many2many(
        comodel_name="hc.vs.procedure.used.code",
        string="Used Codes",
        help="Coded items used during the procedure.")
    performer_ids = fields.One2many(
        comodel_name="hc.procedure.performer",
        inverse_name="procedure_id",
        string="Performers",
        help="The people who performed the procedure.")
    focal_device_ids = fields.One2many(
        comodel_name="hc.procedure.focal.device",
        inverse_name="procedure_id",
        string="Focal Devices",
        help="Device changed in procedure.")

    _sql_constraints = [
        ('performed_date_age_gt_zero',
        'CHECK(performed_date_age >= 0.0)',
        'Age SHALL be a non-negative value.'),

        ('performed_date_range_low_gt_zero',
        'CHECK(performed_date_range_low >= 0.0)',
        'Range Low SHALL be a non-negative value.'),

        ('performed_date_range_high_gt_low',
        'CHECK(performed_date_range_high >= performed_date_range_low)',
        'Range High SHALL not be lower than Range Low.'),

        ('performed_date_period_end_gt_start',
        'CHECK(performed_date_end_date >= performed_date_start_date)',
        'Period End Date SHALL not be before than Period Start Date.')
        ]
    
    @api.depends('performed_date_type')
    def _compute_performed_date_name(self):
        for hc_res_procedure in self:
            if hc_res_procedure.performed_date_type == 'date_time':
                hc_res_procedure.performed_date_name = str(hc_res_procedure.performed_date_date_time)
            elif hc_res_procedure.performed_date_type == 'period':
                hc_res_procedure.performed_date_name = 'Between ' + str(hc_res_procedure.performed_date_start_date) + ' and ' + str(hc_res_procedure.performed_date_end_date)
            elif hc_res_procedure.performed_date_type == 'string':
                hc_res_procedure.performed_date_name = hc_res_procedure.performed_date_string
            elif hc_res_procedure.performed_date_type == 'age':
                hc_res_procedure.performed_date_name = str(hc_res_procedure.performed_date_age) + " " + str(hc_res_procedure.performed_date_age_uom_id.name) + "s old"
            elif hc_res_procedure.performed_date_type == 'range':
                hc_res_procedure.performed_date_name = "Between " + str(hc_res_procedure.performed_date_range_low) + " and " + str(hc_res_procedure.performed_date_range_high) + " " + str(hc_res_procedure.performed_date_range_uom_id.name) + "s ago"

    @api.depends('subject_patient_id', 'subject_group_id', 'code_id', 'performed_date_name')
    def _compute_name(self):
        comp_name = '/'
        for hc_res_procedure in self:
            if hc_res_procedure.subject_type == 'patient':
                comp_name = hc_res_procedure.subject_patient_id.name
                if hc_res_procedure.subject_patient_id.birth_date:
                    subject_patient_birth_date = datetime.strftime(datetime.strptime(hc_res_procedure.subject_patient_id.birth_date, DF), "%Y-%m-%d")
                    comp_name = comp_name + "("+ subject_patient_birth_date + ")"
            if hc_res_procedure.subject_type == 'group':
                comp_name = hc_res_procedure.subject_group_id.name
            if hc_res_procedure.code_id:
                comp_name = comp_name + ", " + hc_res_procedure.code_id.name or ''
            if hc_res_procedure.performed_date_name:
                comp_name = comp_name + ", " + str(hc_res_procedure.performed_date_name) or ''
            hc_res_procedure.name = comp_name

    @api.depends('subject_type')
    def _compute_subject_name(self):
        for hc_res_procedure in self:
            if hc_res_procedure.subject_type == 'patient':
                hc_res_procedure.subject_name = hc_res_procedure.subject_patient_id.name
            elif hc_res_procedure.subject_type == 'group':
                hc_res_procedure.subject_name = hc_res_procedure.subject_group_id.name   

    @api.depends('context_type')
    def _compute_context_name(self):
        for hc_res_procedure in self:
            if hc_res_procedure.context_type == 'encounter':
                hc_res_procedure.context_name = hc_res_procedure.context_encounter_id.name
            elif hc_res_procedure.context_type == 'episode_of_care':
                hc_res_procedure.context_name = hc_res_procedure.context_episode_of_care_id.name

    @api.model
    def create(self, vals):
        status_history_obj = self.env['hc.procedure.status.history']
        res = super(Procedure, self).create(vals)
        if vals and vals.get('status'):
            status_history_vals = {
                'procedure_id': res.id,
                'status': res.status,
                'start_date': datetime.today()
                }
            if vals.get('status') == 'entered-in-error':
                status_history_vals.update({'end_date': datetime.today()})
            status_history_obj.create(status_history_vals)
        return res

    @api.multi                  
    def write(self, vals):                  
        status_history_obj = self.env['hc.procedure.status.history']                
        res = super(Procedure, self).write(vals)               
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
                    'procedure_id': self.id,
                    'status': vals.get('status'),
                    'start_date': datetime.today()
                    }
                if vals.get('status') == 'entered-in-error':
                    status_history_vals.update({'end_date': datetime.today()})
                status_history_obj.create(status_history_vals)    
        return res

class ProcedurePerformer(models.Model):
    _name = "hc.procedure.performer"
    _description = "Procedure Performer"

    procedure_id = fields.Many2one(
        comodel_name="hc.res.procedure",
        string="Procedure",
        help="Procedure associated with this performer.")
    role_id = fields.Many2one(
        comodel_name="hc.vs.performer.role",
        string="Role",
        help="The The role the actor was in.")
    actor_type = fields.Selection(
        string="Actor Type",
        required="True",
        selection=[
            ("practitioner", "Practitioner"),
            ("organization", "Organization"),
            ("patient", "Patient"),
            ("related_person", "Related Person"),
            ("device", "Device")],
        default = "practitioner",
        help="Type of practitioner who was involved in the procedure.")
    actor_name = fields.Char(
        string="Actor",
        compute="_compute_actor_name",
        help="The name of the entity who performs the procedure.")
    actor_practitioner_id = fields.Many2one(
        comodel_name="hc.res.practitioner",
        string="Actor Practitioner",
        help="The practitioner who was involved in the procedure.")
    actor_organization_id = fields.Many2one(
        comodel_name="hc.res.organization",
        string="Actor Organization",
        help="The reference to the organization.")
    actor_patient_id = fields.Many2one(
        comodel_name="hc.res.patient",
        string="Actor Patient",
        help="The reference to the patient.")
    actor_related_person_id = fields.Many2one(
        comodel_name="hc.res.related.person",
        string="Actor Related Person",
        help="The reference to the related person.")
    actor_device_id = fields.Many2one(
        comodel_name="hc.res.device",
        string="Actor Device",
        required="True",
        help="The reference to the device.")
    on_behalf_of_id = fields.Many2one(
        comodel_name="hc.res.organization",
        string="On Behalf Of",
        help="Organization the device or practitioner was acting for.")

    @api.depends('actor_type')
    def _compute_actor_name(self):
        for hc_procedure_performer in self:
            if hc_procedure_performer.actor_type == 'practitioner':
                hc_procedure_performer.actor_name = hc_procedure_performer.actor_practitioner_id.name
            elif hc_procedure_performer.actor_type == 'organization':
                hc_procedure_performer.actor_name = hc_procedure_performer.actor_organization_id.name
            elif hc_procedure_performer.actor_type == 'patient':
                hc_procedure_performer.actor_name = hc_procedure_performer.actor_patient_id.name
            elif hc_procedure_performer.actor_type == 'related_person':
                hc_procedure_performer.actor_name = hc_procedure_performer.actor_related_person_id.name
            elif hc_procedure_performer.actor_type == 'device':
                hc_procedure_performer.actor_name = hc_procedure_performer.actor_device_id.name

class ProcedureFocalDevice(models.Model):
    _name = "hc.procedure.focal.device"
    _description = "Procedure Focal Device"

    procedure_id = fields.Many2one(
        comodel_name="hc.res.procedure",
        string="Procedure",
        help="Procedure associated with this focal device.")
    action_id = fields.Many2one(
        comodel_name="hc.vs.device.action",
        string="Action",
        help="Kind of change to device.")
    manipulated_id = fields.Many2one(
        comodel_name="hc.res.device",
        string="Manipulated",
        required="True",
        help="Device that was changed.")

class ProcedureStatusHistory(models.Model):
    _name = "hc.procedure.status.history"
    _description = "Procedure Status History"

    procedure_id = fields.Many2one(
        comodel_name="hc.res.procedure",
        string="Procedure",
        help="Procedure associated with this Procedure Status History.")
    status = fields.Char(
        string="Status",
        help="The status of the procedure.")
    start_date = fields.Datetime(
        string="Start Date",
        help="Start of the period during which this procedure status is valid.")
    end_date = fields.Datetime(
        string="End Date",
        help="End of the period during which this procedure status is valid.")
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

class ProcedureIdentifier(models.Model):
    _name = "hc.procedure.identifier"
    _description = "Procedure Identifier"
    _inherit = ["hc.basic.association", "hc.identifier"]

    procedure_id = fields.Many2one(
        comodel_name="hc.res.procedure",
        string="Procedure",
        help="Procedure associated with this Procedure Identifier.")

class ProcedureDefinition(models.Model):
    _name = "hc.procedure.definition"
    _description = "Procedure Definition"
    _inherit = ["hc.basic.association"]

    procedure_id = fields.Many2one(
        comodel_name="hc.res.procedure",
        string="Procedure",
        help="Procedure associated with this Procedure Procedure Definition.")
    definition_type = fields.Selection(
        string="Definition Type",
        selection=[
            ("plan_definition", "Plan Definition"),
            ("activity_definition", "Activity Definition"),
            ("healthcare_service", "Healthcare Service")],
        help="Type of instantiates protocol or definition.")
    definition_name = fields.Char(
        string="Definition",
        compute="_compute_definition_name",
        store="True",
        help="Instantiates protocol or definition.")
    definition_plan_definition_id = fields.Many2one(
        comodel_name="hc.res.plan.definition",
        string="Definition Plan Definition",
        help="Plan Definition instantiates protocol or definition.")
    definition_activity_definition_id = fields.Many2one(
        comodel_name="hc.res.activity.definition",
        string="Definition Activity Definition",
        help="Activity Definition instantiates protocol or definition.")
    definition_healthcare_service_id = fields.Many2one(
        comodel_name="hc.res.healthcare.service",
        string="Definition Healthcare Service",
        help="Healthcare Service instantiates protocol or definition.")

class ProcedureBasedOn(models.Model):
    _name = "hc.procedure.based.on"
    _description = "Procedure Based On"
    _inherit = ["hc.basic.association"]

    procedure_id = fields.Many2one(
        comodel_name="hc.res.procedure",
        string="Procedure",
        help="Procedure associated with this Procedure Procedure Based On.")
    based_on_type = fields.Selection(
        string="Based On Type",
        selection=[
            # ("care_plan", "Care Plan"),
            ("procedure_request", "Procedure Request")],
        help="Type of request for this procedure.")
    based_on_name = fields.Char(
        string="Based On",
        compute="_compute_based_on_name",
        store="True",
        help="A request for this procedure.")
    # based_on_care_plan_id = fields.Many2one(
    #     comodel_name="hc.res.care.plan",
    #     string="Based On Care Plan",
    #     help="Care Plan for this procedure.")
    based_on_procedure_request_id = fields.Many2one(
        comodel_name="hc.res.procedure.request",
        string="Based On Procedure Request",
        help="Procedure Request for this procedure.")

class ProcedurePartOf(models.Model):
    _name = "hc.procedure.part.of"
    _description = "Procedure Part Of"
    _inherit = ["hc.basic.association"]

    procedure_id = fields.Many2one(
        comodel_name="hc.res.procedure",
        string="Procedure",
        help="Procedure associated with this Procedure Procedure Part Of.")
    part_of_type = fields.Selection(
        string="Part Of Type",
        selection=[
            ("procedure", "Procedure"),
            ("observation", "Observation"),
            ("medication_administration", "Medication Administration")],
        help="Type of part of referenced event.")
    part_of_name = fields.Char(
        string="Part Of",
        compute="_compute_part_of_name",
        store="True",
        help="Part of referenced event.")
    part_of_procedure_id = fields.Many2one(
        comodel_name="hc.res.procedure",
        string="Part Of Procedure",
        help="Procedure of referenced event.")
    part_of_observation_id = fields.Many2one(
        comodel_name="hc.res.observation",
        string="Part Of Observation",
        help="Observation of referenced event.")
    part_of_medication_administration_id = fields.Many2one(
        comodel_name="hc.res.medication.administration",
        string="Part Of Medication Administration",
        help="Medication Administration of referenced event.")

class ProcedureReasonReference(models.Model):
    _name = "hc.procedure.reason.reference"
    _description = "Procedure Reason Reference"
    _inherit = ["hc.basic.association"]

    procedure_id = fields.Many2one(
        comodel_name="hc.res.procedure",
        string="Procedure",
        help="Procedure associated with this Procedure Reason Reference.")
    reason_reference_id = fields.Many2one(
        comodel_name="hc.res.condition",
        string="Reason Reference",
        help="Condition associated with this Procedure Reason Reference.")

class ProcedureReport(models.Model):
    _name = "hc.procedure.report"
    _description = "Procedure Report"
    _inherit = ["hc.basic.association"]

    procedure_id = fields.Many2one(
        comodel_name="hc.res.procedure",
        string="Procedure",
        help="Procedure associated with this Procedure Report.")
    # report_id = fields.Many2one(
    #     comodel_name="hc.res.diagnostic.report",
    #     string="Report",
    #     help="Diagnostic Report associated with this Procedure Report.")

class ProcedureComplicationDetail(models.Model):
    _name = "hc.procedure.complication.detail"
    _description = "Procedure Complication Detail"
    _inherit = ["hc.basic.association"]

    procedure_id = fields.Many2one(
        comodel_name="hc.res.procedure",
        string="Procedure",
        help="Procedure associated with this Procedure Complication Detail.")
    complication_detail_id = fields.Many2one(
        comodel_name="hc.res.condition",
        string="Complication Detail",
        help="Condition associated with this Procedure Complication Detail.")

class ProcedureNote(models.Model):
    _name = "hc.procedure.note"
    _description = "Procedure Note"
    _inherit = ["hc.basic.association", "hc.annotation"]

    procedure_id = fields.Many2one(
        comodel_name="hc.res.procedure",
        string="Procedure",
        help="Procedure associated with this Procedure Note.")

class ProcedureUsedReference(models.Model):
    _name = "hc.procedure.used.reference"
    _description = "Procedure Used Reference"
    _inherit = ["hc.basic.association"]

    procedure_id = fields.Many2one(
        comodel_name="hc.res.procedure",
        string="Procedure",
        help="Procedure associated with this procedure used reference.")
    used_reference_type = fields.Selection(
        string="Used Reference Type",
        selection=[
            ("device", "Device"),
            ("medication", "Medication"),
            ("substance", "Substance")],
        help="Type of item used during the procedure")
    used_reference_name = fields.Char(
        string="Used Reference",
        compute="_compute_used_reference_name",
        store="True",
        help="The name of the item used during the procedure.")
    used_reference_device_id = fields.Many2one(
        comodel_name="hc.res.device",
        string="Used Reference Device",
        help="Device item used during procedure.")
    used_reference_medication_id = fields.Many2one(
        comodel_name="hc.res.medication",
        string="Used Reference Medication",
        help="Medication item used during procedure.")
    used_reference_substance_id = fields.Many2one(
        comodel_name="hc.res.substance",
        string="Used Reference Substance",
        help="Substance item used during procedure.")

    @api.depends('used_reference_type')
    def _compute_used_reference_name(self):
        for hc_procedure_used_reference in self:
            if hc_procedure_used_reference.used_reference_type == 'device':
                hc_procedure_used_reference.used_reference_name = hc_procedure_used_reference.used_reference_device_id.name
            elif hc_procedure_used_reference.used_reference_type == 'medication':
                hc_procedure_used_reference.used_reference_name = hc_procedure_used_reference.used_reference_medication_id.name
            elif hc_procedure_used_reference.used_reference_type == 'substance':
                hc_procedure_used_reference.used_reference_name = hc_procedure_used_reference.used_reference_substance_id.name

class ProcedureNotPerformedReason(models.Model):
    _name = "hc.vs.procedure.not.performed.reason"
    _description = "Procedure Not Performed Reason"
    _inherit = ["hc.value.set.contains"]

    name = fields.Char(
        string="Name",
        help="Name of this procedure not performed reason.")
    code = fields.Char(
        string="Code",
        help="Code of this procedure not performed reason.")
    contains_id = fields.Many2one(
        comodel_name="hc.vs.procedure.not.performed.reason",
        string="Parent",
        help="Parent procedure not performed reason.")

class ProcedureNotPerformed(models.Model):
    _name = "hc.vs.procedure.not.performed"
    _description = "Procedure Not Performed"
    _inherit = ["hc.value.set.contains"]

    name = fields.Char(
        string="Name",
        help="Name of this procedure not performed.")
    code = fields.Char(
        string="Code",
        help="Code of this procedure not performed.")
    contains_id = fields.Many2one(
        comodel_name="hc.vs.procedure.not.performed",
        string="Parent",
        help="Parent procedure not performed.")

class ParentProcedureNotPerformedReason(models.Model):
    _name = "hc.parent.procedure.not.performed.reason"
    _description = "Parent Procedure Not Performed Reason"
    _inherit = ["hc.basic.association"]
    _inherits = {"hc.vs.procedure.not.performed.reason": "procedure_not_performed_reason_id"}

    procedure_not_performed_reason_id = fields.Many2one(
        comodel_name="hc.vs.procedure.not.performed.reason",
        string="Procedure Not Performed Reason",
        ondelete="restrict",
        required="True",
        help="Procedure Not Performed Reason associated with this Parent Procedure Not Performed Reason.")

class ProcedureNotPerformedReason(models.Model):
    _inherit = "hc.vs.procedure.not.performed.reason"

    contains_ids = fields.One2many(
        comodel_name="hc.parent.procedure.not.performed.reason",
        inverse_name="procedure_not_performed_reason_id",
        string="Parents",
        help="Parent Procedure Not Performed Reason.")

class ProcedureCategory(models.Model):
    _name = "hc.vs.procedure.category"
    _description = "Procedure Category"
    _inherit = ["hc.value.set.contains"]

    name = fields.Char(
        string="Name",
        help="Name of this procedure category.")
    code = fields.Char(
        string="Code",
        help="Code of this procedure category.")
    contains_id = fields.Many2one(
        comodel_name="hc.vs.procedure.category",
        string="Parent",
        help="Parent procedure category.")

class ProcedureOutcome(models.Model):
    _name = "hc.vs.procedure.outcome"
    _description = "Procedure Outcome"
    _inherit = ["hc.value.set.contains"]

    name = fields.Char(
        string="Name",
        help="Name of this procedure outcome.")
    code = fields.Char(
        string="Code",
        help="Code of this procedure outcome.")
    contains_id = fields.Many2one(
        comodel_name="hc.vs.procedure.outcome",
        string="Parent",
        help="Parent procedure outcome.")

class ConditionCode(models.Model):
    _name = "hc.vs.condition.code"
    _description = "Condition Code"
    _inherit = ["hc.value.set.contains"]

    name = fields.Char(
        string="Name",
        help="Name of this condition code.")
    code = fields.Char(
        string="Code",
        help="Code of this condition code.")
    contains_id = fields.Many2one(
        comodel_name="hc.vs.condition.code",
        string="Parent",
        help="Parent condition code.")

class ProcedureFollowUp(models.Model):
    _name = "hc.vs.procedure.follow.up"
    _description = "Procedure Follow Up"
    _inherit = ["hc.value.set.contains"]

    name = fields.Char(
        string="Name",
        help="Name of this procedure follow up.")
    code = fields.Char(
        string="Code",
        help="Code of this procedure follow up.")
    contains_id = fields.Many2one(
        comodel_name="hc.vs.procedure.follow.up",
        string="Parent",
        help="Parent procedure follow up.")

class ProcedureUsedCode(models.Model):
    _name = "hc.vs.procedure.used.code"
    _description = "Procedure Used Code"
    _inherit = ["hc.value.set.contains"]

    name = fields.Char(
        string="Name",
        help="Name of this procedure used code.")
    code = fields.Char(
        string="Code",
        help="Code of this procedure used code.")
    contains_id = fields.Many2one(
        comodel_name="hc.vs.procedure.used.code",
        string="Parent",
        help="Parent procedure used code.")

class PerformerRole(models.Model):
    _name = "hc.vs.performer.role"
    _description = "Performer Role"
    _inherit = ["hc.value.set.contains"]

    name = fields.Char(
        string="Name",
        help="Name of this performer role.")
    code = fields.Char(
        string="Code",
        help="Code of this performer role.")
    contains_id = fields.Many2one(
        comodel_name="hc.vs.performer.role",
        string="Parent",
        help="Parent performer role.")

class DeviceAction(models.Model):
    _name = "hc.vs.device.action"
    _description = "Device Action"
    _inherit = ["hc.value.set.contains"]

    name = fields.Char(
        string="Name",
        help="Name of this device action.")
    code = fields.Char(
        string="Code",
        help="Code of this device action.")
    contains_id = fields.Many2one(
        comodel_name="hc.vs.device.action",
        string="Parent",
        help="Parent device action.")

# External Reference

class EncounterDiagnosis(models.Model):
    _inherit = "hc.encounter.diagnosis"

    condition_type = fields.Selection(
        selection_add=[
            ("procedure", "Procedure")])
    condition_procedure_id = fields.Many2one(
        comodel_name="hc.res.procedure",
        string="Condition Procedure",
        help="Procedure reason the encounter takes place (resource).")

    @api.depends('condition_type')          
    def _compute_condition_name(self):          
        for hc_encounter_diagnosis in self:     
            if hc_encounter_diagnosis.condition_type == 'condition':    
                hc_encounter_diagnosis.condition_name = hc_encounter_diagnosis.condition_condition_id.name
            elif hc_encounter_diagnosis.condition_type == 'procedure':  
                hc_encounter_diagnosis.condition_name = hc_encounter_diagnosis.condition_procedure_id.name    

class AppointmentIndication(models.Model):
    _inherit = "hc.appointment.indication"

    indication_condition_id = fields.Many2one(
        comodel_name="hc.res.condition",
        string="Indication Condition",
        help="Condition reason the appointment is to take place (resource).")
    indication_procedure_id = fields.Many2one(
        comodel_name="hc.res.procedure",
        string="Indication Procedure",
        help="Procedure reason the appointment is to take place (resource).")

    @api.depends('indication_type')
    def _compute_indication_name(self):
        for hc_res_appointment in self:
            if hc_res_appointment.indication_type == 'condition':
                hc_res_appointment.indication_name = hc_res_appointment.indication_condition_id.name
            elif hc_res_appointment.indication_type == 'procedure':
                hc_res_appointment.indication_name = hc_res_appointment.indication_procedure_id.name