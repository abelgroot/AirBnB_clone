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
        """Serializes __objects to the JSON file at __file_path"""
        with open(self.__file_path__, 'w') as f:
            # Convert each object to a dictionary representation
            json_dict = {key: obj.to_dict() for key, obj in self.__objects.items()}
            #save the dictionary representation to the json file
            json.dump(json_dict, f)


    def reload(self): # illustration: https://tinyurl.com/yjr3defa
        """Deserializes the JSON file to __objects if the file exists"""
        if os.path.exists(self.__file_path__):
            with open(self.__file_path__, 'r') as f:
                try:
                # Load the JSON data from the json file into a dictionary
                    json_dict = json.load(f)
                    for key, value in json_dict.items():
                    # Retrieve the class name of the object from its dictionary representation
                        class_name = value["__class__"]
                    # Dynamically create an instance of the class using globals()
                        obj = globals()[class_name](**value)
                    # Store the created object in __objects using the original key
                        self.__objects[key] = obj
                except json.JSONDecodeError:
                    pass
