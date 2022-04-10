from app import app
from flask import jsonify, request, make_response
from controller.get_branch import *
from controller.post_patient import *
from controller.post_appointment import *
from controller.get_appointment import *
from controller.post_employee import *
from controller.get_procedure import *
from api_exceptions import *

"""
Dental Clinic Management System (DCMS) API

    - GET: returns all items in the DB
        - if successful, status code: 200 (OK)
        - if no items are found, returns and empty payload, status code: 404 (NOT FOUND)
        
    - POST: creates and adds items to the DB, generates item ID
        - if successful, status code: 201 (CREATED)
        - if information in payload is missing, status code: 406 (NOT ACCEPTABLE)
        - if item already exists in DB, status code: 406 (NOT ACCEPTABLE)
        - if schema error, return 400 (BAD REQUEST)
        
    - PUT: modifies an item in the DB given an item ID
        - if successful, status code: 200 (OK)
        - if item not found, status code: 404 (NOT FOUND)
        - if information in payload is missing, status code: 406 (NOT ACCEPTABLE)
        - if schema error, return 400 (BAD REQUEST)
        
    - DELETE: deletes an item from the DB given an item ID
        - if successful, status code: 200 (OK)
        - if item not found, status code: 404 (NOT FOUND)
"""


@app.route('/api/branches', methods=['GET'])
def branch_api():
    # http://127.0.0.1:5000/api/branches
    if request.method == 'GET':
        branches = get_all_branches() #[[branch_id1, branch_location1], [branch_id2, branch_location2], []...]
        response = make_response(jsonify(branches), 200)
        return response

@app.route('/api/procedures', methods=['GET'])
def procedure_api():
    # http://127.0.0.1:5000/api/procedures
    if request.method == 'GET':
        procedures = get_all_procedures() #[[branch_id1, branch_location1], [branch_id2, branch_location2], []...]
        response = make_response(jsonify(procedures), 200)
        return response


@app.route('/api/dentists/<branch_id>', methods=['GET'])
def dentist_api(branch_id):
    if request.method == 'GET':
        dentists = get_all_dentists_from_branch(branch_id)
        response = make_response(jsonify(dentists), 200)
        return response

@app.route('/api/appointments/<employee_id>', methods=['GET'])
def upcoming_appointment_api(employee_id):
    if request.method == 'GET':
        appointment = get_upcoming_appointment(employee_id)
        response = make_response(jsonify(appointment), 200)
        return response

@app.route('/api/patients', methods=['POST'])
def patient_api():
    # http://127.0.0.1:5000/api/branches
    if request.method == 'POST':
        data = request.get_json()
        try:
            response = post_patient(data)
            if response['status_code'] == 201:
                return jsonify({
                    'message': response['message']
                }), response['status_code']
            elif response['status_code'] == 400:
                return jsonify({'message': response['message']}), 400
            elif response['status_code'] == 406:
                return jsonify({'message': response['message']}), 406
        except ApiException as e:
            return jsonify({'message': str(e)}), 406

@app.route('/api/employees', methods=['POST'])
def employee_api():
    # http://127.0.0.1:5000/api/employees
    if request.method == 'POST':
        data = request.get_json()
        try:
            response = post_employee(data)
            if response['status_code'] == 201:
                return jsonify({
                    'message': response['message']
                }), response['status_code']
            elif response['status_code'] == 400:
                return jsonify({'message': response['message']}), 400
            elif response['status_code'] == 406:
                return jsonify({'message': response['message']}), 406
        except ApiException as e:
            return jsonify({'message': str(e)}), 406


@app.route('/api/appointments', methods=['POST'])
def appointment_api():
    # http://127.0.0.1:5000/api/appointment
    if request.method == 'POST':
        data = request.get_json()
        try:
            response = post_appointment(data)
            if response['status_code'] == 201:
                return jsonify({
                    'message': response['message']
                }), response['status_code']
            elif response['status_code'] == 400:
                return jsonify({'message': response['message']}), 400
            elif response['status_code'] == 406:
                return jsonify({'message': response['message']}), 406
        except ApiException as e:
            return jsonify({'message': str(e)}), 406
#
# @app.route('/api/items/<item_id>', methods=['GET', 'PUT', 'DELETE'])
# def item_id_api(item_id):
#     if request.method == 'GET':
#         response = get_item_by_id(item_id)
#         if response['status_code'] == 200:
#             return jsonify(response['message']), response['status_code']
#         else:
#             return jsonify({'message': response['message']}), 400


@app.route('/api/test/items', methods=['GET'])
def test_item_api():
    return jsonify({'message': 'Item API is up and running.'}), 200
