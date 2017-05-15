# -*- coding: utf-8 -*-

from openerp import models, fields, api

class Immunization(models.Model):    
    _name = "hc.res.immunization"    
    _description = "Immunization"        

    name = fields.Char(
        string="Event Name", 
        compute="_compute_name", 
        store="True", 
        help="Text representation of the immunization event. Patient + Vaccine + Date.")
    identifier_ids = fields.One2many(
        comodel_name="hc.immunization.identifier", 
        inverse_name="immunization_id", 
        string="Identifiers", 
        help="Business identifier.")                
    status = fields.Selection(
        string="Status", 
        required="True", 
        selection=[
            ("in-progress", "In-Progress"), 
            ("on-hold", "On-Hold"), 
            ("completed", "Completed"), 
            ("entered-in-error", "Entered-In-Error"), 
            ("stopped", "Stopped")], 
        help="The status of the diagnostic report as a whole.")                
    date = fields.Datetime(
        string="Date", 
        required="True", 
        help="Vaccination administration date.")                
    vaccine_code_id = fields.Many2one(
        comodel_name="hc.vs.vaccine.code", 
        string="Vaccine Code", 
        required="True", 
        help="Vaccine product administered.")                
    patient_id = fields.Many2one(
        comodel_name="hc.res.patient", 
        string="Patient", 
        required="True", 
        help="Who was immunized")                
    is_was_not_given = fields.Boolean(
        string="Was Not Given", 
        required="True", 
        help="Flag for whether immunization was given")                
    is_reported = fields.Boolean(
        string="Reported", 
        required="True", 
        help="Indicates a self-reported record")                
    performer_id = fields.Many2one(
        comodel_name="hc.res.practitioner", 
        string="Performer", 
        help="Who administered vaccine")                
    requester_id = fields.Many2one(
        comodel_name="hc.res.practitioner", 
        string="Requester", 
        help="Who ordered vaccination")                
    encounter_id = fields.Many2one(
        comodel_name="hc.res.encounter", 
        string="Encounter", 
        help="Encounter administered as part of.")                
    manufacturer_id = fields.Many2one(
        comodel_name="hc.res.organization", 
        string="Manufacturer", 
        help="Vaccine manufacturer.")                
    location_id = fields.Many2one(
        comodel_name="hc.res.location", 
        string="Location", 
        help="Where vaccination occurred")                
    lot_number = fields.Char(
        string="Lot Number", 
        help="Vaccine lot number.")                
    expiration_date = fields.Date(
        string="Expiration Date", 
        help="Vaccine expiration date.")                
    site_id = fields.Many2one(
        comodel_name="hc.vs.immunization.site", 
        string="Site", 
        help="Body site vaccine was administered.")                
    route_id = fields.Many2one(
        comodel_name="hc.vs.immunization.route", 
        string="Route", 
        help="How vaccine entered body.")                
    dose_quantity = fields.Float(
        string="Dose Quantity", 
        help="Amount of vaccine administered.")                
    note_ids = fields.One2many(
        comodel_name="hc.immunization.note", 
        inverse_name="immunization_id", 
        string="Notes", 
        help="Vaccination notes.")                
    explanation_id = fields.Many2one(
        comodel_name="hc.immunization.explanation", 
        string="Explanation", 
        help="Administration / non-administration reasons.")                
    reaction_ids = fields.One2many(
        comodel_name="hc.immunization.reaction", 
        inverse_name="immunization_id", 
        string="Reactions", 
        help="Details of a reaction that follows immunization.")                
    vaccination_protocol_ids = fields.One2many(
        comodel_name="hc.immunization.vaccination.protocol", 
        inverse_name="immunization_id", 
        string="Vaccination Protocols", 
        help="What protocol was followed.")                

class ImmunizationExplanation(models.Model):    
    _name = "hc.immunization.explanation"    
    _description = "Immunization Explanation"        

    immunization_id = fields.Many2one(
        comodel_name="hc.res.immunization", 
        string="Immunization", 
        help="Immunization associated with this Immunization Explanation.")                
    reason_ids = fields.Many2many(
        comodel_name="hc.vs.immunization.reason", 
        relation="immunization_explanation_reason_rel", 
        string="Reasons", 
        help="Why immunization occurred.")
    reason_not_given_ids = fields.Many2many(
        comodel_name="hc.vs.no.immunization.reason", 
        relation="immunization_explanation_reason_not_given_rel", 
        string="Reasons Not Given", 
        help="Why immunization did not occur.")               

class ImmunizationReaction(models.Model):    
    _name = "hc.immunization.reaction"    
    _description = "Immunization Reaction"        

    immunization_id = fields.Many2one(
        comodel_name="hc.res.immunization", 
        string="Immunization", 
        help="Immunization associated with this Immunization Reaction.")                
    date = fields.Datetime(
        string="Date", 
        help="When reaction started")                
    detail_id = fields.Many2one(
        comodel_name="hc.res.observation", 
        string="Detail", 
        help="Additional information on reaction.")                
    is_reported = fields.Boolean(
        string="Reported", 
        help="Indicates self-reported reaction")                

class ImmunizationVaccinationProtocol(models.Model):    
    _name = "hc.immunization.vaccination.protocol"    
    _description = "Immunization Vaccination Protocol"        

    immunization_id = fields.Many2one(
        comodel_name="hc.res.immunization", 
        string="Immunization", 
        help="Immunization associated with this Immunization Vaccination Protocol.")                
    dose_sequence = fields.Integer(
        string="Dose Sequence", 
        help="Dose number within series")                
    description = fields.Text(
        string="Description", 
        help="Details of vaccine protocol.")                
    authority_id = fields.Many2one(
        comodel_name="hc.res.organization", 
        string="Authority", 
        help="Who is responsible for protocol.")                
    series = fields.Char(
        string="Series", 
        help="Name of vaccine series.")                
    series_doses = fields.Integer(
        string="Series Doses", 
        help="Recommended number of doses for immunity.")                
    target_disease_ids = fields.Many2many(
        comodel_name="hc.vs.vaccination.protocol.dose.target", 
        relation="immunization_vaccination_protocol_target_disease_rel", 
        string="Target Diseases", 
        required="True", 
        help="Disease immunized against.")              
    dose_status_id = fields.Many2one(
        comodel_name="hc.vs.vaccination.protocol.dose.status", 
        string="Dose Status", 
        required="True", 
        help="Indicates if dose counts towards immunity")                
    dose_status_reason_id = fields.Many2one(
        comodel_name="hc.vs.vaccination.protocol.dose.status.reason", 
        string="Dose Status Reason", help="Why dose does (not) count")                

class ImmunizationIdentifier(models.Model):    
    _name = "hc.immunization.identifier"    
    _description = "Immunization Identifier"        
    _inherit = ["hc.basic.association", "hc.identifier"]

    immunization_id = fields.Many2one(
        comodel_name="hc.res.immunization", 
        string="Immunization", 
        help="Immunization associated with this Immunization Identifier.")                

class ImmunizationNote(models.Model):    
    _name = "hc.immunization.note"    
    _description = "Immunization Note"        
    _inherit = ["hc.basic.association", "hc.annotation"]

    immunization_id = fields.Many2one(
        comodel_name="hc.res.immunization", 
        string="Immunization", 
        help="Immunization associated with this Immunization Note.")                               

class ImmunizationRoute(models.Model):    
    _name = "hc.vs.immunization.route"    
    _description = "Immunization Route"        
    _inherit = ["hc.value.set.contains"]

class ImmunizationSite(models.Model):    
    _name = "hc.vs.immunization.site"    
    _description = "Immunization Site"        
    _inherit = ["hc.value.set.contains"]

class VaccinationProtocolDoseStatus(models.Model):    
    _name = "hc.vs.vaccination.protocol.dose.status"    
    _description = "Vaccination Protocol Dose Status"        
    _inherit = ["hc.value.set.contains"]

class VaccinationProtocolDoseStatusReason(models.Model):    
    _name = "hc.vs.vaccination.protocol.dose.status.reason"    
    _description = "Vaccination Protocol Dose Status Reason"        
    _inherit = ["hc.value.set.contains"]

class VaccineCode(models.Model):    
    _name = "hc.vs.vaccine.code"    
    _description = "Vaccine Code"        
    _inherit = ["hc.value.set.contains"]

class VaccinationProtocolDoseTarget(models.Model):    
    _name = "hc.vs.vaccination.protocol.dose.target"    
    _description = "Vaccination Protocol Dose Target"        
    _inherit = ["hc.value.set.contains"]

class ImmunizationReason(models.Model):    
    _name = "hc.vs.immunization.reason"    
    _description = "Immunization Reason"        
    _inherit = ["hc.value.set.contains"]

class NoImmunizationReason(models.Model):    
    _name = "hc.vs.no.immunization.reason"    
    _description = "No Immunization Reason"        
    _inherit = ["hc.value.set.contains"]

