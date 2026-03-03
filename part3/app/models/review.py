#!/usr/bin/python3
"""Review model with SQLAlchemy - Task 7"""

from __future__ import annotations

from typing import Any

from app.extensions import db
from .base_model import BaseModel


class Review(BaseModel):
    """
    Review entity with SQLAlchemy mapping.
    
    Attributes:
        text (str): Content of the review (required)
        rating (int): Rating from 1 to 5 (required)
    """
    
    __tablename__ = 'reviews'

    # ==================== TASK 7: SQLAlchemy Columns ====================
    text = db.Column(db.Text, nullable=False)
    rating = db.Column(db.Integer, nullable=False)

    # Relationships (to be implemented in Task 8)
    # user_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)
    # place_id = db.Column(db.String(36), db.ForeignKey('places.id'), nullable=False)
    # user = db.relationship('User', backref='reviews', lazy=True)
    # place = db.relationship('Place', backref='reviews', lazy=True, cascade='all, delete-orphan')

    def __init__(self, **kwargs):
        """
        Initialize a new Review with validation.
        
        Raises:
            ValueError: If validation fails for any field
        """
        super().__init__(**kwargs)

        # ============= Validation =============
        # Text validation
        if not self.text or not self.text.strip():
            raise ValueError("text is required")
        if len(self.text) > 500:
            raise ValueError("text must be under 500 characters")
        self.text = self.text.strip()

        # Rating validation
        if self.rating is None:
            raise ValueError("rating is required")
        try:
            rating_int = int(self.rating)
            if rating_int < 1 or rating_int > 5:
                raise ValueError("rating must be between 1 and 5")
            self.rating = rating_int
        except (TypeError, ValueError):
            raise ValueError("rating must be an integer between 1 and 5")

    # ============= Serialization =============

    def to_dict(self) -> dict:
        """Convert review to dictionary."""
        base_dict = super().to_dict()
        base_dict.update({
            "rating": self.rating,
            "text": self.text,
        })
        return base_dict

    # ============= Magic Methods =============

    def __str__(self) -> str:
        return f"[Review] {self.rating}/5"

    def __repr__(self) -> str:
        return f"<Review id={self.id} rating={self.rating}>"
