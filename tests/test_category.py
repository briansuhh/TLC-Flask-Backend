from unittest import TestCase
from api import create_app
from api.extensions import db
import json

class CategoryTestCase(TestCase):
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

    def _register_and_login(self):
        """Helper function to register and login a test user."""
        # Register a test user
        register_response = self.client.post("/auth/register", json={
            "username": "Testing",
            "first_name": "Tes",
            "middle_name": "T.",
            "last_name": "Ing",
            "birth_date": "1990-01-15",
            "sex": "M",
            "position": "Cashier",
            "email": "cashier@gmail.com",
            "password": "password"
        })
        
        if register_response.status_code != 201:
            raise ValueError(f"Registration failed: {register_response.data}")
        
        # Login and get token
        login_response = self.client.post("/auth/login", json={
            "email": "cashier@gmail.com",
            "password": "password"
        })
        
        login_data = json.loads(login_response.data)
        
        if login_response.status_code != 200 or 'access_token' not in login_data:
            raise ValueError(f"Login failed: {login_data}")
            
        return f"Bearer {login_data['access_token']}"

    def test_create_category_successful(self):
        try:
            auth_header = {"Authorization": self._register_and_login()}
            response = self.client.post("/categories/", 
                json={"name": "Main Meals"},
                headers=auth_header
            )
            self.assertEqual(response.status_code, 201, "Category should be created successfully")
        except ValueError as e:
            self.fail(str(e))

    def test_create_category_unauthorized(self):
        response = self.client.post("/categories/", 
            json={"name": "Main Meals"}
        )
        self.assertIn(response.status_code, [400, 401], "Should fail without authentication")

    def test_create_category_incomplete_fail(self):
        try:
            auth_header = {"Authorization": self._register_and_login()}
            response = self.client.post("/categories/", 
                json={"name": ""},
                headers=auth_header
            )
            self.assertEqual(response.status_code, 400, "Category creation should fail when required fields are missing")
        except ValueError as e:
            self.fail(str(e))

    def test_create_category_duplicate_fail(self):
        try:
            auth_header = {"Authorization": self._register_and_login()}
            self.client.post("/categories/", 
                json={"name": "Main Meals"},
                headers=auth_header
            )
            
            response = self.client.post("/categories/", 
                json={"name": "Main Meals"},
                headers=auth_header
            )
            self.assertEqual(response.status_code, 409, "Category creation should fail when category name already exists")
        except ValueError as e:
            self.fail(str(e))
    
    def test_get_categories_successful(self):
        try:
            auth_header = {"Authorization": self._register_and_login()}
            response = self.client.get("/categories/", headers=auth_header)
            self.assertEqual(response.status_code, 200, "Categories should be fetched successfully")
        except ValueError as e:
            self.fail(str(e))
    
    def test_get_category_successful(self):
        try:
            auth_header = {"Authorization": self._register_and_login()}
            self.client.post("/categories/", 
                json={"name": "Main Meals"},
                headers=auth_header
            )
            response = self.client.get("/categories/1", headers=auth_header)
            self.assertEqual(response.status_code, 200, "Category should be fetched successfully")
        except ValueError as e:
            self.fail(str(e))
        
    def test_get_category_fail(self):
        try:
            auth_header = {"Authorization": self._register_and_login()}
            response = self.client.get("/categories/1", headers=auth_header)
            self.assertEqual(response.status_code, 404, "Category should not be found")
        except ValueError as e:
            self.fail(str(e))

    def test_update_category_successful(self):
        try:
            auth_header = {"Authorization": self._register_and_login()}
            self.client.post("/categories/", 
                json={"name": "Main Meals"},
                headers=auth_header
            )
            
            response = self.client.put("/categories/1", 
                json={"name": "Main Dishes"},
                headers=auth_header
            )
            self.assertEqual(response.status_code, 200, "Category should be updated successfully")
        except ValueError as e:
            self.fail(str(e))

    def test_update_category_unauthorized(self):
        try:
            auth_header = {"Authorization": self._register_and_login()}
            self.client.post("/categories/", 
                json={"name": "Main Meals"},
                headers=auth_header
            )
            
            # Try update without token
            response = self.client.put("/categories/1", 
                json={"name": "Main Dishes"}
            )
            self.assertIn(response.status_code, [400, 401], "Should fail without authentication")
        except ValueError as e:
            self.fail(str(e))

    def test_update_category_fail(self):
        try:
            auth_header = {"Authorization": self._register_and_login()}
            response = self.client.put("/categories/1", 
                json={"name": "Main Dishes"},
                headers=auth_header
            )
            self.assertEqual(response.status_code, 404, "Category should not be found")
        except ValueError as e:
            self.fail(str(e))
    
    def test_delete_category_successful(self):
        try:
            auth_header = {"Authorization": self._register_and_login()}
            self.client.post("/categories/", 
                json={"name": "Main Meals"},
                headers=auth_header
            )
            
            response = self.client.delete("/categories/1", headers=auth_header)
            self.assertEqual(response.status_code, 200, "Category should be deleted successfully")
        except ValueError as e:
            self.fail(str(e))

    def test_delete_category_unauthorized(self):
        try:
            auth_header = {"Authorization": self._register_and_login()}
            self.client.post("/categories/", 
                json={"name": "Main Meals"},
                headers=auth_header
            )
            
            # Try delete without token
            response = self.client.delete("/categories/1")
            self.assertIn(response.status_code, [400, 401], "Should fail without authentication")
        except ValueError as e:
            self.fail(str(e))

    def test_delete_category_fail(self):
        try:
            auth_header = {"Authorization": self._register_and_login()}
            response = self.client.delete("/categories/1", headers=auth_header)
            self.assertEqual(response.status_code, 404, "Category should not be found")
        except ValueError as e:
            self.fail(str(e))