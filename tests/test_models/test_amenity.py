#!usr/bin/python3
"""unittests for the Amenity class"""

import unittest
import os
from models.amenity import Amenity
from models.engine.file_storage import FileStorage
from models.base_model import BaseModel
from datetime import datetime
from models import storage


class TestAmenity(unittest.TestCase):
    """Test Cases for the amenity class"""

    def setUp(self):
        """setting up test methods"""
        self.resetStorage()
        self.amenity = Amenity()

    def tearDown(self):
        """Tear down the test methods"""
        self.resetStorage()
        del self.amenity

    def resetStorage(self):
        """Resets filestorage data"""
        FileStorage._FileStorage__objects = {}
        if os.path.isfile(FileStorage._FileStorage__file_path):
            os.remove(FileStorage._FileStorage__file_path)

    def test_instantiation(self):
        """test instantiation of the Amenity class"""
        entity = Amenity()
        self.assertEqual(str(type(entity)), "<class 'models.amenity.Amenity'>")
        self.assertIsInstance(entity, Amenity)
        self.assertTrue(issubclass(type(entity), BaseModel))

    def test_attributes(self):
        """tests the attributes of Amenity class"""
        attr = {
            "name": str
        }
        o = Amenity()
        for key, value in attr.items():
            self.assertTrue(hasattr(o, key))
            self.assertEqual(type(getattr(o, key, None)), value)

    def test_name_attribute(self):
        """Test the type of name attribute"""
        self.assertTrue(hasattr(self.amenity, "name"))
        self.assertEqual(type(self.amenity.name), str)
        self.assertEqual(self.amenity.name, "")

    def test_str_method(self):
        """Test the __str__ method of amenity class"""
        expected_str = f"[Amenity] ({self.amenity.id}) {self.amenity.__dict__}"
        self.assertEqual(str(self.amenity), expected_str)

    def test_to_dict_method(self):
        """test the to_dict method of Amenity"""
        amenity_dict = self.amenity.to_dict()
        self.assertIsInstance(amenity_dict, dict)
        self.assertEqual(amenity_dict["__class__"], "Amenity")
        self.assertEqual(amenity_dict["id"], self.amenity.id)
        self.assertEqual(amenity_dict["created_at"], self.amenity.created_at.isoformat())
        self.assertEqual(amenity_dict["updated_at"], self.amenity.updated_at.isoformat())

    def test_kwargs_initialization(self):
        """test init with keyword args"""
        kwargs = {
            "id": "123",
            "created_at": "2023-01-01T00:00:00",
            "updated_at": "2023-01-01T00:00:00",
            "name": "pool"
        }
        amenity = Amenity(**kwargs)
        self.assertEqual(amenity.id, "123")
        self.assertEqual(amenity.created_at, datetime.fromisoformat("2023-01-01T00:00:00"))
        self.assertEqual(amenity.updated_at, datetime.fromisoformat("2023-01-01T00:00:00"))
        self.assertEqual(amenity.name, "pool")

    def test_empty_kwargs_initialization(self):
        """test init with empty kwargs"""
        kwargs = {}
        amenity = Amenity(**kwargs)
        self.assertIsNotNone(amenity.id)
        self.assertIsNotNone(amenity.created_at)
        self.assertIsNotNone(amenity.updated_at)

    def test_storage_new_called(self):
        """Test if storage.new is called during init"""
        amenity = Amenity()
        key = f"Amenity.{amenity.id}"
        self.assertIn(key, storage.all())

    def test_storage_save(self):
        """Test if storage.save is called when save method is used."""
        amenity = Amenity()
        amenity.save()
        storage.save()
        self.assertTrue(os.path.exists(FileStorage._FileStorage__file_path))

    def test_reload(self):
        """Test if reload method works correctly."""
        amenity = Amenity()
        amenity.save()
        storage.save()
        storage.reload()
        key = f"Amenity.{amenity.id}"
        self.assertIn(key, storage.all())

if __name__ == "__main__":
    unittest.main()
