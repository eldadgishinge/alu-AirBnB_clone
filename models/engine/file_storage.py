#!/usr/bin/python3

import json
from os.path import exists


class FileStorage:
    __file_path = "file.json"
    __objects = {}

    def all(self):
        """Returns the dictionary __objects."""
        return self.__objects

    def new(self, obj):
        """Sets in __objects the obj with key <obj class name>.id."""
        key = "{}.{}".format(obj.__class__.__name__, obj.id)
        self.__objects[key] = obj
        self.save()

    def save(self):
        """Serializes __objects to the JSON file (path: __file_path)."""
        serialized_objects = {}
        for key, obj in FileStorage.__objects.items():
            serialized_objects[key] = obj.to_dict()

        with open(FileStorage.__file_path, 'w') as file:
            json.dump(serialized_objects, file)

    def reload(self):
        """
        Deserializes the JSON file to __objects
        (only if the JSON file (__file_path) exists;
        otherwise, do nothing. If the file does not exist,
        no exception should be raised).
        """
        if exists(self.__file_path) is False:
            return

        from .known_objects import classes

        with open(FileStorage.__file_path, 'r') as file:
            data = json.load(file)
            for key, obj_data in data.items():
                class_name, obj_id = key.split('.')
                obj_class = classes[class_name]
                obj_instance = obj_class(**obj_data)
                FileStorage.__objects[key] = obj_instance
