#!/usr/bin/python3
"""HBnB Facade (Tasks 1, 5, 6 & 7)."""

from app.persistence.sqlalchemy_repository import (
    UserRepository, PlaceRepository, ReviewRepository, AmenityRepository
)
from app.models.user import User
from app.models.place import Place
from app.models.review import Review
from app.models.amenity import Amenity


class HBnBFacade:
    """
    Facade for Business Logic Layer - Part 3
    Task 5: SQLAlchemyRepository support
    Task 1: Password hashing validation
    Task 6: UserRepository integration
    Task 7: Place, Review, Amenity repositories integration
    """

    def __init__(self):
        # ==================== TASK 6: UserRepository ====================
        self.user_repo = UserRepository()
        
        # ==================== TASK 7: Place, Review, Amenity ====================
        self.place_repo = PlaceRepository()
        self.review_repo = ReviewRepository()
        self.amenity_repo = AmenityRepository()

    # ==================== USERS (Tasks 1, 5 & 6) ====================

    def create_user(self, user_data):
        """
        Create a new user with password hashing.
        
        Args:
            user_data (dict): User data with password
            
        Returns:
            User: Created user object
            
        Raises:
            ValueError: If password missing or email already exists
        """
        # Check if email already exists (Task 1 & 6)
        if self.get_user_by_email(user_data["email"]):
            raise ValueError("Email already registered")
        
        # Create user (password hashing happens in User.__init__)
        user = User(**user_data)
        
        # Save to database (Task 6)
        return self.user_repo.add(user)

    def get_user(self, user_id):
        """Get user by ID (Task 6)."""
        return self.user_repo.get(user_id)

    def get_users(self):
        """Get all users (Task 6)."""
        return self.user_repo.get_all()

    def get_user_by_email(self, email):
        """Get user by email using UserRepository (Task 6)."""
        return self.user_repo.get_user_by_email(email)

    def update_user(self, user_id, data):
        """
        Update user information.
        
        Args:
            user_id: ID of user to update
            data: Dictionary of fields to update
            
        Returns:
            User: Updated user object or None if not found
            
        Raises:
            ValueError: If email is already taken
        """
        # Get user first
        user = self.get_user(user_id)
        if not user:
            return None
        
        # Check email uniqueness if being updated (Task 1)
        if "email" in data and data["email"] != user.email:
            existing = self.get_user_by_email(data["email"])
            if existing:
                raise ValueError("Email already registered")
        
        # Update user (Task 6)
        return self.user_repo.update(user_id, data)

    def delete_user(self, user_id):
        """Delete user by ID (Task 6)."""
        return self.user_repo.delete(user_id)

    # ==================== PLACES (Task 7) ====================

    def create_place(self, place_data):
        """
        Create a new place.
        
        Args:
            place_data (dict): Place data
            
        Returns:
            Place: Created place object
            
        Raises:
            ValueError: If validation fails
        """
        place = Place(**place_data)
        return self.place_repo.add(place)

    def get_place(self, place_id):
        """Get place by ID (Task 7)."""
        return self.place_repo.get(place_id)

    def get_all_places(self):
        """Get all places (Task 7)."""
        return self.place_repo.get_all()

    def update_place(self, place_id, data):
        """Update place information (Task 7)."""
        return self.place_repo.update(place_id, data)

    def delete_place(self, place_id):
        """Delete place by ID (Task 7)."""
        return self.place_repo.delete(place_id)

    # ==================== REVIEWS (Task 7) ====================

    def create_review(self, review_data):
        """
        Create a new review.
        
        Args:
            review_data (dict): Review data
            
        Returns:
            Review: Created review object
            
        Raises:
            ValueError: If validation fails
        """
        review = Review(**review_data)
        return self.review_repo.add(review)

    def get_review(self, review_id):
        """Get review by ID (Task 7)."""
        return self.review_repo.get(review_id)

    def get_all_reviews(self):
        """Get all reviews (Task 7)."""
        return self.review_repo.get_all()

    def get_reviews_by_place(self, place_id):
        """
        Get all reviews for a specific place.
        Note: This will be implemented in Task 8 with relationships.
        """
        return []

    def get_reviews_by_user(self, user_id):
        """
        Get all reviews by a specific user.
        Note: This will be implemented in Task 8 with relationships.
        """
        return []

    def update_review(self, review_id, data):
        """Update review information (Task 7)."""
        return self.review_repo.update(review_id, data)

    def delete_review(self, review_id):
        """Delete review by ID (Task 7)."""
        return self.review_repo.delete(review_id)

    # ==================== AMENITIES (Task 7) ====================

    def create_amenity(self, amenity_data):
        """
        Create a new amenity.
        
        Args:
            amenity_data (dict): Amenity data
            
        Returns:
            Amenity: Created amenity object
            
        Raises:
            ValueError: If validation fails
        """
        amenity = Amenity(**amenity_data)
        return self.amenity_repo.add(amenity)

    def get_amenity(self, amenity_id):
        """Get amenity by ID (Task 7)."""
        return self.amenity_repo.get(amenity_id)

    def get_all_amenities(self):
        """Get all amenities (Task 7)."""
        return self.amenity_repo.get_all()


    def update_amenity(self, amenity_id, data):
        """Update amenity information (Task 7)."""
        return self.amenity_repo.update(amenity_id, data)
    def delete_amenity(self, amenity_id):
        """Delete amenity by ID (Task 7)."""
        return self.amenity_repo.delete(amenity_id)
