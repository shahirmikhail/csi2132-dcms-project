import boto3
from boto3.dynamodb.conditions import Key
from datetime import datetime

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('inventory')


def put_item(payload, item_id):
    now = datetime.now()
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")

    name = payload["name"]
    quantity = payload["quantity"]
    in_stock = payload["in_stock"]
    date_created = payload["date_created"]
    date_updated = dt_string

    response = table.scan(**{'FilterExpression': Key('id').eq(item_id)})
    inventory_list = response['Items']

    if len(inventory_list) != 0:
        table.delete_item(
            Key={
                "id": item_id,
            }
        )
        if 'collection' in payload.keys():
            collection = payload["collection"]
            table.put_item(
                Item={
                    "name": name,
                    "collection": collection,
                    "quantity": quantity,
                    "in_stock": in_stock,
                    "date_created": date_created,
                    "date_updated": date_updated,
                    "id": item_id
                }
            )
        else:
            table.put_item(
                Item={
                    "name": name,
                    "quantity": quantity,
                    "in_stock": in_stock,
                    "date_created": date_created,
                    "date_updated": date_updated,
                    "id": item_id
                }
            )
        return {"message": 'Item updated successfully', "status_code": 200}
    elif len(inventory_list) == 0:
        return {"message": 'Item not found.', "status_code": 404}
