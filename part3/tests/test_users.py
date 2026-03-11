import unittest
from flask_jwt_extended import create_access_token
from app import create_app, db
from app.models.user import User


class TestUserEndpoints(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = create_app("config.TestingConfig")
        cls.client = cls.app.test_client()

        with cls.app.app_context():
            db.drop_all()
            db.create_all()

            admin = User(
                first_name="Admin",
                last_name="User",
                email="admin@example.com",
                is_admin=True
            )
            admin.hash_password("adminpass")

            normal_user = User(
                first_name="Normal",
                last_name="User",
                email="user@example.com",
                is_admin=False
            )
            normal_user.hash_password("userpass")

            target_user = User(
                first_name="Target",
                last_name="User",
                email="target@example.com",
                is_admin=False
            )
            target_user.hash_password("targetpass")

            db.session.add_all([admin, normal_user, target_user])
            db.session.commit()

            cls.admin_id = str(admin.id)
            cls.normal_user_id = str(normal_user.id)
            cls.target_user_id = str(target_user.id)

            cls.admin_token = create_access_token(
                identity=cls.admin_id,
                additional_claims={"is_admin": True}
            )
            cls.user_token = create_access_token(
                identity=cls.normal_user_id,
                additional_claims={"is_admin": False}
            )

    @classmethod
    def tearDownClass(cls):
        with cls.app.app_context():
            db.session.remove()
            db.drop_all()

    def test_get_users_returns_200(self):
        response = self.client.get("/api/v1/users/")
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.get_json(), list)

    def test_get_nonexistent_user_returns_404(self):
        response = self.client.get("/api/v1/users/nonexistent-id")
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.get_json(), {"error": "User not found"})

    def test_create_user_without_token_returns_401(self):
        response = self.client.post(
            "/api/v1/users/",
            json={
                "first_name": "New",
                "last_name": "User",
                "email": "new@example.com",
                "password": "newpass123"
            },
            content_type="application/json"
        )
        self.assertEqual(response.status_code, 401)

    def test_create_user_with_non_admin_returns_403(self):
        response = self.client.post(
            "/api/v1/users/",
            json={
                "first_name": "New",
                "last_name": "User",
                "email": "new@example.com",
                "password": "newpass123"
            },
            headers={"Authorization": f"Bearer {self.user_token}"},
            content_type="application/json"
        )
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.get_json(), {"error": "Admin access required"})

    def test_create_user_with_admin_returns_201(self):
        response = self.client.post(
            "/api/v1/users/",
            json={
                "first_name": "Created",
                "last_name": "ByAdmin",
                "email": "created@example.com",
                "password": "createdpass123"
            },
            headers={"Authorization": f"Bearer {self.admin_token}"},
            content_type="application/json"
        )
        self.assertEqual(response.status_code, 201)

    def test_update_other_user_by_non_admin_returns_403(self):
        response = self.client.put(
            f"/api/v1/users/{self.target_user_id}",
            json={"first_name": "Hacked"},
            headers={"Authorization": f"Bearer {self.user_token}"},
            content_type="application/json"
        )
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.get_json(), {"error": "Unauthorized action"})

    def test_non_admin_cannot_modify_email_or_password(self):
        response = self.client.put(
            f"/api/v1/users/{self.normal_user_id}",
            json={"email": "changed@example.com"},
            headers={"Authorization": f"Bearer {self.user_token}"},
            content_type="application/json"
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.get_json(), {"error": "Cannot modify email or password"})

    def test_admin_can_update_user(self):
        response = self.client.put(
            f"/api/v1/users/{self.target_user_id}",
            json={"first_name": "UpdatedByAdmin"},
            headers={"Authorization": f"Bearer {self.admin_token}"},
            content_type="application/json"
        )
        self.assertEqual(response.status_code, 200)

    def test_user_can_update_own_name_fields(self):
        response = self.client.put(
            f"/api/v1/users/{self.normal_user_id}",
            json={"first_name": "Updated", "last_name": "Self"},
            headers={"Authorization": f"Bearer {self.user_token}"},
            content_type="application/json"
        )
        self.assertEqual(response.status_code, 200)


class TestUserModel(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = create_app("config.TestingConfig")

    def test_password_hashing(self):
        with self.app.app_context():
            user = User(
                first_name="Hash",
                last_name="Test",
                email="hash@test.com"
            )
            user.hash_password("mypassword123")
            self.assertNotEqual(user.password, "mypassword123")
            self.assertIsNotNone(user.password)

    def test_password_verification(self):
        with self.app.app_context():
            user = User(
                first_name="Verify",
                last_name="Test",
                email="verify@test.com"
            )
            user.hash_password("correctpassword")
            self.assertTrue(user.verify_password("correctpassword"))
            self.assertFalse(user.verify_password("wrongpassword"))


if __name__ == "__main__":
    unittest.main()
