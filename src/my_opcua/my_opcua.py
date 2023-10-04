"""MyOPCUA class to control communication with OPCUA Server"""
from asyncua import Client


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

    async def __aenter__(self):
        """
        Asynchronous context manager method for entering a context.

        This method is used to establish a connection asynchronously when entering an asynchronous context.

        Usage:
            async with MyAsyncObject() as obj:
                # Your asynchronous code here

        Returns:
            self: The instance of the object.

        Raises:
            Any exceptions that may occur during the connection process.
        """
        await self.client.connect()
        return self

    async def __aexit__(self, exc_type, exc_value, traceback):
        """
        Asynchronous context manager method for exiting a context.

        This method is used to gracefully disconnect from a resource or perform cleanup asynchronously when exiting an asynchronous context.

        Args:
            exc_type (type): The type of exception raised within the context, if any.
            exc_value (Exception): The exception object raised within the context, if any.
            traceback (Traceback): The traceback associated with the exception, if any.

        Usage:
            async with MyAsyncObject() as obj:
                # Your asynchronous code here

        Notes:
            This method is typically used in conjunction with an 'async with' statement to ensure proper cleanup.
            If an exception occurred within the context, 'exc_type', 'exc_value', and 'traceback' provide information about the exception.

        Raises:
            Any exceptions that may occur during the disconnection or cleanup process.
        """
        await self.client.disconnect()

    async def get_input_value(self, node_id: str) -> dict:
        """
        Get the input values of a specified node and return them as a dictionary.

        Args:
            node_id (str): The ID of the node from which to retrieve the input values.

        Returns:
            dict: A dictionary containing the input values, where keys are variable names and
            values are the corresponding input values.

        Example:
            node_id = "ns=3;s="Data_DB"."pressure""
            input_values = await get_input_value(node_id)
            # Output (if node value is [1.23, 4.56, 7.89]):
            # {
            #   "pressure[0]": 1.23,
            #   "pressure[1]": 4.56,
            #   "pressure[2]": 7.89
            # }
        """
        dict_temp = {}
        client_node = self.client.get_node(node_id)  # Get the node
        client_node_value = await client_node.get_value()  # Read the node value
        client_node_name = str(await client_node.read_display_name())[
            33:-2
        ]  # Read the node name
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

    async def get_specific_db_node_id(self, db_name: str) -> str:
        """
        Get the Node ID of a specific database node by its name.

        Args:
            db_name (str): The name of the database node to retrieve.

        Returns:
            str: The Node ID of the specified database node, or an empty string if not found.

        Example:
            db_name = "MyDatabase"
            db_node_id = await get_specific_db_node_id(db_name)
            # Output (if the database exists):
            # "ns=3;s=MyDatabase"
            # Output (if the database does not exist):
            # ""
        """
        data_block_global = self.client.get_node("ns=3;s=DataBlocksGlobal")
        databases = await data_block_global.get_children()
        for database in databases:
            if str(await database.read_display_name())[33:-2].lower() == db_name.lower():
                return str(database)
        return ""

    async def get_values_from_db_name(self, db_name: str) -> dict:
        """
        Get all input values from variables within a specific database node and return them as a dictionary.

        Args:
            db_name (str): The name of the database node to retrieve.

        Returns:
            dict: A dictionary containing all input values from variables within the database node,
            where keys are variable names and values are the corresponding input values.

        Example:
            db_name = "MyDatabase"
            values_dict = await get_values_from_db_name(db_name)
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
        db_node_id = await self.get_specific_db_node_id(db_name)
        if db_node_id != "":
            db_node = self.client.get_node(db_node_id)
            # db_name = str(await db_node.read_display_name())[33:-2]
            variables = await db_node.get_children()
            for variable in variables:
                var_dict.update(await self.get_input_value(variable))
        return var_dict

    async def get_values_from_db_node_id(self, db_node_id: str) -> dict:
        """
        Get all input values from variables within a specific database node and return them as a dictionary.

        Args:
            db_node_id (str): The Node ID of the specific database node.

        Returns:
            dict: A dictionary containing all input values from variables within the database node,
            where keys are variable names and values are the corresponding input values.

        Example:
            db_node_id = "ns=3;s=MyDatabase"
            values_dict = await get_values_from_db_node_id(db_node_id)
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
            variables = await db_node.get_children()
            for variable in variables:
                var_dict.update(await self.get_input_value(variable))
        return var_dict

    async def get_list_of_databases(
        self, folder_data_blocks_global_node_id: str = "ns=3;s=DataBlocksGlobal"
    ) -> list[str]:
        """
        List all database names available within the global data blocks.

        Args:
            folder_data_blocks_global_node_id (str): The NodeID of the folder containing databases.
                Defaults to "ns=3;s=DataBlocksGlobal" for SIEMENS OPC/UA-Server.

        Returns:
            list[str]: A list of database names found on "folder_data_blocks_global_node_id".

        Raises:
            Any exceptions that may occur during the retrieval of the database list.

        Example:
            databases = await my_opcua.get_list_of_databases()
            for database in databases:
                print(f"Database: {database}")
        """
        dbs_list = []
        data_block_global = self.client.get_node(folder_data_blocks_global_node_id)
        databases = await data_block_global.get_children()
        for database in databases:
            if (
                database_name := str(await database.read_display_name())[33:-2]
            ) != "Icon":  # Skip the Icon element
                dbs_list.append(database_name)
        return dbs_list
