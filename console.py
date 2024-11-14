#!/usr/bin/python3
"""Console for the AirBnB clone"""

import cmd

from models import storage
from models.amenity import Amenity
from models.base_model import BaseModel
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User

# Dictionary to map class names to class objects
classes = {
    "BaseModel": BaseModel,
    "User": User,
    "State": State,
    "City": City,
    "Amenity": Amenity,
    "Place": Place,
    "Review": Review,
}


class HBNBCommand(cmd.Cmd):
    """Command interpreter for AirBnB clone"""

    prompt = "(hbnb) "
    
    def do_create(self, arg):
        """Create a new instance of a class"""
        if not arg:
            print("** class name missing **")
            return
        if arg not in classes:
            print("** class doesn't exist **")
            return
        instance = classes[arg]()
        instance.save()
        print(instance.id)

    def do_show(self, arg):
        """Show the string representation of an instance"""
        args = arg.split()
        if len(args) == 0:
            print("** class name missing **")
            return
        if args[0] not in classes:
            print("** class doesn't exist **")
            return
        if len(args) == 1:
            print("** instance id missing **")
            return
        key = f"{args[0]}.{args[1]}"
        if key not in storage.all():
            print("** no instance found **")
            return
        print(storage.all()[key])

    def do_destroy(self, arg):
        """Delete an instance"""
        args = arg.split()
        if len(args) == 0:
            print("** class name missing **")
            return
        if args[0] not in classes:
            print("** class doesn't exist **")
            return
        if len(args) == 1:
            print("** instance id missing **")
            return
        key = f"{args[0]}.{args[1]}"
        if key not in storage.all():
            print("** no instance found **")
            return
        del storage.all()[key]
        storage.save()

    def do_all(self, arg):
        """Show all instances, or all instances of a class"""
        if arg and arg not in classes:
            print("** class doesn't exist **")
            return
        objects = [
            str(obj)
            for key, obj in storage.all().items()
            if not arg or key.startswith(arg)
        ]
        print(objects)

    def do_update(self, arg):
        """Update an instance with new attribute values"""
        args = arg.split()
        if len(args) < 1:
            print("** class name missing **")
            return
        if args[0] not in classes:
            print("** class doesn't exist **")
            return
        if len(args) < 2:
            print("** instance id missing **")
            return
        key = f"{args[0]}.{args[1]}"
        if key not in storage.all():
            print("** no instance found **")
            return
        if len(args) < 3:
            print("** attribute name missing **")
            return
        if len(args) < 4:
            print("** value missing **")
            return
        obj = storage.all()[key]
        attr_name = args[2]
        attr_value = eval(args[3])
        setattr(obj, attr_name, attr_value)
        obj.save()

    def default(self, line):
        """Handles <class name>.all(), <class name>.count() and similar syntax commands."""
        if line.endswith(".all()"):
            class_name = line.split(".")[0]
            if class_name in classes:
                self.do_all(class_name)
            else:
                print("** class doesn't exist **")
        elif line.endswith(".count()"):
            class_name = line.split(".")[0]
            if class_name in classes:
                if class_name not in classes:
                    print("** class doesn't exist **")
                    return
                count = sum(
                    1
                    for obj in storage.all().values()
                    if obj.__class__.__name__ == class_name
                )
                print(count)
            else:
                print("** class doesn't exist **")
        # Check if the command is in the format `User.destroy("id")`
        elif line.startswith('User.destroy(\"') and line.endswith('")'):
            id = line[len('User.destroy(\"'):-2]
            self.do_destroy(f"User {id}")
        else:
            print("*** Unknown syntax:", line)

    def emptyline(self):
        """Do nothing on empty line"""
        pass

    def do_quit(self, arg):
        """Exit the console"""
        return True

    def do_EOF(self, arg):
        """Exit the console"""
        print()
        return True


if __name__ == "__main__":
    HBNBCommand().cmdloop()
