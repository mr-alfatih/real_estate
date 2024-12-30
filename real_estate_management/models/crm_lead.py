# -*- coding: utf-8 -*-

from odoo import models, api

class CrmLead(models.Model):
    _inherit = 'crm.lead'

    def action_new_quotation(self):
        action = super(CrmLead, self).action_new_quotation()
        # order_lines = []
        # for line in self.crm_order_line:
        #     if line.is_sale_rent == 'sale':
        #         order_lines.append((0, 0, {
        #             'product_id': line.product_id.id,
        #             'product_uom_qty': 1,
        #             'price_unit': line.product_id.list_price,
        #         }))
        #
        # extended_context = {
        #     'default_order_line': order_lines,
        # }
        # action['context'].update(extended_context)
        print('action----->', action)
        return action
