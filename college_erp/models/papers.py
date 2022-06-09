from odoo import fields, models


class ExamPapers(models.Model):
    _name = 'exam.papers'
    _rec_name = ''
    _description = 'Exam Papers'
    subject = fields.Char(string='Subject')
    pass_mark = fields.Float(string="Pass Marks")
    max_mark = fields.Float(string="Max Marks")
    inverse2_id = fields.Many2one('college.exam')
