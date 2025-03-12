from unittest import TestCase
from api import create_app
from api.extensions import db

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
            # to delete all data from all tables, but not the tables themselves
            for table in reversed(db.metadata.sorted_tables):
                db.session.execute(table.delete())
            db.session.commit()

    def test_create_supplier_successful(self):
        response = self.client.post("/suppliers/", json={
            "name": "Egg Supplier",
            "email": "eggsupplier@gmail.com",
            "phone": "9991114444",
            "country_code": "+63"
        })

        self.assertEqual(response.status_code, 201, "Supplier should be created successfully")
    
    def test_create_supplier_incomplete_fail(self):
        response = self.client.post("/suppliers/", json={
            "name": "Egg Supplier",
            "email": "eggsupplier@gmail.com",
            "phone": "9991114444"
        })

        self.assertEqual(response.status_code, 400, "Supplier creation should fail when required fields are missing")

    def test_create_supplier_invalid_email_fail(self):
        response = self.client.post("/suppliers/", json={
            "name": "Egg Supplier",
            "email": "eggsupplier@gmail",
            "phone": "9991114444",
            "country_code": "+63"
        })

        self.assertEqual(response.status_code, 400, "Supplier email format should be correct.")

    def test_create_supplier_invalid_phone_length_fail(self):
        response = self.client.post("/suppliers/", json={
            "name": "Egg Supplier",
            "email": "eggsupplier@gmail",
            "phone": "999111444400",
            "country_code": "+63"
        })

        self.assertEqual(response.status_code, 400, "Supplier phone number should be 11 digits max (if 0 is included).")
    
    def test_create_supplier_invalid_countrycode_length_fail(self):
        response = self.client.post("/suppliers/", json={
            "name": "Egg Supplier",
            "email": "eggsupplier@gmail",
            "phone": "999111444400",
            "country_code": "+63-451245"
        })

        self.assertEqual(response.status_code, 400, "Supplier country code should be 8 digits max (+ sign is included).")
    
    def test_create_supplier_duplicate_email_fail(self):
        self.client.post("/suppliers/", json={
            "name": "Egg Supplier",
            "email": "eggsupplier@gmail.com",
            "phone": "9991114444",
            "country_code": "+63"
        })

        response = self.client.post("/suppliers/", json={
            "name": "Oil Supplier",
            "email": "eggsupplier@gmail.com",
            "phone": "9991114445",
            "country_code": "+63"
        })

        self.assertEqual(response.status_code, 409, "Supplier creation should fail when email already exists")

    def test_create_supplier_duplicate_phone_fail(self):
        self.client.post("/suppliers/", json={
            "name": "Egg Supplier",
            "email": "eggsupplier@gmail.com",
            "phone": "9991114444",
            "country_code": "+63"
        })

        response = self.client.post("/suppliers/", json={
            "name": "Oil Supplier",
            "email": "oilsupplier@gmail.com",
            "phone": "9991114444",
            "country_code": "+63"
        })

        self.assertEqual(response.status_code, 409, "Supplier creation should fail when phone already exists")
    
    def test_get_suppliers(self):
        response = self.client.get("/suppliers/")

        self.assertEqual(response.status_code, 200, "Should return list of suppliers")
    
    def test_get_supplier_by_id_successful(self):
        self.client.post("/suppliers/", json={
            "name": "Oil Supplier",
            "email": "oilsupplier@gmail.com",
            "phone": "9991114444",
            "country_code": "+63"
        })

        response = self.client.get("/suppliers/1")

        self.assertEqual(response.status_code, 200, "Should return supplier details")
    
    def test_get_supplier_by_id_not_found(self):
        response = self.client.get("/suppliers/999")

        self.assertEqual(response.status_code, 404, "Should return 404 when supplier is not found")
    
    def test_update_supplier_successful(self):
        self.client.post("/suppliers/", json={
            "name": "Egg Supplier",
            "email": "eggsupplier@gmail.com",
            "phone": "9991114444",
            "country_code": "+63"
        })

        response = self.client.put("/suppliers/1", json={
            "name": "New Egg Supplier",
            "email": "eggsupplier@gmail.com",
            "phone": "9991114444",
            "country_code": "+63"
        })

        self.assertEqual(response.status_code, 200, "Supplier should be updated successfully")
    
    def test_update_supplier_not_found(self):
        response = self.client.put("/suppliers/999", json={
            "name": "Fake Supplier",
            "email": "fakesupplier@gmail.com",
            "phone": "9991114444",
            "country_code": "+63"
        })

        self.assertEqual(response.status_code, 404, "Should return 404 when supplier is not found")
    
    def test_delete_supplier_successful(self):
        self.client.post("/suppliers/", json={
            "name": "Egg Supplier",
            "email": "eggsupplier@gmail.com",
            "phone": "9991114444",
            "country_code": "+63"
        })

        response = self.client.delete("/suppliers/1")

        self.assertEqual(response.status_code, 200, "Supplier should be deleted successfully")
    
    def test_delete_supplier_not_found(self):
        response = self.client.delete("/suppliers/999")

        self.assertEqual(response.status_code, 404, "Should return 404 when supplier is not found")