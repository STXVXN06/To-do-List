"""
This module loads the environment configuration for the application.

Uses `dotenv` to load environment variables from a `.env` file.  
Defines the database configuration based on the application's environment.

Variables:
    ENV (str): Specifies the application environment. Defaults to 'dev' if not set.
    DATABASE (dict): Dictionary containing the database configuration.
        - name: Name of the database.
        - engine: Database engine used.
        - user: Username for the database connection.
        - password: Password for the database connection.
        - host: Host address of the database.
        - port: Port used for the database connection.
"""

import os
from dotenv import load_dotenv

# Load environment variables from the .env file.
load_dotenv()

# Set environment to 'dev' by default if 'ENV' is not provided.
ENV = os.getenv("ENV", "dev")

if ENV == "production":
    DATABASE = {
        "name": os.getenv("MYSQL_DATABASE"),
        "engine": "peewee.MySQLDatabase",  # MySQL as the database engine
        "user": os.getenv("MYSQL_USER"),
        "password": os.getenv("MYSQL_PASSWORD"),
        "host": os.getenv("MYSQL_HOST"),
        "port": int(os.getenv("MYSQL_PORT")),
    }
else:
    DATABASE = {
        "name": os.getenv("MYSQL_DATABASE"),
        "engine": "peewee.MySQLDatabase",  # MySQL as the database engine
        "user": os.getenv("MYSQL_USER"),
        "password": os.getenv("MYSQL_PASSWORD"),
        "host": os.getenv("MYSQL_HOST"),
        "port": int(os.getenv("MYSQL_PORT")),
    }
