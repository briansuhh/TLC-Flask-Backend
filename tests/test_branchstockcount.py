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

    def _create_test_data(self, auth_header):
        """Helper function to create test data."""
        try:
            # Create branch
            branch_resp = self.client.post("/branches/", 
                json={
                    "name": "Branch 1",
                    "address": "123 Test St."
                },
                headers=auth_header
            )
            self.assertEqual(branch_resp.status_code, 201)
            self.branch_id = json.loads(branch_resp.data).get('branch_id', 1)

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

    def test_create_branch_stock_count_successful(self):
        """Test successful creation of branch stock count."""
        try:
            auth_header = {"Authorization": self._register_and_login()}
            self._create_test_data(auth_header)

            response = self.client.post("/branchstockcounts/", 
                json={
                    "branch_id": self.branch_id,
                    "item_id": self.item_id,
                    "in_stock": 100.0,
                    "ordered_qty": 20.0
                },
                headers=auth_header
            )

            self.assertEqual(response.status_code, 201)
            self.assertIn("created successfully", response.json["message"])
        except ValueError as e:
            self.fail(str(e))

    def test_create_branch_stock_count_unauthorized(self):
        """Test unauthorized creation of branch stock count."""
        response = self.client.post("/branchstockcounts/", 
            json={
                "branch_id": 1,
                "item_id": 1,
                "in_stock": 100.0,
                "ordered_qty": 20.0
            }
        )
        self.assertIn(response.status_code, [400, 401])

    def test_create_branch_stock_count_incomplete_fail(self):
        """Test branch stock count creation failure due to incomplete data."""
        try:
            auth_header = {"Authorization": self._register_and_login()}
            response = self.client.post("/branchstockcounts/", 
                json={
                    "branch_id": 1,
                    "item_id": 1,
                    "in_stock": 100.0  # Missing ordered_qty
                },
                headers=auth_header
            )
            self.assertEqual(response.status_code, 400)
            self.assertIn("error", response.json)
        except ValueError as e:
            self.fail(str(e))

    def test_create_branch_stock_count_duplicate_fail(self):
        """Test failure when creating a duplicate branch stock count."""
        try:
            auth_header = {"Authorization": self._register_and_login()}
            self._create_test_data(auth_header)

            # First creation
            response1 = self.client.post("/branchstockcounts/", 
                json={
                    "branch_id": self.branch_id,
                    "item_id": self.item_id,
                    "in_stock": 100.0,
                    "ordered_qty": 20.0
                },
                headers=auth_header
            )
            self.assertEqual(response1.status_code, 201)

            # Duplicate creation
            response2 = self.client.post("/branchstockcounts/", 
                json={
                    "branch_id": self.branch_id,
                    "item_id": self.item_id,
                    "in_stock": 100.0,
                    "ordered_qty": 20.0
                },
                headers=auth_header
            )
            self.assertEqual(response2.status_code, 409)
        except ValueError as e:
            self.fail(str(e))

    def test_get_all_branch_stock_counts(self):
        """Test retrieval of all branch stock counts."""
        try:
            auth_header = {"Authorization": self._register_and_login()}
            response = self.client.get("/branchstockcounts/", headers=auth_header)
            self.assertEqual(response.status_code, 200)
            self.assertIsInstance(response.json, list)
        except ValueError as e:
            self.fail(str(e))

    def test_get_branch_stock_count_by_ids(self):
        """Test retrieving a branch stock count by branch_id and item_id."""
        try:
            auth_header = {"Authorization": self._register_and_login()}
            self._create_test_data(auth_header)

            # Create a stock count first
            create_resp = self.client.post("/branchstockcounts/", 
                json={
                    "branch_id": self.branch_id,
                    "item_id": self.item_id,
                    "in_stock": 100.0,
                    "ordered_qty": 20.0
                },
                headers=auth_header
            )
            self.assertEqual(create_resp.status_code, 201)

            response = self.client.get(
                f"/branchstockcounts/{self.branch_id}/{self.item_id}",
                headers=auth_header
            )
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json["branch_id"], self.branch_id)
            self.assertEqual(response.json["item_id"], self.item_id)
        except ValueError as e:
            self.fail(str(e))

    def test_get_branch_stock_count_not_found(self):
        """Test retrieving a branch stock count that does not exist."""
        try:
            auth_header = {"Authorization": self._register_and_login()}
            response = self.client.get(
                "/branchstockcounts/999/999",
                headers=auth_header
            )
            self.assertEqual(response.status_code, 404)
            self.assertIn("not found", response.json["error"])
        except ValueError as e:
            self.fail(str(e))

    def test_update_branch_stock_count(self):
        """Test updating a branch stock count."""
        try:
            auth_header = {"Authorization": self._register_and_login()}
            self._create_test_data(auth_header)

            # Create a stock count first
            create_resp = self.client.post("/branchstockcounts/", 
                json={
                    "branch_id": self.branch_id,
                    "item_id": self.item_id,
                    "in_stock": 100.0,
                    "ordered_qty": 20.0
                },
                headers=auth_header
            )
            self.assertEqual(create_resp.status_code, 201)

            response = self.client.put(
                f"/branchstockcounts/{self.branch_id}/{self.item_id}",
                json={"in_stock": 150.0, "ordered_qty": 30.0},
                headers=auth_header
            )
            self.assertEqual(response.status_code, 200)
            self.assertIn("updated successfully", response.json["message"])
        except ValueError as e:
            self.fail(str(e))

    def test_update_branch_stock_count_unauthorized(self):
        """Test unauthorized update of branch stock count."""
        try:
            auth_header = {"Authorization": self._register_and_login()}
            self._create_test_data(auth_header)

            # Create a stock count first
            create_resp = self.client.post("/branchstockcounts/", 
                json={
                    "branch_id": self.branch_id,
                    "item_id": self.item_id,
                    "in_stock": 100.0,
                    "ordered_qty": 20.0
                },
                headers=auth_header
            )
            self.assertEqual(create_resp.status_code, 201)

            # Try update without token
            response = self.client.put(
                f"/branchstockcounts/{self.branch_id}/{self.item_id}",
                json={"in_stock": 150.0, "ordered_qty": 30.0}
            )
            self.assertIn(response.status_code, [400, 401])
        except ValueError as e:
            self.fail(str(e))

    def test_update_branch_stock_count_not_found(self):
        """Test updating a branch stock count that does not exist."""
        try:
            auth_header = {"Authorization": self._register_and_login()}
            response = self.client.put(
                "/branchstockcounts/999/999",
                json={
                    "in_stock": 150.0,
                    "ordered_qty": 30.0
                },
                headers=auth_header
            )
            self.assertEqual(response.status_code, 404)
            self.assertIn("not found", response.json["error"])
        except ValueError as e:
            self.fail(str(e))

    def test_delete_branch_stock_count(self):
        """Test deleting a branch stock count."""
        try:
            auth_header = {"Authorization": self._register_and_login()}
            self._create_test_data(auth_header)

            # Create a stock count first
            create_resp = self.client.post("/branchstockcounts/", 
                json={
                    "branch_id": self.branch_id,
                    "item_id": self.item_id,
                    "in_stock": 100.0,
                    "ordered_qty": 20.0
                },
                headers=auth_header
            )
            self.assertEqual(create_resp.status_code, 201)

            response = self.client.delete(
                f"/branchstockcounts/{self.branch_id}/{self.item_id}",
                headers=auth_header
            )
            self.assertEqual(response.status_code, 200)
            self.assertIn("deleted successfully", response.json["message"])
        except ValueError as e:
            self.fail(str(e))

    def test_delete_branch_stock_count_unauthorized(self):
        """Test unauthorized deletion of branch stock count."""
        try:
            auth_header = {"Authorization": self._register_and_login()}
            self._create_test_data(auth_header)

            # Create a stock count first
            create_resp = self.client.post("/branchstockcounts/", 
                json={
                    "branch_id": self.branch_id,
                    "item_id": self.item_id,
                    "in_stock": 100.0,
                    "ordered_qty": 20.0
                },
                headers=auth_header
            )
            self.assertEqual(create_resp.status_code, 201)

            # Try delete without token
            response = self.client.delete(
                f"/branchstockcounts/{self.branch_id}/{self.item_id}"
            )
            self.assertIn(response.status_code, [400, 401])
        except ValueError as e:
            self.fail(str(e))

    def test_delete_branch_stock_count_not_found(self):
        """Test deleting a branch stock count that does not exist."""
        try:
            auth_header = {"Authorization": self._register_and_login()}
            response = self.client.delete(
                "/branchstockcounts/999/999",
                headers=auth_header
            )
            self.assertEqual(response.status_code, 404)
            self.assertIn("not found", response.json["error"])
        except ValueError as e:
            self.fail(str(e))