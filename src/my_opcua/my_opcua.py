"""MyOPCUA class to control communication with OPCUA Server"""
from opcua import Client


class MyOPCUA:
    """MyOPCUA class"""

    def __init__(self, url: str) -> None:
        self.client = Client(url)

    def get_variable_type(self, node_id: str) -> str:
        """This function return the type of the specific variable from OPCUA-Server

        Args:
            node_id (string): Node identification: "ns=<namespaceIndex>;s=<stringIdentifier>"

        Returns:
            str: "Real" if Type.float, "Int" if Type.int, "Boolean" if Type.bool, "" if not exist
        """
        client_node = self.client.get_node(node_id)  # get node
        client_node_value = client_node.get_value()
        if isinstance(client_node_value, float):
            return "Real"
        elif isinstance(client_node_value, bool):
            return "Boolean"
        elif isinstance(client_node_value, int):
            return "Int"
        else:
            return ""

    def get_db_variables_type(self, db_node_id: str) -> dict:
        """This function return a dictionay with the name and respetive type of each variables into de specific database

        Args:
            db_name (str): name of the specific DataBase

        Returns:
            dict: {"var_name": "var_type"}
        """
        var_type_temp = {}
        if db_node_id != "":
            db_node = self.client.get_node(db_node_id)
            variables = db_node.get_children()
            for variable in variables:
                variable_type = self.get_variable_type(variable)
                client_node = self.client.get_node(variable)
                client_node_name = str(client_node.get_browse_name())[16:-1]
                var_type_temp.update({f"{client_node_name}": variable_type})
        return var_type_temp

    def get_input_value(self, node_id: str) -> dict:
        """This function return a dictionary with the name and respetive value of the specific variable from OPCUA-Server

        Args:
            node_id (string): Node identification: "ns=<namespaceIndex>;s=<stringIdentifier>"

        Returns:
            dict: {"var_name": "var_value"}
        """
        client_node = self.client.get_node(node_id)  # get node
        client_node_value = client_node.get_value()  # read node value
        client_node_value_type = self.get_variable_type(node_id)
        client_node_name = str(client_node.get_browse_name())[16:-1]
        return {
            f"{client_node_name}": client_node_value
            if client_node_value_type != "Real"
            else round(client_node_value, 2)
        }

    def get_specific_db_node_id(self, db_name: str) -> str:
        """This function return the node id of the specific DataBase

        Args:
            db_name (str): name of the specific DataBase

        Returns:
            str: Node identification: "ns=<namespaceIndex>;s=<stringIdentifier>"
        """
        data_block_global = self.client.get_node("ns=3;s=DataBlocksGlobal")
        databases = data_block_global.get_children()
        for database in databases:
            if str(database.get_browse_name())[16:-1] == db_name:
                return str(database)
        return ""

    def get_all_db_values(self, db_node_id: str) -> dict:
        """This function return a dictionary with the the names and respetive values of each variables into de specific database

        Args:
            db_name (str): name of the specific DataBase

        Returns:
            dict: {"var_name": "var_value"}
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
        """This function return the list of databases names in the server

        Returns:
            list[str]: list of databases names in the server
        """
        dbs_list = []
        data_block_global = self.client.get_node("ns=3;s=DataBlocksGlobal")
        databases = data_block_global.get_children()
        for database in databases:
            if (
                database_name := str(database.get_browse_name())[16:-1]
            ) != "Icon":  # Skip Icon element
                dbs_list.append(database_name)
        return dbs_list
