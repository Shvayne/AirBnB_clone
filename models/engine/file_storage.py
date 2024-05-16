#!/usr/bin/python3
"""this module contains a class file_storage"""
import json
import os
import datetime
from models.base_model import BaseModel
from models.user import User


class FileStorage:
    """serializes instances to a json file
    and deserializes JSON file to instances"""
    __file_path = "file.json"
    __objects = {}

    def all(self):
        """returns __objects"""
        return FileStorage.__objects

    def new(self, obj):
        """
            sets the obj with a key in the dictionary of __objects
        Args:
            obj: the object to be added to the dictionary
        """
        key = f"{type(obj).__name__}.{obj.id}"
        FileStorage.__objects[key] = obj

    def save(self):
        """serialize objects to the json file"""
        objects = {}
        for obj_id, obj in FileStorage.__objects.items():
            objects[obj_id] = obj.to_dict()
        with open(FileStorage.__file_path, "w") as f:
            json.dump(objects, f)

    def reload(self):
        """deserializes Json files"""
        if os.path.isfile(FileStorage.__file_path) and
        os.path.getsize(FileStorage.__file_path) > 0:
            with open(FileStorage.__file_path, "r") as f:
                objects = json.load(f)
                for obj_id, obj_dict in objects.items():
                    class_name, obj_id = obj_id.split(".")
                    if class_name == "BaseModel":
                        obj = BaseModel(**obj_dict)
                    elif class_name == "User":
                        obj = User(**obj_dict)
                    FileStorage.__objects[obj_id] = obj