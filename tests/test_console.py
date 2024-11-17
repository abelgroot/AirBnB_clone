import unittest
from unittest.mock import patch
from io import StringIO
from models.base_model import BaseModel
from models.user import User
from console import HBNBCommand
from models import storage
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review

class TestHBNBCommand(unittest.TestCase):
    """Test cases for the HBNB command interpreter."""

    def setUp(self):
        """Set up for each test."""
        self.console = HBNBCommand()
        self.classes = {
            "BaseModel": BaseModel,
            "User": User,
            "State": State,
            "City": City,
            "Amenity": Amenity,
            "Place": Place,
            "Review": Review
        }

    def tearDown(self):
        """Clean up after each test."""
        storage.all().clear()
        storage.save()

    def test_create(self):
        """Test the create command."""
        # Test create without class name
        with patch('sys.stdout', new=StringIO()) as f:
            self.console.onecmd("create")
            self.assertEqual("** class name missing **", f.getvalue().strip())

        # Test create with invalid class name
        with patch('sys.stdout', new=StringIO()) as f:
            self.console.onecmd("create InvalidClass")
            self.assertEqual("** class doesn't exist **", f.getvalue().strip())

        # Test create with valid class names
        for class_name in self.classes:
            with patch('sys.stdout', new=StringIO()) as f:
                self.console.onecmd(f"create {class_name}")
                obj_id = f.getvalue().strip()
                self.assertTrue(len(obj_id) > 0)
                key = f"{class_name}.{obj_id}"
                self.assertIn(key, storage.all())

    def test_show(self):
        """Test show command."""
        # Test show without class name
        with patch('sys.stdout', new=StringIO()) as f:
            self.console.onecmd("show")
            self.assertEqual("** class name missing **", f.getvalue().strip())

        # Test show with invalid class name
        with patch('sys.stdout', new=StringIO()) as f:
            self.console.onecmd("show InvalidClass")
            self.assertEqual("** class doesn't exist **", f.getvalue().strip())

        # Test show without instance id
        with patch('sys.stdout', new=StringIO()) as f:
            self.console.onecmd("show BaseModel")
            self.assertEqual("** instance id missing **", f.getvalue().strip())

        # Test show with valid class and invalid id
        with patch('sys.stdout', new=StringIO()) as f:
            self.console.onecmd("show BaseModel 121212")
            self.assertEqual("** no instance found **", f.getvalue().strip())

        # Test show with valid class and id
        for class_name in self.classes:
            with patch('sys.stdout', new=StringIO()) as f:
                self.console.onecmd(f"create {class_name}")
                obj_id = f.getvalue().strip()

            with patch('sys.stdout', new=StringIO()) as f:
                self.console.onecmd(f"show {class_name} {obj_id}")
                output = f.getvalue().strip()
                self.assertIn(class_name, output)
                self.assertIn(obj_id, output)

    def test_destroy(self):
        """Test destroy command."""
        # Test destroy without class name
        with patch('sys.stdout', new=StringIO()) as f:
            self.console.onecmd("destroy")
            self.assertEqual("** class name missing **", f.getvalue().strip())

        # Test destroy with invalid class name
        with patch('sys.stdout', new=StringIO()) as f:
            self.console.onecmd("destroy InvalidClass")
            self.assertEqual("** class doesn't exist **", f.getvalue().strip())

        # Test destroy without instance id
        with patch('sys.stdout', new=StringIO()) as f:
            self.console.onecmd("destroy BaseModel")
            self.assertEqual("** instance id missing **", f.getvalue().strip())

        # Test destroy with invalid instance id
        with patch('sys.stdout', new=StringIO()) as f:
            self.console.onecmd("destroy BaseModel 121212")
            self.assertEqual("** no instance found **", f.getvalue().strip())

        # Test destroy with valid class and id
        for class_name in self.classes:
            with patch('sys.stdout', new=StringIO()) as f:
                self.console.onecmd(f"create {class_name}")
                obj_id = f.getvalue().strip()

            self.console.onecmd(f"destroy {class_name} {obj_id}")
            key = f"{class_name}.{obj_id}"
            self.assertNotIn(key, storage.all())

    def test_all(self):
        """Test all command."""
        # Test all with invalid class name
        with patch('sys.stdout', new=StringIO()) as f:
            self.console.onecmd("all InvalidClass")
            self.assertEqual("** class doesn't exist **", f.getvalue().strip())

        # Create some instances
        instances = []
        for class_name in self.classes:
            with patch('sys.stdout', new=StringIO()) as f:
                self.console.onecmd(f"create {class_name}")
                instances.append(f.getvalue().strip())

        # Test all without class name
        with patch('sys.stdout', new=StringIO()) as f:
            self.console.onecmd("all")
            output = f.getvalue().strip()
            for instance_id in instances:
                self.assertIn(instance_id, output)

        # Test all with valid class name
        for class_name in self.classes:
            with patch('sys.stdout', new=StringIO()) as f:
                self.console.onecmd(f"all {class_name}")
                output = f.getvalue().strip()
                self.assertIn(class_name, output)

    def test_update(self):
        """Test update command."""
        # Test update without class name
        with patch('sys.stdout', new=StringIO()) as f:
            self.console.onecmd("update")
            self.assertEqual("** class name missing **", f.getvalue().strip())

        # Test update with invalid class name
        with patch('sys.stdout', new=StringIO()) as f:
            self.console.onecmd("update InvalidClass")
            self.assertEqual("** class doesn't exist **", f.getvalue().strip())

        # Test update without instance id
        with patch('sys.stdout', new=StringIO()) as f:
            self.console.onecmd("update BaseModel")
            self.assertEqual("** instance id missing **", f.getvalue().strip())

        # Create test instance
        with patch('sys.stdout', new=StringIO()) as f:
            self.console.onecmd("create BaseModel")
            obj_id = f.getvalue().strip()

        # Test update without attribute name
        with patch('sys.stdout', new=StringIO()) as f:
            self.console.onecmd(f"update BaseModel {obj_id}")
            self.assertEqual("** attribute name missing **", f.getvalue().strip())

        # Test update without attribute value
        with patch('sys.stdout', new=StringIO()) as f:
            self.console.onecmd(f"update BaseModel {obj_id} name")
            self.assertEqual("** value missing **", f.getvalue().strip())

        # Test update with valid inputs
        attr_name = "test_name"
        attr_value = "test_value"
        self.console.onecmd(f'update BaseModel {obj_id} {attr_name} "{attr_value}"')
        key = f"BaseModel.{obj_id}"
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
            with patch('sys.stdout', new=StringIO()) as f:
                self.console.onecmd(f"{class_name}.count()")
                count = int(f.getvalue().strip())
                self.assertEqual(count, counts[class_name])

    def test_help(self):
        """Test the help command."""
        with patch('sys.stdout', new=StringIO()) as f:
            self.console.onecmd("help show")
            output = f.getvalue().strip()
            self.assertIn("Show the string representation", output)

if __name__ == '__main__':
    unittest.main()
