from unittest import TestCase
from api import create_app
from api.extensions import db
import json

class ProductTestCase(TestCase):
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

    def test_create_product_successful(self):
        try:
            auth_header = {"Authorization": self._register_and_login()}
            response = self.client.post("/products/", 
                json={
                    "name": "Beef Tapa",
                    "variant_group_id": "Beef-Tapa-01",
                    "sku": "123456789",
                    "category_id": 1
                },
                headers=auth_header
            )
            self.assertEqual(response.status_code, 201, "Product should be created successfully")
        except ValueError as e:
            self.fail(str(e))
    
    def test_create_product_unauthorized(self):
        response = self.client.post("/products/", 
            json={
                "name": "Beef Tapa",
                "variant_group_id": "Beef-Tapa-01",
                "sku": "123456789",
                "category_id": 1
            }
        )
        self.assertIn(response.status_code, [400, 401], "Should fail without authentication")
    
    def test_create_product_incomplete_fail(self):
        try:
            auth_header = {"Authorization": self._register_and_login()}
            response = self.client.post("/products/", 
                json={
                    "name": "Beef Tapa",
                    "variant_group_id": "Beef-Tapa-01",
                    "sku": "123456789"
                },
                headers=auth_header
            )
            self.assertEqual(response.status_code, 400, "Product creation should fail when required fields are missing")
        except ValueError as e:
            self.fail(str(e))
    
    def test_create_product_duplicate_sku_fail(self):
        try:
            auth_header = {"Authorization": self._register_and_login()}
            self.client.post("/products/", 
                json={
                    "name": "Beef Tapa",
                    "variant_group_id": "Beef-Tapa-01",
                    "sku": "123456789",
                    "category_id": 1
                },
                headers=auth_header
            )

            response = self.client.post("/products/", 
                json={
                    "name": "Beef Tapa",
                    "variant_group_id": "Beef-Tapa-02",
                    "sku": "123456789",
                    "category_id": 2
                },
                headers=auth_header
            )
            self.assertEqual(response.status_code, 409, "Product creation should fail when SKU already exists")
        except ValueError as e:
            self.fail(str(e))
    
    def test_get_products(self):
        try:
            auth_header = {"Authorization": self._register_and_login()}
            response = self.client.get("/products/", headers=auth_header)
            self.assertEqual(response.status_code, 200, "Should return list of products")
        except ValueError as e:
            self.fail(str(e))

    def test_get_products_unauthorized(self):
        response = self.client.get("/products/")
        self.assertIn(response.status_code, [400, 401], "Should fail without authentication")
    
    def test_get_product_by_id_successful(self):
        try:
            auth_header = {"Authorization": self._register_and_login()}
            self.client.post("/products/", 
                json={
                    "name": "Beef Tapa",
                    "variant_group_id": "Beef-Tapa-01",
                    "sku": "123456789",
                    "category_id": 1
                },
                headers=auth_header
            )

            response = self.client.get("/products/1", headers=auth_header)
            self.assertEqual(response.status_code, 200, "Should return product details")
        except ValueError as e:
            self.fail(str(e))

    def test_get_product_by_id_unauthorized(self):
        try:
            auth_header = {"Authorization": self._register_and_login()}
            self.client.post("/products/", 
                json={
                    "name": "Beef Tapa",
                    "variant_group_id": "Beef-Tapa-01",
                    "sku": "123456789",
                    "category_id": 1
                },
                headers=auth_header
            )

            # Try GET without token
            response = self.client.get("/products/1")
            self.assertIn(response.status_code, [400, 401], "Should fail without authentication")
        except ValueError as e:
            self.fail(str(e))
    
    def test_get_product_by_id_not_found(self):
        try:
            auth_header = {"Authorization": self._register_and_login()}
            response = self.client.get("/products/999", headers=auth_header)
            self.assertEqual(response.status_code, 404, "Should return 404 when product is not found")
        except ValueError as e:
            self.fail(str(e))
    
    def test_update_product_successful(self):
        try:
            auth_header = {"Authorization": self._register_and_login()}
            self.client.post("/products/", 
                json={
                    "name": "Beef Tapa",
                    "variant_group_id": "Beef-Tapa-01",
                    "sku": "123456789",
                    "category_id": 1
                },
                headers=auth_header
            )

            response = self.client.put("/products/1", 
                json={
                    "name": "Updated Beef Tapa",
                    "variant_group_id": "Beef-Tapa-01",
                    "sku": "123456789",
                    "category_id": 2
                },
                headers=auth_header
            )
            self.assertEqual(response.status_code, 200, "Product should be updated successfully")
        except ValueError as e:
            self.fail(str(e))

    def test_update_product_unauthorized(self):
        try:
            auth_header = {"Authorization": self._register_and_login()}
            self.client.post("/products/", 
                json={
                    "name": "Beef Tapa",
                    "variant_group_id": "Beef-Tapa-01",
                    "sku": "123456789",
                    "category_id": 1
                },
                headers=auth_header
            )

            # Try update without token
            response = self.client.put("/products/1", 
                json={
                    "name": "Updated Beef Tapa",
                    "variant_group_id": "Beef-Tapa-01",
                    "sku": "123456789",
                    "category_id": 2
                }
            )
            self.assertIn(response.status_code, [400, 401], "Should fail without authentication")
        except ValueError as e:
            self.fail(str(e))

    def test_update_product_not_found(self):
        try:
            auth_header = {"Authorization": self._register_and_login()}
            response = self.client.put("/products/999", 
                json={
                    "name": "Nonexistent Product",
                    "variant_group_id": "Nonexistent-Group",
                    "sku": "987654321",
                    "category_id": 2
                },
                headers=auth_header
            )
            self.assertEqual(response.status_code, 404, "Should return 404 when product is not found")
        except ValueError as e:
            self.fail(str(e))
    
    def test_delete_product_successful(self):
        try:
            auth_header = {"Authorization": self._register_and_login()}
            self.client.post("/products/", 
                json={
                    "name": "Beef Tapa",
                    "variant_group_id": "Beef-Tapa-01",
                    "sku": "123456789",
                    "category_id": 1
                },
                headers=auth_header
            )

            response = self.client.delete("/products/1", headers=auth_header)
            self.assertEqual(response.status_code, 200, "Product should be deleted successfully")
        except ValueError as e:
            self.fail(str(e))

    def test_delete_product_unauthorized(self):
        try:
            auth_header = {"Authorization": self._register_and_login()}
            self.client.post("/products/", 
                json={
                    "name": "Beef Tapa",
                    "variant_group_id": "Beef-Tapa-01",
                    "sku": "123456789",
                    "category_id": 1
                },
                headers=auth_header
            )

            # Try delete without token
            response = self.client.delete("/products/1")
            self.assertIn(response.status_code, [400, 401], "Should fail without authentication")
        except ValueError as e:
            self.fail(str(e))
    
    def test_delete_product_not_found(self):
        try:
            auth_header = {"Authorization": self._register_and_login()}
            response = self.client.delete("/products/999", headers=auth_header)
            self.assertEqual(response.status_code, 404, "Should return 404 when product is not found")
        except ValueError as e:
            self.fail(str(e))
    
    # Product and Tag Association
    def test_add_tag_to_product(self):
        try:
            auth_header = {"Authorization": self._register_and_login()}
            self.client.post("/products/", 
                json={
                    "name": "Beef Tapa",
                    "variant_group_id": "Beef-Tapa-01",
                    "sku": "123456789",
                    "category_id": 1
                },
                headers=auth_header
            )
            self.client.post("/tags/", 
                json={"name": "Malupit na Tapa"},
                headers=auth_header
            )
            response = self.client.post("/products/1/tags/", 
                json={"tag_id": 1},
                headers=auth_header
            )
            self.assertEqual(response.status_code, 201, "Tag should be added to product successfully")
        except ValueError as e:
            self.fail(str(e))
    
    def test_add_tag_to_product_not_found(self):
        try:
            auth_header = {"Authorization": self._register_and_login()}
            response = self.client.post("/products/999/tags/", 
                json={"tag_id": 1},
                headers=auth_header
            )
            self.assertEqual(response.status_code, 404, "Should return 404 when product is not found")
        except ValueError as e:
            self.fail(str(e))

    def test_add_tag_to_product_duplicate(self):
        try:
            auth_header = {"Authorization": self._register_and_login()}
            self.client.post("/products/", 
                json={
                    "name": "Beef Tapa",
                    "variant_group_id": "Beef-Tapa-01",
                    "sku": "123456789",
                    "category_id": 1
                },
                headers=auth_header
            )
            self.client.post("/tags/", 
                json={"name": "Malupit na Tapa"},
                headers=auth_header
            )
            self.client.post("/products/1/tags/", 
                json={"tag_id": 1},
                headers=auth_header
            )
            response = self.client.post("/products/1/tags/", 
                json={"tag_id": 1},
                headers=auth_header
            )
            self.assertEqual(response.status_code, 409, "Should return 409 when tag is already associated with the product")
        except ValueError as e:
            self.fail(str(e))

    def test_get_product_tags(self):
        try:
            auth_header = {"Authorization": self._register_and_login()}
            self.client.post("/products/", 
                json={
                    "name": "Beef Tapa",
                    "variant_group_id": "Beef-Tapa-01",
                    "sku": "123456789",
                    "category_id": 1
                },
                headers=auth_header
            )
            self.client.post("/tags/", 
                json={"name": "Malupit na Tapa"},
                headers=auth_header
            )
            self.client.post("/products/1/tags/", 
                json={"tag_id": 1},
                headers=auth_header
            )
            response = self.client.get("/products/1/tags/", headers=auth_header)
            self.assertEqual(response.status_code, 200, "Should return list of tags associated with the product")
        except ValueError as e:
            self.fail(str(e))

    def test_get_product_tags_not_found(self):
        try:
            auth_header = {"Authorization": self._register_and_login()}
            response = self.client.get("/products/999/tags/", headers=auth_header)
            self.assertEqual(response.status_code, 404, "Should return 404 when product is not found")
        except ValueError as e:
            self.fail(str(e))

    def test_get_product_tags_empty(self):
        try:
            auth_header = {"Authorization": self._register_and_login()}
            self.client.post("/products/", 
                json={
                    "name": "Beef Tapa",
                    "variant_group_id": "Beef-Tapa-01",
                    "sku": "123456789",
                    "category_id": 1
                },
                headers=auth_header
            )
            response = self.client.get("/products/1/tags/", headers=auth_header)
            self.assertEqual(response.status_code, 200, "Should return empty list when no tags are associated with the product")
        except ValueError as e:
            self.fail(str(e))

    def test_update_product_tag(self):
        try:
            auth_header = {"Authorization": self._register_and_login()}
            self.client.post("/products/", 
                json={
                    "name": "Beef Tapa",
                    "variant_group_id": "Beef-Tapa-01",
                    "sku": "123456789",
                    "category_id": 1
                },
                headers=auth_header
            )
            self.client.post("/tags/", 
                json={"name": "Malupit na Tapa"},
                headers=auth_header
            )
            self.client.post("/products/1/tags/", 
                json={"tag_id": 1},
                headers=auth_header
            )
            response = self.client.put("/products/1/tags/1", 
                json={"tag_id": 2},
                headers=auth_header
            )
            self.assertEqual(response.status_code, 200, "Tag should be updated successfully")
        except ValueError as e:
            self.fail(str(e))

    def test_update_product_tag_not_found(self):
        try:
            auth_header = {"Authorization": self._register_and_login()}
            response = self.client.put("/products/1/tags/999", 
                json={"tag_id": 2},
                headers=auth_header
            )
            self.assertEqual(response.status_code, 404, "Should return 404 when product or tag is not found")
        except ValueError as e:
            self.fail(str(e))

    def test_remove_tag_from_product(self):
        try:
            auth_header = {"Authorization": self._register_and_login()}
            self.client.post("/products/", 
                json={
                    "name": "Beef Tapa",
                    "variant_group_id": "Beef-Tapa-01",
                    "sku": "123456789",
                    "category_id": 1
                },
                headers=auth_header
            )
            self.client.post("/tags/", 
                json={"name": "Malupit na Tapa"},
                headers=auth_header
            )
            self.client.post("/products/1/tags/", 
                json={"tag_id": 1},
                headers=auth_header
            )
            response = self.client.delete("/products/1/tags/1", headers=auth_header)
            self.assertEqual(response.status_code, 200)
        except ValueError as e:
            self.fail(str(e))
    
    def test_remove_tag_not_found(self):
        try:
            auth_header = {"Authorization": self._register_and_login()}
            response = self.client.delete("/products/1/tags/999", headers=auth_header)
            self.assertEqual(response.status_code, 404)
        except ValueError as e:
            self.fail(str(e))