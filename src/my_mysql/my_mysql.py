import mysql.connector
from datetime import datetime


class MySQL:
    """Class to connect with the MySQL Server and generate command bases on specific databases"""

    def __init__(
        self, host_name: str, user_name: str, user_password: str, database_name: str
    ) -> None:
        self.my_db = mysql.connector.connect(
            host=host_name, user=user_name, passwd=user_password, database=database_name
        )
        self.mycursor = self.my_db.cursor()

    def get_create_table_cmd(self, db_name: str, var_types: dict) -> str:
        """This function return the SQL command to create and specific table into the MySQL Server based on the dictionary of variables names and respective types

        Args:
            db_name (str): database name
            var_types (dict): A dictionary with the variables names and respective types: {"var_name": "var_type"}

        Returns:
            str: SQL Command to create the respective table
        """
        table_id = f"{db_name.lower()}_ID"
        variables_and_type_string = ""
        for key, value in var_types.items():
            variables_and_type_string += f", {key} {value} NOT NULL"
        return f"CREATE TABLE IF NOT EXISTS {db_name} ({table_id} int PRIMARY KEY AUTO_INCREMENT {variables_and_type_string}, created TIMESTAMP NOT NULL)"

    def create_table(self, db_name: str, var_types: dict) -> bool:
        """This function create the table in teh MySQL Server

        Args:
            db_name (str): database name
            var_types (dict): A dictionary with the variables names and respective types: {"var_name": "var_type"}

        Returns:
            bool: True if the table was created successfully
        """
        try:
            self.mycursor.execute(self.get_create_table_cmd(db_name, var_types))
            return True
        except Exception:
            return False

    def get_insert_into_cmd(self, db_name: str, variables: dict) -> str:
        """This function return the SQL command to insert into the table based on the dictionary of variables names and respective values

        Args:
            db_name (str): database name
            variables (dict):  A dictionary with the variables names and respective values: {"var_name": "var_value"}

        Returns:
            str: SQL Command to insert into the table
        """
        variables_names = ""
        for key in variables.keys():
            variables_names += f"{key}, "
        variables_names += "created"
        amount_of_variables = ("%s, " * (len(variables) + 1))[:-1]
        return f"INSERT INTO {db_name} ({variables_names}) VALUES({amount_of_variables})"

    def insert_into_table(self, db_name: str, variables: dict) -> bool:
        """This function insert values into the specific table

        Args:
            db_name (str): database name
            variables (dict): A dictionary with the variables names and respective values: {"var_name": "var_value"}

        Returns:
            bool: True if the values were inserted successfully
        """
        try:
            values_insert = []
            for value in variables.values():
                values_insert.append(value)
            values_insert.append(str(datetime.now()))
            sql = self.get_insert_into_cmd(db_name, variables)
            self.mycursor.execute(sql, tuple(values_insert))
            self.my_db.commit()
            return True
        except Exception:
            return False
