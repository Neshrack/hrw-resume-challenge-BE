import unittest
import boto3
import json
import os
from botocore.exceptions import ClientError

def lambda_handler(event, context):
    dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
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

class TestLambdaHandler(unittest.TestCase):

    def test_increment_visitor_count(self):
        # Set up a mock DynamoDB table
        dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
        if 'Visitors' in dynamodb.tables.all():
            table = dynamodb.Table('Visitors')
        else:
            table = dynamodb.create_table(
            TableName='Visitors',
            KeySchema=[
                {
                    'AttributeName': 'VisitorCount',
                    'KeyType': 'HASH'
                }
            ],
            AttributeDefinitions=[
                {
                    'AttributeName': 'VisitorCount',
                    'AttributeType': 'N'
                }
            ],
            BillingMode='PAY_PER_REQUEST'
        )
        table.put_item(Item={'VisitorCount': 'vc', 'Visitors': 0})

        # Invoke the Lambda function
        response = lambda_handler({}, {})

        # Verify the response
        self.assertEqual(response['statusCode'], 200)
        self.assertTrue('Total visitors' in response['body'])