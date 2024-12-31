# -*- coding: utf-8 -*-

from odoo import models, api, fields


class CrmLead(models.Model):
    _inherit = 'crm.lead'

    crm_order_line_ids = fields.One2many('crm.order.line', 'crm_order_id')

    def action_new_quotation(self):
        action = super(CrmLead, self).action_new_quotation()
        order_lines = []
        for line in self.crm_order_line_ids:
            if line.is_sale_rent == 'sale':
                order_lines.append((0, 0, {
                    'product_template_id': line.product_id.id,
                    'product_uom_qty': 1,
                    'product_uom': line.product_id.uom_id.id,
                    'price_unit': line.product_id.list_price,
                }))

        extended_context = {
            'default_order_line': order_lines,
        }
        action['context'].update(extended_context)
        return action


class CrmOrderLine(models.Model):
    _name = 'crm.order.line'
    _description = 'Crm Order Line'

    is_sale_rent = fields.Selection([('sale', 'Sale'), ('rent', 'Rent')], string='Type', default='sale')
    product_id = fields.Many2one('product.template', string='Product')
    crm_order_id = fields.Many2one('crm.lead', string='Order')