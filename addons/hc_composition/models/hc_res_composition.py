# -*- coding: utf-8 -*-

from openerp import models, fields, api
from datetime import datetime
from openerp.tools import DEFAULT_SERVER_DATETIME_FORMAT as DTF

class Composition(models.Model):
    _name = "hc.res.composition"
    _description = "Composition"
    _inherit = ["hc.domain.resource"]
    _rec_name = "title"

    identifier_id = fields.Many2one(
        comodel_name="hc.composition.identifier",
        string="Identifier",
        help="Logical identifier of composition (version-independent).")
    status = fields.Selection(
        string="Status",
        required="True",
        selection=[
            ("preliminary", "Preliminary"),
            ("final", "Final"),
            ("amended", "Amended"),
            ("entered-in-error", "Entered-In-Error")],
        default="preliminary",
        help="The workflow/clinical status of this composition.")
    status_history_ids = fields.One2many(
        comodel_name="hc.composition.status.history",
        inverse_name="composition_id",
        string="Status History",
        help="The status of the composition over time.")
    type_id = fields.Many2one(
        comodel_name="hc.vs.doc.type.code",
        string="Type",
        required="True",
        help="Kind of composition (LOINC if possible).")
    class_id = fields.Many2one(
        comodel_name="hc.vs.doc.class.code",
        string="Class",
        help="Categorization of Composition.")
    subject_type = fields.Char(
        string="Subject Type",
        compute="_compute_subject_type",
        store="True",
        help="Type of who and/or what the composition is about.")
    subject_name = fields.Reference(
        string="Subject",
        selection="_reference_models",
        help="Who and/or what the composition is about.")
    encounter_id = fields.Many2one(
        comodel_name="hc.res.encounter",
        string="Encounter",
        help="Context of the Composition.")
    date = fields.Datetime(
        string="Composition Date",
        required="True",
        help="Composition editing time.")
    author_ids = fields.One2many(
        comodel_name="hc.composition.author",
        inverse_name="composition_id",
        string="Authors",
        required="True",
        help="Who and/or what authored the composition.")
    title = fields.Char(
        string="Title",
        help="Human Readable name/title.")
    confidentiality_id = fields.Many2one(
        comodel_name="hc.vs.confidential.classification",
        string="Confidentiality",
        help="As defined by affinity domain.")
    attester_ids = fields.One2many(
        comodel_name="hc.composition.attester",
        inverse_name="composition_id",
        string="Attesters",
        help="Attests to accuracy of composition.")
    custodian_id = fields.Many2one(
        comodel_name="hc.res.organization",
        string="Custodian",
        help="Organization which maintains the composition.")
    relates_to_ids = fields.One2many(
        comodel_name="hc.composition.relates.to",
        inverse_name="composition_id",
        string="Relates To",
        help="Relationships to other compositions/documents.")
    event_ids = fields.One2many(
        comodel_name="hc.composition.event",
        inverse_name="composition_id",
        string="Events",
        help="The clinical service(s) being documented.")
    section_ids = fields.One2many(
        comodel_name="hc.composition.section",
        inverse_name="composition_id",
        string="Sections",
        help="Composition is broken into sections.")
    # Added for CDA
    version = fields.Char(
        string="Version",
        help="Version of the document")

    @api.model
    def create(self, vals):
        status_history_obj = self.env['hc.composition.status.history']
        res = super(Composition, self).create(vals)
        if vals and vals.get('status'):
            status_history_vals = {
                'composition_id': res.id,
                'status': res.status,
                'start_date': datetime.today()
                }
            if vals.get('status') == 'entered-in-error':
                status_history_vals.update({'end_date': datetime.today()})
            status_history_obj.create(status_history_vals)
        return res

    @api.multi
    def write(self, vals):
        status_history_obj = self.env['hc.composition.status.history']
        res = super(Composition, self).write(vals)
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
                    'composition_id': self.id,
                    'status': vals.get('status'),
                    'start_date': datetime.today()
                    }
                if vals.get('status') == 'entered-in-error':
                    status_history_vals.update({'end_date': datetime.today()})
                status_history_obj.create(status_history_vals)
        return res

    @api.model
    def _reference_models(self):
        models = self.env['ir.model'].search([('state', '!=', 'manual')])
        return [(model.model, model.name)
            for model in models
                if model.model.startswith('hc.res')]

    @api.depends('subject_name')
    def _compute_subject_type(self):
        for this in self:
            if this.subject_name:
                this.subject_type = this.subject_name._description

class CompositionAttester(models.Model):
    _name = "hc.composition.attester"
    _description = "Composition Attester"
    _inherit = ["hc.backbone.element"]

    composition_id = fields.Many2one(
        comodel_name="hc.res.composition",
        string="Composition",
        help="Composition associated with this Composition Attester.")
    mode = fields.Selection(
        string="Mode",
        selection=[
            ("personal", "Personal"),
            ("professional", "Professional"),
            ("legal", "Legal"),
            ("official", "Official")],
        required="True",
        help="The type of attestation the authenticator offers.")
    time = fields.Datetime(
        string="Attester Time",
        help="When the composition was attested.")
    party_type = fields.Selection(
        string="Party Type",
        selection=[
            ("patient", "Patient"),
            ("practitioner", "Practitioner"),
            ("practitioner_role", "Practitioner Role"),
            ("organization", "Organization")],
        help="Type of who attested the composition.")
    party_name = fields.Char(
        string="Party",
        compute="_compute_party_name",
        store="True",
        help="Who attested the composition.")
    party_patient_id = fields.Many2one(
        comodel_name="hc.res.patient",
        string="Party Patient",
        help="Patient who attested the composition.")
    party_practitioner_id = fields.Many2one(
        comodel_name="hc.res.practitioner",
        string="Party Practitioner",
        help="Practitioner who attested the composition.")
    party_practitioner_role_id = fields.Many2one(
        comodel_name="hc.res.practitioner.role",
        string="Party Practitioner Role",
        help="Practitioner Role who attested the composition.")
    party_organization_id = fields.Many2one(
        comodel_name="hc.res.organization",
        string="Party Organization",
        help="Organization who attested the composition.")

    @api.depends('party_type')
    def _compute_party_name(self):
        for hc_composition_attester in self:
            if hc_composition_attester.party_type == 'patient':
                hc_composition_attester.party_name = hc_composition_attester.party_patient_id.name
            elif hc_composition_attester.party_type == 'practitioner':
                hc_composition_attester.party_name = hc_composition_attester.party_practitioner_id.name
            elif hc_composition_attester.party_type == 'practitioner_role':
                hc_composition_attester.party_name = hc_composition_attester.party_practitioner_role_id.name
            elif hc_composition_attester.party_type == 'organization':
                hc_composition_attester.party_name = hc_composition_attester.party_organization_id.name

class CompositionRelatesTo(models.Model):
    _name = "hc.composition.relates.to"
    _description = "Composition Relates To"
    _inherit = ["hc.backbone.element"]

    composition_id = fields.Many2one(
        comodel_name="hc.res.composition",
        string="Composition",
        help="Composition associated with this Composition Relates To.")
    code = fields.Selection(
        string="Code",
        required="True",
        selection=[
            ("replaces", "Replaces"),
            ("transforms", "Transforms"),
            ("signs", "Signs"),
            ("appends", "Appends")],
        help="The type of relationship that this composition has with anther composition or document.")
    target_type = fields.Selection(
        string="Target Type",
        required="True",
        selection=[
            ("identifier", "Identifier"),
            ("composition", "Composition")],
        help="Target of the relationship.")
    target_name = fields.Char(
        string="Target",
        compute="_compute_target_name",
        store="True",
        help="Target of the relationship.")
    target_identifier_id = fields.Many2one(
        comodel_name="hc.composition.relates.to.identifier",
        string="Target Identifier",
        help="Identifier target of the relationship.")
    target_composition_id = fields.Many2one(
        comodel_name="hc.res.composition",
        string="Target Composition",
        help="Composition target of the relationship.")

    @api.depends('target_type')
    def _compute_target_name(self):
        for hc_composition_relates_to in self:
            if hc_composition_relates_to.target_type == 'identifier':
                hc_composition_relates_to.target_name = hc_composition_relates_to.target_identifier_id.name
            elif hc_composition_relates_to.target_type == 'composition':
                hc_composition_relates_to.target_name = hc_composition_relates_to.target_composition_id.title

class CompositionRelatesToIdentifier(models.Model):
    _name = "hc.composition.relates.to.identifier"
    _description = "Composition Relates To Identifier"
    _inherit = ["hc.basic.association", "hc.identifier"]

class CompositionEvent(models.Model):
    _name = "hc.composition.event"
    _description = "Composition Event"
    _inherit = ["hc.backbone.element"]

    composition_id = fields.Many2one(
        comodel_name="hc.res.composition",
        string="Composition",
        help="Composition associated with this Composition Event.")
    code_ids = fields.Many2many(
        comodel_name="hc.vs.act.code",
        string="Codes",
        help="Code(s) that apply to the event being documented.")
    start_date = fields.Datetime(
        string="Start Date",
        help="Start of the the period covered by the documentation.")
    end_date = fields.Datetime(
        string="End Date",
        help="End of the the period covered by the documentation.")
    detail_ids = fields.One2many(
        comodel_name="hc.composition.event.detail",
        inverse_name="event_id",
        string="Details",
        help="Full details for the event(s) the composition consents.")

class CompositionSection(models.Model):
    _name = "hc.composition.section"
    _description = "Composition Section"
    _inherit = ["hc.backbone.element"]    

    composition_id = fields.Many2one(
        comodel_name="hc.res.composition",
        string="Composition",
        help="Composition associated with this Composition Section.")
    title = fields.Char(
        string="Title",
        help="Label for section (e.g. for ToC).")
    code_id = fields.Many2one(
        comodel_name="hc.vs.doc.section.code",
        string="Code",
        help="Classification of section (recommended).")
    text_id = fields.Many2one(
        comodel_name="hc.vs.composition.section.text",
        string="Text",
        help="Text summary of the section, for human interpretation.")
    mode = fields.Many2one(
        comodel_name="hc.vs.list.mode",
        string="Mode",
        required="True",
        help="How the entry list was prepared.")
    ordered_by_id = fields.Many2one(
        comodel_name="hc.vs.list.order",
        string="Ordered By",
        help="Order of section entries.")
    entry_ids = fields.One2many(
        comodel_name="hc.composition.section.entry",
        inverse_name="section_id",
        string="Entries",
        help="A reference to data that supports this section.")
    empty_reason_id = fields.Many2one(
        comodel_name="hc.vs.list.empty.reason",
        string="Empty Reason",
        help="Why the section is empty.")
    section_id = fields.Many2one(
        comodel_name="hc.composition.section",
        string="Section",
        help="A nested sub-section within this section.")

class CompositionAuthor(models.Model):
    _name = "hc.composition.author"
    _description = "Composition Author"
    _inherit = ["hc.basic.association"]

    composition_id = fields.Many2one(
        comodel_name="hc.res.composition",
        string="Composition",
        help="Composition associated with this Composition Author.")
    author_type = fields.Selection(
        string="Author Type",
        selection=[
            ("practitioner", "Practitioner"),
            ("practitioner_role", "Practitioner Role"),
            ("device", "Device"),
            ("patient", "Patient"),
            ("related_person", "Related Person")],
        help="Type of who and/or what authored the composition.")
    author_name = fields.Char(
        string="Author",
        compute="_compute_author_name",
        store="True",
        help="Who and/or what authored the composition.")
    author_practitioner_id = fields.Many2one(
        comodel_name="hc.res.practitioner",
        string="Author Practitioner",
        help="Practitioner who authored the composition.")
    author_practitioner_role_id = fields.Many2one(
        comodel_name="hc.res.practitioner.role",
        string="Author Practitioner Role",
        help="Practitioner Role who authored the composition.")
    author_device_id = fields.Many2one(
        comodel_name="hc.res.device",
        string="Author Device",
        help="Device what authored the composition.")
    author_patient_id = fields.Many2one(
        comodel_name="hc.res.patient",
        string="Author Patient",
        help="Patient who and/or what authored the composition.")
    author_related_person_id = fields.Many2one(
        comodel_name="hc.res.related.person",
        string="Author Related Person",
        help="Related Person who authored the composition.")

    @api.depends('author_type')
    def _compute_author_name(self):
        for hc_composition_author in self:
            if hc_composition_author.author_type == 'practitioner':
                hc_composition_author.author_name = hc_composition_author.author_practitioner_id.name
            elif hc_composition_author.author_type == 'practitioner_role':
                hc_composition_author.author_name = hc_composition_author.author_practitioner_role_id.name
            elif hc_composition_author.author_type == 'device':
                hc_composition_author.author_name = hc_composition_author.author_device_id.name
            elif hc_composition_author.author_type == 'patient':
                hc_composition_author.author_name = hc_composition_author.author_patient_id.name
            elif hc_composition_author.author_type == 'related_person':
                hc_composition_author.author_name = hc_composition_author.author_related_person_id.name

class CompositionIdentifier(models.Model):
    _name = "hc.composition.identifier"
    _description = "Composition Identifier"
    _inherit = ["hc.basic.association", "hc.identifier"]

class CompositionStatusHistory(models.Model):
    _name = "hc.composition.status.history"
    _description = "Composition Status History"

    composition_id = fields.Many2one(
        comodel_name="hc.res.composition",
        string="Composition",
        help="Composition associated with this Composition Status History.")
    status = fields.Char(
        string="Status",
        help="The status of the composition.")
    start_date = fields.Datetime(
        string="Start Date",
        help="Start of the period during which this composition status is valid.")
    end_date = fields.Datetime(
        string="End Date",
        help="End of the period during which this composition status is valid.")
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

class CompositionEventDetail(models.Model):
    _name = "hc.composition.event.detail"
    _description = "Composition Event Detail"
    _inherit = ["hc.basic.association"]

    event_id = fields.Many2one(
        comodel_name="hc.composition.event",
        string="Event",
        help="Event associated with this Composition Event Detail.")
    detail_type = fields.Char(
        string="Detail Type",
        compute="_compute_detail_type",
        store="True",
        help="Type of full details for the event(s) the composition consent.")
    detail_name = fields.Reference(
        string="Detail",
        selection="_reference_models",
        help="Full details for the event(s) the composition consents.")

    @api.model
    def _reference_models(self):
        models = self.env['ir.model'].search([('state', '!=', 'manual')])
        return [(model.model, model.name)
            for model in models
                if model.model.startswith('hc.res')]

    @api.depends('detail_name')
    def _compute_detail_type(self):
        for this in self:
            if this.detail_name:
                this.detail_type = this.detail_name._description

class CompositionSectionEntry(models.Model):
    _name = "hc.composition.section.entry"
    _description = "Composition Section Entry"
    _inherit = ["hc.basic.association"]

    section_id = fields.Many2one(
        comodel_name="hc.composition.section",
        string="Section",
        help="Section associated with this Composition Section Entry.")
    entry_type = fields.Char(
        string="Entry Type",
        compute="_compute_entry_type",
        store="True",
        help="Type of reference to data that supports this section.")
    entry_name = fields.Reference(
        string="Entry",
        selection="_reference_models",
        help="A reference to data that supports this section.")

    @api.model
    def _reference_models(self):
        models = self.env['ir.model'].search([('state', '!=', 'manual')])
        return [(model.model, model.name)
            for model in models
                if model.model.startswith('hc.res')]

    @api.depends('entry_name')
    def _compute_entry_type(self):
        for this in self:
            if this.entry_name:
                this.entry_type = this.entry_name._description

class CompositionAttestationMode(models.Model):
    _name = "hc.vs.composition.attestation.mode"
    _description = "Composition Attestation Mode"
    _inherit = ["hc.value.set.contains"]

class CompositionSectionText(models.Model):
    _name = "hc.vs.composition.section.text"
    _description = "Composition Section Text"
    _inherit = ["hc.value.set.contains"]

class ConfidentialClassification(models.Model):
    _name = "hc.vs.confidential.classification"
    _description = "Confidential Classification"
    _inherit = ["hc.value.set.contains"]

class DocClassCode(models.Model):
    _name = "hc.vs.doc.class.code"
    _description = "Doc Class Code"
    _inherit = ["hc.value.set.contains"]

class DocSectionCode(models.Model):
    _name = "hc.vs.doc.section.code"
    _description = "Doc Section Code"
    _inherit = ["hc.value.set.contains"]

class DocTypeCode(models.Model):
    _name = "hc.vs.doc.type.code"
    _description = "Doc Type Code"
    _inherit = ["hc.value.set.contains"]
