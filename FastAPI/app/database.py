"""
Module for database configuration and models.
"""

import os
from dotenv import load_dotenv
from peewee import MySQLDatabase


# Load environment variables from the .env file
load_dotenv()

database = MySQLDatabase(
    os.getenv("MYSQL_DATABASE"),
    user=os.getenv("MYSQL_USER"),
    passwd=os.getenv("MYSQL_PASSWORD"),
    host=os.getenv("MYSQL_HOST"),
    port=int(os.getenv("MYSQL_PORT")),
)
