"""
Service layer for User operations.

This module contains the business logic for managing users.
It interacts with the `UserModel` and uses the `User` model from Pydantic for data validation.
"""

from typing import Optional, List
from peewee import DoesNotExist
from config.database import UserModel, RoleModel
from models.user import User
from models.role import Role
class UserService:
    """Service layer for User operations."""

    @staticmethod
    def create_user(email: str, password: str, role_id: int) -> User:
        """
        Create a new user.
        """
        try:
            role_instance = RoleModel.get_by_id(role_id)
            user_instance = UserModel.create(email=email, password=password, role=role_instance)
            created_user = User.model_validate(user_instance)
            created_user.role = Role.model_validate(role_instance)
            return created_user
        except DoesNotExist as exc:
            raise ValueError(f"Role with id {role_id} not found") from exc

    @staticmethod
    def get_user_by_id(user_id: int) -> Optional[User]:
        """
        Get a user by their ID.
        """
        try:
            user_instance = UserModel.get_by_id(user_id)
            return User.model_validate(user_instance)  # Asegúrate de que `model_validate` es correcto
        except DoesNotExist:
            return None

@staticmethod
def get_user_by_email(email: str) -> Optional[User]:
    """
    Get a user by their email.
    """
    try:
        user_instance = UserModel.get(UserModel.email == email)
        
        # Convertir el usuario y su rol a diccionarios
        user_data = user_instance.__data__.copy()
        user_data['role'] = user_instance.role.__data__  # Convierte `role` a un diccionario
        
        # Validar el diccionario completo usando Pydantic
        return User.model_validate(user_data)
    except DoesNotExist:
        return None


    @staticmethod
    def update_user(
        user_id: int,
        email: Optional[str] = None,
        password: Optional[str] = None,
        role_id: Optional[int] = None,
    ) -> Optional[User]:
        """
        Update an existing user by their ID.
        """
        try:
            user_instance = UserModel.get_by_id(user_id)

            if email:
                user_instance.email = email
            if password:
                user_instance.password = password
            if role_id:
                try:
                    role_instance = RoleModel.get_by_id(role_id)
                    user_instance.role = role_instance
                except DoesNotExist as exc:
                    raise ValueError(f"Role with id {role_id} not found") from exc

            user_instance.save()
            return User.model_validate(user_instance)  # Asegúrate de que `model_validate` es correcto

        except DoesNotExist:
            return None

    @staticmethod
    def delete_user(user_id: int) -> bool:
        """
        Delete a user by their ID.
        """
        try:
            user_instance = UserModel.get_by_id(user_id)
            user_instance.delete_instance()
            return True
        except DoesNotExist:
            return False

    @staticmethod
    def list_all_users() -> List[User]:
        """
        Get a list of all users.
        """
        users = UserModel.select()
        return [User.model_validate(user) for user in users]  # Asegúrate de que `model_validate` es correcto
