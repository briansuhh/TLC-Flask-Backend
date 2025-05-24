from unittest import TestCase
from api import create_app
from api.extensions import db
import json

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

    def _create_test_data(self):
        """Helper function to create product and inventory item."""
        try:
            # Create product
            product_resp = self.client.post("/products/", json={
                "name": "Product 1",
                "variant_group_id": "12345ABCDE",
                "sku": "ABCDE12345",
                "category_id": 1
            })
            self.assertEqual(product_resp.status_code, 201)
            self.product_id = json.loads(product_resp.data).get('product_id', 1)

            # Create inventory item
            item_resp = self.client.post("/inventory-items/", json={
                "name": "Item 1",
                "cost": 10.0,
                "unit": "kg",
                "stock_warning_level": 5.0,
                "supplier_id": 1
            })
            self.assertEqual(item_resp.status_code, 201)
            self.item_id = json.loads(item_resp.data).get('item_id', 1)
        except Exception as e:
            self.fail(f"Failed to create test data: {str(e)}")

    def test_create_recipe_successful(self):
        self._create_test_data()

        response = self.client.post("/recipes/", json={
            "product_id": self.product_id,
            "item_id": self.item_id,
            "quantity": 5.0,
            "isTakeout": True
        })

        self.assertEqual(response.status_code, 201, "Recipe should be created successfully")

    def test_create_recipe_incomplete_fail(self):
        self._create_test_data()

        response = self.client.post("/recipes/", json={
            "product_id": self.product_id,
            "item_id": self.item_id,
            "quantity": 5.0
            # Missing isTakeout
        })

        self.assertEqual(response.status_code, 400, "Recipe creation should fail when required fields are missing")

    def test_create_recipe_duplicate_fail(self):
        self._create_test_data()

        # Create the first recipe
        response1 = self.client.post("/recipes/", json={
            "product_id": self.product_id,
            "item_id": self.item_id,
            "quantity": 5.0,
            "isTakeout": True
        })
        self.assertEqual(response1.status_code, 201)

        # Try to create the same recipe again
        response2 = self.client.post("/recipes/", json={
            "product_id": self.product_id,
            "item_id": self.item_id,
            "quantity": 5.0,
            "isTakeout": True
        })
        self.assertEqual(response2.status_code, 409)

    def test_get_recipes(self):
        response = self.client.get("/recipes/")
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json, list)

    def test_get_recipe_by_product_item_successful(self):
        self._create_test_data()
        # Create a recipe first
        self.client.post("/recipes/", json={
            "product_id": self.product_id,
            "item_id": self.item_id,
            "quantity": 5.0,
            "isTakeout": True
        })

        response = self.client.get(f"/recipes/{self.product_id}/{self.item_id}")

        self.assertEqual(response.status_code, 200, "Should return recipe details")

    def test_get_recipe_by_product_item_not_found(self):
        response = self.client.get("/recipes/999/999")

        self.assertEqual(response.status_code, 404, "Should return 404 when recipe is not found")

    def test_update_recipe_successful(self):
        self._create_test_data()
        # Create a recipe first
        self.client.post("/recipes/", json={
            "product_id": self.product_id,
            "item_id": self.item_id,
            "quantity": 5.0,
            "isTakeout": True
        })

        response = self.client.put(f"/recipes/{self.product_id}/{self.item_id}", json={
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
        self._create_test_data()
        # Create a recipe first
        self.client.post("/recipes/", json={
            "product_id": self.product_id,
            "item_id": self.item_id,
            "quantity": 5.0,
            "isTakeout": True
        })

        response = self.client.delete(f"/recipes/{self.product_id}/{self.item_id}")

        self.assertEqual(response.status_code, 200, "Recipe should be deleted successfully")

    def test_delete_recipe_not_found(self):
        response = self.client.delete("/recipes/999/999")

        self.assertEqual(response.status_code, 404, "Should return 404 when recipe is not found")
