#!/usr/bin/python3
"""User module with password hashing - Task 1"""

from __future__ import annotations

import re
from typing import Any, List, Optional, TYPE_CHECKING

from app.extensions import bcrypt 
from .base import BaseModel

if TYPE_CHECKING:
    from .place import Place
    from .review import Review


_EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


class User(BaseModel):
    """
    User entity representing system users with password hashing.
    
    Attributes:
        first_name (str): User's first name (required, max 50)
        last_name (str): User's last name (required, max 50)
        email (str): User's email address (required, valid format)
        password (str): Hashed password (stored securely)
        is_admin (bool): Admin privileges flag (default False)
        places (List[Place]): Places owned by user
        reviews (List[Review]): Reviews written by user
    """

    def __init__(
        self,
        first_name: str,
        last_name: str,
        email: str,
        password: str = None,
        is_admin: bool = False,
        **kwargs: Any,
    ) -> None:
        """Initialize a new User."""
        super().__init__(**kwargs)
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.is_admin = is_admin
        self._places: List[Place] = []
        self._reviews: List[Review] = []
        
        if password:
            self.hash_password(password)

    # ============= Password Hashing Methods =============

    def hash_password(self, password: str) -> None:
        """Hashes the password before storing it."""
        self._password = bcrypt.generate_password_hash(password).decode('utf-8')

    def verify_password(self, password: str) -> bool:
        """Verifies if the provided password matches the hashed password."""
        return bcrypt.check_password_hash(self._password, password)

    # ============= Properties with Validation =============

    @property
    def first_name(self) -> str:
        return self._first_name

    @first_name.setter
    def first_name(self, value: str) -> None:
        if not isinstance(value, str) or not value.strip():
            raise ValueError("first_name is required")
        if len(value) > 50:
            raise ValueError("first_name must be at most 50 characters")
        self._first_name = value.strip()

    @property
    def last_name(self) -> str:
        return self._last_name

    @last_name.setter
    def last_name(self, value: str) -> None:
        if not isinstance(value, str) or not value.strip():
            raise ValueError("last_name is required")
        if len(value) > 50:
            raise ValueError("last_name must be at most 50 characters")
        self._last_name = value.strip()

    @property
    def email(self) -> str:
        return self._email

    @email.setter
    def email(self, value: str) -> None:
        if not isinstance(value, str) or not value.strip():
            raise ValueError("email is required")
        if not _EMAIL_RE.match(value.strip()):
            raise ValueError("email must be a valid email address")
        self._email = value.strip().lower()

    @property
    def is_admin(self) -> bool:
        return self._is_admin

    @is_admin.setter
    def is_admin(self, value: bool) -> None:
        if not isinstance(value, bool):
            raise ValueError("is_admin must be a boolean")
        self._is_admin = value

    # ============= Relationship Properties =============

    @property
    def places(self) -> List[Place]:
        return self._places.copy()

    @property
    def reviews(self) -> List[Review]:
        return self._reviews.copy()

    # ============= Relationship Methods =============

    def add_place(self, place: Place) -> None:
        if place not in self._places:
            self._places.append(place)
            self.save()

    def remove_place(self, place: Place) -> None:
        if place in self._places:
            self._places.remove(place)
            self.save()

    def add_review(self, review: Review) -> None:
        if review not in self._reviews:
            self._reviews.append(review)
            self.save()

    def remove_review(self, review: Review) -> None:
        if review in self._reviews:
            self._reviews.remove(review)
            self.save()

    # ============= Business Methods =============

    def register(self) -> None:
        self.save()

    def update_profile(self, data: dict) -> None:
        self.update(data)

    def delete(self) -> None:
        pass

    def is_admin_user(self) -> bool:
        return self.is_admin

    def get_full_name(self) -> str:
        return f"{self.first_name} {self.last_name}"

    # ============= Validation =============

    def validate(self) -> bool:
        try:
            _ = self.first_name
            _ = self.last_name
            _ = self.email
            _ = self.is_admin
            return True
        except (ValueError, AttributeError):
            return False

    # ============= Serialization =============

    def to_dict(self) -> dict:
        base_dict = super().to_dict()
        base_dict.update({
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email,
            "is_admin": self.is_admin,
        })
        return base_dict

    # ============= Magic Methods =============

    def __str__(self) -> str:
        return f"[User] {self.email}"

    def __repr__(self) -> str:
        return f"<User id={self._id} email={self.email}>"
