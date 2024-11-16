#!/usr/bin/python3
"""
Unittest for BaseModel class
"""

import unittest
from datetime import datetime, timedelta  # Import timedelta here

from models.base_model import BaseModel


class TestBaseModel(unittest.TestCase):
    """Test suite for BaseModel class."""

    def setUp(self):
        """Set up a new instance for testing."""
        self.model = BaseModel()

    def test_id_is_unique(self):
        """Test that each BaseModel instance has a unique id."""
        model2 = BaseModel()
        self.assertNotEqual(self.model.id, model2.id)
        self.assertTrue(isinstance(self.model.id, str))

    def test_created_at_initialization(self):
        """Test that created_at is initialized to the current datetime."""
        self.assertTrue(isinstance(self.model.created_at, datetime))
        self.assertAlmostEqual(
            self.model.created_at, datetime.now(), delta=timedelta(seconds=1)
        )  # Updated

    def test_updated_at_initialization(self):
        """Test that updated_at is initialized to the current datetime."""
        self.assertTrue(isinstance(self.model.updated_at, datetime))
        self.assertAlmostEqual(
            self.model.updated_at, datetime.now(), delta=timedelta(seconds=1)
        )  # Updated

    def test_str_method(self):
        """Test the __str__ method returns the correct string format."""
        expected = f"[BaseModel] ({self.model.id}) {self.model.__dict__}"
        self.assertEqual(str(self.model), expected)

    def test_save_method(self):
        """Test that save method updates updated_at to the current datetime."""
        old_updated_at = self.model.updated_at
        self.model.save()
        self.assertNotEqual(self.model.updated_at, old_updated_at)
        self.assertTrue(self.model.updated_at > old_updated_at)

    def test_to_dict_method(self):
        """
        Test that to_dict method returns a
        correct dictionary representation.
        """
        model_dict = self.model.to_dict()
        self.assertTrue(isinstance(model_dict, dict))
        self.assertEqual(model_dict["__class__"], "BaseModel")
        self.assertEqual(model_dict["id"], self.model.id)
        self.assertEqual(
                model_dict["created_at"],
                self.model.created_at.isoformat()
                )
        self.assertEqual(
                model_dict["updated_at"],
                self.model.updated_at.isoformat()
                )

    def test_to_dict_contains_added_attributes(self):
        """Test that to_dict includes attributes added after instantiation."""
        self.model.name = "My First Model"
        self.model.my_number = 89
        model_dict = self.model.to_dict()
        self.assertIn("name", model_dict)
        self.assertIn("my_number", model_dict)
        self.assertEqual(model_dict["name"], "My First Model")
        self.assertEqual(model_dict["my_number"], 89)


if __name__ == "__main__":
    unittest.main()
