"""Main example to connect with OPCUA Server and save data into de MySQL Server"""
import time
import os
from dotenv import load_dotenv, find_dotenv
from my_opcua.my_opcua import MyOPCUA
from my_mysql.my_mysql import MySQL

load_dotenv(find_dotenv())

print("This app allow to read values from OPCUA-Server of SIEMENS")
URL = input("Enter the url of the server (opc.tcp://<IP_OPCUA-SERVERr>:<PORT>): ")
# client = Client("opc.tcp://192.168.0.120:4840")
my_opcua = MyOPCUA(URL)

try:
    my_opcua.client.connect()
    # print(f"Connected with the OPCUA-Server:")
    print(f"Connected with the OPCUA-Server: {URL}")
    print("List of values in the OPCUA-Server:")
    # print all databases un the server
    databases_list = my_opcua.list_all_databases()
    for database in databases_list:
        print(f" -> {database}")
    # reading the name of the database
    specific_db_name = input(
        "Please, enter the name of the database you want to read and save: "
    )
    # getting the node_id of database's name
    specific_db_node_id = my_opcua.get_specific_db_node_id(specific_db_name)
    if specific_db_node_id == "":
        print(f"Error reading database {specific_db_name}")
    else:
        # connecting with the database
        my_mysql = MySQL(
            host_name="192.168.0.99",
            user_name=os.getenv("MYSQL_USER"),
            user_password=os.getenv("MYSQL_PASSWORD"),
            database_name=os.getenv("MYSQL_DATABASE"),
        )
        print("Connected with MySQL Server")
        # creating table
        db_var_types = my_opcua.get_db_variables_type(specific_db_node_id)
        if my_mysql.create_table(specific_db_name, db_var_types):
            print("Table created successfully")
            while True:
                # creating the dict with all values from the specific database
                db_variables = my_opcua.get_all_db_values(specific_db_node_id)
                # inserting values into the table
                if my_mysql.insert_into_table(specific_db_name, db_variables):
                    print(f"Info saved in the database: {db_variables}")
                time.sleep(5)
finally:
    my_opcua.client.disconnect()
