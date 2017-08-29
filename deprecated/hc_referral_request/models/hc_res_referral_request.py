# -*- coding: utf-8 -*-

from openerp import models, fields, api

class ReferralRequest(models.Model):
    _name = "hc.res.referral.request"
    _description = "Referral Request"

    name = fields.Char(
        string="Event Name",
        compute="_compute_name",
        store="True",
        help="Text representation of the referral request event. Patient Name + DOB + Type + Authored Date.")
    identifier_ids = fields.One2many(
        comodel_name="hc.referral.request.identifier",
        inverse_name="referral_request_id",
        string="Identifiers",
        help="Identifier of request.")
    based_on_ids = fields.One2many(
        comodel_name="hc.referral.request.based.on",
        inverse_name="referral_request_id",
        string="Based On",
        help="Request fulfilled by this request.")
    parent_id = fields.Many2one(
        comodel_name="hc.referral.request.parent",
        string="Parent Identifier",
        help="Identifier of composite request this is part of.")
    status = fields.Selection(
        string="Referral Request Status",
        required="True",
        selection=[
            ("draft", "Draft"),
            ("active", "Active"),
            ("cancelled", "Cancelled"),
            ("completed", "Completed"),
            ("entered-in-error", "Entered-In-Error")],
        help="The status of the authorization/intention reflected by the referral request record.")
    category = fields.Selection(
        string="Referral Request Category",
        required="True",
        selection=[
            ("proposal", "Proposal"),
            ("plan", "Plan"),
            ("request", "Request")],
        help='Distinguishes the "level" of authorization/demand implicit in this request.')
    type_id = fields.Many2one(
        comodel_name="hc.vs.referral.type",
        string="Type",
        help="Referral/Transition of care request type.")
    priority_id = fields.Many2one(
        comodel_name="hc.vs.request.priority",
        string="Priority",
        help="Urgency of referral / transfer of care request.")
    # patient_id = fields.Many2one(
    #     comodel_name="hc.res.patient",
    #     string="Patient",
    #     help="Patient patient referred to care or transfer.")
    context_type = fields.Selection(
        string="Context Type",
        selection=[
            ("encounter", "Encounter"),
            ("episode_of_care", "Episode Of Care")],
        help="Type of originating encounter.")
    context_name = fields.Char(
        string="Context",
        compute="_compute_context_name",
        store="True",
        help="Originating encounter.")
    # context_encounter_id = fields.Many2one(
    #     comodel_name="hc.res.encounter",
    #     string="Context Encounter",
    #     help="Encounter urgency of referral / transfer of care request.")
    # context_episode_of_care_id = fields.Many2one(
    #     comodel_name="hc.res.episode.of.care",
    #     string="Context Episode of Care",
    #     help="Episode Of Care patient referred to care or transfer.")
    fulfillment_start_time = fields.Datetime(
        string="Fulfillment Start Time",
        help="Start of the requested service(s) fulfillment time.")
    fulfillment_end_time = fields.Datetime(
        string="Fulfillment End Time",
        help="End of the requested service(s) fulfillment time.")
    authored = fields.Datetime(
        string="Authored",
        help="Date of creation/activation.")
    requester_type = fields.Selection(
        string="Requester Type",
        selection=[
            ("practitioner", "Practitioner"),
            ("organization", "Organization"),
            ("patient", "Patient")],
        help="Type of requester of referral / transfer of care.")
    requester_name = fields.Char(
        string="Requester",
        compute="_compute_requester_name",
        store="True",
        help="Requester of referral / transfer of care.")
    # requester_practitioner_id = fields.Many2one(
    #     comodel_name="hc.res.practitioner",
    #     string="Requester Practitioner",
    #     help="Practitioner requester of referral / transfer of care.")
    # requester_organization_id = fields.Many2one(
    #     comodel_name="hc.res.organization",
    #     string="Requester Organization",
    #     help="Organization requester of referral / transfer of care.")
    # requester_patient_id = fields.Many2one(
    #     comodel_name="hc.res.patient",
    #     string="Requester Patient",
    #     help="Patient requester of referral / transfer of care.")
    specialty_id = fields.Many2one(
        comodel_name="hc.vs.practitioner.specialty",
        string="Specialty",
        help="The clinical specialty (discipline) that the referral is requested for.")
    recipient_ids = fields.One2many(
        comodel_name="hc.referral.request.recipient",
        inverse_name="referral_request_id",
        string="Recipients",
        help="Practitioner receiver of referral / transfer of care request.")
    reason_id = fields.Many2one(
        comodel_name="hc.vs.referral.reason",
        string="Reason",
        help="Reason for referral / Transfer of care request.")
    description = fields.Text(
        string="Description",
        help="A textual description of the referral.")
    service_requested_ids = fields.Many2many(
        comodel_name="hc.vs.c80.practice.code",
        relation="referral_request_service_requested_rel",
        string="Services Requested",
        help="Service(s) requested.")
    supporting_information_ids = fields.One2many(
        comodel_name="hc.referral.request.supporting.information",
        inverse_name="referral_request_id",
        string="Supporting Information",
        help="Additional information to support referral or transfer of care request.")

class ReferralRequestIdentifier(models.Model):
    _name = "hc.referral.request.identifier"
    _description = "Referral Request Identifier"
    _inherit = ["hc.basic.association", "hc.identifier"]

    referral_request_id = fields.Many2one(
        comodel_name="hc.res.referral.request",
        string="Referral Request",
        help="Referral request associated with this Referral Request Identifier.")

class ReferralRequestParent(models.Model):
    _name = "hc.referral.request.parent"
    _description = "Referral Request Parent"
    _inherit = ["hc.basic.association", "hc.identifier"]

class ReferralRequestBasedOn(models.Model):
    _name = "hc.referral.request.based.on"
    _description = "Referral Request Based On"
    _inherit = ["hc.basic.association"]

    referral_request_id = fields.Many2one(
        comodel_name="hc.res.referral.request",
        string="Referral Request",
        help="Referral request associated with this Referral Request Based On.")
    based_on_type = fields.Selection(
        string="Based On Type",
        selection=[
            ("referral_request", "Referral Request"),
            # ("care_plan", "Care Plan"),
            ("diagnostic_request", "Diagnostic Request"),
            ("procedure_request", "Procedure Request")],
        help="Type of request fulfilled by this request.")
    based_on_name = fields.Char(
        string="Based On",
        compute="_compute_based_on_name",
        store="True",
        help="Request fulfilled by this request.")
    based_on_referral_request_id = fields.Many2one(
        comodel_name="hc.res.referral.request",
        string="Based On Referral Request",
        help="Referral Request request fulfilled by this request.")
    # based_on_care_plan_id = fields.Many2one(
    #     comodel_name="hc.res.care.plan",
    #     string="Based On Care Plan",
    #     help="Care Plan request fulfilled by this request.")
    # based_on_diagnostic_request_id = fields.Many2one(
    #     comodel_name="hc.res.diagnostic.request",
    #     string="Based On Diagnostic Request",
    #     help="Diagnostic Request request fulfilled by this request.")
    # based_on_procedure_request_id = fields.Many2one(
    #     comodel_name="hc.res.procedure.request",
    #     string="Based On Procedure Request",
    #     help="Procedure Request request fulfilled by this request.")

class ReferralRequestRecipient(models.Model):
    _name = "hc.referral.request.recipient"
    _description = "Referral Request Recipient"
    _inherit = ["hc.basic.association"]

    referral_request_id = fields.Many2one(
        comodel_name="hc.res.referral.request",
        string="Referral Request",
        help="Referral Request associated with this Referral Request Recipient.")
    recipient_type = fields.Selection(
        string="Recipient Type",
        selection=[
            ("practitioner", "Practitioner"),
            ("organization", "Organization")],
        help="Type of receiver of referral / transfer of care request.")
    recipient_name = fields.Char(
        string="Recipient",
        compute="_compute_recipient_name",
        store="True",
        help="Receiver of referral / transfer of care request.")
    # recipient_practitioner_id = fields.Many2one(
    #     comodel_name="hc.res.practitioner",
    #     string="Recipient Practitioner",
    #     help="Practitioner receiver of referral / transfer of care request.")
    # recipient_organization_id = fields.Many2one(
    #     comodel_name="hc.res.organization",
    #     string="Recipient Organization",
    #     help="Organization receiver of referral / transfer of care request.")

class ReferralRequestSupportingInformation(models.Model):
    _name = "hc.referral.request.supporting.information"
    _description = "Referral Request Supporting Information"
    _inherit = ["hc.basic.association"]

    referral_request_id = fields.Many2one(
        comodel_name="hc.res.referral.request",
        string="Referral Request",
        help="Referral Request associated with this Referral Request Supporting Information.")
    supporting_information_type = fields.Selection(
        string="Supporting Information Type",
        selection=[
            ("string", "String"),
            ("referral_request", "Referral Request")],
        help="Type of additional information to support referral or transfer of care request.")
    supporting_information_name = fields.Char(
        string="Supporting Information",
        compute="_compute_supporting_information_name",
        store="True",
        help="Additional information to support referral or transfer of care request.")
    supporting_information_string = fields.Char(
        string="Supporting Information String",
        help="Specimen additional information to support referral or transfer of care request.")
    supporting_information_code_id = fields.Many2one(
        comodel_name="hc.vs.resource.type",
        string="Supporting Information Code",
        help="Code additional information to support referral or transfer of care request.")

class ReferralReason(models.Model):
    _name = "hc.vs.referral.reason"
    _description = "Referral Reason"
    _inherit = ["hc.value.set.contains"]

class ReferralType(models.Model):
    _name = "hc.vs.referral.type"
    _description = "Referral Type"
    _inherit = ["hc.value.set.contains"]
