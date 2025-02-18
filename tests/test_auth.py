from unittest import TestCase
from api import create_app
from api.extensions import db

class AuthTestCase(TestCase):
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

    def test_register_successful(self):
        response = self.client.post("/auth/register", json={
            "username": "goodusername123",
            "email": "validemail123@gmail.com",
            "password": "goodpassword123"
        })

        self.assertEqual(response.status_code, 201, "User should be registered successfully")
    
    def test_register_incomplete_fail(self):
        response = self.client.post("/auth/register", json={
            "username": "incompleteusername123",
            "password": "incompletepassword123"
        })

        self.assertEqual(response.status_code, 400, "Registration should fail when username, email, or password is missing")

    def test_register_username_already_exists_fail(self):
        self.client.post("/auth/register", json={
            "username": "alreadyexistingusername123",
            "email": "validemail123@gmail.com",
            "password": "alreadyexistingpassword123"
        })

        response = self.client.post("/auth/register", json={
            "username": "alreadyexistingusername123",
            "email": "validemail123@gmail.com",
            "password": "alreadyexistingpassword123"
        })

        self.assertEqual(response.status_code, 409, "Registration should fail when username already exists")
    
    def test_login_successful(self):
        self.client.post("/auth/register", json={
            "username": "goodloginusername123",
            "email": "validemail123@gmail.com",
            "password": "goodpassword123"
        })

        response = self.client.post("/auth/login", json={
            "username": "goodloginusername123",
            "password": "goodpassword123"
        })

        self.assertEqual(response.status_code, 200)
        self.assertIn("access_token", response.get_json(), "Login should return a valid JWT token")
    
    def test_login_doesnt_exist_fail(self):
        response = self.client.post("/auth/login", json={
            "username": "loginnotexistingusername123",
            "password": "goodpassword123"
        })

        self.assertEqual(response.status_code, 401, "Login should fail when username doesn't exist")
    
    def test_login_bad_password_fail(self):
        self.client.post("/auth/register", json={
            "username": "badpasswordusername123",
            "email": "validemail123@gmail.com",
            "password": "password123"
        })

        response = self.client.post("/auth/login", json={
            "username": "badpasswordusername123",
            "password": "password456"
        })

        # print(response.data.decode())

        self.assertEqual(response.status_code, 401, "Login should fail when the password doesn't match the hashed password in the database")

