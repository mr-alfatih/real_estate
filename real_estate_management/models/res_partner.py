# -*- coding: utf-8 -*-

from odoo import models, fields

class ResPartner(models.Model):
    _inherit = 'res.partner'

    is_owner = fields.Boolean(string="Is Owner", default=False)
    is_tenant = fields.Boolean(string="Is Tenant", default=False)
    is_property_manager = fields.Boolean(string="Is Property Manager", default=False)
