# -*- coding: utf-8 -*-

from openerp import models, fields, api

class Contract(models.Model):    
    _name = "hc.res.contract"    
    _description = "Contract"        

    identifier_id = fields.Many2one(
        comodel_name="hc.contract.identifier", 
        string="Identifier", 
        help="Contract identifier.")                
    issued = fields.Datetime(
        string="Issued Date", 
        help="When this Contract was issued.")                
    start_date = fields.Datetime(
        string="Start Date", 
        help="Start of the effective time.")                
    end_date = fields.Datetime(
        string="End Date", 
        help="End of the effective time.")                
    subject_type = fields.Selection(
        string="Subject Type", 
        selection=[
            ("string", "String"), 
            ("code", "Code")], 
        help="Type of subject of this Contract.")                
    subject_name = fields.Char(
        string="Subject", 
        compute="_compute_subject_name", 
        store="True", 
        help="Subject of this Contract.")                
    subject_string = fields.Char(
        string="Subject String", 
        help="String of subject of this contract.")                
    subject_code_id = fields.Many2one(
        comodel_name="hc.vs.resource.type", 
        string="Subject Code", 
        help="Code subject of this contract.")                
    topic_type = fields.Selection(
        string="Topic Type", 
        selection=[
            ("string", "String"), 
            ("code", "Code")], 
        help="Type of context of the Contract.")                
    topic_name = fields.Char(
        string="Topic", 
        compute="_compute_topic_name", 
        store="True", 
        help="Context of the Contract.")                
    topic_string = fields.Char(
        string="Topic String", 
        help="String of context of the contract.")                
    topic_code_id = fields.Many2one(
        comodel_name="hc.vs.resource.type", 
        string="Topic Code", 
        help="Code context of the contract.")                
    authority_ids = fields.One2many(
        comodel_name="hc.contract.authority", 
        inverse_name="contract_id", 
        string="Authorities", 
        help="Authority under which this Contract has standing.")                
    domain_ids = fields.One2many(
        comodel_name="hc.contract.domain", 
        inverse_name="contract_id", 
        string="Domains", 
        help="Domain in which this Contract applies.")                
    type_id = fields.Many2one(
        comodel_name="hc.vs.contract.type", 
        string="Type", 
        help="Contract Type.")                
    sub_type_ids = fields.Many2many(
        comodel_name="hc.vs.contract.sub.type", 
        relation="contract_sub_type_rel", 
        string="Sub Types", 
        help="Contract Sub Type.")                
    action_ids = fields.Many2many(
        comodel_name="hc.vs.contract.action", 
        relation="contract_action_rel", 
        string="Actions", 
        help="Contract Action.")                
    action_reason_ids = fields.Many2many(
        comodel_name="hc.vs.purpose.of.use", 
        relation="contract_action_reason_rel", 
        string="Action Reasons", 
        help="Contract Action Reason.")                
    binding_type = fields.Selection(
        string="Binding Type", 
        required="True", 
        selection=[
            ("attachment", "Attachment"), 
            ("composition", "Composition"), 
            ("document_reference", "Document Reference"), 
            ("questionnaire_response", "Questionnaire Response")], 
        help="Type of Binding Contract.")                
    binding_name = fields.Char(
        string="Binding", 
        compute="_compute_binding_name", 
        store="True", help="Binding Contract.")                
    binding_attachment_id = fields.Many2one(
        comodel_name="hc.contract.binding.attachment", 
        string="Binding Attachment", 
        help="Attachment binding contract.")                
    binding_composition_id = fields.Many2one(
        comodel_name="hc.res.composition", 
        string="Binding Composition", 
        help="Composition binding contract.")                
    binding_document_reference_id = fields.Many2one(
        comodel_name="hc.res.document.reference", 
        string="Binding Document Reference", 
        help="Document Reference binding contract.")                
    binding_questionnaire_response_id = fields.Many2one(
        comodel_name="hc.res.questionnaire.response", 
        string="Binding Questionnaire Response", 
        help="Questionnaire Response binding contract.")                
    agent_ids = fields.One2many(
        comodel_name="hc.contract.agent", 
        inverse_name="contract_id", 
        string="Agents", 
        help="Contract Agent.")                
    valued_item_ids = fields.One2many(
        comodel_name="hc.contract.valued.item", 
        inverse_name="contract_id", 
        string="Valued Items", 
        help="Contract Valued Item.")                
    signer_ids = fields.One2many(
        comodel_name="hc.contract.signatory", 
        inverse_name="contract_id", 
        string="Signatories", 
        help="Contract Signatory.")                
    term_ids = fields.One2many(
        comodel_name="hc.contract.term", 
        inverse_name="contract_id", 
        string="Terms", 
        help="Contract Term List.")                
    friendly_ids = fields.One2many(
        comodel_name="hc.contract.friendly.language", 
        inverse_name="contract_id", 
        string="Friendly Languages", 
        help="Contract Friendly Language.")
    legal_ids = fields.One2many(
        comodel_name="hc.contract.legal.language", 
        inverse_name="contract_id", 
        string="Legal Languages", 
        help="Contract Legal Language.")
    rule_ids = fields.One2many(
        comodel_name="hc.contract.computable.language", 
        inverse_name="contract_id", 
        string="Computable Languages", 
        help="Contract Computable Language.")

class ContractAgent(models.Model):    
    _name = "hc.contract.agent"    
    _description = "Contract Agent"        

    contract_id = fields.Many2one(
        comodel_name="hc.res.contract", 
        string="Contract", 
        help="Contract associated with this Contract Agent.")                
    actor_type = fields.Selection(
        string="Actor Type", 
        required="True", 
        selection=[
            ("Contract", "Contract"), 
            ("Device", "Device"), 
            ("Group", "Group"), 
            ("Location", "Location"), 
            ("Organization", "Organization"), 
            ("Patient", "Patient"), 
            ("Practitioner", "Practitioner"), 
            ("Related Person", "Related Person"),
            ("Substance", "Substance")], 
        help="Type of Contract Agent Type.")
    actor_name = fields.Char(
        string="Actor", 
        compute="_compute_actor_name", 
        store="True", 
        help="Contract Agent Type.")                
    actor_contract_id = fields.Many2one(
        comodel_name="hc.res.contract", 
        string="Actor Contract", 
        help="Contract who or what parties are assigned roles in this contract.")                
    actor_device_id = fields.Many2one(
        comodel_name="hc.res.device", 
        string="Actor Device", 
        help="Device who or what parties are assigned roles in this contract.")                
    actor_group_id = fields.Many2one(
        comodel_name="hc.res.group", 
        string="Actor Group", 
        help="Group who or what parties are assigned roles in this contract.")                
    actor_location_id = fields.Many2one(
        comodel_name="hc.res.location", 
        string="Actor Location", 
        help="Location who or what parties are assigned roles in this contract.")                
    actor_organization_id = fields.Many2one(
        comodel_name="hc.res.organization", 
        string="Actor Organization", 
        help="Organization who or what parties are assigned roles in this contract.")                
    actor_patient_id = fields.Many2one(
        comodel_name="hc.res.patient", 
        string="Actor Patient", 
        help="Patient who or what parties are assigned roles in this contract.")                
    actor_practitioner_id = fields.Many2one(
        comodel_name="hc.res.practitioner", 
        string="Actor Practitioner", 
        help="Practitioner who or what parties are assigned roles in this contract.")                
    actor_related_person_id = fields.Many2one(
        comodel_name="hc.res.related.person", 
        string="Actor Related Person", 
        help="Related Person who or what parties are assigned roles in this contract.")                
    actor_substance_id = fields.Many2one(
        comodel_name="hc.res.substance", 
        string="Actor Substance", 
        help="Substance who or what parties are assigned roles in this contract.")                
    role_ids = fields.Many2many(
        comodel_name="hc.vs.contract.actor.role", 
        relation="contract_agent_role_rel", 
        string="Roles", 
        help="Contract Actor Role.")                

class ContractValuedItem(models.Model):    
    _name = "hc.contract.valued.item"    
    _description = "Contract Valued Item"        

    contract_id = fields.Many2one(
        comodel_name="hc.res.contract", 
        string="Contract", 
        help="Contract associated with this Contract Valued Item.")                
    entity_type = fields.Selection(
        string="Entity Type", 
        required="True", 
        selection=[
            ("Item Type", "Item Type"), 
            ("code", "Code"), 
            ("string", "String")], 
        help="Type of Contract Valued Item Type.")                
    entity_name = fields.Char(
        string="Entity",
        compute="_compute_entity_name", 
        store="True", 
        help="Contract Valued Item Type.")                
    entity_item_type_id = fields.Many2one(
        comodel_name="hc.vs.contract.valued.item.type", 
        string="Entity Item type", 
        help="Contract valued item type.")                
    entity_string = fields.Char(
        string="Entity String", 
        help="String of contract valued item type.")                
    entity_code_id = fields.Many2one(
        comodel_name="hc.vs.resource.type", 
        string="Entity Code", 
        help="Code of contract valued item type.")                
    identifier_id = fields.Many2one(
        comodel_name="hc.contract.valued.item.identifier", 
        string="Identifier", 
        help="Contract Valued Item Identifier.")                
    effective_time = fields.Datetime(
        string="Effective Time", 
        help="Contract Valued Item Effective Tiem.")                
    quantity = fields.Integer(
        string="Quantity", 
        help="Count of Contract Valued Items.")
    quantity_uom_id = fields.Many2one(
        comodel_name="product.uom", 
        string="Quantity UOM", 
        help="Quantity unit of measure.")                 
    unit_price = fields.Float(
        string="Unit Price", 
        help="Contract Valued Item fee, charge, or cost.")                
    factor = fields.Float(
        string="Contract Valued Item Price Scaling Factor.", 
        help="Contract Valued Item Price Scaling Factor.")                
    points = fields.Float(
        string="Contract Valued Item Difficulty Scaling Factor.", 
        help="Contract Valued Item Difficulty Scaling Factor.")                
    net_amount = fields.Float(
        string="Net Amount", 
        help="Total Contract Valued Item Value.")                

class ContractSignatory(models.Model):    
    _name = "hc.contract.signatory"    
    _description = "Contract Signatory"        

    contract_id = fields.Many2one(
        comodel_name="hc.res.contract", 
        string="Contract", 
        help="Contract associated with this Contract Signatory.")                
    type_id = fields.Many2one(
        comodel_name="hc.vs.contract.signer.type", 
        string="Type", 
        required="True", 
        help="Contract Signer Type.")                
    party_type = fields.Selection(
        string="Party Type", 
        required="True", 
        selection=[
            ("organization", "Organization"), 
            ("patient", "Patient"),
            ("practitioner", "Practitioner"),
            ("related_person", "Related Person")], 
        help="Type of Contract Signatory Party.")                
    party_name = fields.Char(
        string="Party", 
        compute="_compute_party_name", 
        store="True", 
        help="Contract Signatory Party.")                
    party_organization_id = fields.Many2one(
        comodel_name="hc.res.organization", 
        string="Party Organization", 
        required="True", 
        help="Organization contract signatory party.")                
    party_patient_id = fields.Many2one(
        comodel_name="hc.res.patient", 
        string="Party Patient", 
        help="Patient contract signatory party.")                
    party_practitioner_id = fields.Many2one(
        comodel_name="hc.res.practitioner", 
        string="Party Practitioner", 
        help="Practitioner contract signatory party.")                
    party_related_person_id = fields.Many2one(
        comodel_name="hc.res.related.person", 
        string="Party Related Person", 
        help="Related Person contract signatory party.")                
    signature_ids = fields.One2many(
        comodel_name="hc.contract.signatory.signature", 
        inverse_name="signatory_id", 
        string="Signatures", 
        required="True", 
        help="Contract Documentation Signature.")                

class ContractTerm(models.Model):    
    _name = "hc.contract.term"    
    _description = "Contract Term"        

    contract_id = fields.Many2one(
        comodel_name="hc.res.contract", 
        string="Contract", 
        help="Contract associated with this Contract Term.")                
    identifier_id = fields.Many2one(
        comodel_name="hc.contract.term.identifier", 
        string="Identifier", 
        help="Contract Term identifier.")                
    issued = fields.Datetime(
        string="Issued Date", 
        help="Contract Term Issue Date Time.")                
    start_date = fields.Datetime(
        string="Start Date", 
        help="Start of the contract term effective time.")                
    end_date = fields.Datetime(
        string="End Date", 
        help="End of the contract term effective time.")                
    type_id = fields.Many2one(
        comodel_name="hc.vs.contract.term.type", 
        string="Type", 
        help="Contract Term Type.")                
    sub_type_id = fields.Many2one(
        comodel_name="hc.vs.contract.term.sub.type", 
        string="Sub Type", 
        help="Contract Term Sub Type.")                
    topic_type = fields.Selection(
        string="Topic Type", 
        selection=[
            ("string", "String"), 
            ("code", "Code")], 
        help="Type of context of the Contract term.")                
    topic_name = fields.Char(
        string="Topic", 
        compute="_compute_topic_name", 
        store="True", 
        help="Context of the Contract term.")                
    topic_string = fields.Char(
        string="Topic String", 
        help="String of context of the contract term.")                
    topic_code_id = fields.Many2one(
        comodel_name="hc.vs.resource.type", 
        string="Topic Code", 
        help="Code context of the contract.")                
    action_ids = fields.Many2many(
        comodel_name="hc.vs.contract.action", 
        relation="contract_term_action_rel", 
        string="Actions", 
        help="Contract Term Action.")                
    action_reason_ids = fields.Many2many(
        comodel_name="hc.vs.purpose.of.use", 
        relation="contract_term_action_reason_rel", 
        string="Action Reasons", 
        help="Contract Term Action Reason.")                
    text = fields.Text(
        string="Text", 
        help="Human readable Contract term text.")                
    group_id = fields.Many2one(
        comodel_name="hc.contract.term", 
        string="Group", 
        help="Nested Contract Term Group.")                
    agent_ids = fields.One2many(
        comodel_name="hc.contract.term.agent", 
        inverse_name="term_id", 
        string="Agents", 
        help="Term Agent List.")                
    valued_item_ids = fields.One2many(
        comodel_name="hc.contract.term.valued.item", 
        inverse_name="term_id", 
        string="Valued Items", 
        help="Term Valued Item.")                

class ContractTermAgent(models.Model):    
    _name = "hc.contract.term.agent"    
    _description = "Contract Term Agent"        

    term_id = fields.Many2one(
        comodel_name="hc.contract.term", 
        string="Term", 
        help="Term List.")                
    actor_type = fields.Selection(
        string="Actor Type", 
        required="True", 
        selection=[
            ("Contract", "Contract"), 
            ("Device", "Device"), 
            ("Group", "Group"), 
            ("Location", "Location"), 
            ("Organization", "Organization"), 
            ("Patient", "Patient"), 
            ("Practitioner", "Practitioner"), 
            ("Related Person", "Related Person"),
            ("Substance", "Substance")], 
        help="Type of Contract Term Agent List.")
    actor_name = fields.Char(
        string="Actor", 
        compute="_compute_actor_name", 
        store="True", 
        help="Contract Term Agent List.")                
    actor_contract_id = fields.Many2one(
        comodel_name="hc.res.contract", 
        string="Actor Contract", 
        required="True", 
        help="Contract who or what parties are assigned roles in this contract.")                
    actor_device_id = fields.Many2one(
        comodel_name="hc.res.device", 
        string="Actor Device", 
        help="Device who or what parties are assigned roles in this contract.")                
    actor_group_id = fields.Many2one(
        comodel_name="hc.res.group", 
        string="Actor Group", 
        help="Group who or what parties are assigned roles in this contract.")                
    actor_location_id = fields.Many2one(
        comodel_name="hc.res.location", 
        string="Actor Location", 
        elp="Location who or what parties are assigned roles in this contract.")                
    actor_organization_id = fields.Many2one(
        comodel_name="hc.res.organization", 
        string="Actor Organization", 
        help="Organization who or what parties are assigned roles in this contract.")                
    actor_patient_id = fields.Many2one(
        comodel_name="hc.res.patient", 
        string="Actor Patient", 
        help="Patient who or what parties are assigned roles in this contract.")                
    actor_practitioner_id = fields.Many2one(
        comodel_name="hc.res.practitioner", 
        string="Actor Practitioner", 
        help="Practitioner who or what parties are assigned roles in this contract.")                
    actor_related_person_id = fields.Many2one(
        comodel_name="hc.res.related.person", 
        string="Actor Related Person", 
        help="Related Person who or what parties are assigned roles in this contract.")                
    actor_substance_id = fields.Many2one(
        comodel_name="hc.res.substance", 
        string="Actor Substance", 
        help="Substance who or what parties are assigned roles in this contract.")                
    role_ids = fields.Many2many(
        comodel_name="hc.vs.contract.actor.role", 
        relation="contract_term_agent_role_rel", 
        string="Roles", 
        help="Contract Term Actor Role.")                

class ContractTermValuedItem(models.Model):    
    _name = "hc.contract.term.valued.item"    
    _description = "Contract Term Valued Item"        

    term_id = fields.Many2one(
        comodel_name="hc.contract.term", 
        string="Term", 
        help="Term List.")                
    entity_type = fields.Selection(
        string="Entity Type", 
        selection=[
            ("Item Type", "Item Type"), 
            ("code", "Code"), 
            ("string", "String")], 
        help="Type of Contract Term Valued Item.")                
    entity_name = fields.Char(
        string="Entity", 
        compute="_compute_entity_name", 
        store="True", 
        help="Contract Term Valued Item Type.")                
    entity_item_type_id = fields.Many2one(
        comodel_name="hc.vs.contract.term.valued.item.type", 
        string="Entity Item Type", 
        help="Contract term valued item type.")                
    entity_string = fields.Char(
        string="Entity String", 
        help="String of contract term valued item type.")                
    entity_code_id = fields.Many2one(
        comodel_name="hc.vs.resource.type", 
        string="Entity Code", 
        help="Code of contract term valued item type.")                
    identifier_id = fields.Many2one(
        comodel_name="hc.contract.term.valued.item.identifier", 
        string="Identifier", 
        help="Contract Term Valued Item Identifier.")                
    effective_time = fields.Datetime(
        string="Effective Time", 
        help="Contract Term Valued Item Effective Tiem.")                
    quantity = fields.Integer(
        string="Quantity", 
        help="Contract Term Valued Item Count.")
    quantity_uom_id = fields.Many2one(
        comodel_name="product.uom", 
        string="Quantity UOM", 
        help="Quantity unit of measure.")               
    unit_price = fields.Float(
        string="Unit Price", 
        help="Contract Term Valued Item fee, charge, or cost.")                
    factor = fields.Float(
        string="Contract Term Valued Item Price Scaling Factor.", 
        help="Contract Term Valued Item Price Scaling Factor.")                
    points = fields.Float(
        string="Contract Term Valued Item Difficulty Scaling Factor.", 
        help="Contract Term Valued Item Difficulty Scaling Factor.")                
    net_amount = fields.Float(
        string="Net Amount", 
        help="Total Contract Term Valued Item Value.")                

class ContractFriendlyLanguage(models.Model):    
    _name = "hc.contract.friendly.language"    
    _description = "Contract Friendly Language"        

    contract_id = fields.Many2one(
        comodel_name="hc.res.contract", 
        string="Contract", 
        help="Contract associated with this Contract Friendly Language.")                
    content_type = fields.Selection(
        string="Content Type", 
        required="True", 
        selection=[
            ("attachment", "Attachment"),
            ("composition", "Composition"),
            ("document_reference", "Document Reference"),
            ("questionnaire_response", "Questionnaire Response")],
        help="Type of easily comprehended representation of this Contract.")                
    content_name = fields.Char(
        string="Content", 
        compute="_compute_content_name", 
        store="True", 
        help="Easily comprehended representation of this Contract.")                
    content_attachment_id = fields.Many2one(
        comodel_name="hc.contract.friendly.language.content.attachment", 
        string="Content Attachment",  
        help="Attachment easily comprehended representation of this contract.")                
    content_composition_id = fields.Many2one(
        comodel_name="hc.res.composition", 
        string="Content Composition", 
        help="Composition easily comprehended representation of this contract.")                
    content_document_reference_id = fields.Many2one(
        comodel_name="hc.res.document.reference", 
        string="Content Document Reference", 
        help="Document Reference easily comprehended representation of this contract.")                
    content_questionnaire_response_id = fields.Many2one(
        comodel_name="hc.res.questionnaire.response", 
        string="Content Questionnaire Response", 
        help="Questionnaire Response easily comprehended representation of this contract.")                

class ContractLegalLanguage(models.Model):    
    _name = "hc.contract.legal.language"    
    _description = "Contract Legal Language"        

    contract_id = fields.Many2one(
        comodel_name="hc.res.contract", 
        string="Contract", 
        help="Contract associated with this Contract Legal Language.")                
    content_type = fields.Selection(
        string="Content Type", 
        required="True", 
        selection=[
            ("attachment", "Attachment"),
            ("composition", "Composition"),
            ("document_reference", "Document Reference"),
            ("questionnaire_response", "Questionnaire Response")],
        help="Type of Contract Legal Text.")                
    content_name = fields.Char(
        string="Content", 
        compute="_compute_content_name", 
        store="True", 
        help="Contract Legal Text.")                
    content_attachment_id = fields.Many2one(
        comodel_name="hc.contract.legal.language.content.attachment", 
        string="Content Attachment",  
        help="Attachment contract legal text.")                
    content_composition_id = fields.Many2one(
        comodel_name="hc.res.composition", 
        string="Content Composition", 
        help="Composition contract legal text.")                
    content_document_reference_id = fields.Many2one(
        comodel_name="hc.res.document.reference", 
        string="Content Document Reference", 
        help="Document Reference contract legal text.")                
    content_questionnaire_response_id = fields.Many2one(
        comodel_name="hc.res.questionnaire.response", 
        string="Content Questionnaire Response",  
        help="Questionnaire Response contract legal text.")                

class ContractComputableLanguage(models.Model):    
    _name = "hc.contract.computable.language"    
    _description = "Contract Computable Language"        

    contract_id = fields.Many2one(
        comodel_name="hc.res.contract", 
        string="Contract", 
        help="Contract associated with this Contract Computable Language.")                
    content_type = fields.Selection(
        string="Content Type", 
        required="True", 
        selection=[
            ("Attachment", "Attachment"), 
            ("Document Reference", "Document Reference")], 
        help="Type of Computable Contract Rules.")                
    content_name = fields.Char(
        string="Content", 
        compute="_compute_content_name", 
        store="True", 
        help="Computable Contract Rules.")                
    content_attachment_id = fields.Many2one(
        comodel_name="hc.contract.computable.language.content.attachment", 
        string="Content Attachment", 
        required="True", 
        help="Attachment computable contract rules.")                
    content_document_reference_id = fields.Many2one(
        comodel_name="hc.res.document.reference", 
        string="Content Document Reference", 
        required="True", 
        help="Document Reference computable contract rules.")                           

class ContractIdentifier(models.Model):    
    _name = "hc.contract.identifier"    
    _description = "Contract Identifier"        
    _inherit = ["hc.basic.association", "hc.identifier"]

class ContractAuthority(models.Model):    
    _name = "hc.contract.authority"    
    _description = "Contract Authority"        
    _inherit = ["hc.basic.association"]

    contract_id = fields.Many2one(
        comodel_name="hc.res.contract", 
        string="Contract", 
        help="Contract associated with this Contract Contract Authority.")
    authority_id = fields.Many2one(
        comodel_name="hc.res.organization", 
        string="Authority", 
        help="Organization associated with this Contract Authority.")                

class ContractDomain(models.Model):    
    _name = "hc.contract.domain"    
    _description = "Contract Domain"        
    _inherit = ["hc.basic.association"]

    contract_id = fields.Many2one(
        comodel_name="hc.res.contract", 
        string="Contract", 
        help="Contract associated with this Contract Contract Domain.")
    domain_id = fields.Many2one(
        comodel_name="hc.res.location", 
        string="Domain", 
        help="Location associated with this Contract Domain.")
                
class ContractBindingAttachment(models.Model):    
    _name = "hc.contract.binding.attachment"    
    _description = "Contract Binding Attachment"        
    _inherit = ["hc.basic.association", "hc.attachment"]

class ContractValuedItemIdentifier(models.Model):    
    _name = "hc.contract.valued.item.identifier"    
    _description = "Contract Valued Item Identifier"        
    _inherit = ["hc.basic.association", "hc.identifier"]

class ContractSignatorySignature(models.Model):    
    _name = "hc.contract.signatory.signature"    
    _description = "Contract Signatory Signature"        
    _inherit = ["hc.basic.association"]

    signatory_id = fields.Many2one(
        comodel_name="hc.contract.signatory", 
        string="Signatory", 
        help="Signatory associated with this Contract Signatory Signature.")
    signature_id = fields.Many2one(
        comodel_name="hc.signature", 
        string="Signature", 
        help="Signature associated with this Contract Signatory Signature.")

class ContractTermIdentifier(models.Model):    
    _name = "hc.contract.term.identifier"    
    _description = "Contract Term Identifier"        
    _inherit = ["hc.basic.association", "hc.identifier"]

class ContractTermValuedItemIdentifier(models.Model):    
    _name = "hc.contract.term.valued.item.identifier"    
    _description = "Contract Term Valued Item Identifier"        
    _inherit = ["hc.basic.association", "hc.identifier"]

class ContractFriendlyLanguageContentAttachment(models.Model):    
    _name = "hc.contract.friendly.language.content.attachment"    
    _description = "Contract Friendly Language Content Attachment"        
    _inherit = ["hc.basic.association", "hc.attachment"]

class ContractLegalLanguageContentAttachment(models.Model):    
    _name = "hc.contract.legal.language.content.attachment"    
    _description = "Contract Legal Language Content Attachment"        
    _inherit = ["hc.basic.association", "hc.attachment"]

class ContractComputableLanguageContentAttachment(models.Model):    
    _name = "hc.contract.computable.language.content.attachment"    
    _description = "Contract Computable Language Content Attachment"        
    _inherit = ["hc.basic.association", "hc.attachment"]

class ContractAction(models.Model):    
    _name = "hc.vs.contract.action"    
    _description = "Contract Action"        
    _inherit = ["hc.value.set.contains"]

class ContractActorRole(models.Model):    
    _name = "hc.vs.contract.actor.role"    
    _description = "Contract Actor Role"        
    _inherit = ["hc.value.set.contains"]

class ContractSignerType(models.Model):    
    _name = "hc.vs.contract.signer.type"    
    _description = "Contract Signer Type"        
    _inherit = ["hc.value.set.contains"]

class ContractSubType(models.Model):    
    _name = "hc.vs.contract.sub.type"    
    _description = "Contract Sub Type"        
    _inherit = ["hc.value.set.contains"]

class ContractTermSubType(models.Model):    
    _name = "hc.vs.contract.term.sub.type"    
    _description = "Contract Term Sub Type"        
    _inherit = ["hc.value.set.contains"]

class ContractTermType(models.Model):    
    _name = "hc.vs.contract.term.type"    
    _description = "Contract Term Type"        
    _inherit = ["hc.value.set.contains"]

class ContractTermValuedItemType(models.Model):    
    _name = "hc.vs.contract.term.valued.item.type"    
    _description = "Contract Term Valued Item Type"        
    _inherit = ["hc.value.set.contains"]

class ContractType(models.Model):
    _name = "hc.vs.contract.type"    
    _description = "Contract Type"        
    _inherit = ["hc.value.set.contains"]

class ContractValuedItemType(models.Model):    
    _name = "hc.vs.contract.valued.item.type"    
    _description = "Contract Valued Item Type"        
    _inherit = ["hc.value.set.contains"]

# External reference

class CoverageContract(models.Model):
    _inherit = "hc.coverage.contract"

    contract_id = fields.Many2one(
        comodel_name="hc.res.contract", 
        string="Contract", 
        help="Contract associated with this Coverage Contract.")
