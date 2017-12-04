# -*- coding: utf-8 -*-

from openerp import models, fields, api
from datetime import datetime
from openerp.tools import DEFAULT_SERVER_DATETIME_FORMAT as DTF

class Claim(models.Model):
    _name = "hc.res.claim"
    _description = "Claim"
    _inherit = ["hc.domain.resource"]
    _rec_name = "name"

    name = fields.Char(
        string="Name",
        required="True",
        help="Text representation of the claim. Claim Number + Patient Name + Created Date.")
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
    type_id = fields.Many2one(
        comodel_name="hc.vs.claim.type",
        string="Type",
        required="True",
        help="The category of claim, eg, oral, pharmacy, vision, institutional, professional.")
    sub_type_ids = fields.Many2many(
        comodel_name="hc.vs.claim.sub.type",
        relation="claim_sub_type_rel",
        string="Sub Types",
        help="Finer grained claim type information.")
    use = fields.Selection(
        string="Use",
        selection=[
            ("complete", "Complete"),
            ("proposed", "Proposed"),
            ("exploratory", "Exploratory"),
            ("other", "Other")],
        help="Complete (Bill or Claim), Proposed (Pre-Authorization), Exploratory (Pre-determination).")
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
        string="Created Date",
        help="Creation date.")
    enterer_id = fields.Many2one(
        comodel_name="hc.res.practitioner",
        string="Enterer",
        help="Author.")
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
    priority_id = fields.Many2one(
        comodel_name="hc.vs.process.priority",
        string="Priority",
        help="Desired processing priority.")
    funds_reserve_id = fields.Many2one(
        comodel_name="hc.vs.funds.reserve",
        string="Funds Reserve",
        help="Funds requested to be reserved.")
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
    facility_id = fields.Many2one(
        comodel_name="hc.res.location",
        string="Facility",
        help="Servicing Facility.")
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
    total = fields.Float(
        string="Total Cost",
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
    care_team_ids = fields.One2many(
        comodel_name="hc.claim.care.team",
        inverse_name="claim_id",
        string="Care Teams",
        help="Members of the care team.")
    information_ids = fields.One2many(
        comodel_name="hc.claim.information",
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
    insurance_ids = fields.One2many(
        comodel_name="hc.claim.insurance",
        inverse_name="claim_id",
        string="Insurance",
        help="Insurance or medical plan.")
    accident_ids = fields.One2many(
        comodel_name="hc.claim.accident",
        inverse_name="claim_id",
        string="Accidents",
        help="Details about an accident.")
    # missing_teeth_ids = fields.One2many(
    #     comodel_name="hc.claim.missing.teeth",
    #     inverse_name="claim_id",
    #     string="Missing Teeth",
    #     help="Only if type = oral.")
    item_ids = fields.One2many(
        comodel_name="hc.claim.item",
        inverse_name="claim_id",
        string="Items",
        help="Goods and Services.")

    @api.depends('prescription_type')
    def _compute_prescription_name(self):
        for hc_res_claim in self:
            if hc_res_claim.prescription_type == 'medication_request':
                hc_res_claim.prescription_name = hc_res_claim.prescription_medication_request_id.name
            elif hc_res_claim.prescription_type == 'vision_prescription':
                hc_res_claim.prescription_name = hc_res_claim.prescription_vision_prescription_id.name

    @api.model
    def create(self, vals):
        status_history_obj = self.env['hc.structure.map.status.history']
        res = super(StructureMap, self).create(vals)
        if vals and vals.get('status_id'):
            status_history_vals = {
                'structure_map_id': res.id,
                'status': res.status,
                'start_date': datetime.today()
                }
            status_history_obj.create(status_history_vals)
        return res

    @api.multi
    def write(self, vals):
        status_history_obj = self.env['hc.structure.map.status.history']
        res = super(StructureMap, self).write(vals)
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
                status_history_vals = {
                    'structure_map_id': self.id,
                    'status': vals.get('status'),
                    'start_date': datetime.today()
                    }
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

    @api.depends('party_type')
    def _compute_party_name(self):
        for hc_claim_payee in self:
            if hc_claim_payee.party_type == 'practitioner':
                hc_claim_payee.party_name = hc_claim_payee.party_practitioner_id.name
            elif hc_claim_payee.party_type == 'organization':
                hc_claim_payee.party_name = hc_claim_payee.party_organization_id.name
            elif hc_claim_payee.party_type == 'patient':
                hc_claim_payee.party_name = hc_claim_payee.party_patient_id.name
            elif hc_claim_payee.party_type == 'related_person':
                hc_claim_payee.party_name = hc_claim_payee.party_related_person_id.name

class ClaimCareTeam(models.Model):
    _name = "hc.claim.care.team"
    _description = "Claim Care Team"

    claim_id = fields.Many2one(
        comodel_name="hc.res.claim",
        string="Claim",
        help="Claim associated with this Claim Care Team.")
    sequence = fields.Integer(
        string="Sequence",
        required="True",
        help="Number to covey order of careTeam.")
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

    @api.depends('provider_type')
    def _compute_provider_name(self):
        for hc_claim_care_team in self:
            if hc_claim_care_team.provider_type == 'practitioner':
                hc_claim_care_team.provider_name = hc_claim_care_team.provider_practitioner_id.name
            elif hc_claim_care_team.provider_type == 'organization':
                hc_claim_care_team.provider_name = hc_claim_care_team.provider_organization_id.name

class ClaimInformation(models.Model):
    _name = "hc.claim.information"
    _description = "Claim Information"

    claim_id = fields.Many2one(
        comodel_name="hc.res.claim",
        string="Claim",
        help="Claim associated with this Claim Special Condition.")
    sequence = fields.Integer(
        string="Sequence",
        required="True",
        help="Information instance identifier.")
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
            ("quantity", "Quantity"),
            ("attachment", "Attachment"),
            ("reference", "Reference")],
        help="Type of Additional Data or supporting information.")
    value_name = fields.Char(
        string="Value",
        compute="_compute_value_name",
        store="True",
        help="Additional Data or supporting information.")
    value_string = fields.Char(
        string="Value String",
        help="String of Additional Data or supporting information.")
    value_quantity = fields.Float(
        string="Value Quantity",
        help="Quantity of Additional Data or supporting information.")
    value_quantity_uom_id = fields.Many2one(
        comodel_name="product.uom",
        string="Value Quantity UOM",
        help="Value Quantity unit of measure.")
    value_attachment_id = fields.Many2one(
        comodel_name="hc.attachment",
        string="Value Attachment",
        help="Attachment of Additional Data or supporting information.")
    value_reference_type = fields.Char(
        string="Value Reference Type",
        compute="_compute_value_reference_type",
        store="True",
        help="Type of additional data or supporting information.")
    value_reference_name = fields.Reference(
        string="Value Reference",
        selection="_reference_models",
        help="Additional Data or supporting information.")
    reason_id = fields.Many2one(
        comodel_name="hc.vs.claim.information.reason",
        string="Reason",
        help="Reason associated with the information.")

    @api.depends('timing_type')
    def _compute_timing_name(self):
        for hc_claim_information in self:
            if hc_claim_information.timing_type == 'date':
                hc_claim_information.timing_name = hc_claim_information.timing_date
            elif hc_claim_information.timing_type == 'period':
                hc_claim_information.timing_name = "Between " + str(hc_claim_information.timing_start_date) + " and" + str(hc_claim_information.timing_end_date)

    @api.model
    def _reference_models(self):
        models = self.env['ir.model'].search([('state', '!=', 'manual')])
        return [(model.model, model.name)
            for model in models
                if model.model.startswith('hc.res')]

    @api.depends('value_reference_name')
    def _compute_value_reference_type(self):
        for this in self:
            if this.value_reference_name:
                this.value_reference_type = this.value_reference_name._description

    @api.depends('value_type')
    def _compute_value_name(self):
        for hc_claim_information in self:
            if hc_claim_information.value_type == 'string':
                hc_claim_information.value_name = hc_claim_information.value_string
            elif hc_claim_information.value_type == 'quantity':
                hc_claim_information.value_name = str(hc_claim_information.value_quantity) + " " + str(hc_claim_information.value_quantity_uom_id.name)
            elif hc_claim_information.value_type == 'attachment':
                hc_claim_information.value_name = hc_claim_information.value_attachment_id.name
            elif hc_claim_information.value_type == 'reference':
                hc_claim_information.value_name = hc_claim_information.value_reference_name

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
    diagnosis_type = fields.Selection(
        string="Diagnosis Type",
        selection=[
            ("code", "Code"),
            ("condition", "Condition")],
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
        help="Code of patient's diagnosis.")
    diagnosis_condition_id = fields.Many2one(
        comodel_name="hc.res.condition",
        string="Diagnosis Condition",
        required="True",
        help="Condition of Patient's diagnosis.")
    type_ids = fields.Many2many(
        comodel_name="hc.vs.diagnosis.type",
        relation="claim_diagnosis_type_rel",
        string="Types",
        help="Type of Diagnosis.")
    package_code_id = fields.Many2one(
        comodel_name="hc.vs.diagnosis.package.code",
        string="Package Code",
        help="Package billing code.")

    @api.depends('diagnosis_type')
    def _compute_diagnosis_name(self):
        for hc_claim_diagnosis in self:
            if hc_claim_diagnosis.diagnosis_type == 'code':
                hc_claim_diagnosis.diagnosis_name = hc_claim_diagnosis.diagnosis_code_id.name
            elif hc_claim_diagnosis.diagnosis_type == 'condition':
                hc_claim_diagnosis.diagnosis_name = hc_claim_diagnosis.diagnosis_condition_id.name

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

    @api.depends('procedure_type')
    def _compute_procedure_name(self):
        for hc_claim_procedure in self:
            if hc_claim_procedure.procedure_type == 'code':
                hc_claim_procedure.procedure_name = hc_claim_procedure.procedure_code_id.name
            elif hc_claim_procedure.procedure_type == 'procedure':
                hc_claim_procedure.procedure_name = hc_claim_procedure.procedure_procedure_id.name

class ClaimInsurance(models.Model):
    _name = "hc.claim.insurance"
    _description = "Claim Insurance"

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
    identifier_id = fields.Many2one(
        comodel_name="hc.claim.insurance.identifier",
        string="Identifier",
        help="Claim number.")
    coverage_id = fields.Many2one(
        comodel_name="hc.res.coverage",
        string="Coverage",
        required="True",
        help="Insurance information.")
    business_arrangement = fields.Char(
        string="Business Arrangement",
        help="Business agreement.")
    pre_auth_ref_ids = fields.One2many(
        comodel_name="hc.claim.insurance.pre.auth.ref",
        inverse_name="insurance_id",
        string="Pre Auth Refs",
        help="Pre-Authorization/Determination Reference.")
    # claim_response_id = fields.Many2one(
    #     comodel_name="hc.res.claim.response",
    #     string="Claim Response",
    #     help="Adjudication results.")

class ClaimAccident(models.Model):
    _name = "hc.claim.accident"
    _description = "Claim Accident"

    claim_id = fields.Many2one(
        comodel_name="hc.res.claim",
        string="Claim",
        help="Claim associated with this Claim Accident.")
    date = fields.Date(
        string="Date",
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

    @api.depends('location_type')
    def _compute_location_name(self):
        for hc_claim_accident in self:
            if hc_claim_accident.location_type == 'address':
                hc_claim_accident.location_name = hc_claim_accident.location_address_id.text
            elif hc_claim_accident.location_type == 'location':
                hc_claim_accident.location_name = hc_claim_accident.location_id.name

# class ClaimMissingTeeth(models.Model):
#     _name = "hc.claim.missing.teeth"
#     _description = "Claim Missing Teeth"

#     claim_id = fields.Many2one(
#         comodel_name="hc.res.claim",
#         string="Claim",
#         help="Claim associated with this Claim Missing Teeth.")
#     tooth_id = fields.Many2one(
#         comodel_name="hc.vs.teeth",
#         string="Tooth",
#         required="True",
#         help="Tooth Code.")
#     reason_id = fields.Many2one(
#         comodel_name="hc.vs.missing.tooth.reason",
#         string="Reason",
#         help="Reason for missing.")
#     extraction_date = fields.Date(
#         string="Extraction Date",
#         help="Date of Extraction.")

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
    care_team_link_id_ids = fields.One2many(
        comodel_name="hc.claim.item.care.team.link.id",
        inverse_name="item_id",
        string="Care Team Link Ids",
        help="Applicable careTeam members.")
    diagnosis_link_id_ids = fields.One2many(
        comodel_name="hc.claim.item.diagnosis.link.id",
        inverse_name="item_id",
        string="Diagnosis Link Ids",
        help="Applicable diagnoses.")
    procedure_link_id_ids = fields.One2many(
        comodel_name="hc.claim.item.procedure.link.id",
        inverse_name="item_id",
        string="Procedure Link Ids",
        help="Applicable procedures.")
    information_link_id_ids = fields.One2many(
        comodel_name="hc.claim.item.information.link.id",
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
    net = fields.Float(
        string="Net",
        help="Total item cost.")
    udi_ids = fields.One2many(
        comodel_name="hc.claim.item.udi",
        inverse_name="item_id",
        string="UDIs",
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
    encounter_ids = fields.One2many(
        comodel_name="hc.claim.item.encounter",
        inverse_name="item_id",
        string="Encounters",
        help="Encounters related to this billed item.")
    detail_ids = fields.One2many(
        comodel_name="hc.claim.item.detail",
        inverse_name="item_id",
        string="Details",
        help="Additional items.")
    # prosthesis_ids = fields.One2many(
    #     comodel_name="hc.claim.item.prosthesis",
    #     inverse_name="item_id",
    #     string="Prosthesis",
    #     help="Prosthetic details.")

    @api.depends('serviced_type')
    def _compute_serviced_name(self):
        for hc_claim_item in self:
            if hc_claim_item.serviced_type == 'date':
                hc_claim_item.serviced_name = hc_claim_item.serviced_date
            elif hc_claim_item.serviced_type == 'period':
                hc_claim_item.serviced_name = "Between " + str(hc_claim_item.serviced_start_date) + " and" + str(hc_claim_item.serviced_end_date)

    @api.depends('location_type')
    def _compute_location_name(self):
        for hc_claim_diagnosis in self:
            if hc_claim_diagnosis.location_type == 'code':
                hc_claim_diagnosis.location_name = hc_claim_diagnosis.location_code_id.name
            elif hc_claim_diagnosis.location_type == 'address':
                hc_claim_diagnosis.location_name = hc_claim_diagnosis.location_address_id.text
            elif hc_claim_diagnosis.location_type == 'location':
                hc_claim_diagnosis.location_name = hc_claim_diagnosis.location_id.name

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
    # points = fields.Float(
    #     string="Points",
    #     help="Difficulty scaling factor.")
    net = fields.Float(
        string="Net",
        help="Total additional item cost.")
    udi_ids = fields.One2many(
        comodel_name="hc.claim.item.detail.udi",
        inverse_name="detail_id",
        string="UDIs",
        help="Unique Device Identifier.")
    sub_detail_ids = fields.One2many(
        comodel_name="hc.claim.item.detail.sub.detail",
        inverse_name="detail_id",
        string="Sub Details",
        help="Additional items.")

class ClaimItemDetailUDI(models.Model):
    _name = "hc.claim.item.detail.udi"
    _description = "Claim Item Detail UDI"
    _inherit = ["hc.basic.association"]

    detail_id = fields.Many2one(
        comodel_name="hc.claim.item.detail",
        string="Detail",
        help="Goods and Services.")
    udi_id = fields.Many2one(
        comodel_name="hc.res.device",
        string="UDI",
        help="UDI associated with this Claim Item Detail UDI.")

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
    net = fields.Float(
        string="Net",
        help="Net additional item cost.")
    udi_ids = fields.One2many(
        comodel_name="hc.claim.item.detail.sub.detail.udi",
        inverse_name="sub_detail_id",
        string="UDIs",
        help="Unique Device Identifier.")

class ClaimItemDetailSubDetailUDI(models.Model):
    _name = "hc.claim.item.detail.sub.detail.udi"
    _description = "Claim Item Detail Sub Detail UDI"
    _inherit = ["hc.basic.association"]

    sub_detail_id = fields.Many2one(
        comodel_name="hc.claim.item.detail.sub.detail",
        string="Sub Detail",
        help="Goods and Services.")
    udi_id = fields.Many2one(
        comodel_name="hc.res.device",
        string="UDI",
        help="UDI associated with this Claim Item Detail Sub Detail UDI.")

# class ClaimItemProsthesis(models.Model):
#     _name = "hc.claim.item.prosthesis"
#     _description = "Claim Item Prosthesis"

#     item_id = fields.Many2one(
#         comodel_name="hc.claim.item",
#         string="Item",
#         help="Goods and Services.")
#     is_initial = fields.Boolean(
#         string="Initial",
#         help="Is this the initial service.")
#     prior_date = fields.Date(
#         string="Prior Date",
#         help="Initial service Date.")
#     prior_material_id = fields.Many2one(
#         comodel_name="hc.vs.oral.prosthodontic.material",
#         string="Prior Material",
#         help="Prosthetic Material.")

class ClaimIdentifier(models.Model):
    _name = "hc.claim.identifier"
    _description = "Claim Identifier"
    _inherit = ["hc.basic.association", "hc.identifier", "hc.identifier.use"]

    claim_id = fields.Many2one(
        comodel_name="hc.res.claim",
        string="Claim",
        help="Claim associated with this Claim Identifier.")
    extension_ids = fields.One2many(
        comodel_name="hc.claim.identifier.extension",
        inverse_name="identifier_id",
        string="Extensions",
        help="Additional Content defined by implementations.")

class ClaimIdentifierExtension(models.Model):
    _name = "hc.claim.identifier.extension"
    _description = "Claim Identifier Extension"
    _inherit = ["hc.basic.association", "hc.extension"]

    identifier_id = fields.Many2one(
        comodel_name="hc.claim.identifier",
        string="Identifier",
        help="Identifier associated with this Claim Identifier Extension.")

class ClaimInsuranceIdentifier(models.Model):
    _name = "hc.claim.insurance.identifier"
    _description = "Claim Insurance Identifier"
    _inherit = ["hc.basic.association", "hc.identifier", "hc.identifier.use"]

    insurance_id = fields.Many2one(
        comodel_name="hc.claim.insurance",
        string="Insurance",
        help="Insurance associated with this Claim Insurance Identifier.")
#     extension_ids = fields.One2many(
#         comodel_name="hc.claim.insurance.identifier.extension",
#         inverse_name="insurance_identifier_id",
#         string="Extensions",
#         help="Additional Content defined by implementations.")

# class ClaimInsuranceIdentifierExtension(models.Model):
#     _name = "hc.claim.insurance.identifier.extension"
#     _description = "Claim Insurance Identifier Extension"
#     _inherit = ["hc.basic.association", "hc.extension"]

#     insurance_identifier_id = fields.Many2one(
#         comodel_name="hc.claim.insurance.identifier",
#         string="Insurance Identifier",
#         help="Insurance Identifier associated with this Claim Insurance Identifier Extension.")

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

class ClaimInsurancePreAuthRef(models.Model):
    _name = "hc.claim.insurance.pre.auth.ref"
    _description = "Claim Insurance Pre Auth Ref"
    _inherit = ["hc.basic.association"]

    insurance_id = fields.Many2one(
        comodel_name="hc.claim.insurance",
        string="Insurance",
        help="Insurance or medical plan.")
    pre_auth_ref = fields.Char(
        string="Pre Auth Ref",
        help="Pre Auth Ref associated with this Claim Insurance Pre Auth Ref.")

class ClaimItemCareTeamLinkId(models.Model):
    _name = "hc.claim.item.care.team.link.id"
    _description = "Claim Item Care Team Link Id"
    _inherit = ["hc.basic.association"]

    item_id = fields.Many2one(
        comodel_name="hc.claim.item",
        string="Item",
        help="Goods and Services.")
    care_team_link_id = fields.Integer(
        string="Care Team Link Id",
        help="Care Team Link Id associated with this Claim Item Care Team Link Id.")

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

class ClaimItemProcedureLinkId(models.Model):
    _name = "hc.claim.item.procedure.link.id"
    _description = "Claim Item Procedure Link Id"
    _inherit = ["hc.basic.association"]

    item_id = fields.Many2one(
        comodel_name="hc.claim.item",
        string="Item",
        help="Goods and Services.")
    procedure_link_id = fields.Integer(
        string="Information Link Id",
        help="Procedure Link Id associated with this Claim Item Procedure Link Id.")

class ClaimItemInformationLinkId(models.Model):
    _name = "hc.claim.item.information.link.id"
    _description = "Claim Item Information Link Id"
    _inherit = ["hc.basic.association"]

    item_id = fields.Many2one(
        comodel_name="hc.claim.item",
        string="Item",
        help="Goods and Services.")
    information_link_id = fields.Integer(
        string="Information Link Id",
        help="Information Link Id associated with this Claim Item Information Link Id.")

class ClaimItemUDI(models.Model):
    _name = "hc.claim.item.udi"
    _description = "Claim Item UDI"
    _inherit = ["hc.basic.association"]

    item_id = fields.Many2one(
        comodel_name="hc.claim.item",
        string="Item",
        help="Goods and Services.")
    udi_id = fields.Many2one(
        comodel_name="hc.res.device",
        string="UDI",
        help="UDI associated with this Claim Item UDI.")

class ClaimItemEncounter(models.Model):
    _name = "hc.claim.item.encounter"
    _description = "Claim Item Encounter"
    _inherit = ["hc.basic.association"]

    item_id = fields.Many2one(
        comodel_name="hc.claim.item",
        string="Item",
        help="Goods and Services.")
    encounter_id = fields.Many2one(
        comodel_name="hc.res.encounter",
        string="Encounter",
        help="Encounter associated with this Claim Item Encounter.")

class ClaimRelatedClaimReference(models.Model):
    _name = "hc.claim.related.claim.reference"
    _description = "Claim Related Claim Reference"
    _inherit = ["hc.basic.association", "hc.identifier", "hc.identifier.use"]

    related_claim_id = fields.Many2one(
        comodel_name="hc.claim.related.claim",
        string="Related Claim",
        help="Related Claim associated with this Claim Related Claim Reference.")

class ClaimType(models.Model):
    _name = "hc.vs.claim.type"
    _description = "Claim Type"
    _inherit = ["hc.value.set.contains"]

    name = fields.Char(
        string="Name",
        help="Name of this claim type.")
    code = fields.Char(
        string="Code",
        help="Code of this claim type.")
    contains_id = fields.Many2one(
        comodel_name="hc.vs.claim.type",
        string="Parent",
        help="Parent claim type.")

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

class DiagnosisPackageCode(models.Model):
    _name = "hc.vs.diagnosis.package.code"
    _description = "Diagnosis Package Code"
    _inherit = ["hc.value.set.contains"]

class DiagnosisType(models.Model):
    _name = "hc.vs.diagnosis.type"
    _description = "Diagnosis Type"
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

# class MissingToothReason(models.Model):
#     _name = "hc.vs.missing.tooth.reason"
#     _description = "Missing Tooth Reason"
#     _inherit = ["hc.value.set.contains"]

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

# class Teeth(models.Model):
#     _name = "hc.vs.teeth"
#     _description = "Teeth"
#     _inherit = ["hc.value.set.contains"]

class Tooth(models.Model):
    _name = "hc.vs.tooth"
    _description = "Tooth"
    _inherit = ["hc.value.set.contains"]

class UniqueDeviceIdentifier(models.Model):
    _name = "hc.vs.unique.device.identifier"
    _description = "Unique Device Identifier"
    _inherit = ["hc.value.set.contains"]

class ClaimInformationReason(models.Model):
    _name = "hc.vs.claim.information.reason"
    _description = "Claim Information Reason"
    _inherit = ["hc.value.set.contains"]
