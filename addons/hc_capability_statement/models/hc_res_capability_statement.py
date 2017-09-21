# -*- coding: utf-8 -*-

from openerp import models, fields, api
from datetime import datetime
from openerp.tools import DEFAULT_SERVER_DATETIME_FORMAT as DTF

class CapabilityStatement(models.Model):
    _name = "hc.res.capability.statement"
    _description = "Capability Statement"
    _rec_name = "title"

    url = fields.Char(
        string="URI",
        help="Logical URI to reference this capability statement (globally unique).")
    version = fields.Char(
        string="Version",
        help="Business version of the capability statement.")
    name = fields.Char(
        string="Name",
        help="Name for this capability statement (Computer friendly).")
    title = fields.Char(
        string="Title",
        help="Name for this capability statement (Human friendly).")
    status_id = fields.Many2one(
        comodel_name="hc.vs.publication.status",
        string="Status",
        required="True",
        help="The status of this capability statement. Enables tracking the life-cycle of the content.")
    status_history_ids = fields.One2many(
        comodel_name="hc.capability.statement.status.history",
        inverse_name="capability_statement_id",
        string="Status History",
        help="The status of the capability statement over time.")
    is_experimental = fields.Boolean(
        string="Experimental",
        help="If for testing purposes, not real usage.")
    date = fields.Datetime(
        string="Date",
        required="True",
        help="Date this was last changed.")
    publisher = fields.Char(
        string="Publisher",
        help="Name of the publisher (Organization or individual).")
    contact_ids = fields.One2many(
        comodel_name="hc.capability.statement.contact",
        inverse_name="capability_statement_id",
        string="Contacts",
        help="Contact details for the publisher.")
    description = fields.Text(
        string="Description",
        help="Natural language description of the capability statement.")
    use_context_ids = fields.One2many(
        comodel_name="hc.capability.statement.use.context",
        inverse_name="capability_statement_id",
        string="Use Contexts",
        help="Content intends to support these contexts.")
    jurisdiction_ids = fields.Many2many(
        comodel_name="hc.vs.jurisdiction",
        relation="capability_statement_jurisdiction_rel",
        string="Jurisdictions",
        help="Intended jurisdiction for capability statement (if applicable).")
    purpose = fields.Text(
        string="Purpose",
        help="Why this capability statement is defined.")
    copyright = fields.Text(
        string="Copyright",
        help="Use and/or publishing restrictions.")
    kind = fields.Selection(
        string="Kind",
        required="True",
        selection=[
            ("instance", "Instance"),
            ("capability", "Capability"),
            ("requirements", "Requirements")],
        help="The way that this statement is intended to be used.")
    instantiates_ids = fields.One2many(
        comodel_name="hc.capability.statement.instantiates",
        inverse_name="capability_statement_id",
        string="Instantiates URIs",
        help="Canonical URL of service implemented/used by software.")
    fhir_version = fields.Char(
        string="FHIR Version",
        required="True",
        help="FHIR Version the system uses.")
    accept_unknown = fields.Selection(
        string="Accept Unknown",
        required="True",
        selection=[
            ("no", "No"),
            ("extensions", "Extensions"),
            ("elements", "Elements"),
            ("both", "Both")],
        help="A code that indicates whether the application accepts unknown elements or extensions when reading resources.")
    format_ids = fields.One2many(
        comodel_name="hc.capability.statement.format",
        inverse_name="capability_statement_id",
        string="Formats",
        required="True",
        help="Formats supported.")
    patch_format_ids = fields.Many2many(
        comodel_name="hc.vs.mime.type",
        relation="capability_statement_patch_format_rel",
        string="Patch Formats",
        help="Patch formats supported.")
    implementation_guide_ids = fields.One2many(
        comodel_name="hc.capability.statement.implementation.guide",
        inverse_name="capability_statement_id",
        string="Implementation Guide URIs",
        help="Implementation Guide supported.")
    profile_ids = fields.One2many(
        comodel_name="hc.capability.statement.profile",
        inverse_name="capability_statement_id",
        string="Profiles",
        help="Profiles for use cases supported.")
    software_ids = fields.One2many(
        comodel_name="hc.capability.statement.software",
        inverse_name="capability_statement_id",
        string="Software",
        help="Software that is covered by this capability statement.")
    implementation_ids = fields.One2many(
        comodel_name="hc.capability.statement.implementation",
        inverse_name="capability_statement_id",
        string="Implementations",
        help="If this describes a specific instance.")
    rest_ids = fields.One2many(
        comodel_name="hc.capability.statement.rest",
        inverse_name="capability_statement_id",
        string="RESTs",
        help="If the endpoint is a RESTful one.")
    messaging_ids = fields.One2many(
        comodel_name="hc.capability.statement.messaging",
        inverse_name="capability_statement_id",
        string="Messaging",
        help="If messaging is supported.")
    document_ids = fields.One2many(
        comodel_name="hc.capability.statement.document",
        inverse_name="capability_statement_id",
        string="Documents",
        help="Document definition.")

    @api.model
    def create(self, vals):
        status_history_obj = self.env['hc.capability.statement.status.history']
        res = super(CapabilityStatement, self).create(vals)
        if vals and vals.get('status_id'):
            status_history_vals = {
                'capability_statement_id': res.id,
                'status' : res.status_id.name,
                'start_date': datetime.today()
                }
            status_history_obj.create(status_history_vals)
        return res

    @api.multi
    def write(self, vals):
        status_history_obj = self.env['hc.capability.statement.status.history']
        publication_status_obj = self.env['hc.vs.publication.status']
        res = super(CapabilityStatement, self).write(vals)
        status_history_record_ids = status_history_obj.search([('end_date','=', False)])
        if status_history_record_ids:
            if vals.get('status_id') and status_history_record_ids[0].status != vals.get('status_id'):
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
                publication_status = publication_status_obj.browse(vals.get('status_id'))
                status_history_vals = {
                    'capability_statement_id': self.id,
                    'status': publication_status.name,
                    'start_date': datetime.today()
                    }
                status_history_obj.create(status_history_vals)
        return res

class CapabilityStatementSoftware(models.Model):
    _name = "hc.capability.statement.software"
    _description = "Capability Statement Software"

    capability_statement_id = fields.Many2one(
        comodel_name="hc.res.capability.statement",
        string="Capability Statement",
        help="Capability Statement associated with this Capability Statement Software.")
    name = fields.Char(
        string="Name",
        required="True",
        help="A name the software is known by.")
    version = fields.Char(
        string="Version",
        help="Version covered by this statement.")
    release_date = fields.Datetime(
        string="Release Date",
        help="Date this version released.")

class CapabilityStatementImplementation(models.Model):
    _name = "hc.capability.statement.implementation"
    _description = "Capability Statement Implementation"

    capability_statement_id = fields.Many2one(
        comodel_name="hc.res.capability.statement",
        string="Capability Statement",
        help="Capability Statement associated with this Capability Statement Implementation.")
    description = fields.Text(
        string="Description",
        required="True",
        help="Describes this specific instance.")
    url = fields.Char(
        string="URI",
        help="Base URL for the installation.")

class CapabilityStatementRest(models.Model):
    _name = "hc.capability.statement.rest"
    _description = "Capability Statement REST"

    capability_statement_id = fields.Many2one(
        comodel_name="hc.res.capability.statement",
        string="Capability Statement",
        help="Capability Statement associated with this Capability Statement REST.")
    mode = fields.Selection(
        string="Mode",
        required="True",
        selection=[
            ("client", "Client"),
            ("server", "Server")],
        help="Identifies whether this portion of the statement is describing ability to initiate or receive restful operations.")
    documentation = fields.Text(
        string="Documentation",
        help="General description of implementation.")
    compartment_ids = fields.One2many(
        comodel_name="hc.capability.statement.rest.compartment",
        inverse_name="rest_id",
        string="Compartment URIs",
        help="URI of compartments served/used by system.")
    search_param_ids = fields.One2many(
        comodel_name="hc.capability.statement.rest.resource.search.param",
        inverse_name="rest_id",
        string="Search Params",
        help="Added items detail adjudication.")
    security_ids = fields.One2many(
        comodel_name="hc.capability.statement.rest.security",
        inverse_name="rest_id",
        string="Securities",
        help="Information about security of implementation.")
    resource_ids = fields.One2many(
        comodel_name="hc.capability.statement.rest.resource",
        inverse_name="rest_id",
        string="Resources",
        help="Resource served on the REST interface.")
    interaction_ids = fields.One2many(
        comodel_name="hc.capability.statement.rest.interaction",
        inverse_name="rest_id",
        string="Interactions",
        help="What operations are supported?")
    operation_ids = fields.One2many(
        comodel_name="hc.capability.statement.rest.operation",
        inverse_name="rest_id",
        string="Operations",
        help="Definition of an operation or a custom query.")

class CapabilityStatementRestSecurity(models.Model):
    _name = "hc.capability.statement.rest.security"
    _description = "Capability Statement REST Security"

    rest_id = fields.Many2one(
        comodel_name="hc.capability.statement.rest",
        string="REST",
        help="If the endpoint is a RESTful one.")
    is_cors = fields.Boolean(
        string="CORS",
        help="Adds CORS Headers (http://enable-cors.org/).")
    service_ids = fields.One2many(
        comodel_name="hc.capability.statement.rest.security.service",
        inverse_name="security_id",
        string="Services",
        help="Types of security services are supported/required by the system.")
    description = fields.Text(
        string="Description",
        help="General description of how security works.")
    certificate_ids = fields.One2many(
        comodel_name="hc.capability.statement.rest.security.certificate",
        inverse_name="security_id",
        string="Certificates",
        help="Certificates associated with security profiles.")

class CapabilityStatementRestSecurityCertificate(models.Model):
    _name = "hc.capability.statement.rest.security.certificate"
    _description = "Capability Statement REST Security Certificate"

    security_id = fields.Many2one(
        comodel_name="hc.capability.statement.rest.security",
        string="Security",
        help="Information about security of implementation.")
    type_id = fields.Many2one(
        comodel_name="hc.vs.mime.type",
        string="Type",
        help="MIME type for certificate.")
    blob = fields.Binary(
        string="Blob",
        help="Actual certificate.")

class CapabilityStatementRestResource(models.Model):
    _name = "hc.capability.statement.rest.resource"
    _description = "Capability Statement REST Resource"

    rest_id = fields.Many2one(
        comodel_name="hc.capability.statement.rest",
        string="REST",
        help="If the endpoint is a RESTful one.")
    type_id = fields.Many2one(
        comodel_name="hc.vs.resource.type",
        string="Type",
        required="True",
        help="A resource type that is supported.")
    profile_id = fields.Many2one(
        comodel_name="hc.res.structure.definition",
        string="Profile",
        help="Base System profile for all uses of resource.")
    documentation = fields.Text(
        string="Documentation",
        help="Additional information about the use of the resource type.")
    versioning = fields.Selection(
        string="Versioning",
        selection=[
            ("no-version", "No Version"),
            ("versioned", "Versioned"),
            ("versioned-update", "Versioned Update")],
        help="This field is set to no-version to specify that the system does not support (server) or use (client) versioning for this resource type.")
    is_read_history = fields.Boolean(
        string="Read History",
        help="Whether vRead can return past versions.")
    is_update_create = fields.Boolean(
        string="Update Create",
        help="If update can commit to a new identity.")
    is_conditional_create = fields.Boolean(
        string="Conditional Create",
        help="If allows/uses conditional create.")
    conditional_read = fields.Selection(
        string="Conditional Read",
        selection=[
            ("not-supported", "Not Supported"),
            ("modified-since", "Modified Since"),
            ("not-match", "Not Match"),
            ("full-support", "Full Support")],
        help="A code that indicates how the server supports conditional read.")
    is_conditional_update = fields.Boolean(
        string="Conditional Update",
        help="If allows/uses conditional update.")
    conditional_delete = fields.Selection(
        string="Conditional Delete",
        selection=[
            ("not-supported", "Not Supported"),
            ("single", "Single"),
            ("multiple", "Multiple")],
        help="How conditional delete is supported")
    reference_policy_ids = fields.One2many(
        comodel_name="hc.capability.statement.rest.resource.reference.policy",
        inverse_name="resource_id",
        string="Reference Policies",
        help="A set of flags that defines how references are supported..")
    search_include_ids = fields.One2many(
        comodel_name="hc.capability.statement.rest.resource.search.include",
        inverse_name="resource_id",
        string="Search Include",
        help="_include values supported by the server.")
    search_rev_include_ids = fields.One2many(
        comodel_name="hc.capability.statement.rest.resource.search.rev.include",
        inverse_name="resource_id",
        string="Search Rev Include",
        help="_revinclude values supported by the server.")
    search_param_ids = fields.One2many(
        comodel_name="hc.capability.statement.rest.resource.search.param",
        inverse_name="resource_id",
        string="Search Params",
        help="Search params supported by implementation.")
    interaction_ids = fields.One2many(
        comodel_name="hc.capability.statement.rest.resource.interaction",
        inverse_name="resource_id",
        string="Interactions",
        required="True",
        help="What operations are supported?")

class CapabilityStatementRestResourceInteraction(models.Model):
    _name = "hc.capability.statement.rest.resource.interaction"
    _description = "Capability Statement REST Resource Interaction"

    resource_id = fields.Many2one(
        comodel_name="hc.capability.statement.rest.resource",
        string="Resource",
        help="Resource served on the REST interface.")
    code = fields.Selection(
        string="Code",
        required="True",
        selection=[
            ("read", "Read"),
            ("vread", "Vread"),
            ("update", "Update"),
            ("patch", "Patch"),
            ("delete", "Delete"),
            ("history-instance", "History-Instance"),
            ("history-type", "History-Type"),
            ("create", "Create"),
            ("search-type", "Search-Type")],
        help="Coded identifier of the operation, supported by the system resource.")
    documentation = fields.Text(
        string="Documentation",
        help="Anything special about operation behavior.")

class CapabilityStatementRestResourceSearchParam(models.Model):
    _name = "hc.capability.statement.rest.resource.search.param"
    _description = "Capability Statement REST Resource Search Param"


    rest_id = fields.Many2one(
        comodel_name="hc.capability.statement.rest",
        string="REST",
        help="If the endpoint is a RESTful one.")
    resource_id = fields.Many2one(
        comodel_name="hc.capability.statement.rest.resource",
        string="Resource served on the REST interface.",
        help="")
    name = fields.Char(
        string="Name",
        required="True",
        help="Name of search parameter.")
    definition = fields.Char(
        string="Definition URI",
        help="Source of definition for parameter.")
    type = fields.Selection(
        string="Type",
        required="True",
        selection=[
            ("number", "Number"),
            ("date", "Date"),
            ("string", "String"),
            ("token", "Token"),
            ("reference", "Reference"),
            ("composite", "Composite"),
            ("quantity", "Quantity"),
            ("uri", "URI")],
        help="The type of value a search parameter refers to, and how the content is interpreted.")
    documentation = fields.Text(
        string="Documentation",
        help="Server-specific usage.")

class CapabilityStatementRestInteraction(models.Model):
    _name = "hc.capability.statement.rest.interaction"
    _description = "Capability Statement REST Interaction"

    rest_id = fields.Many2one(
        comodel_name="hc.capability.statement.rest",
        string="REST",
        help="If the endpoint is a RESTful one.")
    code = fields.Selection(
        string="Code",
        required="True",
        selection=[
            ("transaction", "Transaction"),
            ("batch", "Batch"),
            ("search-system", "Search System"),
            ("history-system", "History System")],
        help="A coded identifier of the operation, supported by the system.")
    documentation = fields.Text(
        string="Documentation",
        help="Anything special about operation behavior.")

class CapabilityStatementRestOperation(models.Model):
    _name = "hc.capability.statement.rest.operation"
    _description = "Capability Statement REST Operation"

    rest_id = fields.Many2one(
        comodel_name="hc.capability.statement.rest",
        string="REST",
        help="If the endpoint is a RESTful one.")
    name = fields.Char(
        string="Name",
        required="True",
        help="Name by which the operation/query is invoked.")
    definition_id = fields.Many2one(
        comodel_name="hc.res.operation.definition",
        string="Definition",
        required="True",
        help="The defined operation/query.")

class CapabilityStatementMessaging(models.Model):
    _name = "hc.capability.statement.messaging"
    _description = "Capability Statement Messaging"

    capability_statement_id = fields.Many2one(
        comodel_name="hc.res.capability.statement",
        string="Capability Statement",
        help="Capability Statement associated with this Capability Statement Messaging.")
    reliable_cache = fields.Integer(
        string="Reliable Cache",
        help="Reliable Message Cache Length (min).")
    documentation = fields.Text(
        string="Documentation",
        help="Messaging interface behavior details.")
    endpoint_ids = fields.One2many(
        comodel_name="hc.capability.statement.messaging.endpoint",
        inverse_name="messaging_id",
        string="Endpoints",
        help="Where messages should be sent.")
    event_ids = fields.One2many(
        comodel_name="hc.capability.statement.messaging.event",
        inverse_name="messaging_id",
        string="Events",
        required="True",
        help="Declare support for this event.")

class CapabilityStatementMessagingEndpoint(models.Model):
    _name = "hc.capability.statement.messaging.endpoint"
    _description = "Capability Statement Messaging Endpoint"

    messaging_id = fields.Many2one(
        comodel_name="hc.capability.statement.messaging",
        string="Messaging",
        help="If messaging is supported.")
    protocol = fields.Selection(
        string="Protocol",
        required="True",
        selection=[
            ("http", "HTTP"),
            ("ftp", "FTP"),
            ("mllp +", "MLLP +")],
        help="A list of the messaging transport protocol(s) identifiers, supported by this endpoint.")
    address = fields.Char(
        string="Address URI",
        required="True",
        help="Address of end-point.")

class CapabilityStatementMessagingEvent(models.Model):
    _name = "hc.capability.statement.messaging.event"
    _description = "Capability Statement Messaging Event"

    messaging_id = fields.Many2one(
        comodel_name="hc.capability.statement.messaging",
        string="Messaging",
        help="If messaging is supported.")
    code_id = fields.Many2one(
        comodel_name="hc.vs.message.event",
        string="Code",
        required="True",
        help="Event type.")
    category = fields.Selection(
        string="Category",
        selection=[
            ("consequence", "Consequence"),
            ("currency", "Currency"),
            ("notification", "Notification")],
        help="The impact of the content of the message.")
    mode = fields.Selection(
        string="Mode",
        required="True",
        selection=[
            ("sender", "Sender"),
            ("receiver", "Receiver")],
        help="The mode of this event declaration - whether application is sender or receiver.")
    focus_id = fields.Many2one(
        comodel_name="hc.vs.resource.type",
        string="Focus",
        required="True",
        help="Resource that's focus of message.")
    request_id = fields.Many2one(
        comodel_name="hc.res.structure.definition",
        string="Request",
        required="True",
        help="Profile that describes the request.")
    response_id = fields.Many2one(
        comodel_name="hc.res.structure.definition",
        string="Response",
        required="True",
        help="Profile that describes the response.")
    documentation = fields.Text(
        string="Documentation",
        help="Endpoint-specific event documentation.")

class CapabilityStatementDocument(models.Model):
    _name = "hc.capability.statement.document"
    _description = "Capability Statement Document"

    capability_statement_id = fields.Many2one(
        comodel_name="hc.res.capability.statement",
        string="Capability Statement",
        help="Capability Statement associated with this Capability Statement Document.")
    mode = fields.Selection(
        string="Mode",
        required="True",
        selection=[
            ("producer", "Producer"),
            ("consumer", "Consumer")],
        help="Mode of this document declaration - whether application is producer or consumer.")
    documentation = fields.Text(
        string="Documentation",
        help="Description of document support.")
    profile_id = fields.Many2one(
        comodel_name="hc.res.structure.definition",
        string="Profile",
        required="True",
        help="Constraint on a resource used in the document.")

class CapabilityStatementStatusHistory(models.Model):
    _name = "hc.capability.statement.status.history"
    _description = "Capability Statement Status History"

    capability_statement_id = fields.Many2one(
        comodel_name="hc.res.capability.statement",
        string="Capability Statement",
        help="Capability Statement associated with this Capability Statement Status History.")
    status = fields.Char(
        string="Status",
        help="The status of the capability statement.")
    start_date = fields.Datetime(
        string="Start Date",
        help="Start of the period during which this capability statement status is valid.")
    end_date = fields.Datetime(
        string="End Date",
        help="End of the period during which this capability statement status is valid.")
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

class CapabilityStatementContact(models.Model):
    _name = "hc.capability.statement.contact"
    _description = "Capability Statement Contact"
    _inherit = ["hc.basic.association"]
    _inherits = {"hc.contact.detail": "contact_id"}

    contact_id = fields.Many2one(
        comodel_name="hc.contact.detail",
        string="Contact",
        ondelete="restrict",
        required="True",
        help="Contact Detail associated with this Capability Statement Contact.")
    capability_statement_id = fields.Many2one(
        comodel_name="hc.res.capability.statement",
        string="Capability Statement",
        help="Capability Statement associated with this Capability Statement Contact.")

class CapabilityStatementUseContext(models.Model):
    _name = "hc.capability.statement.use.context"
    _description = "Capability Statement Use Context"
    _inherit = ["hc.basic.association", "hc.usage.context"]

    capability_statement_id = fields.Many2one(
        comodel_name="hc.res.capability.statement",
        string="Capability Statement",
        help="Capability Statement associated with this Capability Statement Use Context.")

class CapabilityStatementInstantiates(models.Model):
    _name = "hc.capability.statement.instantiates"
    _description = "Capability Statement Instantiates"
    _inherit = ["hc.basic.association"]

    capability_statement_id = fields.Many2one(
        comodel_name="hc.res.capability.statement",
        string="Capability Statement",
        help="Capability Statement associated with this Capability Statement Instantiates.")
    instantiates = fields.Char(
        string="Instantiates URI",
        help="Instantiates associated with this Capability Statement Instantiates.")

class CapabilityStatementFormat(models.Model):
    _name = "hc.capability.statement.format"
    _description = "Capability Statement Format"
    _inherit = ["hc.basic.association"]

    capability_statement_id = fields.Many2one(
        comodel_name="hc.res.capability.statement",
        string="Capability Statement",
        help="Capability Statement associated with this Capability Statement Format.")
    format = fields.Selection(
        string="Format",
        selection=[
            ("xml", "XML"),
            ("json", "JSON"),
            ("ttl", "TTL"),
            ("mime type", "MIME Type")],
        help="A list of the formats supported by this implementation using their content types.")

class CapabilityStatementImplementationGuide(models.Model):
    _name = "hc.capability.statement.implementation.guide"
    _description = "Capability Statement Implementation Guide"
    _inherit = ["hc.basic.association"]

    capability_statement_id = fields.Many2one(
        comodel_name="hc.res.capability.statement",
        string="Capability Statement",
        help="Capability Statement associated with this Capability Statement Implementation Guide.")
    implementation_guide = fields.Char(
        string="Implementation Guide URI",
        help="Implementation Guide associated with this Capability Statement Implementation Guide.")

class CapabilityStatementProfile(models.Model):
    _name = "hc.capability.statement.profile"
    _description = "Capability Statement Profile"
    _inherit = ["hc.basic.association"]

    capability_statement_id = fields.Many2one(
        comodel_name="hc.res.capability.statement",
        string="Capability Statement",
        help="Capability Statement associated with this Capability Statement Profile.")
    profile_id = fields.Many2one(
        comodel_name="hc.res.structure.definition",
        string="Profile",
        help="Structure Definition associated with this Capability Statement Profile.")

class CapabilityStatementRestCompartment(models.Model):
    _name = "hc.capability.statement.rest.compartment"
    _description = "Capability Statement REST Compartment"
    _inherit = ["hc.basic.association"]

    rest_id = fields.Many2one(
        comodel_name="hc.capability.statement.rest",
        string="REST",
        help="REST associated with this Capability Statement REST Compartment.")
    compartment = fields.Char(
        string="Compartment URI",
        help="Compartment associated with this Capability Statement Rest Compartment.")

class CapabilityStatementRestSecurityService(models.Model):
    _name = "hc.capability.statement.rest.security.service"
    _description = "Capability Statement REST Security Service"
    _inherit = ["hc.basic.association"]

    security_id = fields.Many2one(
        comodel_name="hc.capability.statement.rest.security",
        string="Security",
        help="Security associated with this Capability Statement REST Security Service.")
    service = fields.Selection(
        string="Service",
        selection=[
            ("oauth", "Oauth"),
            ("smart-on-fhir", "Smart On FHIR"),
            ("ntlm", "NTLM"),
            ("basic", "Basic"),
            ("kerberos", "Kerberos"),
            ("certificates", "Certificates")],
            help="Types of security services are supported/required by the system.")

class CapabilityStatementRestResourceReferencePolicy(models.Model):
    _name = "hc.capability.statement.rest.resource.reference.policy"
    _description = "Capability Statement REST Resource Reference Policy"
    _inherit = ["hc.basic.association"]

    resource_id = fields.Many2one(
        comodel_name="hc.capability.statement.rest.resource",
        string="Resource",
        help="Resource associated with this Capability Statement REST Resource Reference Policy.")
    reference_policy = fields.Selection(
        string="Reference Policy",
        selection=[
            ("literal", "Literal"),
            ("logical", "Logical"),
            ("resolves", "Resolves"),
            ("enforced", "Enforced"),
            ("local", "Local")],
        help="A set of flags that defines how references are supported.")

class CapabilityStatementRestResourceSearchInclude(models.Model):
    _name = "hc.capability.statement.rest.resource.search.include"
    _description = "Capability Statement REST Resource Search Include"
    _inherit = ["hc.basic.association"]

    resource_id = fields.Many2one(
        comodel_name="hc.capability.statement.rest.resource",
        string="Resource",
        help="Resource associated with this Capability Statement REST Resource Search Include.")
    search_include = fields.Char(
        string="Search Include",
        help="Search Include associated with this Capability Statement REST Resource Search Include.")

class CapabilityStatementRestResourceSearchRevInclude(models.Model):
    _name = "hc.capability.statement.rest.resource.search.rev.include"
    _description = "Capability Statement REST Resource Search Rev Include"
    _inherit = ["hc.basic.association"]

    resource_id = fields.Many2one(
        comodel_name="hc.capability.statement.rest.resource",
        string="Resource",
        help="Resource associated with this Capability Statement REST Resource Search Rev Include.")
    search_rev_include = fields.Char(
        string="Search Rev Include",
        help="Search Rev Include associated with this Capability Statement REST Resource Search Rev Include.")
