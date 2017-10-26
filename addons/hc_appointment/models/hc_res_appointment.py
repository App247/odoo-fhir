# -*- coding: utf-8 -*-

from openerp import models, fields, api
from datetime import datetime
from openerp.tools import DEFAULT_SERVER_DATETIME_FORMAT as DTF

class Appointment(models.Model):
    _name = "hc.res.appointment"
    _description = "Appointment"
    _inherit = ["hc.domain.resource"]
    _rec_name = "description"
    # _rec_name = "actor_name"

    # actor_name = fields.Char(
    #     string="Actor Name",
    #     related="hc_appointment_participant.actor_name",
    #     readonly=True,
    #     help="A Person, Location, Healthcare Service or Device that is participating in the appointment.")
    identifier_ids = fields.One2many(
        comodel_name="hc.appointment.identifier",
        inverse_name="appointment_id",
        string="Identifiers",
        help="External Ids for this item.")
    status = fields.Selection(
        string="Status",
        required="True",
        selection=[
            ("proposed", "Proposed"),
            ("pending", "Pending"),
            ("booked", "Booked"),
            ("arrived", "Arrived"),
            ("fulfilled", "Fulfilled"),
            ("cancelled", "Cancelled"),
            ("noshow", "No Show")],
        default="proposed",
        help="The overall status of the Appointment.")
    status_history_ids = fields.One2many(
        comodel_name="hc.appointment.status.history",
        inverse_name="appointment_id",
        string="Status History",
        help="The status of the appointment over time.")
    service_category_id = fields.Many2one(
        comodel_name="hc.vs.service.category",
        string="Service Category",
        help="A broad categorisation of the service that is to be performed during this appointment.")
    service_type_ids = fields.Many2many(
        comodel_name="hc.vs.service.type",
        relation="appointment_service_type_rel",
        string="Service Types",
        help="The specific service that is to be performed during this appointment.")
    specialty_ids = fields.Many2many(
        comodel_name="hc.vs.c80.practice.code",
        relation="appointment_specialty_rel",
        string="Specialties",
        help="The specialty of a practitioner that would be required to perform the service requested in this appointment.")
    appointment_type_id = fields.Many2one(
        comodel_name="hc.vs.v2.appointment.reason.code",
        string="Type",
        help="The style of appointment or patient that has been booked in the slot (not service type).")
    reason_ids = fields.Many2many(
        comodel_name="hc.vs.encounter.reason",
        relation="appointment_reason_rel",
        string="Reasons",
        help="Reason this appointment is schedule.")
    indication_ids = fields.One2many(
        comodel_name="hc.appointment.indication",
        inverse_name="appointment_id",
        string="Indications",
        help="Reason the appointment is to takes place (resource).")
    priority = fields.Integer(
        string="Priority",
        help="The priority of the appointment. Can be used to make informed decisions if needing to re-prioritize appointments. (The iCal Standard specifies 0 as undefined, 1 as highest, 9 as lowest priority).")
    description = fields.Text(
        string="Description",
        help="The brief description of the appointment as would be shown on a subject line in a meeting request, or appointment list. Detailed or expanded information should be put in the comment field.")
    supporting_information_ids = fields.One2many(
        comodel_name="hc.appointment.supporting.information",
        inverse_name="appointment_id",
        string="Supporting Information",
        help="Additional information to support the appointment.")
    start = fields.Datetime(
        string="Start Date",
        required="True",
        help="Date/Time that the appointment is to take place.")
    end = fields.Datetime(
        string="End Date",
        required="True",
        help="Date/Time that the appointment is to conclude.")
    minutes_duration = fields.Integer(
        string="Minutes Duration",
        help="Can be less than start/end (e.g. estimate).")
    slot_ids = fields.One2many(
        comodel_name="hc.appointment.slot",
        inverse_name="appointment_id",
        string="Slots",
        help="The slot that this appointment is filling. If provided then the schedule will not be provided as slots are not recursive, and the start/end values MUST be the same as from the slot.")
    created = fields.Datetime(
        string="Creation Date",
        help="The date that this appointment was initially created.")
    comment = fields.Text(
        string="Comment",
        help="Additional comments about the appointment.")
    incoming_referral_ids = fields.One2many(
        comodel_name="hc.appointment.incoming.referral",
        inverse_name="appointment_id",
        string="Incoming Referrals",
        help="The slot that this appointment is filling. If provided then the schedule will not be provided as slots are not recursive, and the start/end values MUST be the same as from the slot.")
    requested_period_ids = fields.One2many(
        comodel_name="hc.appointment.requested.period",
        inverse_name="appointment_id",
        string="Requested Periods",
        help="The slot that this appointment is filling. If provided then the schedule will not be provided as slots are not recursive, and the start/end values MUST be the same as from the slot.")
    participant_ids = fields.One2many(
        comodel_name="hc.appointment.participant",
        inverse_name="appointment_id",
        string="Participants",
        required="True",
        help="List of participants involved in the appointment.")

    @api.model
    def create(self, vals):
        status_history_obj = self.env['hc.appointment.status.history']
        res = super(Appointment, self).create(vals)
        if vals and vals.get('status'):
            status_history_vals = {
                'appointment_id': res.id,
                'status' : res.status,
                'start_date': datetime.today()
                }
            status_history_obj.create(status_history_vals)
        return res

    @api.multi
    def write(self, vals):
        status_history_obj = self.env['hc.appointment.status.history']
        res = super(Appointment, self).write(vals)
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
                    'appointment_id': self.id,
                    'status': vals.get('status'),
                    'start_date': datetime.today()
                    }
                status_history_obj.create(status_history_vals)
        return res

class AppointmentParticipant(models.Model):
    _name = "hc.appointment.participant"
    _description = "Appointment Participant"

    appointment_id = fields.Many2one(
        comodel_name="hc.res.appointment",
        string="Appointment",
        help="Appointment associated with this Appointment Participant.")
    type_ids = fields.Many2many(
        comodel_name="hc.vs.encounter.participant.type",
        relation="appointment_participant_type_rel",
        string="Types",
        help="Role of participant in the appointment.")
    actor_type = fields.Selection(
        string="Actor Type",
        selection=[
            ("patient", "Patient"),
            ("practitioner", "Practitioner"),
            ("related_person", "Related Person"),
            ("device", "Device"),
            ("healthcare_service", "Healthcare Service"),
            ("location", "Location")],
        default="patient",
        help="Type of what is account tied to.")
    actor_name = fields.Char(
        string="Actor",
        compute="_compute_actor_name",
        store="True",
        help="A Person, Location, Healthcare Service or Device that is participating in the appointment.")
    actor_patient_id = fields.Many2one(
        comodel_name="hc.res.patient",
        string="Actor Patient",
        help="Patient that is participating in the appointment.")
    actor_practitioner_id = fields.Many2one(
        comodel_name="hc.res.practitioner",
        string="Actor Practitioner",
        help="Practitioner that is participating in the appointment.")
    actor_related_person_id = fields.Many2one(
        comodel_name="hc.res.related.person",
        string="Actor Related Person",
        help="Related Person that is participating in the appointment.")
    actor_device_id = fields.Many2one(
        comodel_name="hc.res.device",
        string="Actor Device",
        help="Device that is participating in the appointment.")
    actor_healthcare_service_id = fields.Many2one(
        comodel_name="hc.res.healthcare.service",
        string="Actor Healthcare Service",
        help="Healthcare Service that is participating in the appointment.")
    actor_location_id = fields.Many2one(
        comodel_name="hc.res.location",
        string="Actor Location",
        help="Location that is participating in the appointment.")
    required = fields.Selection(
        string="Participant Required",
        selection=[
            ("required", "Required"),
            ("optional", "Optional"),
            ("information-only", "Information Only")],
        default="required",
        help="Is this participant required to be present at the meeting.")
    status = fields.Selection(
        string="Participant Status",
        required="True",
        selection=[
            ("accepted", "Accepted"),
            ("declined", "Declined"),
            ("tentative", "Tentative"),
            ("needs-action", "Needs Action")],
        default="tentative",
        help="Participation status of the Patient.")
    status_history_ids = fields.One2many(
        comodel_name="hc.appointment.participant.status.history",
        inverse_name="participant_id",
        string="Status History",
        help="The status of the appointment participant over time.")

    @api.model
    def create(self, vals):
        status_history_obj = self.env['hc.appointment.participant.status.history']
        res = super(AppointmentParticipant, self).create(vals)
        if vals and vals.get('status'):
            status_history_vals = {
                'participant_id': res.id,
                'status' : res.status,
                'start_date': datetime.today()
                }
            status_history_obj.create(status_history_vals)
        return res

    @api.multi
    def write(self, vals):
        status_history_obj = self.env['hc.appointment.participant.status.history']
        res = super(AppointmentParticipant, self).write(vals)
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
                    'participant_id': self.id,
                    'status': vals.get('status'),
                    'start_date': datetime.today()
                    }
                status_history_obj.create(status_history_vals)
        return res

    @api.depends('actor_type')
    def _compute_actor_name(self):
        for hc_appointment_participant in self:
            if hc_appointment_participant.actor_type == 'patient':
                hc_appointment_participant.actor_name = hc_appointment_participant.actor_patient_id.name
            elif hc_appointment_participant.actor_type == 'practitioner':
                hc_appointment_participant.actor_name = hc_appointment_participant.actor_practitioner_id.name
            elif hc_appointment_participant.actor_type == 'related_person':
                hc_appointment_participant.actor_name = hc_appointment_participant.actor_related_person_id.name
            elif hc_appointment_participant.actor_type == 'device':
                hc_appointment_participant.actor_name = hc_appointment_participant.actor_device_id.name
            elif hc_appointment_participant.actor_type == 'healthcare_service':
                hc_appointment_participant.actor_name = hc_appointment_participant.actor_healthcare_service_id.name
            elif hc_appointment_participant.actor_type == 'location':
                hc_appointment_participant.actor_name = hc_appointment_participant.actor_location_id.name

class AppointmentIdentifier(models.Model):
    _name = "hc.appointment.identifier"
    _description = "Appointment Identifier"
    _inherit = ["hc.basic.association", "hc.identifier"]

    appointment_id = fields.Many2one(
        comodel_name="hc.res.appointment",
        string="Appointment",
        help="Appointment associated with this Appointment Identifier.")

class appointmentStatusHistory(models.Model):
    _name = "hc.appointment.status.history"
    _description = "Appointment Status History"

    appointment_id = fields.Many2one(
        comodel_name="hc.res.appointment",
        string="Appointment",
        help="Appointment associated with this Appointment Status History.")
    status = fields.Char(
        string="Status",
        help="The status of the appointment.")
    start_date = fields.Datetime(
        string="Start Date",
        help="Start of the period during which this appointment status is valid.")
    end_date = fields.Datetime(
        string="End Date",
        help="End of the period during which this appointment status is valid.")
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

class AppointmentIndication(models.Model):
    _name = "hc.appointment.indication"
    _description = "Appointment Indication"
    _inherit = ["hc.basic.association"]

    appointment_id = fields.Many2one(
        comodel_name="hc.res.appointment",
        string="Appointment",
        help="Appointment associated with this Appointment Indication.")
    indication_type = fields.Selection(
        string="Indication Type",
        selection=[
            ("condition", "Condition"),
            ("procedure", "Procedure")],
        help="Type of reason the appointment is to take place (resource).")
    indication_name = fields.Char(
        string="Indication",
        compute="_compute_indication_name",
        store="True",
        help="Reason the appointment is to take place (resource).")
    # indication_condition_id = fields.Many2one(
    #     comodel_name="hc.res.condition",
    #     string="Indication Condition",
    #     help="Condition reason the appointment is to take place (resource).")
    # indication_procedure_id = fields.Many2one(
    #     comodel_name="hc.res.procedure",
    #     string="Indication Procedure",
    #     help="Procedure reason the appointment is to take place (resource).")

    # @api.depends('indication_type')
    # def _compute_indication_name(self):
    #     for hc_res_appointment in self:
    #         if hc_res_appointment.indication_type == 'condition':
    #             hc_res_appointment.indication_name = hc_res_appointment.indication_condition_id.name
    #         elif hc_res_appointment.indication_type == 'procedure':
    #             hc_res_appointment.indication_name = hc_res_appointment.indication_procedure_id.name

class AppointmentSupportingInformation(models.Model):
    _name = "hc.appointment.supporting.information"
    _description = "Appointment Supporting Information"
    _inherit = ["hc.basic.association"]

    appointment_id = fields.Many2one(
        comodel_name="hc.res.appointment",
        string="Appointment",
        help="Appointment associated with this Appointment Supporting Information.")
    supporting_information_type = fields.Char(
        string="Supporting Information Type",
        compute="_compute_supporting_information_type",
        store="True",
        help="Type of additional information to support the appointment.")
    supporting_information_name = fields.Reference(
        string="Supporting Information",
        selection="_reference_models",
        help="Additional information to support the appointment.")

    @api.model
    def _reference_models(self):
        models = self.env['ir.model'].search([('state','!=','manual')])
        return [(model.model, model.name)
            for model in models
                if model.model.startswith('hc.res')]

    @api.depends('supporting_information_name')
    def _compute_supporting_information_type(self):
        for this in self:
            if this.supporting_information_name:
                this.supporting_information_type = this.supporting_information_name._description

class AppointmentSlot(models.Model):
    _name = "hc.appointment.slot"
    _description = "Appointment Slot"
    _inherit = ["hc.basic.association"]

    appointment_id = fields.Many2one(
        comodel_name="hc.res.appointment",
        string="Appointment",
        help="Appointment associated with this Appointment Slot.")
    slot_id = fields.Many2one(
        comodel_name="hc.res.slot",
        string="Slot",
        help="The slot that this appointment is filling. If provided then the schedule will not be provided as slots are not recursive, and the start/end values MUST be the same as from the slot")

class AppointmentIncomingReferral(models.Model):
    _name = "hc.appointment.incoming.referral"
    _description = "Appointment Incoming Referral"
    _inherit = ["hc.basic.association"]

    appointment_id = fields.Many2one(
        comodel_name="hc.res.appointment",
        string="Appointment",
        help="Appointment associated with this Appointment Incoming Referral.")
    # incoming_referral_id = fields.Many2one(
    #     comodel_name="hc.res.procedure.request",
    #     string="Incoming Referral",
    #     help="The ProcedureRequest provided as information to allocate to the Encounter.")

class AppointmentRequestedPeriod(models.Model):
    _name = "hc.appointment.requested.period"
    _description = "Appointment Requested Period"
    _inherit = ["hc.basic.association"]

    appointment_id = fields.Many2one(
        comodel_name="hc.res.appointment",
        string="Appointment",
        help="Appointment associated with this Appointment Requested Period.")
    start_date = fields.Datetime(
        string="Start Date",
        help="Start of the potential date/time interval(s) requested to allocate the appointment during.")
    end_date = fields.Datetime(
        string="End Date",
        help="End of the potential date/time interval(s) requested to allocate the appointment during.")

    class AppointmentParticipantStatusHistory(models.Model):
        _name = "hc.appointment.participant.status.history"
        _description = "Appointment Participant Status History"

        participant_id = fields.Many2one(
            comodel_name="hc.appointment.participant",
            string="Appointment Participant",
            help="Appointment Participant associated with this Appointment Participant Status History.")
        status = fields.Char(
            string="Status",
            help="The status of the appointment participant.")
        start_date = fields.Datetime(
            string="Start Date",
            help="Start of the period during which this appointment participant status is valid.")
        end_date = fields.Datetime(
            string="End Date",
            help="End of the period during which this appointment participant status is valid.")
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
