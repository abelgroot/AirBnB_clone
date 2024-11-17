import unittest
from unittest.mock import patch
from io import StringIO
from models.base_model import BaseModel
from models.user import User
from console import HBNBCommand
from models import storage


class TestHBNBCommand(unittest.TestCase):

    def setUp(self):
        """Set up for each test."""
        self.console = HBNBCommand()

    def test_create(self):
        """Test the create command."""
        with patch('sys.stdout', new=StringIO()) as f:
            self.console.onecmd("create User")
            output = f.getvalue().strip()
            # Check if the output is an ID (i.e., non-empty)
            self.assertTrue(output)
            # Check if storage contains the new instance
            self.assertTrue(output in storage.all())

    def test_create_class_missing(self):
        """Test create command with missing class name."""
        with patch('sys.stdout', new=StringIO()) as f:
            self.console.onecmd("create")
            output = f.getvalue().strip()
            self.assertEqual(output, "** class name missing **")

    def test_create_class_does_not_exist(self):
        """Test create command with non-existent class."""
        with patch('sys.stdout', new=StringIO()) as f:
            self.console.onecmd("create NonExistentClass")
            output = f.getvalue().strip()
            self.assertEqual(output, "** class doesn't exist **")

    def test_show(self):
        """Test the show command with valid class and id."""
        with patch('sys.stdout', new=StringIO()) as f:
            # Create a new user instance
            new_user = User()
            new_user.save()
            self.console.onecmd(f"show User {new_user.id}")
            output = f.getvalue().strip()
            self.assertIn(new_user.id, output)

    def test_show_class_missing(self):
        """Test show command with missing class name."""
        with patch('sys.stdout', new=StringIO()) as f:
            self.console.onecmd("show")
            output = f.getvalue().strip()
            self.assertEqual(output, "** class name missing **")

    def test_show_instance_id_missing(self):
        """Test show command with missing instance ID."""
        with patch('sys.stdout', new=StringIO()) as f:
            self.console.onecmd("show User")
            output = f.getvalue().strip()
            self.assertEqual(output, "** instance id missing **")

    def test_show_no_instance_found(self):
        """Test show command with a non-existent instance ID."""
        with patch('sys.stdout', new=StringIO()) as f:
            self.console.onecmd("show User 1234")
            output = f.getvalue().strip()
            self.assertEqual(output, "** no instance found **")

    def test_destroy(self):
        """Test the destroy command."""
        with patch('sys.stdout', new=StringIO()) as f:
            # Create and destroy a new user instance
            new_user = User()
            new_user.save()
            self.console.onecmd(f"destroy User {new_user.id}")
            output = f.getvalue().strip()
            self.assertEqual(output, "")
            self.assertNotIn(f"User.{new_user.id}", storage.all())

    def test_destroy_class_missing(self):
        """Test destroy command with missing class name."""
        with patch('sys.stdout', new=StringIO()) as f:
            self.console.onecmd("destroy")
            output = f.getvalue().strip()
            self.assertEqual(output, "** class name missing **")

    def test_destroy_instance_id_missing(self):
        """Test destroy command with missing instance ID."""
        with patch('sys.stdout', new=StringIO()) as f:
            self.console.onecmd("destroy User")
            output = f.getvalue().strip()
            self.assertEqual(output, "** instance id missing **")

    def test_destroy_no_instance_found(self):
        """Test destroy command with non-existent instance."""
        with patch('sys.stdout', new=StringIO()) as f:
            self.console.onecmd("destroy User 1234")
            output = f.getvalue().strip()
            self.assertEqual(output, "** no instance found **")

    def test_all(self):
        """Test the all command."""
        with patch('sys.stdout', new=StringIO()) as f:
            self.console.onecmd("all User")
            output = f.getvalue().strip()
            self.assertIn("User", output)

    def test_all_class_does_not_exist(self):
        """Test all command with non-existent class."""
        with patch('sys.stdout', new=StringIO()) as f:
            self.console.onecmd("all NonExistentClass")
            output = f.getvalue().strip()
            self.assertEqual(output, "** class doesn't exist **")

    def test_update(self):
        """Test the update command."""
        with patch('sys.stdout', new=StringIO()) as f:
            # Create a new user instance and update an attribute
            new_user = User()
            new_user.save()
            self.console.onecmd(f"update User {new_user.id} name 'Updated Name'")
            output = f.getvalue().strip()
            updated_user = storage.all()[f"User.{new_user.id}"]
            self.assertEqual(updated_user.name, 'Updated Name')

    def test_update_class_missing(self):
        """Test update command with missing class name."""
        with patch('sys.stdout', new=StringIO()) as f:
            self.console.onecmd("update")
            output = f.getvalue().strip()
            self.assertEqual(output, "** class name missing **")

    def test_update_instance_id_missing(self):
        """Test update command with missing instance ID."""
        with patch('sys.stdout', new=StringIO()) as f:
            self.console.onecmd("update User")
            output = f.getvalue().strip()
            self.assertEqual(output, "** instance id missing **")

    def test_update_attribute_name_missing(self):
        """Test update command with missing attribute name."""
        with patch('sys.stdout', new=StringIO()) as f:
            new_user = User()
            new_user.save()
            self.console.onecmd(f"update User {new_user.id}")
            output = f.getvalue().strip()
            self.assertEqual(output, "** attribute name missing **")

    def test_update_value_missing(self):
        """Test update command with missing value."""
        with patch('sys.stdout', new=StringIO()) as f:
            new_user = User()
            new_user.save()
            self.console.onecmd(f"update User {new_user.id} name")
            output = f.getvalue().strip()
            self.assertEqual(output, "** value missing **")

    def test_count(self):
        """Test the count command."""
        with patch('sys.stdout', new=StringIO()) as f:
            self.console.onecmd("User.count()")
            output = f.getvalue().strip()
            self.assertEqual(int(output), 1)  # Since we only created one user in this test

    def test_default(self):
        """Test default command for show, update, etc."""
        with patch('sys.stdout', new=StringIO()) as f:
            self.console.onecmd("User.show()")
            output = f.getvalue().strip()
            self.assertTrue(output)

    def test_help(self):
        """Test the help command."""
        with patch('sys.stdout', new=StringIO()) as f:
            self.console.onecmd("help show")
            output = f.getvalue().strip()
            self.assertIn("Show the string representation", output)


if __name__ == '__main__':
    unittest.main()
