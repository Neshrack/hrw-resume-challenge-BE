import boto3
dynamo_client = boto3.resource('dynamodb')

def update_table(table, pk, column):
    table = dynamo_client.Table(table)
    response = table.update_item(
        Key={pk: 1},
        UpdateExpression='ADD ' + column + ' :incr',
        ExpressionAttributeValues={':incr': 1}
    )

    print(response)

def get_count(table, pk, column):
    dynamodb = boto3.resource('dynamodb')
    table = dynamo_client.Table(table)
    response = table.get_item(
            Key={pk: 1}
        )
    count = response['Item'][column]
    return(count)

def lambda_handler(event, context):
    update_table('Visitors', 'VisitorCount', 'vc')
    get_count('Visitors', 'VisitorCount', 'vc')



    return {
    'statusCode': 200,
    'headers': { "Access-Control-Allow-Origin": "*" },
    'body': get_count('Visitors', 'VisitorCount', 'vc')

    }