# -*- coding: utf-8 -*-

from openerp import models, fields, api

class ImplementationGuideOutput(models.Model):
    _name = "hc.res.implementation.guide.output"
    _description = "Implementation Guide Output"
    _inherit = ["hc.domain.resource"]
    _rec_name = "name"

    url = fields.Char(
        string="URI",
        required="True",
        help="Logical URI to reference this implementation guide output (globally unique).")
    version = fields.Char(
        string="Version",
        help="Business version of the implementation guide output.")
    name = fields.Char(
        string="Name",
        required="True",
        help="Name for this implementation guide output (computer friendly).")
    status_id = fields.Many2one(
        comodel_name="hc.vs.publication.status",
        string="Status",
        required="True",
        help="The status of this implementation guide output. Enables tracking the life-cycle of the content.")
    is_experimental = fields.Boolean(
        string="Experimental",
        help="For testing purposes, not real usage.")
    date = fields.Datetime(
        string="Date",
        help="Date this was last changed.")
    publisher = fields.Char(
        string="Publisher",
        help="Name of the publisher (organization or individual).")
    contact_ids = fields.One2many(
        comodel_name="hc.implementation.guide.output.contact",
        inverse_name="implementation_guide_output_id",
        string="Contacts",
        help="Contact details for the publisher.")
    description = fields.Text(
        string="Description",
        help="Natural language description of the implementation guide output.")
    use_context_ids = fields.One2many(
        comodel_name="hc.implementation.guide.output.use.context",
        inverse_name="implementation_guide_output_id",
        string="Use Contexts",
        help="Context the content is intended to support.")
    jurisdiction_ids = fields.Many2many(
        comodel_name="hc.vs.jurisdiction",
        relation="implementation_guide_output_jurisdiction_rel",
        string="Jurisdictions",
        help="Intended jurisdiction for implementation guide output (if applicable).")
    copyright = fields.Text(
        string="Copyright",
        help="Use and/or publishing restrictions.")
    fhir_version = fields.Char(
        string="FHIR Version",
        help="FHIR Version this Implementation Guide targets.")
    dependency_ids = fields.One2many(
        comodel_name="hc.implementation.guide.output.dependency",
        inverse_name="implementation_guide_output_id",
        string="Dependencies",
        help="Another Implementation guide this depends on.")
    resource_ids = fields.One2many(
        comodel_name="hc.implementation.guide.output.resource",
        inverse_name="implementation_guide_output_id",
        string="Resources",
        help="Resource in the implementation guide.")
    global_ids = fields.One2many(
        comodel_name="hc.implementation.guide.output.global",
        inverse_name="implementation_guide_output_id",
        string="Globals",
        help="Profiles that apply globally.")
    rendering = fields.Char(
        string="Rendering URI",
        help="Location of rendered implementation guide.")
    page_ids = fields.One2many(
        comodel_name="hc.implementation.guide.output.page",
        inverse_name="implementation_guide_output_id",
        string="Pages",
        help="HTML page within the parent IG.")
    image_ids = fields.One2many(
        comodel_name="hc.implementation.guide.output.image",
        inverse_name="implementation_guide_output_id",
        string="Images",
        help="Image within the IG.")
    other_ids = fields.One2many(
        comodel_name="hc.implementation.guide.output.other",
        inverse_name="implementation_guide_output_id",
        string="Others",
        help="Additional linkable file in IG.")

class ImplementationGuideOutputDependency(models.Model):
    _name = "hc.implementation.guide.output.dependency"
    _description = "Implementation Guide Output Dependency"
    _inherit = ["hc.backbone.element"]

    implementation_guide_output_id = fields.Many2one(
        comodel_name="hc.res.implementation.guide.output",
        string="Implementation Guide Output",
        help="Implementation Guide Output associated with this Implementation Guide Output Dependency.")
    type = fields.Selection(
        string="Type",
        required="True",
        selection=[
            ("reference", "Reference"),
            ("inclusion", "Inclusion")],
        help="How the dependency is represented when the guide is published.")
    uri = fields.Char(
        string="URI",
        required="True",
        help="Where to find dependency.")

class ImplementationGuideOutputResource(models.Model):
    _name = "hc.implementation.guide.output.resource"
    _description = "Implementation Guide Output Resource"
    _inherit = ["hc.backbone.element"]

    implementation_guide_output_id = fields.Many2one(
        comodel_name="hc.res.implementation.guide.output",
        string="Implementation Guide Output",
        help="Implementation Guide Output associated with this Implementation Guide Output Resource.")
    reference_type = fields.Char(
        string="Reference Type",
        compute="_compute_reference_type",
        store="True",
        help="Type of location of the resource.")
    reference_name = fields.Reference(
        string="Reference",
        selection="_reference_models",
        help="Location of the resource.")
    example_type = fields.Selection(
        string="Example Type",
        selection=[
            ("boolean", "Boolean"),
            ("structure_definition", "Structure Definition")],
        help="Type of additive associated with container.")
    example_name = fields.Char(
        string="Example",
        compute="_compute_example_name",
        store="True",
        help="Is an example/What is this an example of?")
    example_boolean = fields.Boolean(
        string="Example Boolean",
        help="Code of is an example/what is this an example of?")
    example_structure_definition_id = fields.Many2one(
        comodel_name="hc.res.structure.definition",
        string="Example Structure Definition",
        help="Structure Definition is an example/what is this an example of?")
    relative_path = fields.Char(
        string="Relative Path",
        help="Relative path for page in IG.")

    @api.model
    def _reference_models(self):
        models = self.env['ir.model'].search([('state','!=','manual')])
        return [(model.model, model.name)
            for model in models
                if model.model.startswith('hc.res')]

    @api.depends('reference_name')
    def _compute_reference_type(self):
        for this in self:
            if this.reference_name:
                this.reference_type = this.reference_name._description

class ImplementationGuideOutputGlobal(models.Model):
    _name = "hc.implementation.guide.output.global"
    _description = "Implementation Guide Output Global"
    _inherit = ["hc.backbone.element"]

    implementation_guide_output_id = fields.Many2one(
        comodel_name="hc.res.implementation.guide.output",
        string="Implementation Guide Output",
        help="Implementation Guide Output associated with this Implementation Guide Output Global.")
    type_id = fields.Many2one(
        comodel_name="hc.vs.resource.type",
        string="Type",
        required="True",
        help="Type this profiles applies to.")
    profile_id = fields.Many2one(
        comodel_name="hc.res.structure.definition",
        string="Profile",
        help="Structure Definition associated with this Implementation Guide Output Global.")

class ImplementationGuideOutputPage(models.Model):
    _name = "hc.implementation.guide.output.page"
    _description = "Implementation Guide Output Page"
    _inherit = ["hc.backbone.element"]

    implementation_guide_output_id = fields.Many2one(
        comodel_name="hc.res.implementation.guide.output",
        string="Implementation Guide Output",
        help="Implementation Guide Output associated with this Implementation Guide Output Page.")
    name = fields.Char(
        string="Name",
        required="True",
        help="HTML page name.")
    title = fields.Char(
        string="Title",
        help="Title of the page.")
    anchor = fields.Char(
        string="Anchor",
        help="Anchor available on the page.")

class ImplementationGuideOutputContact(models.Model):
    _name = "hc.implementation.guide.output.contact"
    _description = "Implementation Guide Output Contact"
    _inherit = ["hc.basic.association"]
    _inherits = {"hc.contact.detail": "contact_id"}

    contact_id = fields.Many2one(
        comodel_name="hc.contact.detail",
        string="Contact",
        ondelete="restrict",
        required="True",
        help="Contact Detail associated with this Implementation Guide Output Contact.")
    implementation_guide_output_id = fields.Many2one(
        comodel_name="hc.res.implementation.guide.output",
        string="Implementation Guide Output",
        help="Implementation Guide Output associated with this Implementation Guide Output Contact.")

class ImplementationGuideOutputUseContext(models.Model):
    _name = "hc.implementation.guide.output.use.context"
    _description = "Implementation Guide Output Use Context"
    _inherit = ["hc.basic.association", "hc.usage.context"]

    implementation_guide_output_id = fields.Many2one(
        comodel_name="hc.res.implementation.guide.output",
        string="Implementation Guide Output",
        help="Implementation Guide Output associated with this Implementation Guide Output Use Context.")

class ImplementationGuideOutputImage(models.Model):
    _name = "hc.implementation.guide.output.image"
    _description = "Implementation Guide Output Image"
    _inherit = ["hc.basic.association"]

    implementation_guide_output_id = fields.Many2one(
        comodel_name="hc.res.implementation.guide.output",
        string="Implementation Guide Output",
        help="Implementation Guide Output associated with this Implementation Guide Output Image.")
    image = fields.Char(
        string="Image",
        help="Image associated with this Implementation Guide Output Image.")

class ImplementationGuideOutputOther(models.Model):
    _name = "hc.implementation.guide.output.other"
    _description = "Implementation Guide Output Other"
    _inherit = ["hc.basic.association"]

    implementation_guide_output_id = fields.Many2one(
        comodel_name="hc.res.implementation.guide.output",


































































        string="Implementation Guide Output", help="Implementation Guide Output associated with this Implementation Guide Output Other.")
    other = fields.Char(string="Other", help="Other associated with this Implementation Guide Output Other.")
