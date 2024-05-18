#!/usr/bin/python3
"""Unittest module for the FileStorage Class."""

import unittest
import os
import json
from models.engine.file_storage import FileStorage
from models.base_model import BaseModel
from models.user import User
from models.review import Review
from models.state import State
from models.place import Place
from models.city import City
from models.amenity import Amenity

class TestFileStorage(unittest.TestCase):
    """Test Cases for the FileStorage class."""

    def setUp(self):
        """Sets up test methods."""
        self.resetStorage()
        self.storage = FileStorage()

    def tearDown(self):
        """Tears down test methods."""
        self.resetStorage()

    def resetStorage(self):
        """Resets FileStorage data."""
        FileStorage._FileStorage__objects = {}
        if os.path.isfile(FileStorage._FileStorage__file_path):
            os.remove(FileStorage._FileStorage__file_path)

    def test_all_method(self):
        """test the all method of Filestorage"""
        self.assertEqual(self.storage.all(), {})

        base_model = BaseModel()
        self.storage.new(base_model)
        key = f"BaseModel.{base_model.id}"
        self.assertIn(key, self.storage.all())
        self.assertEqual(self.storage.all()[key], base_model)

    def test_new_method(self):
        """Test the new method of FileStorage"""
        base_model = BaseModel()
        self.storage.new(base_model)
        key = f"BaseModel.{base_model.id}"
        self.assertIn(key, self.storage.all())
        self.assertEqual(self.storage.all()[key], base_model)

    def test_save_method(self):
        """Test the save method of FileStorage."""
        base_model = BaseModel()
        self.storage.new(base_model)
        self.storage.save()
        self.assertTrue(os.path.isfile(FileStorage._FileStorage__file_path))
        with open(FileStorage._FileStorage__file_path, "r") as f:
            content = json.load(f)
            key = f"BaseModel.{base_model.id}"
            self.assertIn(key, content)
            self.assertEqual(content[key], base_model.to_dict())

    def test_reload_method(self):
        """Test the reload method of FileStorage."""
        base_model = BaseModel()
        self.storage.new(base_model)
        self.storage.save()

        self.storage.reload()
        key = f"BaseModel.{base_model.id}"
        self.assertIn(key, self.storage.all())
        self.assertIsInstance(self.storage.all()[key], BaseModel)

    def test_reload_empty_file(self):
        """Test the reload method when file is empty."""
        self.storage.save()
        self.assertTrue(os.path.isfile(FileStorage._FileStorage__file_path))
        with open(FileStorage._FileStorage__file_path, "w") as f:
            f.write("{}")
        self.storage.reload()
        self.assertEqual(self.storage.all(), {})

    def test_reload_no_file(self):
        """Test the reload method when there is no file."""
        if os.path.isfile(FileStorage._FileStorage__file_path):
            os.remove(FileStorage._FileStorage__file_path)
        self.storage.reload()
        self.assertEqual(self.storage.all(), {})

    def test_reload_invalid_file(self):
        """Test the reload method with an invalid JSON file."""
        with open(FileStorage._FileStorage__file_path, "w") as f:
            f.write("invalid json")
        with self.assertRaises(json.JSONDecodeError):
            self.storage.reload()

if __name__ == "__main__":
    unittest.main()
