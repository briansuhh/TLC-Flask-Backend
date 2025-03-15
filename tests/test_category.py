from unittest import TestCase
from api import create_app
from api.extensions import db

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
            # to delete all data from all tables, but not the tables themselves
            for table in reversed(db.metadata.sorted_tables):
                db.session.execute(table.delete())
            db.session.commit()

    def test_create_category_successful(self):
        response = self.client.post("/categories/", json={
            "name": "Main Meals"
        })
        
        self.assertEqual(response.status_code, 201, "Category should be created successfully")

    def test_create_category_incomplete_fail(self):
        response = self.client.post("/categories/", json={
            "name": ""
        })

        self.assertEqual(response.status_code, 400, "Category creation should fail when required fields are missing")

    def test_create_category_duplicate_fail(self):
        self.client.post("/categories/", json={
            "name": "Main Meals"
        })
        
        response = self.client.post("/categories/", json={
            "name": "Main Meals"
        })

        self.assertEqual(response.status_code, 409, "Category creation should fail when category name already exists")
       
    
    def test_get_categories_successful(self):
        response = self.client.get("/categories/")
        self.assertEqual(response.status_code, 200, "Categories should be fetched successfully")
    
    def test_get_category_successful(self):
        response = self.client.post("/categories/", json={
            "name": "Main Meals"
        })

        response = self.client.get("/categories/1")

        self.assertEqual(response.status_code, 200, "Category should be fetched successfully")
        
    def test_get_category_fail(self):
        response = self.client.get("/categories/1")
        self.assertEqual(response.status_code, 404, "Category should not be found")

    def test_update_category_successful(self):
        self.client.post("/categories/", json={
            "name": "Main Meals"
        })
        
        response = self.client.put("/categories/1", json={
            "name": "Main Dishes"
        })

        self.assertEqual(response.status_code, 200, "Category should be updated successfully")

    def test_update_category_fail(self):
        response = self.client.put("/categories/1", json={
            "name": "Main Dishes"
        })

        self.assertEqual(response.status_code, 404, "Category should not be found")
    
    def test_delete_category_successful(self):
        self.client.post("/categories/", json={
            "name": "Main Meals"
        })
        
        response = self.client.delete("/categories/1")
        self.assertEqual(response.status_code, 200, "Category should be deleted successfully")
    
    def test_delete_category_fail(self):
        response = self.client.delete("/categories/1")
        self.assertEqual(response.status_code, 404, "Category should not be found")
