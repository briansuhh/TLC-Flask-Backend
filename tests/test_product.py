from unittest import TestCase
from api import create_app
from api.extensions import db

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
            # to delete all data from all tables, but not the tables themselves
            for table in reversed(db.metadata.sorted_tables):
                db.session.execute(table.delete())
            db.session.commit()

    def test_create_product_successful(self):
        response = self.client.post("/products/", json={
            "name": "Beef Tapa",
            "variant_group_id": "Beef-Tapa-01",
            "sku": "123456789",
            "category_id": 1
        })

        self.assertEqual(response.status_code, 201, "Product should be created successfully")
    
    def test_create_product_incomplete_fail(self):
        response = self.client.post("/products/", json={
            "name": "Beef Tapa",
            "variant_group_id": "Beef-Tapa-01",
            "sku": "123456789"
        })

        self.assertEqual(response.status_code, 400, "Product creation should fail when required fields are missing")
    
    def test_create_product_duplicate_sku_fail(self):
        self.client.post("/products/", json={
            "name": "Beef Tapa",
            "variant_group_id": "Beef-Tapa-01",
            "sku": "123456789",
            "category_id": 1
        })

        response = self.client.post("/products/", json={
            "name": "Beef Tapa",
            "variant_group_id": "Beef-Tapa-02",
            "sku": "123456789",
            "category_id": 2
        })

        self.assertEqual(response.status_code, 409, "Product creation should fail when SKU already exists")
    
    def test_get_products(self):
        response = self.client.get("/products/")

        self.assertEqual(response.status_code, 200, "Should return list of products")
    
    def test_get_product_by_id_successful(self):
        self.client.post("/products/", json={
            "name": "Beef Tapa",
            "variant_group_id": "Beef-Tapa-01",
            "sku": "123456789",
            "category_id": 1
        })

        response = self.client.get("/products/1")

        self.assertEqual(response.status_code, 200, "Should return product details")
    
    def test_get_product_by_id_not_found(self):
        response = self.client.get("/products/999")

        self.assertEqual(response.status_code, 404, "Should return 404 when product is not found")
    
    def test_update_product_successful(self):
        self.client.post("/products/", json={
            "name": "Beef Tapa",
            "variant_group_id": "Beef-Tapa-01",
            "sku": "123456789",
            "category_id": 1
        })

        response = self.client.put("/products/1", json={
            "name": "Updated Beef Tapa",
            "variant_group_id": "Beef-Tapa-01",
            "sku": "123456789",
            "category_id": 2
        })

        self.assertEqual(response.status_code, 200, "Product should be updated successfully")
    
    def test_update_product_not_found(self):
        response = self.client.put("/products/999", json={
            "name": "Nonexistent Product",
            "variant_group_id": "Nonexistent-Group",
            "sku": "987654321",
            "category_id": 2
        })

        self.assertEqual(response.status_code, 404, "Should return 404 when product is not found")
    
    def test_delete_product_successful(self):
        self.client.post("/products/", json={
            "name": "Beef Tapa",
            "variant_group_id": "Beef-Tapa-01",
            "sku": "123456789",
            "category_id": 1
        })

        response = self.client.delete("/products/1")

        self.assertEqual(response.status_code, 200, "Product should be deleted successfully")
    
    def test_delete_product_not_found(self):
        response = self.client.delete("/products/999")

        self.assertEqual(response.status_code, 404, "Should return 404 when product is not found")

    
    # Product and Tag Association
    def test_add_tag_to_product(self):
        self.client.post("/products/", json={
            "name": "Beef Tapa",
            "variant_group_id": "Beef-Tapa-01",
            "sku": "123456789",
            "category_id": 1
        })
        self.client.post("/tags/", json={"name": "Malupit na Tapa"})
        response = self.client.post("/products/1/tags/", json={"tag_id": 1})
        self.assertEqual(response.status_code, 201, "Tag should be added to product successfully")
    
    def test_add_tag_to_product_not_found(self):
        response = self.client.post("/products/999/tags/", json={"tag_id": 1})
        self.assertEqual(response.status_code, 404, "Should return 404 when product is not found")

    def test_add_tag_to_product_duplicate(self):
        self.client.post("/products/", json={
            "name": "Beef Tapa",
            "variant_group_id": "Beef-Tapa-01",
            "sku": "123456789",
            "category_id": 1
        })
        self.client.post("/tags/", json={"name": "Malupit na Tapa"})
        self.client.post("/products/1/tags/", json={"tag_id": 1})
        response = self.client.post("/products/1/tags/", json={"tag_id": 1})
        self.assertEqual(response.status_code, 409, "Should return 409 when tag is already associated with the product")

    def test_get_product_tags(self):
        self.client.post("/products/", json={
            "name": "Beef Tapa",
            "variant_group_id": "Beef-Tapa-01",
            "sku": "123456789",
            "category_id": 1
        })
        self.client.post("/tags/", json={"name": "Malupit na Tapa"})
        self.client.post("/products/1/tags/", json={"tag_id": 1})
        response = self.client.get("/products/1/tags/")
        self.assertEqual(response.status_code, 200, "Should return list of tags associated with the product")

    def test_get_product_tags_not_found(self):
        response = self.client.get("/products/999/tags/")
        self.assertEqual(response.status_code, 404, "Should return 404 when product is not found")

    def test_get_product_tags_empty(self):
        self.client.post("/products/", json={
            "name": "Beef Tapa",
            "variant_group_id": "Beef-Tapa-01",
            "sku": "123456789",
            "category_id": 1
        })
        response = self.client.get("/products/1/tags/")
        self.assertEqual(response.status_code, 200, "Should return empty list when no tags are associated with the product")

    def test_update_product_tag(self):
        self.client.post("/products/", json={
            "name": "Beef Tapa",
            "variant_group_id": "Beef-Tapa-01",
            "sku": "123456789",
            "category_id": 1
        })
        self.client.post("/tags/", json={"name": "Malupit na Tapa"})
        self.client.post("/products/1/tags/", json={"tag_id": 1})
        response = self.client.put("/products/1/tags/1", json={"tag_id": 2})
        self.assertEqual(response.status_code, 200, "Tag should be updated successfully")

    def test_update_product_tag_not_found(self):
        response = self.client.put("/products/1/tags/999", json={"tag_id": 2})
        self.assertEqual(response.status_code, 404, "Should return 404 when product or tag is not found")

    def test_remove_tag_from_product(self):
        self.client.post("/products/", json={
            "name": "Beef Tapa",
            "variant_group_id": "Beef-Tapa-01",
            "sku": "123456789",
            "category_id": 1
        })
        self.client.post("/tags/", json={"name": "Malupit na Tapa"})
        self.client.post("/products/1/tags/", json={"tag_id": 1})
        response = self.client.delete("/products/1/tags/1")
        self.assertEqual(response.status_code, 200)
    
    def test_remove_tag_not_found(self):
        response = self.client.delete("/products/1/tags/999")
        self.assertEqual(response.status_code, 404)