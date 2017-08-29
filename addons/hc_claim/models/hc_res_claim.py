# -*- coding: utf-8 -*-

from openerp import models, fields, api
from datetime import datetime
from openerp.tools import DEFAULT_SERVER_DATETIME_FORMAT as DTF

class Claim(models.Model):
    _name = "hc.res.claim"
    _description = "Claim"

    identifier_ids = fields.One2many(
        comodel_name="hc.claim.identifier",
        inverse_name="claim_id",
        string="Identifiers",
        help="Claim number.")
    status_id = fields.Many2one(
        comodel_name="hc.vs.fm.status",
        string="Status",
        help="The status of the resource instance.")
    status_history_ids = fields.One2many(
        comodel_name="hc.claim.status.history",
        inverse_name="claim_id",
        string="Status History",
        help="The status of the claim over time.")
    type = fields.Selection(
        string="Type",
        required="True",
        selection=[
            ("institutional", "Institutional"),
            ("oral", "Oral"),
            ("pharmacy", "Pharmacy"),
            ("professional", "Professional"),
            ("vision", "Vision")],
        help="The category of claim, eg, oral, pharmacy, vision, insitutional, professional.")
    sub_type_ids = fields.Many2many(
        comodel_name="hc.vs.claim.sub.type",
        relation="claim_sub_type_rel",
        string="Sub Types",
        help="Finer grained claim type information.")
    ruleset_id = fields.Many2one(
        comodel_name="hc.vs.ruleset",
        string="Ruleset",
        help="Current specification followed.")
    original_ruleset_id = fields.Many2one(
        comodel_name="hc.vs.ruleset",
        string="Original Ruleset",
        help="Original specification followed.")
    created = fields.Datetime(
        string="Created Date",
        help="Creation date.")
    start_date = fields.Datetime(
        string="Start Date",
        help="Start of the period for charge submission.")
    end_date = fields.Datetime(
        string="End Date",
        help="End of the period for charge submission.")
    insurer_id = fields.Many2one(
        comodel_name="hc.res.organization",
        string="Insurer",
        help="Target.")
    provider_id = fields.Many2one(
        comodel_name="hc.res.practitioner",
        string="Provider",
        help="Responsible provider.")
    organization_id = fields.Many2one(
        comodel_name="hc.res.organization",
        string="Organization",
        help="Responsible organization.")
    use_id = fields.Selection(
        string="Use",
        selection=[
            ("complete", "Complete"),
            ("proposed", "Proposed"),
            ("exploratory", "Exploratory"),
            ("other", "Other")],
        help="Complete (Bill or Claim), Proposed (Pre-Authorization), Exploratory (Pre-determination).")
    priority_id = fields.Many2one(
        comodel_name="hc.vs.process.priority",
        string="Priority",
        help="Desired processing priority.")
    funds_reserve_id = fields.Many2one(
        comodel_name="hc.vs.funds.reserve",
        string="Funds Reserve",
        help="Funds requested to be reserved.")
    enterer_id = fields.Many2one(
        comodel_name="hc.res.practitioner",
        string="Enterer",
        help="Author.")
    facility_id = fields.Many2one(
        comodel_name="hc.res.location",
        string="Facility",
        help="Servicing Facility.")
    prescription_type = fields.Selection(
        string="Prescription Type",
        selection=[
            ("medication_request", "Medication Request"),
            ("vision_prescription", "Vision Prescription")],
        help="Type of prescription.")
    prescription_name = fields.Char(
        string="Prescription",
        compute="_compute_prescription_name",
        store="True",
        help="Prescription.")
    prescription_medication_request_id = fields.Many2one(
        comodel_name="hc.res.medication.request",
        string="Prescription Medication Request",
        help="Medication Request that is participating in the appointment.")
    prescription_vision_prescription_id = fields.Many2one(
        comodel_name="hc.res.vision.prescription",
        string="Prescription Vision Prescription",
        help="Vision Prescription that is participating in the appointment.")
    original_prescription_id = fields.Many2one(
        comodel_name="hc.res.medication.request",
        string="Original Prescription",
        help="Original Prescription.")
    referral_id = fields.Many2one(
        comodel_name="hc.res.procedure.request",
        string="Referral",
        help="Treatment Referral.")
    patient_id = fields.Many2one(
        comodel_name="hc.res.patient",
        string="Patient",
        required="True",
        help="The subject of the Products and Services.")
    start_date = fields.Datetime(
        string="Start Date",
        help="Start of the period unable to work.")
    end_date = fields.Datetime(
        string="End Date",
        help="End of the period unable to work.")
    start_date = fields.Datetime(
        string="Start Date",
        help="Start of the period in hospital.")
    end_date = fields.Datetime(
        string="End Date",
        help="End of the period in hospital.")
    total = fields.Float(
        string="Total",
        help="Total claim cost.")
    related_ids = fields.One2many(
        comodel_name="hc.claim.related.claim",
        inverse_name="claim_id",
        string="Related",
        help="Related Claims which may be revelant to processing this claim.")
    payee_ids = fields.One2many(
        comodel_name="hc.claim.payee",
        inverse_name="claim_id",
        string="Payees",
        help="Payee.")
    information_ids = fields.One2many(
        comodel_name="hc.claim.special.condition",
        inverse_name="claim_id",
        string="Information",
        help="Exceptions, special considerations, the condition, situation, prior or concurrent issues.")
    diagnosis_ids = fields.One2many(
        comodel_name="hc.claim.diagnosis",
        inverse_name="claim_id",
        string="Diagnosis",
        help="Diagnosis.")
    procedure_ids = fields.One2many(
        comodel_name="hc.claim.procedure",
        inverse_name="claim_id",
        string="Procedures",
        help="Procedures performed.")
    coverage_ids = fields.One2many(
        comodel_name="hc.claim.coverage",
        inverse_name="claim_id",
        string="Coverages",
        help="Insurance or medical plan.")
    accident_ids = fields.One2many(
        comodel_name="hc.claim.accident",
        inverse_name="claim_id",
        string="Accidents",
        help="Details about an accident.")
    missing_teeth_ids = fields.One2many(
        comodel_name="hc.claim.missing.teeth",
        inverse_name="claim_id",
        string="Missing Teeth",
        help="Only if type = oral.")
    item_ids = fields.One2many(
        comodel_name="hc.claim.item",
        inverse_name="claim_id",
        string="Items",
        help="Goods and Services.")

    @api.model
    def create(self, vals):
        status_history_obj = self.env['hc.claim.status.history']
        res = super(Claim, self).create(vals)
        if vals and vals.get('status_id'):
            status_history_vals = {
                'claim_id': res.id,
                'status': res.status_id.name,
                'start_date': datetime.today()
                }
            if vals.get('status_id') == 'entered-in-error':
                status_history_vals.update({'end_date': datetime.today()})
            status_history_obj.create(status_history_vals)
        return res

    @api.multi
    def write(self, vals):
        status_history_obj = self.env['hc.claim.status.history']
        fm_status_obj = self.env['hc.vs.fm.status']
        res = super(Claim, self).write(vals)
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
                fm_status = fm_status_obj.browse(vals.get('status_id'))
                status_history_vals = {
                    'claim_id': self.id,
                    'status': fm_status.name,
                    'start_date': datetime.today()
                    }
                if vals.get('status_id') == 'entered-in-error':
                    status_id_history_vals.update({'end_date': datetime.today()})
                status_history_obj.create(status_history_vals)
        return res


class ClaimRelatedClaim(models.Model):
    _name = "hc.claim.related.claim"
    _description = "Claim Related Claim"

    claim_id = fields.Many2one(
        comodel_name="hc.res.claim",
        string="Claim",
        help="Claim associated with this Claim Related Claim.")
    claim_id = fields.Many2one(
        comodel_name="hc.res.claim",
        string="Claim",
        help="Reference to the related claim.")
    relationship_id = fields.Many2one(
        comodel_name="hc.vs.related.claim.relationship",
        string="Relationship",
        help="How the reference claim is related.")
    reference_id = fields.Many2one(
        comodel_name="hc.claim.related.claim.reference",
        string="Reference",
        help="Related file or case reference.")

class ClaimPayee(models.Model):
    _name = "hc.claim.payee"
    _description = "Claim Payee"

    claim_id = fields.Many2one(
        comodel_name="hc.res.claim",
        string="Claim",
        help="Claim associated with this Claim Payee.")
    type_id = fields.Many2one(
        comodel_name="hc.vs.payee.type",
        string="Type",
        required="True",
        help="Type of party: Subscriber, Provider, other.")
    resource_type = fields.Selection(
        string="Resource Type",
        selection=[
            ("organization", "Organization"),
            ("patient", "Patient"),
            ("practitioner", "Practitioner"),
            ("related_person", "Related Person")],
        help="The type of payee Resource.")
    party_type = fields.Selection(
        string="Party Type",
        selection=[
            ("practitioner", "Practitioner"),
            ("organization", "Organization"),
            ("patient", "Patient"),
            ("related_person", "Related Person")],
        help="Type of party to receive the payable.")
    party_name = fields.Char(
        string="Party",
        compute="_compute_party_name",
        store="True",
        help="Party to receive the payable.")
    party_practitioner_id = fields.Many2one(
        comodel_name="hc.res.practitioner",
        string="Party Practitioner",
        help="Practitioner to receive the payable.")
    party_organization_id = fields.Many2one(
        comodel_name="hc.res.organization",
        string="Party Organization",
        help="Organization to receive the payable")
    party_patient_id = fields.Many2one(
        comodel_name="hc.res.patient",
        string="Party Patient",
        help="Patient to receive the payable.")
    party_related_person_id = fields.Many2one(
        comodel_name="hc.res.related.person",
        string="Party Related Person",
        help="Related Person to receive the payable.")

class ClaimSpecialCondition(models.Model):
    _name = "hc.claim.special.condition"
    _description = "Claim Special Condition"

    claim_id = fields.Many2one(
        comodel_name="hc.res.claim",
        string="Claim",
        help="Claim associated with this Claim Special Condition.")
    category_id = fields.Many2one(
        comodel_name="hc.vs.claim.information.category",
        string="Category",
        required="True",
        help="Category of information.")
    code_id = fields.Many2one(
        comodel_name="hc.vs.claim.exception",
        string="Code",
        help="Type of information.")
    timing_type = fields.Selection(
        string="Timing Type",
        selection=[
            ("date", "Date"),
            ("period", "Period")],
        help="Type of when it occurred.")
    timing_name = fields.Char(
        string="Timing",
        compute="_compute_timing_name",
        store="True",
        help="When it occurred.")
    timing_date = fields.Date(
        string="Timing Date",
        help="Date when it occurred.")
    timing_start_date = fields.Datetime(
        string="Timing Start Date",
        help="Start of the when it occurred.")
    timing_end_date = fields.Datetime(
        string="Timing End Date",
        help="End of the when it occurred.")
    value_type = fields.Selection(
        string="Value Type",
        selection=[
            ("string", "String"),
            ("quantity", "Quantity")],
        help="Type of additional data.")
    value_name = fields.Char(
        string="Value",
        compute="_compute_value_name",
        store="True",
        help="Additional Data.")
    value_string = fields.Char(
        string="Value String",
        help="String of additional data.")
    value_quantity = fields.Float(
        string="Value Quantity",
        help="Quantity of additional data.")
    value_quantity_uom_id = fields.Many2one(
        comodel_name="product.uom",
        string="Value Quantity UOM",
        help="Value Quantity unit of measure.")

class ClaimDiagnosis(models.Model):
    _name = "hc.claim.diagnosis"
    _description = "Claim Diagnosis"

    claim_id = fields.Many2one(
        comodel_name="hc.res.claim",
        string="Claim",
        help="Claim associated with this Claim Diagnosis.")
    sequence = fields.Integer(
        string="Sequence",
        required="True",
        help="Sequence of diagnosis.")
    diagnosis_id = fields.Many2one(
        comodel_name="hc.vs.icd.10",
        string="Diagnosis",
        required="True",
        help="Patient's list of diagnosis.")
    type_ids = fields.Many2many(
        comodel_name="hc.vs.ex.diagnosis.type",
        relation="claim_diagnosis_type_rel",
        string="Types",
        help="Type of Diagnosis.")
    drg_id = fields.Many2one(
        comodel_name="hc.vs.ex.diagnosis.related.group",
        string="DRG",
        help="Diagnosis Related Group.")

class ClaimProcedure(models.Model):
    _name = "hc.claim.procedure"
    _description = "Claim Procedure"

    claim_id = fields.Many2one(
        comodel_name="hc.res.claim",
        string="Claim",
        help="Claim associated with this Claim Procedure.")
    sequence = fields.Integer(
        string="Sequence",
        required="True",
        help="Procedure sequence for reference.")
    date = fields.Datetime(
        string="Date",
        help="When the procedure was performed.")
    procedure_type = fields.Selection(
        string="Procedure Type",
        required="True",
        selection=[
            ("code", "Code"),
            ("procedure", "Procedure")],
        help="Type of patient's list of procedures performed.")
    procedure_name = fields.Char(
        string="Procedure",
        compute="_compute_procedure_name",
        store="True",
        help="Patient's list of procedures performed.")
    procedure_code_id = fields.Many2one(
        comodel_name="hc.vs.icd.10.procedure",
        string="Procedure Code",
        help="Code of patient's list of procedures performed.")
    procedure_id = fields.Many2one(
        comodel_name="hc.res.procedure",
        string="Procedure",
        help="Patient's list of procedures performed.")

class ClaimCoverage(models.Model):
    _name = "hc.claim.coverage"
    _description = "Claim Coverage"

    claim_id = fields.Many2one(
        comodel_name="hc.res.claim",
        string="Claim",
        help="Claim associated with this Claim Coverage.")
    sequence = fields.Integer(
        string="Sequence",
        required="True",
        help="Service instance identifier.")
    is_focal = fields.Boolean(
        string="Focal",
        required="True",
        help="Is the focal Coverage.")
    coverage_id = fields.Many2one(
        comodel_name="hc.res.coverage",
        string="Coverage",
        required="True",
        help="Insurance information.")
    business_arrangement = fields.Char(
        string="Business Arrangement",
        help="Business agreement.")
    pre_auth_ref_ids = fields.One2many(
        comodel_name="hc.claim.coverage.pre.auth.ref",
        inverse_name="coverage_id",
        string="Pre Auth Refs",
        help="Pre-Authorization/Determination Reference.")
    # claim_response_id = fields.Many2one(
    #     comodel_name="hc.res.claim.response",
    #     string="Claim Response",
    #     help="Adjudication results.")
    original_ruleset_id = fields.Many2one(
        comodel_name="hc.vs.ruleset",
        string="Original Ruleset",
        help="Original version.")

class ClaimAccident(models.Model):
    _name = "hc.claim.accident"
    _description = "Claim Accident"

    claim_id = fields.Many2one(
        comodel_name="hc.res.claim",
        string="Claim",
        help="Claim associated with this Claim Accident.")
    date = fields.Date(
        string="Date Date",
        required="True",
        help="When the accident occurred.")
    type_id = fields.Many2one(
        comodel_name="hc.vs.act.incident.code",
        string="Type",
        help="The nature of the accident.")
    location_type = fields.Selection(
        string="Location Type",
        selection=[
            ("address", "Address"),
            ("location", "Location")],
        help="Type of accident place.")
    location_name = fields.Char(
        string="Location",
        compute="_compute_location_name",
        store="True",
        help="Accident Place.")
    location_address_id = fields.Many2one(
        comodel_name="hc.claim.accident.location.address",
        string="Location Address",
        help="Address of accident place.")
    location_id = fields.Many2one(
        comodel_name="hc.res.location",
        string="Location",
        help="Location the reference to the location.")

class ClaimMissingTeeth(models.Model):
    _name = "hc.claim.missing.teeth"
    _description = "Claim Missing Teeth"

    claim_id = fields.Many2one(
        comodel_name="hc.res.claim",
        string="Claim",
        help="Claim associated with this Claim Missing Teeth.")
    tooth_id = fields.Many2one(
        comodel_name="hc.vs.teeth",
        string="Tooth",
        required="True",
        help="Tooth Code.")
    reason_id = fields.Many2one(
        comodel_name="hc.vs.missing.tooth.reason",
        string="Reason",
        help="Reason for missing.")
    extraction_date = fields.Date(
        string="Extraction Date",
        help="Date of Extraction.")

class ClaimItem(models.Model):
    _name = "hc.claim.item"
    _description = "Claim Item"

    claim_id = fields.Many2one(
        comodel_name="hc.res.claim",
        string="Claim",
        help="Claim associated with this Claim Item.")
    sequence = fields.Integer(
        string="Sequence",
        required="True",
        help="Service instance.")
    diagnosis_link_id_ids = fields.One2many(
        comodel_name="hc.claim.item.diagnosis.link.id",
        inverse_name="item_id",
        string="Diagnosis Link Ids",
        help="Diagnosis Link.")
    revenue_id = fields.Many2one(
        comodel_name="hc.vs.ex.revenue.center",
        string="Revenue",
        help="Revenue or cost center code.")
    category_id = fields.Many2one(
        comodel_name="hc.vs.benefit.sub.category",
        string="Category",
        help="Type of service or product.")
    service_id = fields.Many2one(
        comodel_name="hc.vs.service.uscls",
        string="Service",
        required="True",
        help="Item Code.")
    modifier_ids = fields.Many2many(
        comodel_name="hc.vs.claim.modifier",
        relation="claim_item_modifier_rel",
        string="Modifiers",
        help="Service/Product billing modifiers.")
    program_code_ids = fields.Many2many(
        comodel_name="hc.vs.ex.program.code",
        relation="claim_item_program_code_rel",
        string="Program Codes",
        help="Program specific reason for item inclusion.")
    serviced_type = fields.Selection(
        string="Serviced Type",
        selection=[
            ("date", "Date"),
            ("period", "Period")],
        help="Type of date of service.")
    serviced_name = fields.Char(
        string="Serviced",
        compute="_compute_serviced_name",
        store="True",
        help="Date or dates of Service.")
    serviced_date = fields.Date(
        string="Serviced Date",
        help="Date of service.")
    serviced_start_date = fields.Datetime(
        string="Serviced Start Date",
        help="Start of the date of service.")
    serviced_end_date = fields.Datetime(
        string="Serviced End Date",
        help="End of the date of service.")
    location_type = fields.Selection(
        string="Location Type",
        selection=[
            ("code", "Code"),
            ("address", "Address"),
            ("location", "Location")],
        help="Type of place of service.")
    location_name = fields.Char(
        string="Location",
        compute="_compute_location_name",
        store="True",
        help="Place of service.")
    location_code_id = fields.Many2one(
        comodel_name="hc.vs.service.place",
        string="Location Code",
        help="Code of place of service.")
    location_address_id = fields.Many2one(
        comodel_name="hc.claim.item.location.address",
        string="Location Address",
        help="Address of place of service.")
    location_id = fields.Many2one(
        comodel_name="hc.res.location",
        string="Location",
        help="Location of place of service.")
    quantity = fields.Float(
        string="Quantity",
        help="Count of Products or Services.")
    quantity_uom_id = fields.Many2one(
        comodel_name="product.uom",
        string="Quantity UOM",
        help="Quantity unit of measure.")
    unit_price = fields.Float(
        string="Unit Price",
        help="Fee, charge or cost per point.")
    factor = fields.Float(
        string="Factor",
        help="Price scaling factor.")
    points = fields.Float(
        string="Points",
        help="Difficulty scaling factor.")
    net = fields.Float(
        string="Net",
        help="Total item cost.")
    udi_id = fields.Many2one(
        comodel_name="hc.vs.unique.device.identifier",
        string="UDI",
        help="Unique Device Identifier.")
    body_site_id = fields.Many2one(
        comodel_name="hc.vs.tooth",
        string="Body Site",
        help="Service Location.")
    sub_site_ids = fields.Many2many(
        comodel_name="hc.vs.surface",
        relation="claim_item_sub_site_rel",
        string="Sub Sites",
        help="Service Sub-location.")
    detail_ids = fields.One2many(
        comodel_name="hc.claim.item.detail",
        inverse_name="item_id",
        string="Details",
        help="Additional items.")
    care_team_ids = fields.One2many(
        comodel_name="hc.claim.item.care.team",
        inverse_name="item_id",
        string="Care Teams",
        help="Members of the care team.")
    prosthesis_ids = fields.One2many(
        comodel_name="hc.claim.item.prosthesis",
        inverse_name="item_id",
        string="Prosthesis",
        help="Prosthetic details.")

class ClaimItemDetail(models.Model):
    _name = "hc.claim.item.detail"
    _description = "Claim Item Detail"

    item_id = fields.Many2one(
        comodel_name="hc.claim.item",
        string="Item",
        help="Goods and Services.")
    sequence = fields.Integer(
        string="Sequence",
        required="True",
        help="Service instance.")
    revenue_id = fields.Many2one(
        comodel_name="hc.vs.ex.revenue.center",
        string="Revenue",
        help="Revenue or cost center code.")
    category_id = fields.Many2one(
        comodel_name="hc.vs.benefit.sub.category",
        string="Category",
        help="Type of service or product.")
    service_id = fields.Many2one(
        comodel_name="hc.vs.service.uscls",
        string="Service",
        required="True",
        help="Additional item codes.")
    modifier_ids = fields.Many2many(
        comodel_name="hc.vs.claim.modifier",
        relation="claim_item_detail_modifier_rel",
        string="Modifiers",
        help="Service/Product billing modifiers.")
    program_code_ids = fields.Many2many(
        comodel_name="hc.vs.ex.program.code",
        relation="claim_item_detail_program_code_rel",
        string="Program Codes",
        help="Program specific reason for item inclusion.")
    quantity = fields.Float(
        string="Quantity",
        help="Count of Products or Services.")
    quantity_uom_id = fields.Many2one(
        comodel_name="product.uom",
        string="Quantity UOM",
        help="Quantity unit of measure.")
    unit_price = fields.Float(
        string="Unit Price",
        help="Fee, charge or cost per point.")
    factor = fields.Float(
        string="Factor",
        help="Price scaling factor.")
    points = fields.Float(
        string="Points",
        help="Difficulty scaling factor.")
    net = fields.Float(
        string="Net",
        help="Total additional item cost.")
    udi_id = fields.Many2one(
        comodel_name="hc.vs.unique.device.identifier",
        string="UDI",
        help="Unique Device Identifier.")
    sub_detail_ids = fields.One2many(
        comodel_name="hc.claim.item.detail.sub.detail",
        inverse_name="detail_id",
        string="Sub Details",
        help="Additional items.")

class ClaimItemDetailSubDetail(models.Model):
    _name = "hc.claim.item.detail.sub.detail"
    _description = "Claim Item Detail Sub Detail"

    detail_id = fields.Many2one(
        comodel_name="hc.claim.item.detail",
        string="Detail",
        help="Additional items.")
    sequence = fields.Integer(
        string="Sequence",
        required="True",
        help="Service instance.")
    original_ruleset_id = fields.Many2one(
        comodel_name="hc.vs.ruleset",
        string="Original Ruleset",
        help="Revenue or cost center code.")
    type_id = fields.Many2one(
        comodel_name="hc.vs.benefit.sub.category",
        string="Type",
        help="Type of service or product.")
    service_id = fields.Many2one(
        comodel_name="hc.vs.service.uscls",
        string="Service",
        required="True",
        help="Additional item codes.")
    modifier_ids = fields.Many2many(
        comodel_name="hc.vs.claim.modifier",
        relation="claim_item_detail_subdetail_modifier_rel",
        string="Modifiers",
        help="Service/Product billing modifiers.")
    program_code_ids = fields.Many2many(
        comodel_name="hc.vs.ex.program.code",
        relation="claim_item_detail_sub_detail_program_code_rel",
        string="Program Codes",
        help="Program specific reason for item inclusion.")
    quantity = fields.Float(
        string="Quantity",
        help="Count of Products or Services.")
    unit_price = fields.Float(
        string="Unit Price",
        help="Fee, charge or cost per point.")
    factor = fields.Float(
        string="Factor",
        help="Price scaling factor.")
    points = fields.Float(
        string="Points",
        help="Difficulty scaling factor.")
    net = fields.Float(
        string="Net",
        help="Net additional item cost.")
    udi_id = fields.Many2one(
        comodel_name="hc.vs.unique.device.identifier",
        string="UDI",
        help="Unique Device Identifier.")

class ClaimItemCareTeam(models.Model):
    _name = "hc.claim.item.care.team"
    _description = "Claim Item Care Team"

    item_id = fields.Many2one(
        comodel_name="hc.claim.item",
        string="Item",
        help="Goods and Services.")
    provider_type = fields.Selection(
        string="Provider Type",
        required="True",
        selection=[
            ("practitioner", "Practitioner"),
            ("organization", "Organization")],
        help="Type of provider individual or organization.")
    provider_name = fields.Char(
        string="Provider",
        compute="_compute_provider_name",
        store="True",
        help="Provider individual or organization.")
    provider_practitioner_id = fields.Many2one(
        comodel_name="hc.res.practitioner",
        string="Provider Practitioner",
        required="True",
        help="Practitioner that is participating in the appointment.")
    provider_organization_id = fields.Many2one(
        comodel_name="hc.res.organization",
        string="Provider Organization",
        help="Organization that is participating in the appointment.")
    is_responsible = fields.Boolean(
        string="Responsible",
        help="Billing provider.")
    role_id = fields.Many2one(
        comodel_name="hc.vs.claim.care.team.role",
         string="Role",
         help="Role on the team.")
    qualification_id = fields.Many2one(
        comodel_name="hc.vs.provider.qualification",
        string="Qualification",
        help="Type, classification or Specialization.")

class ClaimItemProsthesis(models.Model):
    _name = "hc.claim.item.prosthesis"
    _description = "Claim Item Prosthesis"

    item_id = fields.Many2one(
        comodel_name="hc.claim.item",
        string="Item",
        help="Goods and Services.")
    is_initial = fields.Boolean(
        string="Initial",
        help="Is this the initial service.")
    prior_date = fields.Date(
        string="Prior Date",
        help="Initial service Date.")
    prior_material_id = fields.Many2one(
        comodel_name="hc.vs.oral.prosthodontic.material",
        string="Prior Material",
        help="Prosthetic Material.")

class ClaimIdentifier(models.Model):
    _name = "hc.claim.identifier"
    _description = "Claim Identifier"
    _inherit = ["hc.basic.association", "hc.identifier"]

    claim_id = fields.Many2one(
        comodel_name="hc.res.claim",
        string="Claim",
        help="Claim associated with this Claim Identifier.")

class ClaimStatusHistory(models.Model):
    _name = "hc.claim.status.history"
    _description = "Claim Status History"

    claim_id = fields.Many2one(
        comodel_name="hc.res.claim",
        string="Claim",
        help="Claim associated with this Claim Status History.")
    status = fields.Char(
        string="Status",
        help="The status of the claim.")
    start_date = fields.Datetime(
        string="Start Date",
        help="Start of the period during which this claim status is valid.")
    end_date = fields.Datetime(
        string="End Date",
        help="End of the period during which this claim status is valid.")
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

class ClaimAccidentLocationAddress(models.Model):
    _name = "hc.claim.accident.location.address"
    _description = "Claim Accident Location Address"
    _inherit = ["hc.address.use"]
    _inherits = {"hc.address": "location_id"}

    location_id = fields.Many2one(
        comodel_name="hc.address",
        string="Location",
        ondelete="restrict",
        required="True",
        help="Location Address associated with this Claim Accident Location Address.")

class ClaimItemLocationAddress(models.Model):
    _name = "hc.claim.item.location.address"
    _description = "Claim Item Location Address"
    _inherit = ["hc.address.use"]
    _inherits = {"hc.address": "location_id"}

    location_id = fields.Many2one(
        comodel_name="hc.address",
        string="Location",
        ondelete="restrict",
        required="True",
        help="Location Address associated with this Claim Item Location Address.")

class ClaimCoveragePreAuthRef(models.Model):
    _name = "hc.claim.coverage.pre.auth.ref"
    _description = "Claim Coverage Pre Auth Ref"
    _inherit = ["hc.basic.association"]

    coverage_id = fields.Many2one(
        comodel_name="hc.claim.coverage",
        string="Coverage",
        help="Insurance or medical plan.")
    pre_auth_ref = fields.Char(
        string="Pre Auth Ref",
        help="Pre Auth Ref associated with this Claim Coverage Pre Auth Ref.")

class ClaimItemDiagnosisLinkId(models.Model):
    _name = "hc.claim.item.diagnosis.link.id"
    _description = "Claim Item Diagnosis Link Id"
    _inherit = ["hc.basic.association"]

    item_id = fields.Many2one(
        comodel_name="hc.claim.item",
        string="Item",
        help="Goods and Services.")
    diagnosis_link_id = fields.Integer(
        string="Diagnosis Link Id",
        help="Diagnosis Link Id associated with this Claim Item Diagnosis Link Id.")

class ClaimRelatedClaimReference(models.Model):
    _name = "hc.claim.related.claim.reference"
    _description = "Claim Related Claim Reference"
    _inherit = ["hc.basic.association", "hc.identifier"]

class ActIncidentCode(models.Model):
    _name = "hc.vs.act.incident.code"
    _description = "Act Incident Code"
    _inherit = ["hc.value.set.contains"]

class ClaimCareTeamRole(models.Model):
    _name = "hc.vs.claim.care.team.role"
    _description = "Claim Care Team Role"
    _inherit = ["hc.value.set.contains"]

class ClaimException(models.Model):
    _name = "hc.vs.claim.exception"
    _description = "Claim Exception"
    _inherit = ["hc.value.set.contains"]

class ClaimInformationCategory(models.Model):
    _name = "hc.vs.claim.information.category"
    _description = "Claim Information Category"
    _inherit = ["hc.value.set.contains"]

class ClaimModifier(models.Model):
    _name = "hc.vs.claim.modifier"
    _description = "Claim Modifier"
    _inherit = ["hc.value.set.contains"]

class ClaimSubType(models.Model):
    _name = "hc.vs.claim.sub.type"
    _description = "Claim Sub Type"
    _inherit = ["hc.value.set.contains"]

class ClaimUseLink(models.Model):
    _name = "hc.vs.claim.use.link"
    _description = "Claim Use Link"
    _inherit = ["hc.value.set.contains"]

class ExDiagnosisRelatedGroup(models.Model):
    _name = "hc.vs.ex.diagnosis.related.group"
    _description = "Ex Diagnosis Related Group"
    _inherit = ["hc.value.set.contains"]

class ExDiagnosisType(models.Model):
    _name = "hc.vs.ex.diagnosis.type"
    _description = "Ex Diagnosis Type"
    _inherit = ["hc.value.set.contains"]

class ExPayeeResourceType(models.Model):
    _name = "hc.vs.ex.payee.resource.type"
    _description = "Ex Payee Resource Type"
    _inherit = ["hc.value.set.contains"]

class ExProgramCode(models.Model):
    _name = "hc.vs.ex.program.code"
    _description = "Ex Program Code"
    _inherit = ["hc.value.set.contains"]

class ExRevenueCenter(models.Model):
    _name = "hc.vs.ex.revenue.center"
    _description = "Ex Revenue Center"
    _inherit = ["hc.value.set.contains"]

class FundsReserve(models.Model):
    _name = "hc.vs.funds.reserve"
    _description = "Funds Reserve"
    _inherit = ["hc.value.set.contains"]

class ICD10(models.Model):
    _name = "hc.vs.icd.10"
    _description = "ICD-10"
    _inherit = ["hc.value.set.contains"]

class ICD10Procedure(models.Model):
    _name = "hc.vs.icd.10.procedure"
    _description = "ICD-10 Procedure"
    _inherit = ["hc.value.set.contains"]

class InformationType(models.Model):
    _name = "hc.vs.information.type"
    _description = "Information Type"
    _inherit = ["hc.value.set.contains"]


class MissingToothReason(models.Model):
    _name = "hc.vs.missing.tooth.reason"
    _description = "Missing Tooth Reason"
    _inherit = ["hc.value.set.contains"]

class OralProsthodonticMaterial(models.Model):
    _name = "hc.vs.oral.prosthodontic.material"
    _description = "Oral Prosthodontic Material"
    _inherit = ["hc.value.set.contains"]

class PayeeType(models.Model):
    _name = "hc.vs.payee.type"
    _description = "Payee Type"
    _inherit = ["hc.value.set.contains"]

class ProviderQualification(models.Model):
    _name = "hc.vs.provider.qualification"
    _description = "Provider Qualification"
    _inherit = ["hc.value.set.contains"]

class RelatedClaimRelationship(models.Model):
    _name = "hc.vs.related.claim.relationship"
    _description = "Related Claim Relationship"
    _inherit = ["hc.value.set.contains"]

class ServicePlace(models.Model):
    _name = "hc.vs.service.place"
    _description = "Service Place"
    _inherit = ["hc.value.set.contains"]

class ServiceUSCLS(models.Model):
    _name = "hc.vs.service.uscls"
    _description = "Service USCLS"
    _inherit = ["hc.value.set.contains"]

class Surface(models.Model):
    _name = "hc.vs.surface"
    _description = "Surface"
    _inherit = ["hc.value.set.contains"]

class Teeth(models.Model):
    _name = "hc.vs.teeth"
    _description = "Teeth"
    _inherit = ["hc.value.set.contains"]

class Tooth(models.Model):
    _name = "hc.vs.tooth"
    _description = "Tooth"
    _inherit = ["hc.value.set.contains"]

class UniqueDeviceIdentifier(models.Model):
    _name = "hc.vs.unique.device.identifier"
    _description = "Unique Device Identifier"
    _inherit = ["hc.value.set.contains"]
