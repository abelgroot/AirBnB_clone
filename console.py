#!/usr/bin/python3
"""
This module is the starting point for the airbnb console
"""

import cmd


class HBNBCommand(cmd.Cmd):
    """defines the  quit command, EOF and custom prompt"""
    prompt = "(hbnb) "
    def do_EOF(self, line):
        """exits the console"""
        return True
    def do_quit(self, line):
        """Quit command to exit the program"""
        return True
    def emptyline(self):
        """Prevents execution of the last command when an empty line is entered"""
        pass
if __name__ == '__main__':
    HBNBCommand().cmdloop()
