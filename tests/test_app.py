import unittest
from app import app

class TestApp(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()

    def test_hello(self):
        response = self.app.get('/hello')
        self.assertEqual(response.data, b'Hello, Jenkins and SonarQube!')

if __name__ == '__main__':
    unittest.main()
