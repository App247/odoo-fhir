# -*- coding: utf-8 -*-

from openerp import models, fields, api

# class hc_base_metadata_type(models.Model):
#     _name = 'hc_base_metadata_type.hc_base_metadata_type'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         self.value2 = float(self.value) / 100