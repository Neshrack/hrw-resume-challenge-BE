import unittest
from unittest.mock import MagicMock
from dynamo_helper import update_table, get_count

class TestMyModule(unittest.TestCase):
    
    def setUp(self):
        # create a mock dynamodb table object
        self.table = MagicMock()
        # set up mock response for table.get_item()
        self.table.get_item.return_value = {'Item': {'vc': 1}}
        # set up mock response for table.update_item()
        self.table.update_item.return_value = 'Success'
        # patch dynamo_client.Table() with the mock table
        self.patcher = patch('lambda_function.dynamo_client.Table', return_value=self.table)
        self.patcher.start()

    def tearDown(self):
        # stop patching dynamo_client.Table()
        self.patcher.stop()

    def test_update_table(self):
        update_table('Visitors', 'VisitorCount', 'vc')
        self.table.update_item.assert_called_with(
            Key={'VisitorCount': 1},
            UpdateExpression='ADD vc :incr',
            ExpressionAttributeValues={':incr': 1}
        )

    def test_get_count(self):
        count = get_count('Visitors', 'VisitorCount', 'vc')
        self.table.get_item.assert_called_with(Key={'VisitorCount': 1})
        self.assertEqual(count, 1)


class TestLambdaFunction(unittest.TestCase):

    def test_visitor_count(self):
        old_count = get_count('Visitors', 'VisitorCount', 'vc')
        update_table('Visitors', 'VisitorCount', 'vc')
        new_count = get_count('Visitors', 'VisitorCount', 'vc')
        self.assertGreater(new_count, old_count)

if __name__ == '__main__':
    unittest.main()