import boto3
dynamo_client = boto3.resource('dynamodb')

import boto3

dynamo_client = boto3.resource('dynamodb')

def update_table(table_name, pk, column):
    table = dynamo_client.Table(table_name)
    response = table.update_item(
        Key={pk: 1},
        UpdateExpression='ADD ' + column + ' :incr',
        ExpressionAttributeValues={':incr': 1}
    )
    return response

def get_count(table_name, pk, column):
    table = dynamo_client.Table(table_name)
    response = table.get_item(Key={pk: 1})
    count = response['Item'][column]
    return count


def lambda_handler(event, context):
    update_response = update_table('Visitors', 'VisitorCount', 'vc')
    count = get_count('Visitors', 'VisitorCount', 'vc')

    return {
        'statusCode': 200,
        'headers': { 
            "Access-Control-Allow-Headers": "*",
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "GET",  # Allow only GET request
        },
        'body': count
    }