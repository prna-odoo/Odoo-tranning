from odoo import api,models,fields,_


class ResUser(models.Model):
    _inherit = "res.users"
    
    property_id = fields.One2many('estate.property', 'salse_person')
