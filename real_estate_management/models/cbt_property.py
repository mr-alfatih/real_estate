# -*- coding: utf-8 -*-

from odoo import api, fields, models, _


class Property(models.Model):
    """A class for the model property to represent the property"""

    _name = "property.property"
    _description = "Property"
    # _inherits = {'product.template': 'product_tmpl_id'}
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _parent_name = 'parent_id'  # Enables hierarchy
    _parent_store = True  # Adds parent_path for efficient querying

    name = fields.Char(
        string="Name", required=True, copy=False, help="Name of the Property"
    )
    code = fields.Char(
        string="Reference",
        readonly=True,
        copy=False,
        default=lambda self: _("New"),
        help="Sequence/code for the property",
    )
    product_tmpl_id = fields.Many2one(
        'product.template', 'Product Template',
        auto_join=True, index=True, ondelete="cascade", required=True)
    property_type = fields.Selection(
        [
            ("land", "Land"),
            ("residential", "Residential"),
            ("commercial", "Commercial"),
            ("industry", "Industry"),
            ('apartment', 'Apartments'),
            ('villa', 'Villas'),
            ('office', 'Offices'),
            ('other', 'Other'),
        ],
        string="Type",
        required=True,
        help="The type of the property",
    )
    state = fields.Selection(
        [
            ("draft", "Draft"),
            ("available", "Available"),
            ("rented", "Rented"),
            ("sold", "Sold"),
        ],
        required=True,
        string="Status",
        default="draft",
        help="* The 'Draft' status is used when the property is in draft.\n"
             "* The 'Available' status is used when the property is "
             "available or confirmed\n"
             "* The 'Rented' status is used when the property is rented.\n"
             "* The 'sold' status is used when the property is sold.\n",
    )
    parent_id = fields.Many2one(
        'property.property', string='Parent Property',
        ondelete='restrict', index=True, help="Parent property if applicable."
    )
    child_ids = fields.One2many(
        'property.property', 'parent_id', string='Sub-properties',
        help="Sub-properties associated with this property."
    )
    parent_path = fields.Char(index=True)  # Automatically managed for hierarchy
    is_parent = fields.Boolean(
        string="Is Parent",
        compute="_compute_is_parent",
        store=True,
        help="Indicates whether the property is a parent record."
    )
    is_prop = fields.Boolean(
        string="Is Property?",
        default=False,
        help="Indicates whether the property is a property or level"
    )
    street = fields.Char(string="Street", required=True, help="The street name")
    street2 = fields.Char(string="Street2", help="The street2 name")
    zip = fields.Char(string="Zip", change_default=True, help="Zip code for the place")
    city = fields.Char(string="City", help="The name of the city")
    country_id = fields.Many2one(
        "res.country",
        string="Country",
        ondelete="restrict",
        required=True,
        help="The name of the country",
    )
    state_id = fields.Many2one(
        "res.country.state",
        string="State",
        ondelete="restrict",
        tracking=True,
        domain="[('country_id', '=?', country_id)]",
        help="The name of the state",
    )
    latitude = fields.Float(
        string="Latitude",
        digits=(16, 5),
        help="The latitude of where the property is " "situated",
    )
    longitude = fields.Float(
        string="Longitude",
        digits=(16, 5),
        help="The longitude of where the property is " "situated",
    )

    project = fields.Many2one(
        'project.project', string="Project",
        help="Associated project for the property"
    )
    location = fields.Char(string="Location", help="The location of the property")

    # garden_area = fields.Float(string="Garden Area (Sqft)")
    property_manager = fields.Many2one('res.partner', string="Property Manager")
    ownership = fields.Many2one('res.partner', string="Ownership")
    current_tenant = fields.Many2one('res.partner', string="Current Tenant")
    listed_by = fields.Char(string="Listed By")

    available_from = fields.Date(string="Available From")
    developer = fields.Many2one('res.partner', string="Developer")
    plot_area = fields.Float(string="Plot Area (Sqm)")
    built_up_area = fields.Float(string="Built-up Area (Sqm)")
    completion_status = fields.Selection(
        [
            ('not_started', 'Not Started'),
            ('in_progress', 'In Progress'),
            ('completed', 'Completed')
        ],
        string="Completion Status"
    )

    company_id = fields.Many2one(
        "res.company",
        string="Property Management Company",
        default=lambda self: self.env.company,
    )
    currency_id = fields.Many2one(
        "res.currency", string="Currency", related="company_id.currency_id"
    )
    image = fields.Binary(string="Image", help="Image of the property")
    construct_year = fields.Char(
        string="Construct Year", size=4, help="Year of construction of the property"
    )
    license_no = fields.Char(
        string="License No.", help="License number of the property"
    )
    description = fields.Text(
        string="Description", help="A brief description about the property"
    )
    responsible_id = fields.Many2one(
        "res.users",
        string="Responsible Person",
        help="The responsible person for " "this property",
        default=lambda self: self.env.user,
    )
    # Residence details
    building_name = fields.Char(string="Building Name")
    building_age = fields.Integer(string="Building Age (Years)")
    swimming_pool = fields.Integer(string="Swimming Pool")
    passenger_elevators = fields.Integer(string="Passenger Elevators")
    freight_elevators = fields.Integer(string="Freight Elevators")
    garage = fields.Integer(string="Garage")
    type_residence = fields.Char(
        string="Type of Residence", help="The type of the residence"
    )
    total_floor = fields.Integer(
        string="Total Floor",
        default=1,
        help="The total number of floor in " "the property",
    )
    furnishing = fields.Selection(
        [
            ("no_furnished", "Not Furnished"),
            ("half_furnished", "Partially Furnished"),
            ("furnished", "Fully Furnished"),
        ],
        string="Furnishing",
    )
    bedroom = fields.Integer(
        string="Bedrooms", help="Number of bedrooms in the property"
    )
    bathroom = fields.Integer(
        string="Bathrooms", help="Number of bathrooms in the property"
    )
    balconies = fields.Integer(string="Balconies")
    parking = fields.Integer(
        string="Parking",
        help="Number of cars or bikes that can be parked " "in the property",
    )
    # Land details
    land_name = fields.Char(string="Land Name", help="The name of the land")
    land_area = fields.Char(
        string="Area In Hector", help="The area of the land in hector"
    )
    # commercial details
    shop_name = fields.Char(string="Shop Name", help="The name of the shop")
    # industry details
    industry_name = fields.Char(string="Industry Name", help="The name of the industry")

    usage = fields.Char(
        string="Used For", help="For what purpose is this property used for"
    )

    property_image_ids = fields.One2many(
        "property.image", "property_id", string="Property Images"
    )
    area_measurement_ids = fields.One2many(
        "property.area.measure", "property_id", string="Area Measurement"
    )
    total_sq_feet = fields.Float(
        string="Total Square Feet",
        compute="_compute_total_sq_feet",
        help="The total area square feet of the " "property",
    )

    # Extra fields
    handover_date = fields.Date(string="Handover Date")
    video_url = fields.Char(string="Video URL")
    purchase_price = fields.Monetary(
        string="Purchase Price", currency_field='currency_id'
    )
    sales_price = fields.Monetary(
        string="Sales Price", currency_field='currency_id'
    )
    rent_period = fields.Selection(
        [
            ('monthly', 'Monthly'),
            ('yearly', 'Yearly'),
        ],
        string="Rent Period",
        help="Rent payment frequency",
    )
    rent = fields.Monetary(string="Rent", currency_field='currency_id')
    is_installment_payment = fields.Boolean(
        string="Installment Payment", help="Payments are made in installment"
    )
    payment_terms = fields.Many2one('account.payment.term', string="Payment Terms")

    contact_name = fields.Char(string="Contact Name")
    email = fields.Char(string="Email")
    landline_no = fields.Char(string="Landline No")
    # view = fields.Many2one('property.view', string="View")
    amenities = fields.Many2many('property.tag', string="Amenities")

    facility_ids = fields.Many2many(
        "property.facility", string="Facilities", help="Facilities of the property"
    )
    nearby_connectivity_ids = fields.One2many(
        "property.nearby.connectivity", "property_id", string="Nearby Connectives"
    )

    attachment_id = fields.Many2one("ir.attachment", string="Attachment")
    equipment_ids = fields.One2many('maintenance.equipment', 'property_id', string="Maintenance Equipment")
    maintenance_equipment_count = fields.Integer(compute='_compute_maintenance_equipment_count',
                                                 string="Maintenance Equipment Count")
    maintenance_ids = fields.One2many('maintenance.request', 'property_id', string="Maintenance Requests")
    maintenance_request_count = fields.Integer(compute='_compute_maintenance_request_count',
                                               string="Maintenance Request Count")

    @api.depends('parent_id')
    @api.depends_context('hierarchical_naming')
    def _compute_display_name(self):
        hierarchical_naming = self.env.context.get('hierarchical_naming', True)
        for record in self:
            if hierarchical_naming and record.parent_id:
                record.display_name = f"{record.parent_id.sudo().name} / {record.name}"
            else:
                record.display_name = record.name

    @api.depends("child_ids")
    def _compute_is_parent(self):
        for record in self:
            record.is_parent = bool(record.child_ids)



    def _compute_maintenance_equipment_count(self):
        for rec in self:
            rec.maintenance_equipment_count = len(rec.equipment_ids)

    @api.depends('maintenance_ids')
    def _compute_maintenance_request_count(self):
        for rec in self:
            rec.maintenance_request_count = len(rec.maintenance_ids)

    @api.model
    def create(self, vals):
        print('is_prop------', vals.get('is_prop'))
        print('is_prop', vals.get('is_prop', False))
        """Generating sequence number at the time of creation of record"""
        if vals.get("code", "New") == "New":
            vals["code"] = (
                    self.env["ir.sequence"].next_by_code("property.property") or "New"
            )
            # check if is_prop is true the below code will be executed otherwise not
            if vals.get('is_prop', False):
                # Extract values for floor and bedroom from vals
                furnishing_value = vals.get('furnishing', 'no_furnished')
                amenities_values = vals.get('amenities', [])
                floor_value = vals.get('total_floor', 0)
                bedroom_value = vals.get('bedroom', 0)
                bathroom_value = vals.get('bathroom', 0)
                balconies_value = vals.get('balconies', 0)
                parking_value = vals.get('parking', 0)
                passenger_elevator = vals.get('passenger_elevator', 0)
                freight_elevator = vals.get('freight_elevator', 0)
                swimming_pool = vals.get('swimming_pool', 0)
                garage = vals.get('garage', 0)



                # Prepare the attributes and their values dynamically
                attribute_line_ids = []

                # List of attributes to handle
                attributes = [
                    {'name': 'furnishing_value', 'value': furnishing_value},
                    {'name': 'Floor', 'value': floor_value},
                    {'name': 'Bedroom', 'value': bedroom_value},
                    {'name': 'bathroom_value', 'value': bathroom_value},
                    {'name': 'balconies_value', 'value': balconies_value},
                    {'name': 'parking_value', 'value': parking_value},
                    {'name': 'passenger_elevator', 'value': passenger_elevator},
                    {'name': 'freight_elevator', 'value': freight_elevator},
                    {'name': 'swimming_pool', 'value': swimming_pool},
                    {'name': 'garage', 'value': garage},
                ]

                for attr in attributes:
                    # Search for the attribute, create if not found
                    attribute = self.env['product.attribute'].search([('name', '=', attr['name'])], limit=1)
                    if not attribute:
                        attribute = self.env['product.attribute'].create({'name': attr['name']})

                    # Search for the value, create if not found
                    value = self.env['product.attribute.value'].search([
                        ('name', '=', str(attr['value'])),  # Use the value as the name
                        ('attribute_id', '=', attribute.id)
                    ], limit=1)
                    if not value:
                        value = self.env['product.attribute.value'].create({
                            'name': str(attr['value']),  # Ensure the value is string
                            'display_type': 'multi',
                            'attribute_id': attribute.id
                        })

                    # Add to attribute_line_ids
                    attribute_line_ids.append((0, 0, {
                        'attribute_id': attribute.id,
                        'value_ids': [(6, 0, [value.id])]
                    }))

                # # Add Amenities as an attribute
                # amenities_attribute = self.env['product.attribute'].search([('name', '=', 'Amenities')], limit=1)
                # if not amenities_attribute:
                #     amenities_attribute = self.env['product.attribute'].create({'name': 'Amenities'})
                #
                # amenities = vals.get('amenities', [])
                # print('amenities----->', amenities)
                # amenity_values = []
                # for amenity in amenities:
                #     print('amenity----->', amenity)
                #     amenity_value = self.env['product.attribute.value'].search([
                #         ('name', '=', amenity.name),
                #         ('attribute_id', '=', amenities_attribute.id)
                #     ], limit=1)
                #     if not amenity_value:
                #         amenity_value = self.env['product.attribute.value'].create({
                #             'name': amenity.name,
                #             'attribute_id': amenities_attribute.id
                #         })
                #     amenity_values.append(amenity_value.id)
                # attribute_line_ids.append((0, 0, {
                #     'attribute_id': amenities_attribute.id,
                #     'value_ids': [(6, 0, amenity_values)]
                # }))

                # Add Amenities as an attribute
                amenities_attribute = self.env['product.attribute'].search([('name', '=', 'Amenities')], limit=1)
                if not amenities_attribute:
                    amenities_attribute = self.env['product.attribute'].create({'name': 'Amenities'})

                # Loop through amenities Many2many values (the `amenities` field in the form)
                amenities = vals.get('amenities', [])
                amenity_values = []

                for amenity_id in amenities:
                    # Get the corresponding property.tag record using the amenity_id
                    property_tags = self.env['property.tag'].browse(amenity_id)

                    # Ensure we're iterating through each property_tag individually
                    for property_tag in property_tags:
                        # Check if a value for this attribute already exists with the same name
                        amenity_value = self.env['product.attribute.value'].search([
                            ('name', '=', property_tag.tag),
                            ('attribute_id', '=', amenities_attribute.id)
                        ], limit=1)

                        # If it does not exist, create it
                        if not amenity_value:
                            amenity_value = self.env['product.attribute.value'].create({
                                'name': property_tag.tag,
                                'display_type': 'multi',
                                'attribute_id': amenities_attribute.id
                            })

                        # Append the ID of the amenity value (for use in the relation)
                        amenity_values.append(amenity_value.id)

                # Add attribute line with the amenity values
                attribute_line_ids.append((0, 0, {
                    'attribute_id': amenities_attribute.id,
                    'value_ids': [(6, 0, amenity_values)]  # Linking by IDs
                }))

                # Build product values
                product_vals = {
                    'name': vals.get('name', 'Unnamed Property'),
                    'type': 'product',
                    'rent_ok': True,
                    'list_price': vals.get('sales_price', 0),
                    'standard_price': vals.get('purchase_price', 0),
                    'default_code': vals.get('code', 'New'),
                    'attribute_line_ids': attribute_line_ids,
                }
                product = self.env['product.template'].create(product_vals)

                # Link the product.template to the property
                vals['product_tmpl_id'] = product.id
            # else:
            #     product = self.env['product.template'].create({'name': vals.get('name', 'Unnamed Property')})
            #     # Link the product.template to the property
            #     vals['product_tmpl_id'] = product.id
        res = super(Property, self).create(vals)
        return res

    def _compute_total_sq_feet(self):
        """Calculates the total square feet of the property"""
        for rec in self:
            rec.total_sq_feet = sum(rec.mapped("area_measurement_ids").mapped("area"))

    @api.model
    def _geo_localize(self, street="", zip="", city="", state="", country=""):
        """Generate Latitude and Longitude based on address"""
        geo_obj = self.env["base.geocoder"]
        search = geo_obj.geo_query_address(
            street=street, zip=zip, city=city, state=state, country=country
        )
        result = geo_obj.geo_find(search, force_country=country)
        if result is None:
            search = geo_obj.geo_query_address(city=city, state=state, country=country)
            result = geo_obj.geo_find(search, force_country=country)
        return result

    @api.onchange("street", "zip", "city", "state_id", "country_id")
    def _onchange_address(self):
        """Writing Latitude and Longitude to the record"""
        for rec in self.with_context(lang="en_US"):
            result = rec._geo_localize(
                rec.street, rec.zip, rec.city, rec.state_id.name, rec.country_id.name
            )
            if result:
                rec.write(
                    {
                        "latitude": result[0],
                        "longitude": result[1],
                    }
                )

    def action_get_map(self):
        """Redirects to google map to show location based on latitude
        and longitude"""
        return {
            "type": "ir.actions.act_url",
            "name": "View Map",
            "target": "self",
            # "url": "/map/%s/%s" % (self.latitude, self.longitude),
            "url": "/map/%s/%s?search=%s" % (self.latitude, self.longitude, self.street),
        }

    def action_available(self):
        """Set the state to available"""
        self.state = "available"

    def action_property_maintenance_request(self):
        action = self.env.ref('maintenance.hr_equipment_request_action').read()[0]
        action['domain'] = [('property_id', '=', self.id)]
        action['context'] = {'default_property_id': self.id}
        return action

    def action_property_maintenance_equipment(self):
        action = self.env.ref('maintenance.hr_equipment_action').read()[0]
        action['domain'] = [('property_id', '=', self.id)]
        action['context'] = {'default_property_id': self.id}
        return action


    def action_property_product(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Product Form',
            'res_model': 'product.template',
            'view_mode': 'form',
            'res_id': self.product_tmpl_id.id,
            'target': 'current',
        }


    # define function will return the product form view


    def action_property_tenant(self):
        action = self.env.ref('sale_renting.rental_order_action').read()[0]
        action['domain'] = [('order_line.product_template_id', '=', self.product_tmpl_id.id)]
        action['view_mode'] = 'kanban, form'
        return action
        # return {
        #     'type': 'ir.actions.act_window',
        #     'name': 'Rented Orders',
        #     'res_model': 'sale.order',
        #     'view_mode': 'kanban',
        #     'domain': [('order_line.product_template_id', '=', self.product_tmpl_id.id)],
        # }


    # @api.depends('unit_price', 'no_of_months', 'no_of_years')
    # def _compute_installments(self):
    #     for record in self:
    #         if record.no_of_months or record.no_of_years:
    #             record.no_of_installments = record.no_of_months or record.no_of_years
    #             if record.unit_price:
    #                 record.amount_per_installment = record.unit_price / record.no_of_installments
    #         else:
    #             record.no_of_installments = 0
    #             record.amount_per_installment = 0.00
