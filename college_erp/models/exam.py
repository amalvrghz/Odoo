from odoo import fields, models, api
from datetime import date


class CollegeExam(models.Model):
    _name = 'college.exam'
    _rec_name = ''
    _description = 'College Exam'
    name = fields.Char(compute="_compute_name")
    type_id = fields.Many2one('exam.types')
    class_id = fields.Many2one('college.classes')
    semester_id = fields.Many2one('college.semester', related='class_id.semester_id')
    course_id = fields.Many2one('college.course', related='class_id.course_id')
    start_date = fields.Date(default=date.today())
    end_date = fields.Date(default=date.today())
    state = fields.Selection([('draft', 'Draft'), ('confirmed', 'Confirmed'), ('completed', 'Completed')],
                             default='draft')
    papers_ids = fields.One2many('exam.papers', 'inverse2_id')
    student_count = fields.Integer(compute='_compute_count')

    def button_confirmed(self):
        if self.state == 'draft':
            self.write({'state': 'confirmed'})

    def button_completed(self):
        if self.state == 'confirmed':
            self.write({'state': 'completed'})

    def button_reset(self):
        self.write({'state': 'draft'})

    @api.depends('type_id', 'semester_id')
    def _compute_name(self):
        for rec in self:
            # print(self.semester_id)
            rec.name = str(rec.type_id.type) + '/' + str(rec.semester_id.name)
            print('compute_name')

    @api.onchange('type_id', 'semester_id')
    def _onchange_papers_id(self):
        # for rec in self:
        self.write({'papers_ids': [(5, 0, 0)]})
        if self.type_id.type == 'Semester':
            records = self.env['college.semester'].search([('name', '=', self.semester_id.name)])
            print(records)
            print(self.semester_id.id)
            print(records.syllabus_ids)
            self.write({'papers_ids': [(0, 0, {
                'subject': record.subject,
                'max_mark': record.max_marks
            }) for record in records.syllabus_ids]
                        })
            print(self.papers_ids)

    def update_state(self):
        tody = fields.date.today()
        # print(a)
        domain = self.env['college.exam'].search([('end_date', '<', tody)])
        print(domain)
        domain.write({
            'state': 'completed'})
        print('updatestate')

    def valuation(self):
        print('valuation_fn')
        return {
            'name': 'Students',
            'type': 'ir.actions.act_window',
            'res_model': 'college.student',
            'view_mode': 'tree,form',
            'domain': [('class_id', '=', self.class_id.id)],
        }

    def _compute_count(self):
        for rec in self:
            dom = rec.env['college.student'].search([('class_id', '=', rec.class_id.id)])
            print(len(dom))
            rec.student_count = len(dom)
            print('compute_count')

    def button_generate_marksheet(self):
        print("generate_marksheet")

        dom = self.env['college.student'].search([('class_id', '=', self.class_id.id)])
        print(dom)
        for recc in dom:
            print(recc.first_name)
            # student_dict = {
            #     'student_name': recc.first_name,
            #     'classes_id': recc.class_id.id,
            #     'courses_id': recc.course_id.id,
            #     'semesters_id': recc.semesters_id.id,
            #     'exam_id': self.type_id.id
            # }
            print(self.type_id.id)
            student_list = recc.env['student.mark.sheet'].search([('student_name_id', '=', recc.first_name)])
            print(student_list)
            print(self.papers_ids)
            if len(student_list) == 0:
                lists = []
                # abc = self.env['college.semester'].search([('name', '=', self.semester_id.id)])
                recs = self.env['student.mark.sheet'].create({
                                                                 'student_name_id': recc.id,
                                                                 'classes_id': recc.class_id.id,
                                                                 'courses_id': recc.course_id.id,
                                                                 'semesters_id': recc.semesters_id.id,
                                                                 'exam_id': self.type_id.id,
                                                                 'marks_ids': [(0, 0, {
                                                                     'subject': record.subject,
                                                                     'pass_marks': record.pass_mark,
                                                                     'max_marks': record.max_mark
                                                                 }) for record in self.papers_ids]

                                                             } for recc in recc)
                self.state = 'completed'
            else:
                self.state = 'completed'
                print("student exist")
        # self.ensure_one()
        return {
            'name': 'Mark sheets',
            'type': 'ir.actions.act_window',
            'res_model': 'student.mark.sheet',
            'view_mode': 'tree,form',
        }

    # def show_students(self):
