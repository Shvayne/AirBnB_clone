#!/usr/bin/python3

import uuid
from datetime import datetime
"""base class for all models"""


class BaseModel:
    """base class for all models"""

    def __init__(self, *args, **kwargs):
        """A constructor method initializing BaseModel
        """
        if kwargs and len(kwargs) > 0:
            for key, value in kwargs.items():
                if key == "created_at":
                    self.__dict__["created_at"] = datetime.fromisoformat(value)
                elif key == "updated_at":
                    self.__dict__["updated_at"] = datetime.fromisoformat(value)
                elif key != "__class__":
                    setattr(self, key, value)
        else:
            self.id = str(uuid.uuid4())
            self.created_at = datetime.now()
            self.updated_at = datetime.now()

    def __str__(self) -> str:
        """returns a string representation of the BaseModel
        """
        return f"[{self.__class__.__name__}] ({self.id}) {self.__dict__}"

    def save(self):
        """updates the public instance attribute updated_at
        with the current datetime
        """
        self.updated_at = datetime.now()

    def to_dict(self):
        """returns a dictionary containing all keys/values
        of __dict__ of the instance
        """
        new_dict = self.__dict__.copy()
        new_dict['__class__'] = self.__class__.__name__
        new_dict['created_at'] = self.created_at.isoformat()
        new_dict['updated_at'] = self.updated_at.isoformat()
        return new_dict
