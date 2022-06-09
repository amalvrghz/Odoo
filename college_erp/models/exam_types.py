from odoo import models, fields


class ExamTypes(models.Model):
    _name = 'exam.types'
    _rec_name = 'type'
    _description = 'Exam Types'
    type = fields.Char(string='Exam Type')