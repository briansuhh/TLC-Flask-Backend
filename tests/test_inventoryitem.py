from unittest import TestCase
from api import create_app
from api.extensions import db
import json

class InventoryItemTestCase(TestCase):
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

    def test_create_inventory_item_successful(self):
        try:
            auth_header = {"Authorization": self._register_and_login()}
            response = self.client.post("/inventory-items/", 
                json={
                    "name": "Item 1",
                    "cost": 100.00,
                    "unit": "kg",
                    "stock_warning_level": 10.0,
                    "supplier_id": 1
                },
                headers=auth_header
            )
            self.assertEqual(response.status_code, 201, "Inventory item should be created successfully")
        except ValueError as e:
            self.fail(str(e))
    
    def test_create_inventory_item_unauthorized(self):
        response = self.client.post("/inventory-items/", 
            json={
                "name": "Item 1",
                "cost": 100.00,
                "unit": "kg",
                "stock_warning_level": 10.0,
                "supplier_id": 1
            }
        )
        self.assertIn(response.status_code, [400, 401], "Should fail without authentication")
    
    def test_create_inventory_item_incomplete_fail(self):
        try:
            auth_header = {"Authorization": self._register_and_login()}
            response = self.client.post("/inventory-items/", 
                json={
                    "name": "Item 1",
                    "cost": 100.00,
                    "unit": "kg"
                },
                headers=auth_header
            )
            self.assertEqual(response.status_code, 400, "Inventory item creation should fail when required fields are missing")
        except ValueError as e:
            self.fail(str(e))
    
    def test_get_inventory_items(self):
        try:
            auth_header = {"Authorization": self._register_and_login()}
            response = self.client.get("/inventory-items/", headers=auth_header)
            self.assertEqual(response.status_code, 200, "Should return list of inventory items")
        except ValueError as e:
            self.fail(str(e))
    
    def test_get_inventory_item_by_id_successful(self):
        try:
            auth_header = {"Authorization": self._register_and_login()}
            # Create item first
            self.client.post("/inventory-items/", 
                json={
                    "name": "Item 1",
                    "cost": 100.00,
                    "unit": "kg",
                    "stock_warning_level": 10.0,
                    "supplier_id": 1
                },
                headers=auth_header
            )
            # GET doesn't require authentication
            response = self.client.get("/inventory-items/1", headers=auth_header)
            self.assertEqual(response.status_code, 200, "Should return inventory item details")
        except ValueError as e:
            self.fail(str(e))
    
    def test_get_inventory_item_by_id_not_found(self):
        try:
            auth_header = {"Authorization": self._register_and_login()}
            response = self.client.get("/inventory-items/999", headers=auth_header)
            self.assertEqual(response.status_code, 404, "Should return 404 when inventory item is not found")
        except ValueError as e:
            self.fail(str(e))
    
    def test_update_inventory_item_successful(self):
        try:
            auth_header = {"Authorization": self._register_and_login()}
            # Create item first
            self.client.post("/inventory-items/", 
                json={
                    "name": "Item 1",
                    "cost": 100.00,
                    "unit": "kg",
                    "stock_warning_level": 10.0,
                    "supplier_id": 1
                },
                headers=auth_header
            )
            # Update item
            response = self.client.put("/inventory-items/1", 
                json={
                    "name": "Updated Item 1",
                    "cost": 120.00,
                    "unit": "kg",
                    "stock_warning_level": 15.0,
                    "supplier_id": 2
                },
                headers=auth_header
            )
            self.assertEqual(response.status_code, 200, "Inventory item should be updated successfully")
        except ValueError as e:
            self.fail(str(e))
    
    def test_update_inventory_item_unauthorized(self):
        try:
            auth_header = {"Authorization": self._register_and_login()}
            # Create item first
            self.client.post("/inventory-items/", 
                json={
                    "name": "Item 1",
                    "cost": 100.00,
                    "unit": "kg",
                    "stock_warning_level": 10.0,
                    "supplier_id": 1
                },
                headers=auth_header
            )
            # Try update without token
            response = self.client.put("/inventory-items/1", 
                json={
                    "name": "Updated Item 1",
                    "cost": 120.00,
                    "unit": "kg",
                    "stock_warning_level": 15.0,
                    "supplier_id": 2
                }
            )
            self.assertIn(response.status_code, [400, 401], "Should fail without authentication")
        except ValueError as e:
            self.fail(str(e))
    
    def test_update_inventory_item_not_found(self):
        try:
            auth_header = {"Authorization": self._register_and_login()}
            response = self.client.put("/inventory-items/999", 
                json={
                    "name": "Nonexistent Item",
                    "cost": 150.00,
                    "unit": "kg",
                    "stock_warning_level": 5.0,
                    "supplier_id": 3
                },
                headers=auth_header
            )
            self.assertEqual(response.status_code, 404, "Should return 404 when inventory item is not found")
        except ValueError as e:
            self.fail(str(e))
    
    def test_delete_inventory_item_successful(self):
        try:
            auth_header = {"Authorization": self._register_and_login()}
            # Create item first
            self.client.post("/inventory-items/", 
                json={
                    "name": "Item 1",
                    "cost": 100.00,
                    "unit": "kg",
                    "stock_warning_level": 10.0,
                    "supplier_id": 1
                },
                headers=auth_header
            )
            # Delete item
            response = self.client.delete("/inventory-items/1", headers=auth_header)
            self.assertEqual(response.status_code, 200, "Inventory item should be deleted successfully")
        except ValueError as e:
            self.fail(str(e))
    
    def test_delete_inventory_item_unauthorized(self):
        try:
            auth_header = {"Authorization": self._register_and_login()}
            # Create item first
            self.client.post("/inventory-items/", 
                json={
                    "name": "Item 1",
                    "cost": 100.00,
                    "unit": "kg",
                    "stock_warning_level": 10.0,
                    "supplier_id": 1
                },
                headers=auth_header
            )
            # Try delete without token
            response = self.client.delete("/inventory-items/1")
            self.assertIn(response.status_code, [400, 401], "Should fail without authentication")
        except ValueError as e:
            self.fail(str(e))
    
    def test_delete_inventory_item_not_found(self):
        try:
            auth_header = {"Authorization": self._register_and_login()}
            response = self.client.delete("/inventory-items/999", headers=auth_header)
            self.assertEqual(response.status_code, 404, "Should return 404 when inventory item is not found")
        except ValueError as e:
            self.fail(str(e))