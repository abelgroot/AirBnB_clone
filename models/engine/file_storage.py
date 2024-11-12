#!/usr/bin/python3
"""
This module contains FileStorage class that handles storage of objects
"""
import json
import os

from models.base_model import BaseModel


class FileStorage():
    """This class serializes instances to a JSON file and deserializes JSON file to instances"""
    #private class attributes
    __file_path__ = "file.json"
    __objects = {}

    #publc instance methods
    def all(self):
        """Returns a dict of all objects"""
        return self.__objects

    def new(self, obj):
        """sets in __objects the obj with key <obj class name>.id"""
        #Create the key using class name and id
        key = f"{obj.__class__.__name__}.{obj.id}"
        self.__objects[key] = obj
    
    def save(self):
        """"This method will convert the dictionary of objects into a JSON format and write it to the file"""
        with open(self.__file_path__, 'w') as f:
            # Create a dictionary of serialized objects
            serialized_objects = {}
            for key, value in self.__objects.items():
                self.__objects[key] = value.to_dict()
            json.dump(self.__objects, f)

#https://appflowy.com/app/77045e94-141f-45c6-b098-28dd2829835f/813e6a91-6c58-45ef-822f-ca5c4c321322
    def reload(self):
            """Deserializes the JSON file to __objects """
            try:
                if os.path.exists(self.__file_path):
                    with open(self.__file_path, 'r') as f:
                        serialised_objects = json.load(f)
                    for key, value in serialised_objects.items():
                        class_name = value['__class__']
                        # self.classes[class name] gets the BaseModel class
                        # **value unpacks the dictionary into kwargs
                        instance = self.classes[class_name](**value)
                        # Store in __objects dictionary
                        self.__objects[key] = instance
            except Exception:
                # If any error occurs, do nothing
                pass

