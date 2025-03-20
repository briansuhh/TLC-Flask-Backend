from unittest import TestCase
from api import create_app
from api.extensions import db

class RecipeTestCase(TestCase):
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

    def test_create_recipe_successful(self):
        response = self.client.post("/recipes/", json={
            "product_id": 1,
            "item_id": 101,
            "quantity": 5.0,
            "isTakeout": True
        })

        self.assertEqual(response.status_code, 201, "Recipe should be created successfully")

    def test_create_recipe_incomplete_fail(self):
        response = self.client.post("/recipes/", json={
            "product_id": 1,
            "item_id": 101,
            "quantity": 5.0
        })

        self.assertEqual(response.status_code, 400, "Recipe creation should fail when required fields are missing")

    def test_create_recipe_duplicate_fail(self):
        # Create the first recipe
        self.client.post("/recipes/", json={
            "product_id": 1,
            "item_id": 101,
            "quantity": 5.0,
            "isTakeout": True
        })

        # Try to create the same recipe again
        response = self.client.post("/recipes/", json={
            "product_id": 1,
            "item_id": 101,
            "quantity": 5.0,
            "isTakeout": True
        })

        self.assertEqual(response.status_code, 409, "Recipe creation should fail when duplicate (product_id, item_id) exists")

    def test_get_recipes(self):
        response = self.client.get("/recipes/")

        self.assertEqual(response.status_code, 200, "Should return list of recipes")

    def test_get_recipe_by_product_item_successful(self):
        # Create a recipe first
        self.client.post("/recipes/", json={
            "product_id": 1,
            "item_id": 101,
            "quantity": 5.0,
            "isTakeout": True
        })

        # Get the recipe by product_id and item_id
        response = self.client.get("/recipes/1/101")

        self.assertEqual(response.status_code, 200, "Should return recipe details")

    def test_get_recipe_by_product_item_not_found(self):
        response = self.client.get("/recipes/999/999")

        self.assertEqual(response.status_code, 404, "Should return 404 when recipe is not found")

    def test_update_recipe_successful(self):
        # Create a recipe first
        self.client.post("/recipes/", json={
            "product_id": 1,
            "item_id": 101,
            "quantity": 5.0,
            "isTakeout": True
        })

        # Update the recipe
        response = self.client.put("/recipes/1/101", json={
            "quantity": 10.0,
            "isTakeout": False
        })

        self.assertEqual(response.status_code, 200, "Recipe should be updated successfully")

    def test_update_recipe_not_found(self):
        response = self.client.put("/recipes/999/999", json={
            "quantity": 10.0,
            "isTakeout": False
        })

        self.assertEqual(response.status_code, 404, "Should return 404 when recipe is not found")

    def test_delete_recipe_successful(self):
        # Create a recipe first
        self.client.post("/recipes/", json={
            "product_id": 1,
            "item_id": 101,
            "quantity": 5.0,
            "isTakeout": True
        })

        # Delete the recipe
        response = self.client.delete("/recipes/1/101")

        self.assertEqual(response.status_code, 200, "Recipe should be deleted successfully")

    def test_delete_recipe_not_found(self):
        response = self.client.delete("/recipes/999/999")

        self.assertEqual(response.status_code, 404, "Should return 404 when recipe is not found")
