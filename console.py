import cmd
import json
import shlex
from models.base_model import BaseModel
from models.engine.file_storage import FileStorage


class HBNBCommand(cmd.Cmd):
    """Command interpreter class"""
    prompt = "(hbnb) "

    def do_create(self, arg):
        """Create a new instance of BaseModel,
            save it (to the JSON file) and print the id.
        """
        args = shlex.split(arg)
        if not args:
            print("** class name missing **")
            return
        class_name = args[0]
        if class_name not in ("BaseModel",):
            print("** class doesn't exist **")
            return
        new_instance = BaseModel()
        new_instance.save()
        print(new_instance.id)

    def do_show(self, arg):
        """Prints the string representation of
            an instance based on the class name and id.
        """
        args = shlex.split(arg)
        if not args:
            print("** class name missing **")
            return
        class_name = args[0]
        if class_name not in ("BaseModel",):
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
        print(all_objs[key])

    def do_destroy(self, arg):
        """Deletes an instance based
           on the class name and id.
        """
        args = shlex.split(arg)
        if not args:
            print("** class name missing **")
            return
        class_name = args[0]
        if class_name not in ("BaseModel",):
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
        del all_objs[key]
        FileStorage().save()

    def do_all(self, arg):
        """Prints all string representation of
           all instances based or not on the class name.
        """
        args = shlex.split(arg)
        if args and args[0] not in ("BaseModel",):
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
        if class_name not in ("BaseModel",):
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


if __name__ == '__main__':
    HBNBCommand().cmdloop()