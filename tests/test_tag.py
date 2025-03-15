from unittest import TestCase
from api import create_app
from api.extensions import db

class TagTestCase(TestCase):
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

    def test_create_tag_successful(self):
        response = self.client.post("/tags/", json={
            "name": "Vegan"
        })

        self.assertEqual(response.status_code, 201, "Tag should be created successfully")

    def test_create_tag_incomplete_fail(self):
        response = self.client.post("/tags/", json={
            "name": ""
        })

        self.assertEqual(response.status_code, 400, "Tag creation should fail when required fields are missing")

    def test_create_tag_duplicate_fail(self):
        self.client.post("/tags/", json={
            "name": "Vegan"
        })

        response = self.client.post("/tags/", json={
            "name": "Vegan"
        })

        self.assertEqual(response.status_code, 409, "Tag creation should fail when tag name already exists")

    def test_get_tags_successful(self):
        response = self.client.get("/tags/")
        self.assertEqual(response.status_code, 200, "Tags should be fetched successfully")

    def test_get_tag_successful(self):
        self.client.post("/tags/", json={
            "name": "Vegan"
        })

        response = self.client.get("/tags/1")

        self.assertEqual(response.status_code, 200, "Tag should be fetched successfully")

    def test_get_tag_fail(self):
        response = self.client.get("/tags/1")
        self.assertEqual(response.status_code, 404, "Tag should not be found")

    def test_update_tag_successful(self):
        self.client.post("/tags/", json={
            "name": "Vegan"
        })

        response = self.client.put("/tags/1", json={
            "name": "Vegetarian"
        })

        self.assertEqual(response.status_code, 200, "Tag should be updated successfully")

    def test_update_tag_fail(self):
        response = self.client.put("/tags/1", json={
            "name": "Vegetarian"
        })

        self.assertEqual(response.status_code, 404, "Tag should not be found")

    def test_delete_tag_successful(self):
        self.client.post("/tags/", json={
            "name": "Vegan"
        })

        response = self.client.delete("/tags/1")
        self.assertEqual(response.status_code, 200, "Tag should be deleted successfully")

    def test_delete_tag_fail(self):
        response = self.client.delete("/tags/1")
        self.assertEqual(response.status_code, 404, "Tag should not be found")
