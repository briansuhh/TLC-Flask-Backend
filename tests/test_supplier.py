from unittest import TestCase
from api import create_app
from api.extensions import db
import json

class SupplierTestCase(TestCase):
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

    def test_create_supplier_successful(self):
        try:
            auth_header = {"Authorization": self._register_and_login()}
            response = self.client.post("/suppliers/", 
                json={
                    "name": "Egg Supplier",
                    "email": "eggsupplier@gmail.com",
                    "phone": "9991114444",
                    "country_code": "+63"
                },
                headers=auth_header
            )
            self.assertEqual(response.status_code, 201, "Supplier should be created successfully")
        except ValueError as e:
            self.fail(str(e))
    
    def test_create_supplier_unauthorized(self):
        response = self.client.post("/suppliers/", 
            json={
                "name": "Egg Supplier",
                "email": "eggsupplier@gmail.com",
                "phone": "9991114444",
                "country_code": "+63"
            }
        )
        self.assertIn(response.status_code, [400, 401], "Should fail without authentication")

    def test_create_supplier_incomplete_fail(self):
        try:
            auth_header = {"Authorization": self._register_and_login()}
            response = self.client.post("/suppliers/", 
                json={
                    "name": "Egg Supplier",
                    "email": "eggsupplier@gmail.com",
                    "phone": "9991114444"
                },
                headers=auth_header
            )
            self.assertEqual(response.status_code, 400, "Supplier creation should fail when required fields are missing")
        except ValueError as e:
            self.fail(str(e))

    def test_create_supplier_invalid_email_fail(self):
        try:
            auth_header = {"Authorization": self._register_and_login()}
            response = self.client.post("/suppliers/", 
                json={
                    "name": "Egg Supplier",
                    "email": "eggsupplier@gmail",
                    "phone": "9991114444",
                    "country_code": "+63"
                },
                headers=auth_header
            )
            self.assertEqual(response.status_code, 400, "Supplier email format should be correct.")
        except ValueError as e:
            self.fail(str(e))

    def test_create_supplier_invalid_phone_length_fail(self):
        try:
            auth_header = {"Authorization": self._register_and_login()}
            response = self.client.post("/suppliers/", 
                json={
                    "name": "Egg Supplier",
                    "email": "eggsupplier@gmail.com",
                    "phone": "999111444400",
                    "country_code": "+63"
                },
                headers=auth_header
            )
            self.assertEqual(response.status_code, 400, "Supplier phone number should be 11 digits max (if 0 is included).")
        except ValueError as e:
            self.fail(str(e))
    
    def test_create_supplier_invalid_countrycode_length_fail(self):
        try:
            auth_header = {"Authorization": self._register_and_login()}
            response = self.client.post("/suppliers/", 
                json={
                    "name": "Egg Supplier",
                    "email": "eggsupplier@gmail.com",
                    "phone": "9991114444",
                    "country_code": "+63-451245"
                },
                headers=auth_header
            )
            self.assertEqual(response.status_code, 400, "Supplier country code should be 8 digits max (+ sign is included).")
        except ValueError as e:
            self.fail(str(e))
    
    def test_create_supplier_duplicate_email_fail(self):
        try:
            auth_header = {"Authorization": self._register_and_login()}
            self.client.post("/suppliers/", 
                json={
                    "name": "Egg Supplier",
                    "email": "eggsupplier@gmail.com",
                    "phone": "9991114444",
                    "country_code": "+63"
                },
                headers=auth_header
            )

            response = self.client.post("/suppliers/", 
                json={
                    "name": "Oil Supplier",
                    "email": "eggsupplier@gmail.com",
                    "phone": "9991114445",
                    "country_code": "+63"
                },
                headers=auth_header
            )
            self.assertEqual(response.status_code, 409, "Supplier creation should fail when email already exists")
        except ValueError as e:
            self.fail(str(e))

    def test_create_supplier_duplicate_phone_fail(self):
        try:
            auth_header = {"Authorization": self._register_and_login()}
            self.client.post("/suppliers/", 
                json={
                    "name": "Egg Supplier",
                    "email": "eggsupplier@gmail.com",
                    "phone": "9991114444",
                    "country_code": "+63"
                },
                headers=auth_header
            )

            response = self.client.post("/suppliers/", 
                json={
                    "name": "Oil Supplier",
                    "email": "oilsupplier@gmail.com",
                    "phone": "9991114444",
                    "country_code": "+63"
                },
                headers=auth_header
            )
            self.assertEqual(response.status_code, 409, "Supplier creation should fail when phone already exists")
        except ValueError as e:
            self.fail(str(e))
    
    def test_get_suppliers(self):
        try:
            auth_header = {"Authorization": self._register_and_login()}
            response = self.client.get("/suppliers/", headers=auth_header)
            self.assertEqual(response.status_code, 200, "Should return list of suppliers")
        except ValueError as e:
            self.fail(str(e))

    def test_get_suppliers_unauthorized(self):
        response = self.client.get("/suppliers/")
        self.assertIn(response.status_code, [400, 401], "Should fail without authentication")
    
    def test_get_supplier_by_id_successful(self):
        try:
            auth_header = {"Authorization": self._register_and_login()}
            self.client.post("/suppliers/", 
                json={
                    "name": "Oil Supplier",
                    "email": "oilsupplier@gmail.com",
                    "phone": "9991114444",
                    "country_code": "+63"
                },
                headers=auth_header
            )

            response = self.client.get("/suppliers/1", headers=auth_header)
            self.assertEqual(response.status_code, 200, "Should return supplier details")
        except ValueError as e:
            self.fail(str(e))

    def test_get_supplier_by_id_unauthorized(self):
        try:
            auth_header = {"Authorization": self._register_and_login()}
            self.client.post("/suppliers/", 
                json={
                    "name": "Oil Supplier",
                    "email": "oilsupplier@gmail.com",
                    "phone": "9991114444",
                    "country_code": "+63"
                },
                headers=auth_header
            )

            # Try GET without token
            response = self.client.get("/suppliers/1")
            self.assertIn(response.status_code, [400, 401], "Should fail without authentication")
        except ValueError as e:
            self.fail(str(e))
    
    def test_get_supplier_by_id_not_found(self):
        try:
            auth_header = {"Authorization": self._register_and_login()}
            response = self.client.get("/suppliers/999", headers=auth_header)
            self.assertEqual(response.status_code, 404, "Should return 404 when supplier is not found")
        except ValueError as e:
            self.fail(str(e))
        
    def test_update_supplier_successful(self):
        try:
            auth_header = {"Authorization": self._register_and_login()}
            self.client.post("/suppliers/", 
                json={
                    "name": "Egg Supplier",
                    "email": "eggsupplier@gmail.com",
                    "phone": "9991114444",
                    "country_code": "+63"
                },
                headers=auth_header
            )

            response = self.client.put("/suppliers/1", 
                json={
                    "name": "New Egg Supplier",
                    "email": "eggsupplier@gmail.com",
                    "phone": "9991114444",
                    "country_code": "+63"
                },
                headers=auth_header
            )
            self.assertEqual(response.status_code, 200, "Supplier should be updated successfully")
        except ValueError as e:
            self.fail(str(e))

    def test_update_supplier_unauthorized(self):
        try:
            auth_header = {"Authorization": self._register_and_login()}
            self.client.post("/suppliers/", 
                json={
                    "name": "Egg Supplier",
                    "email": "eggsupplier@gmail.com",
                    "phone": "9991114444",
                    "country_code": "+63"
                },
                headers=auth_header
            )

            # Try update without token
            response = self.client.put("/suppliers/1", 
                json={
                    "name": "New Egg Supplier",
                    "email": "eggsupplier@gmail.com",
                    "phone": "9991114444",
                    "country_code": "+63"
                }
            )
            self.assertIn(response.status_code, [400, 401], "Should fail without authentication")
        except ValueError as e:
            self.fail(str(e))

    def test_update_supplier_not_found(self):
        try:
            auth_header = {"Authorization": self._register_and_login()}
            response = self.client.put("/suppliers/999", 
                json={
                    "name": "Fake Supplier",
                    "email": "fakesupplier@gmail.com",
                    "phone": "9991114444",
                    "country_code": "+63"
                },
                headers=auth_header
            )
            self.assertEqual(response.status_code, 404, "Should return 404 when supplier is not found")
        except ValueError as e:
            self.fail(str(e))
    
    def test_delete_supplier_successful(self):
        try:
            auth_header = {"Authorization": self._register_and_login()}
            self.client.post("/suppliers/", 
                json={
                    "name": "Egg Supplier",
                    "email": "eggsupplier@gmail.com",
                    "phone": "9991114444",
                    "country_code": "+63"
                },
                headers=auth_header
            )

            response = self.client.delete("/suppliers/1", headers=auth_header)
            self.assertEqual(response.status_code, 200, "Supplier should be deleted successfully")
        except ValueError as e:
            self.fail(str(e))

    def test_delete_supplier_unauthorized(self):
        try:
            auth_header = {"Authorization": self._register_and_login()}
            self.client.post("/suppliers/", 
                json={
                    "name": "Egg Supplier",
                    "email": "eggsupplier@gmail.com",
                    "phone": "9991114444",
                    "country_code": "+63"
                },
                headers=auth_header
            )

            # Try delete without token
            response = self.client.delete("/suppliers/1")
            self.assertIn(response.status_code, [400, 401], "Should fail without authentication")
        except ValueError as e:
            self.fail(str(e))
    
    def test_delete_supplier_not_found(self):
        try:
            auth_header = {"Authorization": self._register_and_login()}
            response = self.client.delete("/suppliers/999", headers=auth_header)
            self.assertEqual(response.status_code, 404, "Should return 404 when supplier is not found")
        except ValueError as e:
            self.fail(str(e))