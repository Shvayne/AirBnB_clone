#!/usr/bin/python3
"""Unittest module for the Review class."""

import unittest
from models.review import Review
from models.engine.file_storage import FileStorage
import os
from models import storage
from models.base_model import BaseModel
from datetime import datetime

class TestReview(unittest.TestCase):
    """test case for the review class"""
    def setUp(self):
        """Sets up test methods."""
        self.resetStorage()
        self.review = Review()

    def tearDown(self):
        """Tears down test methods."""
        self.resetStorage()
        del self.review

    def resetStorage(self):
        """Resets FileStorage data."""
        FileStorage._FileStorage__objects = {}
        if os.path.isfile(FileStorage._FileStorage__file_path):
            os.remove(FileStorage._FileStorage__file_path)

    def test_instantiation(self):
        """Tests instantiation of Review class."""
        r = Review()
        self.assertEqual(str(type(r)), "<class 'models.review.Review'>")
        self.assertIsInstance(r, Review)
        self.assertTrue(issubclass(type(r), BaseModel))

    def test_place_id_attribute(self):
        """Test the type of place_id attribute."""
        self.assertTrue(hasattr(self.review, "place_id"))
        self.assertEqual(type(self.review.place_id), str)
        self.assertEqual(self.review.place_id, "")

    def test_user_id_attribute(self):
        """Test the type of user_id attribute."""
        self.assertTrue(hasattr(self.review, "user_id"))
        self.assertEqual(type(self.review.user_id), str)
        self.assertEqual(self.review.user_id, "")

    def test_text_attribute(self):
        """Test the type of text attribute."""
        self.assertTrue(hasattr(self.review, "text"))
        self.assertEqual(type(self.review.text), str)
        self.assertEqual(self.review.text, "")

    def test_str_method(self):
        """Test the __str__ method of Review."""
        expected_str = f"[Review] ({self.review.id}) {self.review.__dict__}"
        self.assertEqual(str(self.review), expected_str)


    def test_kwargs_initialization(self):
        """Test initialization with kwargs."""
        kwargs = {
            "id": "123",
            "created_at": "2023-01-01T00:00:00",
            "updated_at": "2023-01-02T00:00:00",
            "place_id": "place_123",
            "user_id": "user_123",
            "text": "Nice place!"
        }
        review = Review(**kwargs)
        self.assertEqual(review.id, "123")
        self.assertEqual(review.created_at, datetime.fromisoformat("2023-01-01T00:00:00"))
        self.assertEqual(review.updated_at, datetime.fromisoformat("2023-01-02T00:00:00"))
        self.assertEqual(review.place_id, "place_123")
        self.assertEqual(review.user_id, "user_123")
        self.assertEqual(review.text, "Nice place!")

    def test_empty_kwargs_initialization(self):
        """Test initialization with empty kwargs."""
        kwargs = {}
        review = Review(**kwargs)
        self.assertIsNotNone(review.id)
        self.assertIsNotNone(review.created_at)
        self.assertIsNotNone(review.updated_at)

    def test_storage_new_called(self):
        """Test if storage.new is called during initialization."""
        review = Review()
        key = f"Review.{review.id}"
        self.assertIn(key, storage.all())

    def test_storage_save(self):
        """Test if storage.save is called when save method is used."""
        review = Review()
        review.save()
        storage.save()
        self.assertTrue(os.path.exists(FileStorage._FileStorage__file_path))

    def test_reload(self):
        """Test if reload method works correctly."""
        review = Review()
        review.save()
        storage.save()
        storage.reload()
        key = f"Review.{review.id}"
        self.assertIn(key, storage.all())


if __name__ == "__main__":
    unittest.main()