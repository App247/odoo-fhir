# -*- coding: utf-8 -*-

from openerp import models, fields, api

class Measure(models.Model):
    _name = "hc.res.measure"
    _description = "Measure"

    url = fields.Char(
        string="URI",
        help="Logical URI to reference this measure (globally unique).")
    identifier_ids = fields.One2many(
        comodel_name="hc.measure.identifier",
        inverse_name="measure_id",
        string="Identifiers",
        help="Additional identifier for the measure." )
    version = fields.Char(
        string="Version",
        help="Business version of the measure.")
    name = fields.Char(
        string="Name",
        help="Name for this measure (Computer friendly).")
    title = fields.Char(
        string="Title",
        help="Name for this measure (Human friendly).")
    status = fields.Selection(
        string="Status",
        required="True",
        selection=[
            ("draft", "Draft"),
            ("active", "Active"),
            ("retired", "Retired")],
        help="The status of this measure. Enables tracking the life-cycle of the content.")
    is_experimental = fields.Boolean(
        string="Experimental",
        help="If for testing purposes, not real usage.")
    date = fields.Datetime(
        string="Date",
        help="Date this was last changed.")
    description = fields.Text(
        string="Description",
        help="Natural language description of the measure.")
    purpose = fields.Text(
        string="Purpose",
        help="Why this measure is defined.")
    usage = fields.Text(
        string="Usage",
        help="Describes the clinical usage of the measure.")
    approval_date = fields.Date(
        string="Approval Date",
        help="When measure approved by publisher.")
    last_review_date = fields.Date(
        string="Last Review Date",
        help="Last review date for the measure.")
    effective_period_start_date = fields.Datetime(
        string="Effective Period Start Date",
        help="Period The effective date range for the measure.")
    effective_period_end_date = fields.Datetime(
        string="Effective Period End Date",
        help="End of the effective date range for the service definition.")
    use_context_ids = fields.One2many(
        comodel_name="hc.measure.use.context",
        inverse_name="measure_id",
        string="Use Contexts",
        help="Content intends to support these contexts.")
    jurisdiction_ids = fields.Many2many(
        comodel_name="hc.vs.jurisdiction",
        relation="measure_jurisdiction_rel",
        string="Jurisdictions",
        help="Intended jurisdiction for measure (if applicable).")
    topic_ids = fields.Many2many(
        comodel_name="hc.vs.definition.topic", 
        relation="measure_topic_rel",
        string="Topics",
        help="Descriptional topics for the measure.")
    contributor_ids = fields.One2many(
        comodel_name="hc.measure.contributor",
        inverse_name="measure_id",
        string="Contributors",
        help="A content contributor.")
    publisher = fields.Char(
        string="Publisher",
        help="Name of the publisher (Organization or individual).")
    contact_ids = fields.One2many(
        comodel_name="hc.measure.contact",
        inverse_name="measure_id",
        string="Contacts",
        help="Contact details for the publisher.")
    copyright = fields.Text(
        string="Copyright",
        help="Use and/or publishing restrictions.")
    related_artifact_ids = fields.One2many(
        comodel_name="hc.measure.related.artifact",
        inverse_name="measure_id",
        string="Related Artifacts",
        help="Related artifacts for the measure.")
    library_ids = fields.One2many(
        comodel_name="hc.measure.library",
        inverse_name="measure_id",
        string="Libraries",
        help="Logic used by the measure.")
    disclaimer = fields.Text(
        string="Disclaimer",
        help="Disclaimer for the measure.")
    scoring = fields.Selection(
        string="Scoring",
        selection=[
            ("proportion", "Proportion"),
            ("ratio", "Ratio"),
            ("continuous-variable", "Continuous Variable"),
            ("cohort", "Cohort")],
        help="The measure scoring type, e.g. proportion, CV.")
    composite_scoring = fields.Selection(
        string="Composite Scoring",
        selection=[
            ("opportunity", "Opportunity"),
            ("all-or-nothing", "All Or Nothing"),
            ("linear", "Linear"),
            ("weighted", "Weighted")],
        help="If this is a composite measure, the scoring method used to combine the component measures to determine the composite score.")
    type_ids = fields.One2many(
        comodel_name="hc.measure.type",
        inverse_name="measure_id",
        string="Types",
        help="The measure type, e.g. process, outcome.")
    risk_assessment = fields.Text(
        string="Risk Assessment",
        help="How is risk adjustment applied for this measure.")
    rate_aggregation = fields.Text(
        string="Rate Aggregation",
        help="How is rate aggregation performed for this measure.")
    rationale = fields.Text(
        string="Rationale",
        help="Why does this measure exist.")
    clinical_recommendation_statement = fields.Text(
        string="Clinical Recommendation Statement",
        help="Clinical recommendation.")
    improvement_notation = fields.Text(
        string="Improvement Notation",
        help="Improvement notation for the measure, e.g. higher score indicates better quality.")
    definition = fields.Text(
        string="Definition",
        help="A natural language definition of the measure.")
    guidance = fields.Text(
        string="Guidance",
        help="The guidance for the measure.")
    set = fields.Char(
        string="Set",
        help="The measure set, e.g. Preventive Care and Screening.")
    group_ids = fields.One2many(
        comodel_name="hc.measure.group",
        inverse_name="measure_id",
        string="Groups",
        help="Population criteria group.")
    supplemental_data_ids = fields.One2many(
        comodel_name="hc.measure.supplemental.data",
        inverse_name="measure_id",
        string="Supplemental Data",
        help="Supplemental data.")

class MeasureGroup(models.Model):
    _name = "hc.measure.group"
    _description = "Measure Group"

    measure_id = fields.Many2one(
        comodel_name="hc.res.measure",
        string="Measure",
        help="Measure associated with this Measure Group.")
    identifier_id = fields.Many2one(
        comodel_name="hc.measure.group.identifier",
        string="Identifier",
        required="True",
        help="Unique identifier.")
    name = fields.Char(
        string="Name",
        help="Short name.")
    description = fields.Text(
        string="Description",
        help="Summary description.")
    population_ids = fields.One2many(
        comodel_name="hc.measure.group.population",
        inverse_name="group_id",
        string="Populations",
        help="Population criteria.")
    stratifier_ids = fields.One2many(
        comodel_name="hc.measure.group.stratifier",
        inverse_name="group_id",
        string="Stratifiers",
        help="Stratifier criteria for the measure.")

class MeasureGroupPopulation(models.Model):
    _name = "hc.measure.group.population"
    _description = "Measure Group Population"

    group_id = fields.Many2one(
        comodel_name="hc.measure.group",
        string="Group",
        help="Population criteria group.")
    type = fields.Selection(
        string="Type",
        required="True",
        selection=[
            ("initial-population", "Initial Population"),
            ("numerator", "Numerator"),
            ("numerator-exclusion", "Numerator Exclusion"),
            ("denominator", "Denominator"), ("denominator-exclusion", "Denominator Exclusion"),
            ("denominator-exception", "Denominator Exception"),
            ("measure-population", "Measure Population"),
            ("measure-population-exclusion", "Measure Population Exclusion"),
            ("measure-observation", "Measure Observation")],
        help="The type of population criteria.")
    identifier_id = fields.Many2one(
        comodel_name="hc.measure.group.population.identifier",
        string="Identifier",
        required="True",
        help="Unique identifier.")
    name = fields.Char(
        string="Name",
        help="Short name.")
    description = fields.Text(
        string="Description",
        help="The human readable description of this population criteria.")
    criteria = fields.Text(
        string="Criteria",
        required="True",
        help="The name of a valid referenced CQL expression (may be namespaced) that defines this population criteria.")

class MeasureGroupStratifier(models.Model):
    _name = "hc.measure.group.stratifier"
    _description = "Measure Group Stratifier"

    group_id = fields.Many2one(
        comodel_name="hc.measure.group",
        string="Group",
        help="Population criteria group.")
    identifier_id = fields.Many2one(
        comodel_name="hc.measure.group.stratifier.identifier",
        string="Identifier",
        required="True",
        help="The identifier for the stratifier used to coordinate the reported data back to this stratifier.")
    criteria = fields.Text(
        string="Criteria",
        help="Stratifier criteria.")
    path = fields.Char(
        string="Path",
        help="Path to the stratifier.")

class MeasureSupplementalData(models.Model):
    _name = "hc.measure.supplemental.data"
    _description = "Measure Supplemental Data"

    measure_id = fields.Many2one(
        comodel_name="hc.res.measure",
        string="Measure",
        help="Supplemental data.")
    identifier_id = fields.Many2one(
        comodel_name="hc.measure.supplemental.data.identifier",
        string="Identifier",
        required="True",
        help="Identifier, unique within the measure.")
    usage_ids = fields.One2many(
        comodel_name="hc.measure.supplemental.data.usage",
        inverse_name="supplemental_data_id",
        string="Usages",
        help="An indicator of the intended usage for the supplemental data element.")
    criteria = fields.Text(
        string="Criteria",
        help="Supplemental data criteria.")
    path = fields.Char(
        string="Path",
        help="Path to the supplemental data element.")

class MeasureIdentifier(models.Model):
    _name = "hc.measure.identifier"
    _description = "Measure Identifier"
    _inherit = ["hc.basic.association", "hc.identifier"]

    measure_id = fields.Many2one(
        comodel_name="hc.res.measure",
        string="Measure",
        help="Measure associated with this Measure Identifier.")

class MeasureUseContext(models.Model):
    _name = "hc.measure.use.context"
    _description = "Measure Use Context"
    _inherit = ["hc.basic.association", "hc.usage.context"]

    measure_id = fields.Many2one(
        comodel_name="hc.res.measure",
        string="Measure",
        help="Measure associated with this Measure Use Context.")

class MeasureContributor(models.Model):
    _name = "hc.measure.contributor"
    _description = "Measure Contributor"
    _inherit = ["hc.basic.association"]
    _inherits = {"hc.contributor": "contributor_id"}

    contributor_id = fields.Many2one(
        comodel_name="hc.contributor",
        string="Contributor",
        ondelete="restrict",
        required="True",
        help="Contributor associated with this Measure Contributor.")
    measure_id = fields.Many2one(
        comodel_name="hc.res.measure",
        string="Measure",
        help="Measure associated with this Measure Contributor.")

class MeasureContact(models.Model):
    _name = "hc.measure.contact"
    _description = "Measure Contact"
    _inherit = ["hc.basic.association"]
    _inherits = {"hc.contact.detail": "contact_detail_id"}

    contact_detail_id = fields.Many2one(
        comodel_name="hc.contact.detail",
        string="Contact Detail",
        ondelete="restrict",
        required="True",
        help="Contact Detail associated with this Measure Contact.")
    measure_id = fields.Many2one(
        comodel_name="hc.res.measure",
        string="Measure",
        help="Measure associated with this Measure Contact.")

class MeasureRelatedArtifact(models.Model):
    _name = "hc.measure.related.artifact"
    _description = "Measure Related Artifact"
    _inherit = ["hc.basic.association", "hc.related.artifact"]

    measure_id = fields.Many2one(
        comodel_name="hc.res.measure",
        string="Measure",
        help="Measure associated with this Measure Related Artifact.")

class MeasureLibrary(models.Model):
    _name = "hc.measure.library"
    _description = "Measure Library"
    _inherit = ["hc.basic.association"]

    measure_id = fields.Many2one(
        comodel_name="hc.res.measure",
        string="Measure",
        help="Measure associated with this Measure Library.")
    library_id = fields.Many2one(
        comodel_name="hc.res.library",
        string="Library",
        help="Library associated with this Measure Library.")

class MeasureType(models.Model):
    _name = "hc.measure.type"
    _description = "Measure Type"
    _inherit = ["hc.basic.association"]

    measure_id = fields.Many2one(
        comodel_name="hc.res.measure",
        string="Measure",
        help="Measure associated with this Measure Type.")
    type = fields.Selection(
        string="Type",
        selection=[
            ("process", "Process"),
            ("outcome", "Outcome"),
            ("structure", "Structure"),
            ("patient-reported-outcome", "Patient Reported Outcome"),
            ("composite", "Composite")],
        help="The measure type, e.g. process, outcome.")

class MeasureGroupIdentifier(models.Model):
    _name = "hc.measure.group.identifier"
    _description = "Measure Group Identifier"
    _inherit = ["hc.basic.association", "hc.identifier"]

class MeasureGroupPopulationIdentifier(models.Model):
    _name = "hc.measure.group.population.identifier"
    _description = "Measure Group Population Identifier"
    _inherit = ["hc.basic.association", "hc.identifier"]

class MeasureGroupStratifierIdentifier(models.Model):
    _name = "hc.measure.group.stratifier.identifier"
    _description = "Measure Group Stratifier Identifier"
    _inherit = ["hc.basic.association", "hc.identifier"]

class MeasureSupplementalDataIdentifier(models.Model):
    _name = "hc.measure.supplemental.data.identifier"
    _description = "Measure Supplemental Data Identifier"
    _inherit = ["hc.basic.association", "hc.identifier"]

class MeasureSupplementalDataUsage(models.Model):
    _name = "hc.measure.supplemental.data.usage"
    _description = "Measure Supplemental Data Usage"
    _inherit = ["hc.basic.association"]

    supplemental_data_id = fields.Many2one(
        comodel_name="hc.measure.supplemental.data",
        string="Supplemental Data",
        help="Supplemental Data associated with this Measure Supplemental Data Usage.")
    usage = fields.Selection(
        string="Usage",
        selection=[
            ("supplemental-data", "Supplemental Data"),
            ("risk-adjustment-factor", "Risk Adjustment Factor")],
        help="An indicator of the intended usage for the supplemental data element.")
