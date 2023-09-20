# opcua_to_mysql: Industrial Data Integration Project

## Overview

This Python project is designed for industrial data integration, allowing you to connect to a Siemens OPC UA server and store data in a MySQL server. It simplifies the process of retrieving data from industrial machines through OPC UA communication and storing it in a database for analysis and monitoring.

## Project Structure

The project is organized as follows:

- `README.md`: This documentation file.
- `requirements.txt`: List of required Python packages.
- `server/docker-compose.yml`: Docker Compose configuration for the OPC UA and MySQL servers.
- `src/`: Source code directory.
  - `example_mysql.py`: Example code for MySQL interactions.
  - `example_opcua_siemens.py`: Example code for OPC UA communication with Siemens.
  - `main.py`: Main entry point for the project.
  - `my_mysql/`: Package for MySQL operations.
  - `my_opcua/`: Package for OPC UA operations.
- `tests/`: Directory for project tests.

## Features

- **OPC UA Integration**: Seamlessly connect to a Siemens OPC UA server to collect real-time data.

- **MySQL Database**: Store collected data in a MySQL database for easy retrieval and analysis.

- **Flexible Configuration**: Customize the project to suit your specific industrial data integration needs.

## Prerequisites

Before getting started, make sure you have the following dependencies installed:

#### Python 3.x
- [OPC UA Library]([link-to-opc-ua-library](https://github.com/FreeOpcUa/opcua-asyncio))
- [MySQL Connector]([link-to-mysql-connector](https://github.com/mysql/mysql-connector-python))
- [Docker (for server setup)](https://www.docker.com/) or [MySQL Server](https://www.mysql.com/)

## Installation

1. Clone this repository:

   ```bash
   git clone https://github.com/ymtinez/opcua_to_mysql.git

2. Make sure the OPC UA server on the PLC is active before running the project.
   
3. Install the required Python packages:
   ```bash
   pip install -r requirements.txt

## Configuration
Customize the project's behavior by modifying the src/.env file and server/.env file. You can specify MySQL database credentials.

    MYSQL_ROOT_PASSWORD='root_password'
    MYSQL_DATABASE='database_name'
    MYSQL_USER='new_user_name'
    MYSQL_PASSWORD='user_password'

## Usage
1. Start the required servers using Docker Compose:
    ```bash
    cd server
    docker compose up

2. Stop the required servers using Docker Compose:
    ```bash
    cd server
    docker compose down

3. Run the project:
    ```bash
    python src/main.py

4. The program will establish a connection to the OPC UA server, retrieve data, and store it in the MySQL database.

## Contributing
We welcome contributions from the community! If you'd like to improve this project.

## Contact
For questions or support, please contact Yunieski Martinez Espinosa at [ymtinez@gmail.com].