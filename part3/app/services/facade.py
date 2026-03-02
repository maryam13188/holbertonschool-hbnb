#!/usr/bin/python3
"""HBnB Facade (Tasks 1 & 5)."""

from app.persistence.in_memory_repository import InMemoryRepository
from app.persistence.sqlalchemy_repository import SQLAlchemyRepository


class HBnBFacade:
    """
    Task 5: SQLAlchemyRepository support
    Task 1: Password hashing validation and email uniqueness checks
    """

    def __init__(self, user_model=None, user_repo=None):
        if user_repo is not None:
            self.user_repo = user_repo
        elif user_model is not None:
            self.user_repo = SQLAlchemyRepository(user_model)
        else:
            self.user_repo = InMemoryRepository()

    # ==================== USERS (Tasks 1 & 5) ====================

    def create_user(self, user_obj):
        """Create user with password validation (Task 1)"""
        if not hasattr(user_obj, 'password') or not user_obj.password:
            raise ValueError("Password is required")
        
        if self.get_user_by_email(user_obj.email):
            raise ValueError("Email already registered")
        
        return self.user_repo.add(user_obj)

    def get_user(self, user_id):
        return self.user_repo.get(user_id)

    def get_users(self):
        return self.user_repo.get_all()

    def get_user_by_email(self, email):
        return self.user_repo.get_by_attribute("email", email)

    def update_user(self, user_id, data):
        """Update user with email uniqueness check (Task 1)"""
        user = self.get_user(user_id)
        if not user:
            return None
        
        if "email" in data:
            existing = self.get_user_by_email(data["email"])
            if existing and existing.id != user_id:
                raise ValueError("Email already registered")
        
        for key, value in data.items():
            if hasattr(user, key) and key not in ('id', 'password'):
                setattr(user, key, value)
        
        user.save()
        self.user_repo.update(user_id, user)
        return user

    def delete_user(self, user_id):
        return self.user_repo.delete(user_id)
