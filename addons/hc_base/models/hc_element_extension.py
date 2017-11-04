# -*- coding: utf-8 -*-

from openerp import models, fields, api

class ExtensionElementExtension(models.Model):
    _inherit = ["hc.extension"]

class CodingElementExtension(models.Model):
    _inherit = ["hc.extension"]

class CodeableConceptElementExtension(models.Model):
    _inherit = ["hc.extension"]

class ElementExtension(models.Model):
    _inherit = ["hc.extension"]

class PeriodElementExtension(models.Model):
    _inherit = ["hc.extension"]

class ContactPointElementExtension(models.Model):
    _inherit = ["hc.extension"]
