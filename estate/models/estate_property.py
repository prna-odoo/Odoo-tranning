from odoo import models,fields, _, api
from datetime import datetime, timedelta, date
from odoo.exceptions import UserError, ValidationError

#class Buyer_partner(models.Model):
#    _inherit='res.partner'
#
#    is_buyer=fields.Boolean(domain="[('is_buyer','=',['True'])]")

class estate_property_tag(models.Model):
    _name = "estate.property.tag"
    _description = "estate property tag"

    name = fields.Char(required = True)



class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "estate property"

    # _inherit = ['image.mixin','mail.thread','mail.activity.mixin',]

    def _get_description(self):
        if self.env.context.get('is_my_property'):
            return self.env.user.name + "'s Property"
 

    name = fields.Char(required=True)
    description = fields.Text(default=_get_description)
    postcode = fields.Char()
    image = fields.Binary('Course Image')
    date_availability = fields.Date(default = lambda self: fields.Datetime.now(), copy= False)
    expected_price = fields.Float()
    selling_price = fields.Float(copy= False, readonly = True)
    bedrooms = fields.Integer(default= 2)
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection([
        ("North", "North"),
        ("South", "South"),
        ("East", "East"),
        ("West", "West")
        ])
    active = fields.Boolean(default=True)
    image = fields.Image()
    property_type_id = fields.Many2one("estate.property.type")
    #buyer_id=fields.Char(required=True)
    buyer_id = fields.Many2one('res.partner')
    salse_person=fields.Many2one('res.users', string='SalesPerson', index=True, tracking=True, default=lambda self: self.env.user)
    tag_ids = fields.Many2many("estate.property.tag", string="Tags")
    offer_ids = fields.One2many("estate.property.offer", "property_id", string = "Offers")
    total_area = fields.Float(compute='_compute_total')
    best_price = fields.Float(compute = '_best_offer')
    #status = fields.Char()
    status = fields.Selection([("new", "New"),("Offer Received", "Offer Received"),("Offer Accepted", "Offer Accepted"),("sold","Sold"),("cancel", "Cancel")],default="new")



    @api.depends("living_area", "garden_area")
    def _compute_total(self):
        for record in self:
            record.total_area= record.living_area + record.garden_area
        
    @api.depends("offer_ids.price")
    def _best_offer(self):
        for record in self:
            if record.offer_ids:
                record.best_price = max(record.offer_ids.mapped('price'))
            else:
                record.best_price = False

            
            #         if record.offer_ids.price:
            
            #        maxval=0
            
            #         if(max is 0 or record.offer_ids.price > maxval)
            
            #            record.best_price = record.offer_ids.price 

             
    @api.onchange('garden')
    def _garden(self):
        for record in self:
            if record.garden:
                record.garden_area=100
                record.garden_orientation = 'North'
            else:
                record.garden_area=0
                record.garden_orientation = None

    @api.constrains('expected_price')
    def _check_price(self):
        for record in self:
            if record.expected_price < 1:
                raise ValidationError("Expected price must be positive number")


    def action_do_sold(self):
        for record in self:
            if record.status == "cancel":
                raise ValidationError("canceled property cannot be sold")
            record.status='sold'
            
    def action_do_cancel(self):
        for record in self:
            if record.status == "sold":
                raise ValidationError("Sold property cannot be cancel")
            record.status='cancel'

    def open_offers(self):
        view_id_all = self.env.ref('estate.estate_property_offer_tree').id
        return {
            "name":"Offers",
            "type":"ir.actions.act_window",
            "res_model":"estate.property.offer",
            "views":[[view_id_all, 'tree']],
            # "res_id": 2,
            "target":"new",
            "domain": [('property_id', '=', self.id)]
            }
        

    def open_confirm_offers(self):
        view_id_accept = self.env.ref('estate.estate_property_offer_tree').id
        return {
            "name":"Offers",
            "type":"ir.actions.act_window",
            "res_model":"estate.property.offer",
            "views":[[view_id_accept, 'tree']],
            # "res_id": 2,
            # "target":"new",
            "domain": [('property_id', '=', self.id),('status','=','accepted')]
            }




class  EstatePropertyType(models.Model):
    _name="estate.property.type"
    _description="Estate Property Type"

    name = fields.Char()
    property_ids = fields.One2many("estate.property","property_type_id", string="Property Type")



#class Buyer(models.Model):
#    _name="buyers"
#    _description="Proprty buyer" 
#
#    name=fields.Char(required=True)
#
#class SalesPerson(models.Model):
#    _name="sales.person"
#    _description="Sales Person"
#
#    name = fields.Char(default = "Agent", readonly = True)
#    

class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Estate Poperty Offer"

    price = fields.Float(required = True )
    #status = fields.Selection([("none", "None"),
     #   ("Accept", "Accept"),
      #  ("Refuse", "Refuse")])
    status= fields.Selection([('accepted','Accepted'),('refused','Refused')])
    partner_id = fields.Many2one('res.partner')
    property_id = fields.Many2one('estate.property')
    validity = fields.Integer(default=7)
    date_deadline = fields.Date(compute = '_compute_deadline', inverse = '_inverse_date')


    @api.depends('validity')
    def _compute_deadline(self):
        # print('\n\n\n???????', type(self.create_date), self.create_date)
        # self.date_deadline = False
        for record in self:
            if record.validity and record.create_date:
                record.date_deadline = record.create_date + timedelta(days = record.validity)
            else:
                record.date_deadline = False
 
    @api.depends('date_deadline')
    def _inverse_date(self):
        for record in self:
            if record.date_deadline:
                record.validity = int((record.date_deadline - (record.create_date).date()).days) 


    def action_Accept(self):
        for record in self:
            if record.status=="refused":
                raise ValidationError("Refused offer cannot be Accepted")
            record.status="accepted"

    def action_Refuse(self):
        for record in self:
            if record.status=="accepted":
                raise ValidationError("Acceptted offer cannot be Refused")
            record.status="refused"



