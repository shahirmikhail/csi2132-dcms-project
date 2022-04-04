from datetime import datetime


class Validations:

    def __init__(self, payload=None):
        self.payload = payload
        self.error_messages = {"Validation Error": []}
        self.keys_list = payload.keys()

    def validate_payload(self):
        # if 'collection' not in self.keys_list:
        #     error_message = {"Field": "collection", "Message": "Missing field."}
        #     self.error_messages["Validation Error"].append(error_message)
        if 'name' not in self.keys_list:
            error_message = {"Field": "name", "Message": "Missing field."}
            self.error_messages["Validation Error"].append(error_message)
        if 'quantity' not in self.keys_list:
            error_message = {"Field": "quantity", "Message": "Missing field."}
            self.error_messages["Validation Error"].append(error_message)
        if 'in_stock' not in self.keys_list:
            error_message = {"Field": "in_stock", "Message": "Missing field."}
            self.error_messages["Validation Error"].append(error_message)

    def validate_payload_put(self):
        # if 'collection' not in self.keys_list:
        #     error_message = {"Field": "collection", "Message": "Missing field."}
        #     self.error_messages["Validation Error"].append(error_message)
        if 'name' not in self.keys_list:
            error_message = {"Field": "name", "Message": "Missing field."}
            self.error_messages["Validation Error"].append(error_message)
        if 'quantity' not in self.keys_list:
            error_message = {"Field": "quantity", "Message": "Missing field."}
            self.error_messages["Validation Error"].append(error_message)
        if 'in_stock' not in self.keys_list:
            error_message = {"Field": "in_stock", "Message": "Missing field."}
            self.error_messages["Validation Error"].append(error_message)
        if 'date_created' not in self.keys_list:
            error_message = {"Field": "date_created", "Message": "Missing field."}
            self.error_messages["Validation Error"].append(error_message)
        if 'id' not in self.keys_list:
            error_message = {"Field": "id", "Message": "Missing field."}
            self.error_messages["Validation Error"].append(error_message)

    def validate(self, payload):
        name = payload["name"]
        # collection = payload["collection"]
        quantity = payload["quantity"]
        in_stock = payload["in_stock"]

        self.validate_empty_field(name, "name")
        # self.validate_empty_field(collection, "collection")
        self.validate_empty_field(quantity, "quantity")
        self.validate_empty_field(in_stock, "in_stock")

        self.validate_string(name, "name")
        # self.validate_string(collection, "collection")

        # self.validate_collection(collection)
        self.validate_name(name)
        self.validate_quantity(quantity)
        self.validate_in_stock(in_stock)

    def validate_put(self, payload, uri_id):
        name = payload["name"]
        # collection = payload["collection"]
        quantity = payload["quantity"]
        in_stock = payload["in_stock"]
        date_created = payload["date_created"]
        id = payload["id"]

        self.validate_empty_field(name, "name")
        # self.validate_empty_field(collection, "collection")
        self.validate_empty_field(quantity, "quantity")
        self.validate_empty_field(in_stock, "in_stock")
        self.validate_empty_field(date_created, "date_created")
        self.validate_empty_field(id, "id")

        self.validate_string(name, "name")
        # self.validate_string(collection, "collection")
        self.validate_string(date_created, "date_created")
        self.validate_string(id, "id")

        # self.validate_collection(collection)
        self.validate_name(name)
        self.validate_quantity(quantity)
        self.validate_in_stock(in_stock)
        self.validate_date(date_created, "date_created")
        self.validate_item_id(id, uri_id)

    def validate_name(self, name):
        self.validate_alphanumeric(name, "name")
        self.validate_string_length_min(name, "name")
        self.validate_string_length_max(name, "name")
        return None

    def validate_collection(self, collection):
        self.validate_alphanumeric(collection, "collection")
        self.validate_string_length_min(collection, "collection")
        self.validate_string_length_max(collection, "collection")
        return None

    def validate_quantity(self, quantity):
        self.validate_number(quantity, "quantity")
        return None

    def validate_in_stock(self, in_stock):
        self.validate_boolean(in_stock, "in_stock")
        return None

    def validate_item_id(self, payload_id, uri_id):
        if payload_id != uri_id:
            error_message = {"Field": "id", "Message": "Id from uri does not match the one from the payload."}
            self.error_messages["Validation Error"].append(error_message)
        return None

    def validate_empty_field(self, field, field_name):
        if field == "":
            error_message = {"Field": field_name, "Message": "Empty field."}
            self.error_messages["Validation Error"].append(error_message)

    def validate_date(self, date, date_name):
        date_format = "%d/%m/%Y %H:%M:%S"
        try:
            datetime.strptime(date, date_format)
        except ValueError:
            error_message = {"Field": date_name, "Message": "Wrong date format."}
            self.error_messages["Validation Error"].append(error_message)
        return None

    def validate_string(self, field, field_name):
        if not (type(field) == str):
            error_message = {"Field": field_name, "Message": "Field must be a string."}
            self.error_messages["Validation Error"].append(error_message)

    def validate_number(self, field, field_name):
        if not (type(field) == int):
            error_message = {"Field": field_name, "Message": "Field must be an integer."}
            self.error_messages["Validation Error"].append(error_message)

    def validate_boolean(self, field, field_name):
        if not (type(field) == bool):
            error_message = {"Field": field_name, "Message": "Field must be a boolean."}
            self.error_messages["Validation Error"].append(error_message)

    def validate_alphanumeric(self, field, field_name):
        is_alphanumeric = True
        string_list = field.split(" ")
        for elem in string_list:
            if elem.isalnum() is False:
                is_alphanumeric = False
        if is_alphanumeric is False:
            error_message = {"Field": field_name, "Message": "Field must be alphanumeric."}
            self.error_messages["Validation Error"].append(error_message)

    def validate_string_length_min(self, field, field_name):
        if len(field) < 3:
            error_message = {"Field": field_name, "Message": "Field must contain at least 3 characters."}
            self.error_messages["Validation Error"].append(error_message)

    def validate_string_length_max(self, field, field_name):
        if len(field) > 37:
            error_message = {"Field": field_name, "Message": "Field must contain less than 37 characters."}
            self.error_messages["Validation Error"].append(error_message)

    def validate_missing_field(self, field, field_name):
        if field not in self.keys_list:
            error_message = {"Field": field_name, "Message": "Missing field."}
            self.error_messages["Validation Error"].append(error_message)

    def get_error_messages(self):
        return self.error_messages
