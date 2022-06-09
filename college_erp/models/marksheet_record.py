from odoo import models, fields


class MarkSheetMarks(models.Model):
    _name = 'mark.sheet.marks'
    _rec_name = ''
    _description = 'Mark Sheet Marks'
    subject = fields.Char(string="Subject")
    marks = fields.Float(string="Marks Scored")
    pass_marks = fields.Float(string="Pass Marks")
    max_marks = fields.Float(string="Max Marks")
    student_marksheet_id = fields.Many2one('student.mark.sheet')
    pass_fail = fields.Boolean(default=False)
