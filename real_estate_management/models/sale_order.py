from odoo import models, fields, api

class CBTSaleOrder(models.Model):
    _inherit = 'sale.order'

    def action_confirm(self):
        print('override action confirm########')
        res = super(CBTSaleOrder, self).action_confirm()

        for order in self:
            for line in order.order_line:
                # property_ob = line.product_template_id
                property_obj = self.env['property.property'].search([('product_tmpl_id', '=', line.product_template_id.id)])
                print('property_obj', property_obj)

                if property_obj:
                    if order.is_rental_order:
                        property_obj.write({
                            'current_tenant': order.partner_id.id,
                            'rent': order.amount_untaxed,
                            'available_from': order.rental_start_date,
                            'handover_date': order.rental_return_date,
                            'state': 'rented',
                        })
                    else:
                        property_obj.write({
                            'sales_price': order.amount_untaxed,
                            'ownership': order.partner_id.id,
                            'state': 'sold',
                        })
                        line.product_id.write({
                            'list_price': order.amount_untaxed
                        })
        return res
