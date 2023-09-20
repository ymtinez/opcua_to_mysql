"""Main example to connect with OPCUA Server and save data into de MySQL Server"""
import os
import asyncio
from dotenv import load_dotenv, find_dotenv
from my_opcua.my_opcua import MyOPCUA
from my_mysql.my_mysql import MySQL

load_dotenv(find_dotenv())


async def main():
    print("This app allow to read values from OPCUA-Server of SIEMENS")
    url = input("Enter the url of the server (opc.tcp://<IP_OPCUA-SERVERr>:<PORT>): ")
    # client = Client("opc.tcp://192.168.0.120:4840")
    try:
        async with MyOPCUA(url) as my_opcua:
            try:
                print(f"Connected with the OPCUA-Server: {url}")
                print(f"Listing OPCUA-Server {url}:")
                # print all databases un the server
                databases_list = await my_opcua.get_list_of_databases()
                for database in databases_list:
                    print(f" -> {database}")
                # reading the name of the database
                specific_db_name = input(
                    "Please, enter the name of the database you want to read and save: "
                )
                db_variables = await my_opcua.get_values_from_db_name(specific_db_name)
                if bool(db_variables):  # check if db_variable is not empty
                    # connecting with the database
                    my_mysql = MySQL(
                        # host_name="192.168.0.99",
                        host_name="192.168.68.133",
                        user_name=os.getenv("MYSQL_USER"),
                        user_password=os.getenv("MYSQL_PASSWORD"),
                        database_name=os.getenv("MYSQL_DATABASE"),
                    )
                    print("Connected with MySQL Server")
                    # creating the dict with all values from the specific database
                    db_variables = await my_opcua.get_values_from_db_name(
                        specific_db_name
                    )
                    if my_mysql.create_table(specific_db_name, db_variables):
                        print("Table created successfully")
                        while True:
                            # creating the dict with all values from the specific database
                            db_variables = await my_opcua.get_values_from_db_name(
                                specific_db_name
                            )
                            # inserting values into the table
                            if my_mysql.insert_into_table(specific_db_name, db_variables):
                                print(f"Info saved in the database: {db_variables}")
                            await asyncio.sleep(5)
                else:
                    print(f"Error reading database {specific_db_name}")
            finally:
                await my_opcua.client.disconnect()
    except asyncio.exceptions.CancelledError:
        print("An error occurred when we were trying to connect to the server.")
    except TimeoutError:
        print("An error occurred. Timeout Error.")
    except Exception as err:
        print("Error", err)


if __name__ == "__main__":
    asyncio.run(main())
