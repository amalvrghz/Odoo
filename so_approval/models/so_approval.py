from odoo import models, fields, api
from odoo.exceptions import ValidationError


class SaleOrder(models.Model):
    _inherit = 'sale.order'
    state = fields.Selection(selection_add=[('to_approve', 'Waiting For Approval'), ('sent',)])
    flag = fields.Integer()

    def button_send_to_manager(self):
        self.write({'state': 'to_approve'})

    def button_approve(self):
        self.write({'state': 'sent'})
        return super(SaleOrder, self).action_quotation_send()

    @api.onchange("order_line")
    def onchange_order_line(self):
        self.flag = 0
        for rec in self.order_line:
            if rec.price_unit != rec.product_id.list_price:
                self.flag = 1
                return {'warning': {
                    'title': 'Warning',
                    'message': 'Get Approval From Manager'
                    }
                }

    # def action_quotation_send(self):
    #     for rec in self.order_line:
    #         if rec.price_unit != rec.product_id.list_price:
    #             raise ValidationError("Get Approval from Manager")
    #     return super(SaleOrder, self).action_quotation_send()

    def button_reject(self):
        self.write({'state': 'draft'})
