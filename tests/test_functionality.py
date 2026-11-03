import unittest
from app import create_app


class CatalogTests(unittest.TestCase):
    def setUp(self):
        self.client = create_app().test_client()

    def test_health(self):
        self.assertEqual(self.client.get('/health').json, {'status': 'ok'})

    def test_search_routes(self):
        for route in ('search', 'filter'):
            with self.subTest(route=route):
                response = self.client.get('/products/' + route, query_string={'q': 'Mouse'})
                self.assertEqual(response.status_code, 200)
                self.assertEqual(response.json, [{'id': 2, 'name': 'Mouse', 'price': 15}])

    def test_empty_search(self):
        for route in ('search', 'filter'):
            self.assertEqual(len(self.client.get('/products/' + route).json), 3)

    def test_no_match(self):
        for route in ('search', 'filter'):
            self.assertEqual(self.client.get('/products/' + route, query_string={'q': 'Laptop'}).json, [])

    def test_download(self):
        with self.client.get('/files/download?name=welcome.txt') as response:
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'Synthetic catalog', response.data)

    def test_missing_file(self):
        self.assertEqual(self.client.get('/files/download?name=missing.txt').status_code, 404)


if __name__ == '__main__':
    unittest.main()
