from unittest import TestCase
from api import create_app
from api.extensions import db
import json

class BranchStockCountTestCase(TestCase):
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
            # Delete all data from all tables, but not the tables themselves
            for table in reversed(db.metadata.sorted_tables):
                db.session.execute(table.delete())
            db.session.commit()

    def _create_test_data(self):
        """Helper function to create test data."""
        try:
            # Create branch
            branch_resp = self.client.post("/branches/", json={
                "name": "Branch 1",
                "address": "123 Test St."
            })
            self.assertEqual(branch_resp.status_code, 201)
            self.branch_id = json.loads(branch_resp.data).get('branch_id', 1)

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

    def test_create_branch_stock_count_successful(self):
        """Test successful creation of branch stock count."""
        self._create_test_data()

        response = self.client.post("/branchstockcounts/", json={
            "branch_id": self.branch_id,
            "item_id": self.item_id,
            "in_stock": 100.0,
            "ordered_qty": 20.0
        })

        self.assertEqual(response.status_code, 201)
        self.assertIn("created successfully", response.json["message"])

    def test_create_branch_stock_count_incomplete_fail(self):
        """Test branch stock count creation failure due to incomplete data."""
        response = self.client.post("/branchstockcounts/", json={
            "branch_id": 1,
            "item_id": 1,
            "in_stock": 100.0  # Missing ordered_qty
        })
        self.assertEqual(response.status_code, 400)
        self.assertIn("error", response.json)

    def test_create_branch_stock_count_duplicate_fail(self):
        """Test failure when creating a duplicate branch stock count."""
        self._create_test_data()

        # First creation
        response1 = self.client.post("/branchstockcounts/", json={
            "branch_id": self.branch_id,
            "item_id": self.item_id,
            "in_stock": 100.0,
            "ordered_qty": 20.0
        })
        self.assertEqual(response1.status_code, 201)

        # Duplicate creation
        response2 = self.client.post("/branchstockcounts/", json={
            "branch_id": self.branch_id,
            "item_id": self.item_id,
            "in_stock": 100.0,
            "ordered_qty": 20.0
        })
        self.assertEqual(response2.status_code, 409)

    def test_get_all_branch_stock_counts(self):
        """Test retrieval of all branch stock counts."""
        response = self.client.get("/branchstockcounts/")
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json, list)

    def test_get_branch_stock_count_by_ids(self):
        """Test retrieving a branch stock count by branch_id and item_id."""
        self._create_test_data()

        # Create a stock count first
        create_resp = self.client.post("/branchstockcounts/", json={
            "branch_id": self.branch_id,
            "item_id": self.item_id,
            "in_stock": 100.0,
            "ordered_qty": 20.0
        })
        self.assertEqual(create_resp.status_code, 201)

        response = self.client.get(f"/branchstockcounts/{self.branch_id}/{self.item_id}")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json["branch_id"], self.branch_id)
        self.assertEqual(response.json["item_id"], self.item_id)

    def test_get_branch_stock_count_not_found(self):
        """Test retrieving a branch stock count that does not exist."""
        response = self.client.get("/branchstockcounts/999/999")
        self.assertEqual(response.status_code, 404)
        self.assertIn("not found", response.json["error"])

    def test_update_branch_stock_count(self):
        """Test updating a branch stock count."""
        self._create_test_data()

        # Create a stock count first
        create_resp = self.client.post("/branchstockcounts/", json={
            "branch_id": self.branch_id,
            "item_id": self.item_id,
            "in_stock": 100.0,
            "ordered_qty": 20.0
        })
        self.assertEqual(create_resp.status_code, 201)

        response = self.client.put(
            f"/branchstockcounts/{self.branch_id}/{self.item_id}",
            json={"in_stock": 150.0, "ordered_qty": 30.0}
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn("updated successfully", response.json["message"])

    def test_update_branch_stock_count_not_found(self):
        """Test updating a branch stock count that does not exist."""
        response = self.client.put("/branchstockcounts/999/999", json={
            "in_stock": 150.0,
            "ordered_qty": 30.0
        })
        self.assertEqual(response.status_code, 404)
        self.assertIn("not found", response.json["error"])

    def test_delete_branch_stock_count(self):
        """Test deleting a branch stock count."""
        self._create_test_data()

        # Create a stock count first
        create_resp = self.client.post("/branchstockcounts/", json={
            "branch_id": self.branch_id,
            "item_id": self.item_id,
            "in_stock": 100.0,
            "ordered_qty": 20.0
        })
        self.assertEqual(create_resp.status_code, 201)

        response = self.client.delete(f"/branchstockcounts/{self.branch_id}/{self.item_id}")
        self.assertEqual(response.status_code, 200)
        self.assertIn("deleted successfully", response.json["message"])

    def test_delete_branch_stock_count_not_found(self):
        """Test deleting a branch stock count that does not exist."""
        response = self.client.delete("/branchstockcounts/999/999")
        self.assertEqual(response.status_code, 404)
        self.assertIn("not found", response.json["error"])
