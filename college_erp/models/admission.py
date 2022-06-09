from odoo import fields, models, api
from odoo.exceptions import ValidationError, UserError
from datetime import date


class CollegeAdmission(models.Model):
    _name = 'college.admission'
    _description = 'College Admission'
    _rec_name = 'admission_num'

    first_name = fields.Char()
    last_name = fields.Char()
    father = fields.Char()
    mother = fields.Char()
    communication_address = fields.Text()
    permanent_address = fields.Text()
    same_as = fields.Boolean(string="Same as Communication Address", default=False)
    phone = fields.Char()
    mail = fields.Char()
    course_id = fields.Many2one("college.course")
    date_of_apply = fields.Date("Date of Application", default=date.today())
    # academic_year = fields.Integer()
    academic_year_id = fields.Many2one('academic.year')
    prev_qualification = fields.Selection([('higher_sec', 'Higher Secondary'), ('ug', 'UG'), ('pg', 'PG')],
                                          string="Previous Educational Qualification")
    edu_institute = fields.Char(string="Educational Institute")
    document = fields.Binary("Transfer Certificate")
    doc_tc = fields.Char()
    admission_num = fields.Char(string='Admission Number', default='New')
    admission_date = fields.Date(string="Admission Date")
    state = fields.Selection(
        [('draft', 'Draft'), ('application', 'Application'), ('approved', 'Approved'), ('done', 'Done'),
         ('rejected', 'Rejected')], default="draft")
    semester_id = fields.Many2one('college.semester', string="Semester")

    # default = lambda self: self.env['college.semester'].search([('name', '=', '1 Sem: BCA')])
    def write(self, vals):
        if vals.get('state') == 'done':
            lines_dict = {
                'first_name': self.first_name,
                'last_name': self.last_name,
                'father': self.father,
                'mother': self.mother,
                'communication_address': self.communication_address,
                'permanent_address': self.permanent_address,
                'same_as': self.same_as,
                'phone': self.phone,
                'email': self.mail,
                # '': self.course,
                'admission_date': self.admission_date,
                'admission_no': self.admission_num,
                'academic_yr_id': self.academic_year_id.id,
                'course_id': self.course_id.id,
                'semesters_id': self.semester_id.id,
                'state': 'done'
            }
            self.env['college.student'].create(lines_dict)
        return super(CollegeAdmission, self).write(vals)

    def button_confirm(self):
        # for rec in self:
        if self.state == 'draft':
            # for rec in self:
            if self.document:
                self.write({'state': 'application'})

            else:
                # raise ValidationError("This is error message.")
                raise UserError('Please add Attachment')

    def button_reject(self):
        mail_template = self.env.ref('college_erp.email_template2')
        mail_template.send_mail(self.id, force_send=True)
        self.write({'state': 'rejected'})

    def button_done(self):
        admission_list = self.env['college.student'].mapped('admission_no')
        print('admission_list:', admission_list)
        self.admission_num = self.env['ir.sequence'].next_by_code('college.admission')
        while self.admission_num in admission_list:
            print('okay')
            self.admission_num = self.env['ir.sequence'].next_by_code('college.admission')
        self.admission_date = date.today()
        mail_template = self.env.ref('college_erp.email_template')
        mail_template.send_mail(self.id, force_send=True)
        print(self.env.user.company_id.email)
        records_bca = self.env['college.semester'].search([('name', '=', '1 Sem: BCA'), ('course2_id', '=', self.course_id.id)])
        records_cs = self.env['college.semester'].search(
            [('name', '=', '1 Sem: BSC CS'), ('course2_id', '=', self.course_id.id)])
        records_mca = self.env['college.semester'].search([('name', '=', '1 Sem: MCA'), ('course2_id', '=', self.course_id.id)])
        if len(records_bca) == 1:
            print('bca')
            self.semester_id = records_bca.id
        elif len(records_cs) == 1:
            print('cs')
            self.semester_id = records_cs.id
        else:
            print('mca')
            self.semester_id = records_mca.id
        self.write({'state': 'done'})

    def reset_button(self):
        self.write({'state': 'draft'})
