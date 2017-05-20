# -*- coding: utf-8 -*-

from openerp import models, fields, api

class Consent(models.Model):    
    _name = "hc.res.consent"    
    _description = "Consent"        

    identifier_id = fields.Many2one(
        comodel_name="hc.consent.identifier", 
        string="Identifier", 
        help="Identifier for this record (external references).")                
    status = fields.Selection(
        string="Status", 
        required="True", 
        selection=[
            ("draft", "Draft"), 
            ("proposed", "Proposed"), 
            ("active", "Active"), 
            ("rejected", "Rejected"), 
            ("inactive", "Inactive"), 
            ("entered-in-error", "Entered In Error")], 
        help="Indicates the current state of this consent.")               
    category_ids = fields.Many2many(
        comodel_name="hc.vs.consent.category",
        relation="consent_category_rel",  
        string="Categories", 
        help="Classification of the consent statement - for indexing/retrieval.")                
    patient_id = fields.Many2one(
        comodel_name="hc.res.patient", 
        string="Patient", 
        required="True", 
        help="Who the consent applies to.")                
    period_start_date = fields.Datetime(
        string="Period Start Date", 
        help="Start of the period that this consent applies.")              
    period_end_date = fields.Datetime(
        string="Period End Date", 
        help="End of the period that this consent applies.")                
    date_time = fields.Datetime(
        string="Date Time", 
        help="When this Consent was created or indexed.")        
    consenting_party_ids = fields.One2many(
        comodel_name="hc.consent.consenting.party", 
        inverse_name="consent_id", 
        string="Consenting Parties", 
        help="Who is agreeing to the policy and exceptions.")      
    action_ids = fields.Many2many(
        comodel_name="hc.vs.consent.action",
        relation="consent_action_rel", 
        string="Actions", 
        help="Actions controlled by this consent.")
    organization_ids = fields.One2many(
        comodel_name="hc.consent.organization", 
        inverse_name="consent_id", 
        string="Organizations", 
        help="Custodian of the consent.")           
    source_type = fields.Selection(
        string="Source Type", 
        selection=[
            ("attachment", "Attachment"), 
            ("identifier", "Identifier"), 
            ("consent", "Consent"), 
            ("document_reference", "Document Reference"), 
            ("contract", "Contract"), 
            ("questionnaire_response", "Questionnaire Response")],
        help="Type of source from which this consent is taken.")                
    source_name = fields.Char(
        string="Source", 
        compute="_compute_source_name", 
        store="True", 
        help="Source from which this consent is taken.")           
    source_attachment_id = fields.Many2one(
        comodel_name="hc.consent.source.attachment", 
        string="Source Attachment", 
        help="Attachment source from which this consent is taken.")             
    source_identifier_id = fields.Many2one(
        comodel_name="hc.consent.source.identifier", 
        string="Source Identifier", 
        help="Identifier source from which this consent is taken.")             
    source_consent_id = fields.Many2one(
        comodel_name="hc.res.consent", 
        string="Source Consent", 
        help="Consent source from which this consent is taken.")                
    source_document_reference_id = fields.Many2one(
        comodel_name="hc.res.document.reference", 
        string="Source Document Reference", 
        help="Document Reference source from which this consent is taken.")             
    source_contract_id = fields.Many2one(
        comodel_name="hc.res.contract", 
        string="Source Contract", 
        help="Contract source from which this consent is taken.")                
    source_questionnaire_response_id = fields.Many2one(
        comodel_name="hc.res.questionnaire.response", 
        string="Source Questionnaire Response", 
        help="Questionnaire Response source from which this consent is taken.")             
    policy_rule = fields.Char(
        string="Policy Rule URI", 
        help="Policy that this consents to.")
    security_label_ids = fields.Many2many(
        comodel_name="hc.vs.security.label", 
        relation="consent_security_label_rel", 
        string="Security Labels", 
        help="Security Labels that define affected resources.")
    purpose_ids = fields.Many2many(
        comodel_name="hc.vs.purpose.of.use", 
        relation="consent_purpose_rel", 
        string="Purposes", 
        help="Context of activities for which the agreement is made.")
    data_period_start_date = fields.Datetime(
        string="Data Period Start Date", 
        help="Start of the timeframe for data controlled by this consent.")
    data_period_end_date = fields.Datetime(
        string="Data Period End Date", 
        help="End of the timeframe for data controlled by this consent.")
           
    # Extension attribute
    witness_ids = fields.One2many(
        comodel_name="hc.consent.witness", 
        inverse_name="consent_id", 
        string="Witnesses", 
        help="Any witness to the consent.")    

    # Backbone Element
    actor_ids = fields.One2many(
        comodel_name="hc.consent.actor", 
        inverse_name="consent_id", 
        string="Actors", 
        help="Who|what controlled by this consent (or group, by role).")
    policy_ids = fields.One2many(
        comodel_name="hc.consent.policy", 
        inverse_name="consent_id", 
        string="Policies", 
        help="Policies covered by this consent.")
    data_ids = fields.One2many(
        comodel_name="hc.consent.data", 
        inverse_name="consent_id", 
        string="Policies", 
        help="Data controlled by this consent.")              
    except_ids = fields.One2many(
        comodel_name="hc.consent.except", 
        inverse_name="consent_id", 
        string="Excepts", 
        help="Additional rule - addition or removal of permissions.")

    @api.depends('source_type')         
    def _compute_source_name(self):         
        for hc_res_consent in self:     
            if hc_res_consent.source_type == 'consent': 
                hc_res_consent.source_name = hc_res_consent.source_consent_id.name
            elif hc_res_consent.source_type == 'document_reference':    
                hc_res_consent.source_name = hc_res_consent.source_document_reference_id.name
            elif hc_res_consent.source_type == 'contract':  
                hc_res_consent.source_name = hc_res_consent.source_contract_id.name
            elif hc_res_consent.source_type == 'questionnaire_response':    
                hc_res_consent.source_name = hc_res_consent.source_questionnaire_response_id.name

class ConsentActor(models.Model):
    _name = "hc.consent.actor"
    _description = "Consent Actor"

    consent_id = fields.Many2one(
        comodel_name="hc.res.consent", 
        string="Consent", 
        help="Consent associated with this Consent Actor.")       
    role_id = fields.Many2one(
        comodel_name="hc.vs.consent.actor.role", 
        string="Role", 
        required="True", 
        help="How the actor is involved.")       
    reference_type = fields.Selection(
        string="Reference Type", 
        required="True", 
        selection=[
            ("device", "Device"), 
            ("group", "Group"), 
            ("care_team", "Care Team"), 
            ("organization", "Organization"), 
            ("patient", "Patient"), 
            ("practitioner", "Practitioner"), 
            ("related_person", "Related Person")], 
        help="Type of resource for the actor (or group, by role).")     
    reference_name = fields.Char(
        string="Reference", 
        compute="_compute_reference_name", 
        store="True", 
        help="Resource for the actor (or group, by role).")       
    reference_device_id = fields.Many2one(
        comodel_name="hc.res.device", 
        string="Reference Device", 
        help="Device resource for the actor (or group, by role).")       
    reference_group_id = fields.Many2one(
        comodel_name="hc.res.group", 
        string="Reference Group", 
        help="Group resource for the actor (or group, by role).")       
    reference_care_team_id = fields.Many2one(
        comodel_name="hc.res.care.team", 
        string="Reference Care Team", 
        help="Care Team resource for the actor (or group, by role).")        
    reference_organization_id = fields.Many2one(
        comodel_name="hc.res.organization", 
        string="Reference Organization", 
        help="Organization resource for the actor (or group, by role).")       
    reference_patient_id = fields.Many2one(
        comodel_name="hc.res.patient", 
        string="Reference Patient", 
        help="Patient resource for the actor (or group, by role).")       
    reference_practitioner_id = fields.Many2one(
        comodel_name="hc.res.practitioner", 
        string="Reference Practitioner", 
        help="Practitioner resource for the actor (or group, by role).")       
    reference_related_person_id = fields.Many2one(
        comodel_name="hc.res.related.person", 
        string="Reference Related Person", 
        help="Related Person resource for the actor (or group, by role).")        

    @api.depends('reference_type')          
    def _compute_reference_name(self):          
        for hc_consent_actor in self:        
            if hc_consent_actor.reference_type == 'device':  
                hc_consent_actor.reference_name = hc_consent_actor.reference_device_id.name
            elif hc_consent_actor.reference_type == 'group': 
                hc_consent_actor.reference_name = hc_consent_actor.reference_group_id.name
            elif hc_consent_actor.reference_type == 'care_team': 
                hc_consent_actor.reference_name = hc_consent_actor.reference_care_team_id.name
            elif hc_consent_actor.reference_type == 'organization':  
                hc_consent_actor.reference_name = hc_consent_actor.reference_organization_id.name
            elif hc_consent_actor.reference_type == 'practitioner':  
                hc_consent_actor.reference_name = hc_consent_actor.reference_practitioner_id.name
            elif hc_consent_actor.reference_type == 'related_person':    
                hc_consent_actor.reference_name = hc_consent_actor.reference_related_person_id.name

class ConsentPolicy(models.Model):
    _name = "hc.consent.policy"
    _description = "Consent Policy"

    consent_id = fields.Many2one(
        comodel_name="hc.res.consent", 
        string="Consent", 
        help="Consent associated with this Consent Policy.")      
    authority = fields.Char(
        string="Authority URI", 
        help="Enforcement source for policy.")      
    uri = fields.Char(
        string="URI", 
        help="Specific policy covered by this consent.")        
        
class ConsentData(models.Model):
    _name = "hc.consent.data"
    _description = "Consent Data"

    consent_id = fields.Many2one(
        comodel_name="hc.res.consent", 
        string="Consent", 
        help="Consent associated with this Consent Data.")        
    meaning = fields.Selection(
        string="Meaning", 
        required="True", 
        selection=[
            ("instance", "Instance"), 
            ("related", "Related"), 
            ("dependents", "Dependents"), 
            ("authoredby", "Authored by")], 
        help="Action to take - permit or deny - when the exception conditions are met.")        
    reference_type = fields.Char(
        string="Reference Type", 
        compute="_compute_reference_type", 
        store="True", 
        required="True", 
        help="Type of the actual data reference.")      
    reference_name = fields.Reference(
        string="Reference", 
        selection="_reference_models", 
        help="The actual data reference.")     

class ConsentExcept(models.Model):  
    _name = "hc.consent.except" 
    _description = "Consent Except"     

    consent_id = fields.Many2one(
        comodel_name="hc.res.consent", 
        string="Consent", 
        help="Consent associated with this Consent Except.")              
    type = fields.Selection(
        string="Type", 
        required="True", 
        selection=[
            ("deny", "Deny"), 
            ("permit", "Permit")], 
        help="Action to take - permit or deny - when the exception conditions are met.")               
    period_start_date = fields.Datetime(
        string="Period Start Date", 
        help="Start of the timeframe for data controlled by this exception.")               
    period_end_date = fields.Datetime(
        string="Period End Date", 
        help="End of the timeframe for data controlled by this exception.")             
    action_ids = fields.Many2many(
        comodel_name="hc.vs.consent.action",
        relation="consent_except_action_rel",  
        string="Actions", 
        help="Actions controlled by this exception.")             
    security_label_ids = fields.Many2many(
        comodel_name="hc.vs.security.label",
        relation="consent_except_security_label_rel", 
        string="Security Labels", 
        help="Security Labels that define affected resources.")               
    purpose_ids = fields.Many2many(
        comodel_name="hc.vs.purpose.of.use",
        relation="consent_except_purpose_rel", 
        string="Purposes", 
        help="Context of activities covered by this exception.")               
    class_ids = fields.Many2many(
        comodel_name="hc.vs.consent.content.class",
        relation="consent_except_class_rel",
        string="Classes", 
        help="e.g. Resource Type, Profile, or CDA etc.")             
    code_ids = fields.Many2many(
        comodel_name="hc.vs.consent.content.code",
        relation="consent_except_code_rel",  
        string="Codes", 
        help="e.g. LOINC or SNOMED CT code, etc in the content.")               
    actor_ids = fields.One2many(
        comodel_name="hc.consent.except.actor", 
        inverse_name="except_id", 
        string="Actors", 
        help="Who|what controlled by this exception (or group, by role).")               
    data_ids = fields.One2many(
        comodel_name="hc.consent.except.data", 
        inverse_name="except_id", 
        string="Data", 
        help="Data controlled by this exception.")              

class ConsentExceptActor(models.Model):   
    _name = "hc.consent.except.actor"  
    _description = "Consent Except Actor"      

    except_id = fields.Many2one(
        comodel_name="hc.consent.except", 
        string="Except", 
        help="Except associated with this Consent Actor.")               
    role_id = fields.Many2one(
        comodel_name="hc.vs.consent.actor.role", 
        string="Role", 
        required="True", 
        help="How the actor is/was involved.")               
    reference_type = fields.Selection(
        string="Reference Type", 
        required="True", 
        selection=[
            ("device", "Device"), 
            ("group", "Group"), 
            ("care_team", "Care Team"), 
            ("organization", "Organization"), 
            ("patient", "Patient"), 
            ("practitioner", "Practitioner"), 
            ("related_person", "Related Person")],
        help="Type of resource for the actor (or group, by role).")             
    reference_name = fields.Char(
        string="Value", 
        compute="_compute_reference_name", 
        store="True", 
        help="Resource for the actor (or group, by role).")               
    reference_device = fields.Many2one(
        comodel_name="hc.res.device", 
        string="Reference Device", 
        help="Device resource for the actor (or group, by role).")              
    reference_group_id = fields.Many2one(
        comodel_name="hc.res.group", 
        string="Reference Group", 
        help="Group resource for the actor (or group, by role).")               
    reference_care_team_id = fields.Many2one(
        comodel_name="hc.res.care.team", 
        string="Reference Care Team", 
        help="Care Team resource for the actor (or group, by role).")                
    reference_organization_id = fields.Many2one(
        comodel_name="hc.res.organization", 
        string="Reference Organization", 
        help="Organization resource for the actor (or group, by role).")               
    reference_patient_id = fields.Many2one(
        comodel_name="hc.res.patient", 
        string="Reference Patient", 
        help="Patient resource for the actor (or group, by role).")               
    reference_practitioner_id = fields.Many2one(
        comodel_name="hc.res.practitioner", 
        string="Reference Practitioner", 
        help="Practitioner resource for the actor (or group, by role).")               
    reference_related_person_id = fields.Many2one(
        comodel_name="hc.res.related.person", 
        string="Reference Related Person", 
        help="Related Person resource for the actor (or group, by role).")                

    @api.depends('reference_type')          
    def _compute_reference_name(self):          
        for hc_consent_except_actor in self:        
            if hc_consent_except_actor.reference_type == 'device':  
                hc_consent_except_actor.reference_name = hc_consent_except_actor.reference_device_id.name
            elif hc_consent_except_actor.reference_type == 'group': 
                hc_consent_except_actor.reference_name = hc_consent_except_actor.reference_group_id.name
            elif hc_consent_except_actor.reference_type == 'care_team': 
                hc_consent_except_actor.reference_name = hc_consent_except_actor.reference_care_team_id.name
            elif hc_consent_except_actor.reference_type == 'organization':  
                hc_consent_except_actor.reference_name = hc_consent_except_actor.reference_organization_id.name
            elif hc_consent_except_actor.reference_type == 'practitioner':  
                hc_consent_except_actor.reference_name = hc_consent_except_actor.reference_practitioner_id.name
            elif hc_consent_except_actor.reference_type == 'related_person':    
                hc_consent_except_actor.reference_name = hc_consent_except_actor.reference_related_person_id.name

class ConsentExceptData(models.Model):    
    _name = "hc.consent.except.data"   
    _description = "Consent Except Data"       

    except_id = fields.Many2one(
        comodel_name="hc.consent.except", 
        string="Except", 
        help="Except associated with this Consent Data.")                
    meaning = fields.Selection(
        string="Meaning", 
        required="True", 
        selection=[
            ("instance", "Instance"), 
            ("related", "Related"), 
            ("dependents", "Dependents")], 
        help="How the resource reference is interpreted when testing consent restrictions.")            
    reference_type = fields.Char(
        string="Reference Type", 
        compute="_compute_reference_type", 
        store="True",
        required="True", 
        help="Type of the actual data reference.")
    reference_name = fields.Reference(
        string="Reference", 
        selection="_reference_models", 
        help="The actual data reference.")                              

    @api.model          
    def _reference_models(self):            
        models = self.env['ir.model'].search([('state', '!=', 'manual')])       
        return [(model.model, model.name)       
            for model in models 
                if model.model.startswith('hc.res')]
                
    @api.depends('reference_name')          
    def _compute_reference_type(self):          
        for this in self:       
            if this.reference_name: 
                this.reference_type = this.reference_name._description

class ConsentConsentingParty(models.Model): 
    _name = "hc.consent.consenting.party"
    _description = "Consent Consenting Party"
    _inherit = ["hc.basic.association"]

    consent_id = fields.Many2one(
        comodel_name="hc.res.consent", 
        string="Consent", 
        help="Consent associated with this Consent Consenting Party.")               
    consenting_party_type = fields.Selection(
        string="Consenting Party Type", 
        selection=[
            ("organization", "Organization"), 
            ("patient", "Patient"), 
            ("practitioner", "Practitioner"), 
            ("related_person", "Related Person")], 
        help="Type of who is agreeing to the policy and exceptions.")
    consenting_party_name = fields.Char(
        string="Consenting Party", 
        compute="_compute_consenting_party_name", 
        store="True", 
        help="Who is agreeing to the policy and exceptions.")
    consenting_party_organization_id = fields.Many2one(
        comodel_name="hc.res.organization", 
        string="Consenting Party Organization", 
        help="Organization who is agreeing to the policy and exceptions.")
    consenting_party_patient_id = fields.Many2one(
        comodel_name="hc.res.patient", 
        string="Consenting Party Patient", 
        help="Patient who is agreeing to the policy and exceptions.")
    conesenting_party_practitioner_id = fields.Many2one(
        comodel_name="hc.res.practitioner", 
        string="Conesenting Party Practitioner", 
        help="Practitioner who is agreeing to the policy and exceptions.")
    consenting_party_related_person_id = fields.Many2one(
        comodel_name="hc.res.related.person", 
        string="Consenting Party Related Person", 
        help="Related Person who is agreeing to the policy and exceptions.")
              
    @api.depends('consenting_party_type')           
    def _compute_consenting_party_name(self):           
        for hc_consent_consenting_party in self:        
            if hc_consent_consenting_party.consenting_party_type == 'organization': 
                hc_consent_consenting_party.consenting_party_name = hc_consent_consenting_party.consenting_party_organization_id.name
            elif hc_consent_consenting_party.consenting_party_type == 'patient':    
                hc_consent_consenting_party.consenting_party_name = hc_consent_consenting_party.consenting_party_patient_id.name
            elif hc_consent_consenting_party.consenting_party_type == 'practitioner':   
                hc_consent_consenting_party.consenting_party_name = hc_consent_consenting_party.consenting_party_practitioner_id.name
            elif hc_consent_consenting_party.consenting_party_type == 'related_person': 
                hc_consent_consenting_party.consenting_party_name = hc_consent_consenting_party.consenting_party_related_person_id.name
  
class ConsentOrganization(models.Model):
    _name = "hc.consent.organization"
    _description = "Consent Organization"
    _inherit = ["hc.basic.association"]

    consent_id = fields.Many2one(
        comodel_name="hc.res.consent", 
        string="Consent", 
        help="Consent associated with this Consent Organization.")                                
    recipient_type = fields.Selection(
        string="Recipient Type", 
        selection=[
            ("device", "Device"), 
            ("group", "Group"), 
            ("organization", "Organization"), 
            ("patient", "Patient"), 
            ("practitioner", "Practitioner"), 
            ("related_person", "Related Person"), 
            ("care_team", "Care Team")], 
        help="Type of whose access is controlled by the policy.")                                
    recipient_name = fields.Char(
        string="Recipient", 
        compute="_compute_recipient_name", 
        store="True", 
        help="Whose access is controlled by the policy.")                             
    recipient_device_id = fields.Many2one(
        comodel_name="hc.res.device", 
        string="Recipient Device", 
        help="Device whose access is controlled by the policy.")                             
    recipient_group_id = fields.Many2one(
        comodel_name="hc.res.group", 
        string="Recipient Group", 
        help="Group whose access is controlled by the policy.")                             
    recipient_organization_id = fields.Many2one(
        comodel_name="hc.res.organization", 
        string="Recipient Organization", 
        help="Organization whose access is controlled by the policy.")                             
    recipient_patient_id = fields.Many2one(
        comodel_name="hc.res.patient", 
        string="Recipient Patient", 
        help="Patient whose access is controlled by the policy.")                             
    recipient_practitioner_id = fields.Many2one(
        comodel_name="hc.res.practitioner", 
        string="Recipient Practitioner", 
        help="Practitioner whose access is controlled by the policy.")                             
    recipient_related_person_id = fields.Many2one(
        comodel_name="hc.res.related.person", 
        string="Recipient Related Person", 
        help="Related Person whose access is controlled by the policy.")                             
    recipient_care_team_id = fields.Many2one(
        comodel_name="hc.res.care.team", 
        string="Recipient Care Team", 
        help="Care Team whose access is controlled by the policy.")                             

    @api.depends('recipient_type')          
    def _compute_recipient_name(self):          
        for hc_consent_organization in self:        
            if hc_consent_organization.recipient_type == 'device':  
                hc_consent_organization.recipient_name = hc_consent_organization.recipient_device_id.name
            elif hc_consent_organization.recipient_type == 'group': 
                hc_consent_organization.recipient_name = hc_consent_organization.recipient_group_id.name
            elif hc_consent_organization.recipient_type == 'organization':  
                hc_consent_organization.recipient_name = hc_consent_organization.recipient_organization_id.name
            elif hc_consent_organization.recipient_type == 'patient':   
                hc_consent_organization.recipient_name = hc_consent_organization.recipient_patient_id.name
            elif hc_consent_organization.recipient_type == 'practitioner':  
                hc_consent_organization.recipient_name = hc_consent_organization.recipient_practitioner_id.name
            elif hc_consent_organization.recipient_type == 'related_person':    
                hc_consent_organization.recipient_name = hc_consent_organization.recipient_related_person_id.name
            elif hc_consent_organization.recipient_type == 'care_team': 
                hc_consent_organization.recipient_name = hc_consent_organization.recipient_care_team_id.name

class ConsentIdentifier(models.Model):  
    _name = "hc.consent.identifier" 
    _description = "Consent Identifier"     
    _inherit = ["hc.basic.association", "hc.identifier"]                                                                                             

class ConsentSourceAttachment(models.Model):    
    _name = "hc.consent.source.attachment"  
    _description = "Consent Source Attachment"      
    _inherit = ["hc.basic.association", "hc.attachment"]

class ConsentSourceIdentifier(models.Model):    
    _name = "hc.consent.source.identifier"  
    _description = "Consent Source Identifier"      
    _inherit = ["hc.basic.association", "hc.identifier"]

class ConsentWitness(models.Model):
    _name = "hc.consent.witness"
    _description = "Consent Witness"
    _inherit = ["hc.basic.association"]

    consent_id = fields.Many2one(
        comodel_name="hc.res.consent", 
        string="Consent", 
        help="Consent associated with this Consent Witness.")                             
    witness_type = fields.Selection(
        string="Witness Type", 
        selection=[
            ("organization", "Organization"), 
            ("patient", "Patient"), 
            ("practitioner", "Practitioner"), 
            ("related_person", "Related Person")], 
        help="Type of witness to the consent.")                               
    witness_name = fields.Char(
        string="Witness", 
        compute="_compute_witness_name", 
        store="True", 
        help="Any witness to the consent.")                             
    witness_organization_id = fields.Many2one(
        comodel_name="hc.res.organization", 
        string="Witness Organization", 
        help="Organization witness to the consent.")                               
    witness_patient_id = fields.Many2one(
        comodel_name="hc.res.patient", 
        string="Witness Patient", 
        elp="Patient witness to the consent.")                               
    witness_practitioner_id = fields.Many2one(
        comodel_name="hc.res.practitioner", 
        string="Witness Practitioner", 
        help="Practitioner witness to the consent.")                               
    witness_related_person_id = fields.Many2one(
        comodel_name="hc.res.related.person", 
        string="Witness Related Person", 
        help="Related Person witness to the consent.")                              

    @api.depends('witness_type')            
    def _compute_witness_name(self):            
        for hc_consent_witness in self:     
            if hc_consent_witness.witness_type == 'organization':   
                hc_consent_witness.witness_name = hc_consent_witness.witness_organization_id.name
            elif hc_consent_witness.witness_type == 'patient':  
                hc_consent_witness.witness_name = hc_consent_witness.witness_patient_id.name
            elif hc_consent_witness.witness_type == 'practitioner': 
                hc_consent_witness.witness_name = hc_consent_witness.witness_practitioner_id.name
            elif hc_consent_witness.witness_type == 'related_person':   
                hc_consent_witness.witness_name = hc_consent_witness.witness_related_person_id.name

class ConsentAction(models.Model):  
    _name = "hc.vs.consent.action"  
    _description = "Consent Action"     
    _inherit = ["hc.value.set.contains"]

class ConsentActorRole(models.Model):   
    _name = "hc.vs.consent.actor.role"  
    _description = "Consent Actor Role"     
    _inherit = ["hc.value.set.contains"]

class ConsentCategory(models.Model):    
    _name = "hc.vs.consent.category"    
    _description = "Consent Category"       
    _inherit = ["hc.value.set.contains"]

class ConsentContentClass(models.Model):    
    _name = "hc.vs.consent.content.class"   
    _description = "Consent Content Class"      
    _inherit = ["hc.value.set.contains"]

class ConsentContentCode(models.Model): 
    _name = "hc.vs.consent.content.code"    
    _description = "Consent Content Code"       
    _inherit = ["hc.value.set.contains"]
