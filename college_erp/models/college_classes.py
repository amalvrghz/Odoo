from odoo import fields, models, api


class CollegeClasses(models.Model):
    _name = 'college.classes'
    _description = 'College Classes'
    _rec_name = ''
    name = fields.Char(compute="_compute_cname", store=True)
    semester_id = fields.Many2one('college.semester')
    course_id = fields.Many2one("college.course", related='semester_id.course2_id', store=True)
    academic_year_id = fields.Many2one('academic.year')
    student_ids = fields.One2many('college.student', 'class_id')
    promotion_class_id = fields.Many2one('college.classes', string='Promotion Class')

    @api.depends("semester_id.name", "academic_year_id.name")
    def _compute_cname(self):
        for rec in self:
            # print(rec.semester_id.name)
            # print(rec.academic_year.name)
            rec.name = str(rec.semester_id.name) + str(rec.academic_year_id.name)

    @api.onchange("semester_id", "course_id", "academic_year_id")
    def _compute_students(self):
        # self.student_ids = False
        records = self.env['college.student'].search([('course_id', '=', self.course_id.id), ('semesters_id', '=', self.semester_id.id), ('academic_yr_id', '=', self.academic_year_id.id)])
        for rec in records:
            self.write({'student_ids': rec})
