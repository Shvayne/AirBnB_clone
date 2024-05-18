#!/usr/bin/python3
"""Module for testing the console"""
import unittest
from unittest.mock import patch
from io import StringIO
from console import HBNBCommand
from models import storage
from models.base_model import BaseModel
import os


class TestHBNBCommand(unittest.TestCase):
    """tests for the console"""
    def setUp(self):
        """Set up test environment"""
        self.storage_file = "file.json"
        if os.path.isfile(self.storage_file):
            os.remove(self.storage_file)

    def tearDown(self):
        """Tear down test environment"""
        if os.path.isfile(self.storage_file):
            os.remove(self.storage_file)

    def test_create_missing_class_name(self):
        """test create command with no class name"""
        with patch('sys.stdout', new=StringIO()) as out:
            HBNBCommand().onecmd("create")
            self.assertEqual(out.getvalue().strip(), "** class name missing **")

    def test_create_invalid_class_name(self):
        """test create command with invalid class name"""
        with patch('sys.stdout', new=StringIO()) as out:
            HBNBCommand().onecmd("create MyModel")
            self.assertEqual(out.getvalue().strip(), "** class doesn't exist **")

    def test_create_valid_class_name(self):
        """Test create command with valid class name"""
        with patch('sys.stdout', new=StringIO()) as out:
            HBNBCommand().onecmd("create BaseModel")
            output = out.getvalue().strip()
            self.assertTrue(len(output) > 0)
            self.assertIn("BaseModel." + output, storage.all().keys())

    def test_show_missing_class_name(self):
        """Test show command with no class name"""
        with patch('sys.stdout', new=StringIO()) as out:
            HBNBCommand().onecmd("show")
            self.assertEqual(out.getvalue().strip(), "** class name missing **")

    def test_show_invalid_class_name(self):
        """Test show command with invalid class name"""
        with patch('sys.stdout', new=StringIO()) as out:
            HBNBCommand().onecmd("show MyModel")
            self.assertEqual(out.getvalue().strip(), "** class doesn't exist **")

    def test_show_missing_instance_id(self):
        """Test show command with no instance id"""
        with patch('sys.stdout', new=StringIO()) as out:
            HBNBCommand().onecmd("show BaseModel")
            self.assertEqual(out.getvalue().strip(), "** instance id missing **")

    def test_show_nonexistent_instance(self):
        """Test show command with nonexistent instance"""
        with patch('sys.stdout', new=StringIO()) as out:
            HBNBCommand().onecmd("show BaseModel 12345")
            self.assertEqual(out.getvalue().strip(), "** no instance found **")

    def test_show_existing_instance(self):
        """Test show command with an existing instance"""
        obj = BaseModel()
        obj.save()
        with patch('sys.stdout', new=StringIO()) as out:
            HBNBCommand().onecmd(f"show BaseModel {obj.id}")
            self.assertIn(str(obj), out.getvalue().strip())

    def test_destroy_missing_class_name(self):
        """Test destroy command with no class name"""
        with patch('sys.stdout', new=StringIO()) as out:
            HBNBCommand().onecmd("destroy")
            self.assertEqual(out.getvalue().strip(), "** class name missing **")

    def test_destroy_invalid_class_name(self):
        """Test destroy command with invalid class name"""
        with patch('sys.stdout', new=StringIO()) as out:
            HBNBCommand().onecmd("destroy MyModel")
            self.assertEqual(out.getvalue().strip(), "** class doesn't exist **")

    def test_destroy_missing_instance_id(self):
        """Test destroy command with no instance id"""
        with patch('sys.stdout', new=StringIO()) as out:
            HBNBCommand().onecmd("destroy BaseModel")
            self.assertEqual(out.getvalue().strip(), "** instance id missing **")

    def test_destroy_nonexistent_instance(self):
        """Test destroy command with nonexistent instance"""
        with patch('sys.stdout', new=StringIO()) as out:
            HBNBCommand().onecmd("destroy BaseModel 12345")
            self.assertEqual(out.getvalue().strip(), "** no instance found **")

    def test_destroy_existing_instance(self):
        """Test destroy command with an existing instance"""
        obj = BaseModel()
        obj.save()
        with patch('sys.stdout', new=StringIO()) as out:
            HBNBCommand().onecmd(f"destroy BaseModel {obj.id}")
            self.assertEqual(out.getvalue().strip(), "")
            self.assertNotIn(f"BaseModel.{obj.id}", storage.all())

    def test_all_invalid_class_name(self):
        """Test all command with invalid class name"""
        with patch('sys.stdout', new=StringIO()) as out:
            HBNBCommand().onecmd("all MyModel")
            self.assertEqual(out.getvalue().strip(), "** class doesn't exist **")

    def test_all_valid_class_name(self):
        """Test all command with valid class name"""
        obj = BaseModel()
        obj.save()
        with patch('sys.stdout', new=StringIO()) as out:
            HBNBCommand().onecmd("all BaseModel")
            self.assertIn(str(obj), out.getvalue().strip())

    def test_all_no_class_name(self):
        """Test all command with no class name"""
        obj = BaseModel()
        obj.save()
        with patch('sys.stdout', new=StringIO()) as out:
            HBNBCommand().onecmd("all")
            self.assertIn(str(obj), out.getvalue().strip())

    def test_update_missing_class_name(self):
        """Test update command with no class name"""
        with patch('sys.stdout', new=StringIO()) as out:
            HBNBCommand().onecmd("update")
            self.assertEqual(out.getvalue().strip(), "** class name missing **")

    def test_update_invalid_class_name(self):
        """Test update command with invalid class name"""
        with patch('sys.stdout', new=StringIO()) as out:
            HBNBCommand().onecmd("update MyModel")
            self.assertEqual(out.getvalue().strip(), "** class doesn't exist **")

    def test_update_missing_instance_id(self):
        """Test update command with no instance id"""
        with patch('sys.stdout', new=StringIO()) as out:
            HBNBCommand().onecmd("update BaseModel")
            self.assertEqual(out.getvalue().strip(), "** instance id missing **")

    def test_update_nonexistent_instance(self):
        """Test update command with nonexistent instance"""
        with patch('sys.stdout', new=StringIO()) as out:
            HBNBCommand().onecmd("update BaseModel 12345")
            self.assertEqual(out.getvalue().strip(), "** no instance found **")

    def test_update_missing_attribute_name(self):
        """Test update command with no attribute name"""
        obj = BaseModel()
        obj.save()
        with patch('sys.stdout', new=StringIO()) as out:
            HBNBCommand().onecmd(f"update BaseModel {obj.id}")
            self.assertEqual(out.getvalue().strip(), "** attribute name missing **")

    def test_update_missing_value(self):
        """Test update command with no value"""
        obj = BaseModel()
        obj.save()
        with patch('sys.stdout', new=StringIO()) as out:
            HBNBCommand().onecmd(f"update BaseModel {obj.id} name")
            self.assertEqual(out.getvalue().strip(), "** value missing **")


if __name__ == "__main__":
    unittest.main()                                                                                   
