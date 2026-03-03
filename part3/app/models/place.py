#!/usr/bin/python3
"""Place model with SQLAlchemy - Task 7"""

from __future__ import annotations

import re
from typing import Any

from app.extensions import db
from .base_model import BaseModel


class Place(BaseModel):
    """
    Place entity with SQLAlchemy mapping.
    
    Attributes:
        title (str): Title of the place (required, max 100)
        description (str): Description of the place (optional, max 1000)
        price (float): Price per night (required, positive, max 1,000,000)
        latitude (float): Latitude coordinate (required, between -90 and 90)
        longitude (float): Longitude coordinate (required, between -180 and 180)
    """
    
    __tablename__ = 'places'

    # ==================== TASK 7: SQLAlchemy Columns ====================
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    price = db.Column(db.Float, nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)

    # Relationships (to be implemented in Task 8)
    # owner_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)
    # owner = db.relationship('User', backref='places', lazy=True)
    # reviews = db.relationship('Review', backref='place', lazy=True, cascade='all, delete-orphan')
    # amenities = db.relationship('Amenity', secondary='place_amenity', backref='places', lazy=True)

    def __init__(self, **kwargs):
        """
        Initialize a new Place with validation.
        
        Raises:
            ValueError: If validation fails for any field
        """
        super().__init__(**kwargs)

        # ============= Validation =============
        # Title validation
        if not self.title or not self.title.strip():
            raise ValueError("Title is required")
        if len(self.title) > 100:
            raise ValueError("Title must be under 100 characters")
        self.title = self.title.strip()

        # Description validation (optional)
        if self.description and len(self.description) > 1000:
            raise ValueError("Description must be under 1000 characters")
        if self.description:
            self.description = self.description.strip()

        # Price validation
        if self.price is None:
            raise ValueError("Price is required")
        if self.price <= 0:
            raise ValueError("Price must be greater than 0")
        if self.price > 1000000:
            raise ValueError("Price must be under 1,000,000")

        # Latitude validation
        if self.latitude is None:
            raise ValueError("Latitude is required")
        if not (-90 <= self.latitude <= 90):
            raise ValueError("Latitude must be between -90 and 90")

        # Longitude validation
        if self.longitude is None:
            raise ValueError("Longitude is required")
        if not (-180 <= self.longitude <= 180):
            raise ValueError("Longitude must be between -180 and 180")

    # ============= Business Methods =============

    def get_average_rating(self) -> float:
        """
        Calculate average rating from reviews.
        Note: This will be implemented in Task 8 when relationships are added.
        """
        return 0.0

    # ============= Serialization =============

    def to_dict(self) -> dict:
        """Convert place to dictionary."""
        base_dict = super().to_dict()
        base_dict.update({
            "title": self.title,
            "description": self.description,
            "price": self.price,
            "latitude": self.latitude,
            "longitude": self.longitude,
        })
        return base_dict

    # ============= Magic Methods =============

    def __str__(self) -> str:
        return f"[Place] {self.title}"

    def __repr__(self) -> str:
        return f"<Place id={self.id} title={self.title}>"
