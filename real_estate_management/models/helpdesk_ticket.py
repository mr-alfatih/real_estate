# -*- coding: utf-8 -*-

from odoo import models, fields

class HelpdeskTicket(models.Model):
    _inherit = 'helpdesk.ticket'

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

    # define a function "plan" that will create a new record in 'maintenance.request' and pass the proprty_id to proprty_id field and equipment_id to equipment_id and ticket name to the name
    def maintenance_request(self):
        maintenance_request = self.env['maintenance.request'].create({
            'property_id': self.property_id.id,
            'equipment_id': self.equipment_id.id or False,
            'name': self.name,
            'priority': self.priority,
            'user_id': self.user_id.id,
            'description': self.description
        })
        return {
            'type': 'ir.actions.act_window',
            'name': 'Maintenance Request',
            'res_model': 'maintenance.request',
            'view_mode': 'form',
            'res_id': maintenance_request.id
        }
        # return maintenance_request
