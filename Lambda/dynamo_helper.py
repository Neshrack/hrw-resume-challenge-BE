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
    
    return {
        'statusCode': 200,
        'body': 'View count updated successfully'
    }