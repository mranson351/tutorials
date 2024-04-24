# noinspection PyUnresolvedReferences
from odoo import models, fields
# noinspection PyUnresolvedReferences
from odoo.exceptions import UserError
from odoo.odoo import api


class PropertyOffer(models.Model):

    _name = 'estate.property.offer'
    _description = 'EstatePropertyOffer'
    _order = 'price DESC'

    price = fields.Float(string='Title', required=True)
    status = fields.Selection(
        string='Orientation',
        selection=[
            ('accepted', 'Accepted'),
            ('refused', 'Refused'),
        ],
        copy=False,
        help="Orientation corresponds to garden orientation"
    )
    validity = fields.Integer(string='Validity', default=7)
    date_deadline = fields.Date(string='Deadline', compute='_compute_date_deadline', inverse='_inverse_date_deadline')
    partner_id = fields.Many2one('res.partner', string='Buyer', required=True)
    property_id = fields.Many2one('estate.property', string='Property', required=True)
    type_id = fields.Many2one(related="property_id.type_id", string='Property Type', readonly=True)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            self.env['estate.property'].browse(vals['property_id']).state = 'received'
            if vals['price'] < 0.9 * self.env['estate.property'].browse(vals['property_id']).expected_price:
                raise UserError("You are expected to make an offer greater than 90% of the expected price")
            for offer_id in self.env['estate.property'].browse(vals['property_id']).offer_ids:
                if offer_id.price >= vals['price']:
                    raise UserError("You are expected to make a higher offer than those already entered")
            return super(PropertyOffer, self).create(vals)

    @api.depends('create_date', 'validity')
    def _compute_date_deadline(self):
        for record in self:
            try:
                record.date_deadline = fields.Date.add(value=record.create_date, days=record.validity)
            except:
                record.date_deadline = fields.Date.add(value=fields.Date.today(), days=record.validity)

    def _inverse_date_deadline(self):
        for record in self:
            try:
                record.validity = abs((record.date_deadline - record.create_date).days)
            except:
                record.validity = abs((record.date_deadline - fields.Date.today()).days)

    def set_status_offer_accepted(self):
        for record in self:
            record.status = 'accepted'
            record.property_id.selling_price = record.price
            record.property_id.state = 'accepted'
            record.property_id.buyer_id = record.partner_id
        return True

    def set_status_offer_refused(self):
        for record in self:
            record.status = 'refused'
        return True

    def set_status_offer_canceled(self):
        for record in self:
            record.status = None
            record.property_id.selling_price = None
            record.property_id.buyer_id = None
            record.property_id.state = 'received'
        return True
