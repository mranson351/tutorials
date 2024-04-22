from odoo import models
from odoo import fields


class PropertyOffer(models.Model):

    _name = 'estate.property.offer'
    _description = 'EstatePropertyOffer'

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
    partner_id = fields.Many2one('res.partner', string='Buyer', required=True)
    property_id = fields.Many2one('estate.property', string='Property', required=True)


