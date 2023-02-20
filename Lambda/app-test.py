import unittest
from unittest.mock import Mock
from dynamo_helper import lambda_handler

class TestLambdaFunction(unittest.TestCase):

    def test_lambda_handler(self):
        # Create a mock DynamoDB client and table
        table_mock = Mock()
        table_mock.update_item.return_value = {"ResponseMetadata": {"HTTPStatusCode": 200}}
        table_mock.get_item.return_value = {"Item": {"vc": 42}}

        # Call the Lambda function with some sample event data and the mock DynamoDB table
        event = {}
        context = Mock()
        result = lambda_handler(event, context, table=table_mock)

        # Verify that the DynamoDB `update_item` and `get_item` methods were called once with the correct parameters
        table_mock.update_item.assert_called_once_with(
            Key={"VisitorCount": 1},
            UpdateExpression="ADD vc :incr",
            ExpressionAttributeValues={":incr": 1}
        )
        table_mock.get_item.assert_called_once_with(Key={"VisitorCount": 1})

        # Verify that the Lambda function returned a successful response with the correct visitor count
        self.assertEqual(result["statusCode"], 200)
        self.assertEqual(result["body"], "42")

if __name__ == '__main__':
    unittest.main()