# -*- coding: utf-8 -*-

from openerp import models, fields, api

class ImplementationGuideInput(models.Model):
    _name = "hc.res.implementation.guide.input"
    _description = "Implementation Guide Input"
    _inherit = ["hc.domain.resource"]

    url = fields.Char(
        string="URI",
        required="True",
        help="Logical URI to reference this implementation guide input (globally unique).")
    version = fields.Char(
        string="Version",
        help="Business version of the implementation guide input.")
    name = fields.Char(
        string="Name",
        required="True",
        help="Name for this implementation guide input (computer friendly).")
    status_id = fields.Many2one(
        comodel_name="hc.vs.publication.status",
        string="Status",
        required="True",
        help="The status of this implementation guide input. Enables tracking the life-cycle of the content.")
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
        comodel_name="hc.implementation.guide.input.contact",
        inverse_name="implementation_guide_input_id",
        string="Contacts",
        help="Contact details for the publisher.")
    description = fields.Text(
        string="Description",
        help="Natural language description of the implementation guide input.")
    use_context_ids = fields.One2many(
        comodel_name="hc.implementation.guide.input.use.context",
        inverse_name="implementation_guide_input_id",
        string="Use Contexts",
        help="Context the content is intended to support.")
    jurisdiction_ids = fields.Many2many(
        comodel_name="hc.vs.jurisdiction",
        relation="implementation_guide_input_jurisdiction_rel",
        string="Jurisdictions",
        help="Intended jurisdiction for implementation guide input (if applicable).")
    copyright = fields.Text(
        string="Copyright",
        help="Use and/or publishing restrictions.")
    fhir_version = fields.Char(
        string="FHIR Version",
        help="FHIR Version this Implementation Guide targets.")
    dependency_ids = fields.One2many(
        comodel_name="hc.implementation.guide.input.dependency",
        inverse_name="implementation_guide_input_id",
        string="Dependencies",
        help="Another Implementation guide this depends on.")
    package_ids = fields.One2many(
        comodel_name="hc.implementation.guide.input.package",
        inverse_name="implementation_guide_input_id",
        string="Packages",
        help="Group of resources as used in .page.package.")
    global_ids = fields.One2many(
        comodel_name="hc.implementation.guide.input.global",
        inverse_name="implementation_guide_input_id",
        string="Globals",
        help="Profiles that apply globally.")
    page_ids = fields.One2many(
        comodel_name="hc.implementation.guide.input.page",
        inverse_name="implementation_guide_input_id",
        string="Pages",
        help="Page/Section in the Guide.")

class ImplementationGuideInputDependency(models.Model):
    _name = "hc.implementation.guide.input.dependency"
    _description = "Implementation Guide Input Dependency"
    _inherit = ["hc.backbone.element"]

    implementation_guide_input_id = fields.Many2one(
        comodel_name="hc.res.implementation.guide.input",
        string="Implementation Guide Input",
        help="Implementation Guide Input associated with this Implementation Guide Input Dependency.")
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

class ImplementationGuideInputPackage(models.Model):
    _name = "hc.implementation.guide.input.package"
    _description = "Implementation Guide Input Package"
    _inherit = ["hc.backbone.element"]

    implementation_guide_input_id = fields.Many2one(
        comodel_name="hc.res.implementation.guide.input",
        string="Implementation Guide Input",
        help="Implementation Guide Input associated with this Implementation Guide Input Package.")
    name = fields.Char(
        string="Name",
        required="True",
        help="Name used .page.package.")
    description = fields.Text(
        string="Description",
        help="Human readable text describing the package.")
    resource_ids = fields.One2many(
        comodel_name="hc.implementation.guide.input.package.resource",
        inverse_name="package_id",
        string="Resources",
        help="Resource in the implementation guide.")

class ImplementationGuideInputPackageResource(models.Model):
    _name = "hc.implementation.guide.input.package.resource"
    _description = "Implementation Guide Input Package Resource"
    _inherit = ["hc.backbone.element"]

    package_id = fields.Many2one(
        comodel_name="hc.implementation.guide.input.package",
        string="Package",
        help="Group of resources as used in .page.package.")
    reference_type = fields.Char(
        string="Reference Type",
        compute="_compute_reference_type",
        store="True",
        help="Type of location of the resource.")
    reference_name = fields.Reference(
        string="Reference",
        selection="_reference_models",
        help="Location of the resource.")
    name = fields.Char(
        string="Name",
        help="Human Name for the resource.")
    description = fields.Text(
        string="Description",
        help="Reason why included in guide.")
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
        help="Boolean of is an example/what is this an example of?")
    example_structure_definition_id = fields.Many2one(
        comodel_name="hc.res.structure.definition",
        string="Example Structure Definition",
        help="Structure Definition is an example/what is this an example of?")

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

    @api.multi
    def _compute_example_name(self):
        for hc.implementation.guide.input.package.resource in self:
            if hc.implementation.guide.input.package.resource.example_type == 'boolean':
                hc.implementation.guide.input.package.resource.example_name = hc.implementation.guide.input.package.resource.example_boolean
            elif hc.implementation.guide.input.package.resource.example_type == 'structure_definition':
                hc.implementation.guide.input.package.resource.example_name = hc.implementation.guide.input.package.resource.example_structure_definition_id.name


class ImplementationGuideInputGlobal(models.Model):
    _name = "hc.implementation.guide.input.global"
    _description = "Implementation Guide Input Global"
    _inherit = ["hc.backbone.element"]

    implementation_guide_input_id = fields.Many2one(
        comodel_name="hc.res.implementation.guide.input",
        string="Implementation Guide Input",
        help="Implementation Guide Input associated with this Implementation Guide Input Global.")
    type_id = fields.Many2one(
        comodel_name="hc.vs.resource.type",
        string="Type",
        required="True",
        help="Type this profiles applies to.")
    profile_id = fields.Many2one(
        comodel_name="hc.res.structure.definition",
        string="Profile",
        help="Structure Definition associated with this Implementation Guide Input Global.")

class ImplementationGuideInputPage(models.Model):
    _name = "hc.implementation.guide.input.page"
    _description = "Implementation Guide Input Page"
    _inherit = ["hc.backbone.element"]

    implementation_guide_input_id = fields.Many2one(
        comodel_name="hc.res.implementation.guide.input",
        string="Implementation Guide Input",
        help="Implementation Guide Input associated with this Implementation Guide Input Page.")
    source_type = fields.Selection(
        string="Source Type",
        required="True",
        selection=[
            ("uri", "URI"),
            ("binary", "Binary")],
        help="Type of where to find that page.")
    source_name = fields.Char(
        string="Source",
        compute="_compute_source_name",
        store="True",
        help="Where to find that page.")
    source_uri = fields.Char(
        string="Source URI",
        help="Code of where to find that page.")
    source_binary_id = fields.Many2one(
        comodel_name="hc.res.binary",
        string="Source Binary",
        help="Binary where to find that page")
    title = fields.Char(
        string="Title",
        required="True",
        help="Short title shown for navigational assistance.")
    kind = fields.Selection(
        string="Kind",
        required="True",
        selection=[
            ("page", "Page"),
            ("example", "Example"),
            ("list", "List"),
            ("include", "Include"),
            ("directory", "Directory"),
            ("dictionary", "Dictionary"),
            ("toc", "TOC"),
            ("resource", "Resource")],
        help="The kind of page that this is. Some pages are autogenerated (list, example), and other kinds are of interest so that tools can navigate the user to the page of interest.")
    type_ids = fields.Many2many(
        comodel_name="hc.vs.resource.type",
        relation="implementation_guide_input_page_type_rel",
        string="Types",
        help="of resource to include in the list.")
    package_ids = fields.One2many(
        comodel_name="hc.implementation.guide.input.page.package",
        inverse_name="page_id",
        string="Packages",
        help="Name of package to include.")
    format_id = fields.Many2one(
        comodel_name="hc.vs.resource.type",
        string="Format",
        help="Format of the page (e.g. html, markdown, etc.).")
    page_ids = fields.One2many(
        comodel_name="hc.implementation.guide.input.page.page",
        inverse_name="page_id",
        string="Pages",
        help="Content as for ImplementationGuideInput.page Nested Pages / Sections.")

    @api.depends('source_type')
    def _compute_source_name(self):
        for hc_implementation_guide_input_page in self:
            if hc_implementation_guide_input_page.source_type == 'uri':
                hc_implementation_guide_input_page.source_name = hc_implementation_guide_input_page.source_uri
            elif hc_implementation_guide_input_page.source_type == 'binary':
                hc_implementation_guide_input_page.source_name = hc_implementation_guide_input_page.source_binary_id.name

class ImplementationGuideInputContact(models.Model):
    _name = "hc.implementation.guide.input.contact"
    _description = "Implementation Guide Input Contact"
    _inherit = ["hc.basic.association"]
    _inherits = {"hc.contact.detail": "contact_id"}

    contact_id = fields.Many2one(
        comodel_name="hc.contact.detail",
        string="Contact",
        ondelete="restrict",
        required="True",
        help="Contact Detail associated with this Implementation Guide Input Contact.")
    implementation_guide_input_id = fields.Many2one(
        comodel_name="hc.res.implementation.guide.input",
        string="Implementation Guide Input",
        help="Implementation Guide Input associated with this Implementation Guide Input Contact.")

class ImplementationGuideInputUseContext(models.Model):
    _name = "hc.implementation.guide.input.use.context"
    _description = "Implementation Guide Input Use Context"
    _inherit = ["hc.basic.association", "hc.usage.context"]

    implementation_guide_input_id = fields.Many2one(
        comodel_name="hc.res.implementation.guide.input",
        string="Implementation Guide Input",
        help="Implementation Guide Input associated with this Implementation Guide Input Use Context.")

class ImplementationGuideInputPagePackage(models.Model):
    _name = "hc.implementation.guide.input.page.package"
    _description = "Implementation Guide Input Page Package"
    _inherit = ["hc.basic.association"]

    page_id = fields.Many2one(
        comodel_name="hc.implementation.guide.input.page",
        string="Page",
        help="Page associated with this Implementation Guide Input Page Package.")
    package = fields.Char(
        string="Package",
        help="Package associated with this Implementation Guide Input Page Package.")

class ImplementationGuideInputPagePage(models.Model):
    _name = "hc.implementation.guide.input.page.page"
    _description = "Implementation Guide Input Page Page"
    _inherit = ["hc.basic.association"]

    page_id = fields.Many2one(
        comodel_name="hc.implementation.guide.input.page",
        string="Page",
        help="Page associated with this Implementation Guide Input Page Page.")
    page_id = fields.Many2one(
        comodel_name="hc.implementation.guide.input.page",
        string="Page",
        help="Page associated with this Implementation Guide Input Page Page.")
