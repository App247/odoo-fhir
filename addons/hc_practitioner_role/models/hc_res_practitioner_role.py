# -*- coding: utf-8 -*-

from openerp import models, fields, api

class PractitionerRole(models.Model):   
    _name = "hc.res.practitioner.role"  
    _description = "Practitioner Role"
    _inherits = {"hc.res.person": "person_id"}

    person_id = fields.Many2one(
        comodel_name="hc.res.person",
        string="Person",
        required="True",
        ondelete="restrict",
        help="Person who is this practitioner.")  
    name = fields.Char(
        string="Name", 
        required="True", 
        help="Text representation of the practitioner role. Practitioner + Organization + Period Start Date.")
    practitioner_id = fields.Many2one(
        comodel_name="hc.res.practitioner", 
        string="Practitioner", 
        help="Practitioner that is able to provide the defined services for the organization.")
    organization_id = fields.Many2one(
        comodel_name="hc.res.organization", 
        string="Organization", 
        help="Organization where the roles are performed.")
    role_ids = fields.Many2many(
        comodel_name="hc.vs.practitioner.role", 
        relation="practitioner_role_role_rel", 
        string="Roles", 
        help="Roles which this practitioner may perform.")
    specialty_ids = fields.Many2many(
        comodel_name="hc.vs.c80.practice.code", 
        relation="practitioner_role_specialty_rel", 
        string="Specialties", 
        help="Specific specialty of the practitioner.")
    identifier_ids = fields.One2many(
        comodel_name="hc.practitioner.role.identifier", 
        inverse_name="practitioner_role_id", 
        string="Identifiers", 
        help="Business Identifiers that are specific to a role/location.")
    is_active = fields.Boolean(
        string="Active", 
        help="Whether this practitioner role record is in active use.")
    telecom_ids = fields.One2many(
        comodel_name="hc.practitioner.role.telecom", 
        inverse_name="practitioner_role_id", 
        string="Telecoms", 
        help="Contact details that are specific to the role/location/service.")
    period_start_date = fields.Datetime(
        string="Period Start Date", 
        help="Start of the the period during which the practitioner is authorized to perform in these role(s).")
    period_end_date = fields.Datetime(
        string="Period End Date", 
        help="End of the the period during which the practitioner is authorized to perform in these role(s).")
    location_ids = fields.Many2many(
        comodel_name="hc.practitioner.role.location", 
        inverse_name="practitioner_role_id",       
        relation="location_practitioner_role_rel",
        string="Locations", 
        help="The location(s) at which this practitioner provides care.")
    healthcare_service_ids = fields.One2many(
        comodel_name="hc.practitioner.role.healthcare.service", 
        inverse_name="practitioner_role_id", 
        string="Healthcare Services", 
        help="The list of healthcare services that this worker provides for this role's Organization/Location(s).")
    availability_exceptions = fields.Char(
        string="Availability Exceptions", 
        help="Description of availability exceptions.")                    

class PractitionerRoleAvailableTime(models.Model):  
    _name = "hc.practitioner.role.available.time" 
    _description = "Practitioner Role Available Time"
    _inherit =["hc.available.time"]

    practitioner_role_id = fields.Many2one(
        comodel_name="hc.res.practitioner.role",  
        string="Practitioner Role", 
        help="Practitioner Role associated with Practitioner Role Available Time.")       

class PractitionerRoleNotAvailableTime(models.Model):   
    _name = "hc.practitioner.role.not.available.time" 
    _description = "Practitioner Role Not Available Time"
    _inherit =["hc.not.available.time"]     

    practitioner_role_id = fields.Many2one(
        comodel_name="hc.res.practitioner.role",  
        string="Practitioner Role", 
        help="Practitioner Role associated with Practitioner Role Not Available Time.") 

class PractitionerRoleIdentifier(models.Model): 
    _name = "hc.practitioner.role.identifier"   
    _description = "Practitioner Role Identifier"       
    _inherits = {"hc.person.identifier": "person_identifier_id"}
    
    person_identifier_id = fields.Many2one(
        comodel_name="hc.person.identifier", 
        string="Person Identifier",
        required="True", 
        ondelete="restrict", 
        help="Person Identifier associated with this Practitioner Role Identifier.")
    practitioner_role_id = fields.Many2one(
        comodel_name="hc.res.practitioner.role",  
        string="Practitioner Role",
        help="Practitioner Role associated with this Practitioner Role Identifier.")              

class PractitionerRoleTelecom(models.Model):    
    _name = "hc.practitioner.role.telecom"  
    _description = "Practitioner Role Telecom"      
    _inherit = ["hc.contact.point.use"] 
    _inherits = {"hc.contact.point": "telecom_id"}

    telecom_id = fields.Many2one(
        comodel_name="hc.contact.point", 
        string="Telecom", 
        ondelete="restrict", 
        required="True", 
        help="Telecom associated with this Practitioner Role Telecom.")                   
    practitioner_role_id = fields.Many2one(
        comodel_name="hc.res.practitioner.role", 
        string="Practitioner Role", 
        help="Practitioner Role associated with this Practitioner Role Telecom.")                                 

class PractitionerRoleLocation(models.Model):   
    _name = "hc.practitioner.role.location" 
    _description = "Practitioner Role Location"     
    _inherit = ["hc.basic.association"]
    
    practitioner_role_id = fields.Many2one(
        comodel_name="hc.res.practitioner.role",  
        string="Practitioner Role", 
        help="Practitioner Role associated with this Practitioner Role Location.")                
    location_id = fields.Many2one(
        comodel_name="hc.res.location", 
        string="Location", 
        help="Location associated with this Practitioner Role Location.")               

class PractitionerRoleHealthcareService(models.Model):  
    _name = "hc.practitioner.role.healthcare.service"   
    _description = "Practitioner Role Healthcare Service"       
    _inherit = ["hc.basic.association"]

    practitioner_role_id = fields.Many2one(
        comodel_name="hc.res.practitioner.role",  
        string="Practitioner Role", 
        help="Practitioner role associated with this healthcare service.")              
    # healthcare_service_id = fields.Many2one(
    #     comodel_name="hc.res.healthcare service", 
    #     string="Healthcare Service", 
    #     help="Healthcare service associated with this practitioner role.")                                 

class PractitionerRoleRole(models.Model):  
    _name = "hc.vs.practitioner.role"  
    _description = "Practitioner Role" 
    _inherit = ["hc.value.set.contains"]   

# class PractitionerRoleAvailableTimeDaysOfWeek(models.Model):    
#     _name = "hc.practitioner.role.available.time.days.of.week"    
#     _description = "Practitioner Role Available Time Days Of Week"        

#     days_of_week = fields.Selection(
#         string="Days Of Week", 
#         selection=[
#             ("mon", "Mon"), 
#             ("tue", "Tue"), 
#             ("wed", "Wed"), 
#             ("thu", "Thu"), 
#             ("fri", "Fri"), 
#             ("sat", "Sat"), 
#             ("sun", "Sun")], 
#             help="Day of Week associated with the available time.")             
#     available_time_id = fields.Many2one(
#         comodel_name="hc.practitioner.role.available.time", 
#         string="Available Time", 
#         help="Available time associated with the day of week.")

# External Reference

class Practitioner(models.Model):
    _inherit = ["hc.res.practitioner"]

    role_ids = fields.One2many(
        comodel_name="hc.res.practitioner.role", 
        inverse_name="practitioner_id", 
        string="Roles", 
        help="Roles/organizations that the practitioner is associated with.")
