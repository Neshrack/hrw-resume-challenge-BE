import unittest
from unittest.mock import MagicMock
import Lambda.dynamo_helper # assuming the lambda function is named lambda_function.py

class TestLambdaFunction(unittest.TestCase):

    def test_increase_view_count(self):
        # set up a mock DynamoDB client
        dynamodb_client_mock = MagicMock()
        lambda_function.dynamodb_client = dynamodb_client_mock
        
        # invoke the Lambda function
        lambda_function.lambda_handler(None, None)
        
        # verify that the update_item method was called with the correct parameters
        dynamodb_client_mock.update_item.assert_called_once_with(
            TableName='Visitors',
            Key={'table_id': {'S': '1'}},
            UpdateExpression='ADD VisitorCount :val',
            ExpressionAttributeValues={':val': {'N': '1'}}
        )

if __name__ == '__main__':
    unittest.main()
