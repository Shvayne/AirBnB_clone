#!/usr/bin/python3
"""This is an entry point for a command interpreter"""

import cmd
import json
import shlex
from models.base_model import BaseModel
from models import storage
from models.user import User
from models.review import Review
from models.state import State
from models.place import Place
from models.city import City
from models.amenity import Amenity

# Dictionary of available classes
classes = {
    "BaseModel": BaseModel,
    "User": User,
    "City": City,
    "Place": Place,
    "State": State,
    "Amenity": Amenity,
    "Review": Review
}


class HBNBCommand(cmd.Cmd):
    """Command interpreter class"""

    prompt = "(hbnb) "

    def do_quit(self, arg):
        """Quit command to exit the program"""
        return True

    def do_EOF(self, arg):
        """EOF command to exit the program (Ctrl+D)"""
        return True

    def emptyline(self):
        """Do nothing on empty line"""
        pass

    def do_create(self, arg):
        """Create a new instance of BaseModel,
            and all new classes
            save it (to the JSON file) and print the id.
        """
        if not arg:
            print("** class name missing **")
            return
        try:
            cls = eval(arg)
            if not isinstance(cls, type):
                raise NameError()
            obj = cls()
            obj.save()
            print(obj.id)
        except NameError:
            print("** class doesn't exist **")

    def do_show(self, arg):
        """Prints the string representation of
            an instance based on the class name and id.
        """
        args = shlex.split(arg)
        if not args:
            print("** class name missing **")
            return
        if args[0] not in classes:
            print("** class doesn't exist **")
            return
        if len(args) < 2:
            print("** instance id missing **")
            return
        key = f"{args[0]}.{args[1]}"
        all_objs = storage.all().get(key)
        if all_objs:
            print(all_objs)
        else:
            print("** no instance found **")

    def do_destroy(self, arg):
        """Deletes an instance based
           on the class name and id.
        """
        args = shlex.split(arg)
        if not arg:
            print("** class name missing **")
            return
        if args[0] not in classes:
            print("** class doesn't exist **")
            return
        if len(args) < 2:
            print("** instance id missing **")
            return
        key = f"{args[0]}.{args[1]}"
        if key in storage.all():
            del storage.all()[key]
            storage.save()
        else:
            print("** no instance found **")

    def do_all(self, arg):
        """Prints all string representation of
           all instances based or not on the class name.
        """
        args = shlex.split(arg)
        if args and args[0] not in classes:
            print("** class doesn't exist **")
            return
        cls = eval(arg) if arg else None
        objects = storage.all(cls)
        print([str(obj) for obj in objects.values()])

    def do_update(self, arg):
        """Updates an instance based on
        the class name and id by adding or updating attribute."""
        args = shlex.split(arg)
        if not args:
            print("** class name missing **")
            return
        if args[0] not in classes:
            print("** class doesn't exist **")
            return
        if len(args) < 2:
            print("** instance id missing **")
            return
        if len(args) < 3:
            print("** attribute name missing **")
            return
        if len(args) < 4:
            print("** value missing **")
            return
        key = f"{args[0]}.{args[1]}"
        obj = storage.all().get(key)
        if not obj:
            print("** no instance found **")
            return
        setattr(obj, args[2], args[3])
        obj.save()

    def default(self, line):
        """Handle commands with <class name>.action() format"""
        args = line.split(".")
        if len(args) == 2:
            class_name, action = args[0], args[1]
            if class_name in globals():
                cls = eval(class_name)
                if action == "all()":
                    self.do_all(class_name)
                elif action == "count()":
                    print(storage.count(cls))
                elif action.startswith("show"):
                    instance_id = action[action.find("(")+1:action.find(")")]
                    self.do_show("(" + class_name
                                 + instance_id.replace('\"', '') + ")")
                elif action.startswith("destroy"):
                    instance_id = action[action.find("(")+1:action.find(")")]
                    self.do_destroy("(" + class_name
                                    + instance_id.replace('\"', '') + ")")
                else:
                    print(f"*** Unknown syntax: {line}")
            else:
                print(f"*** Unknown syntax: {line}")
        else:
            print(f"*** Unknown syntax: {line}")


if __name__ == '__main__':
    HBNBCommand().cmdloop()
