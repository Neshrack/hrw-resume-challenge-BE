import unittest
from unittest.mock import MagicMock
from dynamo_helper import update_table, get_count

class TestMyModule(unittest.TestCase):

    def setUp(self):
        self.table_name = 'Visitors'
        self.pk = 'VisitorCount'
        self.column = 'vc'
        self.dynamo_client = MagicMock()
        self.table = MagicMock()
        self.dynamo_client.Table.return_value = self.table

    def test_update_table(self):
        self.table.update_item.return_value = {'ResponseMetadata': {'HTTPStatusCode': 200}}
        update_table(self.table_name, self.pk, self.column)
        self.table.update_item.assert_called_with(
            Key={self.pk: 1},
            UpdateExpression='ADD ' + self.column + ' :incr',
            ExpressionAttributeValues={':incr': 1}
        )

    def test_get_count(self):
        self.table.get_item.return_value = {'Item': {self.column: 10}}
        count = get_count(self.table_name, self.pk, self.column)
        self.table.get_item.assert_called_with(Key={self.pk: 1})
        self.assertEqual(count, 10)

if __name__ == '__main__':
    unittest.main()