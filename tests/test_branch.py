from unittest import TestCase
from api import create_app
from api.extensions import db

class BranchTestCase(TestCase):
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

    def test_create_branch_successful(self):
        response = self.client.post("/branches/", json={
            "name": "TLC Mandaluyong",
            "address": "124 Mandaluyong mandaluyon mandaluyong"
        })

        self.assertEqual(response.status_code, 201, "Branch should be created successfully")
    
    def test_create_branch_incomplete_fail(self):
        response = self.client.post("/branches/", json={
            "name": "TLC Mandaluyong"
        })

        self.assertEqual(response.status_code, 400, "Branch creation should fail when required fields are missing")
    
    def test_create_branch_duplicate_name_fail(self):
        self.client.post("/branches/", json={
            "name": "TLC Mandaluyong",
            "address": "124 Mandaluyong mandaluyon mandaluyong"
        })

        response = self.client.post("/branches/", json={
            "name": "TLC Mandaluyong",
            "address": "124 Manila manila manila"
        })

        self.assertEqual(response.status_code, 409, "Branch creation should fail when name already exists")

    def test_create_branch_duplicate_address_fail(self):
        self.client.post("/branches/", json={
            "name": "TLC Mandaluyong",
            "address": "124 Mandaluyong mandaluyon mandaluyong"
        })

        response = self.client.post("/branches/", json={
            "name": "TLC Manila",
            "address": "124 Mandaluyong mandaluyon mandaluyong"
        })

        self.assertEqual(response.status_code, 409, "Branch creation should fail when address already exists")
    
    def test_get_branches(self):
        response = self.client.get("/branches/")

        self.assertEqual(response.status_code, 200, "Should return list of branches")
    
    def test_get_branch_by_id_successful(self):
        self.client.post("/branches/", json={
            "name": "TLC Mandaluyong",
            "address": "124 Mandaluyong mandaluyon mandaluyong"
        })

        response = self.client.get("/branches/1")

        self.assertEqual(response.status_code, 200, "Should return branch details")
    
    def test_get_branch_by_id_not_found(self):
        response = self.client.get("/branches/999")

        self.assertEqual(response.status_code, 404, "Should return 404 when branch is not found")
    
    def test_update_branch_successful(self):
        self.client.post("/branches/", json={
            "name": "TLC Mandaluyong",
            "address": "124 Mandaluyong mandaluyon mandaluyong"
        })

        response = self.client.put("/branches/1", json={
            "name": "Updated TLC Mandaluyong",
            "address": "Updated 124 Mandaluyong mandaluyon mandaluyong"
        })

        self.assertEqual(response.status_code, 200, "Branch should be updated successfully")
    
    def test_update_branch_not_found(self):
        response = self.client.put("/branches/999", json={
            "name": "Nonexistent Branch",
            "address": "Nonexistent Address"
        })

        self.assertEqual(response.status_code, 404, "Should return 404 when branch is not found")
    
    def test_delete_branch_successful(self):
        self.client.post("/branches/", json={
            "name": "TLC Mandaluyong",
            "address": "124 Mandaluyong mandaluyon mandaluyong"
        })

        response = self.client.delete("/branches/1")

        self.assertEqual(response.status_code, 200, "Branch should be deleted successfully")
    
    def test_delete_branch_not_found(self):
        response = self.client.delete("/branches/999")

        self.assertEqual(response.status_code, 404, "Should return 404 when branch is not found")