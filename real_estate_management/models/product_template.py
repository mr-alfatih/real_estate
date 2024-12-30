# -*- coding: utf-8 -*-

from odoo import api, fields, models, _

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    cbt_property_id = fields.Many2one(
        'property.property', string='Property Details', ondelete='cascade', required=True)
    # Delegation inheritance
    _inherits = {'property.property': 'cbt_property_id'}