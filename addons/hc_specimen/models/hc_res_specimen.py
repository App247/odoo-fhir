# -*- coding: utf-8 -*-

from openerp import models, fields, api

class Specimen(models.Model):
    _name = "hc.res.specimen"
    _description = "Specimen"

    name = fields.Char(
        string="Event Name",
        compute="_compute_name",
        store="True",
        help="Text representation of the specimen event. Subject Name + Accession Identifier + Received Time.")
    identifier_ids = fields.One2many(
        comodel_name="hc.specimen.identifier",
        inverse_name="specimen_id",
        string="Identifiers",
        help="External Identifier.")
    accession_identifier_id = fields.Many2one(
        comodel_name="hc.specimen.accession.identifier",
        string="Accession Identifier",
        help="Identifier assigned by the lab.")
    status = fields.Selection(
        string="Status",
        selection=[
            ("available", "Available"),
            ("unavailable", "Unavailable"),
            ("unsatisfactory", "Unsatisfactory"),
            ("entered-in-error", "Entered-In-Error")],
        help="The availability of the specimen.")
    type_id = fields.Many2one(
        comodel_name="hc.vs.v2.specimen.type",
        string="Type",
        help="Kind of material that forms the specimen.")
    subject_type = fields.Selection(
        string="Subject Type",
        required="True",
        selection=[
            ("patient", "Patient"),
            ("group", "Group"),
            ("device", "Device"),
            ("substance", "Substance")],
        help="Type of who has the condition.")
    subject_name = fields.Char(
        string="Subject",
        compute="_compute_subject_name",
        required="True",
        help="Where the specimen came from. This may be from the patient(s) or from the environment or a device.")
    subject_patient_id = fields.Many2one(
        comodel_name="hc.res.patient",
        string="Subject Patient",
        help="Patient where the specimen came from.")
    subject_group_id = fields.Many2one(
        comodel_name="hc.res.group",
        string="Subject Group",
        help="Group where the specimen came from.")
    subject_device_id = fields.Many2one(
        comodel_name="hc.res.device",
        string="Subject Device",
        help="Device where the specimen came from.")
    subject_substance_id = fields.Many2one(
        comodel_name="hc.res.substance",
        string="Subject Substance",
        help="Substance where the specimen came from.")
    received_time = fields.Datetime(
        string="Received Time",
        help="The time when specimen was received for processing.")
    parent_specimen_ids = fields.Many2many(
        comodel_name="hc.specimen.parent",
        string="Parent Specimens",
        help="Specimen from which this specimen originated.")
    request_ids = fields.One2many(
        comodel_name="hc.specimen.request",
        inverse_name="specimen_id",
        string="Requests",
        help="Why the specimen was collected.")
    note_ids = fields.One2many(
        comodel_name="hc.specimen.note",
        inverse_name="specimen_id",
        string="Notes",
        help="Comments.")
    collection_ids = fields.One2many(
        comodel_name="hc.specimen.collection",
        inverse_name="specimen_id",
        string="Collections",
        help="Collection details.")
    treatment_ids = fields.One2many(
        comodel_name="hc.specimen.treatment",
        inverse_name="specimen_id",
        string="Treatments",
        help="Treatment and processing step details.")
    container_ids = fields.One2many(
        comodel_name="hc.specimen.container",
        inverse_name="specimen_id",
        string="Containers",
        help="Direct container of specimen (tube/slide, etc).")

class SpecimenParent(models.Model):
    _name = "hc.specimen.parent"
    _description = "Specimen Parent"
    _inherit = ["hc.basic.association"]
    _inherits = {"hc.res.specimen": "specimen_id"}

    specimen_id = fields.Many2one(
        comodel_name="hc.res.specimen",
        string="Specimen",
        required="true",
        ondelete="restrict",
        help="Specimen that is the originator of another specimen.")
    child_specimen_ids = fields.Many2many(
        comodel_name="hc.res.specimen",
        string="Child Specimens",
        help="Specimen that originated from this specimen.")

class SpecimenCollection(models.Model):
    _name = "hc.specimen.collection"
    _description = "Specimen Collection"

    specimen_id = fields.Many2one(
        comodel_name="hc.res.specimen",
        string="Specimen",
        help="Specimen associated with this Specimen Collection.")
    collector_practitioner_id = fields.Many2one(
        comodel_name="hc.res.practitioner",
        string="Collector Practitioner",
        help="Who collected the specimen.")
    collected_type = fields.Selection(
        string="Collected Type",
        selection=[
            ("date_time", "Date Time"),
            ("period", "Period")],
        help="Type of collection time.")
    collected_name = fields.Char(
        string="Collected",
        compute="_compute_collected_name",
        help="Collection time.")
    collected_date_time = fields.Datetime(
        string="Collected Date Time",
        help="Collection time.")
    start_date = fields.Datetime(
        string="Start Date",
        help="Start of the collection time.")
    end_date = fields.Datetime(
        string="End Date",
        help="End of the collection time.")
    quantity = fields.Float(
        string="Quantity",
        help="The quantity of specimen collected.")
    quantity_uom_id = fields.Many2one(
        comodel_name="product.uom",
        string="Quantity UOM",
        help="Quantity unit of measure.")
    method_id = fields.Many2one(
        comodel_name="hc.vs.specimen.collection.method",
        string="Method",
        help="Technique used to perform collection.")
    body_site_type = fields.Selection(
        string="Body Site Type",
        selection=[
            ("code", "Code"),
            ("body_site", "Body Site")],
        help="Type of anatomical collection site.")
    body_site_name = fields.Char(
        string="Body Site",
        compute="_compute_body_site_name",
        help="Anatomical collection site.")
    body_site_code_id = fields.Many2one(
        comodel_name="hc.vs.body.site",
        string="Body Site Code",
        help="Code of anatomical collection site.")
    body_site_id = fields.Many2one(
        comodel_name="hc.res.body.site",
        string="Body Site",
        help="Body Site anatomical collection site.")

class SpecimenTreatment(models.Model):
    _name = "hc.specimen.treatment"
    _description = "Specimen Treatment"

    specimen_id = fields.Many2one(
        comodel_name="hc.res.specimen",
        string="Specimen",
        help="Specimen associated with this Specimen Treatment.")
    description = fields.Text(
        string="Description",
        help="Textual description of procedure.")
    procedure_id = fields.Many2one(
        comodel_name="hc.vs.specimen.treatment.procedure",
        string="Procedure",
        help="Indicates the treatment or processing step applied to the specimen.")
    additive_substance_ids = fields.One2many(
        comodel_name="hc.specimen.treatment.substance",
        inverse_name="treatment_id",
        string="Additive Substances",
        help="Material used in the processing step.")

class SpecimenContainer(models.Model):
    _name = "hc.specimen.container"
    _description = "Specimen Container"

    specimen_id = fields.Many2one(
        comodel_name="hc.res.specimen",
        string="Specimen",
        help="Specimen associated with this Specimen Container.")
    identifier_ids = fields.One2many(
        comodel_name="hc.specimen.container.identifier",
        inverse_name="container_id",
        string="Identifiers",
        help="Id for the container.")
    description = fields.Text(
        string="Description",
        help="Textual description of the container.")
    type_id = fields.Many2one(
        comodel_name="hc.vs.specimen.container.type",
        string="Type",
        help="Kind of container directly associated with specimen.")
    capacity = fields.Float(
        string="Capacity",
        help="Container volume or size.")
    capacity_uom_id = fields.Many2one(
        comodel_name="product.uom",
        string="Capacity UOM",
        help="Capacity unit of measure.")
    specimen_quantity = fields.Float(
        string="Specimen Quantity",
        help="Quantity of specimen within container.")
    specimen_quantity_uom_id = fields.Many2one(
        comodel_name="product.uom",
        string="Specimen Quantity UOM",
        help="Specimen quantity unit of measure.")
    additive_type = fields.Selection(
        string="Additive Type",
        selection=[
            ("code", "Code"),
            ("substance", "Substance")],
        help="Type of additive associated with container.")
    additive_name = fields.Char(
        string="Additive",
        compute="_compute_additive_name",
        help="Additive associated with container.")
    additive_code_id = fields.Many2one(
        comodel_name="hc.vs.v2.additive.preservative",
        string="Additive Code",
        help="Code of additive associated with container.")
    additive_substance_id = fields.Many2one(
        comodel_name="hc.res.substance",
        string="Additive Substance",
        help="Substance additive associated with container.")

class SpecimenAccessionIdentifier(models.Model):
    _name = "hc.specimen.accession.identifier"
    _description = "Specimen Accession Identifier"
    _inherit = ["hc.identifier"]

class SpecimenContainerIdentifier(models.Model):
    _name = "hc.specimen.container.identifier"
    _description = "Specimen Container Identifier"
    _inherit = ["hc.basic.association", "hc.identifier"]

    container_id = fields.Many2one(
        comodel_name="hc.specimen.container",
        string="Specimen Container",
        help="Container associated with this Specimen Container Identifier.")

class SpecimenIdentifier(models.Model):
    _name = "hc.specimen.identifier"
    _description = "Specimen Identifier"
    _inherit = ["hc.basic.association", "hc.identifier"]

    specimen_id = fields.Many2one(
        comodel_name="hc.res.specimen",
        string="Specimen",
        help="Specimen associated with this Specimen Identifier.")

class SpecimenNote(models.Model):
    _name = "hc.specimen.note"
    _description = "Specimen Note"
    _inherit = ["hc.basic.association", "hc.annotation"]

    specimen_id = fields.Many2one(
        comodel_name="hc.res.specimen",
        string="Specimen",
        help="Specimen associated with this Specimen Note.")

class SpecimenRequest(models.Model):
    _name = "hc.specimen.request"
    _description = "Specimen Request"
    _inherit = ["hc.basic.association"]

    specimen_id = fields.Many2one(
        comodel_name="hc.res.specimen",
        string="Specimen",
        help="Specimen associated with this Specimen Request.")
    request_id = fields.Many2one(
        comodel_name="hc.res.procedure.request",
        string="Request",
        help="Procedure Request why the specimen was collected.")

class SpecimenTreatmentSubstance(models.Model):
    _name = "hc.specimen.treatment.substance"
    _description = "Specimen Treatment Substance"
    _inherit = ["hc.basic.association"]

    treatment_id = fields.Many2one(
        comodel_name="hc.specimen.treatment",
        string="Specimen Treatment",
        help="Treatment associated with this Specimen Treatment Substance.")
    additive_id = fields.Many2one(
        comodel_name="hc.res.substance",
        string="Additive",
        help="Additive associated with this Specimen Treatment Substance.")

class SpecimenCollectionMethod(models.Model):
    _name = "hc.vs.specimen.collection.method"
    _description = "Specimen Collection Method"
    _inherit = ["hc.value.set.contains"]

class SpecimenContainerType(models.Model):
    _name = "hc.vs.specimen.container.type"
    _description = "Specimen Container Type"
    _inherit = ["hc.value.set.contains"]

class SpecimenTreatmentProcedure(models.Model):
    _name = "hc.vs.specimen.treatment.procedure"
    _description = "Specimen Treatment Procedure"
    _inherit = ["hc.value.set.contains"]

class V2AdditivePreservative(models.Model):
    _name = "hc.vs.v2.additive.preservative"
    _description = "V2 Additive Preservative"
    _inherit = ["hc.value.set.contains"]

class V2SpecimenType(models.Model):
    _name = "hc.vs.v2.specimen.type"
    _description = "V2 Specimen Type"
    _inherit = ["hc.value.set.contains"]