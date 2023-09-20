"""Example to connect with OPCUA Server in S7-1500"""
import asyncio
from my_opcua.my_opcua import MyOPCUA


async def main():
    """
    Main asynchronous function for interacting with an OPC UA server.

    This function establishes a connection to an OPC UA server, retrieves a list of databases,
    reads database variables, and provides user interaction to select and view database information.

    Args:
        None

    Returns:
        None

    Raises:
        Any exceptions that may occur during the interaction with the OPC UA server.

    Example:
        To run the main function:
        ```
        asyncio.run(main())
        ```
    """
    # url = "opc.tcp://192.168.0.120:4840"
    url = "opc.tcp://192.168.68.200:4840"
    # my_opcua = MyOPCUA(url)
    try:
        async with MyOPCUA(url) as my_opcua:
            try:
                print(f"Connected with the OPCUA-Server: {url}")
                print(f"Listing OPCUA-Server {url}:")
                # print all databases un the server
                databases_list = await my_opcua.get_list_of_databases()
                print(databases_list)
                for database in databases_list:
                    print(f" -> {database}")
                # reading the name of the database
                specific_db_name = input(
                    "Please, enter the name of the database you want to read: "
                )
                # getting the node_id of database's name
                db_variables = await my_opcua.get_values_from_db_name(specific_db_name)
                if bool(db_variables):  # check if db_variable is not empty
                    print(f"{specific_db_name} variables:")
                    for key, value in db_variables.items():
                        print(f" -> {key}: {value}")
                else:
                    print(f"Error reading database {specific_db_name}")
            except Exception as err:
                print(f"Error: {err}")
                raise err
            finally:
                print("Closing")
                await my_opcua.client.disconnect()
    except asyncio.exceptions.CancelledError:
        print("An error occurred when we were trying to connect to the server.")
    except TimeoutError:
        print("An error occurred when we were trying to connect to the server.")
    except Exception as err:
        print("Error", err)


if __name__ == "__main__":
    asyncio.run(main())
