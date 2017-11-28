# -*- coding: utf-8 -*-

from openerp import models, fields, api

class AvailableTime(models.Model):
    _name = "hc.available.time"
    _description = "Available Time"

    days_of_week_ids = fields.Many2many(
        comodel_name="hc.vs.days.of.week",
        string="Days Of Week",
        help="The days of the week.")
    is_all_day = fields.Boolean(
        string="All Day",
        help="Always available? (e.g. 24 hour service).")
    available_start_time = fields.Char(
        string="Opening Time",
        help="Opening time of day in hours:min (00:00). Ignored if all Day = true.")
    available_end_time = fields.Char(
        string="Closing Time",
        help="Closing time of day in hours:min (00:00). Ignored if all Day = true.")

    _sql_constraints = [
        ('end_greater_start',
        'CHECK(available_end_time >= available_start_time)',
        'Error ! Closing Time cannot be before Opening Time.')
        ]

class NotAvailableTime(models.Model):
    _name = "hc.not.available.time"
    _description = "Not Available Time"

    description = fields.Text(
        string="Description",
        help="Reason presented to the user explaining why time not available.")
    during_start_date = fields.Datetime(
        string="During Start Date",
        help="Start of period when the service not available.")
    during_end_date = fields.Datetime(
        string="During End Date",
        help="End of period when the service not available.")

    _sql_constraints = [
        ('end_greater_start',
        'CHECK(during_end_date >= during_start_date)',
        'Error ! End Date cannot be before Start Date.')
        ]
