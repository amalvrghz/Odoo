from odoo import fields, models, api
from datetime import datetime, date
from dateutil.relativedelta import relativedelta


class estate_model(models.Model):
    _name = "estate.model"
    # _rec_name = 'type'
    name = fields.Char(string='Title', required=True)
    _rec_name = 'name'
    description = fields.Text(string='Description')
    postcode = fields.Char(string='Postcode')
    # date_availability = fields.Datetime(string='Available from', copy=False, default=datetime.now())
    date_availability = fields.Datetime(string='Available from', copy=False,
                                        default=datetime.now() + relativedelta(months=3))
    expected_price = fields.Float(string='Expected price', required=True)
    selling_price = fields.Float(string='Selling price', readonly=True, copy=False)
    bedrooms = fields.Integer(string='Bedrooms', default=2)
    living_area = fields.Integer(string='Living area(sqm)')
    facades = fields.Integer(string='Facades')
    garage = fields.Boolean('Garage', default=False)
    active = fields.Boolean('Active', default=True)
    garden_area = fields.Integer(string='Garden area(sqm)')
    garden = fields.Boolean('Garden', default=False)
    garden_orientation = fields.Selection([('north', 'North'), ('south', 'South'), ('east', 'East'), ('west', 'West')],
                                          string='Garden orientation')
    status = fields.Selection(
        [('new', 'New'), ('offer_received', 'Offer received'), ('offer_accepted', 'Offer accepted'), ('sold', 'Sold'),
         ('cancelled', 'Cancelled')], string='Status', default='new', copy=False)
    property_types_id = fields.Many2one('property.type', string='Property Type')
    property_tags_id = fields.Many2many('property.tag')
    user_id = fields.Many2one('res.users', string='Salesperson', default=lambda self: self.env.user)
    buyer_id = fields.Many2one('res.partner', string='Buyer')
    # partners_id = fields.One2many('estate.model', 'partner_id', 'Partners')
    offers_ids = fields.One2many('property.offer', 'property_field_id', string="Offers List")
    best_offer = fields.Float(compute="_offer_onchange")
    @api.onchange("offers_ids")
    def _offer_onchange(self):
        amounts = []
        if len(self.offers_ids) > 0:
            for rec in self.offers_ids:
                amounts.append(rec.offer_amount)
                # if rec.offer_amount > 0:
                self.best_offer = max(amounts)
        else:
            self.best_offer = 0

    def button_send(self):
        for rec in self:
            rec.write({'status': 'offer_received'})

    def button_accept(self):
        for rec in self:
            rec.write({'status': 'offer_accepted'})

    def button_refuse(self):
        for rec in self:
            rec.write({'status': 'cancelled'})


class Property_Type(models.Model):
    _name = 'property.type'
    property_types = fields.Char()
    _rec_name = 'property_types'
    # user_id = fields.Many2one('res.users', string='Salesperson')
    # buyer_id = fields.Many2one('res.partner', string='Buyer')


class Property_Tag(models.Model):
    _name = 'property.tag'
    property_tags = fields.Char()
    _rec_name = 'property_tags'


class Property_Offer(models.Model):
    _name = 'property.offer'
    offer_amount = fields.Float()
    property_type_id = fields.Many2one('property.type')
    status = fields.Selection([('refused', 'Refused'), ('accepted', 'Accepted')])
    # _rec_name = 'offer_amount'
    # pro_name = fields.Many2one('estate.model', string='Property Name')
    partner_id = fields.Many2one('res.partner', string='Partners')
    validity = fields.Integer(string="Validity(Days)")
    deadline = fields.Date(string="Deadline", default=datetime.today())
    property_field_id = fields.Many2one('estate.model', string="Parent ID")
    @api.onchange("validity")
    def _onchange_validity(self):
        # print("hlo")
        # print(datetime.today()+relativedelta(days=self.validity))
        self.deadline = datetime.today()+relativedelta(days=self.validity)
    @api.onchange("deadline")
    def _onchange_deadline(self):
        # print("hi")
        start = date.today()
        end = self.deadline
        # print(end)
        # print(start)
        # print(end-start)
        self.validity = (end-start).days
