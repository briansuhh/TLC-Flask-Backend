from unittest import TestCase
from api import create_app
from api.extensions import db
import json

class RecipeTestCase(TestCase):
    def setUp(self):
        """Set up the test client and initialize the database."""
        self.app = create_app()
        self.client = self.app.test_client()
        self.app.testing = True

        with self.app.app_context():
            db.create_all()

    def tearDown(self):
        """Tear down the database after each test."""
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
            
        return {"Authorization": f"Bearer {login_data['access_token']}"}

    def _create_test_data(self, auth_header):
        """Helper function to create product and inventory item."""
        try:
            # Create product
            product_resp = self.client.post("/products/", 
                json={
                    "name": "Product 1",
                    "variant_group_id": "12345ABCDE",
                    "sku": "ABCDE12345",
                    "category_id": 1
                },
                headers=auth_header
            )
            self.assertEqual(product_resp.status_code, 201)
            self.product_id = json.loads(product_resp.data).get('product_id', 1)

            # Create inventory item
            item_resp = self.client.post("/inventory-items/", 
                json={
                    "name": "Item 1",
                    "cost": 10.0,
                    "unit": "kg",
                    "stock_warning_level": 5.0,
                    "supplier_id": 1
                },
                headers=auth_header
            )
            self.assertEqual(item_resp.status_code, 201)
            self.item_id = json.loads(item_resp.data).get('item_id', 1)
        except Exception as e:
            self.fail(f"Failed to create test data: {str(e)}")

    def test_create_recipe_successful(self):
        """Test successful creation of recipe."""
        try:
            auth_header = self._register_and_login()
            self._create_test_data(auth_header)

            response = self.client.post("/recipes/", 
                json={
                    "product_id": self.product_id,
                    "item_id": self.item_id,
                    "quantity": 5.0,
                    "isTakeout": True
                },
                headers=auth_header
            )

            self.assertEqual(response.status_code, 201)
            self.assertIn("created successfully", response.json["message"])
        except ValueError as e:
            self.fail(str(e))

    def test_create_recipe_unauthorized(self):
        """Test unauthorized creation of recipe."""
        response = self.client.post("/recipes/", 
            json={
                "product_id": 1,
                "item_id": 1,
                "quantity": 5.0,
                "isTakeout": True
            }
        )
        self.assertIn(response.status_code, [400, 401])

    def test_create_recipe_incomplete_fail(self):
        """Test recipe creation failure due to incomplete data."""
        try:
            auth_header = self._register_and_login()
            self._create_test_data(auth_header)

            response = self.client.post("/recipes/", 
                json={
                    "product_id": self.product_id,
                    "item_id": self.item_id,
                    "quantity": 5.0
                    # Missing isTakeout
                },
                headers=auth_header
            )
            self.assertEqual(response.status_code, 400)
            self.assertIn("error", response.json)
        except ValueError as e:
            self.fail(str(e))

    def test_create_recipe_duplicate_fail(self):
        """Test failure when creating a duplicate recipe."""
        try:
            auth_header = self._register_and_login()
            self._create_test_data(auth_header)

            # First creation
            response1 = self.client.post("/recipes/", 
                json={
                    "product_id": self.product_id,
                    "item_id": self.item_id,
                    "quantity": 5.0,
                    "isTakeout": True
                },
                headers=auth_header
            )
            self.assertEqual(response1.status_code, 201)

            # Duplicate creation
            response2 = self.client.post("/recipes/", 
                json={
                    "product_id": self.product_id,
                    "item_id": self.item_id,
                    "quantity": 5.0,
                    "isTakeout": True
                },
                headers=auth_header
            )
            self.assertEqual(response2.status_code, 409)
        except ValueError as e:
            self.fail(str(e))

    def test_get_all_recipes(self):
        """Test retrieval of all recipes."""
        try:
            auth_header = self._register_and_login()
            response = self.client.get("/recipes/", headers=auth_header)
            self.assertEqual(response.status_code, 200)
            self.assertIsInstance(response.json, list)
        except ValueError as e:
            self.fail(str(e))

    def test_get_recipe_by_product_item_successful(self):
        """Test retrieving a recipe by product_id and item_id."""
        try:
            auth_header = self._register_and_login()
            self._create_test_data(auth_header)

            # Create a recipe first
            create_resp = self.client.post("/recipes/", 
                json={
                    "product_id": self.product_id,
                    "item_id": self.item_id,
                    "quantity": 5.0,
                    "isTakeout": True
                },
                headers=auth_header
            )
            self.assertEqual(create_resp.status_code, 201)

            response = self.client.get(
                f"/recipes/{self.product_id}/{self.item_id}",
                headers=auth_header
            )
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json["product_id"], self.product_id)
            self.assertEqual(response.json["item_id"], self.item_id)
        except ValueError as e:
            self.fail(str(e))

    def test_get_recipe_by_product_item_not_found(self):
        """Test retrieving a recipe that does not exist."""
        try:
            auth_header = self._register_and_login()
            response = self.client.get(
                "/recipes/999/999",
                headers=auth_header
            )
            self.assertEqual(response.status_code, 404)
            self.assertIn("not found", response.json["error"])
        except ValueError as e:
            self.fail(str(e))

    def test_update_recipe_successful(self):
        """Test updating a recipe."""
        try:
            auth_header = self._register_and_login()
            self._create_test_data(auth_header)

            # Create a recipe first
            create_resp = self.client.post("/recipes/", 
                json={
                    "product_id": self.product_id,
                    "item_id": self.item_id,
                    "quantity": 5.0,
                    "isTakeout": True
                },
                headers=auth_header
            )
            self.assertEqual(create_resp.status_code, 201)

            response = self.client.put(
                f"/recipes/{self.product_id}/{self.item_id}",
                json={"quantity": 10.0, "isTakeout": False},
                headers=auth_header
            )
            self.assertEqual(response.status_code, 200)
            self.assertIn("updated successfully", response.json["message"])
        except ValueError as e:
            self.fail(str(e))

    def test_update_recipe_unauthorized(self):
        """Test unauthorized update of recipe."""
        try:
            auth_header = self._register_and_login()
            self._create_test_data(auth_header)

            # Create a recipe first
            create_resp = self.client.post("/recipes/", 
                json={
                    "product_id": self.product_id,
                    "item_id": self.item_id,
                    "quantity": 5.0,
                    "isTakeout": True
                },
                headers=auth_header
            )
            self.assertEqual(create_resp.status_code, 201)

            # Try update without token
            response = self.client.put(
                f"/recipes/{self.product_id}/{self.item_id}",
                json={"quantity": 10.0, "isTakeout": False}
            )
            self.assertIn(response.status_code, [400, 401])
        except ValueError as e:
            self.fail(str(e))

    def test_update_recipe_not_found(self):
        """Test updating a recipe that does not exist."""
        try:
            auth_header = self._register_and_login()
            response = self.client.put(
                "/recipes/999/999",
                json={
                    "quantity": 10.0,
                    "isTakeout": False
                },
                headers=auth_header
            )
            self.assertEqual(response.status_code, 404)
            self.assertIn("not found", response.json["error"])
        except ValueError as e:
            self.fail(str(e))

    def test_delete_recipe_successful(self):
        """Test deleting a recipe."""
        try:
            auth_header = self._register_and_login()
            self._create_test_data(auth_header)

            # Create a recipe first
            create_resp = self.client.post("/recipes/", 
                json={
                    "product_id": self.product_id,
                    "item_id": self.item_id,
                    "quantity": 5.0,
                    "isTakeout": True
                },
                headers=auth_header
            )
            self.assertEqual(create_resp.status_code, 201)

            response = self.client.delete(
                f"/recipes/{self.product_id}/{self.item_id}",
                headers=auth_header
            )
            self.assertEqual(response.status_code, 200)
            self.assertIn("deleted successfully", response.json["message"])
        except ValueError as e:
            self.fail(str(e))

    def test_delete_recipe_unauthorized(self):
        """Test unauthorized deletion of recipe."""
        try:
            auth_header = self._register_and_login()
            self._create_test_data(auth_header)

            # Create a recipe first
            create_resp = self.client.post("/recipes/", 
                json={
                    "product_id": self.product_id,
                    "item_id": self.item_id,
                    "quantity": 5.0,
                    "isTakeout": True
                },
                headers=auth_header
            )
            self.assertEqual(create_resp.status_code, 201)

            # Try delete without token
            response = self.client.delete(
                f"/recipes/{self.product_id}/{self.item_id}"
            )
            self.assertIn(response.status_code, [400, 401])
        except ValueError as e:
            self.fail(str(e))

    def test_delete_recipe_not_found(self):
        """Test deleting a recipe that does not exist."""
        try:
            auth_header = self._register_and_login()
            response = self.client.delete(
                "/recipes/999/999",
                headers=auth_header
            )
            self.assertEqual(response.status_code, 404)
            self.assertIn("not found", response.json["error"])
        except ValueError as e:
            self.fail(str(e))