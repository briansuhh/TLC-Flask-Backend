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
            for table in reversed(db.metadata.sorted_tables):
                db.session.execute(table.delete())
            db.session.commit()            

    def test_register_successful(self):
        response = self.client.post("/auth/register", json={
            "username": "goodusername123",
            "first_name": "Good",
            "middle_name": "User",
            "last_name": "Name",
            "birth_date": "2000-01-01",
            "sex": "M",
            "position": "User",
            "email": "validemail123@gmail.com",
            "password": "goodpassword123"
        })

        self.assertEqual(response.status_code, 201, "User should be registered successfully")
    
    def test_register_incomplete_fail(self):
        response = self.client.post("/auth/register", json={
            "username": "incompleteusername123",
            "password": "incompletepassword123"
        })

        self.assertEqual(response.status_code, 400, "Registration should fail when required fields are missing")

    def test_register_email_already_exists_fail(self):
        self.client.post("/auth/register", json={
            "username": "uniqueuser",
            "first_name": "Unique",
            "middle_name": "User",
            "last_name": "Test",
            "birth_date": "1999-05-05",
            "sex": "F",
            "position": "Admin",
            "email": "duplicateemail@gmail.com",
            "password": "securepass"
        })

        response = self.client.post("/auth/register", json={
            "username": "anotheruser",
            "first_name": "Another",
            "middle_name": "User",
            "last_name": "Test",
            "birth_date": "2001-07-07",
            "sex": "M",
            "position": "User",
            "email": "duplicateemail@gmail.com",
            "password": "securepass"
        })

        self.assertEqual(response.status_code, 409, "Registration should fail when email already exists")
    
    def test_login_successful(self):
        self.client.post("/auth/register", json={
            "username": "goodloginusername123",
            "first_name": "Good",
            "middle_name": "Login",
            "last_name": "User",
            "birth_date": "1998-03-03",
            "sex": "M",
            "position": "User",
            "email": "validemail123@gmail.com",
            "password": "goodpassword123"
        })

        response = self.client.post("/auth/login", json={
            "email": "validemail123@gmail.com",
            "password": "goodpassword123"
        })

        self.assertEqual(response.status_code, 200)
        self.assertIn("access_token", response.get_json(), "Login should return a valid JWT token")
        print(response.get_json())
    
    def test_login_doesnt_exist_fail(self):
        response = self.client.post("/auth/login", json={
            "email": "nonexistentemail@gmail.com",
            "password": "randompassword"
        })

        self.assertEqual(response.status_code, 401, "Login should fail when email doesn't exist")
    
    def test_login_bad_password_fail(self):
        self.client.post("/auth/register", json={
            "username": "badpasswordusername123",
            "first_name": "Bad",
            "middle_name": "Password",
            "last_name": "User",
            "birth_date": "2002-09-09",
            "sex": "F",
            "position": "User",
            "email": "validemail123@gmail.com",
            "password": "correctpassword"
        })

        response = self.client.post("/auth/login", json={
            "email": "validemail123@gmail.com",
            "password": "wrongpassword"
        })

        self.assertEqual(response.status_code, 401, "Login should fail when the password is incorrect")
