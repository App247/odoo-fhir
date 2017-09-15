# -*- coding: utf-8 -*-

from openerp import models, fields, api

class Account(models.Model):
    _name = "hc.res.account"
    _description = "Account"
    _inherit = ["hc.domain.resource"]
    _inherits = {"account.account": "account_account_id"}
    _rec_name = "name"

    account_account_id = fields.Many2one(
        comodel_name="account.account",
        string="Account",
        required="True",
        ondelete="cascade",
        help="Account associated with this Account.")
    identifier_ids = fields.One2many(
        comodel_name="hc.account.identifier",
        inverse_name="account_id",
        string="Identifiers",
        help="Account number.")
    status = fields.Selection(
        string="Account Status",
        selection=[
            ("active", "Active"),
            ("inactive", "Inactive"),
            ("entered-in-error", "Entered-In-Error")],
        help="Indicates whether the account is presently used/useable or not.")
    status_history_ids = fields.One2many(
        comodel_name="hc.account.status.history",
        inverse_name="account_id",
        string="Status History",
        help="The status of the account over time.")
    # type_id = fields.Many2one(
    #     comodel_name="hc.vs.account.type",
    #     string="Type",
    #     help="E.g. patient, expense, depreciation.")
    # name = fields.Char(
    #     string="Name",
    #     help="Human-readable label.")
    subject_type = fields.Selection(
        string="Subject Type",
        selection=[
            ("patient", "Patient"),
            ("device", "Device"),
            ("practitioner", "Practitioner"),
            ("location", "Location"),
            ("healthcare_service", "Healthcare Service"),
            ("organization", "Organization")],
        help="Type of what is account tied to.")
    subject_name = fields.Char(
        string="Subject",
        compute="_compute_subject_name",
        help="What is account tied to.")
    subject_patient_id = fields.Many2one(
        comodel_name="hc.res.patient",
        string="Subject Patient",
        help="Patient account tied to.")
    subject_device_id = fields.Many2one(
        comodel_name="hc.res.device",
        string="Subject Device",
        help="Device account tied to.")
    subject_practitioner_id = fields.Many2one(
        comodel_name="hc.res.practitioner",
        string="Subject Practitioner",
        help="Practitioner account tied to.")
    subject_location_id = fields.Many2one(
        comodel_name="hc.res.location",
        string="Subject Location",
        help="Location account tied to.")
    subject_healthcare_service_id = fields.Many2one(
        comodel_name="hc.res.healthcare.service",
        string="Subject Healthcare Service",
        help="Healthcare Service account tied to.")
    subject_organization_id = fields.Many2one(
        comodel_name="hc.res.organization",
        string="Subject Organization",
        help="Organization account tied to")
    period_start_date = fields.Datetime(
        string="Coverage Period Start Date",
        help="Start of the transaction window.")
    period_end_date = fields.Datetime(
        string="Coverage Period End Date",
        help="End of the transaction window.")
    active_start_date = fields.Datetime(
        string="Active Start Date",
        help="Start of the time window that transactions may be posted to this account.")
    active_end_date = fields.Datetime(
        string="Active End Date",
        help="End of the time window that transactions may be posted to this account.")
    balance = fields.Float(
        string="Balance",
        help="How much is in account?")
    currency = fields.Many2one(
        comodel_name="res.currency",
        string="Currency",
        help="Base currency in which balance is tracked.")
    coverage_ids = fields.One2many(
        comodel_name="hc.account.coverage",
        inverse_name="account_id",
        string="Coverages",
        help="The party(s) that are responsible for covering the payment of this account.")
    priority = fields.Integer(
        string="Priority",
        help="The priority of the coverage in the context of this account.")
    owner_id = fields.Many2one(
        comodel_name="hc.res.organization",
        string="Owner",
        help="Who is responsible?")
    description = fields.Text(
        string="Description",
        help="Explanation of purpose/use.")
    guarantor_ids = fields.One2many(
        comodel_name="hc.account.guarantor",
        inverse_name="account_id",
        string="Guarantors",
        help="Responsible for the account.")

    @api.depends('subject_type')
    def _compute_subject_name(self):
        for hc_res_account in self:
            if hc_res_account.subject_type == 'patient':
                hc_res_account.subject_name = hc_res_account.subject_patient_id.name
            elif hc_res_account.subject_type == 'device':
                hc_res_account.subject_name = hc_res_account.subject_device_id.name
            elif hc_res_account.subject_type == 'practitioner':
                hc_res_account.subject_name = hc_res_account.subject_practitioner_id.name
            elif hc_res_account.subject_type == 'location':
                hc_res_account.subject_name = hc_res_account.subject_location_id.name
            elif hc_res_account.subject_type == 'healthcare_service':
                hc_res_account.subject_name = hc_res_account.subject_healthcare_service_id.name
            elif hc_res_account.subject_type == 'organization':
                hc_res_account.subject_name = hc_res_account.subject_organization_id.name

    @api.model
    def create(self, vals):
        status_history_obj = self.env['hc.account.status.history']
        res = super(Account, self).create(vals)
        if vals and vals.get('status'):
            status_history_vals = {
                'account_id': res.id,
                'status': res.status,
                'start_date': datetime.today()
                }
            if vals.get('status') == 'entered-in-error':
                status_history_vals.update({'end_date': datetime.today()})
            status_history_obj.create(status_history_vals)
        return res

    @api.multi
    def write(self, vals):
        status_history_obj = self.env['hc.account.status.history']
        res = super(Account, self).write(vals)
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
                    'account_id': self.id,
                    'status': vals.get('status'),
                    'start_date': datetime.today()
                    }
                if vals.get('status') == 'entered-in-error':
                    status_history_vals.update({'end_date': datetime.today()})
                status_history_obj.create(status_history_vals)
        return res

class AccountGuarantor(models.Model):
    _name = "hc.account.guarantor"
    _description = "Account Guarantor"

    account_id = fields.Many2one(
        comodel_name="hc.res.account",
        string="Account",
        help="Account associated with this Account Guarantor.")
    party_type = fields.Selection(
        string="Party Type",
        required="True",
        selection=[
            ("patient", "Patient"),
            ("related_person", "Related Person"),
            ("organization", "Organization")],
        help="Type of what is account tied to.")
    party_name = fields.Char(
        string="Party",
        compute="_compute_party_name",
        store="True", help="Responsible entity.")
    party_patient_id = fields.Many2one(
        comodel_name="hc.res.patient",
        string="Party Patient",
        help="Patient account tied to.")
    party_related_person_id = fields.Many2one(
        comodel_name="hc.res.related.person",
        string="Party Related Person",
        help="Related Person account tied to.")
    party_organization_id = fields.Many2one(
        comodel_name="hc.res.organization",
        string="Party Organization",
        help="Organization account tied to.")
    is_on_hold = fields.Boolean(
        string="On Hold",
        help="Credit or other hold applied.")
    start_date = fields.Datetime(
        string="Start Date",
        help="Start of the guarantee account during.")
    end_date = fields.Datetime(
        string="End Date",
        help="End of the guarantee account during.")

    @api.depends('party_type')
    def _compute_party_name(self):
        for hc_account_guarantor in self:
            if hc_account_guarantor.party_type == 'patient':
                hc_account_guarantor.party_name = hc_account_guarantor.party_patient_id.name
            elif hc_account_guarantor.party_type == 'related_person':
                hc_account_guarantor.party_name = hc_account_guarantor.party_related_person_id.name
            elif hc_account_guarantor.party_type == 'organization':
                hc_account_guarantor.party_name = hc_account_guarantor.party_organization_id.name

class AccountIdentifier(models.Model):
    _name = "hc.account.identifier"
    _description = "Account Identifier"
    _inherit = ["hc.basic.association", "hc.identifier", "hc.identifier.use"]

    account_id = fields.Many2one(
        comodel_name="hc.res.account",
        string="Account",
        help="Account associated with this Account Identifier.")

class AccountCoverage(models.Model):
    _name = "hc.account.coverage"
    _description = "Account Coverage"
    _inherit = ["hc.basic.association"]

    account_id = fields.Many2one(
        comodel_name="hc.res.account",
        string="Account",
        help="Account associated with this Account Coverage.")
    coverage_id = fields.Many2one(
        comodel_name="hc.res.coverage",
        string="Coverage",
        help="Coverage associated with this Account Coverage.")

class AccountStatusHistory(models.Model):
    _name = "hc.account.status.history"
    _description = "Account Status History"

    account_id = fields.Many2one(
        comodel_name="hc.res.account",
        string="Account",
        help="Account associated with this Account Status History.")
    status = fields.Char(
        string="Status",
        help="The status of the account.")
    start_date = fields.Datetime(
        string="Start Date",
        help="Start of the period during which this account status is valid.")
    end_date = fields.Datetime(
        string="End Date",
        help="End of the period during which this account status is valid.")
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

# class AccountType(models.Model):
#     _name = "hc.vs.account.type"
#     _description = "Account Type"
#     _inherit = ["hc.value.set.contains"]

#     name = fields.Char(
#         string="Name",
#         help="Name of this account type.")
#     code = fields.Char(
#         string="Code",
#         help="Code of this account type.")
#     contains_id = fields.Many2one(
#         comodel_name="hc.vs.account.type",
#         string="Parent",
#         help="Parent account type.")

# External reference

class AccountAccountType(models.Model):
    _inherit = "account.account.type"

    type = fields.Selection(
        selection_add=[
            ("patient","Patient")])
