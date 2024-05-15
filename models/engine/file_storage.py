#!/usr/bin/python3
"""this module contains a class file_storage"""
import json
import os
import datetime

class FileStorage:
    """serializes instances to a json file and deserializes JSON file to instances"""
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
            obj_dict = obj.to_dict()
            objects[obj_id] = obj_dict
        with open(FileStorage.__file_path, "w", encoding='utf-8') as f:
            json.dump(objects, f)

    def reload(self):
        """deserializes Json files"""
        if os.path.isFile(FileStorage.__file_path) and os.path.getsize(FileStorage.__file_path) > 0:
            with open(FileStorage.__file_path, "r", encoding="utf-8") as f:
                obj_dict = json.load(f)
