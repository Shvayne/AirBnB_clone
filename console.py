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
        if args[0] not in ("BaseModel", "User", "Review", "State",
                           "Place", "City", "Amenity"):
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
        if not args:
            print("** class name missing **")
            return
        if args[0] not in ("BaseModel", "User", "Review", "State",
                           "Place", "City", "Amenity"):
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
        del all_objs[key]
        FileStorage().save()

    def do_all(self, arg):
        """Prints all string representation of
           all instances based or not on the class name.
        """
        args = shlex.split(arg)
        if args and args[0] not in ("BaseModel", "User", "Review", "State",
                                    "Place", "City", "Amenity"):
            print("** class doesn't exist **")
            return
        all_objs = FileStorage().all()
        if args:
            objs = [str(obj) for key, obj in all_objs.items()
                    if key.startswith(args[0])]
        else:
            objs = [str(obj) for obj in all_objs.values()]
        print(objs)

    def do_update(self, arg):
        """Updates an instance based on
        the class name and id by adding or updating attribute."""
        args = shlex.split(arg)
        if not args:
            print("** class name missing **")
            return
        class_name = args[0]
        if class_name not in ("BaseModel", "User", "Review", "State",
                              "Place", "City", "Amenity"):
            print("** class doesn't exist **")
            return
        if len(args) < 2:
            print("** instance id missing **")
            return
        obj_id = args[1]
        key = "{}.{}".format(class_name, obj_id)
        all_objs = FileStorage().all()
        if key not in all_objs:
            print("** no instance found **")
            return
        if len(args) < 3:
            print("** attribute name missing **")
            return
        if len(args) < 4:
            print("** value missing **")
            return
        attr_name = args[2]
        attr_value_str = args[3]
        if hasattr(all_objs[key], attr_name):
            attr_value = type(getattr(all_objs[key], attr_name))
            (attr_value_str)
            setattr(all_objs[key], attr_name, attr_value)
            FileStorage().save()
        else:
            print("** attribute doesn't exist **")

    def default(self, line):
        """Handle commands with <class name>.action() format
           Supports <class name>.all() and <class name>.count().
        """
        args = line.split(".")
        if len(args) == 2:
            class_name, action = args[0], args[1]
            if class_name in classes:
                cls = eval(class_name)
                if action == "all()":
                    self.do_all(class_name)
                elif action == "count()":
                    print(storage.count(cls))
                else:
                    print(f"*** Unknown syntax: {line}")
            else:
                print(f"*** Unknown syntax: {line}")
        else:
            print(f"*** Unknown syntax: {line}")


if __name__ == "__main__":
    if len(sys.argv) > 1:
        command = ' '.join(sys.argv[1:])
        HBNBCommand().onecmd(command)
    else:
        HBNBCommand().cmdloop()
