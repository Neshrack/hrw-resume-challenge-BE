import boto3
import unittest
from moto import mock_dynamodb2

class TestLambdaFunction(unittest.TestCase):

    @mock_dynamodb2
    def test_lambda_handler(self):
        # Setup the mock DynamoDB table
        dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
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
                    'AttributeType': 'S'
                }
            ],
            ProvisionedThroughput={
                'ReadCapacityUnits': 5,
                'WriteCapacityUnits': 5
            }
        )
        
        # Call the lambda function
        from dynamo_helper import lambda_handler
        response = lambda_handler(None, None)
        
        # Check the response body and DynamoDB table
        expected_body = f'View count updated successfully. Total visitors: 1'
        self.assertEqual(response['body'], expected_body)
        self.assertEqual(table.get_item(Key={'VisitorCount': 'vc'})['Item']['