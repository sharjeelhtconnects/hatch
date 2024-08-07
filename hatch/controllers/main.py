# -*- coding: utf-8 -*-

import json
from odoo import http
from odoo.http import content_disposition, request
from odoo.addons.web.controllers.main import _serialize_exception
from odoo.tools import html_escape


class RecuritmentControllers(http.Controller):

    @http.route('/get_opening', type='http', auth='none')
    def get_opening(self):
        open_jobs = request.env['hr.job'].sudo().search(['|', ('state', '=', 'recruit'), ('website_published', '=', True)])
        job_data = {open_jobs}
        try:
            # job_data['jobs'] = open_jobs
            # Convert data dictionary to JSON string
            # json_data = json.dumps(job_data)
            
            # Convert the recordset to a list of dictionaries
            job_data = []
            for job in open_jobs:
                job_data.append({
                    'id': job.id,
                    'name': job.name,
                    'description': job.description,
                    'department_id': job.department_id.name,
                    # Add more fields as needed
                })

            # Convert list to JSON string
            json_data = json.dumps(job_data)
            return request.make_response(data=json_data, headers=[('Content-Type', 'application/json')])
        except Exception as e:
            se = _serialize_exception(e)
            error = {
                'code': 200,
                'message': 'Something went wroung',
                'data': se
            }
            return request.make_response(html_escape(json.dumps(error))) 
    
    @http.route('/job_form/<int:job_id>/<str:job_title>', type='http', auth='none')
    def job_form(self, job_id, job_title):
        open_jobs = request.env['hr.job'].sudo().search([('id', '=', job_id)])
        if not open_jobs:
            error = {
                'code': 404,
                'message': 'Not Found',
            }
            return request.make_response(html_escape(json.dumps(error)))
        try:
            # job_data['jobs'] = open_jobs
            # Convert data dictionary to JSON string
            # json_data = json.dumps(job_data)
            
            # Convert the recordset to a list of dictionaries
            host = request.httprequest.environ.get('HTTP_HOST', '')
            job_data = []
            for job in open_jobs:
                title = (job.name).lower().replace(" ", "-")
                url = (str(host))+"/jobs/detail/"+title+"-"+(str(job.id))
                job_data.append({
                    'id': job.id,
                    'name': job.name,
                    'description': job.description,
                    'department_id': job.department_id.name,
                    'url': url
                    # Add more fields as needed
                })

            # Convert list to JSON string
            json_data = json.dumps(job_data)
            return request.make_response(data=json_data, headers=[('Content-Type', 'application/json')])
        except Exception as e:
            se = _serialize_exception(e)
            error = {
                'code': 200,
                'message': 'Something went wroung',
                'data': se
            }
            return request.make_response(html_escape(json.dumps(error)))