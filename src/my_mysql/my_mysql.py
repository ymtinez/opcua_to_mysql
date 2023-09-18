"""MySQL class to handle comminication with MySQL Server, create table and insert values"""
import mysql.connector
from datetime import datetime


class MySQL:
    """
    A class for interacting with a MySQL database.

    Args:
        host_name (str): The hostname or IP address of the MySQL server.
        user_name (str): The MySQL user name for authentication.
        user_password (str): The password associated with the MySQL user.
        database_name (str): The name of the MySQL database to connect to.

    Example:
        mysql_connection = MySQL(
            host_name="localhost",
            user_name="myuser",
            user_password="mypassword",
            database_name="mydatabase"
        )
    """

    def __init__(
        self, host_name: str, user_name: str, user_password: str, database_name: str
    ) -> None:
        """
        Initialize a new instance of MySQL.

        Args:
            host_name (str): The hostname or IP address of the MySQL server.
            user_name (str): The MySQL user name for authentication.
            user_password (str): The password associated with the MySQL user.
            database_name (str): The name of the MySQL database to connect to.
        """
        self.my_db = mysql.connector.connect(
            host=host_name, user=user_name, passwd=user_password, database=database_name
        )
        self.mycursor = self.my_db.cursor()

    def get_variables_types(self, variables: dict) -> dict:
        """
        Analyzes the types of values in a dictionary and returns a new dictionary
        mapping variable names to their inferred data types.

        Args:
            variables (dict): A dictionary where keys are variable names and values
                are the variable values to be analyzed.

        Returns:
            dict: A dictionary mapping variable names to their inferred data types.
                Data types can be one of the following: "Real" (for float values),
                "Boolean" (for boolean values), "Int" (for integer values), or
                "VARCHAR(255)" (for values of other data types).

        Example:
            variables = {
                "first_name": "John",
                "last_name": "Doe",
                "age": 30,
                'height': 1.75,
                "is_manager": True
            }
            types = get_variables_types(variables)
            # Output:
            # {
            #   'first_name': 'VARCHAR(255)',
            #   'last_name': 'VARCHAR(255)',
            #   'age': 'Int',
            #   'height': 'Real'
            #   "is_manager": 'Boolean',
            # }
        """
        dict_temp = {}
        for key, value in variables.items():
            value_type = ""
            if isinstance(value, float):
                value_type = "Real"
            elif isinstance(value, bool):
                value_type = "Boolean"
            elif isinstance(value, int):
                value_type = "Int"
            else:
                value_type = "VARCHAR(255)"
            dict_temp.update({f"{key}": value_type})
        return dict_temp

    def get_create_table_cmd(self, db_name: str, variables: dict) -> str:
        """
        Generate a SQL command to create a table in a database with specified variables.

        Args:
            db_name (str): The name of the database table to be created.
            var_types (dict): A dictionary mapping variable names to their values.

        Returns:
            str: A SQL command for creating the table with the specified variables and data types.

        Example:
            db_name = "employees"
            variables = {
                "first_name": "John",
                "last_name": "Doe",
                "age": 30,
                'height': 1.75,
                "is_manager": True
            }
            sql_command = get_create_table_cmd(db_name, variables)
            # Output:
            # "CREATE TABLE IF NOT EXISTS employees (employees_id int PRIMARY KEY AUTO_INCREMENT,
            # first_name VARCHAR(255) NOT NULL, last_name VARCHAR(255) NOT NULL, age int NOT NULL,
            # height real NOT NULL, is_manager Boolean NOT NULL, created TIMESTAMP NOT NULL)"
        """
        var_types = self.get_variables_types(variables)
        table_id = f"{db_name.lower()}_id"
        variables_and_type_string = ""
        for key, value in var_types.items():
            variables_and_type_string += f", {key} {value} NOT NULL"
        return f"CREATE TABLE IF NOT EXISTS {db_name} ({table_id} int PRIMARY KEY AUTO_INCREMENT{variables_and_type_string}, created TIMESTAMP NOT NULL)"

    def create_table(self, db_name: str, variables: dict) -> bool:
        """
        Create a table in a database with specified variable types and return True if successful, False otherwise.

        Args:
            db_name (str): The name of the database table to be created.
            var_types (dict): A dictionary mapping variable names to their data types.

        Returns:
            bool: True if the table creation is successful, False otherwise.

        Example:
            db_name = "employees"
            variables = {
                "first_name": "John",
                "last_name": "Doe",
                "age": 30,
                'height': 1.75,
                "is_manager": True
            }
            success = create_table(db_name, variables)
            if success:
                print(f"Table '{db_name}' created successfully.")
            else:
                print(f"Failed to create table '{db_name}'.")
        """
        var_types = self.get_variables_types(variables)
        try:
            self.mycursor.execute(self.get_create_table_cmd(db_name, var_types))
            return True
        except mysql.connector.Error as err:
            # Handle specific database-related errors here.
            print(f"Database error: {err}")
            return False
        except Exception as err:
            # Handle other exceptions here.
            print(f"An unexpected error occurred: {err}")
            return False

    def get_insert_into_cmd(self, db_name: str, variables: dict) -> str:
        """
        Generate a SQL command to insert data into a database table.

        Args:
            db_name (str): The name of the database table where data will be inserted.
            variables (dict): A dictionary mapping variable names to their corresponding values.

        Returns:
            str: A SQL command for inserting data into the specified table.

        Example:
            db_name = "employees"
            variables = {
                "first_name": "John",
                "last_name": "Doe",
                "age": 30,
                'height': 1.75,
                "is_manager": True
            }
            sql_command = get_insert_into_cmd(db_name, variables)
            # Output:
            # "INSERT INTO employees (first_name, last_name, age, height, is_manager, created)
            # VALUES (%s, %s, %s, %s, %s, %s)"
        """
        variables_names = ", ".join(variables.keys()) + ", created"
        amount_of_variables = ("%s, " * (len(variables) + 1))[:-2]
        return f"INSERT INTO {db_name} ({variables_names}) VALUES({amount_of_variables})"

    def insert_into_table(self, db_name: str, variables: dict) -> bool:
        """
        Insert data into a database table and return True if successful, False otherwise.

        Args:
            db_name (str): The name of the database table where data will be inserted.
            variables (dict): A dictionary mapping variable names to their corresponding values.

        Returns:
            bool: True if the insertion is successful, False otherwise.

        Example:
            db_name = "employees"
            variables = {
                "first_name": "John",
                "last_name": "Doe",
                "age": 30,
                'height': 1.75,
                "is_manager": True
            }
            success = insert_into_table(db_name, variables)
            if success:
                print("Data inserted successfully.")
            else:
                print("Failed to insert data.")
        """
        try:
            sql = self.get_insert_into_cmd(db_name, variables)
            values_insert = list(variables.values())
            values_insert.append(str(datetime.now()))
            self.mycursor.execute(sql, tuple(values_insert))
            self.my_db.commit()
            return True
        except mysql.connector.Error as err:
            # Handle specific database-related errors here.
            print(f"Database error: {err}")
            return False
        except Exception as err:
            # Handle other exceptions here.
            print(f"An unexpected error occurred: {err}")
            return False
