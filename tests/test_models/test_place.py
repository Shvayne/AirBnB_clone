#!/usr/bin/python3
"""Unittest module for the Place Class."""

import unittest
from models.place import Place
from models.engine.file_storage import FileStorage
import os
from models import storage
from models.base_model import BaseModel
from datetime import datetime

class TestPlace(unittest.TestCase):
    """Test Cases for the place Class"""

    def setUp(self):
        """Sets up test methods."""
        self.resetStorage()
        self.place = Place()

    def tearDown(self):
        """Tears down test methods."""
        self.resetStorage()
        del self.place

    def resetStorage(self):
        """Resets FileStorage data."""
        FileStorage._FileStorage__objects = {}
        if os.path.isfile(FileStorage._FileStorage__file_path):
           os.remove(FileStorage._FileStorage__file_path)

    def test_instantiation(self):
        """Tests instantiation of Place class."""
        p = Place()
        self.assertEqual(str(type(p)), "<class 'models.place.Place'>")
        self.assertIsInstance(p, Place)
        self.assertTrue(issubclass(type(p), BaseModel))

    def test_attribute(self):
        """tests for the attributes of place class"""
        attributes = {
            "city_id": str,
            "user_id": str,
            "name": str,
            "description": str,
            "number_bathrooms": int,
            "number_rooms": int,
            "max_guest": int,
            "price_by_night": int,
            "latitude": float,
            "longitude": float,
            "amenity_ids": list
        }
        for attr_name, attr_type in attributes.items():
            self.assertTrue(hasattr(self.place, attr_name))
            self.assertEqual(type(getattr(self.place, attr_name, None)), attr_type)

    def test_city_id_attribute(self):
        """Test the type of city_id attribute."""
        self.assertTrue(hasattr(self.place, "city_id"))
        self.assertEqual(type(self.place.city_id), str)

    def test_user_id_attribute(self):
        """Test the type of user_id attribute."""
        self.assertTrue(hasattr(self.place, "user_id"))
        self.assertEqual(type(self.place.user_id), str)
        self.assertEqual(self.place.user_id, "")

    def test_name_attribute(self):
        """Test the type of name attribute."""
        self.assertTrue(hasattr(self.place, "name"))
        self.assertEqual(type(self.place.name), str)
        self.assertEqual(self.place.name, "")

    def test_description_attribute(self):
        """Test the type of description attribute."""
        self.assertTrue(hasattr(self.place, "description"))
        self.assertEqual(type(self.place.description), str)
        self.assertEqual(self.place.description, "")

    def test_number_bathrooms_attribute(self):
        """Test the type of number_bathrooms attribute."""
        self.assertTrue(hasattr(self.place, "number_bathrooms"))
        self.assertEqual(type(self.place.number_bathrooms), int)
        self.assertEqual(self.place.number_bathrooms, 0)

    def test_number_rooms_attribute(self):
        """Test the type of number_rooms attribute."""
        self.assertTrue(hasattr(self.place, "number_rooms"))
        self.assertEqual(type(self.place.number_rooms), int)
        self.assertEqual(self.place.number_rooms, 0)

    def test_max_guest_attribute(self):
        """Test the type of max_guest attribute."""
        self.assertTrue(hasattr(self.place, "max_guest"))
        self.assertEqual(type(self.place.max_guest), int)
        self.assertEqual(self.place.max_guest, 0)

    def test_price_by_night_attribute(self):
        """Test the type of price_by_night attribute."""
        self.assertTrue(hasattr(self.place, "price_by_night"))
        self.assertEqual(type(self.place.price_by_night), int)
        self.assertEqual(self.place.price_by_night, 0)

    def test_latitude_attribute(self):
        """Test the type of latitude attribute."""
        self.assertTrue(hasattr(self.place, "latitude"))
        self.assertEqual(type(self.place.latitude), float)
        self.assertEqual(self.place.latitude, 0.0)

    def test_longitude_attribute(self):
        """Test the type of longitude attribute."""
        self.assertTrue(hasattr(self.place, "longitude"))
        self.assertEqual(type(self.place.longitude), float)
        self.assertEqual(self.place.longitude, 0.0)

    def test_amenity_ids_attribute(self):
        """Test the type of amenity_ids attribute."""
        self.assertTrue(hasattr(self.place, "amenity_ids"))
        self.assertEqual(type(self.place.amenity_ids), list)
        self.assertEqual(self.place.amenity_ids, [])

    def test_str_method(self):
        """Test the __str__ method of Place."""
        expected_str = f"[Place] ({self.place.id}) {self.place.__dict__}"
        self.assertEqual(str(self.place), expected_str)

    def test_kwargs_initialization(self):
        """Test initialization with kwargs."""
        kwargs = {
            "id": "123",
            "created_at": "2023-01-01T00:00:00",
            "updated_at": "2023-01-02T00:00:00",
            "city_id": "city_123",
            "user_id": "user_123",
            "name": "My place",
            "description": "A lovely place",
            "number_bathrooms": 2,
            "number_rooms": 3,
            "max_guest": 4,
            "price_by_night": 100,
            "latitude": 12.34,
            "longitude": 56.78,
            "amenity_ids": ["amenity_1", "amenity_2"]
        }
        place = Place(**kwargs)
        self.assertEqual(place.id, "123")
        self.assertEqual(place.created_at, datetime.fromisoformat("2023-01-01T00:00:00"))
        self.assertEqual(place.updated_at, datetime.fromisoformat("2023-01-02T00:00:00"))
        self.assertEqual(place.city_id, "city_123")
        self.assertEqual(place.user_id, "user_123")
        self.assertEqual(place.name, "My place")
        self.assertEqual(place.description, "A lovely place")
        self.assertEqual(place.number_bathrooms, 2)
        self.assertEqual(place.number_rooms, 3)
        self.assertEqual(place.max_guest, 4)
        self.assertEqual(place.price_by_night, 100)
        self.assertEqual(place.latitude, 12.34)
        self.assertEqual(place.longitude, 56.78)
        self.assertEqual(place.amenity_ids, ["amenity_1", "amenity_2"])

    def test_empty_kwargs_initialization(self):
        """Test initialization with empty kwargs."""
        kwargs = {}
        place = Place(**kwargs)
        self.assertIsNotNone(place.id)
        self.assertIsNotNone(place.created_at)
        self.assertIsNotNone(place.updated_at)

    def test_storage_new_called(self):
        """Test if storage.new is called during initialization."""
        place = Place()
        key = f"Place.{place.id}"
        self.assertIn(key, storage.all())

    def test_storage_save(self):
        """Test if storage.save is called when save method is used."""
        place = Place()
        place.save()
        storage.save()
        self.assertTrue(os.path.exists(FileStorage._FileStorage__file_path))

    def test_reload(self):
        """Test if reload method works correctly."""
        place = Place()
        place.save()
        storage.save()
        storage.reload()
        key = f"Place.{place.id}"
        self.assertIn(key, storage.all())

if __name__ == "__main__":
    unittest.main()