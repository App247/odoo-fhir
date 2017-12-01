# -*- coding: utf-8 -*-

from openerp import models, fields, api

class ExplanationOfBenefit(models.Model):
    _name = "hc.res.explanation.of.benefit"
    _description = "Explanation Of Benefit"

    identifier_ids = fields.One2many(
        comodel_name="hc.explanation.of.benefit.identifier",
        inverse_name="explanation_of_benefit_id",
        string="Identifiers",
        help="Business Identifier.")
    status = fields.Selection(
        string="Explanation Of Benefit Status",
        required="True",
        selection=[
            ("active", "Active"),
            ("cancelled", "Cancelled"),
            ("draft", "Draft"),
            ("entered-in-error", "Entered-In-Error")],
        help="The status of the resource instance.")
    type_id = fields.Many2one(
        comodel_name="hc.vs.claim.type",
        string="Type",
        required="True",
        help="Type or discipline.")
    sub_type_ids = fields.Many2many(
        comodel_name="hc.vs.claim.sub.type",
        relation="explanation_of_benefit_sub_type_rel",
        string="Sub Types",
        help="Finer grained claim type information.")
    patient_id = fields.Many2one(
        comodel_name="hc.res.patient",
        string="Patient",
        required="True",
        help="The subject of the Products and Services.")
    billable_period_start_date = fields.Datetime(
        string="Billable Period Start Date",
        help="Start of the period for charge submission.")
    billable_period_end_date = fields.Datetime(
        string="Billable Period End Date",
        help="End of the period for charge submission.")
    created = fields.Datetime(
        string="Created",
        help="Creation date.")
    insurer_id = fields.Many2one(
        comodel_name="hc.res.organization",
        string="Insurer",
        help="Insurer responsible for the EOB.")
    provider_id = fields.Many2one(
        comodel_name="hc.res.practitioner",
        string="Provider",
        help="Responsible provider for the claim.")
    organization_id = fields.Many2one(
        comodel_name="hc.res.organization",
        string="Organization",
        help="Responsible organization for the claim.")
    referral_id = fields.Many2one(
        comodel_name="hc.res.procedure.request",
        string="Referral",
        help="Treatment Referral.")
    facility_id = fields.Many2one(
        comodel_name="hc.res.location",
        string="Facility",
        help="Servicing Facility.")
    claim_id = fields.Many2one(
        comodel_name="hc.res.claim",
        string="Claim",
        help="Claim reference.")
    claim_response_id = fields.Many2one(
        comodel_name="hc.res.claim.response",
        string="Claim Response",
        help="Claim response reference.")
    outcome = fields.Selection(
        string="Explanation Of Benefit Outcome",
        selection=[
            ("complete", "Complete"),
            ("error", "Error"),
            ("partial", "Partial")],
        help="Processing outcome error, partial or complete processing.")
    disposition = fields.Char(
        string="Disposition",
        help="Disposition Message.")
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
        help="Medication Request prescription.")
    prescription_vision_prescription_id = fields.Many2one(
        comodel_name="hc.res.vision.prescription",
        string="Prescription Vision Prescription",
        help="Vision Prescription prescription.")
    original_prescription_id = fields.Many2one(
        comodel_name="hc.res.medication.request",
        string="Original Prescription",
        help="Original Prescription.")
    precedence = fields.Integer(
        string="Precedence",
        help="Precedence (primary, secondary, etc.).")
    employment_impacted_start_date = fields.Datetime(
        string="Employment Impacted Start Date",
        help="Start of the period unable to work.")
    employment_impacted_end_date = fields.Datetime(
        string="Employment Impacted End Date",
        help="End of the period unable to work.")
    hospitalization_start_date = fields.Datetime(
        string="Hospitalization Start Date",
        help="Start of the period in hospital.")
    hospitalization_end_date = fields.Datetime(
        string="Hospitalization End Date",
        help="End of the period in hospital.")
    total_cost = fields.Float(
        string="Total Cost",
        help="Total Cost of service from the Claim.")
    unalloc_deductable = fields.Float(
        string="Unalloc Deductable",
        help="Unallocated deductable.")
    total_benefit = fields.Float(
        string="Total Benefit",
        help="Total benefit payable for the Claim.")
    form_id = fields.Many2one(
        comodel_name="hc.vs.forms",
        string="Form",
        help="Printed Form Identifier.")
    is_payee = fields.Boolean(
        string="Payee",
        help="Payee.")
    payee_type_id = fields.Many2one(
        comodel_name="hc.vs.payee.type",
        string="Payee Type",
        help="Type of party: Subscriber, Provider, other.")
    payee_resource_type = fields.Selection(
        string="Payee Resource Type",
        selection=[
            ("organization", "Organization"),
            ("patient", "Patient"),
            ("practitioner", "Practitioner"),
            ("related_person", "Related Person")],
        help="The type of payee Resource.")
    payee_party_type = fields.Selection(
        string="Payee Party Type",
        selection=[
            ("identifier", "Identifier"),
            ("practitioner", "Practitioner"),
            ("organization", "Organization"),
            ("patient", "Patient"),
            ("related_person", "Related Person")],
            help="Type of party to receive the payable.")
    payee_party_name = fields.Char(
        string="Payee Party",
        compute="_compute_payee_party_name",
        store="True",
        help="Party to receive the payable.")
    payee_party_identifier_id = fields.Many2one(
        comodel_name="hc.explanation.of.benefit.payee.party.identifier",
        string="Payee Party Identifier",
        help="Identifier of party to receive the payable.")
    payee_party_practitioner_id = fields.Many2one(
        comodel_name="hc.res.practitioner",
        string="Payee Party Practitioner",
        help="Practitioner to receive the payable.")
    payee_party_organization_id = fields.Many2one(
        comodel_name="hc.res.organization",
        string="Payee Party Organization",
        help="Organization to receive the payable.")
    payee_party_patient_id = fields.Many2one(
        comodel_name="hc.res.patient",
        string="Payee Party Patient",
        help="Patient to receive the payable.")
    payee_party_related_person_id = fields.Many2one(
        comodel_name="hc.res.related.person",
        string="Payee Party Related Person",
        help="Related Person to receive the payable.")
    is_insurance = fields.Boolean(
        string="Insurance",
        help="Insurance or medical plan.")
    insurance_coverage_id = fields.Many2one(
        comodel_name="hc.res.coverage",
        string="Insurance Coverage",
        help="Insurance information.")
    insurance_pre_auth_ref_ids = fields.One2many(
        comodel_name="hc.explanation.of.benefit.insurance.pre.auth.ref",
        inverse_name="explanation_of_benefit_id",
        string="Insurance Pre Auth Refs",
        help="Pre-Authorization/Determination Reference.")
    is_accident = fields.Boolean(
        string="Accident",
        help="Details of an accident.")
    accident_date = fields.Date(
        string="Accident Date",
        help="When the accident occurred.")
    accident_type_id = fields.Many2one(
        comodel_name="hc.vs.act.incident.code",
        string="Accident Type",
        help="The nature of the accident.")
    accident_location_type = fields.Selection(
        string="Accident Location Type",
        selection=[
            ("address", "Address"),
            ("location", "Location")],
        help="Type of accident Place.")
    accident_location_name = fields.Char(
        string="Accident Location",
        compute="_compute_accident_location_name",
        store="True",
        help="Accident Place.")
    accident_location_address_id = fields.Many2one(
        comodel_name="hc.address",
        string="Accident Location Address",
        help="Address of accident place.")
    accident_location_location_id = fields.Many2one(
        comodel_name="hc.res.location",
        string="Accident Location Location",
        help="Location of accident place.")
    is_payment = fields.Boolean(
        string="Payment",
        help="Payment (if paid).")
    payment_type_id = fields.Many2one(
        comodel_name="hc.vs.ex.payment.type",
        string="Payment Type",
        help="Partial or Complete.")
    payment_adjustment = fields.Float(
        string="Payment Adjustment",
        help="Payment adjustment for non-Claim issues.")
    payment_adjustment_reason_id = fields.Many2one(
        comodel_name="hc.vs.payment.adjustment.reason",
        string="Payment Adjustment Reason",
        help="Reason for Payment adjustment.")
    payment_date = fields.Date(
        string="Payment Date",
        help="Expected date of Payment.")
    payment_amount = fields.Float(
        string="Payment Amount",
        help="Payment amount.")
    payment_identifier_id = fields.Many2one(
        comodel_name="hc.explanation.of.benefit.payment.identifier",
        string="Payment Identifier",
        help="Payment identifier.")
    related_ids = fields.One2many(
        comodel_name="hc.explanation.of.benefit.related.claim",
        inverse_name="explanation_of_benefit_id",
        string="Related",
        help="Related Claims which may be revelant to processing this claimn.")
    information_ids = fields.One2many(
        comodel_name="hc.explanation.of.benefit.special.condition",
        inverse_name="explanation_of_benefit_id",
        string="Information",
        help="Exceptions, special considerations, the condition, situation, prior or concurrent issues.")
    care_team_ids = fields.One2many(
        comodel_name="hc.explanation.of.benefit.care.team",
        inverse_name="explanation_of_benefit_id",
        string="Care Teams",
        help="Care Team members.")
    diagnosis_ids = fields.One2many(
        comodel_name="hc.explanation.of.benefit.diagnosis",
        inverse_name="explanation_of_benefit_id",
        string="Diagnosis",
        help="Diagnosis.")
    procedure_ids = fields.One2many(
        comodel_name="hc.explanation.of.benefit.procedure",
        inverse_name="explanation_of_benefit_id",
        string="Procedures",
        help="Procedures performed.")
    item_ids = fields.One2many(
        comodel_name="hc.explanation.of.benefit.item",
        inverse_name="explanation_of_benefit_id",
        string="Items",
        help="Goods and Services.")
    added_item_ids = fields.One2many(
        comodel_name="hc.explanation.of.benefit.added.item",
        inverse_name="explanation_of_benefit_id",
        string="Added Items",
        help="Insurer added line items.")
    note_ids = fields.One2many(
        comodel_name="hc.explanation.of.benefit.note",
        inverse_name="explanation_of_benefit_id",
        string="Notes",
        help="Processing notes.")
    benefit_balance_ids = fields.One2many(
        comodel_name="hc.explanation.of.benefit.balance",
        inverse_name="explanation_of_benefit_id",
        string="Benefit Balances",
        help="Balance by Benefit Category.")

class ExplanationOfBenefitRelatedClaim(models.Model):
    _name = "hc.explanation.of.benefit.related.claim"
    _description = "Explanation Of Benefit Related Claim"

    explanation_of_benefit_id = fields.Many2one(
        comodel_name="hc.res.explanation.of.benefit",
        string="Explanation Of Benefit",
        help="Explanation Of Benefit associated with this Explanation Of Benefit Related Claim.")
    claim_id = fields.Many2one(
        comodel_name="hc.res.claim",
        string="Claim",
        help="Reference to the related claim.")
    relationship_id = fields.Many2one(
        comodel_name="hc.vs.related.claim.relationship",
        string="Relationship",
        help="How the reference claim is related.")
    reference_id = fields.Many2one(
        comodel_name="hc.explanation.of.benefit.related.claim.reference",
        string="Reference",
        help="Related file or case reference.")

class ExplanationOfBenefitSpecialCondition(models.Model):
    _name = "hc.explanation.of.benefit.special.condition"
    _description = "Explanation Of Benefit Special Condition"

    explanation_of_benefit_id = fields.Many2one(
        comodel_name="hc.res.explanation.of.benefit",
        string="Explanation Of Benefit",
        help="Explanation Of Benefit associated with this Explanation Of Benefit Special Condition.")
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
        help="Code of when it occurred.")
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
        help="Type of additional Data.")
    value_name = fields.Char(
        string="Value",
        compute="_compute_value_name",
        store="True",
        help="Additional Data.")
    value_string = fields.Char(
        string="Value String",
        help="Code of additional data.")
    value_quantity = fields.Float(
        string="Value Quantity",
        help="Quantity additional data.")
    value_quantity_uom_id = fields.Many2one(
        comodel_name="product.uom",
        string="Value Quantity UOM",
        help="Value Quantity unit of measure.")

class ExplanationOfBenefitCareTeam(models.Model):
    _name = "hc.explanation.of.benefit.care.team"
    _description = "Explanation Of Benefit Care Team"

    explanation_of_benefit_id = fields.Many2one(
        comodel_name="hc.res.explanation.of.benefit",
        string="Explanation Of Benefit",
        help="Explanation Of Benefit associated with this Explanation Of Benefit Care Team.")
    provider_type = fields.Selection(
        string="Provider Type",
        required="True",
        selection=[
            ("practitioner", "Practitioner"),
            ("organization", "Organization")],
        help="Type of member of the care team.")
    provider_name = fields.Char(
        string="Provider",
        compute="_compute_provider_name",
        store="True",
        help="Member of the Care Team.")
    provider_practitioner_id = fields.Many2one(
        comodel_name="hc.res.practitioner",
        string="Provider Practitioner",
        required="True",
        help="Practitioner member of the care team.")
    provider_organization_id = fields.Many2one(
        comodel_name="hc.res.organization",
        string="Provider Organization",
        help="Organization member of the care team.")
    is_responsible = fields.Boolean(
        string="Responsible",
        help="Billing practitioner.")
    role_id = fields.Many2one(
        comodel_name="hc.vs.claim.care.team.role",
        string="Role",
        help="Role on the team.")
    qualification_id = fields.Many2one(
        comodel_name="hc.vs.provider.qualification",
        string="Qualification",
        help="Type, classification or Specialization.")

class ExplanationOfBenefitDiagnosis(models.Model):
    _name = "hc.explanation.of.benefit.diagnosis"
    _description = "Explanation Of Benefit Diagnosis"

    explanation_of_benefit_id = fields.Many2one(
        comodel_name="hc.res.explanation.of.benefit",
        string="Explanation Of Benefit",
        help="Explanation Of Benefit associated with this Explanation Of Benefit Diagnosis.")
    sequence = fields.Integer(
        string="Sequence",
        required="True",
        help="Number to covey order of diagnosis.")
    diagnosis_type = fields.Selection(
        string="Diagnosis Type",
        required="True",
        selection=[
            ("code", "Code"),
            ("procedure", "Procedure")],
        help="Type of patient's diagnosis.")
    diagnosis_name = fields.Char(
        string="Diagnosis",
        compute="_compute_diagnosis_name",
        store="True",
        help="Patient's diagnosis.")
    diagnosis_code_id = fields.Many2one(
        comodel_name="hc.vs.icd.10",
        string="Diagnosis Code",
        required="True",
        help="Patient's diagnosis.")
    diagnosis_condition_id = fields.Many2one(
        comodel_name="hc.res.condition",
        string="Diagnosis Condition",
        help="Patient's diagnosis.")
    type_ids = fields.Many2many(
        comodel_name="hc.vs.diagnosis.type",
        relation="explanation_of_benefit_diagnosis_type_rel",
        string="Types",
        help="Type of Diagnosis.")
    package_code_id = fields.Many2one(
        comodel_name="hc.vs.diagnosis.package.code",
        string="Package Code",
        help="Package billing code.")

class ExplanationOfBenefitProcedure(models.Model):
    _name = "hc.explanation.of.benefit.procedure"
    _description = "Explanation Of Benefit Procedure"

    explanation_of_benefit_id = fields.Many2one(
        comodel_name="hc.res.explanation.of.benefit",
        string="Explanation Of Benefit",
        help="Explanation Of Benefit associated with this Explanation Of Benefit Procedure.")
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
        help="Type of procedures performed.")
    procedure_name = fields.Char(
        string="Procedure",
        compute="_compute_procedure_name",
        store="True",
        help="Patient's list of procedures performed.")
    procedure_code_id = fields.Many2one(
        comodel_name="hc.vs.icd.10.procedure",
        string="Procedure Code",
        help="Code of patient's list of procedures performed.")
    procedure_procedure_id = fields.Many2one(
        comodel_name="hc.res.procedure",
        string="Procedure",
        help="Procedure performed.")

class ExplanationOfBenefitItem(models.Model):
    _name = "hc.explanation.of.benefit.item"
    _description = "Explanation Of Benefit Item"

    explanation_of_benefit_id = fields.Many2one(
        comodel_name="hc.res.explanation.of.benefit",
        string="Explanation Of Benefit",
        help="Explanation Of Benefit associated with this Explanation Of Benefit Item.")
    sequence = fields.Integer(
        string="Sequence",
        required="True",
        help="Service instance.")
    care_team_link_id_ids = fields.One2many(
        comodel_name="hc.explanation.of.benefit.item.care.team.link.id",
        inverse_name="item_id",
        string="Care Team Link Ids",
        help="Applicable care team members.")
    diagnosis_link_id_ids = fields.One2many(
        comodel_name="hc.explanation.of.benefit.item.diagnosis.link.id",
        inverse_name="item_id",
        string="Diagnosis Link Ids",
        help="Applicable diagnoses.")
    procedure_link_id_ids = fields.One2many(
        comodel_name="hc.explanation.of.benefit.item.procedure.link.id",
        inverse_name="item_id",
        string="Procedure Link Ids",
        help="Applicable procedures.")
    information_link_id_ids = fields.One2many(
        comodel_name="hc.explanation.of.benefit.item.information.link.id",
        inverse_name="item_id",
        string="Information Link Ids",
        help="Applicable exception and supporting information.")
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
        help="Billing Code.")
    modifier_ids = fields.Many2many(
        comodel_name="hc.vs.claim.modifier",
        relation="explanation_of_benefit_item_modifier_rel",
        string="Modifiers",
        help="Service/Product billing modifiers.")
    program_code_ids = fields.Many2many(
        comodel_name="hc.vs.ex.program.code",
        relation="explanation_of_benefit_item_program_code_rel",
        string="Program Codes",
        help="Program specific reason for item inclusion.")
    serviced_type = fields.Selection(
        string="Serviced Type",
        selection=[
            ("date", "Date"),
            ("period", "Period")],
        help="Type of date or dates of Service.")
    serviced_name = fields.Char(
        string="Serviced",
        compute="_compute_serviced_name",
        store="True",
        help="Date or dates of Service.")
    serviced_date = fields.Date(
        string="Serviced Date",
        help="Code of date or dates of service.")
    serviced_start_date = fields.Datetime(
        string="Serviced Start Date",
        help="Start of the date or dates of service.")
    serviced_end_date = fields.Datetime(
        string="Serviced End Date",
        help="End of the date or dates of service.")
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
        comodel_name="hc.address",
        string="Location Address",
        help="Address of place of service.")
    location_location_id = fields.Many2one(
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
    net = fields.Float(
        string="Net",
        help="Total item cost.")
    udi_ids = fields.One2many(
        comodel_name="hc.explanation.of.benefit.item.udi",
        inverse_name="item_id",
        string="UDIs",
        help="Unique Device Identifier.")
    body_site_id = fields.Many2one(
        comodel_name="hc.vs.tooth",
        string="Body Site",
        help="Service Location.")
    sub_site_ids = fields.Many2many(
        comodel_name="hc.vs.surface",
        relation="explanation_of_benefit_item_sub_site_rel",
        string="Sub Sites",
        help="Service Sub-location.")
    note_number_ids = fields.One2many(
        comodel_name="hc.explanation.of.benefit.item.note.number",
        inverse_name="item_id",
        string="Note Numbers",
        help="List of note numbers which apply.")
    is_prosthesis = fields.Boolean(
        string="Prosthesis",
        help="Prosthetic details.")
    is_prosthesis_initial = fields.Boolean(
        string="Prosthesis Initial",
        help="Is this the initial service.")
    prosthesis_prior_date = fields.Date(
        string="Prosthesis Prior Date",
        help="Initial service Date.")
    prosthesis_prior_material_id = fields.Many2one(
        comodel_name="hc.vs.oral.prosthodontic.material",
        string="Prosthesis Prior Material",
        help="Prosthetic Material.")
    adjudication_ids = fields.One2many(
        comodel_name="hc.explanation.of.benefit.item.adjudication",
        inverse_name="item_id",
        string="Adjudications",
        help="Adjudication details.")
    detail_ids = fields.One2many(
        comodel_name="hc.explanation.of.benefit.item.detail",
        inverse_name="item_id",
        string="Details",
        help="Additional items.")

class ExplanationOfBenefitItemAdjudication(models.Model):
    _name = "hc.explanation.of.benefit.item.adjudication"
    _description = "Explanation Of Benefit Item Adjudication"

    item_id = fields.Many2one(
        comodel_name="hc.explanation.of.benefit.item",
        string="Item",
        help="Item associated with this Explanation Of Benefit Item Adjudication.")
    detail_id = fields.Many2one(
        comodel_name="hc.explanation.of.benefit.item.detail",
        string="Detail",
        help="Detail associated with this Explanation Of Benefit Item Adjudication.")
    sub_detail_id = fields.Many2one(
        comodel_name="hc.explanation.of.benefit.item.sub.detail",
        string="Sub Detail",
        help="Sub Detail associated with this Explanation Of Benefit Item Adjudication.")
    added_item_id = fields.Many2one(
        comodel_name="hc.explanation.of.benefit.added.item",
        string="Added Item",
        help="Added Item associated with this Explanation Of Benefit Item Adjudication.")
    added_items_detail_id = fields.Many2one(
        comodel_name="hc.explanation.of.benefit.added.items.detail",
        string="Added Items Detail",
        help="Added Items Detail associated with this Explanation Of Benefit Item Adjudication.")
    category_id = fields.Many2one(
        comodel_name="hc.vs.benefit.sub.category",
        string="Category",
        required="True",
        help="Adjudication category such as co-pay, eligible, benefit, etc..")
    reason_id = fields.Many2one(
        comodel_name="hc.vs.adjudication.reason",
        string="Reason",
        help="Adjudication reason.")
    amount = fields.Float(
        string="Amount",
        help="Monetary amount.")
    value = fields.Float(
        string="Value",
        help="Non-monitory value.")

class ExplanationOfBenefitItemDetail(models.Model):
    _name = "hc.explanation.of.benefit.item.detail"
    _description = "Explanation Of Benefit Item Detail"

    item_id = fields.Many2one(
        comodel_name="hc.explanation.of.benefit.item",
        string="Item",
        help="Item associated with this Explanation Of Benefit Item Detail.")
    sequence = fields.Integer(
        string="Sequence",
        required="True",
        help="Service instance.")
    type_id = fields.Many2one(
        comodel_name="hc.vs.act.invoice.group.code",
        string="Type", required="True",
        help="Group or type of product or service.")
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
        help="Billing Code.")
    modifier_ids = fields.Many2many(
        comodel_name="hc.vs.claim.modifier",
        relation="explanation_of_benefit_item_detail_modifier_rel",
        string="Modifiers",
        help="Service/Product billing modifiers.")
    program_code_ids = fields.Many2many(
        comodel_name="hc.vs.ex.program.code",
        relation="explanation_of_benefit_item_detail_program_code_rel",
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
    net = fields.Float(
        string="Net",
        help="Total additional item cost.")
    udi_ids = fields.One2many(
        comodel_name="hc.explanation.of.benefit.item.detail.udi",
        inverse_name="detail_id",
        string="UDIs",
        help="Unique Device Identifier.")
    note_number_ids = fields.One2many(
        comodel_name="hc.explanation.of.benefit.item.detail.note.number",
        inverse_name="detail_id",
        string="Note Numbers",
        help="List of note numbers which apply.")
    adjudication_ids = fields.One2many(
        comodel_name="hc.explanation.of.benefit.item.adjudication",
        inverse_name="detail_id",
        string="Adjudications",
        help="Detail adjudication.")
    sub_detail_ids = fields.One2many(
        comodel_name="hc.explanation.of.benefit.item.sub.detail",
        inverse_name="detail_id",
        string="Sub Details",
        help="Additional items.")

class ExplanationOfBenefitItemSubDetail(models.Model):
    _name = "hc.explanation.of.benefit.item.sub.detail"
    _description = "Explanation Of Benefit Item Sub Detail"

    detail_id = fields.Many2one(
        comodel_name="hc.explanation.of.benefit.item.sub.detail",
        string="Detail",
        help="Detail associated with this Explanation Of Benefit Item Detail Sub Detail.")
    sequence = fields.Integer(
        string="Sequence",
        required="True",
        help="Service instance.")
    type_id = fields.Many2one(
        comodel_name="hc.vs.act.invoice.group.code",
        string="Type",
        required="True",
        help="Type of product or service.")
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
        help="Billing Code.")
    modifier_ids = fields.Many2many(
        comodel_name="hc.vs.claim.modifier",
        relation="explanation_of_benefit_item_detail_sub_detail_modifier_rel",
        string="Modifiers",
        help="Service/Product billing modifiers.")
    program_code_ids = fields.Many2many(
        comodel_name="hc.vs.ex.program.code",
        relation="explanation_of_benefit_item_detail_sub_detail_program_code_rel",
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
    net = fields.Float(
        string="Net",
        help="Net additional item cost.")
    udi_ids = fields.One2many(
        comodel_name="hc.explanation.of.benefit.item.sub.detail.udi",
        inverse_name="sub_detail_id",
        string="UDIs",
        help="Unique Device Identifier.")
    note_number_ids = fields.One2many(
        comodel_name="hc.explanation.of.benefit.item.sub.detail.note.number",
        inverse_name="sub_detail_id",
        string="Note Numbers",
        help="List of note numbers which apply.")
    adjudication_ids = fields.One2many(
        comodel_name="hc.explanation.of.benefit.item.adjudication",
        inverse_name="sub_detail_id",
        string="Adjudications",
        help="Subdetail adjudication.")

class ExplanationOfBenefitAddedItem(models.Model):
    _name = "hc.explanation.of.benefit.added.item"
    _description = "Explanation Of Benefit Added Item"

    explanation_of_benefit_id = fields.Many2one(
        comodel_name="hc.res.explanation.of.benefit",
        string="Explanation Of Benefit",
        help="Explanation Of Benefit associated with this Explanation Of Benefit Added Item.")
    sequence_link_id_ids = fields.One2many(
        comodel_name="hc.explanation.of.benefit.added.item.sequence.link.id",
        inverse_name="added_item_id",
        string="Sequence Link Ids",
        help="Service instances.")
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
        help="Billing Code.")
    modifier_ids = fields.Many2many(
        comodel_name="hc.vs.claim.modifier",
        relation="explanation_of_benefit_added_item_modifier_rel",
        string="Modifiers",
        help="Service/Product billing modifiers.")
    fee = fields.Float(
        string="Fee",
        help="Professional fee or Product charge.")
    note_number_ids = fields.One2many(
        comodel_name="hc.explanation.of.benefit.added.item.note.number",
        inverse_name="added_item_id",
        string="Note Numbers",
        help="List of note numbers which apply.")
    adjudication_ids = fields.One2many(
        comodel_name="hc.explanation.of.benefit.item.adjudication",
        inverse_name="added_item_id",
        string="Adjudications",
        help="Added items adjudication.")
    detail_ids = fields.One2many(
        comodel_name="hc.explanation.of.benefit.added.items.detail",
        inverse_name="added_item_id",
        string="Details",
        help="Added items details.")

class ExplanationOfBenefitAddedItemsDetail(models.Model):
    _name = "hc.explanation.of.benefit.added.items.detail"
    _description = "Explanation Of Benefit Added Items Detail"

    added_item_id = fields.Many2one(
        comodel_name="hc.explanation.of.benefit.added.item",
        string="Added Item",
        help="Added Item associated with this Explanation Of Benefit Added Items Detail.")
    revenue_id = fields.Many2one(
        comodel_name="hc.vs.ex.revenue.center",
        string="Revenue", help="Revenue or cost center code.")
    category_id = fields.Many2one(
        comodel_name="hc.vs.benefit.sub.category",
        string="Category",
        help="Type of service or product.")
    service_id = fields.Many2one(
        comodel_name="hc.vs.service.uscls",
        string="Service",
        help="Billing Code.")
    modifier_ids = fields.Many2many(
        comodel_name="hc.vs.claim.modifier",
        relation="eob_added_item_added_items_detail_modifier_rel",
        string="Modifiers",
        help="Service/Product billing modifiers.")
    fee = fields.Float(
        string="Fee",
        help="Professional fee or Product charge.")
    note_number_ids = fields.One2many(
        comodel_name="hc.explanation.of.benefit.added.items.detail.note.number",
        inverse_name="added_items_detail_id",
        string="Note Numbers",
        help="List of note numbers which apply.")
    adjudication_ids = fields.One2many(
        comodel_name="hc.explanation.of.benefit.item.adjudication",
        inverse_name="added_items_detail_id",
        string="Adjudications",
        help="Added items detail adjudication.")

class ExplanationOfBenefitNote(models.Model):
    _name = "hc.explanation.of.benefit.note"
    _description = "Explanation Of Benefit Note"

    explanation_of_benefit_id = fields.Many2one(
        comodel_name="hc.res.explanation.of.benefit",
        string="Explanation Of Benefit",
        help="Explanation Of Benefit associated with this Explanation Of Benefit Note.")
    number = fields.Integer(
        string="Number",
        help="Note Number for this note.")
    type = fields.Selection(
        string="Note Type",
        selection=[
            ("display", "Display"),
            ("print", "Print"),
            ("printoper", "Printoper")],
        help="The note purpose: Print/Display.")
    text = fields.Text(
        string="Text",
        help="Note explanatory text.")
    language_id = fields.Many2one(
        comodel_name="hc.vs.language",
        string="Language",
        help="Language.")

class ExplanationOfBenefitBalance(models.Model):
    _name = "hc.explanation.of.benefit.balance"
    _description = "Explanation Of Benefit Balance"

    explanation_of_benefit_id = fields.Many2one(
        comodel_name="hc.res.explanation.of.benefit",
        string="Explanation Of Benefit",
        help="Explanation Of Benefit associated with this Explanation Of Benefit Benefit Balance.")
    category_id = fields.Many2one(
        comodel_name="hc.vs.benefit.sub.category",
        string="Category",
        required="True",
        help="Benefit Category.")
    sub_category_id = fields.Many2one(
        comodel_name="hc.vs.benefit.sub.category",
        string="Sub Category",
        help="Benefit SubCategory.")
    is_excluded = fields.Boolean(
        string="Excluded",
        help="Excluded from the plan.")
    name = fields.Char(
        string="Name",
        help="Short name for the benefit.")
    description = fields.Text(
        string="Description",
        help="Description of the benefit.")
    network_id = fields.Many2one(
        comodel_name="hc.vs.benefit.network",
        string="Network",
        help="In or out of network.")
    unit_id = fields.Many2one(
        comodel_name="hc.vs.benefit.unit",
        string="Unit",
        help="Individual or family.")
    term_id = fields.Many2one(
        comodel_name="hc.vs.benefit.term",
        string="Term",
        help="Annual or lifetime.")
    financial_ids = fields.One2many(
        comodel_name="hc.explanation.of.benefit.balance.benefit",
        inverse_name="benefit_balance_id",
        string="Financials",
        help="Benefit Summary.")

class ExplanationOfBenefitBalanceBenefit(models.Model):
    _name = "hc.explanation.of.benefit.balance.benefit"
    _description = "Explanation Of Benefit Balance Benefit"

    benefit_balance_id = fields.Many2one(
        comodel_name="hc.explanation.of.benefit.balance",
        string="Benefit Balance",
        help="Benefit Balance associated with this Explanation Of Benefit Benefit.")
    type_id = fields.Many2one(
        comodel_name="hc.vs.benefit.type",
        string="Type",
        required="True",
        help="Deductable, visits, benefit amount.")
    allowed_type = fields.Selection(
        string="Allowed Type",
        selection=[
            ("unsigned_int", "Unsigned Int"),
            ("string", "String"),
            ("money", "Money")],
        help="Type of benefits allowed.")
    allowed_name = fields.Char(
        string="Allowed",
        compute="_compute_allowed_name",
        store="True",
        help="Benefits allowed.")
    allowed_unsigned_int = fields.Integer(
        string="Allowed Unsigned Int",
        help="Code of benefits allowed.")
    allowed_string = fields.Char(
        string="Allowed String",
        help="String of content of this set of documents.")
    allowed_money = fields.Float(
        string="Allowed Money",
        help="Money content of this set of documents.")
    used_type = fields.Selection(
        string="Used Type",
        selection=[
            ("unsigned Int", "Unsigned Int"),
            ("money", "Money")],
        help="Type of benefits used.")
    used_name = fields.Char(
        string="Used",
        compute="_compute_used_name",
        store="True",
        help="Benefits used.")
    used_unsigned_int = fields.Integer(
        string="Used Unsigned Int",
        help="Code of benefits used.")
    used_money = fields.Float(
        string="Used Money",
        help="Money content of this set of documents.")

class ExplanationOfBenefitIdentifier(models.Model):
    _name = "hc.explanation.of.benefit.identifier"
    _description = "Explanation Of Benefit Identifier"
    _inherit = ["hc.basic.association", "hc.identifier"]

    explanation_of_benefit_id = fields.Many2one(
        comodel_name="hc.res.explanation.of.benefit",
        string="Explanation Of Benefit",
        help="Explanation Of Benefit associated with this Explanation Of Benefit Identifier.")

class ExplanationOfBenefitRelatedClaimReference(models.Model):
    _name = "hc.explanation.of.benefit.related.claim.reference"
    _description = "Explanation Of Benefit Related Claim Reference"
    _inherit = ["hc.basic.association"]

    explanation_of_benefit_id = fields.Many2one(
        comodel_name="hc.res.explanation.of.benefit",
        string="Explanation Of Benefit",
        help="Explanation Of Benefit associated with this Explanation Of Benefit Related Claim Reference.")

class ExplanationOfBenefitPayeePartyIdentifier(models.Model):
    _name = "hc.explanation.of.benefit.payee.party.identifier"
    _description = "Explanation Of Benefit Payee Party Identifier"
    _inherit = ["hc.basic.association", "hc.identifier"]

class ExplanationOfBenefitInsurancePreAuthRef(models.Model):
    _name = "hc.explanation.of.benefit.insurance.pre.auth.ref"
    _description = "Explanation Of Benefit Insurance Pre Auth Ref"
    _inherit = ["hc.basic.association"]

    explanation_of_benefit_id = fields.Many2one(
        comodel_name="hc.res.explanation.of.benefit",
        string="Explanation Of Benefit",
        help="Explanation Of Benefit associated with this Explanation Of Benefit Insurance Pre Auth Ref.")
    insurance_pre_auth_ref = fields.Char(
        string="Insurance Pre Auth Ref",
        help="Insurance Pre Auth Ref associated with this Explanation Of Benefit Insurance Pre Auth Ref.")

class ExplanationOfBenefitItemCareTeamLinkId(models.Model):
    _name = "hc.explanation.of.benefit.item.care.team.link.id"
    _description = "Explanation Of Benefit Item Care Team Link Id"
    _inherit = ["hc.basic.association"]

    item_id = fields.Many2one(
        comodel_name="hc.explanation.of.benefit.item",
        string="Item",
        help="Item associated with this Explanation Of Benefit Item Care Team Link Id.")
    care_team_link_id = fields.Integer(
        string="Care Team Link Id",
        help="Care Team Link Id associated with this Explanation Of Benefit Item Care Team Link Id.")

class ExplanationOfBenefitItemDiagnosisLinkId(models.Model):
    _name = "hc.explanation.of.benefit.item.diagnosis.link.id"
    _description = "Explanation Of Benefit Item Diagnosis Link Id"
    _inherit = ["hc.basic.association"]

    item_id = fields.Many2one(
        comodel_name="hc.explanation.of.benefit.item",
        string="Item",
        help="Item associated with this Explanation Of Benefit Item Diagnosis Link Id.")
    diagnosis_link_id = fields.Integer(
        string="Diagnosis Link Id",
        help="Diagnosis Link Id associated with this Explanation Of Benefit Item Diagnosis Link Id.")

class ExplanationOfBenefitItemProcedureLinkId(models.Model):
    _name = "hc.explanation.of.benefit.item.procedure.link.id"
    _description = "Explanation Of Benefit Item Procedure Link Id"
    _inherit = ["hc.basic.association"]

    item_id = fields.Many2one(
        comodel_name="hc.explanation.of.benefit.item",
        string="Item",
        help="Item associated with this Explanation Of Benefit Item Procedure Link Id.")
    procedure_link_id = fields.Integer(
        string="Procedure Link Id",
        help="Procedure Link Id associated with this Explanation Of Benefit Item Procedure Link Id.")

class ExplanationOfBenefitItemInformationLinkId(models.Model):
    _name = "hc.explanation.of.benefit.item.information.link.id"
    _description = "Explanation Of Benefit Item Information Link Id"
    _inherit = ["hc.basic.association"]

    item_id = fields.Many2one(
        comodel_name="hc.explanation.of.benefit.item",
        string="Item",
        help="Item associated with this Explanation Of Benefit Item Information Link Id.")
    information_link_id = fields.Integer(
        string="Information Link Id",
        help="Information Link Id associated with this Explanation Of Benefit Item Information Link Id.")

class ExplanationOfBenefitItemUDI(models.Model):
    _name = "hc.explanation.of.benefit.item.udi"
    _description = "Explanation Of Benefit Item UDI"
    _inherit = ["hc.basic.association"]

    item_id = fields.Many2one(
        comodel_name="hc.explanation.of.benefit.item",
        string="Item",
        help="Item associated with this Explanation Of Benefit Item UDI.")
    udi_id = fields.Many2one(
        comodel_name="hc.res.device",
        string="UDI",
        help="Unique Device Identifier.")

class ExplanationOfBenefitItemNoteNumber(models.Model):
    _name = "hc.explanation.of.benefit.item.note.number"
    _description = "Explanation Of Benefit Item Note Number"
    _inherit = ["hc.basic.association"]

    item_id = fields.Many2one(
        comodel_name="hc.explanation.of.benefit.item",
        string="Item",
        help="Item associated with this Explanation Of Benefit Item Note Number.")
    note_number = fields.Integer(
        string="Note Number",
        help="Note Number associated with this Explanation Of Benefit Item Note Number.")

class ExplanationOfBenefitItemDetailUDI(models.Model):
    _name = "hc.explanation.of.benefit.item.detail.udi"
    _description = "Explanation Of Benefit Item Detail UDI"
    _inherit = ["hc.basic.association"]

    detail_id = fields.Many2one(
        comodel_name="hc.explanation.of.benefit.item.detail",
        string="Detail",
        help="Detail associated with this Explanation Of Benefit Item Detail UDI.")
    udi_id = fields.Many2one(
        comodel_name="hc.res.device",
        string="UDI",
        help="Unique Device Identifier.")

class ExplanationOfBenefitItemDetailNoteNumber(models.Model):
    _name = "hc.explanation.of.benefit.item.detail.note.number"
    _description = "Explanation Of Benefit Item Detail Note Number"
    _inherit = ["hc.basic.association"]

    detail_id = fields.Many2one(
        comodel_name="hc.explanation.of.benefit.item.detail",
        string="Detail",
        help="Detail associated with this Explanation Of Benefit Item Detail Note Number.")
    note_number = fields.Integer(
        string="Note Number",
        help="Note Number associated with this Explanation Of Benefit Item Detail Note Number.")

class ExplanationOfBenefitItemSubDetailUDI(models.Model):
    _name = "hc.explanation.of.benefit.item.sub.detail.udi"
    _description = "Explanation Of Benefit Item Sub Detail UDI"
    _inherit = ["hc.basic.association"]

    sub_detail_id = fields.Many2one(
        comodel_name="hc.explanation.of.benefit.item.sub.detail",
        string="Sub Detail",
        help="Sub Detail associated with this Explanation Of Benefit Item Detail Sub Detail Udi.")
    udi_id = fields.Many2one(
        comodel_name="hc.res.device",
        string="UDI",
        help="Unique Device Identifier.")

class ExplanationOfBenefitItemSubDetailNoteNumber(models.Model):
    _name = "hc.explanation.of.benefit.item.sub.detail.note.number"
    _description = "Explanation Of Benefit Item Sub Detail Note Number"
    _inherit = ["hc.basic.association"]

    sub_detail_id = fields.Many2one(
        comodel_name="hc.explanation.of.benefit.item.sub.detail",
        string="Sub Detail",
        help="Sub Detail associated with this Explanation Of Benefit Item Detail Sub Detail Note Number.")
    note_number = fields.Integer(
        string="Note Number",
        help="Note Number associated with this Explanation Of Benefit Item Detail Sub Detail Note Number.")

class ExplanationOfBenefitAddedItemSequenceLinkId(models.Model):
    _name = "hc.explanation.of.benefit.added.item.sequence.link.id"
    _description = "Explanation Of Benefit Added Item Sequence Link Id"
    _inherit = ["hc.basic.association"]

    added_item_id = fields.Many2one(
        comodel_name="hc.explanation.of.benefit.added.item",
        string="Added Item",
        help="Added Item associated with this Explanation Of Benefit Added Item Sequence Link Id.")
    sequence_link_id = fields.Integer(
        string="Sequence Link Id",
        help="Sequence Link Id associated with this Explanation Of Benefit Added Item Sequence Link Id.")

class ExplanationOfBenefitAddedItemNoteNumber(models.Model):
    _name = "hc.explanation.of.benefit.added.item.note.number"
    _description = "Explanation Of Benefit Added Item Note Number"
    _inherit = ["hc.basic.association"]

    added_item_id = fields.Many2one(
        comodel_name="hc.explanation.of.benefit.added.item",
        string="Added Item",
        help="Added Item associated with this Explanation Of Benefit Added Item Note Number.")
    note_number = fields.Integer(
        string="Note Number",
        help="Note Number associated with this Explanation Of Benefit Added Item Note Number.")

class ExplanationOfBenefitAddedItemsDetailNoteNumber(models.Model):
    _name = "hc.explanation.of.benefit.added.items.detail.note.number"
    _description = "Explanation Of Benefit Added Items Detail Note Number"
    _inherit = ["hc.basic.association"]

    added_items_detail_id = fields.Many2one(
        comodel_name="hc.explanation.of.benefit.added.items.detail",
        string="Added Items Detail",
        help="Added Items Detail associated with this Explanation Of Benefit Added Items Detail Note Number.")
    note_number = fields.Integer(
        string="Note Number",
        help="Note Number associated with this Explanation Of Benefit Added Items Detail Note Number.")

class ExplanationOfBenefitPaymentIdentifier(models.Model):
    _name = "hc.explanation.of.benefit.payment.identifier"
    _description = "Explanation Of Benefit Payment Identifier"
    _inherit = ["hc.basic.association", "hc.identifier"]

class ActInvoiceGroupCode(models.Model):
    _name = "hc.vs.act.invoice.group.code"
    _description = "Act Invoice Group Code"
    _inherit = ["hc.value.set.contains"]

class BenefitType(models.Model):
    _name = "hc.vs.benefit.type"
    _description = "Benefit Type"
    _inherit = ["hc.value.set.contains"]

class ClaimType(models.Model):
    _name = "hc.vs.claim.type"
    _description = "Claim Type"
    _inherit = ["hc.value.set.contains"]
