# -*- coding: utf-8 -*-

from openerp import models, fields, api

class Narrative(models.Model):
    _name = "hc.narrative"
    _description = "Narrative"
    _inherit = ["hc.element"]
    _rec_name = "title"

    title = fields.Char(
        string="Title",
        help="Human Readable name/title.")
    status = fields.Selection(
    	string="Narrative Status",
    	required="True",
    	selection=[
    		("generated", "Generated"),
    		("extensions", "Extensions"),
    		("additional", "Additional"),
    		("empty", "Empty")],
    	help="The status of the narrative - whether it's entirely generated (from just the defined data or the extensions too), or whether a human authored it and it may contain additional data.")
    status_history_ids = fields.One2many(
        comodel_name="hc.narrative.status.history",
        inverse_name="narrative_id",
        string="Status History",
        help="The status of the narrative over time.")
    div = fields.Html(
    	string="Div",
    	help="Limited xhtml content.")

    @api.model
    def create(self, vals):
        status_history_obj = self.env['hc.narrative.status.history']
        res = super(narrative, self).create(vals)
        if vals and vals.get('status'):
            status_history_vals = {
                'narrative_id': res.id,
                'status': res.status,
                'start_date': datetime.today()
                }
            status_history_obj.create(status_history_vals)
        return res

    @api.multi
    def write(self, vals):
        status_history_obj = self.env['hc.narrative.status.history']
        res = super(narrative, self).write(vals)
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
                    'narrative_id': self.id,
                    'status': vals.get('status'),
                    'start_date': datetime.today()
                    }
                status_history_obj.create(status_history_vals)
        return res

    class narrativeStatusHistory(models.Model):
        _name = "hc.narrative.status.history"
        _description = "Narrative Status History"

        narrative_id = fields.Many2one(
            comodel_name="hc.narrative",
            string="Narrative",
            help="Narrative associated with this Narrative Status History.")
        status = fields.Char(
            string="Status",
            help="The status of the narrative.")
        start_date = fields.Datetime(
            string="Start Date",
            help="Start of the period during which this narrative status is valid.")
        end_date = fields.Datetime(
            string="End Date",
            help="End of the period during which this narrative status is valid.")
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
