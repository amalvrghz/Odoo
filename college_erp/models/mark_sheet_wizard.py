from odoo import models, fields
from odoo.exceptions import ValidationError
import io
import json
from odoo.tools import date_utils
from odoo.tools.misc import xlsxwriter


class MarkSheetWizard(models.TransientModel):
    _name = 'mark.sheet.wizard'
    _description = 'Marksheet Wizard'
    report_type = fields.Selection([('student_wise', 'Student Wise'), ('class_wise', 'Class Wise')], 'Report Type')
    student_id = fields.Many2one('college.student', 'Student')
    class_id = fields.Many2one('college.classes', 'Class')
    semester_id = fields.Many2one('college.semester', string='Semester')
    exam_type = fields.Many2one('exam.types', 'Exam Type')

    def button_print_report(self):
        if not self.report_type:
            raise ValidationError("Choose A Report type")
        elif self.report_type == 'student_wise':
            data = {
                'report_type': self.report_type,
                'student_id': self.student_id.id,
                # 'class_id': self.class_id.id,
                'semester_id': self.semester_id.id,
                'exam_type': self.exam_type.id
            }
            return self.env.ref('college_erp.action_student_mark_sheet').report_action(None, data=data)

        else:
            data = {
                'report_type': self.report_type,
                # 'student_id': self.student_id.id,
                'class_id': self.class_id.id,
                'semester_id': self.semester_id.id,
                'exam_type': self.exam_type.id
            }
            return self.env.ref('college_erp.action_class_wise_mark_sheet').report_action(None, data=data)

    def button_print_xlsx(self):
        dom = []
        data = []
        if not self.report_type:
            raise ValidationError("Choose A Report type")
        elif self.report_type == 'student_wise':
            if self.student_id:
                dom.append(('student_name_id', '=', self.student_id.id))
            if self.semester_id:
                dom.append(('semesters_id', '=', self.semester_id.id))
            if self.exam_type:
                dom.append(('exam_id', '=', self.exam_type.id))
            data = self.env['student.mark.sheet'].search_read(dom)
            doc = self.env['mark.sheet.marks'].search_read([])
            for rec in doc:
                data.append(rec)
            for rec in data:
                rec['flag'] = 'flag'
        else:
            q1 = 'select college_classes.name as class,college_course.name as course,academic_year.name as year,exam_types.type,college_classes.id as cid from college_exam ' \
                 'inner join college_classes on college_exam.class_id=college_classes.id ' \
                 'inner join college_course on college_classes.course_id=college_course.id ' \
                 'inner join academic_year on college_classes.academic_year_id=academic_year.id ' \
                 'inner join exam_types on college_exam.type_id=exam_types.id'
            q2 = 'select college_classes.name as class,college_course.name as course,academic_year.name as year,exam_types.type,college_classes.id as cid from college_exam'
            q3 = 'inner join college_classes on college_exam.class_id=college_classes.id'
            q4 = 'inner join college_course on college_classes.course_id=college_course.id'
            q5 = 'inner join academic_year on college_classes.academic_year_id=academic_year.id'
            q6 = 'inner join exam_types on college_exam.type_id=exam_types.id'
            q7 = 'inner join college_semester on college_classes.semester_id=college_semester.id'
            if not self.class_id and not self.semester_id and not self.exam_type:
                self.env.cr.execute(q1)
                data = self.env.cr.dictfetchall()
            elif self.class_id:
                self.env.cr.execute(
                    '{} {} and college_exam.class_id={} {} {} {} {}'.format(q2, q3, self.class_id.id, q4, q5, q6, q7))
                data = self.env.cr.dictfetchall()
            elif self.semester_id:
                self.env.cr.execute(
                    '{} {} {} {} {} {} and college_classes.semester_id={}'.format(q2, q3, q4, q5, q6, q7, self.semester_id.id))
                data = self.env.cr.dictfetchall()
            elif self.class_id and self.semester_id:
                self.env.cr.execute(
                    '{} {} and college_exam.class_id={} {} {} {} {} and college_classes.semester_id={}'.format(q2, q3, self.class_id.id, q4, q5, q6, q7, self.semester_id.id))
                data = self.env.cr.dictfetchall()
            elif self.exam_type:
                self.env.cr.execute(
                    '{} {} {} {} {} and college_exam.type_id={} {}'.format(q2, q3, q4, q5, q6, self.exam_type.id, q7))
                data = self.env.cr.dictfetchall()
            elif self.class_id and self.exam_type:
                self.env.cr.execute(
                    '{} {} and college_exam.class_id={} {} {} {} and college_exam.type_id={} {}'.format(q2, q3, self.class_id.id, q4, q5, q6, self.exam_type.id, q7))
                data = self.env.cr.dictfetchall()
            elif self.semester_id and self.exam_type:
                self.env.cr.execute(
                    '{} {} {} {} {} and college_exam.type_id={} {} and college_classes.semester_id={}'.format(q2, q3, q4, q5, q6, self.exam_type.id, q7, self.semester_id))
                data = self.env.cr.dictfetchall()
            else:
                self.env.cr.execute(
                    '{} {} and college_exam.class_id={} {} {} {} and college_exam.type_id={} {} and college_classes.semester_id={}'.format(q2, q3, self.class_id.id, q4, q5, q6, self.exam_type.id, q7, self.semester_id.id))
                data = self.env.cr.dictfetchall()

            students = self.env['student.mark.sheet'].search_read([])
            for rec in students:
                data.append(rec)
            marks = self.env['mark.sheet.marks'].search_read([])
            for rec in marks:
                data.append(rec)

        return {
            'type': 'ir.actions.report',
            'report_type': 'xlsx',
            'data': {
                'model': 'mark.sheet.wizard',
                'output_format': 'xlsx',
                'options': json.dumps(data, default=date_utils.json_default),
                'report_name': 'MY REPORT',
            }
        }

    def get_xlsx_report(self, response, data):
        output = io.BytesIO()
        workbook = xlsxwriter.Workbook(output, {'in_memory': True})
        sheet = workbook.add_worksheet()
        cell_format = workbook.add_format({'font_size': '12px'})
        head = workbook.add_format({'align': 'center', 'bold': True, 'font_size': '18px'})
        head2 = workbook.add_format({'align': 'center', 'bold': True, 'font_size': '12px'})
        txt = workbook.add_format({'font_size': '10px', 'align': 'center', 'bold': True})
        txt3 = workbook.add_format({'font_size': '10px', 'bold': True})
        txt4 = workbook.add_format({'font_size': '10px', 'align': 'center', 'bold': True})
        txt2 = workbook.add_format({'font_size': '10px', 'align': 'center'})
        row1 = 1
        row2 = 2
        col1 = 2
        col2 = 8

        for rec in data:
            if 'flag' in rec:
                if 'student_name_id' in rec:
                    title = rec['student_name_id'][1]
                    title += ' : Mark List'
                    exam = 'Exam : '
                    exam += rec['exam_id'][1]
                    course = 'Course : ' + rec['courses_id'][1]
                    result = 'Result : '
                    if rec['pass_fails']:
                        result += 'Pass'
                    else:
                        result += 'Fail'
                    sheet.merge_range(row1, col1, row2, col2, title, head)
                    sheet.merge_range(row1 + 2, col1 + 2, row1 + 2, col2 - 2, course, head2)
                    sheet.merge_range(row1 + 4, col1 - 2, row1 + 4, col1 - 1, exam)
                    sheet.merge_range(row1 + 5, col1 - 2, row1 + 5, col1 - 1, result)
                    sheet.merge_range(row1 + 6, col1, row1 + 6, col1 + 1, 'Subject', txt)
                    sheet.merge_range(row1 + 6, col1 + 2, row1 + 6, col1 + 3, 'Mark', txt)
                    sheet.merge_range(row1 + 6, col1 + 4, row1 + 6, col1 + 5, 'Pass Mark', txt)
                    sheet.merge_range(row1 + 6, col1 + 6, row1 + 6, col1 + 7, 'Pass/Fail', txt)
                    i = 0
                    for recc in data:
                        if 'subject' in recc:
                            if rec['id'] == recc['student_marksheet_id'][0]:
                                sheet.merge_range(row1 + 7 + i, col1, row1 + 7 + i, col1 + 1, recc['subject'], txt2)
                                sheet.merge_range(row1 + 7 + i, col1 + 2, row1 + 7 + i, col1 + 3, recc['marks'], txt2)
                                sheet.merge_range(row1 + 7 + i, col1 + 4, row1 + 7 + i, col1 + 5, recc['pass_marks'],
                                                  txt2)
                                if recc['pass_fail']:
                                    sheet.merge_range(row1 + 7 + i, col1 + 6, row1 + 7 + i, col1 + 7, 'Pass', txt2)
                                else:
                                    sheet.merge_range(row1 + 7 + i, col1 + 6, row1 + 7 + i, col1 + 7, 'Fail', txt2)
                                i += 1

            else:
                if 'class' in rec:
                    col1 = 2
                    col2 = 8
                    sheet.merge_range(row1, col1 + 2, row2, col2 + 2, rec['class'] + ' : Mark List', head)
                    sheet.merge_range(row1 + 2, col1 + 4, row1 + 2, col2, rec['course'] + ' : ' + rec['year'],
                                      head2)
                    sheet.merge_range(row1 + 4, col1 - 2, row1 + 4, col1 - 1, 'Exam : ' + rec['type'], txt3)
                    count = 0
                    pas = 0
                    fail = 0
                    for recordd in data:
                        if 'student_name_id' in recordd:
                            if rec['cid'] == recordd['classes_id'][0]:
                                count += 1
                                if recordd['pass_fails']:
                                    pas += 1
                                else:
                                    fail += 1
                    sheet.write(row1 + 5, col1 - 2, 'Total : ', txt3)
                    sheet.write(row1 + 5, col1 - 1, count, txt4)
                    sheet.write(row1 + 6, col1 - 2, 'Pass : ', txt3)
                    sheet.write(row1 + 6, col1 - 1, pas, txt4)
                    sheet.write(row1 + 7, col1 - 2, 'Fail : ', txt3)
                    sheet.write(row1 + 7, col1 - 1, fail, txt4)
                    sheet.merge_range(row1 + 10, col1 - 1, row1 + 10, col1, 'Student', txt)
                    j = 0
                    for record in data:
                        if 'classes_id' in record:
                            if rec['cid'] == record['classes_id'][0]:
                                for recrd in data:
                                    if 'subject' in recrd:
                                        if record['id'] == recrd['student_marksheet_id'][0]:
                                            if j < 3:
                                                col1 += 1
                                                sheet.merge_range(row1 + 10, col1, row1 + 10, col1 + 1,
                                                                  recrd['subject'], txt)
                                                col1 += 1
                                                j += 1
                                x = col1
                    sheet.merge_range(row1 + 10, col1 + 1, row1 + 10, col1 + 2, 'Obtained Mark', txt)
                    sheet.merge_range(row1 + 10, col1 + 3, row1 + 10, col1 + 4, 'Total', txt)
                    sheet.merge_range(row1 + 10, col1 + 5, row1 + 10, col1 + 6, 'Pass/Fail', txt)
                    k = 0
                    col1 = 2
                    col2 = 8
                    j = 0
                    for record in data:
                        if 'student_name_id' in record:
                            tot = 0
                            for recrd in data:
                                if 'subject' in recrd:
                                    if record['id'] == recrd['student_marksheet_id'][0]:
                                        tot += recrd['max_marks']
                            if rec['cid'] == record['classes_id'][0]:
                                sheet.merge_range(row1 + 11 + k, col1 - 1, row1 + 11 + k, col1,
                                                  record['student_name_id'][1], txt2)
                                sheet.merge_range(row1 + 11 + k, x + 1, row1 + 11 + k, x + 2, record['total'], txt2)
                                sheet.merge_range(row1 + 11 + k, x + 3, row1 + 11 + k, x + 4, tot, txt2)
                                if record['pass_fails']:
                                    sheet.merge_range(row1 + 11 + k, x + 5, row1 + 11 + k, x + 6, 'Pass', txt2)
                                else:
                                    sheet.merge_range(row1 + 11 + k, x + 5, row1 + 11 + k, x + 6, 'Fail', txt2)
                                k += 1
                    for recc in data:
                        if 'classes_id' in recc:
                            if rec['cid'] == recc['classes_id'][0]:
                                for recrd in data:
                                    if 'subject' in recrd:
                                        if recc['id'] == recrd['student_marksheet_id'][0]:
                                            if j < 3:
                                                col1 += 1
                                                sheet.merge_range(row1 + 11, col1, row1 + 11, col1 + 1, recrd['marks'],
                                                                  txt2)
                                                col1 += 1
                                                j += 1
                                            if j > 3:
                                                col1 += 1
                                                sheet.merge_range(row1 + 12, col1 - 6, row1 + 12, col1 - 5,
                                                                  recrd['marks'],
                                                                  txt2)
                                                col1 += 1
                                                j += 1
                                            if j == 3:
                                                j += 1
            row1 += 14
            row2 += 14
        workbook.close()
        output.seek(0)
        response.stream.write(output.read())
        output.close()
