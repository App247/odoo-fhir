# -*- coding: utf-8 -*-

from openerp import models, fields, api

class HealthcareService(models.Model):  
    _name = "hc.res.healthcare.service" 
    _description = "Healthcare Service"

    identifier_ids = fields.One2many(
        comodel_name="hc.healthcare.service.identifier", 
        inverse_name="healthcare_service_id", 
        string="Identifiers", 
        help="External Identifiers for this item.")       
    is_active = fields.Boolean(
        string="Active", 
        help="Whether this healthcare service is in active use.")
    provided_by_id = fields.Many2one(
        comodel_name="hc.res.organization", 
        string="Provided By", 
        help="The organization that provides this Healthcare Service.")      
    service_category_id = fields.Many2one(
        comodel_name="hc.vs.service.category", 
        string="Category", 
        help="Identifies the broad category of service being performed or delivered. Selecting a Service Category then determines the list of relevant service types that can be selected in the Primary Service Type.")        
    type_ids = fields.Many2many(
        comodel_name="hc.vs.service.type", 
        relation="healthcare_service_type_rel", 
        string="Types", 
        help="Type of service that may be delivered or performed.")
    specialty_ids = fields.Many2many(
        comodel_name="hc.vs.c80.practice.code",
        relation="healthcare_service_specialty_rel", 
        string="Specialties", 
        help="Collection of Specialties handled by the Service Site. This is more of a Medical Term.")
    location_ids = fields.One2many(
        comodel_name="hc.healthcare.service.location", 
        inverse_name="healthcare_service_id", 
        string="Location", 
        help="Location(s) where service may be provided.")        
    name = fields.Char(
        string="Name", 
        help="Further description of the service as it would be presented to a consumer while searching.")        
    comment = fields.Text(
        string="Comment", 
        help="Any additional description of the service and/or any specific issues not covered by the other attributes, which can be displayed as further detail under the serviceName.")       
    extra_details = fields.Text(
        string="Extra Details", 
        help="Extra details about the service that can't be placed in the other fields.")       
    photo_id = fields.Many2one(
        comodel_name="hc.healthcare.service.photo", 
        string="Photo", 
        help="If there is a photo/symbol associated with this Healthcare Service, it may be included here to facilitate quick identification of the service in a list.")       
    telecom_ids = fields.One2many(
        comodel_name="hc.healthcare.service.telecom", 
        inverse_name="healthcare_service_id", 
        string="Telecoms", 
        help="List of contacts related to this specific healthcare service. If this is empty, then refer to the location's contacts.")     
    coverage_area_ids = fields.One2many(
        comodel_name="hc.healthcare.service.coverage.area", 
        inverse_name="healthcare_service_id", 
        string="Coverage Areas", 
        help="The location(s) that this service is available to (not where the service is provided).")       
    service_provision_code_ids = fields.Many2many(
        comodel_name="hc.vs.service.provision.condition",
        relation="healthcare_service_service_provision_code_rel", 
        string="Service Provision Codes", 
        help="The code(s) that detail the conditions under which the healthcare service is available/offered.")
    eligibility_id = fields.Many2one(
        comodel_name="hc.vs.service.eligibility", 
        string="Eligibility", 
        help="Does this service have specific eligibility requirements that need to be met in order to use the service.")      
    eligibility_note = fields.Text(
        string="Eligibility Note", 
        help="Describes the eligibility conditions for the service.")     
    program_name_ids = fields.One2many(
        comodel_name="hc.healthcare.service.program.name", 
        inverse_name="healthcare_service_id", 
        string="Program Names", 
        help="Program Names that can be used to categorize the service.")       
    characteristic_ids = fields.Many2many(
        comodel_name="hc.vs.service.characteristic",
        relation="healthcare_service_characteristic_rel", 
        string="Characteristics", 
        help="Collection of Characteristics (attributes).")      
    referral_method_ids = fields.Many2many(
        comodel_name="hc.vs.service.referral.method",
        relation="healthcare_service_referral_method_rel", 
        string="Referral Methods", 
        help="Ways that the service accepts referrals.")              
    is_appointment_required = fields.Boolean(
        string="Appointment Required", 
        help="Indicates if an appointment is required for access to this service.")     
    availability_exceptions = fields.Text(
        string="Availability Exceptions", 
        help="A description of Site availability exceptions, e.g., public holiday availability. Succinctly describing all possible exceptions to normal Site availability as details in the Available Times and Not Available Times.")      
    endpoint_ids = fields.One2many(
        comodel_name="hc.healthcare.service.endpoint", 
        inverse_name="healthcare_service_id", 
        string="Endpoints", 
        help="Technical endpoints providing access to services operated for the location.")
    available_time_ids = fields.One2many(
        comodel_name="hc.healthcare.service.available.time", 
        inverse_name="healthcare_service_id", 
        string="Available Times", 
        help="A Collection of times that the Service Site is available.")
    not_available_ids = fields.One2many(
        comodel_name="hc.healthcare.service.not.available.time", 
        inverse_name="healthcare_service_id", 
        string="Not Available Times", 
        help="The Healthcare Service is not available during this period of time due to the provided reason.")

class HealthcareServiceAvailableTime(models.Model): 
    _name = "hc.healthcare.service.available.time"  
    _description = "Healthcare Service Available Time"      
    _inherit = ["hc.available.time"]    

    healthcare_service_id = fields.Many2one(
        comodel_name="hc.res.healthcare.service", 
        string="Healthcare Service", 
        help="Healthcare Service associated with this Healthcare Service Available Time.")                 

class HealthcareServiceNotAvailableTime(models.Model):  
    _name = "hc.healthcare.service.not.available.time"  
    _description = "Healthcare Service Not Available Time"      
    _inherit = ["hc.not.available.time"]

    healthcare_service_id = fields.Many2one(
        comodel_name="hc.res.healthcare.service", 
        string="Healthcare Service", 
        help="Healthcare Service associated with this Healthcare Service Not Available.")                 

class HealthcareServiceIdentifier(models.Model):    
    _name = "hc.healthcare.service.identifier"  
    _description = "Healthcare Service Identifier"          
    _inherit = ["hc.basic.association", "hc.identifier"]    

    healthcare_service_id = fields.Many2one(
        comodel_name="hc.res.healthcare.service", 
        string="Healthcare Service", 
        help="Healthcare Service associated with this Healthcare Service Identifier.")                       

class HealthcareServiceLocation(models.Model):  
    _name = "hc.healthcare.service.location"    
    _description = "Healthcare Service Location"            
    _inherit = ["hc.basic.association"] 
    _inherits = {"hc.res.location": "location_id"}

    location_id = fields.Many2one(
        comodel_name="hc.res.location", 
        string="Location", 
        ondelete="restrict", 
        required="True", 
        help="Location associated with this Healthcare Service Location.")                       
    healthcare_service_id = fields.Many2one(
        comodel_name="hc.res.healthcare.service", 
        string="Healthcare Service", 
        help="Healthcare Service associated with this Healthcare Service Location.")   

class HealthcareServicePhoto(models.Model): 
    _name = "hc.healthcare.service.photo" 
    _description = "Healthcare Service Photo"           
    _inherit = ["hc.basic.association", "hc.attachment"]                       

class HealthcareServiceTelecom(models.Model):   
    _name = "hc.healthcare.service.telecom" 
    _description = "Healthcare Service Telecom"         
    _inherit = ["hc.contact.point.use"] 
    _inherits = {"hc.contact.point": "telecom_id"}

    telecom_id = fields.Many2one(
        comodel_name="hc.contact.point", 
        string="Telecom", 
        ondelete="restrict", 
        required="True", 
        help="Telecom associated with this Healthcare Service Telecom.")                      
    healthcare_service_id = fields.Many2one(
        comodel_name="hc.res.healthcare.service", 
        string="Healthcare Service", 
        help="Healthcare Service associated with this Healthcare Service Telecom.")                      

class HealthcareServiceCoveredArea(models.Model):   
    _name = "hc.healthcare.service.coverage.area"    
    _description = "Healthcare Service Coverage Area"            
    _inherit = ["hc.basic.association"] 
    _inherits = {"hc.res.location": "location_id"}

    location_id = fields.Many2one(
        comodel_name="hc.res.location", 
        string="Location", 
        ondelete="restrict", 
        required="True", 
        help="Location associated with this Healthcare Service Coverage Area.")                       
    healthcare_service_id = fields.Many2one(
        comodel_name="hc.res.healthcare.service", 
        string="Healthcare Service", 
        help="Healthcare Service associated with this Healthcare Service Coverage Area.")

class HealthcareServiceProgramName(models.Model):   
    _name = "hc.healthcare.service.program.name"    
    _description = "Healthcare Service Program Name"            
    _inherit = ["hc.basic.association"] 

    healthcare_service_id = fields.Many2one(
        comodel_name="hc.res.healthcare.service", 
        string="Healthcare Service", 
        help="Healthcare Service associated with this Healthcare Service Program Name.")                     
    name = fields.Char(
        string="Name", 
        help="Name of this healthcare service.")                      

class HealthcareServiceEndpoint(models.Model):  
    _name = "hc.healthcare.service.endpoint"    
    _description = "Healthcare Service Endpoint"            
    _inherit = ["hc.basic.association"] 

    healthcare_service_id = fields.Many2one(
        comodel_name="hc.res.healthcare.service", 
        string="Healthcare Service", 
        help="Healthcare Service associated with this Healthcare Service Endpoint.")                     
    endpoint_id = fields.Many2one(
        comodel_name="hc.res.endpoint", 
        string="Endpoint", 
        help="Endpoint associated with this Healthcare Service Endpoint.")                     

class ServiceType(models.Model):    
    _name = "hc.vs.service.type"    
    _description = "Service Type"       
    _inherit = ["hc.value.set.contains"]

    name = fields.Char(
        string="Name", 
        help="Name of this service type.")
    code = fields.Char(
        string="Code", 
        help="Code of this service type.")
    contains_id = fields.Many2one(
        comodel_name="hc.vs.service.type", 
        string="Parent", 
        help="Parent service type.")

class ServiceProvisionCondition(models.Model): 
    _name = "hc.vs.service.provision.condition"    
    _description = "Service Provision Condition"       
    _inherit = ["hc.value.set.contains"]

    name = fields.Char(
        string="Name", 
        help="Name of this service provision condition.")
    code = fields.Char(
        string="Code", 
        help="Code of this service provision condition.")
    contains_id = fields.Many2one(
        comodel_name="hc.vs.service.provision.condition", 
        string="Parent", 
        help="Parent service provision condition.")    

class ServiceCategory(models.Model):    
    _name = "hc.vs.service.category"    
    _description = "Service Category"       
    _inherit = ["hc.value.set.contains"]

    name = fields.Char(
        string="Name", 
        help="Name of this service category.")
    code = fields.Char(
        string="Code", 
        help="Code of this service category.")
    contains_id = fields.Many2one(
        comodel_name="hc.vs.service.category", 
        string="Parent", 
        help="Parent service category.")
   
class ServiceEligibility(models.Model): 
    _name = "hc.vs.service.eligibility" 
    _description = "Service Eligibility"        
    _inherit = ["hc.value.set.contains"]    

    name = fields.Char(
        string="Name", 
        help="Name of this service eligibility.")
    code = fields.Char(
        string="Code", 
        help="Code of this service eligibility.")
    contains_id = fields.Many2one(
        comodel_name="hc.vs.service.eligibility", 
        string="Parent", 
        help="Parent service eligibility.")

class ServiceReferralMethod(models.Model):  
    _name = "hc.vs.service.referral.method" 
    _description = "Service Referral Method"        
    _inherit = ["hc.value.set.contains"]

    name = fields.Char(
        string="Name", 
        help="Name of this service referral method.")
    code = fields.Char(
        string="Code", 
        help="Code of this service referral method.")
    contains_id = fields.Many2one(
        comodel_name="hc.vs.service.referral.method", 
        string="Parent", 
        help="Parent service referral method.")    

class ServiceCharacteristic(models.Model):  
    _name = "hc.vs.service.characteristic"  
    _description = "Service Characteristic"     
    _inherit = ["hc.value.set.contains"]

    name = fields.Char(
        string="Name", 
        help="Name of this service characteristic.")
    code = fields.Char(
        string="Code", 
        help="Code of this service characteristic.")
    contains_id = fields.Many2one(
        comodel_name="hc.vs.service.characteristic", 
        string="Parent", 
        help="Parent service characteristic.")