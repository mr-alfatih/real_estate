# -*- coding: utf-8 -*-

{
    'name': "Real Estate | Property Management System",
    'version': '17.0.1.0',
    'sequence': 1,
    'summary': """
        Real estate system manages viewing, mapping, commissions, reporting, invoicing, payments.
    """,

    'description': """
        Real Estate Management System
    """,
    'author': 'Cybobits',
    'maintainer': 'Cybobits',
    'currency': 'USD',
    'website': 'https://www.cybobits.com/',
    'depends': ['base', 'mail', 'sale_management', 'website',
                'base_geolocalize', 'web', 'sale', 'board', 'project'],
    'data': [
        'security/user_groups.xml',
        'security/property_security.xml',
        'security/ir.model.access.csv',
        'data/ir_sequence_data.xml',
        # 'data/real_estate_management_data.xml',
        'views/documents_folder_views.xml',
        'views/property_property_views.xml',
        'views/property_facility_views.xml',
        'views/property_tag_views.xml',
        'views/property_commision_views.xml',
        'views/maintenance_equipment_views.xml',
        'views/maintenance_request_view.xml',
        'views/helpdesk_ticket_view.xml',
        'views/property_website.xml',
        'views/res_partner.xml',
        'views/product_template_view.xml',
        'views/crm_lead.xml',
    ],
    'assets': {
        'web.assets_frontend': [
        ],
        'web.assets_backend': [
        ],
    },
    'demo': [

    ],
    # 'images': ['static/description/banner.gif'],
    'installable': True,
    'application': True,
    'auto_install': False,
    'qweb': [

    ],
}
