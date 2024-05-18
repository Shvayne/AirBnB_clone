#!usr/bin/python3
"""unittests for the City class"""

import unittest
import os
from models.city import City
from models.engine.file_storage import FileStorage
from models.base_model import BaseModel
from datetime import datetime
from models import storage

class TestCity(unittest.TestCase):
    """Test Cases for the city class"""

    def setUp(self):
        """sets up test methods"""
        self.resetStorage()
        self.city = City()

    def tearDown(self):
        """tears down the test methods"""
        self.resetStorage()
        del self.city

    def resetStorage(self):
        """resets Filestorage data"""
        FileStorage._FileStorage__objects = {}
        if os.path.isfile(FileStorage._FileStorage__file_path):
            os.remove(FileStorage._FileStorage__file_path)

    def test_initialization(self):
        """test init of City class"""
        c = City()
        self.assertEqual(str(type(c)), "<class 'models.city.City'>")
        self.assertIsInstance(c, City)
        self.assertTrue(issubclass(type(c), BaseModel))

    def test_attributes(self):
        """tests the attibutes of City class"""
        attributes =  {
            "name": str,
            "state_id": str
        }
        o = City()
        for key, value in attributes.items():
            self.assertTrue(hasattr(o, key))
            self.assertEqual(type(getattr(o, key, None)), value)

    def test_state_id_attribute(self):
        """Test the type of state_id attribute."""
        self.assertTrue(hasattr(self.city, "state_id"))
        self.assertEqual(type(self.city.state_id), str)

    def test_name_attribute(self):
        """Test the type of name attribute."""
        self.assertTrue(hasattr(self.city, "name"))
        self.assertEqual(type(self.city.name), str)

    def test_str_method(self):
        """Test the __str__ method of City."""
        expected_str = f"[City] ({self.city.id}) {self.city.__dict__}"
        self.assertEqual(str(self.city), expected_str)

    def test_kwargs_initialization(self):
        """Test initialization with kwargs."""
        kwargs = {
            "id": "123",
            "created_at": "2023-01-01T00:00:00",
            "updated_at": "2023-01-02T00:00:00",
            "state_id": "CA",
            "name": "San Francisco"
        }
        city = City(**kwargs)
        self.assertEqual(city.id, "123")
        self.assertEqual(city.created_at, datetime.fromisoformat("2023-01-01T00:00:00"))
        self.assertEqual(city.updated_at, datetime.fromisoformat("2023-01-02T00:00:00"))
        self.assertEqual(city.state_id, "CA")
        self.assertEqual(city.name, "San Francisco")

    def test_empty_kwargs_initialization(self):
        """Test initialization with empty kwargs."""
        kwargs = {}
        city = City(**kwargs)
        self.assertIsNotNone(city.id)
        self.assertIsNotNone(city.created_at)
        self.assertIsNotNone(city.updated_at)

    def test_storage_new_called(self):
        """Test if storage.new is called during initialization."""
        city = City()
        key = f"City.{city.id}"
        self.assertIn(key, storage.all())

    def test_storage_save(self):
        """Test if storage.save is called when save method is used."""
        city = City()
        city.save()
        storage.save()
        self.assertTrue(os.path.exists(FileStorage._FileStorage__file_path))

    def test_reload(self):
        """Test if reload method works correctly."""
        city = City()
        city.save()
        storage.save()
        storage.reload()
        key = f"City.{city.id}"
        self.assertIn(key, storage.all())

if __name__ == "__main__":
    unittest.main()