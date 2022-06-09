from odoo import fields, models, api


class CollegeCourse(models.Model):
    _name = 'college.course'
    _description = 'College Course'
    _rec_name = ''
    name = fields.Char()
    category = fields.Selection(
        [('under_grad', 'Under Graduation'), ('post_grad', 'Post Graduation'), ('diploma', 'Diploma')])
    duration = fields.Integer("Duration(years)")
    num_of_sem = fields.Integer(string="Number of Semester")
    semesters_ids = fields.One2many('college.semester', 'course2_id')
