from unittest import mock, TestCase
import boto3
from Lambda.dynamo_helper import update_table, get_count, lambda_handler

class TestLambdaFunction(TestCase):
    @mock.patch('boto3.resource')
    def test_update_table(self, mock_resource):
        mock_table = mock.MagicMock()
        mock_table.update_item.return_value = {"ResponseMetadata": {"HTTPStatusCode": 200}}
        mock_resource.return_value.Table.return_value = mock_table
        table_name = 'test_table'
        pk = 'my_pk'
        column = 'my_column'
        update_table(table_name, pk, column)
        mock_resource.assert_called_with('dynamodb')
        mock_resource.return_value.Table.assert_called_with(table_name)
        mock_table.update_item.assert_called_once_with(
            Key={pk: 1},
            UpdateExpression='ADD ' + column + ' :incr',
            ExpressionAttributeValues={':incr': 1}
        )

    @mock.patch('boto3.resource')
    def test_get_count(self, mock_resource):
        mock_table = mock.MagicMock()
        mock_response = {'Item': {'my_column': 42}}
        mock_table.get_item.return_value = mock_response
        mock_resource.return_value.Table.return_value = mock_table
        table_name = 'test_table'
        pk = 'my_pk'
        column = 'my_column'
        result = get_count(table_name, pk, column)
        mock_resource.assert_called_with('dynamodb')
        mock_resource.return_value.Table.assert_called_with(table_name)
        mock_table.get_item.assert_called_once_with(Key={pk: 1})
        self.assertEqual(result, 42)

    @mock.patch('dynamo_helper.update_table')
    @mock.patch('dynamo_helper.get_count')
    def test_lambda_handler(self, mock_get_count, mock_update_table):
        mock_get_count.return_value = 42
        event = {}
        context = mock.MagicMock()
        result = lambda_handler(event, context)
        mock_update_table.assert_called_once_with('Visitors', 'VisitorCount', 'vc')
        mock_get_count.assert_called_once_with('Visitors', 'VisitorCount', 'vc')
        self.assertEqual(result['statusCode'], 200)
        self.assertEqual(result['body'], '42')