from unittest import TestCase
from api import create_app
from api.extensions import db
import json

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
            for table in reversed(db.metadata.sorted_tables):
                db.session.execute(table.delete())
            db.session.commit()
    
    def _register_and_login(self):
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
        
        # Check if registration was successful
        if register_response.status_code != 201:
            raise ValueError(f"Registration failed: {register_response.data}")
        
        # Login and get token
        login_response = self.client.post("/auth/login", json={
            "email": "cashier@gmail.com",
            "password": "password"
        })
        
        # Parse the JSON response
        login_data = json.loads(login_response.data)
        
        # Check if login was successful and contains token
        if login_response.status_code != 200 or 'access_token' not in login_data:
            raise ValueError(f"Login failed: {login_data}")
            
        return f"Bearer {login_data['access_token']}"

    # Test cases with authentication
    def test_create_branch_successful(self):
        try:
            auth_header = {"Authorization": self._register_and_login()}
            response = self.client.post("/branches/", 
                json={
                    "name": "TLC Mandaluyong",
                    "address": "124 Mandaluyong mandaluyon mandaluyong"
                },
                headers=auth_header
            )
            self.assertEqual(response.status_code, 201)
        except ValueError as e:
            self.fail(str(e))
    
    def test_create_branch_unauthorized(self):
        response = self.client.post("/branches/", 
            json={
                "name": "TLC Mandaluyong",
                "address": "124 Mandaluyong mandaluyon mandaluyong"
            }
        )
        # Some APIs return 400 for missing auth, others return 401
        self.assertIn(response.status_code, [400, 401])
    
    def test_create_branch_incomplete_fail(self):
        try:
            auth_header = {"Authorization": self._register_and_login()}
            response = self.client.post("/branches/", 
                json={"name": "TLC Mandaluyong"},
                headers=auth_header
            )
            self.assertEqual(response.status_code, 400)
        except ValueError as e:
            self.fail(str(e))
    
    def test_create_branch_duplicate_name_fail(self):
        try:
            auth_header = {"Authorization": self._register_and_login()}
            
            # First create
            self.client.post("/branches/", 
                json={
                    "name": "TLC Mandaluyong",
                    "address": "124 Mandaluyong mandaluyon mandaluyong"
                },
                headers=auth_header
            )

            # Try duplicate
            response = self.client.post("/branches/", 
                json={
                    "name": "TLC Mandaluyong",
                    "address": "124 Manila manila manila"
                },
                headers=auth_header
            )
            self.assertEqual(response.status_code, 409)
        except ValueError as e:
            self.fail(str(e))
    
    def test_create_branch_duplicate_address_fail(self):
        try:
            auth_header = {"Authorization": self._register_and_login()}
            
            self.client.post("/branches/", 
                json={
                    "name": "TLC Mandaluyong",
                    "address": "124 Mandaluyong mandaluyon mandaluyong"
                },
                headers=auth_header
            )

            response = self.client.post("/branches/", 
                json={
                    "name": "TLC Manila",
                    "address": "124 Mandaluyong mandaluyon mandaluyong"
                },
                headers=auth_header
            )
            self.assertEqual(response.status_code, 409)
        except ValueError as e:
            self.fail(str(e))
    
    def test_update_branch_successful(self):
        try:
            auth_header = {"Authorization": self._register_and_login()}
            
            self.client.post("/branches/", 
                json={
                    "name": "TLC Mandaluyong",
                    "address": "124 Mandaluyong mandaluyon mandaluyong"
                },
                headers=auth_header
            )

            response = self.client.put("/branches/1", 
                json={
                    "name": "Updated TLC Mandaluyong",
                    "address": "Updated 124 Mandaluyong mandaluyon mandaluyong"
                },
                headers=auth_header
            )
            self.assertEqual(response.status_code, 200)
        except ValueError as e:
            self.fail(str(e))
    
    def test_update_branch_unauthorized(self):
        try:
            auth_header = {"Authorization": self._register_and_login()}
            
            # Create branch first
            self.client.post("/branches/", 
                json={
                    "name": "TLC Mandaluyong",
                    "address": "124 Mandaluyong mandaluyon mandaluyong"
                },
                headers=auth_header
            )

            # Try update without token
            response = self.client.put("/branches/1", 
                json={
                    "name": "Updated TLC Mandaluyong",
                    "address": "Updated 124 Mandaluyong mandaluyon mandaluyong"
                }
            )
            self.assertIn(response.status_code, [400, 401])
        except ValueError as e:
            self.fail(str(e))
    
    def test_delete_branch_successful(self):
        try:
            auth_header = {"Authorization": self._register_and_login()}
            
            self.client.post("/branches/", 
                json={
                    "name": "TLC Mandaluyong",
                    "address": "124 Mandaluyong mandaluyon mandaluyong"
                },
                headers=auth_header
            )

            response = self.client.delete("/branches/1", headers=auth_header)
            self.assertEqual(response.status_code, 200)
        except ValueError as e:
            self.fail(str(e))
    
    def test_delete_branch_unauthorized(self):
        try:
            auth_header = {"Authorization": self._register_and_login()}
            
            # Create branch first
            self.client.post("/branches/", 
                json={
                    "name": "TLC Mandaluyong",
                    "address": "124 Mandaluyong mandaluyon mandaluyong"
                },
                headers=auth_header
            )

            # Try delete without token
            response = self.client.delete("/branches/1")
            self.assertIn(response.status_code, [400, 401])
        except ValueError as e:
            self.fail(str(e))

    def test_get_branches(self):
        try:
            auth_header = {"Authorization": self._register_and_login()}
            response = self.client.get("/branches/", headers=auth_header)
            self.assertEqual(response.status_code, 200)
        except ValueError as e:
            self.fail(str(e))
    
    def test_get_branch_by_id_successful(self):
        try:
            auth_header = {"Authorization": self._register_and_login()}
            
            self.client.post("/branches/", 
                json={
                    "name": "TLC Mandaluyong",
                    "address": "124 Mandaluyong mandaluyon mandaluyong"
                },
                headers=auth_header
            )

            response = self.client.get("/branches/1", headers=auth_header)
            self.assertEqual(response.status_code, 200)
        except ValueError as e:
            self.fail(str(e))
    
    def test_get_branch_by_id_not_found(self):
        auth_header = {"Authorization": self._register_and_login()}
        response = self.client.get("/branches/999", headers=auth_header)
        self.assertEqual(response.status_code, 404)
    
    def test_update_branch_not_found(self):
        try:
            auth_header = {"Authorization": self._register_and_login()}
            response = self.client.put("/branches/999", 
                json={
                    "name": "Nonexistent Branch",
                    "address": "Nonexistent Address"
                },
                headers=auth_header
            )
            self.assertEqual(response.status_code, 404)
        except ValueError as e:
            self.fail(str(e))
    
    def test_delete_branch_not_found(self):
        try:
            auth_header = {"Authorization": self._register_and_login()}
            response = self.client.delete("/branches/999", headers=auth_header)
            self.assertEqual(response.status_code, 404)
        except ValueError as e:
            self.fail(str(e))