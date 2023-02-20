import boto3

def lambda_handler(event, context):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('Visitors')

    response = table.update_item(
        Key={
            'VisitorCount': 'vc'
        },
        UpdateExpression='SET VisitorCount = VisitorCount + :val',
        ExpressionAttributeValues={
            ':val': 1
        }
    )

    total_visitors = table.get_item(
        Key={
            'VisitorCount': 'vc'
        }
    )['Item']['VisitorCount']

    return {
        'statusCode': 200,
        'body': f'View count updated successfully. Total visitors: {total_visitors}'
    }