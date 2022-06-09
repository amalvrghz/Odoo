from odoo import fields, models


class CollegeStudent(models.Model):
    _name = "college.student"
    _inherit = 'mail.thread'
    _description = 'College Student'
    _rec_name = 'first_name'
    admission_no = fields.Char(string='Admission No')
    admission_date = fields.Date(string="Admission Date")
    first_name = fields.Char(string="First Name")
    last_name = fields.Char(string="Last Name")
    father = fields.Char(string="Father")
    mother = fields.Char(string="Mother")
    communication_address = fields.Text(string="Communication Address")
    permanent_address = fields.Text(string="Permanent Address")
    same_as = fields.Boolean(string="Same as Communication Address", default=False)
    phone = fields.Char(string="Phone")
    email = fields.Char(string="Email")
    course_id = fields.Many2one(comodel_name='college.course', string='Course', related="class_id.course_id")
    semesters_id = fields.Many2one(comodel_name='college.semester', string="Semester", related="class_id.semester_id")
    class_id = fields.Many2one(comodel_name='college.classes', string="Class")
    student_promotion_id = fields.Many2one(comodel_name='promotion.class')
    academic_yr_id = fields.Many2one(comodel_name='academic.year', string="Academic Year", related="class_id.academic_year_id")
    state = fields.Selection([('pending', 'Pending'), ('done', 'Done')], default="pending")

    def button_create(self):
        self.admission_no = self.env['ir.sequence'].next_by_code('college.student')
        admission_list = self.env['college.student'].mapped('admission_no')
        print('list:', admission_list)
        while self.admission_no in admission_list:
            print('admission')
            self.admission_no = self.env['ir.sequence'].next_by_code('college.student')
        self.write({'state': 'done'})


