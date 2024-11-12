#!/usr/bin/python3
"""Unit tests for the HBNB command interpreter."""
import unittest
from io import StringIO
from unittest.mock import patch

from console import HBNBCommand
from models import storage
from models.amenity import Amenity
from models.base_model import BaseModel
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User


class TestHBNBCommand(unittest.TestCase):
    """Test cases for the HBNB command interpreter."""

    def setUp(self):
        """Set up test cases."""
        self.console = HBNBCommand()
        self.classes = {
            "BaseModel": BaseModel,
            "User": User,
            "State": State,
            "City": City,
            "Amenity": Amenity,
            "Place": Place,
            "Review": Review,
        }

    def tearDown(self):
        """Clean up after each test."""
        storage.all().clear()
        storage.save()

    def test_help_commands(self):
        """Test help command outputs."""
        with patch("sys.stdout", new=StringIO()) as f:
            self.console.onecmd("help")
            output = f.getvalue().strip()
            self.assertIn("Documented commands", output)
            self.assertIn("EOF", output)
            self.assertIn("quit", output)
            self.assertIn("create", output)
            self.assertIn("show", output)
            self.assertIn("destroy", output)
            self.assertIn("all", output)
            self.assertIn("update", output)

        # Test help for specific commands
        commands = ["show",
                    "create",
                    "destroy",
                    "all",
                    "update",
                    "count",
                    "quit"
                    ]
        for cmd in commands:
            with patch("sys.stdout", new=StringIO()) as f:
                self.console.onecmd(f"help {cmd}")
                output = f.getvalue().strip()
                self.assertNotEqual(
                        "** No help available for {cmd} **",
                        output
                        )
                self.assertTrue(len(output) > 0)

    def test_quit_and_EOF(self):
        """Test quit and EOF commands."""
        with patch("sys.stdout", new=StringIO()) as f:
            self.assertTrue(self.console.onecmd("quit"))
            self.assertTrue(self.console.onecmd("EOF"))

    def test_emptyline(self):
        """Test empty line input."""
        with patch("sys.stdout", new=StringIO()) as f:
            self.console.onecmd("")
            self.assertEqual("", f.getvalue().strip())

    def test_create(self):
        """Test create command."""
        # Test create without class name
        with patch("sys.stdout", new=StringIO()) as f:
            self.console.onecmd("create")
            self.assertEqual("** class name missing **", f.getvalue().strip())

        # Test create with invalid class name
        with patch("sys.stdout", new=StringIO()) as f:
            self.console.onecmd("create InvalidClass")
            self.assertEqual("** class doesn't exist **", f.getvalue().strip())

        # Test create with valid class names
        for class_name in self.classes:
            with patch("sys.stdout", new=StringIO()) as f:
                self.console.onecmd(f"create {class_name}")
                obj_id = f.getvalue().strip()
                self.assertTrue(len(obj_id) > 0)
                key = f"{class_name}.{obj_id}"
                self.assertIn(key, storage.all())
                # Verify storage contains the new instance
                self.assertTrue(obj_id in storage.all())

    def test_show(self):
        """Test show command."""
        # Test show without class name
        with patch("sys.stdout", new=StringIO()) as f:
            self.console.onecmd("show")
            self.assertEqual("** class name missing **", f.getvalue().strip())

        # Test show with invalid class name
        with patch("sys.stdout", new=StringIO()) as f:
            self.console.onecmd("show InvalidClass")
            self.assertEqual("** class doesn't exist **", f.getvalue().strip())

        # Test show without instance id
        with patch("sys.stdout", new=StringIO()) as f:
            self.console.onecmd("show BaseModel")
            self.assertEqual("** instance id missing **", f.getvalue().strip())

        # Test show with valid class and invalid id
        with patch("sys.stdout", new=StringIO()) as f:
            self.console.onecmd("show BaseModel 121212")
            self.assertEqual("** no instance found **", f.getvalue().strip())

        # Test show with valid class and id
        for class_name in self.classes:
            with patch("sys.stdout", new=StringIO()) as f:
                # Create a new instance
                new_instance = self.classes[class_name]()
                new_instance.save()
                self.console.onecmd(f"show {class_name} {new_instance.id}")
                output = f.getvalue().strip()
                self.assertIn(class_name, output)
                self.assertIn(new_instance.id, output)

    def test_destroy(self):
        """Test destroy command."""
        # Test destroy without class name
        with patch("sys.stdout", new=StringIO()) as f:
            self.console.onecmd("destroy")
            self.assertEqual("** class name missing **", f.getvalue().strip())

        # Test destroy with invalid class name
        with patch("sys.stdout", new=StringIO()) as f:
            self.console.onecmd("destroy InvalidClass")
            self.assertEqual("** class doesn't exist **", f.getvalue().strip())

        # Test destroy without instance id
        with patch("sys.stdout", new=StringIO()) as f:
            self.console.onecmd("destroy BaseModel")
            self.assertEqual("** instance id missing **", f.getvalue().strip())

        # Test destroy with invalid instance id
        with patch("sys.stdout", new=StringIO()) as f:
            self.console.onecmd("destroy BaseModel 121212")
            self.assertEqual("** no instance found **", f.getvalue().strip())

        # Test destroy with valid class and id
        for class_name in self.classes:
            # Create and destroy a new instance
            new_instance = self.classes[class_name]()
            new_instance.save()
            instance_id = new_instance.id
            key = f"{class_name}.{instance_id}"

            # Verify instance exists before destroy
            self.assertIn(key, storage.all())

            self.console.onecmd(f"destroy {class_name} {instance_id}")

            # Verify instance no longer exists after destroy
            self.assertNotIn(key, storage.all())

    def test_all(self):
        """Test all command."""
        # Test all with invalid class name
        with patch("sys.stdout", new=StringIO()) as f:
            self.console.onecmd("all InvalidClass")
            self.assertEqual("** class doesn't exist **", f.getvalue().strip())

        # Create some instances
        instances = []
        for class_name in self.classes:
            with patch("sys.stdout", new=StringIO()) as f:
                self.console.onecmd(f"create {class_name}")
                instances.append(f.getvalue().strip())

        # Test all without class name
        with patch("sys.stdout", new=StringIO()) as f:
            self.console.onecmd("all")
            output = f.getvalue().strip()
            for instance_id in instances:
                self.assertIn(instance_id, output)

        # Test all with valid class name
        for class_name in self.classes:
            with patch("sys.stdout", new=StringIO()) as f:
                self.console.onecmd(f"all {class_name}")
                output = f.getvalue().strip()
                self.assertIn(class_name, output)

    def test_update(self):
        """Test update command."""
        # Test update without class name
        with patch("sys.stdout", new=StringIO()) as f:
            self.console.onecmd("update")
            self.assertEqual("** class name missing **", f.getvalue().strip())

        # Test update with invalid class name
        with patch("sys.stdout", new=StringIO()) as f:
            self.console.onecmd("update InvalidClass")
            self.assertEqual("** class doesn't exist **", f.getvalue().strip())

        # Test update without instance id
        with patch("sys.stdout", new=StringIO()) as f:
            self.console.onecmd("update BaseModel")
            self.assertEqual("** instance id missing **", f.getvalue().strip())

        # Create test instance
        new_instance = BaseModel()
        new_instance.save()
        instance_id = new_instance.id

        # Test update without attribute name
        with patch("sys.stdout", new=StringIO()) as f:
            self.console.onecmd(f"update BaseModel {instance_id}")
            self.assertEqual(
                    "** attribute name missing **",
                    f.getvalue().strip()
                    )

        # Test update without attribute value
        with patch("sys.stdout", new=StringIO()) as f:
            self.console.onecmd(f"update BaseModel {instance_id} name")
            self.assertEqual("** value missing **", f.getvalue().strip())

        # Test update with valid inputs
        attr_name = "test_name"
        attr_value = "test_value"
        self.console.onecmd(
            f'update BaseModel {instance_id} {attr_name} "{attr_value}"'
        )
        key = f"BaseModel.{instance_id}"
        obj = storage.all()[key]
        self.assertEqual(getattr(obj, attr_name), attr_value)

    def test_count(self):
        """Test count command."""
        # Create multiple instances of each class
        counts = {class_name: 2 for class_name in self.classes}

        for class_name in self.classes:
            for _ in range(counts[class_name]):
                self.console.onecmd(f"create {class_name}")

        # Test count for each class
        for class_name in self.classes:
            with patch("sys.stdout", new=StringIO()) as f:
                self.console.onecmd(f"{class_name}.count()")
                count = int(f.getvalue().strip())
                self.assertEqual(count, counts[class_name])

    def test_alternative_syntax(self):
        """Test alternative command syntax (class_name.command())."""
        # Create test instance
        new_instance = BaseModel()
        new_instance.save()
        instance_id = new_instance.id

        # Test show
        with patch("sys.stdout", new=StringIO()) as f:
            self.console.onecmd(f'BaseModel.show("{instance_id}")')
            output = f.getvalue().strip()
            self.assertIn("BaseModel", output)
            self.assertIn(instance_id, output)

        # Test all
        with patch("sys.stdout", new=StringIO()) as f:
            self.console.onecmd("BaseModel.all()")
            output = f.getvalue().strip()
            self.assertIn("BaseModel", output)

        # Test destroy
        self.console.onecmd(f'BaseModel.destroy("{instance_id}")')
        key = f"BaseModel.{instance_id}"
        self.assertNotIn(key, storage.all())

        # Test update with dictionary
        new_user = User()
        new_user.save()
        user_id = new_user.id
        update_dict = '{"first_name": "John", "age": 89}'
        self.console.onecmd(f'User.update("{user_id}", {update_dict})')
        key = f"User.{user_id}"
        obj = storage.all()[key]
        self.assertEqual(obj.first_name, "John")
        self.assertEqual(obj.age, "89")


if __name__ == "__main__":
    unittest.main()
