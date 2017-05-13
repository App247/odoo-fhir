# -*- coding: utf-8 -*-

from openerp import models, fields, api

class PartnerTitle(models.Model):
    _inherit = ["res.partner.title"]

    description = fields.Text(
        string="Description",
        help="Describes a title/prefix.")
    type = fields.Selection(
        string="Type", 
        selection=[
            ("academic", "Academic"),
            ("generational", "Generational"),
            ("practitioner", "Healthcare Practitioner"), 
            ("honorary", "Honorary"),
            ("legal", "Legal"),
            ("organizational", "Organizational"),
            ("professional", "Professional"),
            ("religious", "Religious")],
        default="generational",
        help="Category of title.")

class HumanNameTermType(models.Model):
    _name = "hc.vs.human.name.term.type"
    _description = "Human Name Term Type"
    _inherit = ["hc.value.set.contains"]

    name = fields.Char(
        string="Name", 
        help="Name of this human name term type.")                                
    code = fields.Char(
        string="Code", 
        help="Code of this human name term type.")                                
    contains_id = fields.Many2one(
        comodel_name="hc.vs.human.name.term.type", 
        string="Parent", 
        help="Parent human name term type.")                              

class HumanNameTerm(models.Model):  
    _name = "hc.human.name.term" 
    _description = "Human Name Term"       

    name = fields.Char(
        string="Human Name Term",
        required="True", 
        help="A single term of a human name (e.g., John, Smith).")
    type_ids = fields.Many2many(
        comodel_name="hc.vs.human.name.term.type", 
        relation="human_name_term_type_rel", 
        string="Types", 
        help="Type of human name term.")

    _sql_constraints = [
        ("name_unique",
        "UNIQUE(name)",
        "The term must be unique.")
        ]

class HumanNameSuffix(models.Model):    
    _name = "hc.human.name.suffix"   
    _description = "Human Name Suffix"
    _inherit = ["res.partner.title"] 
    _order = "long_name"       

    name = fields.Char( 
        string="Suffix",
        required = "True",
        help="Characters that come after the given and last names. Aka post-nominal letters. May be a generational term (e.g., Jr.) a credential (e.g., RN), an honorary title (.e.g., OBE), or an academic degree (e.g., PhD).")
    long_name = fields.Char(
        string="Suffix Name", 
        help="Full text of suffix abbreviation (e.g., Junior for Jr.)")
    description = fields.Text(
        string="Description",
        help="Describes a suffix.")
    type = fields.Selection(
        help="Category of suffix.")

class HumanNameUse(models.Model):   
    _name = "hc.human.name.use" 
    _description = "Human Name Use"         
    _inherit = ["hc.basic.association"]

    use = fields.Selection(
        string="Use", 
        selection=[
            ("usual", "Usual"), 
            ("official", "Official"), 
            ("temp", "Temp"), 
            ("nickname", "Nickname"), 
            ("anonymous", "Anonymous"), 
            ("old", "Old"), 
            ("maiden", "Maiden")], 
        default="usual",
        help="The use of a human name.")                   
    start_date = fields.Datetime(
        string="Start Date", 
        help="Start of the time period when name was/is in use.")                 
    end_date = fields.Datetime(
        string="End Date", 
        help="End of the time period when name was/is in use.")
    
class HumanName(models.Model):
    _name = "hc.human.name"
    _description = "Human Name"
    
    name = fields.Char(
        compute='_compute_full_name',
        store="True",
        string="Full Name",
        help="A full text representation of the human name.")
    family = fields.Char(
        store="True",
        string="Family Name", 
        readonly="True",
        help="The terms of a name that links to the genealogy. (e.g., surname, birth last name).")
    given = fields.Char(
        store="True",
        string="Given Name", 
        readonly="True",
        help="Terms that identify a specific person (not always 'first'). Includes middle names.")
    prefix_ids = fields.Many2many(
        comodel_name="res.partner.title",
        relation="human_name_prefix_rel", 
        string="Prefix Names", 
        help="Terms that come before the full name.")
    suffix_ids = fields.Many2many(
        comodel_name="hc.human.name.suffix",
        relation="human_name_suffix_rel", 
        string="Suffix Names", 
        help="Terms that come after the full name.")
    first_id = fields.Many2one(
        comodel_name="hc.human.name.term", 
        string="First Name", 
        help="First term of a given name.")
    middle_ids = fields.Many2many(
        comodel_name="hc.human.name.term", 
        relation="middle_name_human_term_rel", 
        string="Middle Names", 
        help="Middle term of a given name.")
    initial_ids = fields.Many2many(
        comodel_name="hc.human.name.term", 
        relation="initial_name_human_term_rel", 
        string="Initial Names", 
        help="First letter of a term in a given name.")
    nickname_ids = fields.Many2many(
        comodel_name="hc.human.name.term", 
        relation="nickname_human_term_rel", 
        string="Nicknames", 
        help="Familiar term of a given name.")
    surname_id = fields.Many2one(
        comodel_name="hc.human.name.term", 
        string="Surname", 
        help="Hereditary name common to all members of a famly. Also known as family name, last name and patronymic.")
    previous_surname_ids = fields.Many2many(
        comodel_name="hc.human.name.term", 
        relation="human_name_previous_surname_rel", 
        string="Previous Married Last Names", 
        help="Previous married last name.")
    preferred_name = fields.Char(
        string="Preferred Name", 
        help="How the person prefers to be addressed in a conversation (e.g., John, Mr. Smith).")
    mother_maiden_id = fields.Many2one(
        comodel_name="hc.human.name.term", 
        string="Mother Maiden Family Name", 
        help="Mother's surname at birth. Part of the family name.")
    birth_surname_id = fields.Many2one(
        comodel_name="hc.human.name.term", 
        string="Birth Last Name", 
        help="Person's surname at birth.")
    display_order = fields.Selection(
        string="Display Name Order", 
        selection=[
            ("first_maiden_last", "First Last (default)"), 
            ("maiden_last_first", "Last First (e.g., East Asian name)"),
            ("first_last_maiden", "First Last Maiden (e.g., Hispanic name)")],
        default="first_maiden_last",
        help="The display order of this human name.")                 
    use = fields.Selection(
        string="Use", 
        selection=[
            ("usual", "Usual"), 
            ("official", "Official"), 
            ("temp", "Temp"), 
            ("nickname", "Nickname"), 
            ("anonymous", "Anonymous"), 
            ("old", "Old"), ("maiden", "Maiden")], 
        default="usual",
        help="The use of a human name.")
    
    # Requirements

    # No mandatory fields

    # compute: Given = First Name + Middle Names + Initial Names + "(" + Nicknames +")"
    # compute: Family = Mother Maiden Name + Birth Name + Previous Name + Last Name
    # compute: Family_Reverse = Birth Name + Previous Name + Last Name + Mother Maiden Name
    # compute: Full = Prefix + Given + Family + Suffix
    # compute: Full_Reverse = Prefix + Family + Given + Suffix
    # compute: Full_Family_Reverse = Prefix + Given + Family_Reverse + Suffix

    @api.depends('display_order', 'prefix_ids', 'first_id', 'middle_ids', 'initial_ids', 'nickname_ids', 'mother_maiden_id', 'surname_id', 'suffix_ids', 'previous_surname_ids', 'birth_surname_id')
    def _compute_full_name(self):
        for rec in self:
            first = rec.first_id.name if rec.first_id else ''
            middle = " ".join([middle.name for middle in rec.middle_ids]) if rec.middle_ids else ''
            initial = " ".join([initial.name for initial in rec.initial_ids]) if rec.initial_ids else ''
            nickname = " ".join([nickname.name for nickname in rec.nickname_ids]) if rec.nickname_ids else ''

            if nickname == '':
                given = first + ' ' + middle + ' ' + initial
                rec.given = given

            if nickname != '':
                given = first + ' ' + middle + ' ' + initial + ' (' + nickname + ')'
                rec.given = given

            mother_maiden = rec.mother_maiden_id.name if rec.mother_maiden_id else ''
            birth_surname = rec.birth_surname_id.name if rec.birth_surname_id else ''
            previous_surname = " ".join([previous_surname.name for previous_surname in rec.previous_surname_ids]) if rec.previous_surname_ids else ''
            surname = rec.surname_id.name if rec.surname_id else ''
            family = mother_maiden + ' ' + birth_surname + ' ' + previous_surname + ' ' + surname
            rec.family = family

            family_reverse = birth_surname + ' ' + surname + ' ' + mother_maiden
            
            prefix = " ".join([prefix.name for prefix in rec.prefix_ids]) if rec.prefix_ids else ''
            suffix = " ".join([suffix.name for suffix in rec.suffix_ids]) if rec.suffix_ids else ''
            
            if rec.display_order == 'first_maiden_last':
                full = prefix + ' ' + given + ' ' + family + ' ' + suffix
                rec.name = full

            if rec.display_order == 'maiden_last_first':
                full_reverse = prefix + ' ' + family + ' ' + given + ' ' + suffix
                rec.name = full_reverse

            if rec.display_order == 'first_last_maiden':
                full_family_reverse = prefix + ' ' + given + ' ' + family_reverse + ' ' + suffix
                rec.name = full_family_reverse