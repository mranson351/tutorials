from odoo import models
from odoo import fields


class TestModel(models.Model):

    _name = 'estate.property'
    _description = 'EstateProperty'

    name = fields.Char(string='Title', required=True)
    description = fields.Text(string='Description')
    postcode = fields.Char(string='Postcode')
    date_availability = fields.Date(
        string='Date Availability',
        copy=False,
        default=fields.Date.add(value=fields.Date.today(), months=3)
    )
    expected_price = fields.Float(string='Expected Price', required=True)
    selling_price = fields.Float(string='Selling Price', readonly=True, copy=False)
    bedrooms = fields.Integer(string='Bedrooms', default=2)
    living_area = fields.Integer(string='Living Area')
    facades = fields.Integer(string='Facades')
    garage = fields.Boolean(string='Garage')
    garden = fields.Boolean(string='Garden')
    garden_area = fields.Integer(string='Garden Area')
    garden_orientation = fields.Selection(
        string='Orientation',
        selection=[
            ('north', 'North'),
            ('south', 'South'),
            ('east', 'East'),
            ('west', 'West')
        ],
        help="Orientation corresponds to garden orientation"
    )
    active = fields.Boolean(string='Active', default=True)
    state = fields.Selection(
        string='State',
        selection=[
            ('new', 'New'),
            ('received', 'Offer received'),
            ('accepted', 'Offer accepted'),
            ('sold', 'Sold'),
            ('canceled', 'Canceled')
        ],
        help="Orientation corresponds to garden orientation",
        required=True,
        default='new'
    )

