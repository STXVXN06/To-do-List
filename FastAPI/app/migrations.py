"""
Necessary imports to define data models using SQLAlchemy ORM.
- Column: Defines a column in a table.
- Integer: Integer data type for columns.
- String: Variable-length string data type.
- Text: Large text data type for columns.
- Date: Date data type for columns.
- Boolean: Boolean data type for columns.
- ForeignKey: Defines a foreign key constraint.
- CheckConstraint: Adds a check constraint to a column.
- declarative_base: Base class for declarative model definitions.
- relationship: Establishes relationships between models.
- sessionmaker: Factory for creating new Session objects.
- create_engine: Creates a new SQLAlchemy Engine instance.
"""
from sqlalchemy import Column, Integer, String, Text, Date, Boolean, ForeignKey, CheckConstraint
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy import create_engine
from config.settings import DATABASE

# Base declarative class for SQLAlchemy models
Base = declarative_base()

class Role(Base):# pylint: disable=too-few-public-methods
    """Role table for storing user roles."""
    __tablename__ = "role"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50),nullable=False)

class Status(Base):# pylint: disable=too-few-public-methods
    """Status table defining the various states for tasks."""
    __tablename__ = "status"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)

    __table_args__ = (
        CheckConstraint("name IN ('TO_DO', 'IN_PROGRESS', 'COMPLETED')", name="check_status_name"),
    )

class User(Base):  # pylint: disable=too-few-public-methods
    """User table for storing user information and their associated roles."""
    __tablename__ = "user"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(100), unique=True, nullable=False)
    password = Column(String(255))  # Solo aquí se maneja hashed_password
    role_id = Column(Integer, ForeignKey('role.id'), nullable=True)
    role = relationship("Role", back_populates="users")
    is_active = Column(Boolean, default=True)


class Task(Base): # pylint: disable=too-few-public-methods
    """Task table for storing tasks with relationships to users and statuses."""
    __tablename__ = "task"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(100), nullable=False)
    description = Column(Text, nullable=True)
    date_of_creation = Column(Date, nullable=False)
    expiration_date = Column(Date, nullable=True)
    status_id = Column(Integer, ForeignKey('status.id'), nullable=False)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    is_favorite = Column(Boolean, default=False)

    status = relationship("Status", back_populates="tasks")
    user = relationship("User", back_populates="tasks")

    # Constraints for the table (comparison between columns)
    __table_args__ = (
        CheckConstraint(
            "expiration_date IS NULL OR expiration_date >= date_of_creation", 
            name="check_expiration_date"
        ),
    )

class Change(Base):# pylint: disable=too-few-public-methods
    """Change table for logging modifications to tasks."""
    __tablename__ = "change"
    id = Column(Integer, primary_key=True, index=True)
    task_id = Column(Integer, ForeignKey('task.id'), nullable=False)
    timestamp = Column(Date, nullable=False)
    field_changed = Column(String(100), nullable=False)
    old_value = Column(Text, nullable=True)
    new_value = Column(Text, nullable=True)

    task = relationship("Task", back_populates="changes")

# Configurar la base de datos
DATABASE_URL = (
    f"mysql+pymysql://{DATABASE['user']}:{DATABASE['password']}@"
    f"{DATABASE['host']}/{DATABASE['name']}"
)
engine = create_engine(DATABASE_URL)

# Crear una sesión de base de datos
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
