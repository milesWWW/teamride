import unittest
from unittest.mock import patch
from wxcloudrun import app

class TestViews(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()

    @patch('wxcloudrun.dao.query_counterbyid')
    def test_get_count(self, mock_query):
        # 测试获取计数
        mock_query.return_value = None
        response = self.app.get('/api/count')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['data'], 0)

    @patch('wxcloudrun.dao.insert_counter')
    def test_post_count_inc(self, mock_insert):
        # 测试自增计数
        response = self.app.post('/api/count', json={'action': 'inc'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['data'], 1)

    @patch('wxcloudrun.dao.delete_counterbyid')
    def test_post_count_clear(self, mock_delete):
        # 测试清0计数
        response = self.app.post('/api/count', json={'action': 'clear'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['data'], None)

if __name__ == '__main__':
    unittest.main()