from odoo import models, fields, api
from odoo.exceptions import ValidationError


class MarkSheetReport(models.AbstractModel):
    _name = 'report.college_erp.report_student_mark_sheet'

    @api.model
    def _get_report_values(self, docids, data=None):
        dom = []
        if data['report_type'] == 'student_wise':
            if data['student_id']:
                dom.append(('student_name_id', '=', data['student_id']))
            if data['semester_id']:
                dom.append(('semesters_id', '=', data['semester_id']))
            if data['exam_type']:
                dom.append(('exam_id', '=', data['exam_type']))
            docs = self.env['student.mark.sheet'].search(dom)

        return {
            'doc_ids': docs.ids,
            'doc_model': 'student.mark.sheet',
            'data': data,
            'docs': docs,
        }
