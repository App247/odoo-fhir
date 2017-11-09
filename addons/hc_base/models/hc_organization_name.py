# -*- coding: utf-8 -*-

from openerp import models, fields, api

# class OrganizationNameTermType(models.Model):
#     _name = "hc.vs.human.name.term.type"
#     _description = "Organization Name Term Type"
#     _inherit = ["hc.value.set.contains"]

#     name = fields.Char(
#         string="Name",
#         help="Name of this organization name term type.")
#     code = fields.Char(
#         string="Code",
#         help="Code of this organization name term type.")
#     contains_id = fields.Many2one(
#         comodel_name="hc.vs.human.name.term.type",
#         string="Parent",
#         help="Parent organization name term type.")

class OrganizationNameTerm(models.Model):
    _name = "hc.organization.name.term"
    _description = "Organization Name Term"

    name = fields.Char(
        string="Organization Name Term",
        required="True",
        help="A single term of a organization name (e.g., Mayo, Clinic).")
    # type_ids = fields.Many2many(
    #     comodel_name="hc.vs.human.name.term.type",
    #     relation="organization_name_term_type_rel",
    #     string="Types",
    #     help="Type of organization name term.")

    _sql_constraints = [
        ("name_unique",
        "UNIQUE(name)",
        "The term must be unique.")
        ]

class OrganizationNameSuffix(models.Model):
    _name = "hc.organization.name.suffix"
    _description = "Organization Name Suffix"
    _inherit = ["res.partner.title"]
    _order = "long_name"

    name = fields.Char(
        string="Suffix",
        required = "True",
        help="Characters that come after the given names. Aka post-nominal letters (e.g., Inc.)")
    long_name = fields.Char(
        string="Suffix Name",
        help="Full text of suffix abbreviation (e.g., Incorporated for Inc.)")
    description = fields.Text(
        string="Description",
        help="Describes a suffix.")

class OrganizationNameUse(models.Model):
    _name = "hc.organization.name.use"
    _description = "Organization Name Use"
    _inherit = ["hc.basic.association"]

    use = fields.Selection(
        string="Use",
        selection=[
            ("usual", "Usual"),
            ("legal", "Legal"),
            ("temp", "Temp"),
            ("nickname", "Nickname"),
            ("anonymous", "Anonymous"),
            ("old", "Old"),
            ("symbol", "Symbol")],
        default="usual",
        help="The use of a organization name.")
    start_date = fields.Datetime(
        string="Start Date",
        help="Start of the time period when name was/is in use.")
    end_date = fields.Datetime(
        string="End Date",
        help="End of the time period when name was/is in use.")

class OrganizationName(models.Model):
    _name = "hc.organization.name"
    _description = "Organization Name"
    _inherit = ["hc.element"]
    _rec_name = "name"

    name = fields.Char(
        compute='_compute_full_name',
        store="True",
        string="Full Name",
        help="A full text representation of the organization name.")
    # family = fields.Char(
    #     store="True",
    #     string="Family Name",
    #     readonly="True",
    #     help="The terms of a name that links to the genealogy. (e.g., surname, birth last name).")
    given = fields.Char(
        store="True",
        string="Given Name",
        readonly="True",
        help="Terms that identify a specific organization")
    # prefix_ids = fields.Many2many(
    #     comodel_name="res.partner.title",
    #     relation="organization_name_prefix_rel",
    #     string="Prefix Names",
    #     help="Terms that come before the full name.")
    suffix_ids = fields.Many2many(
        comodel_name="hc.organization.name.suffix",
        relation="organization_name_suffix_rel",
        string="Suffix Names",
        help="Terms that come after the given names.")
    first_id = fields.Many2one(
        comodel_name="hc.organization.name.term",
        string="First Name",
        help="First term of a given name.")
    middle_ids = fields.Many2many(
        comodel_name="hc.organization.name.term",
        relation="middle_name_organization_term_rel",
        string="Middle Names",
        help="Middle term of a given name.")
    # initial_ids = fields.Many2many(
    #     comodel_name="hc.organization.name.term",
    #     relation="initial_name_organization_term_rel",
    #     string="Initial Names",
    #     help="First letter of a term in a given name.")
    nickname_ids = fields.Many2many(
        comodel_name="hc.organization.name.term",
        relation="nickname_organization_term_rel",
        string="Nicknames",
        help="Familiar term of a given name.")
    # surname_id = fields.Many2one(
    #     comodel_name="hc.organization.name.term",
    #     string="Surname",
    #     help="Hereditary name common to all members of a famly. Also known as family name, last name and patronymic.")
    # previous_surname_ids = fields.Many2many(
    #     comodel_name="hc.organization.name.term",
    #     relation="organization_name_previous_surname_rel",
    #     string="Previous Married Last Names",
    #     help="Previous married last name.")
    # preferred_name = fields.Char(
    #     string="Preferred Name",
    #     help="How the organization prefers to be addressed in a conversation (e.g., John, Mr. Smith).")
    # mother_maiden_id = fields.Many2one(
    #     comodel_name="hc.organization.name.term",
    #     string="Mother Maiden Family Name",
    #     help="Mother's surname at birth. Part of the family name.")
    # birth_surname_id = fields.Many2one(
    #     comodel_name="hc.organization.name.term",
    #     string="Birth Last Name",
    #     help="Person's surname at birth.")
    # display_order = fields.Selection(
    #     string="Display Name Order",
    #     selection=[
    #         ("first_maiden_last", "First Last (default)"),
    #         ("maiden_last_first", "Last First (e.g., East Asian name)"),
    #         ("first_last_maiden", "First Last Maiden (e.g., Hispanic name)")],
    #     default="first_maiden_last",
    #     help="The display order of this organization name.")
    # is_animal_name = fields.Boolean(
    #     string="Animal Name",
    #     help="Indicates if this name is an animal name.")

    _sql_constraints = [
        ('name_uniq',
        'UNIQUE (name)',
        'Full Name must be unique.')
        ]


    @api.depends('first_id', 'middle_ids', 'nickname_ids', 'suffix_ids')
    def _compute_full_name(self):
        full_name = '/'
        for rec in self:
            first = rec.first_id.name if rec.first_id else ''
            middle = " ".join([middle.name for middle in rec.middle_ids]) if rec.middle_ids else ''
            nickname = " ".join([nickname.name for nickname in rec.nickname_ids]) if rec.nickname_ids else ''

            if nickname == '':
                given = first + ' ' + middle
                rec.given = given

            if nickname != '':
                given = first + ' ' + middle + ' (' + nickname + ')'
                rec.given = given

            if not first and not middle and nickname:
                given = nickname
                rec.given = given

            suffix = " ".join([suffix.name for suffix in rec.suffix_ids]) if rec.suffix_ids else ''

            full_name = given + ' ' + suffix
            rec.name = full_name
