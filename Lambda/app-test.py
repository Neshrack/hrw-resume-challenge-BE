import unittest
from unittest.mock import Mock, patch
import boto3
from botocore.exceptions import ClientError
from dynamo_helper import update_table, get_count

# Define a mock DynamoDB resource
mock_dynamodb = Mock()

class TestUpdateTable(unittest.TestCase):
    def setUp(self):
        self.mock_table = mock_dynamodb.Table('test_table')
        self.mock_table.update_item = Mock(return_value={'Attributes': {'column': 2}})

    @patch('boto3.resource', return_value=mock_dynamodb)
    def test_update_table(self, mock_resource):
        update_table('test_table', 'pk', 'column')
        self.mock_table.update_item.assert_called_once_with(
            Key={'pk': 1},
            UpdateExpression='ADD column :incr',
            ExpressionAttributeValues={':incr': 1}
        )

class TestGetCount(unittest.TestCase):
    def setUp(self):
        self.mock_table = mock_dynamodb.Table('test_table')
        self.mock_table.get_item = Mock(return_value={'Item': {'column': 2}})

    @patch('boto3.resource', return_value=mock_dynamodb)
    def test_get_count(self, mock_resource):
        count = get_count('test_table', 'pk', 'column')
        self.assertEqual(count, 2)
        self.mock_table.get_item.assert_called_once_with(Key={'pk': 1})

if __name__ == '__main__':
    unittest.main()
