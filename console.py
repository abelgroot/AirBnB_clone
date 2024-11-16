#!/usr/bin/python3
"""
a command interpreter program for the HBNB clone Project
"""

import cmd

from models import storage
from models.amenity import Amenity
from models.base_model import BaseModel
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User


class HBNBCommand(cmd.Cmd):
    """Command interpreter for the HBNB clone."""

    prompt = "(hbnb) "
    classes = {
        "BaseModel": BaseModel,
        "User": User,
        "State": State,
        "City": City,
        "Amenity": Amenity,
        "Place": Place,
        "Review": Review,
    }

    def do_quit(self, arg):
        """Quit command to exit the program."""
        return True

    def do_EOF(self, arg):
        """Handle EOF to exit the program."""
        print()
        return True

    def emptyline(self):
        """Do nothing on an empty line."""
        pass

    def do_create(self, arg):
        """Create a new instance of a class.
        Syntax: create <class_name>
        """
        if not arg:
            print("** class name missing **")
            return
        if arg not in self.classes:
            print("** class doesn't exist **")
            return

        new_instance = self.classes[arg]()
        new_instance.save()
        print(new_instance.id)

    def do_show(self, arg):
        """
        Show the string representation of an instance of a class.
        Syntax:
        - show <class_name.id> → Display a specific instance by ID.
        """
        args = arg.split()

        if len(args) == 0:
            print("** class name missing **")
            return

        class_name = args[0]
        if class_name not in self.classes:
            print("** class doesn't exist **")
            return

        if len(args) == 1:
            print("** instance id missing **")
            return

        # Show specific instance by ID
        if len(args) == 2:
            instance_id = args[1]
            key = f"{class_name}.{instance_id}"
            if key in storage.all():
                print(storage.all()[key])
            else:
                print("** no instance found **")

    def do_destroy(self, arg):
        """Delete an instance of a class.
        Syntax: destroy <class_name> <id>
        """
        args = arg.split()

        if len(args) == 0:
            print("** class name missing **")
            return

        class_name = args[0]
        if class_name not in self.classes:
            print("** class doesn't exist **")
            return

        if len(args) == 1:
            print("** instance id missing **")
            return

        instance_id = args[1]
        key = f"{class_name}.{instance_id}"
        if key in storage.all():
            del storage.all()[key]
            storage.save()
        else:
            print("** no instance found **")

    def do_all(self, arg):
        """Show all instances or all instances of a class.
        Syntax: all or all <class_name>
        """
        if arg and arg not in self.classes:
            print("** class doesn't exist **")
            return

        instances = [
            str(obj)
            for key, obj in storage.all().items()
            if not arg or key.startswith(arg + ".")
        ]
        print(instances)

    def do_update(self, arg):
        """Update an instance's attribute.
        Syntax: update <class_name> <id> <attribute_name> <attribute_value>
        """
        args = arg.split()

        if len(args) == 0:
            print("** class name missing **")
            return

        class_name = args[0]
        if class_name not in self.classes:
            print("** class doesn't exist **")
            return

        if len(args) == 1:
            print("** instance id missing **")
            return

        instance_id = args[1]
        key = f"{class_name}.{instance_id}"
        if key not in storage.all():
            print("** no instance found **")
            return

        if len(args) == 2:
            print("** attribute name missing **")
            return

        if len(args) == 3:
            print("** value missing **")
            return

        attr_name = args[2]
        attr_value = args[3].strip('"')

        obj = storage.all()[key]
        setattr(obj, attr_name, attr_value)
        obj.save()

    def do_count(self, class_name):
        """Count the number of instances of a class.
        Syntax: <class_name>.count()
        """
        count = 0
        for key in storage.all().keys():
            if key.startswith(class_name + "."):
                count += 1
        print(count)

    def default(self, line):
        """Handle commands in the format <class_name>.command()."""
        tokens = line.split(".")
        if len(tokens) == 2:
            class_name, method_call = tokens
            if class_name in self.classes:
                if method_call == "show()":
                    self.do_show(class_name)
                    return

                elif method_call.startswith("show("):
                    # Extract the id from show(id)
                    # instance_id = method_call[5:-1].strip('"').strip("'")
                    instance_id = method_call.strip("show(")
                    if not instance_id.startswith('"'):
                        print("** instance id wrong **")
                        return
                    elif not instance_id.endswith('")'):
                        print("** instance id wrong **")
                        return
                    instance_id = instance_id.strip('"').strip('")')
                    self.do_show(f"{class_name} {instance_id}")
                    return

                elif method_call == "all()":
                    self.do_all(class_name)
                    return

                elif method_call == "count()":
                    self.do_count(class_name)
                    return
                elif method_call.startswith("destroy("):
                    instance_id = method_call.strip("destroy(")
                    if not instance_id.startswith('"'):
                        print("** instance id wrong1 **")
                        return
                    elif not instance_id.endswith('")'):
                        print("** instance id wrong2 **")
                        return
                    instance_id = instance_id.strip('"').strip('")')
                    self.do_destroy(f"{class_name} {instance_id}")
                    return
        # If no matching command, fallback to default error
        print(f"*** Unknown syntax: {line}")

    def do_help(self, arg):
        """Display help information for commands."""
        if not arg:
            # Display general help for all commands
            print("Documented commands (type help <topic>):")
            print("========================================")
            print("EOF   - End of file (quit)")
            print("all   - Show all instances of a class")
            print("create <class_name> - Create a new instance of a class")
            print("destroy <class_name> <id> - Delete an instance of a class")
            print("help - Display this help message")
            print("quit  - Quit command to exit the program")
            print(
                "show <class_name> [id] - Show instances\
                of a class or a specific instance by id"
            )
            print(
                "update <class_name> <id> <attribute_name> <attribute_value>\
                - Update instance attributes"
            )
        else:
            # Provide detailed help for specific commands
            if arg == "show":
                print(
                    "Show the string representation of an instance or all \
                    instances of a class."
                )
                print("Syntax:")
                print(
                    "  show <class_name> → Display all instances of \
                the class."
                )
                print(
                    "  show <class_name.id> → Display a specific\
                 instance by ID."
                )
            elif arg == "create":
                print("Create a new instance of a class.")
                print("Syntax: create <class_name>")
            elif arg == "destroy":
                print("Delete an instance of a class.")
                print("Syntax: destroy <class_name> <id>")
            elif arg == "all":
                print("Display all instances of a class.")
                print("Syntax: all or all <class_name>")
            elif arg == "update":
                print("Update an instance's attribute.")
                print(
                    "Syntax: update <class_name> <id>\
                    <attribute_name> <attribute_value>"
                )
            elif arg == "count":
                print("Count the number of instances of a class.")
                print("Syntax: <class_name>.count()")
            elif arg == "quit":
                print("Quit command to exit the program")
                print("Syntax: quit")
            else:
                print(f"** No help available for {arg} **")


if __name__ == "__main__":
    HBNBCommand().cmdloop()
