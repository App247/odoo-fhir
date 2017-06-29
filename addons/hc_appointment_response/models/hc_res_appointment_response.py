# -*- coding: utf-8 -*-

from openerp import models, fields, api
from datetime import datetime
from openerp.tools import DEFAULT_SERVER_DATETIME_FORMAT as DTF

class AppointmentResponse(models.Model):
    _name = "hc.res.appointment.response"
    _description = "Appointment Response"
    _rec_name = "appointment_id"

    identifier_ids = fields.One2many(
        comodel_name="hc.appointment.response.identifier",
        inverse_name="appointment_response_id",
        string="Identifiers",
        help="External Ids for this item.")
    appointment_id = fields.Many2one(
        comodel_name="hc.res.appointment",
        string="Appointment",
        required="True",
        help="Parent appointment that this response is replying to.")
    start = fields.Datetime(
        string="Start Date",
        help="Date/Time that the appointment is to take place, or requested new start time.")
    end = fields.Datetime(
        string="End Date",
        help="Date/Time that the appointment is to conclude, or requested new end time.")
    participant_type_ids = fields.Many2many(
        comodel_name="hc.vs.encounter.participant.type",
        relation="appointment_response_participant_type_rel",
        string="Participant Types",
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
    participant_status = fields.Selection(
        string="Participant Status",
        required="True",
        selection=[
            ("accepted", "Accepted"),
            ("declined", "Declined"),
            ("tentative", "Tentative"),
            ("in-process", "In-Process"),
            ("completed", "Completed"),
            ("needs-action", "Needs-Action")],
        help="Participation status of the participant.")
    comment = fields.Text(
        string="Comment",
        help="Additional comments about the appointment.")
    participant_status_history_ids = fields.One2many(
        comodel_name="hc.appointment.response.participant.status.history",
        inverse_name="appointment_response_id",
        string="Participant Status History",
        help="The participant status of the appointment response over time.")

    @api.model
    def create(self, vals):
        participant_status_history_obj = self.env['hc.appointment.response.participant.status.history']
        res = super(AppointmentResponse, self).create(vals)
        if vals and vals.get('participant_status'):
            participant_status_history_vals = {
                'appointment_response_id': res.id,
                'participant_status': res.participant_status,
                'start_date': datetime.today()
                }
            participant_status_history_obj.create(participant_status_history_vals)
        return res

    @api.multi
    def write(self, vals):
        participant_status_history_obj = self.env['hc.appointment.response.participant.status.history']
        res = super(AppointmentResponse, self).write(vals)
        participant_status_history_record_ids = participant_status_history_obj.search([('end_date','=', False)])
        if participant_status_history_record_ids:
            if vals.get('participant_status') and participant_status_history_record_ids[0].participant_status != vals.get('participant_status'):
                for participant_status_history in participant_status_history_record_ids:
                    participant_status_history.end_date = datetime.strftime(datetime.today(), DTF)
                    time_diff = datetime.today() - datetime.strptime(participant_status_history.start_date, DTF)
                    if time_diff:
                        days = str(time_diff).split(',')
                        if days and len(days) > 1:
                            participant_status_history.time_diff_day = str(days[0])
                            times = str(days[1]).split(':')
                            if times and times > 1:
                                participant_status_history.time_diff_hour = str(times[0])
                                participant_status_history.time_diff_min = str(times[1])
                                participant_status_history.time_diff_sec = str(times[2])
                        else:
                            times = str(time_diff).split(':')
                            if times and times > 1:
                                participant_status_history.time_diff_hour = str(times[0])
                                participant_status_history.time_diff_min = str(times[1])
                                participant_status_history.time_diff_sec = str(times[2])
                participant_status_history_vals = {
                    'appointment_response_id': self.id,
                    'participant_status': vals.get('participant_status'),
                    'start_date': datetime.today()
                    }
                participant_status_history_obj.create(participant_status_history_vals)
        return res

    @api.depends('actor_type')
    def _compute_actor_name(self):
        for hc_res_appointment_response in self:
            if hc_res_appointment_response.actor_type == 'patient':
                hc_res_appointment_response.actor_name = hc_res_appointment_response.actor_patient_id.name
            elif hc_res_appointment_response.actor_type == 'practitioner':
                hc_res_appointment_response.actor_name = hc_res_appointment_response.actor_practitioner_id.name
            elif hc_res_appointment_response.actor_type == 'related_person':
                hc_res_appointment_response.actor_name = hc_res_appointment_response.actor_related_person_id.name
            elif hc_res_appointment_response.actor_type == 'device':
                hc_res_appointment_response.actor_name = hc_res_appointment_response.actor_device_id.name
            elif hc_res_appointment_response.actor_type == 'healthcare_service':
                hc_res_appointment_response.actor_name = hc_res_appointment_response.actor_healthcare_service_id.name
            elif hc_res_appointment_response.actor_type == 'location':
                hc_res_appointment_response.actor_name = hc_res_appointment_response.actor_location_id.name

class AppointmentResponseIdentifier(models.Model):
    _name = "hc.appointment.response.identifier"
    _description = "Appointment Response Identifier"
    _inherit = ["hc.basic.association", "hc.identifier"]

    appointment_response_id = fields.Many2one(
        comodel_name="hc.res.appointment.response",
        string="Appointment Response",
        help="Appointment Response associated with this Appointment Response Identifier.")

class AppointmentResponseParticipantStatusHistory(models.Model):
    _name = "hc.appointment.response.participant.status.history"
    _description = "Appointment Response Participant Status History"

    appointment_response_id = fields.Many2one(
        comodel_name="hc.res.appointment.response",
        string="Appointment Response",
        help="Appointment Response associated with this Appointment Response Participant Status History.")
    participant_status = fields.Char(
        string="Participant Status",
        help="The participant status of the appointment response.")
    start_date = fields.Datetime(
        string="Start Date",
        help="Start of the period during which this appointment response participant status is valid.")
    end_date = fields.Datetime(
        string="End Date",
        help="End of the period during which this appointment response participant status is valid.")
    time_diff_day = fields.Char(
        string="Time Diff (days)",
        help="Days duration of the participant status.")
    time_diff_hour = fields.Char(
        string="Time Diff (hours)",
        help="Hours duration of the participant status.")
    time_diff_min = fields.Char(
        string="Time Diff (minutes)",
        help="Minutes duration of the participant status.")
    time_diff_sec = fields.Char(
        string="Time Diff (seconds)",
        help="Seconds duration of the participant status.")