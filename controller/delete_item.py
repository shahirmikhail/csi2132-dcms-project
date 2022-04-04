import boto3
from boto3.dynamodb.conditions import Key


dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('inventory')


def delete_item(item_id):
    response = table.scan(**{'FilterExpression': Key('id').eq(item_id)})
    item_list = response['Items']
    if len(item_list) != 0:
        table.delete_item(
            Key={
                "id": item_id
            }
        )
        return {"message": 'Item deleted successfully', "status_code": 200}
    else:
        return {"message": 'Item not found.', "status_code": 404}
