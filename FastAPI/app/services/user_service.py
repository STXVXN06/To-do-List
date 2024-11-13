"""
Service layer for User operations.

This module contains the business logic for managing users.
It interacts with the `UserModel` and uses the `User` model from Pydantic for data validation.
"""

from typing import Optional, List
from fastapi import HTTPException
from peewee import DoesNotExist
from config.database import UserModel, RoleModel
from models.user import UserRead
from models.role import Role
import re

class UserService:
    """Service layer for User operations."""
    
    @staticmethod
    def email_format(email: str) -> str:
        """Valida que el formato del correo sea correcto."""
        valid_chars = re.compile(r'^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$')
        if not valid_chars.match(email):
            raise ValueError("Email format is invalid")
        return email

    @staticmethod
    def create_user(email: str, password: str, role_id: int) -> UserRead:
        """
        Crear un nuevo usuario.
        """
        try:
            role_instance = RoleModel.get_by_id(role_id)
            user_instance = UserModel.create(email=email, password=password, role=role_instance)
            
            # Preparar datos para Pydantic
            user_data = user_instance.__data__.copy()
            user_data['role_id'] = role_instance.id  # Añadir role_id explícitamente
            
            # Serializar el campo 'role' correctamente
            role_data = {
                "id": role_instance.id,
                "name": role_instance.name
            }
            user_data['role'] = Role.model_validate(role_data)  # Usar el modelo Pydantic Role
            
            return UserRead.model_validate(user_data)
        except DoesNotExist:
            raise HTTPException(status_code=404, detail=f"Status:{404}, Role with id {role_id} not found")
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    @staticmethod
    def get_user_by_email_login(email: str) -> Optional[UserModel]:
        """
        Recupera el usuario completo desde la base de datos por su email.
        """
        try:
            return UserModel.get(UserModel.email == email)
        except UserModel.DoesNotExist:
            return None


    @staticmethod
    def get_user_by_email(email: str) -> Optional[UserRead]:
        """
        Obtener un usuario por su email.
        """
        try:
            user_instance = UserModel.get(UserModel.email == email)
            user_data = user_instance.__data__.copy()
            user_data['role_id'] = user_instance.role.id  # Añadir role_id explícitamente
            
            # Serializar el campo 'role' correctamente
            role_instance = user_instance.role
            role_data = {
                "id": role_instance.id,
                "name": role_instance.name
            }
            user_data['role'] = Role.model_validate(role_data)  # Usar el modelo Pydantic Role
            
            return UserRead.model_validate(user_data)
        except DoesNotExist:
            return None

    @staticmethod
    def get_user_by_id(user_id: int) -> Optional[UserRead]:
        """
        Obtener un usuario por su ID.
        """
        try:
            user_instance = UserModel.get_by_id(user_id)
            user_data = user_instance.__data__.copy()
            user_data['role_id'] = user_instance.role.id  # Añadir role_id explícitamente
            
            # Serializar el campo 'role' correctamente
            role_instance = user_instance.role
            role_data = {
                "id": role_instance.id,
                "name": role_instance.name
            }
            user_data['role'] = Role.model_validate(role_data)  # Usar el modelo Pydantic Role
            
            return UserRead.model_validate(user_data)
        except DoesNotExist:
            return None

    @staticmethod
    def update_user_status(user_id: int, is_active: bool) -> bool:
        """
        Actualiza el estado activo de un usuario.
        """
        try:
            user_instance = UserModel.get_by_id(user_id)
            user_instance.is_active = is_active
            user_instance.save()
            return True
        except DoesNotExist:
            return False
        
    @staticmethod
    def update_user(
        user_id: int,
        email: Optional[str] = None,
        password: Optional[str] = None,
        role_id: Optional[int] = None,
    ) -> Optional[UserRead]:
        """
        Actualizar un usuario existente por su ID.
        La contraseña debe venir ya hasheada desde el controlador.
        """

        # Validación inicial para evitar valores vacíos
        if email == "" or (email is not None and not email.strip()):
            raise ValueError("Email cannot be empty")
        if password == "" or (password is not None and not password.strip()):
            raise ValueError("Password cannot be empty")
        if role_id == "" or role_id == 0:
            raise ValueError("Role ID cannot be empty or zero")

        try:
            # Obtener el usuario existente
            user_instance = UserModel.get_by_id(user_id)

            # Validar y actualizar email si se proporciona
            if email:
                # Validar el formato del correo
                email = UserService.email_format(email)

                # Verificar si el email ya existe para otro usuario
                existing_user = UserModel.select().where(
                    (UserModel.email == email) & 
                    (UserModel.id != user_id)
                ).first()
                if existing_user:
                    raise ValueError("Email already registered")
                
                # Asignar el correo al usuario si es válido
                user_instance.email = email

            # Validar y actualizar la contraseña si se proporciona
            if password:
                user_instance.password = password  # Ya viene hasheada

            # Validar y actualizar el rol si se proporciona
            if role_id:
                try:
                    role_instance = RoleModel.get_by_id(role_id)
                    user_instance.role = role_instance
                except DoesNotExist:
                    raise ValueError(f"Role with id {role_id} not found")

            # Guardar los cambios solo si todas las validaciones se pasaron correctamente
            user_instance.save()

            # Recargar la instancia para asegurar que tenemos los datos más recientes
            user_instance = UserModel.get_by_id(user_id)
            
            # Crear el objeto Role para el UserRead
            role = Role(
                id=user_instance.role.id,
                name=user_instance.role.name
            )

            # Crear el UserRead con los datos actualizados
            updated_user = UserRead(
                id=user_instance.id,
                email=user_instance.email,
                role_id=user_instance.role.id,
                is_active=user_instance.is_active,
                role=role
            )

            return updated_user

        except DoesNotExist:
            raise HTTPException(status_code=404, detail=f"Status:{404}, User not found")
        except Exception as e:
            raise ValueError(str(e)) from e

    @staticmethod
    def delete_user(user_id: int) -> bool:
        """
        Eliminar un usuario por su ID.
        """
        try:
            user_instance = UserModel.get_by_id(user_id)
            user_instance.delete_instance()
            return True
        except DoesNotExist:
            return False

    @staticmethod
    def list_all_users() -> List[UserRead]:
        """
        Obtener una lista de todos los usuarios.
        """
        users = UserModel.select()
        user_list = []
        for user_instance in users:
            user_data = user_instance.__data__.copy()
            user_data['role_id'] = user_instance.role.id
            user_data['role'] = user_instance.role
            user_list.append(UserRead.model_validate(user_data))
        return user_list