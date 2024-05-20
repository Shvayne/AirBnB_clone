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
        if key not in all_objs:
            print("** no instance found **")
            return
        print(all_objs)

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

    def do_all(self, arg):
        """Prints all string representation of
           all instances based or not on the class name.
        """
        args = shlex.split(arg)
        if args and args[0] not in classes:
            print("** class doesn't exist **")
            return
        cls = classes.get(arg, None)
        objects = storage.all()
        if cls:
            objects = {k: v for k, v in objects.items() if k.startswith(arg)}
        print([str(obj) for obj in objects.values()])

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

    def do_count(self, cls=None):
        """
        Count the number of instances of a given class,
        or all instances if no class is specified.
        Args:
            cls (type, optional): The class type to count instances of.
        Returns:
            int: The number of instances.
        """
        if cls:
            return sum(
                1 for obj in self.__objects.values()
                if isinstance(obj, cls)
            )
        return len(self.__objects)

    def default(self, line):
        """Handle commands with <class name>.action() format"""
        args = line.split(".")
        if len(args) == 2:
            class_name, action = args[0], args[1]
            if class_name in classes:
                cls = classes[class_name]
                if action == "all()":
                    self.do_all(class_name)
                elif action == "count()":
                    print(sum(
                            1 for key in storage.all().keys()
                            if key.startswith(class_name)))
                elif action.startswith("show(") and action.endswith(")"):
                    obj_id = action[5:-1]
                    self.do_show(f"{class_name} {obj_id}")
                elif action.startswith("destroy(") and action.endswith(")"):
                    obj_id = action[8:-1]
                    self.do_destroy(f"{class_name} {obj_id}")
                else:
                    print(f"*** Unknown syntax: {line}")
            else:
                print(f"*** Unknown syntax: {line}")
        else:
            print(f"*** Unknown syntax: {line}")


if __name__ == '__main__':
    HBNBCommand().cmdloop()
