from odoo import fields, models, api


class StudentMarkSheet(models.Model):
    _name = 'student.mark.sheet'
    _description = 'Student Mark sheet'
    _rec_name = 'student_name_id'
    student_name_id = fields.Many2one('college.student', 'Name')
    exam_id = fields.Many2one('exam.types')
    classes_id = fields.Many2one('college.classes', 'Class')
    courses_id = fields.Many2one('college.course', 'Course')
    semesters_id = fields.Many2one('college.semester', 'Semester')
    marks_ids = fields.One2many('mark.sheet.marks', 'student_marksheet_id', string="Marks")
    pass_fails = fields.Boolean(default=False, string="Pass/Fail")
    rank = fields.Integer(string='Rank', default=0, compute='_compute_rank')
    total = fields.Float(string='Total', store=True, compute='_compute_total')

    @api.onchange('marks_ids')
    def _compute_pass_fails(self):
        self.pass_fails = False
        ab = 0
        for rec in self.marks_ids:
            # print(rec.marks)
            # print(rec.pass_marks)
            if rec.marks > rec.pass_marks:
                rec.pass_fail = True
            else:
                rec.pass_fail = False
            if not rec.pass_fail:
                ab = 1
        if ab == 1:
            self.pass_fails = False
        else:
            self.pass_fails = True

    @api.depends('marks_ids.marks')
    def _compute_total(self):
        for rec in self:
            totals = 0
            for recc in rec.marks_ids:
                totals = totals + recc.marks
                # print(self.total)
            print("VALUE: ", totals)
            rec.total = totals
        print(self, "as")
        for rec in self:
            print("Totals: ", rec.total)

    @api.depends('total')
    def _compute_rank(self):
        self.rank = 1
        a = self.env['student.mark.sheet'].search([('total', '>=', 0)])
        print(a)
        mapp = a.mapped('total')
        mapp.sort(reverse=True)
        print(len(mapp))
        j = 0
        while j < len(mapp):
            for rec in a:
                if rec.total == mapp[j]:
                    rec.rank = j+1
            j = j + 1

