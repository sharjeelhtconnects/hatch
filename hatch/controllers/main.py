# -*- coding: utf-8 -*-

import json
from odoo import http
from odoo.http import content_disposition, request
from odoo.addons.web.controllers.main import _serialize_exception
from odoo.tools import html_escape
import socket

class RecuritmentControllers(http.Controller):

    @http.route('/get_opening', type='http', auth='none')
    def get_opening(self):
        open_jobs = request.env['hr.job'].sudo().search(['|', ('state', '=', 'recruit'), ('website_published', '=', True)])
        job_data = {open_jobs}
        host = socket.gethostname()
        try:
            job_data = []
            for job in open_jobs:
                title = (job.name).lower().replace(" ", "-")
                url = "http://"+"147.182.193.37:8069" +"/jobs/detail/"+title+"-"+(str(job.id))
                job_data.append({
                    'id': job.id,
                    'name': job.name,
                    'description': job.description,
                    'department_id': job.department_id.name,
                    # 'create_date': job.create_date,
                    'city': job.address_id.city,
                    'coutry': job.address_id.country_id.name,
                    'no_position': job.no_of_recruitment,
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
    
    # @http.route('/job_form/<int:job_id>', type='http', auth='none')
    # def job_form(self, job_id):
    #     open_jobs = request.env['hr.job'].sudo().search([('id', '=', job_id)])
    #     try:
    #         host = socket.gethostname()
    #         job_data = []
    #         for job in open_jobs:
    #             title = (job.name).lower().replace(" ", "-")
    #             url = (str(host))+"/jobs/detail/"+title+"-"+(str(job.id))
    #             job_data.append({
    #                 'id': job.id,
    #                 'name': job.name,
    #                 'description': job.description,
    #                 'department_id': job.department_id.name,
    #                 'url': url
    #                 # Add more fields as needed
    #             })

    #         # Convert list to JSON string
    #         json_data = json.dumps(job_data)
    #         return request.make_response(data=json_data, headers=[('Content-Type', 'application/json')])
    #     except Exception as e:
    #         se = _serialize_exception(e)
    #         error = {
    #             'code': 200,
    #             'message': 'Something went wroung',
    #             'data': se
    #         }
    #         return request.make_response(html_escape(json.dumps(error)))