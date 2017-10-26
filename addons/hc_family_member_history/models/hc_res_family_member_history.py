# -*- coding: utf-8 -*-

from openerp import models, fields, api
from datetime import datetime
from openerp.tools import DEFAULT_SERVER_DATE_FORMAT as DF
from openerp.tools import DEFAULT_SERVER_DATETIME_FORMAT as DTF

class FamilyMemberHistory(models.Model):
    _name = "hc.res.family.member.history"
    _description = "Family Member History"
    _rec_name="record_name"

    record_name = fields.Char(
        string="Record Name",
        compute="_compute_record_name",
        store="True",
        help="Human-readable label for this family member history definition. Patient Name + DOB + Family Member Name + Relationship + Update Date.")
    identifier_ids = fields.One2many(
        comodel_name="hc.family.member.history.identifier",
        inverse_name="family_member_history_id",
        string="Identifiers",
        help="External Id(s) for this record.")
    definition_ids = fields.One2many(
        comodel_name="hc.family.member.history.definition",
        inverse_name="family_member_history_id",
        string="Definitions",
        help="Instantiates protocol or definition.")
    status = fields.Selection(
        string="Status",
        required="True",
        selection=[
            ("partial", "Partial"),
            ("completed", "Completed"),
            ("entered-in-error", "Entered-In-Error"),
            ("health-unknown", "Health-Unknown")],
        default="partial",
        help="A code specifying the status of the record of the family history of a specific family member.")
    status_history_ids = fields.One2many(
        comodel_name="hc.family.member.history.status.history",
        inverse_name="family_member_history_id",
        string="Status History",
        help="The status of the family member history over time.")
    data_absent_reason = fields.Selection(
        string="Data Absent Reason",
        selection=[
            ("subject-unknown", "Subject-Unknown"),
            ("withheld", "Withheld"),
            ("unable-to-obtain", "Unable-To-Obtain"),
            ("deferred", "Deferred")],
        help="Describes why the family member history did not occur in coded and/or textual form.")
    patient_id = fields.Many2one(
        comodel_name="hc.res.patient",
        string="Patient",
        required="True",
        help="Patient history is about.")
    date = fields.Datetime(
        string="Date",
        required="True",
        default=fields.datetime.now(),
        help="When history was captured/updated.")
    family_member_name_type = fields.Selection(
        string="Family Member Name Type",
        required="True",
        selection=[
            ("string", "String"),
            ("related_person", "Related Person")],
        help="Type of name of family member.")
    family_member_name = fields.Char(
        string="Family Member",
        compute="_compute_family_member_name",
        store="True",
        help="The family member described.")
    family_member_name_string = fields.Char(
        string="Family Member Name String",
        help="String value of the family member described (e.g., 'My aunt Agatha', 'uncle'.")
    family_member_name_related_person_id = fields.Many2one(
        comodel_name="hc.res.related.person",
        string="Family Member Related Person Name",
        help="Related Person who is a family member of this patient.")
    relationship_id = fields.Many2one(
        comodel_name="hc.vs.v3.family.member",
        string="Relationship",
        required="True",
        help="Relationship to the subject.")
    # gender = fields.Selection(
    #     related="person_id.gender",
    #     readonly=True,
    #     help="The gender a family member used for administrative purposes.")
    # born = fields.Char(
    #     string="Birth Date",
    #     related="person_id.born_name",
    #     readonly=True,
    #     help="(approximate) date of birth.")
    # age = fields.Char(
    #     string="Age",
    #     related="person_id.age_name",
    #     readonly=True,
    #     help="(approximate) age.")
    # deceased = fields.Char(
    #     string="Deceased Age",
    #     related="person_id.deceased_name",
    #     readonly=True,
    #     help="Dead? How old/when?")
    gender = fields.Selection(
        string="Gender",
        selection=[
            ("male", "Male"),
            ("female", "Female"),
            ("other", "Other"),
            ("unknown", "Unknown")],
        help="The gender of a family member used for administrative purposes.")
    born_type = fields.Selection(
        string="Born Type",
        selection=[
            ("period", "Period"),
            ("date", "Date"),
            ("string", "String")],
        help="Type of date of birth.")
    born_name = fields.Char(
        string="Born",
        compute="_compute_born_name",
        help="Date of birth.")
    earliest_born_date = fields.Date(
        string="Earliest Born Date",
        help="Earliest approximate date of birth.")
    latest_born_date = fields.Date(
        string="Latest Born Date",
        help="Latest approximate date of birth.")
    born_date = fields.Date(
        string="Born Date",
        help="Date of birth.")
    born_string = fields.Char(
        string="Born",
        help="String of approximate date of birth.")
    age_type = fields.Selection(
        string="Age Type",
        selection=[
            ("age", "Age"),
            ("range", "Range"),
            ("string", "String")],
        help="Type of age.")
    age_name = fields.Char(
        string="Age",
        compute="_compute_age_name",
        help="Age.")
    age = fields.Integer(
        string="Age Integer",
        size=3,
        help="Approximate age.")
    age_uom_id = fields.Many2one(
        comodel_name="product.uom",
        string="Age UOM",
        domain="[('category_id','=','Time (UCUM)')]",
        default="a",
        help="Age unit of measure.")
    age_range_low = fields.Float(
        string="Age Range Low",
        help="Low limit of approximate age.")
    age_range_high = fields.Float(
        string="Age Range High",
        help="High limit of approximate age.")
    age_string = fields.Char(
        string="Age",
        help="String of approximate age.")
    is_estimated_age = fields.Boolean(
        string="Estimated Age",
        help="Age is estimated?")
    is_deceased = fields.Boolean(
        string="Deceased",
        help="Dead? How old/when?")
    # is_deceased_age_known = fields.Boolean(
    #     string="Is Deceased Age Known",
    #     help="Deceased age known?")
    deceased_age_type = fields.Selection(
        string="Deceased Age Type",
        selection=[
            ("age", "Age"),
            ("range", "Range"),
            ("date", "Date"),
            ("string", "String")],
        help="Type of dead? how old/when?")
    deceased_age_name = fields.Char(
        string="Deceased Age",
        compute="_compute_deceased_age_name",
        help="Dead? How old/when?")
    deceased_age = fields.Integer(
        string="Deceased Age Integer",
        size=3,
        help="Dead? How old/when?")
    deceased_age_uom_id = fields.Many2one(
        comodel_name="product.uom",
        string="Deceased Age UOM",
        domain="[('category_id','=','Time (UCUM)')]",
        default="a",
        help="Deceased age unit of measure.")
    deceased_age_range_low = fields.Float(
        string="Deceased Age Range Low",
        help="Low limit of dead? how old/when?")
    deceased_age_range_high = fields.Float(
        string="Deceased Age Range High",
        help="High limit of dead? how old/when?")
    deceased_age_date = fields.Date(
        string="Deceased Age Date",
        help="Deceased date.")
    deceased_age_string = fields.Char(
        string="Deceased Age String",
        help="String of dead? how old/when?")
    reason_code_ids = fields.Many2many(
        comodel_name="hc.vs.clinical.finding",
        relation="family_member_history_reason_code_rel",
        string="Reason Codes",
        help="Why was family member history performed?")
    reason_reference_ids = fields.One2many(
        comodel_name="hc.family.member.history.reason.reference",
        inverse_name="family_member_history_id",
        string="Reason References",
        help="Why was family member history performed?")
    note_ids = fields.One2many(
        comodel_name="hc.family.member.history.note",
        inverse_name="family_member_history_id",
        string="Notes",
        help="General note about related person.")

    #Extension attribute
    patient_record_ids = fields.One2many(
        comodel_name="hc.family.member.history.patient.record",
        inverse_name="family_member_history_id",
        string="Patient Records",
        help="A link to one to more patient records for the relation.")
    severity_id = fields.Many2one(
        comodel_name="hc.vs.condition.severity",
        string="Severity",
        help="A qualification of the seriousness or impact on health of the family member condition.")
    type_id = fields.Many2one(
        comodel_name="hc.vs.family.member.history.type",
        string="Type",
        help="Purpose of the family member history or why it was created, such as when family member history is targeted for cardiovascular health, mental health, or genetic counseling.")
    genetics_observation_ids = fields.One2many(
        comodel_name="hc.family.member.history.genetics.observation",
        inverse_name="family_member_history_id",
        string="Genetics Observations",
        help="Allows capturing risk-relevant observations about the relative that aren't themselves a specific health condition; e.g. Certain ethnic ancestries that are disease-relevant, presence of particular genetic markers, etc..")

    # Backbone element
    condition_ids = fields.One2many(
        comodel_name="hc.family.member.history.condition",
        inverse_name="family_member_history_id",
        string="Conditions",
        help="Condition that the related person had.")

    #Extension bacbone element
    parent_ids = fields.One2many(
        comodel_name="hc.family.member.history.parent",
        inverse_name="family_member_history_id",
        string="Parents",
        help="Identifies a parent of the relative.")
    sibling_ids = fields.One2many(
        comodel_name="hc.family.member.history.sibling",
        inverse_name="family_member_history_id",
        string="Siblings",
        help="Identifies a sibling of the relative.")

    # technical attribute
    has_born = fields.Boolean(
        string='Has Born',
        invisible=True,
        help="Indicates if born exists. Used to enforce constraint born or age.")

    @api.onchange('born_type')
    def onchange_born_type(self):
        if self.born_type:
            self.age_type = True
            self.has_born = True
        else:
            self.has_born = False

    @api.depends('patient_id', 'family_member_name', 'date')
    def _compute_record_name(self):
        comp_name = '/'
        for hc_res_family_member_history in self:
            if hc_res_family_member_history.patient_id:
                comp_name = hc_res_family_member_history.patient_id.name
                if hc_res_family_member_history.patient_id.birth_date:
                    patient_birth_date = datetime.strftime(datetime.strptime(hc_res_family_member_history.patient_id.birth_date, DF), "%Y-%m-%d")
                    comp_name = comp_name + "("+ patient_birth_date + "),"
            if hc_res_family_member_history.family_member_name:
                comp_name = comp_name + " " + hc_res_family_member_history.family_member_name + ", " + hc_res_family_member_history.relationship_id.name + "," or ''
            if hc_res_family_member_history.date:
                patient_date = datetime.strftime(datetime.strptime(hc_res_family_member_history.date, DTF), "%Y-%m-%d")
                comp_name = comp_name + " " + patient_date
            hc_res_family_member_history.record_name = comp_name

    @api.depends('family_member_name_type')
    def _compute_family_member_name(self):
        for hc_res_family_member_history in self:
            if hc_res_family_member_history.family_member_name_type == 'string':
                hc_res_family_member_history.family_member_name = hc_res_family_member_history.family_member_name_string
            elif hc_res_family_member_history.family_member_name_type == 'related_person':
                hc_res_family_member_history.family_member_name = hc_res_family_member_history.family_member_name_related_person_id.name

    @api.depends('born_type')
    def _compute_born_name(self):
        for hc_res_family_member_history in self:
            if hc_res_family_member_history.born_type == 'period':
                hc_res_family_member_history.born_name = 'Between ' + str(hc_res_family_member_history.earliest_born_date) + ' and ' + str(hc_res_family_member_history.latest_born_date)
            elif hc_res_family_member_history.born_type == 'date':
                hc_res_family_member_history.born_name = str(hc_res_family_member_history.born_date)
            elif hc_res_family_member_history.born_type == 'string':
                hc_res_family_member_history.born_name = hc_res_family_member_history.born_string

    @api.depends('age_type')
    def _compute_age_name(self):
        for hc_res_family_member_history in self:
            if hc_res_family_member_history.age_type == 'age':
                hc_res_family_member_history.age_name = str(hc_res_family_member_history.age) + ' ' + str(hc_res_family_member_history.age_uom_id.name) + 's old'
            elif hc_res_family_member_history.age_type == 'range':
                hc_res_family_member_history.age_name = 'Between ' + str(hc_res_family_member_history.age_range_low) + ' and ' + str(hc_res_family_member_history.age_range_high)
            elif hc_res_family_member_history.age_type == 'string':
                hc_res_family_member_history.age_name = hc_res_family_member_history.age_string

    # @api.multi
    @api.depends('deceased_age_type')
    def _compute_deceased_age_name(self):
        for hc_res_family_member_history in self:
            if hc_res_family_member_history.deceased_age_type == 'age':
                hc_res_family_member_history.deceased_age_name = str(hc_res_family_member_history.deceased_age) + ' ' + str(hc_res_family_member_history.deceased_age_uom_id.name) + 's old'
            elif hc_res_family_member_history.deceased_age_type == 'range':
                hc_res_family_member_history.deceased_age_name = 'Between ' + str(hc_res_family_member_history.deceased_age_range_low) + ' and ' + str(hc_res_family_member_history.deceased_age_range_high)
            elif hc_res_family_member_history.deceased_age_type == 'date':
                hc_res_family_member_history.deceased_age_name = str(hc_res_family_member_history.deceased_age_date)
            elif hc_res_family_member_history.deceased_age_type == 'string':
                hc_res_family_member_history.deceased_age_name = hc_res_family_member_history.deceased_age_string

# Constraints

# fhs-1: Can have age[x] or born[x], but not both (expression : age.empty() or born.empty())
# fhs-2: Can only have estimatedAge if age[x] is present (expression : age.exists() or estimatedAge.empty())

    @api.model
    def create(self, vals):
        status_history_obj = self.env['hc.family.member.history.status.history']
        res = super(FamilyMemberHistory, self).create(vals)
        if vals and vals.get('status'):
            status_history_vals = {
                'family_member_history_id': res.id,
                'status': res.status,
                'start_date': datetime.today()
                }
            if vals.get('status') == 'entered-in-error':
                status_history_vals.update({'end_date': datetime.today()})
            status_history_obj.create(status_history_vals)
        return res

    @api.multi
    def write(self, vals):
        status_history_obj = self.env['hc.family.member.history.status.history']
        res = super(FamilyMemberHistory, self).write(vals)
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
                    'family_member_history_id': self.id,
                    'status': vals.get('status'),
                    'start_date': datetime.today()
                    }
                if vals.get('status') == 'entered-in-error':
                    status_history_vals.update({'end_date': datetime.today()})
                status_history_obj.create(status_history_vals)
        return res

class FamilyMemberHistoryCondition(models.Model):
    _name = "hc.family.member.history.condition"
    _description = "Family Member History Condition"

    family_member_history_id = fields.Many2one(
        comodel_name="hc.res.family.member.history",
        string="Family Member History",
        help="Family Member History associated with this Condition.")
    code_id = fields.Many2one(
        comodel_name="hc.vs.condition.code",
        string="Code",
        required="True",
        help="Condition suffered by relation.")
    outcome = fields.Selection(
        string="Condition Outcome",
        selection=[
            ("deceased", "Deceased"),
            ("permanent disability", "Permanent Disability"),
            ("etc.", "Etc.")],
        help="Indicates what happened as a result of this condition. If the condition resulted in death, deceased date is captured on the relation.")
    onset_type = fields.Selection(
        string="Onset Type",
        selection=[
            ("age", "Age"),
            ("range", "Range"),
            ("string", "String")],
        help="Type of when condition first manifested.")
    onset_name = fields.Char(
        string="Onset",
        compute="_compute_onset_name",
        help="When condition first manifested.")
    onset_age = fields.Integer(
        string="Onset Age",
        size=3,
        help="When condition first manifested.")
    onset_age_uom_id = fields.Many2one(
        comodel_name="product.uom",
        string="Onset Age UOM",
        domain="[('category_id','=','Time (UCUM)')]",
        default="a",
        help="Onset age unit of measure.")
    onset_range_low = fields.Float(
        string="Onset Range Low",
        help="Low limit of when condition first manifested.")
    onset_range_high = fields.Float(
        string="Onset Range High",
        help="High limit of when condition first manifested.")
    onset_string = fields.Char(
        string="Onset",
        help="String of when condition first manifested.")
    note_ids = fields.One2many(
        comodel_name="hc.family.member.history.condition.note",
        inverse_name="condition_id",
        string="Notes",
        help="Extra information about condition.")

    # Extension attribute
    abatement_type = fields.Selection(
        string="Abatement Type",
        required="True",
        selection=[
            ("date", "Date"),
            ("Age", "Age"),
            ("boolean", "Boolean")],
        help="Type of the approximate date, age, or flag indicating that the condition of the family member resolved.")
    abatement_name = fields.Char(
        string="Abatement",
        compute="_compute_abatement_name", store="True",
        help="The approximate date, age, or flag indicating that the condition of the family member resolved.")
    abatement_date = fields.Date(
        string="Abatement Date",
        help="The approximate date indicating that the condition of the family member resolved.")
    abatement_age = fields.Integer(
        string="Abatement Age",
        size=3,
        help="The approximate age indicating that the condition of the family member resolved.")
    abatement_age_uom_id = fields.Many2one(
        comodel_name="product.uom",
        string="Abatement Age UOM",
        domain="[('category_id','=','Time (UCUM)')]",
        default="a",
        help="Abatement age unit of measure.")
    abatement_boolean = fields.Boolean(
        string="Abatement Boolean",
        help="The flag indicating that the condition of the family member resolved.")

    @api.depends('onset_type')
    def _compute_onset_name(self):
        for hc_family_member_history_condition in self:
            if hc_family_member_history_condition.onset_type == 'age':
                hc_family_member_history_condition.onset_name = str(hc_family_member_history_condition.onset_age) + " " + str(hc_family_member_history_condition.onset_age_uom_id.name) + "s old"
            elif hc_family_member_history_condition.onset_type == 'string':
                hc_family_member_history_condition.onset_name = hc_family_member_history_condition.onset_string
            elif hc_family_member_history_condition.onset_type == 'range':
                hc_family_member_history_condition.onset_name = "Between " + str(hc_family_member_history_condition.onset_range_low) + " and " + str(hc_family_member_history_condition.onset_range_high)

    @api.depends('abatement_type')
    def _compute_abatement_name(self):
        for hc_family_member_history_condition in self:
            if hc_family_member_history_condition.abatement_type == 'date':
                hc_family_member_history_condition.abatement_name = str(hc_family_member_history_condition.abatement_date)
            elif hc_family_member_history_condition.abatement_type == 'age':
                hc_family_member_history_condition.abatement_name = str(hc_family_member_history_condition.abatement_age) + " " + str(hc_family_member_history_condition.abatement_age_uom_id.name) + "s old"
            elif hc_family_member_history_condition.abatement_type == 'boolean':
                hc_family_member_history_condition.abatement_name = hc_family_member_history_condition.abatement_boolean

# Extension class
class FamilyMemberHistoryParent(models.Model):
    _name = "hc.family.member.history.parent"
    _description = "Family Member History Parent"

    family_member_history_id = fields.Many2one(
        comodel_name="hc.res.family.member.history",
        string="Family Member History",
        help="Family Member History associated with this Family Member History Parent.")
    type_id = fields.Many2one(
        comodel_name="hc.vs.v3.family.member",
        string="Type",
        domain="[('hierarchy_id','=','parent')]",
        help="mother | father | adoptive mother | etc..")
    reference_id = fields.Many2one(
        comodel_name="hc.res.family.member.history",
        string="Reference",
        help="Link to parent relative(s).")

class FamilyMemberHistorySibling(models.Model):
    _name = "hc.family.member.history.sibling"
    _description = "Family Member History Sibling"

    family_member_history_id = fields.Many2one(
        comodel_name="hc.res.family.member.history",
        string="Family Member History",
        help="Family Member History associated with this Family Member History Sibling.")
    type_id = fields.Many2one(
        comodel_name="hc.vs.v3.family.member",
        string="Type",
        domain="[('hierarchy_id','=','sibling')]",
        help="sibling | brother | sister | etc..")
    reference_id = fields.Many2one(
        comodel_name="hc.res.family.member.history",
        string="Reference",
        help="Link to sibling relative(s).")


class FamilyMemberHistoryIdentifier(models.Model):
    _name = "hc.family.member.history.identifier"
    _description = "Family Member History Identifier"
    _inherits = {"hc.person.identifier": "identifier_id"}

    identifier_id = fields.Many2one(
        comodel_name="hc.person.identifier",
        string="Identifier",
        ondelete="restrict",
        required="True",
        help="Person Identifier associated with this Family Member Identifier.")
    family_member_history_id = fields.Many2one(
        comodel_name="hc.res.family.member.history",
        string="Family Member History",
        help="Family Member History associated with this Family Member Identifier.")

class FamilyMemberHistoryDefinition(models.Model):
    _name = "hc.family.member.history.definition"
    _description = "Family Member History Definition"
    _inherit = ["hc.basic.association"]

    family_member_history_id = fields.Many2one(
        comodel_name="hc.res.family.member.history",
        string="Family Member History",
        help="Family Member History associated with this Family Member History Definition.")
    definition_type = fields.Selection(
        string="Definition Type",
        selection=[
            ("plan_definition", "Plan Definition"),
            ("questionnaire", "Questionnaire")],
        help="Type of instantiates protocol or definition.")
    definition_name = fields.Char(
        string="Definition",
        compute="_compute_definition_name",
        store="True",
        help="Instantiates protocol or definitio.")
    definition_plan_definition_id = fields.Many2one(
        comodel_name="hc.res.plan.definition",
        string="Definition Plan Definition",
        help="Plan Definition instantiates protocol or definition.")
    definition_questionnaire_id = fields.Many2one(
        comodel_name="hc.res.questionnaire",
        string="Definition Questionnaire",
        help="Questionnaire instantiates protocol or definition.")

    @api.depends('definition_type')
    def _compute_definition_name(self):
        for hc_family_member_history_definition in self:
            if hc_family_member_history_definition.definition_type == 'plan_definition':
                hc_family_member_history_definition.definition_name = hc_family_member_history_definition.definition_plan_definition_id.name
            elif hc_family_member_history_definition.definition_type == 'questionnaire':
                hc_family_member_history_definition.definition_name = hc_family_member_history_definition.definition_questionnaire_id.name

class FamilyMemberHistoryStatusHistory(models.Model):
    _name = "hc.family.member.history.status.history"
    _description = "Family Member History Status History"

    family_member_history_id = fields.Many2one(
        comodel_name="hc.res.family.member.history",
        string="Family Member History",
        help="Family Member History associated with this Family Member History Status History.")
    status = fields.Char(
        string="Status",
        help="The status of the family member history.")
    start_date = fields.Datetime(
        string="Start Date",
        help="Start of the period during which this family member history status is valid.")
    end_date = fields.Datetime(
        string="End Date",
        help="End of the period during which this family member history status is valid.")
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

class FamilyMemberHistoryReasonReference(models.Model):
    _name = "hc.family.member.history.reason.reference"
    _description = "Family Member History Reason Reference"
    _inherit = ["hc.basic.association"]

    family_member_history_id = fields.Many2one(
        comodel_name="hc.res.family.member.history",
        string="Family Member History",
        help="Family Member History associated with this Family Member History Reason Reference.")
    reason_reference_type = fields.Selection(
        string="Reason Reference Type",
        selection=[
            ("condition", "Condition"),
            ("observation", "Observation"),
            ("allergy_intolerance", "Allergy Intolerance"),
            ("questionnaire_response", "Questionnaire Response")],
        help="Type of what is account tied to.")
    reason_reference_name = fields.Char(
        string="Reason Reference",
        compute="_compute_reason_reference_name",
        store="True",
        help="Why was family member history performed.")
    reason_reference_condition_id = fields.Many2one(
        comodel_name="hc.res.condition",
        string="Reason Reference Condition",
        help="Condition account tied to.")
    reason_reference_observation_id = fields.Many2one(
        comodel_name="hc.res.observation",
        string="Reason Reference Observation",
        help="Observation account tied to.")
    reason_reference_allergy_intolerance_id = fields.Many2one(
        comodel_name="hc.res.allergy.intolerance",
        string="Reason Reference Allergy Intolerance",
        help="Allergy Intolerance account tied to.")
    reason_reference_questionnaire_response_id = fields.Many2one(
        comodel_name="hc.res.questionnaire.response",
        string="Reason Reference Questionnaire Response",
        help="Questionnaire Response account tied to.")

    @api.depends('reason_reference_type')
    def _compute_reason_reference_name(self):
        for hc_family_member_history_reason_reference in self:
            if hc_family_member_history_reason_reference.reason_reference_type == 'condition':
                hc_family_member_history_reason_reference.reason_reference_name = hc_family_member_history_reason_reference.reason_reference_condition_id.name
            elif hc_family_member_history_reason_reference.reason_reference_type == 'observation':
                hc_family_member_history_reason_reference.reason_reference_name = hc_family_member_history_reason_reference.reason_reference_observation_id.name
            elif hc_family_member_history_reason_reference.reason_reference_type == 'allergy_intolerance':
                hc_family_member_history_reason_reference.reason_reference_name = hc_family_member_history_reason_reference.reason_reference_allergy_intolerance_id.name
            elif hc_family_member_history_reason_reference.reason_reference_type == 'questionnaire_response':
                hc_family_member_history_reason_reference.reason_reference_name = hc_family_member_history_reason_reference.reason_reference_questionnaire_response_id.name

class FamilyMemberHistoryNote(models.Model):
    _name = "hc.family.member.history.note"
    _description = "Family Member History Note"
    _inherit = ["hc.basic.association", "hc.annotation"]

    family_member_history_id = fields.Many2one(
        comodel_name="hc.res.family.member.history",
        string="Family Member History",
        help="Family Member History associated with this Family Member History Note.")

    @api.depends('author_type')
    def _compute_author_name(self):
        for hc_family_member_history_note in self:
            if hc_family_member_history_note.author_type == 'string':
                hc_family_member_history_note.author_name = hc_family_member_history_note.author_string
            elif hc_family_member_history_note.author_type == 'practitioner':
                hc_family_member_history_note.author_name = hc_family_member_history_note.author_practitioner_id.name
            elif hc_family_member_history_note.author_type == 'patient':
                hc_family_member_history_note.author_name = hc_family_member_history_note.author_patient_id.name
            elif hc_family_member_history_note.author_type == 'related_person':
                hc_family_member_history_note.author_name = hc_family_member_history_note.author_related_person_id.name

class FamilyMemberHistoryConditionNote(models.Model):
    _name = "hc.family.member.history.condition.note"
    _description = "Family Member History Condition Note"
    _inherit = ["hc.basic.association", "hc.annotation"]

    condition_id = fields.Many2one(
        comodel_name="hc.family.member.history.condition",
        string="Condition",
        help="Condition associated with this Family Member History Condition Note.")

    @api.depends('author_type')
    def _compute_author_name(self):
        for hc_family_member_history_note in self:
            if hc_family_member_history_note.author_type == 'string':
                hc_family_member_history_note.author_name = hc_family_member_history_note.author_string
            elif hc_family_member_history_note.author_type == 'practitioner':
                hc_family_member_history_note.author_name = hc_family_member_history_note.author_practitioner_id.name
            elif hc_family_member_history_note.author_type == 'patient':
                hc_family_member_history_note.author_name = hc_family_member_history_note.author_patient_id.name
            elif hc_family_member_history_note.author_type == 'related_person':
                hc_family_member_history_note.author_name = hc_family_member_history_note.author_related_person_id.name

# Extension association
class FamilyMemberHistoryPatientRecord(models.Model):
    _name = "hc.family.member.history.patient.record"
    _description = "Family Member History Patient Record"
    _inherit = ["hc.basic.association"]

    family_member_history_id = fields.Many2one(
        comodel_name="hc.res.family.member.history",
        string="Family Member History",
        help="Family Member History associated with this Family Member History Patient Record.")
    patient_record_type = fields.Selection(
        string="Patient Record Type",
        selection=[
            ("person", "Person"),
            ("patient", "Patient"),
            ("practitioner", "Practitioner"),
            ("related_person", "Related Person")],
        help="Type of instantiates protocol or definition.")
    patient_record_name = fields.Char(
        string="Patient Record",
        compute="_compute_patient_record_name",
        store="True",
        help="A link to one to more patient records for the relation.")
    patient_record_person_id = fields.Many2one(
        comodel_name="hc.res.person",
        string="Patient Record Person",
        help="Person link to one to more patient records for the relation.")
    patient_record_patient_id = fields.Many2one(
        comodel_name="hc.res.patient",
        string="Patient Record Patient",
        help="Patient link to one to more patient records for the relation.")
    patient_record_practitioner_id = fields.Many2one(
        comodel_name="hc.res.practitioner",
        string="Patient Record Practitioner",
        help="Practitioner link to one to more patient records for the relation.")
    patient_record_related_person_id = fields.Many2one(
        comodel_name="hc.res.related.person",
        string="Patient Record Related Person",
        help="Related Person link to one to more patient records for the relation.")

    @api.depends('patient_record_type')
    def _compute_patient_record_name(self):
        for hc_family_member_history_patient_record in self:
            if hc_family_member_history_patient_record.patient_record_type == 'person':
                hc_family_member_history_patient_record.patient_record_name = hc_family_member_history_patient_record.patient_record_person_id.name
            elif hc_family_member_history_patient_record.patient_record_type == 'patient':
                hc_family_member_history_patient_record.patient_record_name = hc_family_member_history_patient_record.patient_record_patient_id.name
            elif hc_family_member_history_patient_record.patient_record_type == 'practitioner':
                hc_family_member_history_patient_record.patient_record_name = hc_family_member_history_patient_record.patient_record_practitioner_id.name
            elif hc_family_member_history_patient_record.patient_record_type == 'related_person':
                hc_family_member_history_patient_record.patient_record_name = hc_family_member_history_patient_record.patient_record_related_person_id.name

class FamilyMemberHistoryGeneticsObservation(models.Model):
    _name = "hc.family.member.history.genetics.observation"
    _description = "Family Member History Genetics Observation"
    _inherit = ["hc.basic.association"]

    family_member_history_id = fields.Many2one(
        comodel_name="hc.res.family.member.history",
        string="Family Member History",
        help="Family Member History associated with this Family Member History Genetics Observation.")
    genetics_observation_id = fields.Many2one(
        comodel_name="hc.res.observation",
        string="Genetics Observation",
        help="Allows capturing risk-relevant observations about the relative that aren't themselves a specific health condition; e.g. Certain ethnic ancestries that are disease-relevant, presence of particular genetic markers, etc..")

class V3FamilyMember(models.Model):
    _name = "hc.vs.v3.family.member"
    _description = "V3 Family Member"
    _inherit = ["hc.value.set.contains"]

    name = fields.Char(
        string="Name",
        help="Name of this family member.")
    code = fields.Char(
        string="Code",
        help="Code of this family member.")
    contains_id = fields.Many2one(
        comodel_name="hc.vs.v3.family.member",
        string="Parent",
        help="Parent family member.")
    hierarchy_id = fields.Many2one(
        comodel_name="hc.vs.v3.family.member",
        string="Hierarchy",
        help="Hierarchy family member.")

# Extension value set
class FamilyMemberHistoryType(models.Model):
    _name = "hc.vs.family.member.history.type"
    _description = "Family Member History Type"
    _inherit = ["hc.value.set.contains"]

    name = fields.Char(
        string="Name",
        help="Name of this family member history type.")
    code = fields.Char(
        string="Code",
        help="Code of this family member history type.")
    contains_id = fields.Many2one(
        comodel_name="hc.vs.family.member.history.type",
        string="Parent",
        help="Parent family member history type.")
