# -*- coding: utf-8 -*-
import werkzeug.utils
from odoo import fields, http
from odoo.http import request


class PropertyController(http.Controller):

    @http.route('/property_webform', type="http", auth="user", website=True)
    def property_webform(self, **kw):
        partner = request.env.user.partner_id
        # properties = request.env['property.property'].sudo().search([])
        # if partner.is_owner and partner.is_tenant:
        #     properties = request.env['property.property'].sudo().search([
        #         '|',
        #         ('ownership', '=', partner.id),
        #         ('current_tenant', '=', partner.id)
        #     ])
        # else:
        #     properties = request.env['property.property']
        properties = request.env['property.property'].sudo().search([
            '|',
            '|',
            ('ownership', '=', partner.id),
            ('current_tenant', '=', partner.id),
            ('property_manager', '=', partner.id)
        ])
        return http.request.render('real_estate_management.create_property_ticket', {'partner': partner, 'properties': properties})
        # return http.request.render('real_estate_management.create_property_ticket', {'name': 'Property Ticket', 'partner': partner, 'properties': properties})

    @http.route('/map/<latitude>/<longitude>', type='http', auth='user')
    def redirect_map(self, latitude, longitude):
        """ Returns the Google map location for the corresponding latitude
        and longitude """
        return werkzeug.utils.redirect(
            "https://www.google.com/maps/@%s,%s,115m/data=!3m1!1e3" % (
                latitude, longitude))

    @http.route('/create/property_ticket', type="http", auth="public", website=True)
    def create_property_ticket(self, **kw):
        print('kw----->', kw)
        partner = request.env['res.partner'].sudo().browse(int(kw.get('partner_id')))
        property = request.env['property.property'].sudo().browse(int(kw.get('property_id')))

        ticket = {
            'name': kw.get('name'),
            'partner_id': partner.id,
            'property_id': property.id,
            'description': kw.get('property_complaint_description'),
        }
        print('ticket----->', ticket)
        request.env['helpdesk.ticket'].sudo().create(ticket)
        # request.env['helpdesk.ticket'].sudo().create(kw)
        return request.render('real_estate_management.property_thanks', {})
