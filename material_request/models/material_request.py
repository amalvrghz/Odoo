from odoo import models, fields
from datetime import datetime
from odoo.exceptions import ValidationError


class MaterialRequest(models.Model):
    _name = 'material.request'
    _rec_name = 'sequence'
    _description = ''
    sequence = fields.Char(string="Sequence", default='New')
    employee_id = fields.Many2one(comodel_name='res.users', string="Employee", default=lambda self: self.env.user)
    request_line_ids = fields.One2many('material.request.lines', 'material_request_id', string="Request Lines")
    state = fields.Selection([('draft', 'Draft'), ('to_approve', 'To Approve'), ('first_approval', 'First Approval'),
                              ('approved', 'Approved'), ('rejected', 'Rejected')], default='draft')

    def button_request(self):
        temp = 0
        for rec in self.request_line_ids:
            if rec.request_type and rec.product_id:
                temp = 1
            else:
                raise ValidationError('Some Mandatory Fields Are Empty')

        if temp == 1:
            self.write({
                'state': 'to_approve'
            })
            self.sequence = self.env['ir.sequence'].next_by_code('material.request')

        #     ------------------------------------------------------------------

    def button_confirm(self):
        print('confirm')
        self.write({
            'state': 'first_approval'
        })

    def button_approve(self):

        temp = 0
        for rec in self.request_line_ids:
            if rec.request_type == 'purchase_order':
                prices = rec.product_id.seller_ids.mapped('price')
                print('minimum price:', min(prices))
                for recc in rec.product_id.seller_ids:
                    if min(prices) == recc.price:
                        self.env['purchase.order'].create({
                            'partner_id': recc.name.id,
                            'order_line': [
                                (0, 0, {
                                    'name': rec.product_id.name,
                                    'product_id': rec.product_id.id,
                                    'product_qty': 1.0,
                                    'product_uom': 1,
                                    'price_unit': recc.price,
                                    'date_planned': datetime.today(),
                                    'taxes_id': False,
                                })]

                        })
                temp = 1
            else:
                print('internal transfer, print rec:', rec)
                a = self.env['stock.picking'].create({
                    'location_id': rec.from_location.id,
                    'location_dest_id': rec.to_location.id,
                    'picking_type_id': 5,
                    'immediate_transfer': True,
                    #  made state of internal transfer ready
                    'state': 'done',
                    'move_ids_without_package': [(0, 0, {
                        'name': rec.product_id.name,
                        'product_id': rec.product_id.id,
                        'product_uom': 1,
                        'location_id': rec.from_location.id,
                        'location_dest_id': rec.to_location.id,
                        'quantity_done': 1,
                        'state': 'done'
                    })],
                })
                # a = self.env['stock.picking'].create({
                #     'picking_type_id': 5,
                #     'location_id': 8,
                #     'location_dest_id': 8,
                #     'state': 'done',
                #     'move_lines': [(0, 0, {
                #         'name': rec.product_id.name,
                #         'product_id': rec.product_id.id,
                #         'product_uom': 1,
                #         'product_uom_qty': 1,
                #         'location_id': rec.from_location.id,
                #         'location_dest_id': rec.to_location.id,
                #     })],
                # })
                print('created record:', a)
                # self.env['stock.move'].create({
                #     'name': rec.product_id.name,
                #     'product_id': rec.product_id.id,
                #     'product_uom_qty': 1,
                #     'product_uom': 1,
                #     'location_id': 8,
                #     'location_dest_id': 8,
                #     'state': 'done',
                # })

                temp = 1
        if temp == 1:
            self.write({
                'state': 'approved'
            })

    def button_reject(self):
        print('reject')
        self.write({
            'state': 'rejected'
        })
