from odoo import models, fields, api


class ClassWiseMarkSheetReport(models.AbstractModel):
    _name = 'report.college_erp.report_class_wise_mark_sheet'

    @api.model
    def _get_report_values(self, docids, data=None):
        if not data['class_id'] and not data['semester_id'] and not data['exam_type']:
            # print('data:', data)

            self.env.cr.execute('select college_classes.name,college_course.name,academic_year.name,exam_types.type,college_classes.id from college_exam '
                                'inner join college_classes on college_exam.class_id=college_classes.id '
                                'inner join college_course on college_classes.course_id=college_course.id '
                                'inner join academic_year on college_classes.academic_year_id=academic_year.id '
                                'inner join exam_types on college_exam.type_id=exam_types.id')
            rec_list = self.env.cr.fetchall()
            # print('rec list:', rec_list)
        if data['class_id']:
            self.env.cr.execute(
                'select college_classes.name,college_course.name,academic_year.name,exam_types.type,college_classes.id from college_exam '
                'inner join college_classes on college_exam.class_id=college_classes.id and college_exam.class_id={} '
                'inner join college_course on college_classes.course_id=college_course.id '
                'inner join academic_year on college_classes.academic_year_id=academic_year.id '
                'inner join exam_types on college_exam.type_id=exam_types.id '
                'inner join college_semester on college_classes.semester_id=college_semester.id'.format(data['class_id']))
            rec_list = self.env.cr.fetchall()
        if data['semester_id']:
            self.env.cr.execute(
                'select college_classes.name,college_course.name,academic_year.name,exam_types.type,college_classes.id from college_exam '
                'inner join college_classes on college_exam.class_id=college_classes.id '
                'inner join college_course on college_classes.course_id=college_course.id '
                'inner join academic_year on college_classes.academic_year_id=academic_year.id '
                'inner join exam_types on college_exam.type_id=exam_types.id '
                'inner join college_semester on college_classes.semester_id=college_semester.id and college_classes.semester_id={}'.format(data['semester_id']))
            rec_list = self.env.cr.fetchall()
        if data['class_id'] and data['semester_id']:
            self.env.cr.execute(
                'select college_classes.name,college_course.name,academic_year.name,exam_types.type,college_classes.id from college_exam '
                'inner join college_classes on college_exam.class_id=college_classes.id and college_exam.class_id={} '
                'inner join college_course on college_classes.course_id=college_course.id '
                'inner join academic_year on college_classes.academic_year_id=academic_year.id '
                'inner join exam_types on college_exam.type_id=exam_types.id '
                'inner join college_semester on college_classes.semester_id=college_semester.id and college_classes.semester_id={}'.format(data['class_id'], data['semester_id']))
            rec_list = self.env.cr.fetchall()
        if data['exam_type']:
            self.env.cr.execute(
                'select college_classes.name,college_course.name,academic_year.name,exam_types.type,college_classes.id from college_exam '
                'inner join college_classes on college_exam.class_id=college_classes.id '
                'inner join college_course on college_classes.course_id=college_course.id '
                'inner join academic_year on college_classes.academic_year_id=academic_year.id '
                'inner join exam_types on college_exam.type_id=exam_types.id and college_exam.type_id={} '
                'inner join college_semester on college_classes.semester_id=college_semester.id'.format(data['exam_type']))
            rec_list = self.env.cr.fetchall()
        if data['class_id'] and data['exam_type']:
            self.env.cr.execute(
                'select college_classes.name,college_course.name,academic_year.name,exam_types.type,college_classes.id from college_exam '
                'inner join college_classes on college_exam.class_id=college_classes.id and college_exam.class_id={} '
                'inner join college_course on college_classes.course_id=college_course.id '
                'inner join academic_year on college_classes.academic_year_id=academic_year.id '
                'inner join exam_types on college_exam.type_id=exam_types.id and college_exam.type_id={} '
                'inner join college_semester on college_classes.semester_id=college_semester.id'.format(data['class_id'], data['exam_type']))
            rec_list = self.env.cr.fetchall()
        if data['semester_id'] and data['exam_type']:
            self.env.cr.execute(
                'select college_classes.name,college_course.name,academic_year.name,exam_types.type,college_classes.id from college_exam '
                'inner join college_classes on college_exam.class_id=college_classes.id '
                'inner join college_course on college_classes.course_id=college_course.id '
                'inner join academic_year on college_classes.academic_year_id=academic_year.id '
                'inner join exam_types on college_exam.type_id=exam_types.id and college_exam.type_id={} '
                'inner join college_semester on college_classes.semester_id=college_semester.id and college_classes.semester_id={}'.format(data['exam_type'], data['semester_id']))
            rec_list = self.env.cr.fetchall()
        if data['class_id'] and data['semester_id'] and data['exam_type']:
            self.env.cr.execute(
                'select college_classes.name,college_course.name,academic_year.name,exam_types.type,college_classes.id from college_exam '
                'inner join college_classes on college_exam.class_id=college_classes.id and college_exam.class_id={} '
                'inner join college_course on college_classes.course_id=college_course.id '
                'inner join academic_year on college_classes.academic_year_id=academic_year.id '
                'inner join exam_types on college_exam.type_id=exam_types.id and college_exam.type_id={} '
                'inner join college_semester on college_classes.semester_id=college_semester.id and college_classes.semester_id={}'.format(data['class_id'], data['exam_type'], data['semester_id']))
            rec_list = self.env.cr.fetchall()
        doc = []
        students = self.env['student.mark.sheet'].search([])
        return {
            'doc_ids': docids,
            'doc_model': 'student.mark.sheet',
            'data': students,
            'docs': rec_list,
        }

