from app import app
from flask import jsonify, request, make_response
from controller.get_item import *
from controller.post_item import *
from controller.put_item import *
from controller.delete_item import *
from api_exceptions import *
from controller.validations import Validations

"""
Inventory API
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


@app.route('/api/items', methods=['POST', 'GET'])
def inventory_api():
    if request.method == 'GET':
        collection = request.args.get('collection')
        if collection is not None:
            items = get_item_by_collection(collection)
            response = make_response(jsonify(items), 200)
            return response
        items = get_all_items()
        response = make_response(jsonify(items), 200)
        return response

    if request.method == 'POST':
        data = request.get_json()
        try:
            validation = Validations(data)

            validation.validate_payload()
            error_messages = validation.get_error_messages()
            if not(len(error_messages["Validation Error"]) == 0):
                return jsonify({'message': validation.error_messages}), 406

            validation.validate(data)
            error_messages = validation.get_error_messages()
            if not(len(error_messages["Validation Error"]) == 0):
                return jsonify({'message': validation.error_messages}), 406

            response = post_items(data)
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


@app.route('/api/items/<item_id>', methods=['GET', 'PUT', 'DELETE'])
def item_id_api(item_id):
    if request.method == 'GET':
        response = get_item_by_id(item_id)
        if response['status_code'] == 200:
            return jsonify(response['message']), response['status_code']
        else:
            return jsonify({'message': response['message']}), 400

    if request.method == 'PUT':
        data = request.get_json()
        try:
            validation = Validations(data)

            validation.validate_payload_put()
            error_messages = validation.get_error_messages()
            if not (len(error_messages["Validation Error"]) == 0):
                return jsonify({'message': validation.error_messages}), 406

            validation.validate_put(data, item_id)
            error_messages = validation.get_error_messages()
            if not (len(error_messages["Validation Error"]) == 0):
                return jsonify({'message': validation.error_messages}), 406

            response = put_item(data, item_id)
            if response['status_code'] == 200:
                return jsonify({
                    'message': response['message']
                }), response['status_code']
            elif response['status_code'] == 404:
                return jsonify({'message': response['message']}), 404
            elif response['status_code'] == 400:
                return jsonify({'message': response['message']}), 400
            elif response['status_code'] == 406:
                return jsonify({'message': response['message']}), 406
        except ApiException as e:
            return jsonify({'message': str(e)}), 406

    if request.method == 'DELETE':
        try:
            response = delete_item(item_id)
            if response['status_code'] == 200:
                return jsonify({
                    'message': response['message']
                }), response['status_code']
            elif response['status_code'] == 404:
                return jsonify({'message': response['message']}), 404
        except ApiException as e:
            return jsonify({'message': str(e)}), 404


@app.route('/api/test/items', methods=['GET'])
def test_item_api():
    return jsonify({'message': 'Item API is up and running.'}), 200
