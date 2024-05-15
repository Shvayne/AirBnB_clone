#!/usr/bin/python3

import unittest
from unittest.mock import patch
from models.base_model import BaseModel
from datetime import datetime

class TestBaseModel(unittest.TestCase):
    """Test cases for the BaseModel class"""
    def setUp(self):
        """Set up a BaseModel instance for testing"""
        self.base_model = BaseModel()

    def test_init(self):
        """Test initialization of the BaseModel"""
        self.assertIsNotNone(self.base_model.id)
        self.assertIsInstance(self.base_model.created_at, datetime)
        self.assertIsInstance(self.base_model.updated_at, datetime)

    def test_str(self):
        """Test the __str__ method of the basemodel"""
        expected_output = f"[BaseModel] ({self.base_model.id}) {self.base_model.__dict__}"
        self.assertEqual(str(self.base_model), expected_output)

    @patch('models.base_model.datetime')
    def test_save(self, mock_datetime):
        """Test the save method of the Basemodel"""
        mock_datetime.now.return_value = datetime(2024, 5, 15)
        self.base_model.save()
        self.assertEqual(self.base_model.updated_at, datetime(2024, 5, 15))

    def test_to_dict(self):
        """test the to_dict method of Basemodel"""
        expected_output = {
            'id': self.base_model.id,
            '__class__': 'BaseModel',
            'created_at': self.base_model.created_at.isoformat(),
            'updated_at': self.base_model.updated_at.isoformat()
        }
        self.assertEqual(self.base_model.to_dict(), expected_output)

if __name__ == '__main__':
    unittest.main()
