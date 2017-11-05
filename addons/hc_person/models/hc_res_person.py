# -*- coding: utf-8 -*-

from openerp import models, fields, api
from datetime import datetime
from openerp.tools import DEFAULT_SERVER_DATE_FORMAT as DF

class Person(models.Model):
    _name = "hc.res.person"
    _description = "Person"
    _inherit = ["hc.domain.resource"]
    _rec_name = "name_id"

    partner_id = fields.Many2one(
        comodel_name="res.partner",
        string="Partner",
        help="Partner associated with this Person.")
    unique_person = fields.Char(
        string="Unique Person",
        compute="_compute_unique_person",
        store="True",
        help="Unique identifier of a person. Full Name + Gender + Birth Date.")
    type = fields.Selection(
        string="Type",
        selection=[
            ("human", "Human"),
            ("animal", "Animal")],
        default="human",
        help="Person is human or animal.")
    identifier_ids = fields.One2many(
        comodel_name="hc.person.identifier",
        inverse_name="person_id",
        string="Identifiers",
        help="A human identifier for this Person.")
    name_id = fields.Many2one(
        comodel_name="hc.human.name",
        string="Full Name",
        required="True",
        help="A full text representation of this Person's or Animal's name when the record was created.")
    name = fields.Char(
        related="name_id.name",
        help="Human Readable name of the person.")
    name_ids = fields.One2many(
        comodel_name="hc.person.name",
        inverse_name="person_id",
        string="Names",
        help="A name associated with this Person.")
    telecom_ids = fields.One2many(
        comodel_name="hc.person.telecom",
        inverse_name="person_id",
        string="Telecoms",
        help="A contact detail for the person.")
    gender = fields.Selection(
        string="Gender",
        required="True", # Standard is False
        selection=[
            ("male", "Male"),
            ("female", "Female"),
            ("other", "Other"),
            ("unknown", "Unknown")],
        help="The gender of a person used for administrative purposes.")
    gender_other = fields.Selection(
        string="Other Gender",
        selection=[
            ("A", "Ambiguous"),
            ("MTF", "male-to-female"),
            ("FTM", "female-to-male")],
        help="Type of other gender. An extension of the standard gender value set.")
    birth_date = fields.Date(
        string="Birth Date",
        # required="True", # Standard is False
        help="The birth date for the person.")
    address_ids = fields.One2many(
        comodel_name="hc.person.address",
        inverse_name="person_id",
        string="Addresses",
        help="One or more addresses for the person.")
    photo_ids = fields.One2many(
        comodel_name="hc.person.photo",
        inverse_name="person_id",
        string="Photos",
        help="Image of the Person.")
#     managing_organization_id = fields.Many2one(
#         comodel_name="hc.res.organization",
#         string="Managing Organization",
#         help="The Organization that is the custodian of the person record.")
    is_active = fields.Boolean(
        string="Active",
        default="True",
        help="Whether this person's record is in active use.")
    link_ids = fields.One2many(
        comodel_name="hc.person.link",
        inverse_name="person_id",
        string="Links",
        help="Link to a resource that concerns the same actual person.")

    #Added from res.partner
    image = fields.Binary(
        string="Image",
        attachment=True,
        help="This field holds the image used as avatar for this contact, limited to 1024x1024px",)
    image_medium = fields.Binary(
        string="Medium-sized image",
        attachment=True,
        help="Medium-sized image of this contact. It is automatically "\
             "resized as a 128x128px image, with aspect ratio preserved. "\
             "Use this field in form views or some kanban views.")
    image_small = fields.Binary(
        string="Small-sized image",
        attachment=True,
        help="Small-sized image of this contact. It is automatically "\
             "resized as a 64x64px image, with aspect ratio preserved. "\
             "Use this field anywhere a small image is required.")

    @api.depends('name_id', 'gender', 'birth_date')
    def _compute_unique_person(self):
        comp_unique_person = '/'
        for hc_person in self:
            if hc_person.name_id:
                comp_unique_person = hc_person.name_id.name or ''
            if hc_person.gender:
                comp_unique_person = comp_unique_person + ", " + hc_person.gender or ''
            if hc_person.birth_date:
                comp_unique_person = comp_unique_person + ", " + datetime.strftime(datetime.strptime(hc_person.birth_date, DF), "%Y-%m-%d")
            hc_person.unique_person = comp_unique_person

    _sql_constraints = [
        ('person_uniq',
        'UNIQUE (unique_person)',
        'Person must be a unique combination of name, gender and birth date')
        ]

    # For a new record, add Person Name to the list of Person Names and mark it as "preferred" with Start Date = Birth Date.
    # In addition, create Partner and Partner Link records.

    @api.model
    def create(self, vals):
        partner_obj = self.env['res.partner'] # Variable to create partner
        person_name_obj = self.env['hc.person.name'] # Variable to create person name
        partner_link_obj = self.env['hc.partner.link'] # Variable to create partner link
        name = self.env['hc.human.name'].browse(vals['name_id']) # Variable to create name of person
        res = super(Person, self).create(vals)

        if not vals.get('partner_id'):
            partner_id = partner_obj.create({
                'company_type': 'person',
                'is_company': False,
                'is_person': True,
                'is_healthcare': True,
                'name': name.name,
                'birthdate': str(res.birth_date),
                })
            vals.update({'partner_id': partner_id.id})
        vals.update({'name': name.name})

        # names_vals = {}
        link = partner_link_obj.create({
            'link_type': 'person',
            'link_person_id': res.id,
            'partner_id': vals.get('partner_id'),
            'start_date': datetime.today(),
            })

        names_vals = {}
        if name:
            names_vals.update({
                'is_preferred': True,
                'human_name_id': name.id,
                'person_id': res.id,
                'start_date': res.birth_date,
                })
            person_name_obj.create(names_vals)

        return res

    # @api.model
    # def create(self, vals):
    #     partner_obj = self.env['res.partner'] # Variable to create partner
    #     person_name_obj = self.env['hc.person.name'] # Variable to create person name
    #     partner_link_obj = self.env['hc.partner.link'] # Variable to create partner link
    #     name = self.env['hc.human.name'].browse(vals['name_id']) # Variable to create name of person
    #     res = super(Person, self).create(vals)
    #     if not vals.get('partner_id'):
        #     if res.type == 'human':
        #         partner_id = partner_obj.create({
        #             'company_type': 'person',
        #             'is_company': False,
        #             'is_person': True,
        #             'is_healthcare': True,
        #             'name': name.name,
        #             'birthdate': str(res.birth_date),
        #             })
        #     else:
        #         partner_id = partner_obj.create({
        #             'company_type': 'animal',
        #             'is_company': False,
        #             'is_animal': True,
        #             'is_healthcare': True,
        #             'name': name.name,
        #             'birthdate': str(res.birth_date),
        #             })
        #     vals.update({'partner_id': partner_id.id})
        # vals.update({'name': name.name})

    #     names_vals = {}
    #     if res.type == 'human':
    #         link = partner_link_obj.create({
    #             'link_type': 'person',
    #             'link_person_id': res.id,
    #             'partner_id': vals.get('partner_id'),
    #             'start_date': datetime.today(),
    #             })
    #         if name:
    #             names_vals.update({
    #                 'is_preferred': True,
    #                 'human_name_id': name.id,
    #                 'person_id': res.id,
    #                 'start_date': res.birth_date,
    #                 })
    #             person_name_obj.create(names_vals)
    #     elif res.type == 'animal':
    #         link = partner_link_obj.create({
    #             'link_type': 'animal',
    #             'link_person_id': res.id,
    #             'partner_id': vals.get('partner_id'),
    #             'start_date': datetime.today(),
    #             })
    #         if name:
    #             names_vals.update({
    #                 'is_preferred': True,
    #                 'human_name_id': name.id,
    #                 'person_id': res.id,
    #                 'start_date': res.birth_date,
    #                 })
    #             person_name_obj.create(names_vals)
    #     return res

    # For an existing record, if new Person Name is preferred, remove preferred from previous name.

    @api.multi
    def write(self, vals):
        person_name_obj = self.env['hc.person.name']
        names_vals = {}
        if vals and vals.get('birth_date'):
            for rec in self:
                for name_id in rec.name_ids:
                    if vals.get('birth_date') > name_id.start_date:
                        name_id.start_date = vals.get('birth_date')
        if vals and vals.get('name_id'):
            person_name_ids = person_name_obj.search([('person_id','=', self.id),('human_name_id','=',vals.get('name_id'))])
            if person_name_ids:
                for person in person_name_ids:
                    person.is_preferred = True
                    person.end_date = False
            else:
                names_vals.update({
                'is_preferred': True,
                'human_name_id': vals.get('name_id'),
                'person_id': self.id,
                'start_date': datetime.today(),
                })
            person_name_obj.create(names_vals)
        res = super(Person, self).write(vals)
        if vals and vals.get('name_ids'):
            for rec in self:
                for name_id in rec.name_ids.search([('is_preferred','=',True),('person_id','=',self.id)]):
                    self.name_id = name_id.human_name_id.id
        return res

    @api.multi
    def unlink(self):
        res = super(Person, self).unlink()
        return res

    # Display Person Name and Birth Date in Dropdown

    @api.model
    def name_search(self, name='', args=None, operator='ilike', limit=100):
        context = dict(self._context)
        if context is None:
            context = {}
        if args is None:
            args = []
        if not operator:
            operator = 'ilike'
        if name:
                args.append(('name_id', operator, name))
        ids = self.search(args, limit=limit)
        name_rec = []
        for id in ids:
            if id.birth_date:
                name_rec.append((id.id, id.name_id.name + " ("+id.birth_date+")"))
            else:
                name_rec.append((id.id, id.name_id.name))
        return name_rec

class PersonLink(models.Model):
    _name = "hc.person.link"
    _description = "Person Link"
    _inherit = "hc.backbone.element"

    person_id = fields.Many2one(
        comodel_name="hc.res.person",
        string="Person",
        help="Person associated with this Person Link.")
    target_type = fields.Selection(
        string="Target Type",
        required="True",
        selection=[
            # ("patient", "Patient"),
            # ("practitioner", "Practitioner"),
            # ("related_person", "Related Person"),
            ("person", "Person")],
        help="Type of resource to which this actual person is associated.")
    target_name = fields.Char(
        string="Target",
        compute="_compute_target_name",
        store="True",
        help="The resource to which this actual person is associated.")
    # target_patient_id = fields.Many2one(
    #     comodel_name="hc.res.patient",
    #     string="Target Patient",
    #     help="Patient who is the resource to which this actual person is associated.")
    # target_practitioner_id = fields.Many2one(
    #     comodel_name="hc.res.practitioner",
    #     string="Target Practitioner",
    #     help="Practitioner who is the resource to which this actual person is associated.")
    # target_related_person_id = fields.Many2one(
    #     comodel_name="hc.res.related.person",
    #     string="Target Related Person",
    #     help="Related Person who is the resource to which this actual person is associated.")
    target_person_id = fields.Many2one(
        comodel_name="hc.res.person",
        string="Target Person",
        help="Person who is the resource to which this actual person is associated.")
    assurance = fields.Selection(
        string="Assurance Level",
        selection=[
            ("level1", "Level 1"),
            ("level2", "Level 2"),
            ("level3", "Level 3"),
            ("level4", "Level 4")],
        default="level1",
        help="Level of assurance that this link is actually associated with the link resource.")

    @api.depends('target_type')
    def _compute_target_name(self):
        for hc_person_link in self:
            if hc_person_link.target_type == 'person':
                hc_person_link.target_name = hc_person_link.target_person_id.name_id.name
    #         elif hc_person_link.target_type == 'patient':
    #             hc_person_link.target_name = hc_person_link.target_patient_id.name
    #         elif hc_person_link.target_type == 'practitioner':
    #             hc_person_link.target_name = hc_person_link.target_practitioner_id.name
    #         elif hc_person_link.target_type == 'related_person':
    #             hc_person_link.target_name = hc_person_link.target_related_person_id.name

class PersonIdentifier(models.Model):
    _name = "hc.person.identifier"
    _description = "Person Identifier"
    _inherit = ["hc.basic.association", "hc.identifier", "hc.identifier.use"]

    person_id = fields.Many2one(
        comodel_name="hc.res.person",
        string="Person",
        help="Person associated with this Person Identifier.")
    extension_ids = fields.One2many(
        comodel_name="hc.person.identifier.extension",
        inverse_name="person_identifier_id",
        string="Extensions",
        help="Additional Content defined by implementations.")

class PersonIdentifierExtension(models.Model):
    _name = "hc.person.identifier.extension"
    _description = "Person Identifier Extension"
    _inherit = ["hc.basic.association", "hc.extension"]

    person_identifier_id = fields.Many2one(
        comodel_name="hc.person.identifier",
        string="Person Identifier",
        help="Person Identifier associated with this Person Identifier Extension.")

class PersonName(models.Model):
    _name = "hc.person.name"
    _description = "Person Name"
    _inherit = ["hc.human.name.use"]
    _inherits = {"hc.human.name": "human_name_id"}

    human_name_id = fields.Many2one(
        comodel_name="hc.human.name",
        string="Human Name",
        required="True",
        ondelete="restrict",
        help="Human Name associated with this Person Name.")
    person_id = fields.Many2one(
        comodel_name="hc.res.person",
        string="Person",
        help="Person associated with this Person Name.")

    # technical field used to manage unique person name
    person_name = fields.Char(
        string="Person Name",
        compute="_compute_name",
        store="True",
        help="Human Name ID + Person ID.")

    @api.depends('human_name_id', 'person_id')
    def _compute_name(self):
        comp_name = '/'
        for hc_person_name in self:
            if hc_person_name.human_name_id:
                comp_name = str(hc_person_name.human_name_id) or ''
            if hc_person_name.person_id:
                comp_name = comp_name + ", " + str(hc_person_name.person_id) or ''

    # _sql_constraints = [
    #     ('name_uniq',
    #     'UNIQUE (name)',
    #     'Person name must be unique.')
    #
    # For a new person record,
    # Full Name = Person Name.
    # Add Person Name to the list of Person Names and mark it as preferred.

    @api.model
    def create(self, vals):
        person_obj = self.env['hc.res.person']
        person_ids = self.search([('person_id','=',vals.get('person_id')),('end_date', '=', False)])
        if vals and vals.get('is_preferred'):
            for person in person_ids:
                person.is_preferred = False
                if not vals.get('start_date'):
                    person.end_date = datetime.today()
                    vals.update({'start_date': datetime.today()})
                else:
                    person.end_date = vals.get('start_date')
        else:
            vals.update({'start_date': datetime.today()})
        return super(PersonName, self).create(vals)

    # For an existing person record,
    # If new name is preferred, set old name not preferred and set its end date to the start date of the new preferred name.
    # If new name is not preferred, don't change old name record.

    @api.multi
    def write(self, vals):
        person_name_obj = self.env['hc.person.name']
        # hc_person_obj = self.env['hc.res.person']
        if vals and vals.get('is_preferred'):
            person_ids = self.search([('person_id','=',self.person_id.id),('id','!=',self.id), ('end_date', '=', False)])
            for person in person_ids:
                person.is_preferred = False
                person.end_date = datetime.today()
            vals.update({'end_date': False})
        return super(PersonName, self).write(vals)

    # When deleting a name,
    # If name to be deleted is the only name remaining, raise error message and do nothing.
    # If other names are remaining, delete the selected name and make the name with with the latest End Date become preferred and its End Date become blank.

    @api.multi
    def unlink(self):
        hc_person_obj = self.env['hc.res.person']
        person_ids = self.search([('person_id','=',self.person_id.id),('id','!=',self.id)])
        if not person_ids:
            raise UserError(_('Person must have at least one Person Name.'))
        return super(PersonName, self).unlink()

    # version 2
    # @api.multi
    # def write(self, vals):
    #     person_name_obj = self.env['hc.person.name']
    #     if vals and vals.get('is_preferred'):
    #         person_ids = self.search([('person_id','=',self.person_id.id),('id','!=',self.id), ('end_date', '=', False)])
    #         for person in person_ids:
    #             person.is_preferred = False
    #             person.end_date = datetime.today()
    #         vals.update({'end_date': False})
    #     return super(PersonName, self).write(vals)

    # version 1
    # @api.model
    # def create(self, vals):
    #     person_obj = self.env['hc.res.person']
    #     if vals and vals.get('is_preferred'):
    #         person_ids = self.search([('person_id','=',vals.get('person_id'))])
    #         for person in person_ids:
    #             person.is_preferred = False
    #     if vals:
    #         person_ids = self.search([('person_id','=',vals.get('person_id')),('end_date','=',False)])
    #         for person in person_ids:
    #             if not vals.get('start_date'):
    #                 person.end_date = datetime.today()
    #             else:
    #                 person.end_date = vals.get('start_date')
    #         if not vals.get('start_date'):
    #             vals.update({'start_date': datetime.today()})
    #     return super(PersonName, self).create(vals)

    # @api.multi
    # def write(self, vals):
    #     if vals and vals.get('is_preferred'):
    #         person_ids = self.search([('person_id','=',self.person_id.id),('id','!=',self.id)])
    #         for person in person_ids:
    #             person.is_preferred = False
    #     return super(PersonName, self).write(vals)

class PersonTelecom(models.Model):
    _name = "hc.person.telecom"
    _description = "Person Telecom"
    _inherit = ["hc.contact.point.use"]
    _inherits = {"hc.contact.point": "telecom_id"}

    telecom_id = fields.Many2one(
        comodel_name="hc.contact.point",
        string="Telecom",
        ondelete="restrict",
        required="True",
        help="Telecom associated with this Person Telecom.")
    person_id = fields.Many2one(
        comodel_name="hc.res.person",
        string="Person",
        help="Person associated with this Person Telecom.")

class PersonAddress(models.Model):
    _name = "hc.person.address"
    _description = "Person Address"
    _inherit = ["hc.address.use"]
    _inherits = {"hc.address": "address_id"}
    _rec_name = "text"

    address_id = fields.Many2one(
        comodel_name="hc.address",
        string="Address",
        required="True",
        ondelete="restrict",
        help="Address associated with this Person Address.")
    person_id = fields.Many2one(
        comodel_name="hc.res.person",
        string="Person",
        help="Person associated with this Person Address.")

class PersonPhoto(models.Model):
    _name = "hc.person.photo"
    _description = "Person Photo"
    _inherit = ["hc.basic.association", "hc.attachment"]

    person_id = fields.Many2one(
        comodel_name="hc.res.person",
        string="Person",
        help="Entity associated with this Person Photo.")

# External Reference

class Partner(models.Model):
    _inherit = ["res.partner"]

    company_type = fields.Selection(
        selection_add=[
            ("animal", "Animal")])
    is_person = fields.Boolean(
        string="Is a person",
        help="This partner is a health care person.")
    is_animal = fields.Boolean(
        string="Is an animal",
        help="This partner is a health care animal.")
    # is_patient = fields.Boolean(
    #     string="Is a patient",
    #     help="This partner is a patient.")
    # is_practitioner = fields.Boolean(
    #     string="Is a practitioner",
    #     help="This partner is a health care practitioner.")
    # is_related_person = fields.Boolean(
    #     string="Is a related person",
    #     help="This partner is a health care related person.")
    link_ids = fields.One2many(
        comodel_name="hc.partner.link",
        inverse_name="partner_id",
        string="Links",
        help="Link to a resource that concerns the same actual partner.")

class PartnerLink(models.Model):
    _name = "hc.partner.link"
    _description = "Partner Link"
    _inherit = ["hc.basic.association"]

    partner_id = fields.Many2one(
        comodel_name="res.partner",
        string="Partner",
        help="Partner associated with this Partner Link.")
    link_type = fields.Selection(
        string="Link Type",
        required="True",
        selection=[
            ("person", "Person"),
            ("animal", "Animal")
            # ("patient", "Patient"),
            # ("patient_contact", "Patient Contact"),
            # ("related_person", "Related Person"),
            # ("practitioner", "Practitioner")
            ],
        help="Type of resource to which this actual partner is associated.")
    link_name = fields.Char(
        string="Link",
        compute="_compute_link_name",
        store="True",
        help="The resource to which this actual partner is associated.")
    link_person_id = fields.Many2one(
        comodel_name="hc.res.person",
        string="Link Person",
        domain="[('type','=','human')]",
        help="Person who is the resource to which this actual partner is associated.")
    link_animal_id = fields.Many2one(
        comodel_name="hc.res.person",
        string="Link Animal",
        domain="[('type','=','animal')]",
        # domain="[('is_animal','=','True')]",
        # domain="[('company_type','=','animal')]",
        help="Animal who is the resource to which this actual partner is associated.")
    # link_patient_id = fields.Many2one(
    #     comodel_name="res.partner",
    #     string="Link Patient",
    #     help="Patient who is the resource to which this actual partner is associated.")
    # link_patient_contact_id = fields.Many2one(
    #     comodel_name="res.partner",
    #     string="Link Patient Contact",
    #     help="Patient who is the resource to which this actual partner is associated.")
    # link_related_person_id = fields.Many2one(
    #     comodel_name="res.partner",
    #     string="Link Related Person",
    #     help="Related Person who is the resource to which this actual partner is associated.")
    # link_practitioner_id = fields.Many2one(
    #     comodel_name="res.partner",
    #     string="Link Practitioner",
    #     help="Practitioner who is the resource to which this actual partner is associated.")

    @api.depends('link_type')
    def _compute_link_name(self):
        for hc_partner_link in self:
            if hc_partner_link.link_type == 'person':
                hc_partner_link.link_name = hc_partner_link.link_person_id.name
            elif hc_partner_link.link_type == 'animal':
                hc_partner_link.link_name = hc_partner_link.link_animal_id.name
            # elif hc_partner_link.link_type == 'patient':
            #     hc_partner_link.link_name = hc_partner_link.link_patient_id.name
            # elif hc_partner_link.link_type == 'patient_contact':
            #     hc_partner_link.link_name = hc_partner_link.link_patient_contact_id.name
            # elif hc_partner_link.link_type == 'related_person':
            #     hc_partner_link.link_name = hc_partner_link.link_related_person_id.name
            # elif hc_partner_link.link_type == 'practitioner':
            #     hc_partner_link.link_name = hc_partner_link.link_practitioner_id.name
