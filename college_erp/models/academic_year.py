from odoo import models, fields


class AcademicYear(models.Model):
    _name = "academic.year"
    _description = 'Academic Year'
    _rec_name = ''
    name = fields.Char(string='Academic Year')
