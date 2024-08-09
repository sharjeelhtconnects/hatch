# -*- coding: utf-8 -*-

import base64
import json
from odoo import http
from odoo.http import content_disposition, request, Response
from odoo.addons.web.controllers.main import _serialize_exception
from odoo.tools import html_escape

class RecuritmentControllers(http.Controller):

    @http.route('/api/get_opening', type='http', auth='none')
    def get_opening(self):
        open_jobs = request.env['hr.job'].sudo().search(['|', ('state', '=', 'recruit'), ('website_published', '=', True)])
        job_data = {open_jobs}
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
                    'create_date': job.create_date.strftime('%Y-%m-%d %H:%M:%S'),
                    'city': job.address_id.city,
                    'coutry': job.address_id.country_id.name,
                    'no_position': job.no_of_recruitment,
                    'url': url
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
    
    
    @http.route('/api/get_recruitment_jobs', type='http', auth='public', methods=['GET'], csrf=False)
    def get_recruitment_jobs(self, **post):
        try:
            # Fetch all jobs in "Recruitment" state
            jobs = request.env['hr.job'].sudo().search([('state', '=', 'recruit')])

            # Prepare list to store job data
            job_data = []
            for job in jobs:
                job_data.append({
                    'id': job.id,
                    'title': job.name,
                    'industry_id': job.industry_id,
                    'industry_title': job.industry_id.name
                    # Add more fields as needed
                })

            # Serialize data to JSON
            json_data = json.dumps(job_data)

            # Return JSON response
            return request.make_response(json_data, headers={'Content-Type': 'application/json'})

        except Exception as e:
            # Handle exceptions and return error response
            return "Error fetching recruitment jobs: %s" % str(e)

    
    @http.route('/api/create_applicant', type='http', auth='none', methods=['POST'], csrf=False)
    def create_applicant(self, **kwargs):
        try:
            # Parse JSON data from POST request
            data = json.loads(request.httprequest.data)
            
            # Extract fields from JSON data
            name = data.get('name')
            last_name = data.get('last_name')
            email = data.get('email')
            phone = data.get('phone')
            industry = data.get('industry')  # Assuming industry is a selection field
            applied_position_id = data.get('applied_position')  # Assuming applied_position is a job ID
            resume = data.get('resume')  # Assuming resume is a base64 encoded file

            # Decode resume file from base64
            resume_data = base64.b64decode(resume)

            # Find the job position by ID
            job_position = request.env['hr.job'].sudo().browse(int(applied_position_id))

            # Create applicant record
            applicant_vals = {
                'name': name,
                'last_name': last_name,
                'email': email,
                'phone': phone,
                'industry_id': industry,
                'job_id': job_position.id,
                'resume': resume_data,
                # Add more fields as needed
            }

            # applicant = request.env['hr.applicant'].sudo().create(applicant_vals)

            # Return success response
            # return "Applicant created successfully with ID: %s" % applicant.id
            # return Response(status=204)
            # Convert list to JSON string
            json_data = json.dumps("Application is successfult submitted")
            return request.make_response(data=json_data, headers=[('Content-Type', 'application/json')])
        except Exception as e:
            se = _serialize_exception(e)
            error = {
                'code': 200,
                'message': 'Something went wroung',
                'data': se
            }
            return request.make_response(html_escape(json.dumps(error)))