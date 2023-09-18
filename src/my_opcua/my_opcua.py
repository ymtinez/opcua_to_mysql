"""MyOPCUA class to control communication with OPCUA Server"""
from opcua import Client


class MyOPCUA:
    """
    A class for interacting with OPC UA servers.

    Args:
        url (str): The URL of the OPC UA server to connect to.

    Example:
        client = MyOPCUA("opc.tcp://localhost:4840")
    """

    def __init__(self, url: str) -> None:
        """
        Initialize a new instance of MyOPCUA.

        Args:
            url (str): The URL of the OPC UA server to connect to.
        """
        self.client = Client(url)

    def get_input_value(self, node_id: str) -> dict:
        """
        Get the input values of a specified node and return them as a dictionary.

        Args:
            node_id (str): The ID of the node from which to retrieve the input values.

        Returns:
            dict: A dictionary containing the input values, where keys are variable names and
            values are the corresponding input values.

        Example:
            node_id_name = "pressure"
            input_values = get_input_value(node_id)
            # Output (if node value is [1.23, 4.56, 7.89]):
            # {
            #   "pressure[0]": 1.23,
            #   "pressure[1]": 4.56,
            #   "pressure[2]": 7.89
            # }
        """
        dict_temp = {}
        client_node = self.client.get_node(node_id)  # Get the node
        client_node_value = client_node.get_value()  # Read the node value
        client_node_name = str(client_node.get_browse_name())[16:-1]  # Read the node name
        if isinstance(client_node_value, list):
            for index, value in enumerate(client_node_value):
                dict_temp.update(
                    {
                        f"{client_node_name}[{index}]": value
                        if not isinstance(value, float)
                        else round(value, 2)
                    }
                )
            return dict_temp
        else:
            return {
                f"{client_node_name}": client_node_value
                if not isinstance(client_node_value, float)
                else round(client_node_value, 2)
            }

    def get_specific_db_node_id(self, db_name: str) -> str:
        """
        Get the Node ID of a specific database node by its name.

        Args:
            db_name (str): The name of the database node to retrieve.

        Returns:
            str: The Node ID of the specified database node, or an empty string if not found.

        Example:
            db_name = "MyDatabase"
            db_node_id = get_specific_db_node_id(db_name)
            # Output (if the database exists):
            # "ns=3;s=MyDatabase"
            # Output (if the database does not exist):
            # ""
        """
        data_block_global = self.client.get_node("ns=3;s=DataBlocksGlobal")
        databases = data_block_global.get_children()
        for database in databases:
            if str(database.get_browse_name())[16:-1] == db_name:
                return str(database)
        return ""

    def get_all_db_values(self, db_node_id: str) -> dict:
        """
        Get all input values from variables within a specific database node and return them as a dictionary.

        Args:
            db_node_id (str): The Node ID of the specific database node.

        Returns:
            dict: A dictionary containing all input values from variables within the database node,
            where keys are variable names and values are the corresponding input values.

        Example:
            db_node_id = "ns=3;s=MyDatabase"
            values_dict = get_all_db_values(db_node_id)
            # Output (if variables in the database have input values):
            # {
            #   "Variable1": 123,
            #   "Variable2": 45.67,
            #   "Variable3": True
            # }
            # Output (if no variables with input values are found):
            # {}
        """
        var_dict = {}
        if db_node_id != "":
            db_node = self.client.get_node(db_node_id)
            # db_name = str(db_node.get_browse_name())[16:-1]
            variables = db_node.get_children()
            for variable in variables:
                var_dict.update(self.get_input_value(variable))
        return var_dict

    def list_all_databases(self) -> list[str]:
        """
        List all database names available within the global data blocks.

        Returns:
            list[str]: A list of database names.

        Example:
            databases = list_all_databases()
            # Output:
            # ['Database1', 'Database2', 'Database3']
        """
        dbs_list = []
        data_block_global = self.client.get_node("ns=3;s=DataBlocksGlobal")
        databases = data_block_global.get_children()
        for database in databases:
            if (
                database_name := str(database.get_browse_name())[16:-1]
            ) != "Icon":  # Skip the Icon element
                dbs_list.append(database_name)
        return dbs_list
