from unittest import TestCase
from api import create_app
from api.extensions import db

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
            # To delete all data from all tables, but not the tables themselves
            for table in reversed(db.metadata.sorted_tables):
                db.session.execute(table.delete())
            db.session.commit()

    def test_create_inventory_item_successful(self):
        response = self.client.post("/inventory-items/", json={
            "name": "Item 1",
            "cost": 100.00,
            "unit": "kg",
            "stock_warning_level": 10.0,
            "supplier_id": 1
        })

        self.assertEqual(response.status_code, 201, "Inventory item should be created successfully")
    
    def test_create_inventory_item_incomplete_fail(self):
        response = self.client.post("/inventory-items/", json={
            "name": "Item 1",
            "cost": 100.00,
            "unit": "kg"
        })

        self.assertEqual(response.status_code, 400, "Inventory item creation should fail when required fields are missing")
    
    def test_get_inventory_items(self):
        response = self.client.get("/inventory-items/")

        self.assertEqual(response.status_code, 200, "Should return list of inventory items")
    
    def test_get_inventory_item_by_id_successful(self):
        # Assuming item is created first
        self.client.post("/inventory-items/", json={
            "name": "Item 1",
            "cost": 100.00,
            "unit": "kg",
            "stock_warning_level": 10.0,
            "supplier_id": 1
        })

        response = self.client.get("/inventory-items/1")

        self.assertEqual(response.status_code, 200, "Should return inventory item details")
    
    def test_get_inventory_item_by_id_not_found(self):
        response = self.client.get("/inventory-items/999")

        self.assertEqual(response.status_code, 404, "Should return 404 when inventory item is not found")
    
    def test_update_inventory_item_successful(self):
        self.client.post("/inventory-items/", json={
            "name": "Item 1",
            "cost": 100.00,
            "unit": "kg",
            "stock_warning_level": 10.0,
            "supplier_id": 1
        })

        response = self.client.put("/inventory-items/1", json={
            "name": "Updated Item 1",
            "cost": 120.00,
            "unit": "kg",
            "stock_warning_level": 15.0,
            "supplier_id": 2
        })

        self.assertEqual(response.status_code, 200, "Inventory item should be updated successfully")
    
    def test_update_inventory_item_not_found(self):
        response = self.client.put("/inventory-items/999", json={
            "name": "Nonexistent Item",
            "cost": 150.00,
            "unit": "kg",
            "stock_warning_level": 5.0,
            "supplier_id": 3
        })

        self.assertEqual(response.status_code, 404, "Should return 404 when inventory item is not found")
    
    def test_delete_inventory_item_successful(self):
        self.client.post("/inventory-items/", json={
            "name": "Item 1",
            "cost": 100.00,
            "unit": "kg",
            "stock_warning_level": 10.0,
            "supplier_id": 1
        })

        response = self.client.delete("/inventory-items/1")

        self.assertEqual(response.status_code, 200, "Inventory item should be deleted successfully")
    
    def test_delete_inventory_item_not_found(self):
        response = self.client.delete("/inventory-items/999")

        self.assertEqual(response.status_code, 404, "Should return 404 when inventory item is not found")
