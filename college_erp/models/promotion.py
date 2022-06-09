from odoo import fields, models
from odoo.exceptions import UserError


class PromotionClass(models.Model):
    _name = 'promotion.class'
    _description = 'Class Promotion'
    _rec_name = 'exam_id'
    exam_id = fields.Many2one('college.exam', string='Exam')
    college_class_id = fields.Many2one('college.classes', string='Class')
    semester_id = fields.Many2one('college.semester', string='Semester', related='college_class_id.semester_id')
    academic_yr_id = fields.Many2one('academic.year', string='Academic Year', related='college_class_id.academic_year_id')
    promoted_students_ids = fields.One2many('college.student', 'student_promotion_id', string='Promoted Students')
    state = fields.Selection([('pending', 'Pending'), ('completed', 'Completed')])
    btn_hide = fields.Integer(default=0)

    def button_generate_promotion(self):
        print('alo')
        records = self.env['student.mark.sheet'].search([('classes_id', '=', self.college_class_id.id), ('pass_fails', '=', True)])
        print(records)
        # print(records.mapped('student_name_id'))
        print(records.student_name_id)
        # print(records.pass_fails)
        if len(records) > 0:
            # for rec in records:
                # self.write({'promoted_students_ids': [(5, 0, 0)]})
            self.write({
                'promoted_students_ids': records.student_name_id.ids
                })
            self.btn_hide = 1
            self.state = 'pending'
        else:
            print('No Passed Students Exist')
            raise UserError('No Passed Students Exist')

    def button_promote(self):
        print('hi')
        records = self.env['college.classes'].search([('semester_id', '=', self.semester_id.id), ('academic_year_id', '=', self.academic_yr_id.id)]).promotion_class_id
        print('records of college classes:', records)
        print('self:', self)
        if len(records) > 0:
            for rec in self.promoted_students_ids:
                print('record:', rec)
                print('hiii')
                records.write({'student_ids': rec})
            self.btn_hide = 0
            self.env['college.student'].search([('class_id', '=', self.college_class_id.id)]).write({'class_id': records.id})
            self.state = 'completed'
        else:
            raise UserError('No Students To Promote')





