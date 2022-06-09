from odoo import fields, models


class CourseSyllabus(models.Model):
    _name = 'course.syllabus'
    _description = 'Course Syllabus'
    subject = fields.Char(string="Subject")
    max_marks = fields.Float(string="Maximum Marks")
    syllabus_semester_id = fields.Many2one('college.semester')
