from odoo import fields, models, api


class CollegeSemester(models.Model):
    _name = 'college.semester'
    _description = 'Semesters of the Course'
    name = fields.Char()
    _rec_name = ''
    num_of_sem = fields.Char(string="Semester Number")
    course2_id = fields.Many2one('college.course', string="Course")
    syllabus_ids = fields.One2many('course.syllabus', 'syllabus_semester_id', string="Syllabus")

    @api.onchange("course2_id", "num_of_sem")
    def _compute_name(self):
        print('hi')
        self.name = str(self.num_of_sem) + ' Sem: ' + str(self.course2_id.name)
        # rec.sem_name = str(rec.num_of_sem) + ' Sem: ' + str(rec.course2_id.name)
        print('hi')

