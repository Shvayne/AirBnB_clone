#!/usr/bin/python3

import unittest
from unittest.mock import patch
from models.base_model import BaseModel
from datetime import datetime


class TestBaseModel(unittest.TestCase):
    """Test cases for the BaseModel class"""

    def test_init(self):
        """Test initialization of the BaseModel"""
        base_model = BaseModel()
        self.assertIsNotNone(base_model.id)
        self.assertIsInstance(base_model.created_at, datetime)
        self.assertIsInstance(base_model.updated_at, datetime)

    def test_init_with_kwargs(self):
        """test initislization with keyword arguments"""
        kwargs = {
            'id': 'test_id',
            'created_at': '2024-01-01T12:00:00',
            'updated_at': '2024-01-01T12:00:00',
            'some_attribute': 'some_value'
        }
        base_model = BaseModel(**kwargs)
        self.assertEqual(base_model.id, 'test_id')
        self.assertIsInstance(base_model.created_at, datetime)
        self.assertIsInstance(base_model.updated_at, datetime)
        self.assertEqual(base_model.some_attribute, 'some_value')

    def test_str(self):
        """Test the __str__ method of the basemodel"""
        base_model = BaseModel()
        expected_output = f"[BaseModel] ({base_model.id}) {base_model.__dict__}"
        self.assertEqual(str(base_model), expected_output)

    @patch('models.base_model.datetime', wraps=datetime)
    def test_save(self, mock_datetime):
        """Test the save method of the Basemodel"""
        base_model = BaseModel()
        mock_datetime.now.return_value = datetime(2024, 5, 18)
        base_model.save()
        self.assertEqual(base_model.updated_at, datetime(2024, 5, 18))

    def test_to_dict(self):
        """test the to_dict method of Basemodel"""
        base_model = BaseModel()
        expected_output = {
            'id': base_model.id,
            '__class__': 'BaseModel',
            'created_at': base_model.created_at.isoformat(),
            'updated_at': base_model.updated_at.isoformat()
        }
        self.assertEqual(base_model.to_dict(), expected_output)


if __name__ == '__main__':
    unittest.main()
