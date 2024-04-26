from odoo import models, fields, api
from odoo.exceptions import UserError, ValidationError


class EstateProperty(models.Model):

    _name = "estate.property"
    _description = "EstateProperty"
    _order = "id DESC"

    name = fields.Char(string="Title", required=True)
    description = fields.Text(string="Description")
    postcode = fields.Char(string="Postcode")
    date_availability = fields.Date(
        string="Date Availability",
        copy=False,
        default=fields.Date.add(value=fields.Date.today(), months=3),
    )
    expected_price = fields.Float(string="Expected Price", required=True)
    selling_price = fields.Float(string="Selling Price", readonly=True, copy=False)
    best_offer = fields.Float(string="Best Offer", readonly=True, compute="_compute_best_offer")
    bedrooms = fields.Integer(string="Bedrooms", default=2)
    living_area = fields.Integer(string="Living Area")
    facades = fields.Integer(string="Facades")
    garage = fields.Boolean(string="Garage")
    garden = fields.Boolean(string="Garden")
    garden_area = fields.Integer(string="Garden Area", default=False)
    total_area = fields.Integer(string="Total Area", readonly=True, compute="_compute_total_area")
    garden_orientation = fields.Selection(
        string="Orientation",
        selection=[
            ("north", "North"),
            ("south", "South"),
            ("east", "East"),
            ("west", "West"),
        ],
        help="Orientation corresponds to garden orientation",
    )
    active = fields.Boolean(string="Active", default=True)
    state = fields.Selection(
        string="State",
        selection=[
            ("new", "New"),
            ("received", "Offer received"),
            ("accepted", "Offer accepted"),
            ("sold", "Sold"),
            ("canceled", "Canceled"),
        ],
        help="Property's state",
        required=True,
        default="new",
    )
    type_id = fields.Many2one("estate.property.type", string="Type")
    salesperson_id = fields.Many2one("res.users", string="Sales Person", default=lambda self: self.env.user)
    buyer_id = fields.Many2one("res.partner", string="Buyer", copy=False)
    tag_ids = fields.Many2many("estate.property.tag", string="Tags")
    offer_ids = fields.One2many("estate.property.offer", "property_id", string="Offers")
    _sql_constraints = [
        (
            "check_expected_price",
            "CHECK(expected_price > 0)",
            "The expected price should be strictly positive",
        ),
        (
            "check_bedrooms_number",
            "CHECK(bedrooms >= 0)",
            "The number of bedrooms should be strictly positive",
        ),
        (
            "check_living_area",
            "CHECK(living_area >= 0)",
            "The living area should be strictly positive",
        ),
        (
            "check_facades",
            "CHECK(facades >= 0)",
            "The number of facades should be strictly positive",
        ),
        (
            "check_garden_area",
            "CHECK(garden_area >= 0)",
            "The garden area should be strictly positive",
        ),
    ]

    @api.ondelete(at_uninstall=False)
    def _unlink_if_state_is_not_new_or_canceled(self):
        for record in self:
            if record.state == "received":
                raise UserError("Can't delete a property with a received offer")
            elif record.state == "accepted":
                raise UserError("Can't delete a property with an accepted offer")
            elif record.state == "sold":
                raise UserError("Can't delete a sold property")

    @api.constrains("expected_price")
    def _check_expected_price(self):
        for record in self:
            if (
                bool(record.selling_price)
                & (record.selling_price != 0)
                & (record.selling_price < 0.9 * record.expected_price)
            ):
                raise ValidationError("Selling price shouldn't be below 90 % of expected price")

    @api.depends("living_area", "garden_area")
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    @api.depends("offer_ids")
    def _compute_best_offer(self):
        for record in self:
            best_offer = max(record.offer_ids.mapped("price"), default=0)
            record.best_offer = best_offer

    @api.onchange("garden")
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = "north"
        else:
            self.garden_area = 0
            self.garden_orientation = None

    def set_canceled(self):
        for record in self:
            if record.state != "sold":
                record.state = "canceled"
            else:
                raise UserError("You can't cancel a sold property!")
        return True

    def set_sold(self):
        for record in self:
            if record.state != "canceled":
                record.state = "sold"
            else:
                raise UserError("You can't sell a canceled property!")
        return True
