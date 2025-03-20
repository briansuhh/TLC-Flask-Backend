from unittest import TestCase
from api import create_app
from api.extensions import db

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
            # to delete all data from all tables, but not the tables themselves
            for table in reversed(db.metadata.sorted_tables):
                db.session.execute(table.delete())
            db.session.commit()

    def test_create_outlet_successful(self):
        response = self.client.post("/outlets/", json={
            "product_id": 2,
            "name": "New Outlet",
            "price": 60.00
        })
        self.assertEqual(response.status_code, 201, "Outlet should be created successfully")

    def test_create_outlet_incomplete_fail(self):
        response = self.client.post("/outlets/", json={
            "product_id": 2,
            "name": "In-Store"
        })
        self.assertEqual(response.status_code, 400, "Outlet creation should fail when required fields are missing")
    
    def test_create_outlet_duplicate_name_fail(self):
        self.client.post("/outlets/", json={
            "product_id": 2,
            "name": "In-Store",
            "price": 55.00
        })

        response = self.client.post("/outlets/", json={
            "product_id": 2,
            "name": "In-Store",
            "price": 55.00
        })
        self.assertEqual(response.status_code, 409, "Outlet creation should fail when name already exists")
    
    def test_get_outlets(self):
        response = self.client.get("/outlets/")
        self.assertEqual(response.status_code, 200, "Should return list of outlets")
    
    def test_get_outlet_by_id_successful(self):
        self.client.post("/outlets/", json={
            "product_id": 2,
            "name": "In-Store",
            "price": 55.00
        })
        
        response = self.client.get("/outlets/1")
        self.assertEqual(response.status_code, 200, "Should return outlet details")
    
    def test_get_outlet_by_id_not_found(self):
        response = self.client.get("/outlets/999")
        self.assertEqual(response.status_code, 404, "Should return 404 when outlet is not found")
        
    def test_update_outlet_successful(self):
        self.client.post("/outlets/", json={
            "product_id": 2,
            "name": "In-Store",
            "price": 55.00
        })

        response = self.client.put("/outlets/1", json={
            "name": "Updated In-Store",
            "price": 51.00
        })
        self.assertEqual(response.status_code, 200, "Outlet should be updated successfully")

    def test_update_outlet_not_found(self):
        response = self.client.put("/outlets/999", json={
            "name": "Updated In-Store",
            "price": 51.00
        })
        self.assertEqual(response.status_code, 404, "Should return 404 when outlet is not found")
    
    def test_delete_outlet_successful(self):
        self.client.post("/outlets/", json={
            "product_id": 2,
            "name": "New Outlet",
            "price": 60.00
        })

        response = self.client.delete("/outlets/1")
        self.assertEqual(response.status_code, 200, "Outlet should be deleted successfully")
    
    def test_delete_outlet_not_found(self):
        response = self.client.delete("/outlets/999")
        self.assertEqual(response.status_code, 404, "Should return 404 when outlet is not found")
