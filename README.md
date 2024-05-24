# AirBnB_clone

This project is an implementation of a simplified version of the AirBnB platform, allowing users to create, manage, and book accommodations. It includes both a command-line interface (CLI) and backend functionality to handle data storage and management.

## Command Interpreter

The command interpreter is a command-line interface (CLI) tool that allows users to interact with the AirBnB_clone project. It provides various commands for managing users, places, bookings, and more.

### How to Start

To start the command interpreter, follow these steps:
1. Clone the repository to your local machine.
2. Navigate to the project directory.
3. Run the command `./console.py` to start the CLI.

### How to Use

Once the command interpreter is running, you can use various commands to interact with the AirBnB_clone project. Here are some basic commands:

- `help`: Displays a list of available commands or provides information about a specific command.
- `create <class_name>`: Creates a new instance of the specified class.
- `show <class_name> <id>`: Displays information about the specified instance.
- `destroy <class_name> <id>`: Deletes the specified instance.
- `all [class_name]`: Displays all instances of the specified class or all instances across all classes.
- `update <class_name> <id> <attribute_name> "<new_value>"`: Updates the specified attribute of the specified instance.

### Examples

Here are some examples of how to use the command interpreter:

- To create a new user:
  ```
    (hbnb) create User
    ```

- To display information about a user:
  ```
    (hbnb) show User 1234-5678
    ```

- To update the name of a user:
  ```
    (hbnb) update User 1234-5678 name "John Doe"
    ```

- To display all instances of a class:
  ```
    (hbnb) all User
    ```


## Authors

- Ngayep Jessica
- Christiana Apinoko

For a detailed list of contributors, please refer to the [AUTHORS](AUTHORS) file.



