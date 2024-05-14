import cmd

"""a command line interpreter
"""


class HBNBCommand(cmd.Cmd):
    """Command interpreter"""

    prompt = "(hbnb) "

    def do_quit(self, arg):
        """Exit the program"""
        return True

    def do_EOF(self, arg):
        """Exit the program"""
        return True

    def emptyline(self):
        """Do nothing on an empty line"""
        pass


if __name__ == '__main__':
    HBNBCommand().cmdloop()
