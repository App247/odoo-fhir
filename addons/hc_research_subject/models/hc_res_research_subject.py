# -*- coding: utf-8 -*-

from openerp import models, fields, api
from datetime import datetime
from openerp.tools import DEFAULT_SERVER_DATETIME_FORMAT as DTF

class ResearchSubject(models.Model):
    _name = "hc.res.research.subject"
    _description = "Research Subject"
    _inherit = ["hc.domain.resource"]
    _rec_name = "name"

    name = fields.Char(
        string="Name",
        compute="_compute_name",
        store="True",
        help="Text representation of the research subject. Identifier + Individual + Study + Start Date.")
    identifier_id = fields.Many2one(
        comodel_name="hc.research.subject.identifier",
        string="Identifier",
        help="Business Identifier for research subject.")
    status = fields.Selection(
        string="Status",
        required="True",
        selection=[
            ("candidate", "Candidate"),
            ("enrolled", "Enrolled"),
            ("active", "Active"),
            ("suspended", "Suspended"),
            ("withdrawn", "Withdrawn"),
            ("completed", "Completed")],
        help="The current state of the event.")
    status_history_ids = fields.One2many(
        comodel_name="hc.research.subject.status.history",
        inverse_name="research_subject_id",
        string="Status History",
        help="The status of the research subject over time.")
    period_start_date = fields.Datetime(
        string="Period Start Date",
        help="Start of participation.")
    period_end_date = fields.Datetime(
        string="Period End Date",
        help="End of participation.")
    study_id = fields.Many2one(
        comodel_name="hc.res.research.study",
        string="Study",
        required="True",
        help="Study subject is part of.")
    individual_id = fields.Many2one(
        comodel_name="hc.res.patient",
        string="Individual",
        required="True",
        help="Who is part of study.")
    assigned_arm = fields.Char(
        string="Assigned Arm",
        help="What path should be followed.")
    actual_arm = fields.Char(
        string="Actual Arm",
        help="What path was followed.")
    consent_id = fields.Many2one(
        comodel_name="hc.res.consent",
        string="Consent",
        help="Agreement to participate in study.")

    @api.depends('identifier_id', 'individual_id', 'study_id', 'period_start_date')
    def _compute_name(self):
        comp_name = '/'
        for hc_res_research_subject in self:
            if hc_res_research_subject.identifier_id:
                comp_name = hc_res_research_subject.identifier_id.name or ''
            if hc_res_research_subject.individual_id:
                comp_name = comp_name + ", " + hc_res_research_subject.individual_id.name or ''
            if hc_res_research_subject.study_id:
                comp_name = comp_name + ", " + hc_res_research_subject.study_id.name or ''
            if hc_res_research_subject.period_start_date:
                comp_name = comp_name + ", " + datetime.strftime(datetime.strptime(hc_res_research_subject.period_start_date, DTF), "%Y-%m-%d")
            hc_res_research_subject.name = comp_name

    @api.model
    def create(self, vals):
        status_history_obj = self.env['hc.research.subject.status.history']
        res = super(ResearchSubject, self).create(vals)
        if vals and vals.get('status'):
            status_history_vals = {
                'research_subject_id': res.id,
                'status': res.status,
                'start_date': datetime.today()
                }
            status_history_obj.create(status_history_vals)
        return res

    @api.multi
    def write(self, vals):
        status_history_obj = self.env['hc.research.subject.status.history']
        res = super(ResearchSubject, self).write(vals)
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
                    'research_subject_id': self.id,
                    'status': vals.get('status'),
                    'start_date': datetime.today()
                    }
                status_history_obj.create(status_history_vals)
        return res

class ResearchSubjectIdentifier(models.Model):
    _name = "hc.research.subject.identifier"
    _description = "Research Subject Identifier"
    _inherit = ["hc.basic.association", "hc.identifier"]

    research_subject_id = fields.Many2one(
        comodel_name="hc.res.research.subject",
        string="Research Subject",
        help="Research Subject associated with this Research Subject Identifier.")

class ResearchSubjectStatusHistory(models.Model):
    _name = "hc.research.subject.status.history"
    _description = "Research Subject Status History"

    research_subject_id = fields.Many2one(
        comodel_name="hc.res.research.subject",
        string="Research Subject",
        help="Research Subject associated with this Research Subject Status History.")
    status = fields.Char(
        string="Status",
        help="The status of the research subject.")
    start_date = fields.Datetime(
        string="Start Date",
        help="Start of the period during which this research subject status is valid.")
    end_date = fields.Datetime(
        string="End Date",
        help="End of the period during which this research subject status is valid.")
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
