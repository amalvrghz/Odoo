from odoo import models, fields


class MaterialRequestLines(models.Model):
    _name = 'material.request.lines'
    # _inherit = 'crm.lead'
    _rec_name = ''
    _description = 'Material Request Lines'
    product_id = fields.Many2one(comodel_name='product.product', string="Product Name")
    # product_id = fields.Many2one('product.template', 'Product')
    # partner_id = fields.Many2one('res.partner', 'Partners')
    request_type = fields.Selection([('purchase_order', 'Purchase Order'), ('internal_transfer', 'Internal Transfer')], string="Request Type")
    material_request_id = fields.Many2one('material.request')
    from_location = fields.Many2one(comodel_name="stock.location", string="From Location")
    to_location = fields.Many2one(comodel_name="stock.location", string="To Location")
