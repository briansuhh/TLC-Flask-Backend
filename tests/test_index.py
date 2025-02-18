from unittest import TestCase
from api import create_app
from api.extensions import db


class TestApp(TestCase):
    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()
        self.app.testing = True

        with self.app.app_context():
            db.create_all()
    
    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def test_app_running(self):
        """
        Tests the route screen message
        """
        response = self.client.get('/')

        self.assertEqual({"message": "Hello, Flask!"}, response.get_json())
