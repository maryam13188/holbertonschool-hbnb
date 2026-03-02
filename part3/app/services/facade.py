#!/usr/bin/python3
"""HBnB Facade (Tasks 1, 5 & 6)."""

from app.persistence.sqlalchemy_repository import UserRepository
from app.models.user import User


class HBnBFacade:
    """
    Facade for Business Logic Layer - Part 3
    Task 5: SQLAlchemyRepository support
    Task 1: Password hashing validation
    Task 6: UserRepository integration
    """

    def __init__(self):
        # ==================== TASK 6: Use UserRepository ====================
        self.user_repo = UserRepository()
        
        # Other repositories (Tasks 6,7)
        self.amenity_repo = None
        self.place_repo = None
        self.review_repo = None

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

    # ==================== PLACEHOLDERS FOR TASKS 6 & 7 ====================

    def create_amenity(self, amenity_data):
        """Placeholder - Task 6/7"""
        pass

    def get_amenity(self, amenity_id):
        """Placeholder - Task 6/7"""
        pass

    def get_all_amenities(self):
        """Placeholder - Task 6/7"""
        return []

    def create_place(self, place_data):
        """Placeholder - Task 7"""
        pass

    def get_place(self, place_id):
        """Placeholder - Task 7"""
        pass

    def get_all_places(self):
        """Placeholder - Task 7"""
        return []

    def create_review(self, review_data):
        """Placeholder - Task 7"""
        pass

    def get_review(self, review_id):
        """Placeholder - Task 7"""
        pass

    def get_reviews_by_place(self, place_id):
        """Placeholder - Task 7"""
        return []

    def get_reviews_by_user(self, user_id):
        """Placeholder - Task 7"""
        return []
