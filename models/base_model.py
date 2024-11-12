#!/usr/bin/python3
"""
This module defines the BaseModel class that serves as the base class for other models.
"""

import uuid
from datetime import datetime


class BaseModel:
    """Defines common attributes/methods for other classes."""

    def __init__(self):
        """Initializes a new instance with unique id, created_at, and updated_at."""
        self.id = str(uuid.uuid4())
        self.created_at = datetime.now()
        self.updated_at = self.created_at

    def __str__(self):
        """Returns a string representation of the instance."""
        return f"[{self.__class__.__name__}] ({self.id}) {self.__dict__}"

    def save(self):
        """Updates the updated_at attribute with the current datetime."""
        self.updated_at = datetime.now()

    def to_dict(self):
        """Returns a dictionary containing all keys/values of the instance."""
        dict_repr = self.__dict__.copy()
        dict_repr["__class__"] = self.__class__.__name__
        dict_repr["created_at"] = self.created_at.isoformat()
        dict_repr["updated_at"] = self.updated_at.isoformat()
        return dict_repr
