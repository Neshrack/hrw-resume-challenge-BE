import boto3
import unittest
from unittest.mock import MagicMock

class TestLambdaFunction(unittest.TestCase):

    def test_lambda_handler(self):
        # Mock the DynamoDB table
        table_mock = MagicMock()
        table_mock.get_item.return_value = {
            'Item': {
                'VisitorCount': '0'
            }
        }
        dynamodb_mock = MagicMock()
        dynamodb_mock.Table.return_value = table_mock
        boto3.resource = MagicMock(return_value=dynamodb_mock)

        # Call the lambda function
        from dynamo_helper import lambda_handler
        response = lambda_handler(None, None)

        # Check the response body and DynamoDB table
        expected_body = f'View count updated successfully. Total visitors: 1'
        self.assertEqual(response['body'], expected_body)
        table_mock.put_item.assert_called_with(Item={'VisitorCount': '1'})