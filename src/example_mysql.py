"""Example testing MySQL class"""
import os
from dotenv import load_dotenv, find_dotenv
from my_mysql.my_mysql import MySQL

load_dotenv(find_dotenv())

my_mysql = MySQL(
    host_name="192.168.0.99",
    user_name=os.getenv("MYSQL_USER"),
    user_password=os.getenv("MYSQL_PASSWORD"),
    database_name=os.getenv("MYSQL_DATABASE"),
)

variables = {"temp": 236.8, "visc": 13.7, "system_Start": True, "hours": 10}

# print(my_mysql.get_create_table_cmd("HTU", variables))
if my_mysql.create_table("HTU", variables):
    print("Table created successfully")
else:
    print("Error")

# print(my_mysql.get_insert_into_cmd("HTU", variables))
if my_mysql.insert_into_table("HTU", variables):
    print(f"Variables inserted into table: {variables}")
else:
    print("Error")
