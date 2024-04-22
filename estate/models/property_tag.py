from odoo import models
from odoo import fields


class PropertyTag(models.Model):

    _name = 'estate.property.tag'
    _description = 'EstatePropertyTag'

    name = fields.Char(string='Title', required=True)

