#!/usr/bin/python3
"""This is an entry point for a command interpreter"""

import cmd
import json
import shlex
from models.base_model import BaseModel
from models.engine.file_storage import FileStorage
from models.user import User
from models.review import Review
from models.state import State
from models.place import Place
from models.city import City
from models.amenity import Amenity


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
        all_objs = FileStorage().all()
        if key not in all_objs:
            print("** no instance found **")
            return
        print(all_objs[key])

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
        elif len(args) == 1:
            print("** instance id missing **")
        else:
            all_objs = storage.all()
            for key, value in all_objs.items():
                obj_name = value.__class__.__name__
                obj_id = value.id
                if obj_name == args[0] and obj_id == args[1].strip('"'):
                    del value
                    del storage._FileStorage__objects[key]
                    storage.save()
                    return
            print("** no instance found **")

    def do_all(self, arg):
        """Prints all string representation of
           all instances based or not on the class name.
        """
        args = shlex.split(arg)
        if args and args[0] not in classes:
            print("** class doesn't exist **")
            return
        else:
            all_objs = storage.all()
            list_instances = []
            for key, value in all_objs.items():
                obj_name = value.__class__.__name__
                if obj_name == args[0]:
                    list_instances += [value.__str__()]
            print(list_instances)

    def do_update(self, arg):
        """Updates an instance based on
        the class name and id by adding or updating attribute."""
        if not arg:
            print("** class name missing **")
            return

        arg = ""
        for argv in arg.split(','):
            arg = arg + argv

        args = shlex.split(arg)

        if args[0] not in classes:
            print("** class doesn't exist **")
        elif len(args) == 1:
            print("** instance id missing **")
        else:
            all_objs = storage.all()
            for key, objc in all_objs.items():
                ob_name = objc.__class__.__name__
                ob_id = objc.id
                if ob_name == args[0] and ob_id == args[1].strip('"'):
                    if len(args) == 2:
                        print("** attribute name missing **")
                    elif len(args) == 3:
                        print("** value missing **")
                    else:
                        setattr(objc, args[2], args[3])
                        storage.save()
                    return
            print("** no instance found **")


if __name__ == '__main__':
    HBNBCommand().cmdloop()
