import json

class FileStorage:
    """
    Class FileStorage
    Represents an abstracted storage engine.

    It serializes instances to a JSON file and deserializes
    JSON files to instances.
    """
    __file_path = 'file.json'
    __objects = {}

    def all(self):
        """Return dictionary __objects."""
        return self.__objects

    def new(self, obj):
        """Set in __objects obj with the key <obj_class_name>.id"""
        key = '{}.{}'.format(obj.__class__.__name__, obj.id)
        self.__objects[key] = obj

    def save(self):
        """Serialize __objects to JSON file __file_path."""
        object_dict = {}
        for key, obj in self.__objects.items():
            object_dict[key] = obj.to_dict()
        with open(self.__file_path, 'w') as file:
            json.dump(object_dict, file)

    def reload(self):
        """
        Deserializes the JSON file to __objects (only if the JSON file exists).
        """
        try:
            with open(self.__file_path) as file:
                serialized_content = json.load(file)
                for key, value in serialized_content.items():
                    class_name = value['__class__']
                    self.new(eval(class_name)(**value))
        except FileNotFoundError:
            pass

    def delete(self, obj=None):
        """
        Deletes obj from __objects if it's present.
        """
        if obj:
            key = '{}.{}'.format(obj.__class__.__name__, obj.id)
            if key in self.__objects:
                del self.__objects[key]

    def close(self):
        """
        Calls reload() method to deserialize objects
        and close the session.
        """
        self.reload()

