import json
from odoo import http
from odoo.http import content_disposition, request
from odoo.addons.web.controllers.main import _serialize_exception
from odoo.tools import html_escape


class XLSXReportController(http.Controller):
    @http.route('/xlsx_reports', type='http', auth='user', methods=['POST'])
    def get_report_xlsx(self, model, output_format, options, report_name):
        uid = request.session.uid
        report_obj = request.env[model].with_user(uid)
        options = json.loads(options)
        try:
            if output_format == 'xlsx':
                response = request.make_response(
                    None,
                    headers=[('Content-Type', 'application/vnd.ms-excel'),
                             ('Content-Disposition', content_disposition(report_name + '.xlsx'))
                             ]
                )
                report_obj.get_xlsx_report(response, options)
            return response
        except Exception as e:
            se = _serialize_exception(e)
            error = {
                'code': 200,
                'message': 'Odoo Server Error',
                'data': se
            }
            return request.make_response(html_escape(json.dumps(error)))
