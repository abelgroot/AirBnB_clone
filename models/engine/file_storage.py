#!/usr/bin/python3
"""FileStorage module for handling file serialization and deserialization"""

import json
import os

from models.amenity import Amenity
from models.base_model import BaseModel
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User


class FileStorage:
    """Serializes instances to a JSON file and
    deserializes back to instances"""

    __file_path = "file.json"
    __objects = {}

    # Map class names to class objects for easy lookup
    classes = {
        "BaseModel": BaseModel,
        "User": User,
        "State": State,
        "City": City,
        "Amenity": Amenity,
        "Place": Place,
        "Review": Review,
    }

    def all(self):
        """Returns the dictionary of all objects"""
        return self.__objects

    def new(self, obj):
        """Sets in __objects the obj with key <obj class name>.id"""
        if obj:
            key = f"{obj.__class__.__name__}.{obj.id}"
            self.__objects[key] = obj

    def save(self):
        """Serializes __objects to the JSON file"""
        obj_dict = {k: v.to_dict() for k, v in self.__objects.items()}
        with open(self.__file_path, "w") as f:
            json.dump(obj_dict, f)

    def reload(self):
        """Deserializes the JSON file to __objects,
        if the file exists and is not empty.
        If the file doesn't exist, it creates an empty one."""
        try:
            # Check if the file exists and is not empty
            if (
                os.path.exists(self.__file_path)
                and os.path.getsize(self.__file_path) > 0
            ):
                with open(self.__file_path, "r") as f:
                    obj_dict = json.load(f)
                    for key, value in obj_dict.items():
                        class_name = value["__class__"]
                        if class_name in self.classes:
                            self.__objects[key] =\
                                    self.classes[class_name](**value)
            else:
                # Create the file if it doesn't exist or is empty
                with open(self.__file_path, "w") as f:
                    pass
        except json.JSONDecodeError:
            """Handle case where file exists but
            contains invalid JSON (corrupted or empty)
            """
            print(
                "Invalid or empty JSON file. \
                        Continuing with an empty object dictionary."
            )
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
