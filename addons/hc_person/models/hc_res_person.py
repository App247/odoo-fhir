# -*- coding: utf-8 -*-

from openerp import models, fields, api

class Person(models.Model): 
    _name = "hc.res.person" 
    _description = "Person"
    _inherits = {"res.partner": "partner_id"}

    partner_id = fields.Many2one(
        comodel_name="res.partner", 
        string="Partner", 
        required="True", 
        ondelete="restrict", 
        help="Partner associated with this Person.")
    name_id = fields.Many2one(
        comodel_name="hc.human.name",
        string="Full Name",
        required="True",
        help="A full text representation of this Person's name.")
    identifier_ids = fields.One2many(
        comodel_name="hc.person.identifier", 
        inverse_name="person_id", 
        string="Identifiers", 
        help="A human identifier for this Person.")
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
    birth_date = fields.Date(
        string="Birth Date",
        required="True", # Standard is False
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
#     person_managing_organization_id = fields.Many2one(
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

    # When creating a new record, add Person Name to the list of Person Names and mark it as preferred.

    @api.model
    def create(self, vals):
        person_name_obj = self.env['hc.person.name']
        name = self.env['hc.human.name'].browse(vals['name_id'])
        vals['name'] = name.name
        names_vals = {}
        res = super(Person, self).create(vals)
        if name:
            names_vals.update({
                        'is_preferred': True,
                        'human_name_id': name.id,
                        'person_id': res.id
                        })
            person_name_obj.create(names_vals)

        return res

        # vals['is_patient'] = self.env.context.get('is_patient', False)
        # vals['is_practitioner'] = self.env.context.get('is_practitioner', False)
        # vals['is_related_person'] = self.env.context.get('is_related_person', False)     
    
    _defaults = {
        "is_company": False,
        "customer": False,
        "company_type": "person",
        "is_person": True,
        }

    # _sql_constraints = [    
    #     ('name_uniq',
    #     'UNIQUE (name)',
    #     'Book title must be unique.')
    #     ]


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
                name_rec.append((id.id, id.name_id.name + "("+id.birth_date+")"))
            else:
                name_rec.append((id.id, id.name_id.name))
        return name_rec

class PersonLink(models.Model): 
    _name = "hc.person.link"    
    _description = "Person Link"

    person_id = fields.Many2one(
        comodel_name="hc.res.person", 
        string="Person", 
        help="Person associated with this Person Link.")
    target_type = fields.Selection(
        string="Target Type", 
        required="True", 
        selection=[
            ("person", "Person"),
            ("practitioner", "Practitioner"), 
            ("related_person", "Related Person"), 
            ("patient", "Patient")], 
        help="Type of resource to which this actual person is associated.")                
    target_name = fields.Char(
        string="Target", 
        compute="_compute_target_name", 
        store="True", 
        help="The resource to which this actual person is associated.")
    target_person_id = fields.Many2one(
        comodel_name="hc.res.person", 
        string="Target Person", 
        help="Person who is the resource to which this actual person is associated.")
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
    assurance = fields.Selection(
        string="Assurance Level", 
        selection=[
            ("level1", "Level 1"), 
            ("level2", "Level 2"), 
            ("level3", "Level 3"), 
            ("level4", "Level 4")],
        default="level1", 
        help="Level of assurance that this link is actually associated with the target resource.")

    @api.depends('target_type')            
    def _compute_target_name(self):         
        for hc_person_link in self:      
            if hc_person_link.target_type == 'person': 
                hc_person_link.target_name = hc_person_link.target_person_id.name
    #         elif hc_person_link.target_type == 'practitioner':   
    #             hc_person_link.target_name = hc_person_link.target_practitioner_id.name
    #         elif hc_person_link.target_type == 'related_person': 
    #             hc_person_link.target_name = hc_person_link.target_related_person_id.name
    #         elif hc_person_link.target_type == 'patient':  
    #             hc_person_link.target_name = hc_person_link.target_patient_id.name

class PersonIdentifier(models.Model):   
    _name = "hc.person.identifier"  
    _description = "Person Identifier"
    _inherit = ["hc.basic.association", "hc.identifier"]

    person_id = fields.Many2one(
        comodel_name="hc.res.person", 
        string="Person", 
        help="Person associated with this Person Identifier.")

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
    # start_date = fields.Datetime(
    #     default=person_id.birth_date)

    @api.model
    def create(self, vals):
        person_obj = self.env['hc.res.person']
        if vals and vals.get('is_preferred'):
            person_ids = self.search([('person_id','=',vals.get('person_id'))])
            for person in person_ids:
                person.is_preferred = False
        return super(PersonName, self).create(vals)

    @api.multi
    def write(self, vals):
        if vals and vals.get('is_preferred'):
            person_ids = self.search([('person_id','=',self.person_id.id),('id','!=',self.id)])
            for person in person_ids:
                person.is_preferred = False
        return super(PersonName, self).write(vals)

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
    patient_id = fields.Many2one(
        comodel_name="hc.res.patient", 
        string="Person", 
        help="Patient associated with this Person Address.")

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

    is_person = fields.Boolean(
        string="Is a person", 
        help="This partner is a health care person.")
    # is_patient = fields.Boolean(
    #     string="Is a patient", 
    #     help="This partner is a patient.")
    # is_practitioner = fields.Boolean(
    #     string="Is a practitioner", 
    #     help="This partner is a health care practitioner.")
    # is_related_person = fields.Boolean(
    #     string="Is a related person", 
    #     help="This partner is a health care related person.")
