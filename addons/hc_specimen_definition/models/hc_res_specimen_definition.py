# -*- coding: utf-8 -*-

from openerp import models, fields, api

class SpecimenDefinition(models.Model):
    _name = "hc.res.specimen.definition"
    _description = "Specimen Definition"
    _inherit = ["hc.domain.resource"]
    _rec_name = "name"

    name = fields.Char(
        string="Name",
        compute="_compute_name",
        store="True",
        help="Text representation of the specimen definition. Identifier + Type Collected + Time Aspect.")
    identifier_id = fields.Many2one(
        comodel_name="hc.specimen.definition.identifier",
        string="Identifier",
        help="Business identifier of a kind of specimen.")
    type_collected_id = fields.Many2one(
        comodel_name="hc.vs.v2.specimen.type",
        string="Type Collected",
        help="Kind of material to collect.")
    patient_preparation = fields.Char(
        string="Patient Preparation",
        help="Patient preparation for collection.")
    time_aspect = fields.Char(
        string="Time Aspect",
        help="Time aspect for collection.")
    collection_ids = fields.Many2many(
        comodel_name="hc.vs.specimen.collected",
        relation="specimen_definition_collection_rel",
        string="Collections",
        help="Specimen collection procedure.")
    specimen_to_lab_ids = fields.One2many(
        comodel_name="hc.specimen.definition.specimen.to.lab",
        inverse_name="specimen_definition_id",
        string="Specimen To Labs",
        help="Specimen in container intended for testing by lab.")

    @api.depends('patient_preparation', 'type_collected_id', 'time_aspect')
    def _compute_name(self):
        comp_name = '/'
        for hc_hc_res_specimen_definition in self:
            if hc_hc_res_specimen_definition.identifier_id:
                comp_name = hc_hc_res_specimen_definition.identifier_id.name or ''
            if hc_hc_res_specimen_definition.type_collected_id:
                comp_name = comp_name + ", " + hc_hc_res_specimen_definition.type_collected_id.name or ''
            if hc_hc_res_specimen_definition.time_aspect:
                comp_name = comp_name + ", " + hc_hc_res_specimen_definition.time_aspect or ''
            hc_hc_res_specimen_definition.name = comp_name

class SpecimenDefinitionSpecimenToLab(models.Model):
    _name = "hc.specimen.definition.specimen.to.lab"
    _description = "Specimen Definition Specimen To Lab"
    _inherit = ["hc.backbone.element"]

    specimen_definition_id = fields.Many2one(
        comodel_name="hc.res.specimen.definition",
        string="Specimen Definition",
        help="Specimen Definition associated with this Specimen Definition Specimen To Lab.")
    is_derived = fields.Boolean(
        string="Derived",
        required="True",
        default="True",
        help="Primary or secondary specimen.")
    type_id = fields.Many2one(
        comodel_name="hc.vs.v2.specimen.type",
        string="Type",
        help="Type of intended specimen.")
    preference = fields.Selection(
        string="Specimen To Lab Preference",
        selection=[
            ("mild", "Mild"),
            ("moderate", "Moderate"),
            ("severe", "Severe")],
        help="The preference for this type of conditioned specimen.")
    container_material_id = fields.Many2one(
        comodel_name="hc.vs.container.material",
        string="Container Material",
        help="Container material.")
    container_type_id = fields.Many2one(
        comodel_name="hc.vs.specimen.container.type",
        string="Container Type",
        help="Kind of container associated with the kind of specimen.")
    container_cap_id = fields.Many2one(
        comodel_name="hc.vs.container.cap",
        string="Container Cap",
        help="Color of container cap.")
    container_description = fields.Char(
        string="Container Description",
        help="Container description.")
    container_capacity_id = fields.Many2one(
        comodel_name="hc.specimen.definition.specimen.to.lab.container.capacity",
        string="Container Capacity",
        help="Container capacity.")
    container_minimum_volume_id = fields.Many2one(
        comodel_name="hc.specimen.definition.specimen.to.lab.container.minimum.volume",
        string="Container Minimum Volume",
        help="Minimum volume.")
    # container_capacity = fields.Float(
    #     string="Container Capacity",
    #     help="Container capacity.")
    # container_capacity_uom_id = fields.Many2one(
    #     comodel_name="product.uom",
    #     string="Container Capacity UOM",
    #     help="Container Capacity unit of measure.")
    # container_minimum_volume = fields.Float(
    #     string="Container Minimum Volume",
    #     help="Minimum volume.")
    # container_minimum_volume_uom_id = fields.Many2one(
    #     comodel_name="product.uom",
    #     string="Container Minimum Volume UOM",
    #     help="Container Minimum Volume unit of measure.")
    container_preparation = fields.Char(
        string="Container Preparation",
        help="Specimen container preparation.")
    requirement = fields.Char(
        string="Requirement",
        help="Specimen requirements.")
    retention_time_id = fields.Many2one(
        comodel_name="hc.specimen.definition.specimen.to.lab.retention.time",
        string="Retention Time",
        help="Specimen retention time.")

    # retention_time = fields.Float(
    #     string="Retention Time",
    #     help="Specimen retention time.")
    # retention_time_uom_id = fields.Many2one(
    #     comodel_name="product.uom",
    #     string="Retection Time UOM",
    #     domain="[('category_id','=','Time (UCUM)')]",
    #     help="Retention time unit of measure.")
    rejection_criterion_ids = fields.Many2many(
        comodel_name="hc.vs.rejection.criteria",
        relation="specimen_definition_specimen_to_lab_rejection_criterion_rel",
        string="Rejection Criteria",
        help="Criterion for rejection of the specimen in its container by the laboratory.")
    container_additive_ids = fields.One2many(
        comodel_name="hc.specimen.definition.specimen.to.lab.container.additive",
        inverse_name="specimen_to_lab_id",
        string="Container Additives",
        help="Additive associated with container.")
    handling_ids = fields.One2many(
        comodel_name="hc.specimen.definition.specimen.to.lab.handling",
        inverse_name="specimen_to_lab_id",
        string="Handlings",
        help="Specimen handling before testing.")

class SpecimenDefinitionSpecimenToLabContainerAdditive(models.Model):
    _name = "hc.specimen.definition.specimen.to.lab.container.additive"
    _description = "Specimen Definition Specimen To Lab Container Additive"
    _inherit = ["hc.backbone.element"]

    specimen_to_lab_id = fields.Many2one(
        comodel_name="hc.specimen.definition.specimen.to.lab",
        string="Specimen To Lab",
        help="Specimen in container intended for testing by lab.")
    additive_type = fields.Selection(
        string="Additive Type",
        required="True",
        selection=[
            ("codeable_concept", "Codeable Concept"),
            ("substance", "Substance")],
        help="Type of additive associated with container.")
    additive_name = fields.Char(
        string="Additive",
        compute="_compute_additive_name",
        store="True",
        help="Additive associated with container.")
    additive_code_id = fields.Many2one(
        comodel_name="hc.vs.v2.additive.preservative",
        string="Additive Code",
        help="Additive associated with container.")
    additive_substance_id = fields.Many2one(
        comodel_name="hc.res.substance",
        string="Additive Substance",
        help="Substance additive associated with container.")

class SpecimenDefinitionSpecimenToLabHandling(models.Model):
    _name = "hc.specimen.definition.specimen.to.lab.handling"
    _description = "Specimen Definition Specimen To Lab Handling"
    _inherit = ["hc.backbone.element"]

    specimen_to_lab_id = fields.Many2one(
        comodel_name="hc.specimen.definition.specimen.to.lab",
        string="Specimen To Lab",
        help="Specimen in container intended for testing by lab.")
    condition_set_id = fields.Many2one(
        comodel_name="hc.vs.handling.condition",
        string="Condition Set",
        help="Conservation condition set.")
    temp_range_low = fields.Float(
        string="Temp Range Low",
        help="Low limit of temperature range.")
    temp_range_high = fields.Float(
        string="Temp Range High",
        help="High limit of temperature range.")
    temp_range_uom_id = fields.Many2one(
        comodel_name="product.uom",
        string="Temp Range UOM",
        help="Temp range unit of measure.")
    max_duration_id = fields.Many2one(
        comodel_name="hc.specimen.definition.specimen.to.lab.handling.max.duration",
        string="Max Duration",
        help="Maximum conservation time.")
    # max_duration = fields.Float(
    #     string="Maximum Duration",
    #     help="Maximum conservation time.")
    # max_duration_uom_id = fields.Many2one(
    #     comodel_name="product.uom",
    #     string="Maximum Duration UOM",
    #     domain="[('category_id','=','Time (UCUM)')]",
    #     help="Maximum duration unit of measure.")
    light_exposure = fields.Char(
        string="Light Exposure",
        help="Light exposure.")
    instruction = fields.Char(
        string="Instruction",
        help="Conservation instruction.")

class SpecimenDefinitionIdentifier(models.Model):
    _name = "hc.specimen.definition.identifier"
    _description = "Specimen Definition Identifier"
    _inherit = ["hc.basic.association", "hc.identifier"]

    specimen_definition_id = fields.Many2one(
        comodel_name="hc.res.specimen.definition",
        string="Specimen Definition",
        help="Specimen Definition associated with this Specimen Definition Identifier.")

class SpecimenDefinitionSpecimenToLabContainerCapacity(models.Model):
    _name = "hc.specimen.definition.specimen.to.lab.container.capacity"
    _description = "Specimen Definition Specimen To Lab Container Capacity"
    _inherit = ["hc.basic.association", "hc.simple.quantity"]

    # specimen_to_lab_id = fields.Many2one(
    #     comodel_name="hc.specimen.definition.specimen.to.lab",
    #     string="Specimen To Lab",
    #     help="Specimen To Lab associated with this Specimen Definition Specimen To Lab Container Capacity.")

class SpecimenDefinitionSpecimenToLabContainerMinimumVolume(models.Model):
    _name = "hc.specimen.definition.specimen.to.lab.container.minimum.volume"
    _description = "Specimen Definition Specimen To Lab Container Minimum Volume"
    _inherit = ["hc.basic.association", "hc.simple.quantity"]

    specimen_to_lab_id = fields.Many2one(
        comodel_name="hc.specimen.definition.specimen.to.lab",
        string="Specimen To Lab",
        help="Specimen To Lab associated with this Specimen Definition Specimen To Lab Container Minimum Volume.")

class SpecimenDefinitionSpecimenToLabRetentionTime(models.Model):
    _name = "hc.specimen.definition.specimen.to.lab.retention.time"
    _description = "Specimen Definition Specimen To Lab Retention Time"
    _inherit = ["hc.basic.association", "hc.duration"]

    specimen_to_lab_id = fields.Many2one(
        comodel_name="hc.specimen.definition.specimen.to.lab",
        string="Specimen To Lab",
        help="Specimen To Lab associated with this Specimen Definition Specimen To Lab Retention Time.")

class SpecimenDefinitionSpecimenToLabHandlingMaxDuration(models.Model):
    _name = "hc.specimen.definition.specimen.to.lab.handling.max.duration"
    _description = "Specimen Definition Specimen To Lab Handling Max Duration"
    _inherit = ["hc.basic.association", "hc.duration"]

    handling_id = fields.Many2one(
        comodel_name="hc.specimen.definition.specimen.to.lab.handling",
        string="Handling",
        help="Handling associated with this Specimen Definition Specimen To Lab Handling Max Duration.")

class ContainerMaterial(models.Model):
    _name = "hc.vs.container.material"
    _description = "Container Material"
    _inherit = ["hc.value.set.contains"]

    name = fields.Char(
        string="Name",
        help="Name of this container material.")
    code = fields.Char(
        string="Code",
        help="Code of this container material.")
    contains_id = fields.Many2one(
        comodel_name="hc.vs.container.material",
        string="Parent",
        help="Parent concept.")

class SpecimenContainedPreference(models.Model):
    _name = "hc.vs.specimen.contained.preference"
    _description = "Specimen Contained Preference"
    _inherit = ["hc.value.set.contains"]

    name = fields.Char(
        string="Name",
        help="Name of this specimen contained preference.")
    code = fields.Char(
        string="Code",
        help="Code of this specimen contained preference.")
    contains_id = fields.Many2one(
        comodel_name="hc.vs.specimen.contained.preference",
        string="Parent",
        help="Parent concept.")

class ContainerCap(models.Model):
    _name = "hc.vs.container.cap"
    _description = "Container Cap"
    _inherit = ["hc.value.set.contains"]

    name = fields.Char(
        string="Name",
        help="Name of this container cap.")
    code = fields.Char(
        string="Code",
        help="Code of this container cap.")
    contains_id = fields.Many2one(
        comodel_name="hc.vs.container.cap",
        string="Parent",
        help="Parent concept.")

class V2AdditivePreservative(models.Model):
    _name = "hc.vs.v2.additive.preservative"
    _description = "V2 Additive Preservative"
    _inherit = ["hc.value.set.contains"]

    name = fields.Char(
        string="Name",
        help="Name of this additive preservative.")
    code = fields.Char(
        string="Code",
        help="Code of this additive preservative.")
    contains_id = fields.Many2one(
        comodel_name="hc.vs.v2.additive.preservative",
        string="Parent",
        help="Parent concept.")

class RejectionCriteria(models.Model):
    _name = "hc.vs.rejection.criteria"
    _description = "Rejection Criteria"
    _inherit = ["hc.value.set.contains"]

    name = fields.Char(
        string="Name",
        help="Name of this rejection criteria.")
    code = fields.Char(
        string="Code",
        help="Code of this rejection criteria.")
    contains_id = fields.Many2one(
        comodel_name="hc.vs.rejection.criteria",
        string="Parent",
        help="Parent concept.")

class HandlingCondition(models.Model):
    _name = "hc.vs.handling.condition"
    _description = "Handling Condition"
    _inherit = ["hc.value.set.contains"]

    name = fields.Char(
        string="Name",
        help="Name of this handling condition.")
    code = fields.Char(
        string="Code",
        help="Code of this handling condition.")
    contains_id = fields.Many2one(
        comodel_name="hc.vs.handling.condition",
        string="Parent",
        help="Parent concept.")

class SpecimenCollected(models.Model):
    _name = "hc.vs.specimen.collected"
    _description = "Specimen Collected"
    _inherit = ["hc.value.set.contains"]

    name = fields.Char(
        string="Name",
        help="Name of this specimen collected.")
    code = fields.Char(
        string="Code",
        help="Code of this specimen collected.")
    contains_id = fields.Many2one(
        comodel_name="hc.vs.specimen.collected",
        string="Parent",
        help="Parent concept.")
