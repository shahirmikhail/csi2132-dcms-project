import boto3
from boto3.dynamodb.conditions import Key

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('inventory')


def get_all_items():
    response = table.scan()
    inventory_list = response['Items']
    return inventory_list


def get_item_by_id(item_id):
    response = table.scan(**{'FilterExpression': Key('id').eq(item_id)})
    inventory_list = response['Items']
    if len(inventory_list) != 0:
        return {"message": inventory_list, "status_code": 200}
    else:
        return {"message": "Item not found.", "status_code": 404}


def get_item_by_collection(collection):
    response = table.scan(**{'FilterExpression': Key('collection').eq(collection)})
    inventory_list = response['Items']
    if len(inventory_list) != 0:
        return {"message": inventory_list, "status_code": 200}
    else:
        return {"message": "No items found in this collection.", "status_code": 404}
