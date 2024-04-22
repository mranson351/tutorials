from odoo import models
from odoo import fields


class PropertyType(models.Model):

    _name = 'estate.property.type'
    _description = 'EstatePropertyType'

    name = fields.Char(string='Title', required=True)

