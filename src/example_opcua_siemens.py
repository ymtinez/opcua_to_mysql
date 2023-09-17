"""Example to connect with OPCUA Server in S7-1500"""
from my_opcua.my_opcua import MyOPCUA

URL = "opc.tcp://192.168.0.120:4840"
my_opcua = MyOPCUA(URL)

try:
    my_opcua.client.connect()
    # print(f"Connected with the OPCUA-Server:")
    print(f"Connected with the OPCUA-Server: {URL}")
    print(f"Listing OPCUA-Server {URL}:")
    # print all databases un the server
    databases_list = my_opcua.list_all_databases()
    for database in databases_list:
        print(f" -> {database}")
    # reading the name of the database
    specific_db_name = input("Please, enter the name of the database you want to read: ")
    # getting the node_id of database's name
    specific_db_node_id = my_opcua.get_specific_db_node_id(specific_db_name)
    if specific_db_node_id == "":
        print(f"Error reading database {specific_db_name}")
    else:
        db_var_types = my_opcua.get_db_variables_type(specific_db_node_id)
        print(f"{specific_db_name} variables types:")
        for key, value in db_var_types.items():
            print(f" -> {key}: {value}")
        db_variables = my_opcua.get_all_db_values(specific_db_node_id)
        print(f"{specific_db_name} variables:")
        for key, value in db_variables.items():
            print(f" -> {key}: {value}")
except Exception as err:
    print(err)
    raise err
finally:
    my_opcua.client.disconnect()
