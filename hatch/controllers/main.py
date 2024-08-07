# -*- coding: utf-8 -*-

import json
from odoo import http
from odoo.http import content_disposition, request
from odoo.addons.web.controllers.main import _serialize_exception
from odoo.tools import html_escape


class RecuritmentControllers(http.Controller):

    @http.route('/get_opening', type='http', auth='none')
    def get_opening(self):
        open_jobs = request.env['hr.job'].sudo().search(['|', ('state', '=', 'open'), ('website_published', '=', True)])
        job_data = {}
        try:
            job_data['jobs'] = open_jobs
            return json.dumps(job_data)
        except Exception as e:
            se = _serialize_exception(e)
            error = {
                'code': 200,
                'message': 'Something went wroung',
                'data': se
            }
            return request.make_response(html_escape(json.dumps(error)))