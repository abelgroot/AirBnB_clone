#!/usr/bin/python3
"""
Console for the Airbnb clone
"""

import cmd

from models import storage
from models.base_model import BaseModel


class HBNBCommand(cmd.Cmd):
    """Command interpreter for the Airbnb clone"""

    prompt = "(hbnb) "
    classes = {"BaseModel": BaseModel}

    def do_create(self, args):
        """Creates a new instance of BaseModel, saves it, and prints the id"""
        if not args:
            print("** class name missing **")
            return
        if args not in self.classes:
            print("** class doesn't exist **")
            return
        # Create and save new instance
        instance = self.classes[args]()
        instance.save()
        print(instance.id)

    def do_show(self, args):
        """Prints the string representation of an instance based on the class name and id"""
        args = args.split()
        if len(args) < 1:
            print("** class name missing **")
            return
        if args[0] not in self.classes:
            print("** class doesn't exist **")
            return
        if len(args) < 2:
            print("** instance id missing **")
            return
        key = f"{args[0]}.{args[1]}"
        instance = storage.all().get(key)
        if instance is None:
            print("** no instance found **")
        else:
            print(instance)

    def do_destroy(self, args):
        """Deletes an instance based on the class name and id"""
        args = args.split()
        if len(args) < 1:
            print("** class name missing **")
            return
        if args[0] not in self.classes:
            print("** class doesn't exist **")
            return
        if len(args) < 2:
            print("** instance id missing **")
            return
        key = f"{args[0]}.{args[1]}"
        if key not in storage.all():
            print("** no instance found **")
        else:
            del storage.all()[key]
            storage.save()

    def do_all(self, args):
        """Prints all string representations of instances of a specified class, or all if no class is specified"""
        if args:
            if args not in self.classes:
                print("** class doesn't exist **")
                return
            # Filter and display instances of specified class
            instances = [
                str(obj) for key, obj in storage.all().items() if key.startswith(args)
            ]
        else:
            # Display all instances
            instances = [str(obj) for obj in storage.all().values()]
        print(instances)

    def do_update(self, args):
        """Updates an instance based on the class name and id by adding or updating attribute"""
        args = args.split()
        if len(args) < 1:
            print("** class name missing **")
            return
        if args[0] not in self.classes:
            print("** class doesn't exist **")
            return
        if len(args) < 2:
            print("** instance id missing **")
            return
        key = f"{args[0]}.{args[1]}"
        instance = storage.all().get(key)
        if instance is None:
            print("** no instance found **")
            return
        if len(args) < 3:
            print("** attribute name missing **")
            return
        if len(args) < 4:
            print("** value missing **")
            return
        attr_name = args[2]
        attr_value = args[3].strip('"')  # Strip quotes from value if provided
        setattr(instance, attr_name, attr_value)
        instance.save()

    def do_quit(self, args):
        """Quit command to exit the program"""
        return True

    def do_EOF(self, args):
        """EOF command to exit the program"""
        print()
        return True

    def emptyline(self):
        """Overrides the default behavior of repeating the last command when an empty line is entered"""
        pass


if __name__ == "__main__":
    HBNBCommand().cmdloop()
