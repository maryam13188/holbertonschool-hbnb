import unittest
from flask_jwt_extended import create_access_token
from app import create_app, db
from app.models.user import User
from app.models.place import Place
from app.models.review import Review


class TestReviewEndpoints(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = create_app("config.TestingConfig")
        cls.client = cls.app.test_client()

        with cls.app.app_context():
            db.drop_all()
            db.create_all()

            owner = User(
                first_name="Owner",
                last_name="User",
                email="reviewowner@example.com",
                is_admin=False
            )
            owner.hash_password("ownerpass")

            reviewer = User(
                first_name="Reviewer",
                last_name="User",
                email="reviewer@example.com",
                is_admin=False
            )
            reviewer.hash_password("reviewerpass")

            other_user = User(
                first_name="Other",
                last_name="User",
                email="otherreview@example.com",
                is_admin=False
            )
            other_user.hash_password("otherpass")

            admin = User(
                first_name="Admin",
                last_name="User",
                email="adminreview@example.com",
                is_admin=True
            )
            admin.hash_password("adminpass")

            db.session.add_all([owner, reviewer, other_user, admin])
            db.session.commit()

            place = Place(
                title="Review Place",
                description="Place for review tests",
                price=120.0,
                latitude=24.5,
                longitude=46.5,
                owner_id=str(owner.id)
            )
            db.session.add(place)
            db.session.commit()

            review = Review(
                text="Amazing experience!",
                rating=5,
                user_id=str(reviewer.id),
                place_id=str(place.id)
            )
            db.session.add(review)
            db.session.commit()

            cls.place_id = str(place.id)
            cls.review_id = str(review.id)
            cls.owner_id = str(owner.id)
            cls.reviewer_id = str(reviewer.id)
            cls.other_user_id = str(other_user.id)
            cls.admin_id = str(admin.id)

            cls.owner_token = create_access_token(
                identity=cls.owner_id,
                additional_claims={"is_admin": False}
            )
            cls.reviewer_token = create_access_token(
                identity=cls.reviewer_id,
                additional_claims={"is_admin": False}
            )
            cls.other_user_token = create_access_token(
                identity=cls.other_user_id,
                additional_claims={"is_admin": False}
            )
            cls.admin_token = create_access_token(
                identity=cls.admin_id,
                additional_claims={"is_admin": True}
            )

    @classmethod
    def tearDownClass(cls):
        with cls.app.app_context():
            db.session.remove()
            db.drop_all()

    def test_get_reviews_returns_200(self):
        response = self.client.get("/api/v1/reviews/")
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.get_json(), list)

    def test_get_nonexistent_review_returns_404(self):
        response = self.client.get("/api/v1/reviews/nonexistent-id")
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.get_json(), {"error": "Review not found"})

    def test_get_reviews_for_place_returns_200(self):
        response = self.client.get(f"/api/v1/reviews/places/{self.place_id}/reviews")
        self.assertEqual(response.status_code, 200)

    def test_create_review_without_token_returns_401(self):
        response = self.client.post(
            "/api/v1/reviews/",
            json={
                "text": "Great place!",
                "rating": 5,
                "place_id": self.place_id
            },
            content_type="application/json"
        )
        self.assertEqual(response.status_code, 401)

    def test_owner_cannot_review_own_place(self):
        response = self.client.post(
            "/api/v1/reviews/",
            json={
                "text": "My own place",
                "rating": 5,
                "place_id": self.place_id
            },
            headers={"Authorization": f"Bearer {self.owner_token}"},
            content_type="application/json"
        )
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.get_json(), {"error": "Cannot review your own place"})

    def test_duplicate_review_returns_403(self):
        response = self.client.post(
            "/api/v1/reviews/",
            json={
                "text": "Duplicate review",
                "rating": 4,
                "place_id": self.place_id
            },
            headers={"Authorization": f"Bearer {self.reviewer_token}"},
            content_type="application/json"
        )
        self.assertEqual(response.status_code, 403)

    def test_update_review_by_non_owner_returns_403(self):
        response = self.client.put(
            f"/api/v1/reviews/{self.review_id}",
            json={"text": "Hacked review", "rating": 1},
            headers={"Authorization": f"Bearer {self.other_user_token}"},
            content_type="application/json"
        )
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.get_json(), {"error": "Unauthorized action"})

    def test_update_review_by_owner_returns_200(self):
        response = self.client.put(
            f"/api/v1/reviews/{self.review_id}",
            json={"text": "Updated review", "rating": 4},
            headers={"Authorization": f"Bearer {self.reviewer_token}"},
            content_type="application/json"
        )
        self.assertEqual(response.status_code, 200)

    def test_delete_review_by_non_owner_returns_403(self):
        response = self.client.delete(
            f"/api/v1/reviews/{self.review_id}",
            headers={"Authorization": f"Bearer {self.other_user_token}"}
        )
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.get_json(), {"error": "Unauthorized action"})


class TestReviewModel(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = create_app("config.TestingConfig")

    def test_review_creation(self):
        with self.app.app_context():
            review = Review(
                text="Amazing experience!",
                rating=5,
                user_id="test-user-id",
                place_id="test-place-id"
            )
            self.assertEqual(review.text, "Amazing experience!")
            self.assertEqual(review.rating, 5)
            self.assertIsNotNone(review)


if __name__ == "__main__":
    unittest.main()
