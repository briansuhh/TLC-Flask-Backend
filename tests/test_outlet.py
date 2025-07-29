from unittest import TestCase
from api import create_app
from api.extensions import db
import json

class OutletTestCase(TestCase):
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

    def test_create_outlet_successful(self):
        try:
            auth_header = {"Authorization": self._register_and_login()}
            response = self.client.post("/outlets/", 
                json={
                    "product_id": 2,
                    "name": "New Outlet",
                    "price": 60.00
                },
                headers=auth_header
            )
            self.assertEqual(response.status_code, 201, "Outlet should be created successfully")
        except ValueError as e:
            self.fail(str(e))

    def test_create_outlet_unauthorized(self):
        response = self.client.post("/outlets/", 
            json={
                "product_id": 2,
                "name": "New Outlet",
                "price": 60.00
            }
        )
        self.assertIn(response.status_code, [400, 401], "Should fail without authentication")

    def test_create_outlet_incomplete_fail(self):
        try:
            auth_header = {"Authorization": self._register_and_login()}
            response = self.client.post("/outlets/", 
                json={
                    "product_id": 2,
                    "name": "In-Store"
                },
                headers=auth_header
            )
            self.assertEqual(response.status_code, 400, "Outlet creation should fail when required fields are missing")
        except ValueError as e:
            self.fail(str(e))
    
    def test_get_outlets(self):
        try:
            auth_header = {"Authorization": self._register_and_login()}
            response = self.client.get("/outlets/", headers=auth_header)
            self.assertEqual(response.status_code, 200, "Should return list of outlets")
        except ValueError as e:
            self.fail(str(e))

    def test_get_outlets_unauthorized(self):
        response = self.client.get("/outlets/")
        self.assertIn(response.status_code, [400, 401], "Should fail without authentication")
    
    def test_get_outlet_by_id_successful(self):
        try:
            auth_header = {"Authorization": self._register_and_login()}
            self.client.post("/outlets/", 
                json={
                    "product_id": 2,
                    "name": "In-Store",
                    "price": 55.00
                },
                headers=auth_header
            )
            
            response = self.client.get("/outlets/1", headers=auth_header)
            self.assertEqual(response.status_code, 200, "Should return outlet details")
        except ValueError as e:
            self.fail(str(e))

    def test_get_outlet_by_id_unauthorized(self):
        try:
            auth_header = {"Authorization": self._register_and_login()}
            self.client.post("/outlets/", 
                json={
                    "product_id": 2,
                    "name": "In-Store",
                    "price": 55.00
                },
                headers=auth_header
            )
            
            # Try GET without token
            response = self.client.get("/outlets/1")
            self.assertIn(response.status_code, [400, 401], "Should fail without authentication")
        except ValueError as e:
            self.fail(str(e))
    
    def test_get_outlet_by_id_not_found(self):
        try:
            auth_header = {"Authorization": self._register_and_login()}
            response = self.client.get("/outlets/999", headers=auth_header)
            self.assertEqual(response.status_code, 404, "Should return 404 when outlet is not found")
        except ValueError as e:
            self.fail(str(e))
        
    def test_update_outlet_successful(self):
        try:
            auth_header = {"Authorization": self._register_and_login()}
            self.client.post("/outlets/", 
                json={
                    "product_id": 2,
                    "name": "In-Store",
                    "price": 55.00
                },
                headers=auth_header
            )

            response = self.client.put("/outlets/1", 
                json={
                    "name": "Updated In-Store",
                    "price": 51.00
                },
                headers=auth_header
            )
            self.assertEqual(response.status_code, 200, "Outlet should be updated successfully")
        except ValueError as e:
            self.fail(str(e))

    def test_update_outlet_unauthorized(self):
        try:
            auth_header = {"Authorization": self._register_and_login()}
            self.client.post("/outlets/", 
                json={
                    "product_id": 2,
                    "name": "In-Store",
                    "price": 55.00
                },
                headers=auth_header
            )

            # Try update without token
            response = self.client.put("/outlets/1", 
                json={
                    "name": "Updated In-Store",
                    "price": 51.00
                }
            )
            self.assertIn(response.status_code, [400, 401], "Should fail without authentication")
        except ValueError as e:
            self.fail(str(e))

    def test_update_outlet_not_found(self):
        try:
            auth_header = {"Authorization": self._register_and_login()}
            response = self.client.put("/outlets/999", 
                json={
                    "name": "Updated In-Store",
                    "price": 51.00
                },
                headers=auth_header
            )
            self.assertEqual(response.status_code, 404, "Should return 404 when outlet is not found")
        except ValueError as e:
            self.fail(str(e))
    
    def test_delete_outlet_successful(self):
        try:
            auth_header = {"Authorization": self._register_and_login()}
            self.client.post("/outlets/", 
                json={
                    "product_id": 2,
                    "name": "New Outlet",
                    "price": 60.00
                },
                headers=auth_header
            )

            response = self.client.delete("/outlets/1", headers=auth_header)
            self.assertEqual(response.status_code, 200, "Outlet should be deleted successfully")
        except ValueError as e:
            self.fail(str(e))

    def test_delete_outlet_unauthorized(self):
        try:
            auth_header = {"Authorization": self._register_and_login()}
            self.client.post("/outlets/", 
                json={
                    "product_id": 2,
                    "name": "New Outlet",
                    "price": 60.00
                },
                headers=auth_header
            )

            # Try delete without token
            response = self.client.delete("/outlets/1")
            self.assertIn(response.status_code, [400, 401], "Should fail without authentication")
        except ValueError as e:
            self.fail(str(e))
    
    def test_delete_outlet_not_found(self):
        try:
            auth_header = {"Authorization": self._register_and_login()}
            response = self.client.delete("/outlets/999", headers=auth_header)
            self.assertEqual(response.status_code, 404, "Should return 404 when outlet is not found")
        except ValueError as e:
            self.fail(str(e))