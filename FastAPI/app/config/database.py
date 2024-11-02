"""
Necessary imports to define data models using Peewee ORM.
- Model: Base class for all models.
- CharField, TextField, DateField, etc.: Database field types.
- ForeignKeyField: Defines relationships between tables.
- Check: Defines column-level constraints.
- AutoField: Auto-incrementing field used as a primary key.
- fn: Provides SQL functions like CURRENT_TIMESTAMP.
"""
from datetime import date
from dotenv import load_dotenv
from config.settings import DATABASE
from peewee import (
    MySQLDatabase, Model, CharField, TextField, DateField,
    ForeignKeyField, BooleanField, TimestampField, Check, AutoField, fn, SQL
)

# Load environment variables from the .env file
load_dotenv()

# Create a MySQL database instance using environment variables
database = MySQLDatabase(
    DATABASE["name"],
    user=DATABASE["user"],
    passwd=DATABASE["password"],
    host=DATABASE["host"],
    port=DATABASE["port"],
)

class RoleModel(Model):
    """Role table."""
    id = AutoField(primary_key=True)
    name = CharField(null=False)

    class Meta:# pylint: disable=too-few-public-methods
        """Meta information for the Role model."""
        table_name = "role"
        database = DATABASE


class StatusModel(Model):
    """Status table with constraints on the name field."""
    id = AutoField(primary_key=True)
    name = CharField(
        null=False,
        constraints=[Check(SQL('"name" IN (\'TO_DO\', \'IN_PROGRESS\', \'COMPLETED\')'))]
    )

    class Meta:# pylint: disable=too-few-public-methods
        """Meta information for the Status model."""
        table_name = "status"
        database = DATABASE


class UserModel(Model):
    """User table with a relation to Role."""
    id = AutoField(primary_key=True)
    email = CharField(unique=True, null=False)
    password = CharField(null=False)
    role = ForeignKeyField(RoleModel, backref='users', null=True, on_delete='SET NULL')

    class Meta:# pylint: disable=too-few-public-methods
        """Meta information for the User model."""
        table_name = "user"
        database = DATABASE


class TaskModel(Model):
    """Task table with relationships to User and Status."""
    id = AutoField(primary_key=True)
    title = CharField(null=False)
    description = TextField(null=True)
    date_of_creation = DateField(default=date.today, null=False)
    expiration_date = DateField(null=True)
    status = ForeignKeyField(StatusModel, backref='tasks', on_delete='CASCADE')
    user = ForeignKeyField(UserModel, backref='tasks', on_delete='CASCADE')
    is_favorite = BooleanField(default=False)

    class Meta:# pylint: disable=too-few-public-methods
        """Meta information for the Task model."""
        table_name = "task"
        database = DATABASE
        constraints = [
            Check('expiration_date IS NULL OR expiration_date >= date_of_creation')
        ]


class ChangeModel(Model):
    """Change table to log modifications in Task."""
    id = AutoField(primary_key=True)
    task = ForeignKeyField(TaskModel, backref='changes', on_delete='CASCADE')
    timestamp = TimestampField(default=fn.CURRENT_TIMESTAMP)
    field_changed = CharField(null=False)
    old_value = TextField(null=True)
    new_value = TextField(null=True)

    class Meta:# pylint: disable=too-few-public-methods
        """Meta information for the Change model."""
        table_name = "change"
        database = DATABASE
