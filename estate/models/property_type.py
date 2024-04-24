# noinspection PyUnresolvedReferences
from odoo import models, fields
# noinspection PyUnresolvedReferences
from odoo.exceptions import ValidationError
from odoo.odoo import api


class PropertyType(models.Model):

    _name = 'estate.property.type'
    _description = 'EstatePropertyType'
    _order = 'name ASC'

    name = fields.Char(string='Title', required=True)
    property_ids = fields.One2many('estate.property', 'type_id', string='Properties')
    sequence = fields.Integer('Sequence', default=1, help="Used to order stages. Lower is better.")
    offer_ids = fields.One2many('estate.property.offer', 'type_id', string='Offers')
    offers_count = fields.Integer(compute='_compute_offers_count', string='Offer count')

    @api.depends('offer_ids')
    def _compute_offers_count(self):
        for record in self:
            record.offers_count = len(record.offer_ids)

    _sql_constraints = [
        ('unique_type', 'UNIQUE(name)', "Property type already exists.")
    ]
