# noinspection PyUnresolvedReferences
from odoo import models, fields


class PropertyTag(models.Model):

    _name = 'estate.property.tag'
    _description = 'EstatePropertyTag'
    _order = 'name ASC'

    name = fields.Char(string='Title', required=True)
    color = fields.Integer(string='Color')

    _sql_constraints = [
        ('unique_tags', 'UNIQUE(name)', "Tag already exists.")
    ]

