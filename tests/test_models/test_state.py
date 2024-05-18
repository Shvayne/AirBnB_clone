#!/usr/bin/python3
"""Unittest module for the State class."""

import unittest
from models.state import State
from models.engine.file_storage import FileStorage
import os
from models import storage
from models.base_model import BaseModel
from datetime import datetime

class TestState(unittest.TestCase):
    """Test Cases for the State class."""
    def setUp(self):
            """Sets up test methods."""
            self.resetStorage()
            self.state = State()

    def tearDown(self):
        """Tears down test methods."""
        self.resetStorage()
        del self.state

    def resetStorage(self):
        """Resets FileStorage data."""
        FileStorage._FileStorage__objects = {}
        if os.path.isfile(FileStorage._FileStorage__file_path):
                os.remove(FileStorage._FileStorage__file_path)

    def test_instantiation(self):
        """Tests instantiation of State class."""
        s = State()
        self.assertEqual(str(type(s)), "<class 'models.state.State'>")
        self.assertIsInstance(s, State)
        self.assertTrue(issubclass(type(s), BaseModel))

    def test_name_attribute(self):
        """Test the type of name attribute."""
        self.assertTrue(hasattr(self.state, "name"))
        self.assertEqual(type(self.state.name), str)
        self.assertEqual(self.state.name, "")

    def test_str_method(self):
        """Test the __str__ method of State."""
        expected_str = f"[State] ({self.state.id}) {self.state.__dict__}"
        self.assertEqual(str(self.state), expected_str)

    def test_kwargs_initialization(self):
        """Test initialization with kwargs."""
        kwargs = {
                "id": "123",
                "created_at": "2023-01-01T00:00:00",
                "updated_at": "2023-01-02T00:00:00",
                "name": "California"
            }
        state = State(**kwargs)
        self.assertEqual(state.id, "123")
        self.assertEqual(state.created_at, datetime.fromisoformat("2023-01-01T00:00:00"))
        self.assertEqual(state.updated_at, datetime.fromisoformat("2023-01-02T00:00:00"))
        self.assertEqual(state.name, "California")

    def test_empty_kwargs_initialization(self):
        """Test initialization with empty kwargs."""
        kwargs = {}
        state = State(**kwargs)
        self.assertIsNotNone(state.id)
        self.assertIsNotNone(state.created_at)
        self.assertIsNotNone(state.updated_at)

    def test_storage_new_called(self):
        """Test if storage.new is called during initialization."""
        state = State()
        key = f"State.{state.id}"
        self.assertIn(key, storage.all())

    def test_storage_save(self):
        """Test if storage.save is called when save method is used."""
        state = State()
        state.save()
        storage.save()
        self.assertTrue(os.path.exists(FileStorage._FileStorage__file_path))

    def test_reload(self):
        """Test if reload method works correctly."""
        state = State()
        state.save()
        storage.save()
        storage.reload()
        key = f"State.{state.id}"
        self.assertIn(key, storage.all())


if __name__ == "__main__":
    unittest.main()