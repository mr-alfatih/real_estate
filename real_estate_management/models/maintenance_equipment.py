# -*- coding: utf-8 -*-

from odoo import models, fields

class MaintenanceEquipment(models.Model):
    _inherit = 'maintenance.equipment'

    property_id = fields.Many2one('property.property', string="Property")
    # property_building = fields.Char(related='property_id.property_type', string="Building", readonly=True)
    property_reference = fields.Char(related='property_id.code', string="Reference", readonly=True)
    property_location = fields.Char(related='property_id.location', string="Location", readonly=True)
    # property_floor = fields.Char(related='property_id.total_floor', string="Floor", readonly=True)
    # property_project = fields.Char(related='property_id.project', string="Project", readonly=True)



class MaintenanceRequest(models.Model):
    _inherit = 'maintenance.request'

    property_id = fields.Many2one('property.property', string="Property")
    property_reference = fields.Char(related='property_id.code', string="Reference", readonly=True)
    property_location = fields.Char(related='property_id.location', string="Location", readonly=True)
    equipment_id = fields.Many2one(
        'maintenance.equipment',
        string='Equipment',
        ondelete='restrict',
        index=True,
        check_company=True,
        domain="[('property_id', '=', property_id)]"
    )