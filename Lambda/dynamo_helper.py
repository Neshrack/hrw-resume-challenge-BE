import boto3

dynamo_client = boto3.resource('dynamodb')
table_name = 'Visitors'
pk = 'VisitorCount'
column = 'vc'

def update_table():
    table = dynamo_client.Table(table_name)
    response = table.update_item(
        Key={pk: 1},
        UpdateExpression='ADD ' + column + ' :incr',
        ExpressionAttributeValues={':incr': 1}
    )

    print(response)

def get_count():
    table = dynamo_client.Table(table_name)
    response = table.get_item(
        Key={pk: 1}
    )
    count = response['Item'][column]
    return count

def lambda_handler(event, context):
    update_table()
    count = get_count()

    return {
        'statusCode': 200,
        'headers': { 
            "Access-Control-Allow-Headers": "*",
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "GET",  # Allow only GET request
        },
        'body': str(count)
    }