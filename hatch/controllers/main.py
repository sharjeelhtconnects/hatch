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
                    'department_id': job.department_id.id,
                    'department_title': job.department_id.name
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
            # data = json.loads(request.httprequest.data)
            
            # Extract fields from JSON data
            name = kwargs.get('name')
            last_name = kwargs.get('last_name')
            email = kwargs.get('email')
            phone = kwargs.get('phone')
            industry = kwargs.get('industry')  # Assuming department is a selection field
            applied_position_id = kwargs.get('applied_position')  # Assuming applied_position is a job ID
            resume_file = kwargs.get('resume')  # Assuming resume is a base64 encoded file

            # Find the job position by ID
            job_position = request.env['hr.job'].sudo().browse(int(applied_position_id))
            full_name = name
            # Create applicant record
            applicant_vals = {
                'name': full_name,
                'email_from': email,
                'partner_phone': phone,
                'department_id': industry,
                'job_id': job_position.id,
                # Add more fields as neededs
            }
            

            applicant = request.env['hr.applicant'].sudo().create(applicant_vals)
            
            # Handle file upload (resume)
            # if resume_file:
            #     resume_data = base64.b64encode(resume_file.read()) if resume_file else None
            #     applicant_vals.update({
            #         'resume': resume_data,
            #         'resume_filename': resume_file.filename if resume_file else None,
            #     })

            # Return success response
            # return "Applicant created successfully with ID: %s" % applicant.id
            # return Response(status=204)
            
            # Attach CV as attachment
            if resume_file:
                resume_data = base64.b64encode(resume_file.read())
                attachment_vals = {
                    'name': resume_file.filename,
                    'res_name': f"CV for {name} {last_name}",
                    'res_model': 'hr.applicant',
                    'res_id': applicant.id,
                    'datas': resume_data,
                    'type': 'binary',
                }
                request.env['ir.attachment'].sudo().create(attachment_vals)

            
            # Convert list to JSON string
            json_data = json.dumps(f"Application is successfult submitted {applicant}")
            return request.make_response(data=json_data, headers=[('Content-Type', 'application/json')])
        except Exception as e:
            se = _serialize_exception(e)
            error = {
                'code': 200,
                'message': 'Something went wroung',
                'data': se
            }
            return request.make_response(html_escape(json.dumps(error)))