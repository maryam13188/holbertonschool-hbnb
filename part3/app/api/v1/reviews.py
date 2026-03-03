#!/usr/bin/python3
"""Review endpoints - Tasks 3 and 4 (Amaal)"""

from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from app.services.facade import facade

api = Namespace("reviews", description="Review operations")

review_model = api.model("Review", {
    "text":     fields.String(required=True,  description="Review text"),
    "rating":   fields.Integer(required=True, description="Rating 1-5"),
    "place_id": fields.String(required=True,  description="Place ID"),
})

review_update_model = api.model("ReviewUpdate", {
    "text":   fields.String(description="Review text"),
    "rating": fields.Integer(description="Rating 1-5"),
})

def review_to_dict(review):
    return {
        "id":       review.id,
        "text":     review.text,
        "rating":   review.rating,
        "user_id":  getattr(review, "user_id",  None),
        "place_id": getattr(review, "place_id", None),
    }


@api.route("/")
class ReviewList(Resource):

    @api.response(200, "List of reviews retrieved successfully")
    def get(self):
        """Retrieve all reviews - PUBLIC"""
        return [review_to_dict(r) for r in facade.get_all_reviews()], 200

    @api.expect(review_model, validate=True)
    @api.response(201, "Review created successfully")
    @api.response(403, "Cannot review your own place or duplicate review")
    @api.response(404, "Place not found")
    @jwt_required()
    def post(self):
        """Create a review - AUTHENTICATED (Task 3)"""
        current_user_id = get_jwt_identity()
        review_data = api.payload
        place_id = review_data.get("place_id")

        place = facade.get_place(place_id)
        if not place:
            return {"error": "Place not found"}, 404

        owner_id = getattr(place, "owner_id", None)
        if owner_id and owner_id == current_user_id:
            return {"error": "Cannot review your own place"}, 403

        if facade.get_review_by_user_and_place(current_user_id, place_id):
            return {"error": "You have already reviewed this place"}, 403

        review_data["user_id"] = current_user_id
        try:
            new_review = facade.create_review(review_data)
        except ValueError as e:
            return {"error": str(e)}, 400
        return review_to_dict(new_review), 201


@api.route("/<string:review_id>")
class ReviewResource(Resource):

    @api.response(200, "Review details retrieved successfully")
    @api.response(404, "Review not found")
    def get(self, review_id):
        """Get review by ID - PUBLIC"""
        review = facade.get_review(review_id)
        if not review:
            return {"error": "Review not found"}, 404
        return review_to_dict(review), 200

    @api.expect(review_update_model, validate=False)
    @api.response(200, "Review updated successfully")
    @api.response(403, "Unauthorized action")
    @api.response(404, "Review not found")
    @jwt_required()
    def put(self, review_id):
        """Update review - AUTHENTICATED + OWNER CHECK (Task 3 and 4)"""
        current_user_id = get_jwt_identity()
        is_admin = get_jwt().get("is_admin", False)

        review = facade.get_review(review_id)
        if not review:
            return {"error": "Review not found"}, 404

        user_id = getattr(review, "user_id", None)
        if not is_admin and user_id and user_id != current_user_id:
            return {"error": "Unauthorized action"}, 403

        try:
            updated = facade.update_review(review_id, api.payload)
        except ValueError as e:
            return {"error": str(e)}, 400
        return review_to_dict(updated), 200

    @api.response(200, "Review deleted successfully")
    @api.response(403, "Unauthorized action")
    @api.response(404, "Review not found")
    @jwt_required()
    def delete(self, review_id):
        """Delete review - AUTHENTICATED + OWNER CHECK (Task 3 and 4)"""
        current_user_id = get_jwt_identity()
        is_admin = get_jwt().get("is_admin", False)

        review = facade.get_review(review_id)
        if not review:
            return {"error": "Review not found"}, 404

        user_id = getattr(review, "user_id", None)
        if not is_admin and user_id and user_id != current_user_id:
            return {"error": "Unauthorized action"}, 403

        facade.delete_review(review_id)
        return {"message": "Review deleted successfully"}, 200


@api.route("/places/<string:place_id>/reviews")
class PlaceReviewList(Resource):

    @api.response(200, "Reviews for place retrieved successfully")
    @api.response(404, "Place not found")
    def get(self, place_id):
        """Get all reviews for a place - PUBLIC"""
        if not facade.get_place(place_id):
            return {"error": "Place not found"}, 404
        return [review_to_dict(r) for r in facade.get_reviews_by_place(place_id)], 200
